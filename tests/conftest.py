# -*- coding: utf-8 -*-
"""
pytest fixtures 配置

此模块集中定义所有测试共享的fixture，包括：
- 登录相关fixture
- 文化资产相关fixture
- API客户端fixture
"""

import sys
import os

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import pytest
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# =============================================================================
# 登录相关 Fixture
# =============================================================================

@pytest.fixture(scope="function")
def login_actions():
    """
    创建登录动作实例
    
    提供APP端和WEB端登录功能
    """
    from src.actions.login import LoginActions
    return LoginActions()


# =============================================================================
# 文化资产相关 Fixture
# =============================================================================

@pytest.fixture(scope="function")
def cultural_asset_actions():
    """
    创建文化资产业务动作实例
    
    提供文化资产登记、查询、审核等功能
    """
    from src.actions.cultural_assets.cultural_asset_actions import CulturalAssetActions
    return CulturalAssetActions()
