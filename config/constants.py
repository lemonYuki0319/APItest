# -*- coding: utf-8 -*-
"""
项目路径常量
"""

import os
import sys

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件目录
CONFIG_DIR = os.path.join(PROJECT_ROOT, 'config')

# 核心代码目录
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

# 测试用例目录
TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')

# 资源文件目录
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')

# 测试数据目录
TESTDATA_DIR = os.path.join(RESOURCES_DIR, 'testdata')

# 报告目录
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')

# 日志目录
LOGS_DIR = os.path.join(REPORTS_DIR, 'logs')

# 脚本目录
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')

# 添加项目根目录到 Python 路径
sys.path.insert(0, PROJECT_ROOT)
