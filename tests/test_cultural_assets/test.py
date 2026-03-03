import sys
import os

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from src.actions.cultural_asset_actions import CulturalAssetActions

response = CulturalAssetActions().login("18671450802", "a123456")
access_token = response.get('data', {}).get('accessToken')
print(f"获取accessToken: {access_token}")