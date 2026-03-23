# -*- coding: utf-8 -*-
"""
仅包含登录动作
"""

from src.api.login import UserAPI as CulturalAssetAPI
from src.utils.logger import logger

class LoginActions:
    def __init__(self):
        """初始化登录动作"""
        self.api = CulturalAssetAPI()
        
    def login_APP(self, mobile, password, code=""):
        """APP端登录"""
        response = self.api.login_APP(mobile, password, code)
        if response.get("code") == 200:
            logger.info("APP端登录成功")
        else:
            logger.error(f"APP端登录失败: {response.get('msg')}")
        return response

    def login_WEB(self, tenantName, username, password, rememberMe=True):
        """WEB端登录"""
        response = self.api.login_WEB(tenantName, username, password, rememberMe)
        if response.get("code") == 200:
            logger.info("WEB端登录成功")
        else:
            logger.error(f"WEB端登录失败: {response.get('msg')}")
        return response

    def reset_password(self, user_id, password=None):
        """重置用户密码"""
        response = self.api.reset_password(user_id, password)
        if response.get("code") == 200:
            logger.info("密码重置成功")
        else:
            logger.error(f"密码重置失败: {response.get('msg')}")
        return response