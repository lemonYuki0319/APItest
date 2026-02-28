# -*- coding: utf-8 -*-
"""
用户密码重置测试用例
"""

import pytest
from src.utils.data_utils import DataUtils

#使用数据驱动
def test_reset_password(user_actions):
    """测试重置用户密码（数据驱动）"""
    user_ids = DataUtils.get_user_ids()
    for user_id in user_ids:
        result = user_actions.reset_password(user_id)
        assert result["code"] == 200, f"用户 {user_id} 重置成功: {result.get('msg')}"

#使用参数化
@pytest.mark.parametrize("user_id", DataUtils.get_user_ids())
def test_reset_password(user_actions, user_id):
    """测试重置用户密码（参数化）"""
    result = user_actions.reset_password(user_id)
    assert result["code"] == 200, f"用户 {user_id} 重置成功: {result.get('msg')}"
