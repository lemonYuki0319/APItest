"""
文化资产多轮对话
"""
import pytest
import json
import time
from src.actions.cultural_asset_actions import CulturalAssetActions

@pytest.fixture(scope="function")
def cultural_asset_actions():
    """创建文化资产业务动作实例"""
    return CulturalAssetActions()

def test_Multi_turn_Dialogue(cultural_asset_actions):
    """测试多轮对话"""
    #APP登录
    login_response = cultural_asset_actions.login_APP("18671450802", "a123456")
    assert login_response.get("code") == 200, f"APP登录失败: {login_response.get('msg')}"
    #获取对话
    dialog_data = {"chatType":1,"useContext":True}
    response, conversation_id = cultural_asset_actions.get_conversation(dialog_data)
    assert response.get("code") == 200, f"获取对话失败: {response.get('msg')}"
    print(f"获取对话成功，对话ID: {conversation_id}")
    #多轮对话
    asset_data = {
    "serviceName": "hy-ai-evaluate",
    "conversationId": conversation_id,
    "uri": "/api/culture_asset_chat_ai/stream",
    "params": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "culture_asset_type": "digital_art_valuation",
                        "type": "confirm_file",
                        "text": "file",
                        "text_value": "",
                        "file_list": [
                            {
                                "filename": "00数字艺术品评估-信息收集.docx",
                                "file_url": "https://www.whhnhy.com:29000/szxc/8bbdbbb3ebd7091fe07ebf35af1ace86bb68d275caca83293eb1552978365cb0.docx"
                            },
                            {
                                "filename": "01数字艺术品证书.png",
                                "file_url": "https://www.whhnhy.com:29000/szxc/d516d13b9f1b2105f78096a3ce11c2f678adf52c65801a3f2197abaebdd565ad.png"
                            },
                            {
                                "filename": "02资产权属证明.docx",
                                "file_url": "https://www.whhnhy.com:29000/szxc/73c62f2d89df8ed625367d9d9f6a00cbfe0cbe7355fdafa8b1bd8fbe2c6ab9a6.docx"
                            },
                            {
                                "filename": "03区块链存证证明.png",
                                "file_url": "https://www.whhnhy.com:29000/szxc/c517ec556f0801394943e2652f8df98324a7fac97d81f4716a850ff24e5c5401.png"
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
    response = cultural_asset_actions.multi_turn_dialogue(asset_data)
    assert response.status_code == 200, f"多轮对话生成失败，状态码: {response.status_code}"
    
    # 等待5分钟，让多轮对话进行中
    print("等待10分钟，让多轮对话进行中...")
    time.sleep(600)  # 600秒 = 10分钟

    #WEB登录
    login_response = cultural_asset_actions.login_WEB("芋道源码", "admin", "Szxc@2024")
    assert login_response.get("code") == 200, f"WEB登录失败: {login_response.get('msg')}"
    time.sleep(5)
    
    response = cultural_asset_actions.query_registered_assets()
    assert response.get("code") == 200, f"查询登记资产失败: {response.get('msg')}"
    # 获取第一个资产的id
    asset_list = response.get('data', {}).get('list', [])
    first_asset_id = asset_list[0].get('id')
    print(f"第一个资产的ID: {first_asset_id}")
    time.sleep(5)
    # 资产登记审核
    asset_data=({
    "id": f"{first_asset_id}",
    "auditStatus": "2",
    "auditReason": "1"
    })

    response = cultural_asset_actions.asset_Registration_Review(asset_data)
    assert response.get("code") == 200, f"资产登记审核失败: {response.get('msg')}"

    time.sleep(300)
    print(f"等待五分钟后开始公示")
    # 资产公示审核
    asset_data=({
    "id": f"{first_asset_id}",
    "noticeStatus": "2"
    })

    response = cultural_asset_actions.asset_Disclosure_Review(asset_data)
    assert response.get("code") == 200, f"资产公示审核失败: {response.get('msg')}"
    print(f"资产公示审核成功，资产ID: {first_asset_id}")
