# -*- coding: utf-8 -*-
"""
配置工具类
"""

import yaml
import os
from config.constants import CONFIG_DIR

_config = None

def get_config():
    """获取配置"""
    global _config
    if _config is None:
        config_path = os.path.join(CONFIG_DIR, 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            _config = yaml.safe_load(f)
    return _config

def get_env_config():
    """获取环境配置"""
    return get_config()['env']

def get_admin_config():
    """获取管理员配置"""
    return get_config()['admin']

def get_api_config():
    """获取 API 配置"""
    return get_config()['api']

def get_test_config():
    """获取测试配置"""
    return get_config()['test']


def get_database_config():
    """获取数据库配置"""
    return get_config().get('database', {})
