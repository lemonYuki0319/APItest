# -*- coding: utf-8 -*-
"""
配置工具（兼容层）

建议：
- 代码统一使用：`from config.config import get_config`
"""

from __future__ import annotations

from config.config import (  # noqa: F401
    get_admin_config,
    get_api_config,
    get_config,
    get_env_config,
    get_test_config,
)

__all__ = [
    "get_config",
    "get_env_config",
    "get_admin_config",
    "get_api_config",
    "get_test_config",
]
