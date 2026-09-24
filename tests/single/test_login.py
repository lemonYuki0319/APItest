# -*- coding: utf-8 -*-
"""
登录接口自动化测试（单接口）

数据驱动方式：pytest.param + yaml 数据文件
- 登录用例: resources/testdata/login_cases.yaml

说明：本文件即测试登录接口本身，每条用例独立登录，凭证由用例显式控制。
"""

import os
import yaml
import pytest
from config.constants import TESTDATA_DIR


def load_yaml(filename):
    """加载 yaml 测试数据文件"""
    path = os.path.join(TESTDATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


login_data = load_yaml("login_cases.yaml")

LOGIN_CASES = [
    pytest.param(
        {
            "case_id": c.get("case_id", "login_case"),
            "title": c.get("title", "登录用例"),
            "mobile": c.get("mobile", ""),
            "password": c.get("password", ""),
            "code": c.get("code", ""),
            "expected_code": c.get("expected_code", 200),
            "expected_has_token": c.get("expected_has_token", False),
        },
        id=c.get("case_id", "login_case"),
    )
    for c in login_data.get("cases", [])
]


class TestLoginDataDriven:
    """登录接口参数化测试"""

    @pytest.mark.parametrize("case", LOGIN_CASES)
    def test_login(self, login_actions, case):
        """登录接口数据驱动测试"""
        response = login_actions.login_APP(case["mobile"], case["password"], case["code"])

        actual_code = response.get("code")
        data = response.get("data") or {}
        actual_token = data.get("accessToken")

        assert actual_code == case["expected_code"], (
            f"[{case['case_id']}] 期望 code={case['expected_code']}, 实际 code={actual_code}, msg={response.get('msg')}"
        )

        if case["expected_has_token"]:
            assert actual_token, f"[{case['case_id']}] 正向用例应返回 accessToken"
        else:
            assert not actual_token, f"[{case['case_id']}] 反向用例不应返回 accessToken"
