# -*- coding: utf-8 -*-
"""
文化资产业务动作层
"""

from src.api.cultural_asset_api import CulturalAssetAPI
from src.utils.logger import logger

class CulturalAssetActions:
    def __init__(self):
        """初始化文化资产业务动作"""
        self.api = CulturalAssetAPI()
    
    def login(self, mobile, password, code=""):
        """用户登录"""
        response = self.api.login(mobile, password, code)
        if response.get("code") == 200:
            logger.info("用户登录成功")
        else:
            logger.error(f"用户登录失败: {response.get('msg')}")
        return response
    
    def create_asset(self, asset_data):
        """创建文化资产"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login("18671450802", "a123456")
        response = self.api.create_asset(asset_data)
        if response.get("code") == 200:
            logger.info("文化资产创建成功")
        else:
            logger.error(f"文化资产创建失败: {response.get('msg')}")
        return response

    def query_asset(self, pageNo=1, pageSize=10, cultureAssetName="", cultureAssetType="2997845276013892013"):
        """查询文化资产"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login("18671450802", "a123456")
        response = self.api.query_asset(pageNo, pageSize, cultureAssetName, cultureAssetType)
        if response.get("code") == 200:
            logger.info("文化资产查询成功")
        else:
            logger.error(f"文化资产查询失败: {response.get('msg')}")
        return response