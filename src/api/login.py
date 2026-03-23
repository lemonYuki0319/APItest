# -*- coding: utf-8 -*-
"""
仅包含登录接口
"""

from src.api.base_api import BaseAPI

class LoginAPI(BaseAPI):
    def __init__(self, token=None):
        """初始化登录 API 客户端"""
        super().__init__()
        if token:
            self.token = token

    def login_APP(self, mobile, password, code=""):
        """APP端登录"""
        endpoint = "/converge-app-api/converge/auth/login"
        data = {
            "mobile": mobile,
            "password": password,
            "code": code
        }
        response = self.post(endpoint, json=data)
        if response.get("code") == 200:
            data_obj = response.get("data", {})
            self.token = data_obj.get("accessToken")
        return response

    def login_WEB(self, tenantName, username, password, rememberMe=True):
        """WEB端登录"""
        endpoint = "/admin-api/system/auth/login"
        data = {
            "tenantName": tenantName,
            "username": username,
            "password": password,
            "rememberMe": rememberMe
        }
        response = self.post(endpoint, json=data)
        if response.get("code") == 200:
            data_obj = response.get("data", {})
            self.token = data_obj.get("accessToken")
        return response

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