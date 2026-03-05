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

def test_register_asset_symm(cultural_asset_actions):
    """登记商业秘密文化资产"""
    login_response = cultural_asset_actions.login_APP("18671450802", "a123456")
    assert login_response.get("code") == 200, "登录失败"
    
    # 准备资产数据
    asset_data = {
        "isRegistered": 1,
        "cultureAssetName": "商业秘密",
        "cultureAssetType": "2997845276013894001",
        "registerSubjectType": "1",
        "ownershipType": "1",
        "coOwnerSaveReqList": [
            {
                "coOwnerName": "",
                "coOwnerPhone": ""
            }
        ],
        "assetDesc": "啊啥就拉开公对私哦",
        "assetImgUrl": [
            {
                "name": "04企业营业执照.png",
                "url": "https://www.whhnhy.com:29000/szxc/af497fc3e6f1e527a8437537cc2c3f8c585bcf369d0682bc6e97f9b489924d5d.png"
            }
        ],
        "ownershipFileUrl": [
            {
                "name": "01资产权属证明.docx",
                "url": "https://www.whhnhy.com:29000/szxc/d1e248393b329c0246a6c954592b104c7ef9bbb6c1bdb561974da90f01bac190.docx"
            }
        ],
        "assetDetailValidJson": json.dumps({
            "secretCategory": "1",
            "completionTime": "2027-03-01",
            "carrierType": "4",
            "secretStatus": "1",
            "confidentialLevel": "1",
            "responsiblePerson": "张文骏",
            "applicationField": "哦房管局哦四鬼啊国防",
            "secretDescription": [{
                "name": "01商业秘密说明.docx",
                "url": "https://www.whhnhy.com:29000/szxc/3d9b985fe49082a996cadeea73054e5d5702b1fa1a96c9e599aaab2864573c52.docx"
            }],
            "confidentialAgreement": [{
                "name": "03保密协议.docx",
                "url": "https://www.whhnhy.com:29000/szxc/e4caec11c88a4682045d71db5daa1edaeaa9cd185c9db57f77d0d6fda96aaf0f.docx"
            }]
        }, ensure_ascii=False),
        "assetDetailJson": json.dumps([
            {"label": "秘密类别", "name": "secretCategory", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择秘密类别"}], "dictionary": "culture_secret_category", "value": "1", "valueName": "技术信息"},
            {"label": "秘密形成完成时间", "name": "completionTime", "type": "datePicker", "isWrap": True, "placeholder": "年/月/日", "rules": [{"required": True, "message": "请选择秘密形成完成时间"}], "value": "2027-03-01"},
            {"label": "秘密载体类型", "name": "carrierType", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择秘密载体类型"}], "dictionary": "culture_secret_carrier_type", "value": "4", "valueName": "口头知悉"},
            {"label": "秘密状态", "name": "secretStatus", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择秘密状态"}], "dictionary": "culture_secret_status", "value": "1", "valueName": "正在使用"},
            {"label": "保密等级", "name": "confidentialLevel", "type": "picker", "isWrap": True, "placeholder": "请选择", "rules": [{"required": True, "message": "请选择保密等级"}], "dictionary": "culture_confidential_level", "value": "1", "valueName": "绝密"},
            {"label": "保密负责人", "name": "responsiblePerson", "type": "input", "isWrap": True, "placeholder": "请输入", "rules": [{"required": True, "message": "请输入保密负责人"}], "value": "张文骏"},
            {"label": "应用领域", "name": "applicationField", "type": "textarea", "isWrap": True, "placeholder": "请输入", "maxlength": 500, "showWordLimit": True, "autosize": {"minHeight": 100}, "rules": [{"required": True, "message": "请输入应用领域"}], "value": "哦i房管局哦i四鬼啊国防"},
            {"label": "商业秘密说明", "name": "secretDescription", "type": "uploader", "isWrap": True, "placeholder": "点击上传\n支持Word格式，单个文件不超过10MB", "maxSize": 10485760, "fileType": ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"], "rules": [{"required": True, "message": "请上传商业秘密说明"}], "value": [{"name": "01商业秘密说明.docx", "url": "https://www.whhnhy.com:29000/szxc/3d9b985fe49082a996cadeea73054e5d5702b1fa1a96c9e599aaab2864573c52.docx"}], "fileState": True},
            {"label": "保密协议", "name": "confidentialAgreement", "type": "uploader", "isWrap": True, "placeholder": "点击上传\n支持Word格式，单个文件不超过10MB", "maxSize": 10485760, "fileType": ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"], "rules": [{"required": True, "message": "请上传保密协议"}], "value": [{"name": "03保密协议.docx", "url": "https://www.whhnhy.com:29000/szxc/e4caec11c88a4682045d71db5daa1edaeaa9cd185c9db57f77d0d6fda96aaf0f.docx"}], "fileState": True}
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