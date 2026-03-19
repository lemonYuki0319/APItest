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

    # 兼容旧用例/示例：部分用例里使用 cultural_asset_actions.login(mobile, password)
    # 这里将其视为 APP 端登录的别名，避免初学者运行时直接 AttributeError
    def login(self, mobile, password, code=""):
        """兼容方法：等价于 login_APP"""
        return self.login_APP(mobile, password, code)

    def login_APP(self, mobile, password, code=""):
        """APP端登录"""
        response = self.api.login_APP(mobile, password, code)
        if response.get("code") == 200:
            logger.info("APP端登录成功")
        else:
            logger.error(f"APP端登录失败: {response.get('msg')}")
        return response

    def login_WEB(self, tenantName, username, password,rememberMe=True):
        """WEB端登录"""
        response = self.api.login_WEB(tenantName, username, password,rememberMe)
        if response.get("code") == 200:
            logger.info("WEB端登录成功")
        else:
            logger.error(f"WEB端登录失败: {response.get('msg')}")
        return response

    def asset_Registration_Review(self,asset_data):
        """资产登记审核"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login_WEB("芋道源码", "admin", "Szxc@2024")
        response = self.api.asset_Registration_Review(asset_data)
        if response.get("code") == 200:
            logger.info("资产登记审核成功")
        else:
            logger.error(f"资产登记审核失败: {response.get('msg')}")
        return response

    def asset_Disclosure_Review(self,asset_data):
        """资产公示审核"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login_WEB("芋道源码", "admin", "Szxc@2024")
        response = self.api.asset_Disclosure_Review(asset_data)
        if response.get("code") == 200:
            logger.info("资产公示审核成功")
        else:
            logger.error(f"资产公示审核失败: {response.get('msg')}")
        return response

    def create_asset(self, asset_data):
        """文化资产登记"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login_APP("18800000091", "a123456")
        response, asset_id = self.api.create_asset(asset_data)
        if response.get("code") == 200:
            logger.info("文化资产登记成功")
        else:
            logger.error(f"文化资产登记失败: {response.get('msg')}")
        return response, asset_id

    def query_asset(self, pageNo=1, pageSize=10, cultureAssetName="", cultureAssetType="2997845276013892013"):
        """查询文化资产"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login_APP("18671450802", "a123456")
        response = self.api.query_asset(pageNo, pageSize, cultureAssetName, cultureAssetType)
        if response.get("code") == 200:
            logger.info("文化资产查询成功")
        else:
            logger.error(f"文化资产查询失败: {response.get('msg')}")
        return response

    def multi_turn_dialogue(self,asset_data):
        """多轮对话"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login_APP("18800000091", "a123456")
        # 注意：这里调用的是api.multi_turn_dialogue（小写），不是api.Multi_turn_Dialogue
        response = self.api.multi_turn_dialogue(asset_data)
        # 对于SSE流式响应，我们只需要检查响应状态码
        if response.status_code == 200:
            logger.info("多轮对话生成成功")
        else:
            logger.error(f"多轮对话生成失败，状态码: {response.status_code}")
        return response

    def query_registered_assets(self,pageNo=1,pageSize=10):
        """查询已注册资产"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login_WEB("芋道源码", "admin", "Szxc@2024")
        response = self.api.query_registered_assets(pageNo,pageSize)
        if response.get("code") == 200:
            logger.info("查询已注册资产成功")
        else:
            logger.error(f"查询已注册资产失败: {response.get('msg')}")
        return response

    def get_conversation(self,asset_data):
        """获取对话"""
        if not self.api.token:
            # 如果未登录，先登录
            self.login_APP("18800000091", "a123456")
        response, conversation_id = self.api.get_conversation(asset_data)
        if response.get("code") == 200:
            logger.info("获取对话成功")
        else:
            logger.error(f"获取对话失败: {response.get('msg')}")
        return response, conversation_id
