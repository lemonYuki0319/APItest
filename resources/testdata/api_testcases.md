# 接口详细测试用例文档

## 文档信息
- **项目名称**: 数字文化资产平台API测试
- **文档版本**: v1.0
- **创建日期**: 2026-02-25
- **测试环境**: https://whhnhy.com:38868

---

## 目录
1. [登录接口 (/converge-app-api/converge/auth/login)](#1-登录接口)
2. [资产登记接口 (/api/converge-app-api/digital/culture/asset/create)](#2-资产登记接口)

---

## 1. 登录接口

### 1.1 接口基本信息

| 字段 | 值 |
|------|-----|
| 接口名称 | 用户登录 |
| 接口URL | /converge-app-api/converge/auth/login |
| 完整URL | https://whhnhy.com:38868/converge-app-api/converge/auth/login |
| 请求方法 | POST |
| Content-Type | application/json |
| 认证方式 | 无（公开接口） |
| 接口描述 | 用户通过手机号和密码登录系统，返回访问令牌 |

### 1.2 请求参数定义

#### Header参数
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| Content-Type | string | 是 | 请求内容类型 | application/json |

#### Body参数
| 参数名 | 类型 | 必填 | 长度限制 | 说明 | 示例值 |
|--------|------|------|----------|------|--------|
| mobile | string | 是 | 11 | 手机号码 | "18671450802" |
| password | string | 是 | 6-20 | 登录密码 | "a123456" |
| code | string | 否 | - | 验证码（可选） | "" |

### 1.3 响应参数定义

#### 成功响应示例
```json
{
  "code": 200,
  "data": {
    "userId": "1913060399566032898",
    "accessToken": "71831e1e9afb403d8389fda376b25506",
    "refreshToken": "e6c88d94f5b146b98738229de0a58c8a",
    "expiresTime": 1774420577456,
    "cancelStatus": "0"
  },
  "msg": ""
}
```

#### 响应字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 响应状态码，200表示成功 |
| data | object | 响应数据对象 |
| data.userId | string | 用户唯一标识 |
| data.accessToken | string | 访问令牌，用于后续接口认证 |
| data.refreshToken | string | 刷新令牌，用于刷新accessToken |
| data.expiresTime | long | accessToken过期时间戳（毫秒） |
| data.cancelStatus | string | 用户注销状态，0表示正常 |
| msg | string | 响应消息，成功时为空字符串 |

#### 失败响应示例
```json
{
  "code": 400,
  "data": null,
  "msg": "用户名或密码错误"
}
```

### 1.4 详细测试用例

#### API-LOGIN-001: 正常登录流程
**用例名称**: 使用正确的手机号和密码成功登录

**前置条件**:
1. 用户已在系统中注册
2. 用户状态正常（未注销、未锁定）

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "18671450802",
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 200,
  "data": {
    "userId": "1913060399566032898",
    "accessToken": "valid_token_string",
    "refreshToken": "refresh_token_string",
    "expiresTime": 1774420577456,
    "cancelStatus": "0"
  },
  "msg": ""
}
```

**断言规则**:
- HTTP状态码 = 200
- response.code = 200
- response.data.userId 不为空
- response.data.accessToken 不为空
- response.data.refreshToken 不为空
- response.data.expiresTime > 当前时间戳
- response.data.cancelStatus = "0"
- response.msg = ""

---

#### API-LOGIN-002: 手机号参数缺失
**用例名称**: 请求体中不包含mobile参数

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "手机号不能为空"
}
```

**断言规则**:
- HTTP状态码 = 200 或 400
- response.code != 200
- response.msg 包含 "手机号" 关键词

---

#### API-LOGIN-003: 密码参数缺失
**用例名称**: 请求体中不包含password参数

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "18671450802",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "密码不能为空"
}
```

**断言规则**:
- HTTP状态码 = 200 或 400
- response.code != 200
- response.msg 包含 "密码" 关键词

---

#### API-LOGIN-004: 手机号为空字符串
**用例名称**: mobile字段存在但值为空字符串

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "",
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "手机号不能为空"
}
```

**断言规则**:
- response.code != 200

---

#### API-LOGIN-005: 密码为空字符串
**用例名称**: password字段存在但值为空字符串

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "18671450802",
  "password": "",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "密码不能为空"
}
```

**断言规则**:
- response.code != 200

---

#### API-LOGIN-006: 手机号格式错误-包含字母
**用例名称**: 手机号中包含非数字字符

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "1867145080a",
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "手机号格式不正确"
}
```

**断言规则**:
- response.code != 200

---

#### API-LOGIN-007: 手机号长度不足11位
**用例名称**: 手机号只有10位数字

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "1867145080",
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "手机号长度不正确"
}
```

**断言规则**:
- response.code != 200

---

#### API-LOGIN-008: 手机号长度超过11位
**用例名称**: 手机号有12位数字

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "1867145080222",
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "手机号长度不正确"
}
```

**断言规则**:
- response.code != 200

---

#### API-LOGIN-009: 密码错误
**用例名称**: 手机号正确但密码错误

**前置条件**: 用户已注册

**请求信息**:
```http
POST https://whhnhy.com::38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "18671450802",
  "password": "wrongpassword",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 401,
  "data": null,
  "msg": "用户名或密码错误"
}
```

**断言规则**:
- response.code = 401 或 response.code != 200
- response.msg 包含 "错误" 或 "不正确"

---

#### API-LOGIN-010: 手机号不存在
**用例名称**: 使用未注册的手机号

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "13800138000",
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 404,
  "data": null,
  "msg": "用户不存在"
}
```

**断言规则**:
- response.code = 404 或 response.code != 200

---

#### API-LOGIN-011: SQL注入测试
**用例名称**: 在mobile字段尝试SQL注入

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "18671450802' OR '1'='1",
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "手机号格式不正确"
}
```

**断言规则**:
- response.code != 200
- 系统应拒绝SQL注入攻击

---

#### API-LOGIN-012: XSS攻击测试
**用例名称**: 在mobile字段尝试XSS攻击

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/converge-app-api/converge/auth/login
Content-Type: application/json

{
  "mobile": "18671450802<script>alert('XSS')</script>",
  "password": "a123456",
  "code": ""
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "手机号格式不正确"
}
```

**断言规则**:
- response.code != 200
- 系统应拒绝XSS攻击

---

---

## 2. 资产登记接口

### 2.1 接口基本信息

| 字段 | 值 |
|------|-----|
| 接口名称 | 数字文化资产登记 |
| 接口URL | /api/converge-app-api/digital/culture/asset/create |
| 完整URL | https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create |
| 请求方法 | POST |
| Content-Type | application/json;charset=UTF-8 |
| 认证方式 | Bearer Token |
| 接口描述 | 创建并登记新的数字文化资产 |

### 2.2 请求参数定义

#### Header参数
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| Accept | string | 是 | 接受的响应类型 | application/json, text/plain, */* |
| Content-Type | string | 是 | 请求内容类型 | application/json;charset=UTF-8 |
| Authorization | string | 是 | 访问令牌 | Bearer {accessToken} |

#### Body参数
**assetDetailValidJson**: JSON字符串，资产验证信息
```json
{
  "assetName": "测试资产",
  "assetType": "1",
  "assetCategory": "01",
  "description": "测试资产描述"
}
```

**assetDetailJson**: JSON字符串，资产详细信息
```json
{
  "creator": "测试创作者",
  "createTime": "2026-02-25",
  "resourceUrl": "https://example.com/resource"
}
```

### 2.3 响应参数定义

#### 成功响应示例
```json
{
  "code": 200,
  "data": "2026546800613134338",
  "msg": ""
}
```

#### 响应字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 响应状态码，200表示成功 |
| data | string | 新创建的资产ID |
| msg | string | 响应消息，成功时为空字符串 |

#### 失败响应示例
```json
{
  "code": 401,
  "data": null,
  "msg": "未授权访问"
}
```

### 2.4 详细测试用例

#### API-ASSET-001: 正常创建资产
**用例名称**: 使用有效token和完整参数成功创建资产

**前置条件**:
1. 已成功登录获取有效的accessToken
2. accessToken未过期

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Authorization: Bearer {valid_access_token}

{
  "assetDetailValidJson": "{\"assetName\":\"测试资产\",\"assetType\":\"1\",\"assetCategory\":\"01\"}",
  "assetDetailJson": "{\"creator\":\"测试创作者\",\"createTime\":\"2026-02-25\"}"
}
```

**预期响应**:
```json
{
  "code": 200,
  "data": "2026546800613134338",
  "msg": ""
}
```

**断言规则**:
- HTTP状态码 = 200
- response.code = 200
- response.data 不为空，且为字符串类型
- response.data 为纯数字字符串（资产ID）
- response.msg = ""

---

#### API-ASSET-002: 未携带Authorization头
**用例名称**: 请求头中缺少Authorization字段

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8

{
  "assetDetailValidJson": "{\"assetName\":\"测试资产\"}",
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 401,
  "data": null,
  "msg": "未授权访问"
}
```

**断言规则**:
- HTTP状态码 = 401
- response.code = 401 或 response.code != 200
- response.msg 包含 "未授权" 或 "认证" 关键词

---

#### API-ASSET-003: Authorization头格式错误
**用例名称**: Authorization头缺少Bearer前缀

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-88
Authorization: 71831e1e9afb403d8389fda376b25506

{
  "assetDetailValidJson": "{\"assetName\":\"测试资产\"}",
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 401,
  "data": null,
  "msg": "认证格式错误"
}
```

**断言规则**:
- HTTP状态码 = 401
- response.code != 200

---

#### API-ASSET-004: 使用无效Token
**用例名称**: Authorization头使用无效的token

**前置条件**: 无

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Authorization: Bearer invalid_token_12345

{
  "assetDetailValidJson": "{\"assetName\":\"测试资产\"}",
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 401,
  "data": null,
  "msg": "无效的访问令牌"
}
```

**断言规则**:
- HTTP状态码 = 401
- response.code = 401

---

#### API-ASSET-005: 使用过期Token
**用例名称**: Authorization头使用已过期的token

**前置条件**: 拥有已过期的token

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Authorization: Bearer {expired_token}

{
  "assetDetailValidJson": "{\"assetName\":\"测试资产\"}",
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 401,
  "data": null,
  "msg": "访问令牌已过期"
}
```

**断言规则**:
- HTTP状态码 = 401
- response.code = 401
- response.msg 包含 "过期" 关键词

---

#### API-ASSET-006: 请求体为空
**用例名称**: POST请求体为空

**前置条件**: 已获取有效accessToken

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Authorization: Bearer {valid_access_token}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "请求体不能为空"
}
```

**断言规则**:
- HTTP状态码 = 400
- response.code != 200

---

#### API-ASSET-007: 缺少assetDetailValidJson字段
**用例名称**: 请求体缺少必填字段assetDetailValidJson

**前置条件**: 已获取有效accessToken

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Authorization: Bearer {valid_access_token}

{
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "缺少必填字段：assetDetailValidJson"
}
```

**断言规则**:
- response.code != 200
- response.msg 包含 "assetDetailValidJson" 或 "必填"

---

#### API-ASSET-008: assetDetailValidJson格式错误
**用例名称**: assetDetailValidJson字段不是有效的JSON字符串

**前置条件**: 已获取有效accessToken

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Authorization: Bearer {valid_access_token}

{
  "assetDetailValidJson": "invalid json string",
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "JSON格式错误"
}
```

**断言规则**:
- response.code != 200

---

#### API-ASSET-009: Content-Type错误
**用例名称**: Content-Type设置为非application/json

**前置条件**: 已获取有效accessToken

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: text/plain
Authorization: Bearer {valid_access_token}

{
  "assetDetailValidJson": "{\"assetName\":\"测试资产\"}",
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 415,
  "data": null,
  "msg": "不支持的媒体类型"
}
```

**断言规则**:
- HTTP状态码 = 415 或 response.code != 200

---

#### API-ASSET-010: SQL注入测试
**用例名称**: 在资产名称字段尝试SQL注入

**前置条件**: 已获取有效accessToken

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Authorization: Bearer {valid_access_token}

{
  "assetDetail": "{\"assetName\":\"测试资产' OR '1'='1\",\"assetType\":\"1\"}",
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "参数包含非法字符"
}
```

**断言规则**:
- response.code != 200
- 系统应拒绝SQL注入攻击

---

#### API-ASSET-011: XSS攻击测试
**用例名称**: 在资产描述字段尝试XSS攻击

**前置条件**: 已获取有效accessToken

**请求信息**:
```http
POST https://whhnhy.com:38868/api/converge-app-api/digital/culture/asset/create
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Authorization: Bearer {valid_access_token}

{
  "assetDetailValidJson": "{\"assetName\":\"测试资产\",\"description\":\"<script>alert('XSS')</script>\"}",
  "assetDetailJson": "{}"
}
```

**预期响应**:
```json
{
  "code": 400,
  "data": null,
  "msg": "参数包含非法字符"
}
```

**断言规则**:
- response.code != 200
- 系统应拒绝XSS攻击或正确转义处理

---

#### API-ASSET-012: 并发请求测试
**用例名称**: 使用同一token并发发起多个资产创建请求

**前置条件**: 已获取有效accessToken

**请求信息**:
- 同时发送10个有效的资产创建请求
- 每个请求使用相同的accessToken

**预期结果**:
- 所有请求正常响应
- 每个请求返回不同的资产ID
- 没有请求返回401错误

**断言规则**:
- 所有HTTP状态码 = 200
- 所有response.code = 200
- 返回的资产ID各不相同

---

## 测试环境配置

### 测试账号
| 字段 | 值 |
|------|-----|
| 测试手机号 | 18671450802 |
| 测试密码 | a123456 |

### 接口地址
| 字段 | 值 |
|------|-----|
| Base URL | https://whhnhy.com:38868 |
| 登录接口 | /converge-app-api/converge/auth/login |
| 资产创建接口 | /api/converge-app-api/digital/culture/asset/create |

### Token管理
- accessToken有效期：约24小时（根据expiresTime计算）
- refreshToken用于刷新accessToken
- 过期时间戳单位：毫秒

---

## 测试数据模板

### 资产登记最小数据
```json
{
  "assetDetailValidJson": "{\"assetName\":\"最小测试资产\",\"assetType\":\"1\",\"assetCategory\":\"01\"}",
  "assetDetailJson": "{}"
}
```

### 资产登记完整数据
```json
{
  "assetDetailValidJson": "{\"assetName\":\"完整测试资产\",\"assetType\":\"1\",\"assetCategory\":\"01\",\"description\":\"这是一条完整的测试资产描述\",\"keywords\":\"测试,资产\",\"status\":\"1\"}",
  "assetDetailJson": "{\"creator\":\"测试创作者\",\"createTime\":\"2026-02-25\",\"updateTime\":\"2026-02-25\",\"resourceUrl\":\"https://example.com/resource\",\"thumbnail\":\"https://example.com/thumb.png\",\"fileSize\":\"1024\",\"fileFormat\":\"jpg\",\"duration\":\"60\"}"
}
```

---

## 附录

### 错误码说明
| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权/Token无效/Token过期 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 415 | 不支持的媒体类型 |
| 500 | 服务器内部错误 |

### 测试注意事项
1. 所有测试需要先获取有效的accessToken
2. Token过期后需要重新登录
3. 并发测试时注意Token有效期
4. 创建的资产应在测试后清理
5. 安全测试需要确认系统已进行参数校验
