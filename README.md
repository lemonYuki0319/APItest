# API 接口自动化测试项目（pytest + requests）

> 目标：提供一个**可直接上手学习**的接口自动化项目模板，包含：
> - 配置中心（环境/base_url/超时/重试/账号）
> - API Client 层（统一请求封装）
> - Actions 业务动作层（组合登录+业务流程）
> - pytest 用例层（fixture、参数化、数据驱动）
> - 日志与 Allure 报告产出

---

## 1. 环境要求

- Python 3.10+（推荐 3.12）
- pip

> 若要生成并打开 Allure 报告，还需要安装 `allure-commandline`（系统命令行工具）。

---

## 2. 安装依赖

```bash
pip install -r requirements.txt
```

### Allure 命令行安装说明
- Windows：可通过 scoop/choco 安装，或手动下载安装包配置环境变量
- 安装完成后验证：
```bash
allure --version
```

---

## 3. 项目结构

```
APItest/
├── config/                       # 配置中心
│   ├── config.yaml               # 环境、账号、API 等配置
│   ├── config.py                 # 配置加载（带缓存）
│   └── constants.py              # 项目路径常量
├── src/                          # 核心代码层
│   ├── api/                      # API 客户端封装
│   │   ├── base_api.py           # 统一 request 封装（timeout/重试/日志/响应落盘）
│   │   ├── login.py              # 登录相关 API（APP端/WEB端）
│   │   └── cultural_assets/      # 文化资产 API 模块
│   │       └── cultural_asset_api.py
│   ├── actions/                  # 业务动作层（组合多个 API）
│   │   ├── login.py              # 登录动作（APP端/WEB端）
│   │   └── cultural_assets/      # 文化资产动作模块
│   │       └── cultural_asset_actions.py
│   └── utils/                    # 通用工具
│       ├── logger.py             # 控制台+文件日志
│       ├── data_utils.py         # YAML 测试数据读取（支持 limit）
│       └── config.py             # 兼容层：转发到 config/config.py
├── resources/                    # 测试资产
│   ├── endpoints/
│   │   └── api_endpoints.yaml    # API 端点配置
│   └── testdata/
│       └── user_data.yaml        # user_id 列表（用于数据驱动）
├── tests/                        # pytest 用例
│   ├── conftest.py               # fixtures（登录、client/actions）
│   └── test_Cultural_Assets/     # 文化资产测试用例
│       ├── test_cultural_asset.py      # 登录测试用例
│       ├── test_register_asset_qywh.py # 企业文化资产登记
│       ├── test_register_asset_symm.py # 数字商标资产登记
│       ├── test_register_asset_szsb.py # 数字商标资产登记
│       └── test_reset_password.py      # 重置密码测试
├── scripts/
│   └── run.py                    # 一键运行入口
├── reports/
│   ├── logs/                     # 运行日志
│   └── response/                 # BaseAPI 自动落盘的请求响应（便于排障）
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 4. 快速运行

### 4.1 直接 pytest 运行
```bash
pytest
```

运行某个文件：
```bash
pytest tests/test_Cultural_Assets/test_cultural_asset.py -v
```

运行某个用例：
```bash
pytest tests/test_Cultural_Assets/test_cultural_asset.py::test_login_success -v
```

### 4.2 使用脚本运行（推荐新手）
```bash
python scripts/run.py
```

指定目录/文件：
```bash
python scripts/run.py --path tests/test_Cultural_Assets/
```

生成并打开 Allure 报告：
```bash
python scripts/run.py --generate-report
```

---

## 5. 配置说明（config/config.yaml）

常用配置项：
- `env.base_url`：接口域名
- `env.timeout`：请求超时（秒）
- `env.retry_count`：失败重试次数（BaseAPI 已支持）
- `admin.*`：管理端登录账号
- `test.verify_ssl`：是否校验 HTTPS 证书（调试环境可关闭）

---

## 6. Fixture 使用说明

项目使用 pytest fixture 管理测试依赖，所有 fixture 定义在 `tests/conftest.py` 中：

| Fixture | 说明 | 使用场景 |
|---------|------|----------|
| `login_actions` | 登录动作实例 | 需要登录的测试用例 |
| `cultural_asset_actions` | 文化资产业务动作实例 | 文化资产相关测试 |
| `web_api` | 已登录的 WEB 端 API | 需要管理员权限的接口测试 |
| `app_api` | 已登录的 APP 端 API | 需要用户权限的接口测试 |

使用示例：
```python
def test_login_success(login_actions):
    """测试登录"""
    response = login_actions.login_APP("18671450802", "Aa123456")
    assert response.get("code") == 200

def test_create_asset(cultural_asset_actions, login_actions):
    """测试创建资产"""
    # 先登录
    login_actions.login_APP("18671450802", "Aa123456")
    cultural_asset_actions.api.token = login_actions.api.token
    
    # 执行业务操作
    response, asset_id = cultural_asset_actions.create_asset(asset_data)
    assert response.get("code") == 200
```

---

## 7. 框架分层（学习建议）

1. **BaseAPI（src/api/base_api.py）**  
   学习点：统一 request 封装、timeout、重试、header/token 注入、异常处理、响应落盘。

2. **API 层（src/api/*.py）**  
   学习点：每个业务模块一个 Client 类，只写"接口层面的输入输出"。
   - `login.py`：APP端/WEB端登录 API
   - `cultural_assets/cultural_asset_api.py`：文化资产相关 API

3. **Actions 层（src/actions/*.py）**  
   学习点：把"登录->业务接口->校验/日志"串成可复用业务动作，供测试用例直接调用。
   - `login.py`：登录动作封装
   - `cultural_assets/cultural_asset_actions.py`：文化资产业务动作

4. **Tests 层（tests/）**  
   学习点：pytest fixture、参数化、断言、报告维度。

---

## 8. 安全与可维护性建议（重要）

当前仓库中存在**明文账号/密码**（包括 `config.yaml` 与部分业务动作层的默认账号）。
建议实践：
- 使用环境变量或 `.env` 文件管理敏感信息（可选依赖 `python-dotenv`）
- 将本地配置文件加入 `.gitignore`（例如 `config/config.local.yaml`），避免提交到仓库

---

## 9. 已知可优化点（待办方向）

- 端点配置存在多处来源，建议统一收敛到 `config/config.yaml`
- Allure 报告目前仅输出用例结果，后续可将请求/响应作为附件写入（更利于接口排障）
- "长耗时/依赖外部状态"的用例建议用 marker 标记为 slow，默认不跑

---

## 10. Allure 报告使用

### 10.1 Allure 辅助类

项目提供了 `AllureHelper` 工具类（`src/utils/allure_helper.py`），封装了常用的 Allure 操作：

#### 主要功能

| 方法 | 说明 |
|------|------|
| `AllureHelper.step(title)` | 测试步骤装饰器 |
| `AllureHelper.attach_request(method, url, data, headers)` | 添加请求信息附件 |
| `AllureHelper.attach_response(response, name)` | 添加响应信息附件 |
| `AllureHelper.attach_text(content, name)` | 添加文本附件 |
| `AllureHelper.attach_image(file_path, name)` | 添加图片附件 |
| `AllureHelper.set_title(title)` | 设置测试用例标题 |
| `AllureHelper.set_description(description)` | 设置测试用例描述 |
| `AllureHelper.set_severity(level)` | 设置严重程度 |
| `AllureHelper.add_feature(name)` | 添加功能模块标签 |
| `AllureHelper.add_story(name)` | 添加用户故事标签 |

#### 使用示例

```python
import allure
from src.utils.allure_helper import AllureHelper, attach_response

@allure.feature("登录模块")
@allure.story("APP端登录")
class TestLogin:
    
    @allure.title("正确的手机号和密码登录")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, login_actions):
        with allure.step("步骤1: 执行APP端登录"):
            response = login_actions.login_APP("18671450802", "Aa123456")
            attach_response(response, "登录响应")  # 添加响应附件
        
        with allure.step("步骤2: 验证响应结果"):
            assert response.get("code") == 200
            AllureHelper.attach_text("登录成功", "验证结果")
```

### 10.2 生成 Allure 报告

```bash
# 运行测试并生成 Allure 结果
pytest --alluredir=reports/allure-results

# 生成并打开 HTML 报告
allure serve reports/allure-results

# 或者生成静态报告
allure generate reports/allure-results -o reports/allure-report --clean
```

### 10.3 使用脚本一键生成报告

```bash
python scripts/run.py --generate-report
```

---

## 11. 模块说明

### 11.1 登录模块（src/actions/login.py）

提供 APP 端和 WEB 端登录功能：
- `login_APP(mobile, password, code)`：APP 端登录
- `login_WEB(tenantName, username, password, rememberMe)`：WEB 端登录
- `reset_password(user_id, password)`：重置用户密码

### 11.2 文化资产模块（src/actions/cultural_assets/）

提供文化资产全生命周期管理：
- `create_asset(asset_data)`：登记文化资产
- `query_asset(**kwargs)`：查询文化资产列表
- `asset_Registration_Review(asset_data)`：资产登记审核
- `asset_Disclosure_Review(asset_data)`：资产公示审核

### 11.3 Allure 辅助模块（src/utils/allure_helper.py）

提供 Allure 报告封装功能，简化测试用例中的 Allure 操作。
