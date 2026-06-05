"""
登记文化资产
"""
import json
from src.utils.logger import Logger


logger = Logger(__name__).get_logger()

def test_register_asset_szsb(cultural_asset_actions, login_actions):
    """登记数字商标文化资产"""
    login_response = login_actions.login_APP("18671450802", "a123456")
    assert login_response.get("code") == 200, "登录失败"
    # 将token传递给文化资产动作
    cultural_asset_actions.api.token = login_actions.api.token
    
    # 准备资产数据
    asset_data = {
        "isRegistered": 1,
        "cultureAssetName": "数字商标456",
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

    # 保存原始资产数据（用于后续提交评估）
    original_asset_name = asset_data["cultureAssetName"]
    original_asset_type = asset_data["cultureAssetType"]

    #WEB端登录
    login_response = login_actions.login_WEB("芋道源码", "admin", "Szxc@2024")
    assert login_response.get("code") == 200, "登录失败"
    # 将token传递给文化资产动作
    cultural_asset_actions.api.token = login_actions.api.token
    # 资产登记审核
    review_data = {
        "id": f"{asset_id}",
        "auditStatus": "2",
        "auditReason": "1"
    }

    response = cultural_asset_actions.asset_Registration_Review(review_data)
    assert response.get("code") == 200, f"资产登记审核失败: {response.get('msg')}"

    # 资产公示审核
    disclosure_data = {
        "id": f"{asset_id}",
        "noticeStatus": "2"
    }

    response = cultural_asset_actions.asset_Disclosure_Review(disclosure_data)
    assert response.get("code") == 200, f"资产公示审核失败: {response.get('msg')}"
    print(f"资产公示审核成功，资产ID: {asset_id}")

    # 将APP端token传递给文化资产动作端token
    login_response = login_actions.login_APP("18671450802", "a123456")
    assert login_response.get("code") == 200, "APP登录失败"
    
    cultural_asset_actions.api.token = login_actions.api.token
    # 提交评估
    valuation_data = {
        "id": "",
        "digitalCultureAssetId": f"{asset_id}",
        "assetsTypeId": original_asset_type,
        "cultureAssetName": original_asset_name,
        "investmentCost": 427,
        "historicalIncome": 2738,
        "valuationPurpose": "资产确权与登记",
        "uploadedDocumentsList": [
            {
                "name": "04年费缴纳证明.docx",
                "url": "https://www.whhnhy.com:29000/szxc/f3ccb29e32a7002f62bc8e9d485401279046a3e9472eb8f8aac7561d68ef2c47.docx"
            },
            {
                "name": "03财务报表.xlsx",
                "url": "https://www.whhnhy.com:29000/szxc/494162cecf021b2d52b28059db903312f4f0552acc930fc3d4eda0e64c405abc.xlsx"
            }
        ]
    }
    response, valuation_id = cultural_asset_actions.submit_valuation(valuation_data)
    assert response.get("code") == 200, f"提交评估失败: {response.get('msg')}"
    print(f"提交评估成功，评估ID: {valuation_id}")