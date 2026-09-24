# -*- coding: utf-8 -*-
"""
登录接口与文化资产创建接口自动化测试

数据驱动方式：pytest.param + yaml 数据文件
- 登录用例: resources/testdata/login_cases.yaml
- 资产创建用例: resources/testdata/create_asset_cases.yaml

项目约定：
- 所有业务方法调用前必须显式登录并赋值 token
- 登录凭证由测试用例显式控制，不在 action 层自动登录
- 正向用例创建成功后，校验数据是否落库；已落库则清理，保持数据健康
"""

import os
import copy
import yaml
import pytest
from config.constants import TESTDATA_DIR


def load_yaml(filename):
    """加载 yaml 测试数据文件"""
    path = os.path.join(TESTDATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# =============================================================================
# 登录用例
# =============================================================================

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


# =============================================================================
# 文化资产创建用例
# =============================================================================

asset_data = load_yaml("create_asset_cases.yaml")
BASE_ASSET = asset_data.get("base_asset_data", {})


def build_asset_data(case):
    """根据 override 和 remove_fields 组合构造最终 asset_data"""
    data = copy.deepcopy(BASE_ASSET)
    for key, value in (case.get("override") or {}).items():
        data[key] = value
    for key in (case.get("remove_fields") or []):
        data.pop(key, None)
    return data


ASSET_CASES = [
    pytest.param(
        {
            "case_id": c.get("case_id", "asset_case"),
            "title": c.get("title", "资产创建用例"),
            "asset_data": build_asset_data(c),
            "expected_code": c.get("expected_code", 200),
            "expected_has_asset_id": c.get("expected_has_asset_id", False),
        },
        id=c.get("case_id", "asset_case"),
    )
    for c in asset_data.get("cases", [])
]


class TestAssetCreateDataDriven:
    """文化资产创建接口参数化测试"""

    @pytest.mark.parametrize("case", ASSET_CASES)
    def test_create_asset(self, cultural_asset_actions, login_actions, db, case):
        """文化资产创建接口数据驱动测试"""
        # 显式登录并赋值 token
        login_response = login_actions.login_APP("18671450802", "Aa123456")
        assert login_response.get("code") == 200, "登录失败，无法继续创建资产"
        cultural_asset_actions.api.token = login_actions.api.token

        # 创建文化资产
        response, asset_id = cultural_asset_actions.create_asset(case["asset_data"])

        actual_code = response.get("code")

        # 数据库清理：只要接口创建了数据（返回 asset_id）就先清理落库记录，保持数据健康
        # 必须在断言之前执行，确保反向用例被接口意外放行、后续断言失败前也能清掉脏数据
        if asset_id and db.exists_by_id(asset_id):
            db.delete_by_id(asset_id)
            db.commit()
            print(f"[{case['case_id']}] 数据库清理成功, asset_id={asset_id}")

        assert actual_code == case["expected_code"], (
            f"[{case['case_id']}] 期望 code={case['expected_code']}, 实际 code={actual_code}, msg={response.get('msg')}"
        )

        if case["expected_has_asset_id"]:
            assert asset_id, f"[{case['case_id']}] 正向用例应返回 asset_id"
        else:
            assert not asset_id, f"[{case['case_id']}] 反向用例不应返回 asset_id"
