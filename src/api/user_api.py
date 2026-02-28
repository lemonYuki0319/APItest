# -*- coding: utf-8 -*-
"""
用户 API 客户端
"""

from src.api.base_api import BaseAPI

class UserAPI(BaseAPI):
    def __init__(self, token=None):
        """初始化用户 API 客户端"""
        super().__init__()
        if token:
            self.token = token
    
    def reset_password(self, user_id, password=None):
        """重置用户密码"""
        endpoint = self.config['api']['user']['update_password']
        if password is None:
            password = self.config['test']['new_password']
        data = {
            "id": user_id,
            "password": password
        }
        headers = self.get_headers()
        response = self.put(endpoint, json=data, headers=headers)
        assert response["code"] == 200, f"重置密码失败: {response.get('msg')}"
        return response
