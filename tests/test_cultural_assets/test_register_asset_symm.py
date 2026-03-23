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

def test_register_asset_symm(cultural_asset_actions, login_actions):
    """登记商业秘密文化资产"""
    login_response = login_actions.login_APP("18310665081", "a123456")
    assert login_response.get("code") == 200, "登录失败"
    # 将token传递给文化资产动作
    cultural_asset_actions.api.token = login_actions.api.token
    
    # 准备资产数据
    asset_data = {
        "isRegistered": 1,
        "cultureAssetName": "商业秘密333",
        "cultureAssetType": "2997845276013894001",
        "registerSubjectType": "1",
        "ownershipType": "1",
        "coOwnerSaveReqList": [
            {
                "coOwnerName": "",
                "coOwnerPhone": ""
            }
        ],
        "assetDesc": "水电费收到刚发的好多个",
        "assetImgUrl": [
            {
                "name": "04企业营业执照.png",
                "url": "https://www.whhnhy.com:8900/szxc/af497fc3e6f1e527a8437537cc2c3f8c585bcf369d0682bc6e97f9b489924d5d.png"
            }
        ],
        "ownershipFileUrl": [
            {
                "name": "02商业秘密权属与合法证明.docx",
                "url": "https://www.whhnhy.com:8900/szxc/b0e3fabb8549f665d1af1c818aa28352e364baff93b8608143ba4ca8bb8bae70.docx"
            }
        ],
        "assetDetailValidJson": "{\"secretCategory\":\"1\",\"completionTime\":\"2026-05-01\",\"carrierType\":\"1\",\"secretStatus\":\"1\",\"confidentialLevel\":\"1\",\"responsiblePerson\":\"张文骏\",\"applicationField\":\"测试\",\"secretDescription\":[{\"name\":\"01商业秘密说明.docx\",\"url\":\"https://www.whhnhy.com:8900/szxc/3d9b985fe49082a996cadeea73054e5d5702b1fa1a96c9e599aaab2864573c52.docx\"}],\"confidentialAgreement\":[{\"name\":\"03保密协议.docx\",\"url\":\"https://www.whhnhy.com:8900/szxc/e4caec11c88a4682045d71db5daa1edaeaa9cd185c9db57f77d0d6fda96aaf0f.docx\"}]}",
        "assetDetailJson": "[{\"label\":\"秘密类别\",\"name\":\"secretCategory\",\"type\":\"picker\",\"isWrap\":true,\"placeholder\":\"请选择\",\"rules\":[{\"required\":true,\"message\":\"请选择秘密类别\"}],\"dictionary\":\"culture_secret_category\",\"value\":\"1\",\"valueName\":\"技术信息\"},{\"label\":\"秘密形成完成时间\",\"name\":\"completionTime\",\"type\":\"datePicker\",\"isWrap\":true,\"placeholder\":\"年/月/日\",\"rules\":[{\"required\":true,\"message\":\"请选择秘密形成完成时间\"}],\"value\":\"2026-05-01\"},{\"label\":\"秘密载体类型\",\"name\":\"carrierType\",\"type\":\"picker\",\"isWrap\":true,\"placeholder\":\"请选择\",\"rules\":[{\"required\":true,\"message\":\"请选择秘密载体类型\"}],\"dictionary\":\"culture_secret_carrier_type\",\"value\":\"1\",\"valueName\":\"纸质文档\"},{\"label\":\"秘密状态\",\"name\":\"secretStatus\",\"type\":\"picker\",\"isWrap\":true,\"placeholder\":\"请选择\",\"rules\":[{\"required\":true,\"message\":\"请选择秘密状态\"}],\"dictionary\":\"culture_secret_status\",\"value\":\"1\",\"valueName\":\"正在使用\"},{\"label\":\"保密等级\",\"name\":\"confidentialLevel\",\"type\":\"picker\",\"isWrap\":true,\"placeholder\":\"请选择\",\"rules\":[{\"required\":true,\"message\":\"请选择保密等级\"}],\"dictionary\":\"culture_confidential_level\",\"value\":\"1\",\"valueName\":\"绝密\"},{\"label\":\"保密负责人\",\"name\":\"responsiblePerson\",\"type\":\"input\",\"maxlength\":30,\"isWrap\":true,\"placeholder\":\"请输入\",\"rules\":[{\"required\":true,\"message\":\"请输入保密负责人\"}],\"value\":\"张文骏\"},{\"label\":\"应用领域\",\"name\":\"applicationField\",\"type\":\"textarea\",\"isWrap\":true,\"placeholder\":\"请输入\",\"maxlength\":500,\"showWordLimit\":true,\"autosize\":{\"minHeight\":100},\"rules\":[{\"required\":true,\"message\":\"请输入应用领域\"}],\"value\":\"测试\"},{\"label\":\"商业秘密说明\",\"name\":\"secretDescription\",\"type\":\"uploader\",\"isWrap\":true,\"placeholder\":\"点击上传\\n支持Word格式，excel格式，pdf格式，单个文件不超过10MB\",\"maxSize\":10485760,\"fileType\":[\"application/msword\",\"application/vnd.openxmlformats-officedocument.wordprocessingml.document\",\"application/vnd.ms-excel\",\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\",\"application/pdf\"],\"rules\":[{\"required\":true,\"message\":\"请上传商业秘密说明\"}],\"value\":[{\"name\":\"01商业秘密说明.docx\",\"url\":\"https://www.whhnhy.com:8900/szxc/3d9b985fe49082a996cadeea73054e5d5702b1fa1a96c9e599aaab2864573c52.docx\"}],\"fileState\":true},{\"label\":\"保密协议\",\"name\":\"confidentialAgreement\",\"type\":\"uploader\",\"isWrap\":true,\"placeholder\":\"点击上传\\n支持Word格式，excel格式，pdf格式，单个文件不超过10MB\",\"maxSize\":10485760,\"fileType\":[\"application/msword\",\"application/vnd.openxmlformats-officedocument.wordprocessingml.document\",\"application/vnd.ms-excel\",\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\",\"application/pdf\"],\"rules\":[{\"required\":true,\"message\":\"请上传保密协议\"}],\"value\":[{\"name\":\"03保密协议.docx\",\"url\":\"https://www.whhnhy.com:8900/szxc/e4caec11c88a4682045d71db5daa1edaeaa9cd185c9db57f77d0d6fda96aaf0f.docx\"}],\"fileState\":true}]"
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
    "auditReason": "1"})

    response = cultural_asset_actions.asset_Registration_Review(asset_data)
    assert response.get("code") == 200, f"资产登记审核失败: {response.get('msg')}"

    # 资产公示审核
    asset_data=({
    "id": f"{asset_id}",
    "noticeStatus": "2"})

    response = cultural_asset_actions.asset_Disclosure_Review(asset_data)
    assert response.get("code") == 200, f"资产公示审核失败: {response.get('msg')}"
    print(f"资产公示审核成功，资产ID: {asset_id}")