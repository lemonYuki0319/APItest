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

## 3. 项目结构（以仓库实际为准）

```
APItest/
├── config/                       # 配置中心
│   ├── config.yaml               # 环境、账号、API 等配置
│   ├── config.py                 # 配置加载（带缓存）
│   ├── constants.py              # 项目路径常量
├── src/                          # 核心代码层
│   ├── api/                      # API 客户端封装
│   │   ├── base_api.py           # 统一 request 封装（timeout/重试/日志/响应落盘）
│   │   ├── auth_api.py           # WEB 管理端登录
│   │   ├── user_api.py           # 用户相关 API（示例：重置密码）
│   │   └── cultural_asset_api.py # 文化资产相关 API（含 SSE 流式示例）
│   ├── actions/                  # 业务动作层（组合多个 API）
│   │   ├── user_actions.py
│   │   └── cultural_asset_actions.py
│   └── utils/                    # 通用工具
│       ├── logger.py             # 控制台+文件日志
│       ├── data_utils.py         # YAML 测试数据读取（支持 limit）
│       └── config.py             # 兼容层：转发到 config/config.py（避免重复实现）
├── resources/                    # 测试资产
│   ├── endpoints/api_endpoints.yaml  # 端点示例（建议后续统一收敛到一处）
│   └── testdata/
│       ├── user_data.yaml        # user_id 列表（用于数据驱动）
│       ├── testcases.md          # 用例设计文档（示例）
│       └── api_testcases.md      # 更详细的接口测试用例文档（示例）
├── tests/                        # pytest 用例
│   ├── conftest.py               # fixtures（登录、client/actions）
│   └── test_Cultural_Assets/     # 示例：文化资产 + 重置密码等用例
├── scripts/
│   └── run.py                    # 一键运行入口（支持生成 allure results / report）
├── reports/
│   ├── allure-results/           # Allure 原始数据（脚本运行生成）
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
pytest tests/test_Cultural_Assets/test_reset_password.py -v
```

运行某个用例：
```bash
pytest tests/test_Cultural_Assets/test_reset_password.py::test_reset_password_parametrize -v
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
- `admin.*`：管理端登录账号（示例中为明文，建议本地化管理，见下文）
- `test.verify_ssl`：是否校验 HTTPS 证书（调试环境可关闭）

---

## 6. 数据驱动说明（resources/testdata/user_data.yaml）

`src/utils/data_utils.py` 提供：
- `DataUtils.get_user_ids(limit=None)`：读取 user_id 列表  
  - `limit=5`：适合初学者快速跑通（本项目默认用 5 条）
  - `limit=None`：全量读取（适合压测/全量回归）

---

## 7. 框架分层（学习建议）

1. **BaseAPI（src/api/base_api.py）**  
   学习点：统一 request 封装、timeout、重试、header/token 注入、异常处理、响应落盘。
2. **API 层（src/api/*.py）**  
   学习点：每个业务模块一个 Client 类，只写“接口层面的输入输出”。
3. **Actions 层（src/actions/*.py）**  
   学习点：把“登录->业务接口->校验/日志”串成可复用业务动作，供测试用例直接调用。
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

- 端点配置存在两处来源：`config/config.yaml` 与 `resources/endpoints/api_endpoints.yaml`，建议统一收敛
- Allure 报告目前仅输出用例结果，后续可将请求/响应作为附件写入（更利于接口排障）
- “长耗时/依赖外部状态”的用例建议用 marker 标记为 slow，默认不跑
