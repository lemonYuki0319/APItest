# -*- coding: utf-8 -*-
"""
Allure 报告辅助工具类

提供统一的 Allure 报告封装，简化测试用例中的 Allure 操作。
包括：测试步骤、附件添加、标签管理、动态描述等功能。
allure serve reports/allure-results打开报告
"""

import json
import allure
from functools import wraps
from typing import Any, Callable, Optional


class AllureHelper:
    """
    Allure 报告辅助类
    
    功能：
    - 统一的测试步骤封装
    - 自动添加请求/响应附件
    - 支持动态标题和描述
    - 提供常用标签快捷方法
    
    使用示例：
        >>> from src.utils.allure_helper import AllureHelper
        >>> 
        >>> @AllureHelper.step("执行登录操作")
        >>> def login(username, password):
        ...     # 登录逻辑
        ...     AllureHelper.attach_request("POST", "/login", {"username": username})
        ...     AllureHelper.attach_response(response)
    """
    
    @staticmethod
    def step(title: str):
        """
        测试步骤装饰器
        
        Args:
            title: 步骤标题
            
        Returns:
            装饰器函数
            
        示例：
            >>> @AllureHelper.step("用户登录")
            >>> def test_login():
            ...     pass
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                with allure.step(title):
                    return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def attach_request(method: str, url: str, data: Optional[dict] = None, 
                       headers: Optional[dict] = None, name: str = "请求信息"):
        """
        添加请求信息附件
        
        Args:
            method: HTTP 方法 (GET/POST/PUT/DELETE)
            url: 请求 URL
            data: 请求数据
            headers: 请求头
            name: 附件名称
        """
        request_info = {
            "method": method,
            "url": url,
            "headers": headers or {},
            "data": data or {}
        }
        
        content = json.dumps(request_info, ensure_ascii=False, indent=2)
        allure.attach(
            content,
            name=name,
            attachment_type=allure.attachment_type.JSON
        )
    
    @staticmethod
    def attach_response(response: Any, name: str = "响应信息"):
        """
        添加响应信息附件
        
        Args:
            response: 响应对象或字典
            name: 附件名称
        """
        if hasattr(response, 'json'):
            try:
                content = json.dumps(response.json(), ensure_ascii=False, indent=2)
            except:
                content = str(response.text)
        elif isinstance(response, dict):
            content = json.dumps(response, ensure_ascii=False, indent=2)
        else:
            content = str(response)
        
        allure.attach(
            content,
            name=name,
            attachment_type=allure.attachment_type.JSON
        )
    
    @staticmethod
    def attach_text(content: str, name: str = "文本信息"):
        """
        添加文本附件
        
        Args:
            content: 文本内容
            name: 附件名称
        """
        allure.attach(
            content,
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )
    
    @staticmethod
    def attach_image(file_path: str, name: str = "截图"):
        """
        添加图片附件
        
        Args:
            file_path: 图片文件路径
            name: 附件名称
        """
        allure.attach.file(
            file_path,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    
    @staticmethod
    def set_title(title: str):
        """
        设置测试用例标题
        
        Args:
            title: 标题内容
        """
        allure.title(title)
    
    @staticmethod
    def set_description(description: str):
        """
        设置测试用例描述
        
        Args:
            description: 描述内容
        """
        allure.description(description)
    
    @staticmethod
    def set_severity(level: str):
        """
        设置测试用例严重程度
        
        Args:
            level: 严重程度级别
                  blocker, critical, normal, minor, trivial
        """
        severity_map = {
            "blocker": allure.severity_level.BLOCKER,
            "critical": allure.severity_level.CRITICAL,
            "normal": allure.severity_level.NORMAL,
            "minor": allure.severity_level.MINOR,
            "trivial": allure.severity_level.TRIVIAL
        }
        allure.severity(severity_map.get(level, allure.severity_level.NORMAL))
    
    @staticmethod
    def add_tag(*tags: str):
        """
        添加标签
        
        Args:
            *tags: 标签名称列表
        """
        for tag in tags:
            allure.tag(tag)
    
    @staticmethod
    def add_feature(name: str):
        """
        添加功能模块标签
        
        Args:
            name: 功能模块名称
        """
        allure.feature(name)
    
    @staticmethod
    def add_story(name: str):
        """
        添加用户故事标签
        
        Args:
            name: 用户故事名称
        """
        allure.story(name)
    
    @staticmethod
    def add_link(url: str, name: str = "链接", link_type: str = "link"):
        """
        添加链接
        
        Args:
            url: 链接地址
            name: 链接名称
            link_type: 链接类型 (link, issue, test_case)
        """
        link_type_map = {
            "link": allure.link,
            "issue": allure.issue,
            "test_case": allure.testcase
        }
        link_func = link_type_map.get(link_type, allure.link)
        link_func(url, name=name)


# 便捷函数，直接通过模块调用
def step(title: str):
    """便捷函数：创建测试步骤装饰器"""
    return AllureHelper.step(title)


def attach_request(method: str, url: str, data: Optional[dict] = None, 
                   headers: Optional[dict] = None, name: str = "请求信息"):
    """便捷函数：添加请求附件"""
    AllureHelper.attach_request(method, url, data, headers, name)


def attach_response(response: Any, name: str = "响应信息"):
    """便捷函数：添加响应附件"""
    AllureHelper.attach_response(response, name)


def attach_text(content: str, name: str = "文本信息"):
    """便捷函数：添加文本附件"""
    AllureHelper.attach_text(content, name)


def set_title(title: str):
    """便捷函数：设置标题"""
    AllureHelper.set_title(title)


def set_description(description: str):
    """便捷函数：设置描述"""
    AllureHelper.set_description(description)


def set_severity(level: str):
    """便捷函数：设置严重程度"""
    AllureHelper.set_severity(level)


def add_feature(name: str):
    """便捷函数：添加功能标签"""
    AllureHelper.add_feature(name)


def add_story(name: str):
    """便捷函数：添加故事标签"""
    AllureHelper.add_story(name)
