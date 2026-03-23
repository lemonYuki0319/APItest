# -*- coding: utf-8 -*-
"""
用户密码重置测试用例
"""

import pytest
from src.utils.data_utils import DataUtils
from src.api.login import UserAPI

# 使用数据驱动（for循环方式）
def test_reset_password_data_driven_loop(user_api):
    """测试重置用户密码（数据驱动：for循环）"""
    # 初学者默认只跑少量数据，避免首次运行生成过多用例/耗时过长
    user_ids = DataUtils.get_user_ids(limit=5)
    for user_id in user_ids:
        result = user_api.reset_password(user_id)
        assert result["code"] == 200, f"用户 {user_id} 重置失败: {result.get('msg')}"


# 使用参数化（推荐：pytest 原生能力，更易生成报告维度）
@pytest.mark.parametrize("user_id", DataUtils.get_user_ids(limit=5))
def test_reset_password_parametrize(user_api, user_id):
    """测试重置用户密码（参数化）"""
    result = user_api.reset_password(user_id)
    assert result["code"] == 200, f"用户 {user_id} 重置失败: {result.get('msg')}"
