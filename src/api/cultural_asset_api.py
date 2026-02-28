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
    
    def login(self, mobile, password, code=""):
        """用户登录"""
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
    
    def create_asset(self, asset_data):
        """创建文化资产"""
        endpoint = "/api/converge-app-api/digital/culture/asset/create"
        headers = self.get_headers()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        response = self.post(endpoint, json=asset_data, headers=headers)
        return response

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