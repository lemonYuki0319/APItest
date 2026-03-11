# -*- coding: utf-8 -*-
"""
文化资产 API 客户端
"""

from src.api.base_api import BaseAPI
import json

class CulturalAssetAPI(BaseAPI):
    def __init__(self, token=None):
        """初始化文化资产 API 客户端"""
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

    def login_WEB(self, tenantName, username, password,rememberMe=True):
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

    def asset_Registration_Review(self,asset_data):
        """资产登记审核"""
        endpoint = "/admin-api/digital/culture/asset/audit"
        headers = self.get_headers()
        headers["Accept"] = "application/json, text/plain, */*"
        response = self.put(endpoint, json=asset_data, headers=headers)
        return response

    def asset_Disclosure_Review(self,asset_data):
        """资产公示审核"""
        endpoint = "/admin-api/digital/culture/asset/update-notice-status"
        headers = self.get_headers()
        headers["Accept"] = "application/json, text/plain, */*"
        response = self.put(endpoint, json=asset_data, headers=headers)
        return response


    def create_asset(self, asset_data):
        """创建文化资产"""
        endpoint = "/api/converge-app-api/digital/culture/asset/create"
        headers = self.get_headers()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        response = self.post(endpoint, json=asset_data, headers=headers)
        asset_id = None
        if response.get("code") == 200:
            asset_id = response.get("data")
        return response, asset_id

    def query_asset(self,pageNo=1,pageSize=10,cultureAssetName="",cultureAssetType="2997845276013892013"):
        """查询资产管理"""
        endpoint = f"/api/converge-app-api/digital/culture/asset/page"
        headers = self.get_headers()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        params = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "cultureAssetName": cultureAssetName,
            "cultureAssetType": cultureAssetType
        }
        headers["Accept"] = "application/json, text/plain, */*"
        response = self.get(endpoint, headers=headers,params=params)
        return response

    def multi_turn_dialogue(self,asset_data):
        """多轮对话"""
        endpoint = "/api/converge-app-api/ai/assistant/common/stream"
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        headers["Accept"] = "text/event-stream, text/event-stream"
        # 直接使用session.post，不使用父类的post方法，因为需要处理SSE流式响应
        response = self.session.post(url, json=asset_data, headers=headers, stream=True)
        # 返回响应对象，而不是尝试解析为JSON
        return response

    def query_registered_assets(self,pageNo=1,pageSize=10):
        """查询登记资产"""
        endpoint = "/admin-api/digital/culture/asset/page"
        headers = self.get_headers()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        params = {
            "pageNo": pageNo,
            "pageSize": pageSize
        }
        headers["Accept"] = "application/json, text/plain, */*"
        response = self.get(endpoint, headers=headers,params=params)
        return response

    def get_conversation(self,asset_data):
        """获取对话"""
        endpoint = "/api/converge-app-api/ai/chat/conversation/create-my"
        headers = self.get_headers()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        response = self.post(endpoint, json=asset_data, headers=headers)
        conversation_id = None
        if response.get("code") == 200:
            conversation_id = response.get("data", {}).get("id")
        return response, conversation_id
