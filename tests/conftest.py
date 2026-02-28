# -*- coding: utf-8 -*-
"""
pytest fixtures 配置
"""

import sys
import os

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import pytest
import urllib3
from src.actions.user_actions import UserActions

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@pytest.fixture(scope="function")
def user_actions():
    """创建用户业务动作实例"""
    actions = UserActions()
    actions.login()
    yield actions

@pytest.fixture(scope="function")
def api_client():
    """创建 API 客户端（兼容旧测试用例）"""
    actions = UserActions()
    actions.login()
    yield actions.user_api
