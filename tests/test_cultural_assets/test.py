import sys
import os

from urllib3 import response

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from src.actions.login import CulturalAssetActions
from src.api.auth_api import AuthAPI

def test_APPlogin():
    response = CulturalAssetActions().login_APP("18671450802", "a123456")
    assert response.get("code") == 200, f"登录失败: {response.get('msg')}"
    access_token = response.get('data', {}).get('accessToken')
    print(f"获取accessToken: {access_token}")
    return access_token

def test_web_login():
    auth_api = AuthAPI()
    token = auth_api.login()
    print(f"获取accessToken: {token}")
    return token
    
if __name__ == "__main__":
    test_APPlogin()
    test_web_login()