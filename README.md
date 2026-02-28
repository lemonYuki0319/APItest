# API 测试项目

## 项目简介

这是一个基于 pytest 的 API 测试项目，用于测试华军 API 接口，主要包括登录认证和用户密码重置功能。

## 项目结构

```
APItest/ 
├── config/                       # 配置中心
│   ├── config.yaml               # 环境、API 等配置
│   └── constants.py              # 项目路径常量
├── src/                           # 核心代码层
│   ├── api/                      # API 客户端
│   │   ├── base_api.py           # API 基础类
│   │   ├── auth_api.py           # 认证 API
│   │   └── user_api.py           # 用户 API
│   ├── actions/                   # 业务动作层
│   │   └── user_actions.py       # 用户业务流程
│   └── utils/                     # 通用工具类
│       ├── config.py              # 配置工具
│       ├── data_utils.py          # 数据工具
│       └── logger.py              # 日志工具
├── tests/                          # 测试用例层
│   ├── conftest.py                 # pytest fixtures
│   ├── test_auth/                 # 认证模块测试
│   │   └── test_login.py          # 登录测试用例
│   └── test_user/                 # 用户模块测试
│       └── test_reset_password.py # 密码重置测试用例
├── resources/                      # 测试资产
│   ├── testdata/                   # 测试数据
│   │   └── 用户数据.xls            # 用户 ID 数据
│   ├── images/                      # 测试图片
│   └── endpoints/                  # API 端点配置
│       └── api_endpoints.yaml     # API 端点定义
├── reports/                         # 测试报告与日志
│   ├── allure-results/              # Allure 原始数据
│   ├── logs/                        # 运行日志
│   └── response/                    # API 响应结果
├── scripts/                         # 运维脚本
│   └── run.py                       # 测试执行入口
├── requirements.txt                 # 项目依赖
├── pytest.ini                       # pytest 配置
└── README.md                        # 项目文档
```

## 环境要求

- Python 3.8+
- pip 包管理工具

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

### 方法 1：使用 pytest 直接运行

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_user/test_reset_password.py -v

# 运行指定测试用例
pytest tests/test_user/test_reset_password.py::test_reset_password -v
```

### 方法 2：使用运行脚本

```bash
# 运行所有测试
python scripts/run.py

# 运行指定测试目录
python scripts/run.py --path tests/test_user/

# 运行测试并生成报告
python scripts/run.py --generate-report
```

## 配置文件

### config.yaml

主要配置项：
- `env`: 环境配置，包括 base_url、timeout 等
- `admin`: 管理员登录凭据
- `api`: API 端点配置
- `test`: 测试相关配置
- `log`: 日志配置

### pytest.ini

pytest 运行配置，包括：
- 运行选项
- 测试文件模式
- 警告过滤器
- 日志配置
- Allure 报告配置

## 测试数据

用户 ID 数据存储在 `resources/testdata/用户数据.xls` 文件中，脚本会自动读取该文件中的用户 ID 进行测试。

## 报告生成

项目使用 Allure 生成测试报告：

1. 安装 Allure 命令行工具
2. 运行测试时添加 `--generate-report` 参数
3. 报告将生成在 `reports/allure-report` 目录

## 日志记录

测试运行日志会记录在：
- 控制台输出
- `reports/logs/pytest.log` 文件

## 注意事项

1. 请确保 `config.yaml` 中的配置信息正确
2. 测试前请确保网络连接正常
3. 运行测试时会自动处理 SSL 证书验证警告

## 扩展指南

1. **添加新的 API 测试**：
   - 在 `src/api/` 目录下创建新的 API 客户端类
   - 在 `src/actions/` 目录下创建对应的业务动作类
   - 在 `tests/` 目录下创建测试用例

2. **添加新的测试数据**：
   - 在 `resources/testdata/` 目录下添加数据文件
   - 在 `src/utils/data_utils.py` 中添加相应的读取方法

3. **修改配置**：
   - 编辑 `config/config.yaml` 文件修改配置信息
   - 编辑 `pytest.ini` 文件修改 pytest 运行配置
