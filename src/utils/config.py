# -*- coding: utf-8 -*-
"""
配置工具（兼容层）

说明：
- 本项目历史上同时存在 `config/config.py` 与 `src/utils/config.py` 两份重复实现，容易让初学者困惑、也不利于维护。
- 现在统一以 `config/config.py` 作为唯一配置实现入口；
- 本文件仅作为“向后兼容转发层”，避免旧代码导入路径变化导致报错。

建议：
- 新代码统一使用：`from config.config import get_config`
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
