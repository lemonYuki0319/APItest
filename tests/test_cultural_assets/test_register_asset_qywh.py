"""
登记文化资产
"""
import pytest
import json
from src.actions.cultural_asset_actions import CulturalAssetActions


@pytest.fixture(scope="function")
def cultural_asset_actions():
    """创建文化资产业务动作实例"""
    return CulturalAssetActions()

def test_register_asset_qywh(cultural_asset_actions):
    """登记企业文化资产"""
    login_response = cultural_asset_actions.login_APP("18310665081", "a123456")
    assert login_response.get("code") == 200, "登录失败"

    # 准备资产数据
    asset_data = {
        "isRegistered": 1,
        "cultureAssetName": "企业文化002",
        "cultureAssetType": "2997845276013894002",
        "registerSubjectType": "1",
        "ownershipType": "1",
        "coOwnerSaveReqList": [
            {
                "coOwnerName": "",
                "coOwnerPhone": ""
            }
        ],
        "assetDesc": "山东感觉偶的贵啊更多",
        "assetImgUrl": [
            {
                "name": "4784c45070c1992760d2b64f7fac697.png",
                "url": "https://www.whhnhy.com:8900/szxc/14d3e2c86b989fe7c3c5dba385a192eaa1f3a6423b71930c8df6a1c76553e789.png"
            }
        ],
        "ownershipFileUrl": [
            {
                "name": "01资产权属证明.docx",
                "url": "https://www.whhnhy.com:8900/szxc/d1e248393b329c0246a6c954592b104c7ef9bbb6c1bdb561974da90f01bac190.docx"
            }
        ],
        "assetDetailValidJson": json.dumps({
            "enterpriseMission": "测试企业使命",
            "enterpriseVision": "测试企业愿景",
            "coreValues": "测试核心价值观",
            "managementPhilosophy": "测试经营管理理念",
            "responsibleDepartment": "1",
            "coreMeasures": "3",
            "culturalSystemDocuments": [{
                "name": "02企业文化建设管理制度.docx",
                "url": "https://www.whhnhy.com:29000/szxc/03872d2671b36e0f3cda040a26bf5c17f6e01580f39b24d4f2bd9ca6b6a73891.docx"
            }],
            "supplementaryDocuments": []
        }, ensure_ascii=False),
        "assetDetailJson": json.dumps([
            {"label": "企业使命", "name": "enterpriseMission", "type": "textarea", "isWrap": True, "placeholder": "请输入", "maxlength": 500, "showWordLimit": True, "autosize": {"minHeight": 100}, "rules": [{"required": True, "message": "请输入企业使命"}], "value": "测试企业使命"},
            {"label": "企业愿景", "name": "enterpriseVision", "type": "textarea", "isWrap": True, "placeholder": "请输入", "maxlength": 500, "showWordLimit": True, "autosize": {"minHeight": 100}, "rules": [{"required": True, "message": "请输入企业愿景"}], "value": "测试企业愿景"},
            {"label": "核心价值观", "name": "coreValues", "type": "textarea", "isWrap": True, "placeholder": "请输入", "maxlength": 500, "showWordLimit": True, "autosize": {"minHeight": 100}, "rules": [{"required": True, "message": "请输入核心价值观"}], "value": "测试核心价值观"},
            {"label": "经营管理理念", "name": "managementPhilosophy", "type": "textarea", "isWrap": True, "placeholder": "请输入", "maxlength": 500, "showWordLimit": True, "autosize": {"minHeight": 100}, "value": "测试经营管理理念"},
            {"label": "文化落地负责部门", "name": "responsibleDepartment", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择文化落地负责部门"}], "dictionary": "culture_responsible_department", "value": "1", "valueName": "品牌文化部"},
            {"label": "文化落地核心措施", "name": "coreMeasures", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择文化落地核心措施"}], "dictionary": "culture_core_measures", "value": "3", "valueName": "开展全员文化培训"},
            {"label": "文化制度文件", "name": "culturalSystemDocuments", "type": "uploader", "isWrap": True, "placeholder": "点击上传\n支持Word格式，单个文件不超过10MB", "maxSize": 10485760, "fileType": ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"], "rules": [{"required": True, "message": "请上传文化制度文件"}], "value": [{"name": "02企业文化建设管理制度.docx", "url": "https://www.whhnhy.com:29000/szxc/03872d2671b36e0f3cda040a26bf5c17f6e01580f39b24d4f2bd9ca6b6a73891.docx"}], "fileState": True},
            {"label": "补充说明文件", "name": "supplementaryDocuments", "type": "uploader", "isWrap": True, "placeholder": "点击上传\n支持Word格式，单个文件不超过10MB", "maxSize": 10485760, "fileType": ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"], "value": [], "fileState": True}
        ], ensure_ascii=False)
    }

    # 创建资产
    response, asset_id = cultural_asset_actions.create_asset(asset_data)
    assert response.get("code") == 200, f"登记资产失败: {response.get('msg')}"
    print(f"资产登记成功，资产ID: {asset_id}")

    #WEB端登录
    login_response = cultural_asset_actions.login_WEB("芋道源码", "admin", "Szxc@2024")
    assert login_response.get("code") == 200, "登录失败"
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
