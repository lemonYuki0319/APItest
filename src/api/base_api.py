# -*- coding: utf-8 -*-
"""
API 基础类，封装通用的 HTTP 请求方法

面向初学者的关键点：
1. timeout 必须在每次请求时传入（requests.Session 没有 session.timeout 这种全局属性）
2. 建议统一入口 request()，便于做：重试、日志、异常处理、Allure 附件、header/token 注入
3. 不要在业务 API 里到处写重复的 get/post/put/delete 逻辑
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from requests import Response
from requests.exceptions import RequestException

from config.config import get_config
from config.constants import REPORTS_DIR
from src.utils.logger import logger


class BaseAPI:
    """所有 API Client 的基类"""

    def __init__(self) -> None:
        # 统一从配置中心加载（带缓存）
        self.config: Dict[str, Any] = get_config()

        env_cfg = self.config.get("env", {})
        test_cfg = self.config.get("test", {})

        self.base_url: str = env_cfg.get("base_url", "").rstrip("/")
        self.timeout: int | float = env_cfg.get("timeout", 30)
        self.retry_count: int = int(env_cfg.get("retry_count", 0))
        self.verify_ssl: bool = bool(test_cfg.get("verify_ssl", True))

        # 创建会话
        self.session = requests.Session()
        self.session.verify = self.verify_ssl

        # token（由登录接口写入）
        self.token: Optional[str] = None

        # 响应保存目录（可选，用于排查问题）
        self.response_dir = os.path.join(REPORTS_DIR, "response")
        os.makedirs(self.response_dir, exist_ok=True)

    # ----------------------------
    # 基础能力
    # ----------------------------
    def _build_url(self, endpoint: str) -> str:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_url}{endpoint}"

    def get_headers(self) -> Dict[str, str]:
        """获取默认请求头（自动携带 token）"""
        headers: Dict[str, str] = {"Accept": "application/json, text/plain, */*"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _merge_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        merged = self.get_headers()
        if headers:
            merged.update(headers)
        return merged

    def _save_response(self, method: str, endpoint: str, response: Response) -> None:
        """保存响应信息到文件，便于定位问题（不影响测试执行）"""
        try:
            safe_endpoint = endpoint.strip("/").replace("/", "_") or "root"
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{ts}_{method.upper()}_{safe_endpoint}.json"
            path = os.path.join(self.response_dir, filename)

            payload = {
                "url": response.url,
                "method": method.upper(),
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "text": response.text,
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.debug(f"保存响应文件失败（可忽略）: {e}")

    def _parse_json(self, response: Response) -> Dict[str, Any]:
        """把 Response 解析为 dict；若不是 JSON，抛出带上下文的异常"""
        try:
            return response.json()
        except Exception:
            # 尽量带上关键上下文，方便初学者定位
            raise ValueError(
                f"响应不是合法 JSON: status={response.status_code}, url={response.url}, text={response.text[:500]}"
            )

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Any = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
        timeout: Optional[int | float] = None,
    ) -> Response | Dict[str, Any]:
        """
        统一请求入口：
        - 自动拼接 base_url
        - 自动注入 token header
        - 支持 retry_count
        - 默认返回 JSON(dict)；stream=True 时返回 Response（用于 SSE/下载等）
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)
        actual_timeout = self.timeout if timeout is None else timeout

        last_exc: Optional[Exception] = None

        for attempt in range(self.retry_count + 1):
            try:
                logger.info(
                    f"[HTTP] {method.upper()} {url} attempt={attempt + 1}/{self.retry_count + 1}"
                )
                resp = self.session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    json=json_body,
                    data=data,
                    headers=merged_headers,
                    timeout=actual_timeout,
                    stream=stream,
                )

                # 保存响应（便于排查）
                self._save_response(method, endpoint, resp)

                # 这里不强制 resp.raise_for_status()：因为很多业务用 code 字段表示业务成功与否
                if stream:
                    return resp

                return self._parse_json(resp)

            except RequestException as e:
                last_exc = e
                logger.warning(f"[HTTP] 请求异常: {e}")
            except Exception as e:
                last_exc = e
                logger.warning(f"[HTTP] 解析/处理异常: {e}")

            # 失败重试等待（简单退避）
            if attempt < self.retry_count:
                time.sleep(min(0.5 * (attempt + 1), 2.0))

        raise RuntimeError(f"请求失败（已重试 {self.retry_count} 次）: {method.upper()} {url}") from last_exc

    # ----------------------------
    # 便捷方法：保持对旧代码的兼容（返回 dict）
    # ----------------------------
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return self.request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint: str, json: Any = None, data: Any = None, headers: Optional[Dict[str, str]] = None):
        return self.request("POST", endpoint, json_body=json, data=data, headers=headers)

    def put(self, endpoint: str, json: Any = None, data: Any = None, headers: Optional[Dict[str, str]] = None):
        return self.request("PUT", endpoint, json_body=json, data=data, headers=headers)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None):
        return self.request("DELETE", endpoint, headers=headers)
