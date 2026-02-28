# -*- coding: utf-8 -*-
"""
用户业务动作层
"""

from src.api.auth_api import AuthAPI
from src.api.user_api import UserAPI
from src.utils.logger import logger

class UserActions:
    def __init__(self):
        """初始化用户业务动作"""
        self.auth_api = AuthAPI()
        self.user_api = None
    
    def login(self):
        """登录并获取 token"""
        token = self.auth_api.login()
        logger.info("管理员登录成功")
        # 使用获取的 token 初始化用户 API
        self.user_api = UserAPI(token)
        return token
    
    def reset_password(self, user_id, password=None):
        """重置用户密码"""
        if not self.user_api:
            self.login()
        result = self.user_api.reset_password(user_id, password)
        logger.info(f"用户 {user_id} 密码重置成功")
        return result
