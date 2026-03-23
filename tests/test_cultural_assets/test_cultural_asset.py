# -*- coding: utf-8 -*-
"""
文化资产测试用例

使用 Allure 报告封装展示测试步骤和附件
"""

import pytest
import json
import allure
from src.utils.allure_helper import AllureHelper, step, attach_request, attach_response


@allure.feature("登录模块")
@allure.story("APP端登录")
class TestLogin:
    """登录相关测试用例"""
    
    @allure.title("正确的手机号和密码登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证使用正确的手机号和密码可以成功登录")
    def test_login_success(self, login_actions):
        """测试1: 正确的手机号和密码登录"""
        with allure.step("步骤1: 执行APP端登录"):
            response = login_actions.login_APP("18671450802", "a123456")
            attach_response(response, "登录响应")
        
        with allure.step("步骤2: 验证响应结果"):
            assert response.get("code") == 200, f"登录失败: {response.get('msg')}"
            assert response.get("data", {}).get("accessToken") is not None, "Token 不应为空"
            AllureHelper.attach_text("登录成功，Token已获取", "验证结果")

    @allure.title("缺少mobile参数")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_mobile(self, login_actions):
        """测试2: 缺少mobile参数"""
        with allure.step("执行登录（不填手机号）"):
            response = login_actions.login_APP("", "a123456")
            attach_response(response, "响应结果")
        
        with allure.step("验证登录失败"):
            assert response.get("code") != 200, "缺少mobile参数应该失败"

    @allure.title("缺少password参数")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_password(self, login_actions):
        """测试3: 缺少password参数"""
        with allure.step("执行登录（不填密码）"):
            response = login_actions.login_APP("18671450802", "")
            attach_response(response, "响应结果")
        
        with allure.step("验证登录失败"):
            assert response.get("code") != 200, "缺少password参数应该失败"

    @allure.title("密码错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self, login_actions):
        """测试4: 密码错误"""
        with allure.step("执行登录（错误密码）"):
            response = login_actions.login_APP("18671450802", "wrongpass")
            attach_response(response, "响应结果")
        
        with allure.step("验证登录失败"):
            assert response.get("code") != 200, "密码错误应该失败"

    @allure.title("不存在的手机号")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_unregistered_mobile(self, login_actions):
        """测试5: 不存在的手机号"""
        with allure.step("执行登录（未注册手机号）"):
            response = login_actions.login_APP("13800138000", "a123456")
            attach_response(response, "响应结果")
        
        with allure.step("验证登录失败"):
            assert response.get("code") != 200, "不存在的手机号应该失败"


@allure.feature("文化资产模块")
@allure.story("资产登记")
class TestAssetCreate:
    """资产创建相关测试用例"""
    
    @allure.title("成功创建资产 - 数字商标")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证可以成功登记数字商标类文化资产")
    def test_create_asset_success(self, cultural_asset_actions, login_actions):
        """测试6: 成功创建资产 - 数字商标"""
        
        with allure.step("步骤1: 用户登录"):
            login_response = login_actions.login_APP("18671450802", "a123456")
            attach_response(login_response, "登录响应")
            assert login_response.get("code") == 200, "登录失败"
            cultural_asset_actions.api.token = login_actions.api.token
        
        with allure.step("步骤2: 准备资产数据"):
            asset_data = {
                "isRegistered": 1,
                "cultureAssetName": "数字商标",
                "cultureAssetType": "2997845276013893005",
                "registerSubjectType": "1",
                "ownershipType": "1",
                "coOwnerSaveReqList": [
                    {
                        "coOwnerName": "",
                        "coOwnerPhone": ""
                    }
                ],
                "assetDesc": "测试",
                "assetImgUrl": [
                    {
                        "name": "05数字出版许可证（非必传，仅供参考）.png",
                        "url": "https://www.whhnhy.com:29000/szxc/942fbdf590c51fc498d11074733e9fa5552b0f9012dfa7e81efd2084b0717d6f.png"
                    }
                ],
                "ownershipFileUrl": [
                    {
                        "name": "04商标注册证（非必传，仅供参考）.png",
                        "url": "https://www.whhnhy.com:29000/szxc/942fbdf590c51fc498d11074733e9fa5552b0f9012dfa7e81efd2084b0717d6f.png"
                    }
                ],
                "assetDetailValidJson": json.dumps({
                    "trademarkName": "测试商标",
                    "trademarkCategory": "35类",
                    "registrationNumber": "12345678",
                    "registrationDate": "2024-01-01",
                    "validityPeriod": "2034-01-01",
                    "trademarkOwner": "测试公司"
                }, ensure_ascii=False),
                "assetDetailJson": json.dumps([
                    {"label": "商标名称", "name": "trademarkName", "type": "text", "value": "测试商标"},
                    {"label": "商标类别", "name": "trademarkCategory", "type": "text", "value": "35类"},
                    {"label": "注册号", "name": "registrationNumber", "type": "text", "value": "12345678"}
                ], ensure_ascii=False)
            }
            AllureHelper.attach_text(json.dumps(asset_data, ensure_ascii=False, indent=2), "资产数据")
        
        with allure.step("步骤3: 创建资产"):
            response, asset_id = cultural_asset_actions.create_asset(asset_data)
            attach_response(response, "创建响应")
            AllureHelper.attach_text(f"资产ID: {asset_id}", "创建结果")
        
        with allure.step("步骤4: 验证结果"):
            assert response.get("code") == 200, f"创建资产失败: {response.get('msg')}"
            assert asset_id, "创建资产成功时 asset_id 不应为空"

    @allure.title("缺少必填字段")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_asset_missing_required_field(self, cultural_asset_actions, login_actions):
        """测试7: 缺少必填字段"""
        
        with allure.step("步骤1: 用户登录"):
            login_response = login_actions.login_APP("18671450802", "a123456")
            assert login_response.get("code") == 200, "登录失败"
            cultural_asset_actions.api.token = login_actions.api.token
        
        with allure.step("步骤2: 准备不完整数据"):
            asset_data = {"assetDetailJson": "{}"}
            AllureHelper.attach_text(json.dumps(asset_data, ensure_ascii=False, indent=2), "不完整数据")
        
        with allure.step("步骤3: 尝试创建资产"):
            response, asset_id = cultural_asset_actions.create_asset(asset_data)
            attach_response(response, "响应结果")
        
        with allure.step("步骤4: 验证失败"):
            assert response.get("code") != 200, "缺少必填字段应该失败"
            assert not asset_id, "创建失败时 asset_id 应为空"


@allure.feature("文化资产模块")
@allure.story("资产查询")
class TestAssetQuery:
    """资产查询相关测试用例"""
    
    @allure.title("查询资产列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_query_asset(self, cultural_asset_actions, login_actions):
        """测试8: 查询资产"""
        
        with allure.step("步骤1: 用户登录"):
            login_response = login_actions.login_APP("18671450802", "a123456")
            assert login_response.get("code") == 200, "登录失败"
            cultural_asset_actions.api.token = login_actions.api.token
        
        with allure.step("步骤2: 查询资产列表"):
            response = cultural_asset_actions.query_asset()
            attach_response(response, "查询响应")
        
        with allure.step("步骤3: 验证结果"):
            assert response.get("code") == 200, f"查询资产失败: {response.get('msg')}"
            data = response.get("data", {})
            AllureHelper.attach_text(f"共查询到 {len(data.get('list', []))} 条记录", "查询统计")
