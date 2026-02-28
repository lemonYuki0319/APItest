# -*- coding: utf-8 -*-
"""
登录测试用例
"""

import pytest
from src.api.auth_api import AuthAPI


def test_admin_login():
    """测试管理员登录"""
    auth_api = AuthAPI()
    token = auth_api.login()
    assert token is not None, "Token 不应为空"


def test_login_with_invalid_credentials():
    """测试使用无效凭据登录"""
    auth_api = AuthAPI()
    # 临时修改密码为无效值
    original_password = auth_api.config['admin']['password']
    auth_api.config['admin']['password'] = "invalid_password"
    
    try:
        auth_api.login()
        assert False, "应该登录失败"
    except AssertionError:
        # 预期登录失败
        pass
    finally:
        # 恢复原始密码
        auth_api.config['admin']['password'] = original_password
