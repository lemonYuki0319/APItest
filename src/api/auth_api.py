# -*- coding: utf-8 -*-
"""
认证 API 客户端
"""

from src.api.base_api import BaseAPI

class AuthAPI(BaseAPI):
    def login(self):
        """管理员登录"""
        endpoint = self.config['api']['auth']['login']
        data = {
            "tenantName": self.config['admin']['tenant_name'],
            "username": self.config['admin']['username'],
            "password": self.config['admin']['password'],
            "rememberMe": self.config['admin']['remember_me']
        }
        response = self.post(endpoint, json=data)
        assert response["code"] == 200, f"登录失败: {response.get('msg')}"
        self.token = response["data"]["accessToken"]
        return self.token
