# tests 目录重构：single（单接口）+ flow（业务流程）

## Context

当前所有测试文件混在 `tests/test_Cultural_Assets/` 下，新手无法一眼区分"哪个是单接口测试、哪个是多接口业务流程"。用户要求把 tests 拆成两个顶层目录：
- `single/` — 单接口自动化（参数化、聚焦单个端点）
- `flow/` — 业务流程自动化（多接口串联、审核/公示等完整链路）

扁平结构，conftest.py 留在 tests/ 根。

## 目标结构

```
tests/
├── conftest.py                      # 保持在 tests/ 根（fixtures + sys.path 注入）
└── resources/                        # 不动（仅 pycache 残留，实际数据在项目根 resources/）
    └── ...

tests/single/                        # 单接口测试
├── test_error.py                    # 数据驱动：登录 + 创建 单接口参数化
└── test_cultural_asset.py            # 登录/创建/查询（带 allure，保持原样）

tests/flow/                          # 业务流程测试
├── test_register_asset_qywh.py      # 企业文化资产 全流程（含 DB 校验+清理）
├── test_register_asset_symm.py      # 商业秘密资产 全流程
├── test_register_asset_szsb.py      # 数字商标资产 全流程
└── test_AI_Multi_turn_Dialogue.py    # AI 多轮对话 全流程
```

删除空的 `tests/test_Cultural_Assets/` 目录及其 `__pycache__`。

## 为什么安全（已核对）

1. **conftest.py 在 tests/ 根**：[tests/conftest.py:15-16](file:///e:/python_project/APItest/tests/conftest.py#L15-L16) 注入 `PROJECT_ROOT` 到 sys.path；pytest 向上发现 conftest 机制保证 `tests/single/` 和 `tests/flow/` 都能用 fixtures（login_actions / cultural_asset_actions / db）和 `from src...` 导入。
2. **pytest.ini 无 testpaths**：[pytest.ini](file:///e:/python_project/APItest/pytest.ini) 未配 testpaths，`python_files = test_*.py *_test.py` 是通用模式，移动后 `pytest tests/` 照常递归收集。
3. **TESTDATA_DIR 是绝对路径**：[config/constants.py:24](file:///e:/python_project/APItest/config/constants.py#L24) `TESTDATA_DIR = PROJECT_ROOT/resources/testdata`，test_error.py 从 single/ 加载 yaml 不受影响。
4. **无跨文件导入**：每个测试文件只用 fixtures，相互独立，移动不产生导入链断裂。
5. **不加 `__init__.py`**：原 `test_Cultural_Assets/` 没有 `__init__.py` 也能跑，保持一致。

## 执行步骤

1. 新建目录 `tests/single/` 和 `tests/flow/`（用 Shell `New-Item -ItemType Directory`）。
2. 用 PowerShell `Move-Item` 移动文件：
   - `test_error.py`、`test_cultural_asset.py` → `tests/single/`
   - `test_register_asset_qywh.py`、`test_register_asset_symm.py`、`test_register_asset_szsb.py`、`test_AI_Multi_turn_Dialogue.py` → `tests/flow/`
3. 删除空的 `tests/test_Cultural_Assets/`（含其 `__pycache__`）。
4. 清理 `tests/__pycache__/`（避免 conftest 旧缓存影响）。

## 验证

1. 整体收集：`python -m pytest tests/ --collect-only -q` —— 应收集到全部用例（预期约 38 条），无 import error。
2. 单目录验证：
   - `python -m pytest tests/single/ --collect-only -q`
   - `python -m pytest tests/flow/ --collect-only -q`
3. 真跑一条（确认 fixtures/sys.path 正常）：`python -m pytest tests/flow/test_register_asset_qywh.py -s` —— 应 PASSED，DB 连接 + 清理正常。

## 不做（保持范围）

- 不动 conftest.py 内容（除非验证发现需要）。
- 不改测试代码本身（allure 装饰器、断言逻辑等保持原样）。
- 不改 README（如需同步路径说明，用户后续单独提）。
- 不删 `tests/resources/`（仅 pycache，无实际数据，留着无害；若要清也可顺带删 pycache）。
