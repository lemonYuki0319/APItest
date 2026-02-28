# -*- coding: utf-8 -*-
"""
API 基础类，封装通用的 HTTP 请求方法
"""

import requests
import yaml
import os
from config.constants import CONFIG_DIR

class BaseAPI:
    def __init__(self):
        """初始化 API 客户端"""
        # 加载配置
        config_path = os.path.join(CONFIG_DIR, 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.base_url = self.config['env']['base_url']
        self.timeout = self.config['env']['timeout']
        self.verify_ssl = self.config['test']['verify_ssl']
        
        # 创建会话
        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        self.session.timeout = self.timeout
        
        # 存储 token
        self.token = None
    
    def get(self, endpoint, params=None, headers=None):
        """发送 GET 请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, headers=headers)
        return response.json()
    
    def post(self, endpoint, json=None, data=None, headers=None):
        """发送 POST 请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=json, data=data, headers=headers)
        return response.json()
    
    def put(self, endpoint, json=None, data=None, headers=None):
        """发送 PUT 请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=json, data=data, headers=headers)
        return response.json()
    
    def delete(self, endpoint, headers=None):
        """发送 DELETE 请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, headers=headers)
        return response.json()
    
    def get_headers(self):
        """获取带认证信息的请求头"""
        headers = {
            "Accept": "application/json, text/plain, */*"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
