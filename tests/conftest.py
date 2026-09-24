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
    创建登录动作实例（function 级，每条用例独立）

    用于需要测试登录接口本身的用例（如 test_login）。
    """
    from src.actions.login import LoginActions
    return LoginActions()


@pytest.fixture(scope="session")
def app_token():
    """
    会话级登录：整个测试会话只登录一次，返回 token，避免反复登录。

    用于需要登录态但不测登录本身的用例（如创建资产）。
    测试用例拿到 token 后自行赋值给业务 API 客户端再调用接口。
    """
    from src.actions.login import LoginActions
    actions = LoginActions()
    response = actions.login_APP("18671450802", "Aa123456")
    assert response.get("code") == 200, f"会话登录失败: {response.get('msg')}"
    token = actions.api.token
    assert token, "会话登录未获取到 accessToken"
    return token


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


# =============================================================================
# 数据库相关 Fixture
# =============================================================================

@pytest.fixture(scope="function")
def db():
    """
    达梦数据库工具实例（function 级，用例结束自动关闭连接）

    用法：
        exists = db.exists_by_id(asset_id)   # 查询文化资产表
        db.delete_by_id(asset_id)           # 删除文化资产表记录
        db.commit()                          # 提交事务（删除后需 commit 才生效）
    """
    from src.utils.db import DBHelper
    helper = DBHelper()
    yield helper
    helper.close()
