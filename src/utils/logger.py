# -*- coding: utf-8 -*-
"""
日志工具类 - 统一的日志记录封装

提供控制台和文件双输出的日志记录功能，支持按日期分割日志文件。
"""

import logging
import os
from datetime import datetime
from config.constants import LOGS_DIR
from config.config import get_config


class Logger:
    """
    日志记录器封装类
    
    特性：
    - 支持控制台和文件双输出
    - 日志文件按日期自动分割
    - 支持自定义日志级别和名称
    - 单例模式避免重复创建 handler
    
    示例：
        >>> logger = Logger('my_module').get_logger()
        >>> logger.info("这是一条信息日志")
        >>> logger.error("这是一条错误日志")
    """
    
    def __init__(self, name: str = 'interface_test', log_level: int | None = None) -> None:
        """
        初始化日志记录器
        
        Args:
            name: logger 名称，用于区分不同模块的日志
            log_level: 日志级别（可选），默认从配置文件读取
                      可选值：logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
        """
        # 确保日志目录存在
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # 获取配置
        config = get_config()
        
        # 设置日志级别（优先使用参数，否则从配置读取）
        actual_level: int
        if log_level is not None:
            actual_level = log_level
        else:
            config_level = config.get('log', {}).get('level', 'INFO')
            actual_level = getattr(logging, config_level, logging.INFO)
        
        # 设置日志格式（从配置读取或使用默认格式）
        log_format = config.get('log', {}).get(
            'format', 
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        date_format = config.get('log', {}).get('date_format', '%Y-%m-%d %H:%M:%S')
        
        # 创建日志记录器
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(actual_level)
        
        # 避免重复添加处理器（单例模式关键）
        if not self.logger.handlers:
            # 创建格式化器
            formatter = logging.Formatter(log_format, date_format)
            
            # 1. 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(actual_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # 2. 文件处理器（按日期命名）
            log_file = os.path.join(
                LOGS_DIR,
                f'{datetime.now().strftime("%Y%m%d")}.log'
            )
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(actual_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def get_logger(self) -> logging.Logger:
        """
        获取 logger 实例
        
        Returns:
            logging.Logger: 标准库 logger 实例，可直接调用 info/error 等方法
        """
        return self.logger
    
    def debug(self, message: str) -> None:
        """记录调试信息"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """记录信息"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录警告信息"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """记录错误信息"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """记录严重错误信息"""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """
        记录异常信息（自动包含堆栈跟踪）
        
        Args:
            message: 异常描述信息
        """
        self.logger.exception(message)


# 创建全局日志实例（默认使用）
logger: logging.Logger = Logger().get_logger()


# ============================================
# 使用示例
# ============================================
if __name__ == '__main__':
    # 方式1: 使用全局 logger 实例（推荐）
    from src.utils.logger import logger
    
    logger.debug("这是一条调试日志")
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
    logger.critical("这是一条严重错误日志")
    
    # 方式2: 创建自定义 logger（适用于特定模块）
    from src.utils.logger import Logger
    
    custom_logger = Logger('my_module').get_logger()
    custom_logger.info("自定义模块的日志")
    
    # 方式3: 自定义日志级别
    debug_logger = Logger('debug_module', log_level=logging.DEBUG).get_logger()
    debug_logger.debug("调试模式的详细日志")
