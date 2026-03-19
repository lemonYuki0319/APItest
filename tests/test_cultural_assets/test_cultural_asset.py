# -*- coding: utf-8 -*-
"""
文化资产测试用例
"""

import pytest
import json
from src.actions.cultural_asset_actions import CulturalAssetActions


@pytest.fixture(scope="function")
def cultural_asset_actions():
    """创建文化资产业务动作实例"""
    return CulturalAssetActions()


def test_login_success(cultural_asset_actions):
    """测试1: 正确的手机号和密码登录"""
    response = cultural_asset_actions.login("18671450802", "a123456")
    assert response.get("code") == 200, f"登录失败: {response.get('msg')}"
    assert response.get("data", {}).get("accessToken") is not None, "Token 不应为空"


def test_login_missing_mobile(cultural_asset_actions):
    """测试2: 缺少mobile参数"""
    response = cultural_asset_actions.login("", "a123456")
    assert response.get("code") != 200, "缺少mobile参数应该失败"


def test_login_missing_password(cultural_asset_actions):
    """测试3: 缺少password参数"""
    response = cultural_asset_actions.login("18671450802", "")
    assert response.get("code") != 200, "缺少password参数应该失败"


def test_login_wrong_password(cultural_asset_actions):
    """测试4: 密码错误"""
    response = cultural_asset_actions.login("18671450802", "wrongpass")
    assert response.get("code") != 200, "密码错误应该失败"


def test_login_unregistered_mobile(cultural_asset_actions):
    """测试5: 不存在的手机号"""
    response = cultural_asset_actions.login("13800138000", "a123456")
    assert response.get("code") != 200, "不存在的手机号应该失败"


def test_create_asset_success(cultural_asset_actions):
    """测试6: 成功创建资产 - 数字商标"""
    # 先登录
    login_response = cultural_asset_actions.login("18671450802", "a123456")
    assert login_response.get("code") == 200, "登录失败"
    
    # 准备资产数据
    asset_data = {
        "isRegistered": 1,
        "cultureAssetName": "数字商标",
        "cultureAssetType": "2997845276013893005",
        "registerSubjectType": "1",
        "ownershipType": "1",
        "coOwnerSaveReqList": [
            {
                "coOwnerName": "",
                "coOwnerPhone": ""
            }
        ],
        "assetDesc": "测试",
        "assetImgUrl": [
            {
                "name": "05数字出版许可证（非必传，仅供参考）.png",
                "url": "https://www.whhnhy.com:29000/szxc/942fbdf590c51fc498d11074733e9fa5552b0f9012dfa7e81efd2084b0717d6f.png"
            }
        ],
        "ownershipFileUrl": [
            {
                "name": "02资产权属证明.docx",
                "url": "https://www.whhnhy.com:29000/szxc/20c2947be1237ac709d2b12ea4e85c88716aae7bd747dbbe9f818c54d7746ebd.docx"
            }
        ],
        "assetDetailValidJson": json.dumps({
            "registrationNumber": "4546944",
            "markType": "1",
            "trademarkCategory": "6",
            "acquisitionMethod": "4",
            "validityPeriod": "2026-02-10 ~ 2026-02-11",
            "transactionRightsScope": "4",
            "scopeOfApplication": "陈成的口味",
            "registrationCertificate": [{
                "name": "01商标注册证书.png",
                "url": "https://www.whhnhy.com:29000/szxc/9d012b98493fee6b4c261b99ef3b8dcbf0734a44bc5d76006d12b8caaf9f048a.png"
            }]
        }, ensure_ascii=False),
        "assetDetailJson": json.dumps([
            {"type": "title", "label": "资产详细信息"},
            {"label": "商标注册号", "name": "registrationNumber", "type": "input", "isWrap": True, "placeholder": "请输入", "rules": [{"required": True, "message": "请输入商标注册号"}], "value": "4546944"},
            {"label": "商标标识类型", "name": "markType", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择商标标识类型"}], "dictionary": "cultural_asset_digital_trademark_mark_type", "value": "1", "valueName": "文字商标"},
            {"label": "商标类别", "name": "trademarkCategory", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择商标类别"}], "dictionary": "cultural_asset_digital_trademark_type", "value": "6", "valueName": "第6类-金属材料"},
            {"label": "获得方式", "name": "acquisitionMethod", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择获得方式"}], "dictionary": "cultural_asset_patent_acquisition_method", "value": "4", "valueName": "受赠"},
            {"label": "有效期限", "name": "validityPeriod", "type": "DateRange", "isWrap": True, "placeholder": "年/月/日", "rules": [{"required": True, "message": "请选择有效期限"}], "value": "2026-02-10 ~ 2026-02-11"},
            {"label": "交易权利范围", "name": "transactionRightsScope", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择交易权利范围"}], "dictionary": "cultural_asset_transaction_rights_scope", "value": "4", "valueName": "普通实施许可"},
            {"label": "适用范围", "name": "scopeOfApplication", "type": "textarea", "isWrap": True, "placeholder": "请输入商标适用范围", "rules": [{"required": True, "message": "请输入适用范围"}], "value": "陈成的口味", "autosize": {"minHeight": 80}, "maxlength": 500, "showWordLimit": True},
            {"label": "商标注册证附件", "name": "registrationCertificate", "type": "uploader", "isWrap": True, "placeholder": "点击上传\n支持PNG, JPG，小于10MB", "maxSize": 10, "fileType": ["image/png", "image/jpg"], "rules": [{"required": True, "message": "请上传商标注册证附件"}], "value": [{"name": "01商标注册证书.png", "url": "https://www.whhnhy.com:29000/szxc/9d012b98493fee6b4c261b99ef3b8dcbf0734a44bc5d76006d12b8caaf9f048a.png"}], "fileState": True}
        ], ensure_ascii=False)
    }
    
    # 创建资产
    response, asset_id = cultural_asset_actions.create_asset(asset_data)
    assert response.get("code") == 200, f"创建资产失败: {response.get('msg')}"
    assert asset_id, "创建资产成功时 asset_id 不应为空"


def test_create_asset_missing_required_field(cultural_asset_actions):
    """测试7: 缺少必填字段"""
    # 先登录
    login_response = cultural_asset_actions.login("18671450802", "a123456")
    assert login_response.get("code") == 200, "登录失败"
    
    # 准备不完整的资产数据
    asset_data = {
        "assetDetailJson": "{}"
    }
    
    # 创建资产
    response, asset_id = cultural_asset_actions.create_asset(asset_data)
    assert response.get("code") != 200, "缺少必填字段应该失败"
    assert not asset_id, "创建失败时 asset_id 应为空"

def test_query_asset(cultural_asset_actions):
    """测试8: 查询资产"""
    # 先登录
    login_response = cultural_asset_actions.login("18671450802", "a123456")
    assert login_response.get("code") == 200, "登录失败"
    
    # 查询资产
    response = cultural_asset_actions.query_asset()
    assert response.get("code") == 200, f"查询资产失败: {response.get('msg')}"
