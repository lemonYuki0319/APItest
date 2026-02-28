# -*- coding: utf-8 -*-
"""
日志工具类
"""

import logging
import os
from config.constants import LOGS_DIR
from config.config import get_config

class Logger:
    def __init__(self, name=__name__):
        """初始化日志记录器"""
        # 确保日志目录存在
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # 获取配置
        config = get_config()
        log_level = getattr(logging, config['log']['level'])
        log_format = config['log']['format']
        date_format = config['log']['date_format']
        
        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(logging.Formatter(log_format, date_format))
            
            # 文件处理器
            log_file = os.path.join(LOGS_DIR, 'test.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(logging.Formatter(log_format, date_format))
            
            # 添加处理器
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """记录调试信息"""
        self.logger.debug(message)
    
    def info(self, message):
        """记录信息"""
        self.logger.info(message)
    
    def warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录错误信息"""
        self.logger.error(message)
    
    def critical(self, message):
        """记录严重错误信息"""
        self.logger.critical(message)

# 创建全局日志实例
logger = Logger()
