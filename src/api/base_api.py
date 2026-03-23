# -*- coding: utf-8 -*-
"""
API 基础类 - 封装通用的 HTTP 请求方法

核心设计：
1. 统一请求入口 request()，集中处理：重试、日志、异常、响应保存
2. 自动注入 token 到请求头
3. 支持配置化：base_url、timeout、retry_count、verify_ssl
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

    # =========================================================================
    # 初始化
    # =========================================================================
    
    def __init__(self) -> None:
        # 加载配置
        self.config: Dict[str, Any] = get_config()
        env_cfg = self.config.get("env", {})
        test_cfg = self.config.get("test", {})

        # 基础配置
        self.base_url: str = env_cfg.get("base_url", "").rstrip("/")
        self.timeout: int | float = env_cfg.get("timeout", 30)
        self.retry_count: int = int(env_cfg.get("retry_count", 0))
        self.verify_ssl: bool = bool(test_cfg.get("verify_ssl", True))

        # 创建会话
        self.session = requests.Session()
        self.session.verify = self.verify_ssl

        # Token（由登录接口写入）
        self.token: Optional[str] = None

        # 响应保存目录（用于排查问题）
        self.response_dir = os.path.join(REPORTS_DIR, "response")
        os.makedirs(self.response_dir, exist_ok=True)

    # =========================================================================
    # 内部工具方法
    # =========================================================================

    def _build_url(self, endpoint: str) -> str:
        """构建完整 URL"""
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_url}{endpoint}"

    def _get_headers(self) -> Dict[str, str]:
        """获取默认请求头（自动携带 token）"""
        headers: Dict[str, str] = {"Accept": "application/json, text/plain, */*"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _merge_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """合并默认请求头和自定义请求头"""
        merged = self._get_headers()
        if headers:
            merged.update(headers)
        return merged

    def _save_response(self, method: str, endpoint: str, response: Response) -> None:
        """保存响应到文件（便于排查问题）"""
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
        """解析响应为 JSON"""
        try:
            return response.json()
        except Exception:
            raise ValueError(
                f"响应不是合法 JSON: status={response.status_code}, "
                f"url={response.url}, text={response.text[:500]}"
            )

    # =========================================================================
    # 核心请求方法
    # =========================================================================

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
        统一请求入口
        
        Args:
            method: HTTP 方法 (GET/POST/PUT/DELETE)
            endpoint: API 端点路径
            params: URL 查询参数
            json_body: JSON 请求体
            data: Form 请求体
            headers: 自定义请求头
            stream: 是否流式响应（用于 SSE/下载）
            timeout: 请求超时时间（秒）
            
        Returns:
            正常返回 JSON(dict)；stream=True 时返回 Response 对象
            
        Raises:
            RuntimeError: 请求失败（包括重试后仍失败）
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)
        actual_timeout = self.timeout if timeout is None else timeout
        last_exc: Optional[Exception] = None

        for attempt in range(self.retry_count + 1):
            try:
                logger.info(
                    f"[HTTP] {method.upper()} {url} "
                    f"attempt={attempt + 1}/{self.retry_count + 1}"
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

                # 流式响应直接返回 Response 对象
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

        raise RuntimeError(
            f"请求失败（已重试 {self.retry_count} 次）: {method.upper()} {url}"
        ) from last_exc

    # =========================================================================
    # 便捷方法（保持旧代码兼容）
    # =========================================================================

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """发送 GET 请求"""
        return self.request("GET", endpoint, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        json: Any = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """发送 POST 请求"""
        return self.request("POST", endpoint, json_body=json, data=data, headers=headers)

    def put(
        self,
        endpoint: str,
        json: Any = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """发送 PUT 请求"""
        return self.request("PUT", endpoint, json_body=json, data=data, headers=headers)

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """发送 DELETE 请求"""
        return self.request("DELETE", endpoint, headers=headers)
