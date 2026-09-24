# -*- coding: utf-8 -*-
"""
API 基础类 - 封装通用的 HTTP 请求方法

核心设计：
1. 统一请求入口 request()，集中处理：重试、日志、异常
2. 自动注入 token 到请求头
3. 支持配置化：base_url、timeout、retry_count、verify_ssl
"""

import time
from typing import Any

import requests
from requests.exceptions import RequestException

from config.config import get_config
from src.utils.logger import logger


class BaseAPI:
    """所有 API Client 的基类"""

    def __init__(self) -> None:
        # 加载配置
        self.config: dict[str, Any] = get_config()
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
        self.token: str | None = None

    # ----------------------------------------------------------------------
    # 内部工具方法
    # ----------------------------------------------------------------------

    def build_url(self, endpoint: str) -> str:
        """构建完整 URL"""
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_url}{endpoint}"

    def get_headers(self) -> dict[str, str]:
        """获取默认请求头（自动携带 token）"""
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def parse_json(self, response: requests.Response) -> dict[str, Any]:
        """解析响应为 JSON"""
        try:
            return response.json()
        except Exception:
            raise ValueError(
                f"响应不是合法 JSON: status={response.status_code}, "
                f"url={response.url}, text={response.text[:500]}"
            )

    # ----------------------------------------------------------------------
    # 核心请求方法
    # ----------------------------------------------------------------------

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
        data: Any = None,
        headers: dict[str, str] | None = None,
        stream: bool = False,
        timeout: int | float | None = None,
    ) -> dict[str, Any] | requests.Response:
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
        url = self.build_url(endpoint)
        # 合并默认请求头和自定义请求头
        merged_headers = self.get_headers()
        if headers:
            merged_headers.update(headers)
        actual_timeout = self.timeout if timeout is None else timeout
        last_exc: Exception | None = None

        for attempt in range(self.retry_count + 1):
            try:
                logger.info(f"[HTTP] {method.upper()} {url}")
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

                # 流式响应直接返回 Response 对象
                if stream:
                    return resp

                return self.parse_json(resp)

            except RequestException as e:
                last_exc = e
                logger.warning(f"[HTTP] 请求异常: {e}")
            except Exception as e:
                last_exc = e
                logger.warning(f"[HTTP] 解析/处理异常: {e}")

            # 失败重试等待（简单退避）
            if attempt < self.retry_count:
                time.sleep(0.5 * (attempt + 1))

        raise RuntimeError(
            f"请求失败（已重试 {self.retry_count} 次）: {method.upper()} {url}"
        ) from last_exc

    # ----------------------------------------------------------------------
    # 便捷方法
    # ----------------------------------------------------------------------

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """发送 GET 请求"""
        return self.request("GET", endpoint, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        json: Any = None,
        data: Any = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """发送 POST 请求"""
        return self.request("POST", endpoint, json_body=json, data=data, headers=headers)

    def put(
        self,
        endpoint: str,
        json: Any = None,
        data: Any = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """发送 PUT 请求"""
        return self.request("PUT", endpoint, json_body=json, data=data, headers=headers)

    def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """发送 DELETE 请求"""
        return self.request("DELETE", endpoint, headers=headers)
