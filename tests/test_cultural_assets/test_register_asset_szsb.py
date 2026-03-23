"""
登记文化资产
"""
import pytest
import json
from src.actions.cultural_assets.cultural_asset_actions import CulturalAssetActions
from src.actions.login import CulturalAssetActions as LoginActions


@pytest.fixture(scope="function")
def cultural_asset_actions():
    """创建文化资产业务动作实例"""
    return CulturalAssetActions()

@pytest.fixture(scope="function")
def login_actions():
    """创建登录动作实例"""
    return LoginActions()

def test_register_asset_szsb(cultural_asset_actions, login_actions):
    """登记数字商标文化资产"""
    login_response = login_actions.login_APP("18310665081", "a123456")
    assert login_response.get("code") == 200, "登录失败"
    # 将token传递给文化资产动作
    cultural_asset_actions.api.token = login_actions.api.token
    
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
    assert response.get("code") == 200, f"登记资产失败: {response.get('msg')}"
    print(f"资产登记成功，资产ID: {asset_id}")

    #WEB端登录
    login_response = login_actions.login_WEB("芋道源码", "admin", "Szxc@2024")
    assert login_response.get("code") == 200, "登录失败"
    # 将token传递给文化资产动作
    cultural_asset_actions.api.token = login_actions.api.token
    # 资产登记审核
    asset_data=({
    "id": f"{asset_id}",
    "auditStatus": "2",
    "auditReason": "1"
    })

    response = cultural_asset_actions.asset_Registration_Review(asset_data)
    assert response.get("code") == 200, f"资产登记审核失败: {response.get('msg')}"

    # 资产公示审核
    asset_data=({
    "id": f"{asset_id}",
    "noticeStatus": "2"
    })

    response = cultural_asset_actions.asset_Disclosure_Review(asset_data)
    assert response.get("code") == 200, f"资产公示审核失败: {response.get('msg')}"
    print(f"资产公示审核成功，资产ID: {asset_id}")