# -*- coding: utf-8 -*-
"""
用户密码重置测试用例
"""

import pytest
from src.utils.data_utils import DataUtils


@pytest.mark.parametrize("user_id", DataUtils.get_user_ids())
def test_reset_password(user_actions, user_id):
    """测试重置用户密码"""
    result = user_actions.reset_password(user_id)
    assert result["code"] == 200, f"重置失败: {result.get('msg')}"


def test_reset_password_with_custom_password(user_actions):
    """测试使用自定义密码重置"""
    user_id = DataUtils.get_user_ids()[0]  # 使用第一个用户 ID
    custom_password = "Custom@123"
    result = user_actions.reset_password(user_id, custom_password)
    assert result["code"] == 200, f"重置失败: {result.get('msg')}"
