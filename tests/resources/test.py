"""
测试用户注册接口
"""
import pytest
import requests
import xlrd
import os

# 读取Excel文件中的用户名
def get_usernames():
    """从用户数据（1.xls文件中读取前50个用户名"""
    excel_path = os.path.join(os.path.dirname(__file__), 'testdata', '用户数据 (1).xls')
    wb = xlrd.open_workbook(excel_path)
    ws = wb.sheet_by_index(0)
    
    usernames = []
    # 假设用户名列在第一列，从第二行开始（第一行是表头）
    for row in range(1, min(51, ws.nrows)):  # 读取前50个，xlrd的行索引从0开始
        username = ws.cell_value(row, 0)
        if username:
            usernames.append(username)
    
    return usernames

# 生成测试数据
test_data = []
for username in get_usernames():
    test_data.append({
        "username": username,
        "password": "Xiaoqian@0319",
        "password2": "Xiaoqian@0319",
        "email": "",
        "verification_code": "",
        "wechat_verification_code": "",
        "aff_code": "XniC"
    })

def test_user_register():
    """测试用户注册接口（数据驱动）"""
    url = "https://ai.xingyungept.cn/api/user/register?turnstile="
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    # 遍历测试数据
    for data in test_data:
        response = requests.post(url, json=data, headers=headers)
        
        # 打印响应信息
        print(f"注册用户: {data['username']}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 断言响应状态码
        assert response.status_code == 200, f"注册失败: {response.text}"
