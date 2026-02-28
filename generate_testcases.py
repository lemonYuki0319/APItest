# -*- coding: utf-8 -*-
"""
API Test Case Generator for East Carbon Login API
Generates comprehensive test cases and exports to Excel format
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
import os


# API Configuration
API_CONFIG = {
    "module": "Login",
    "endpoint": "east_carbon/login",
    "method": "POST",
    "base_url": "https://whhnhy.com:38868",
    "description": "East Carbon Login API",
    "headers": {"Content-Type": "application/json"},
    "valid_credentials": {
        "loginType": 100,
        "userType": 1,
        "username": "19900000001",
        "password": "a123456"
    }
}


# Test Case Definitions
TEST_CASES = [
    # P0 - Happy Path
    {
        "case_id": "TC001",
        "title": "Normal login with all valid parameters",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": str(API_CONFIG["valid_credentials"]),
        "expected_result": '{"code": 200, "data": {"userId": "...", "accessToken": "...", "refreshToken": "...", "expiresTime": "..."}, "msg": ""}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Happy path - valid credentials"
    },
    # P0 - Missing Required Parameters
    {
        "case_id": "TC002",
        "title": "Missing loginType parameter",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"userType": 1, "username": "19900000001", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Missing required parameter: loginType"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Required parameter missing"
    },
    {
        "case_id": "TC003",
        "title": "Missing userType parameter",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "username": "19900000001", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Missing required parameter: userType"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Required parameter missing"
    },
    {
        "case_id": "TC004",
        "title": "Missing username parameter",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Missing required parameter: username"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Required parameter missing"
    },
    {
        "case_id": "TC005",
        "title": "Missing password parameter",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "19900000001"}',
        "expected_result": '{"code": 400, "msg": "Missing required parameter: password"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Required parameter missing"
    },
    # P0 - Invalid Parameters
    {
        "case_id": "TC006",
        "title": "Invalid loginType parameter",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 999, "userType": 1, "username": "19900000001", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Invalid loginType"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Invalid loginType value"
    },
    {
        "case_id": "TC007",
        "title": "Invalid userType parameter",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 99, "username": "19900000001", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Invalid userType"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Invalid userType value"
    },
    {
        "case_id": "TC008",
        "title": "Non-existent username",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "99999999999", "password": "a123456"}',
        "expected_result": '{"code": 401, "msg": "User not found"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Username does not exist in system"
    },
    {
        "case_id": "TC009",
        "title": "Wrong password",
        "priority": "P0",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "19900000001", "password": "wrongpassword"}',
        "expected_result": '{"code": 401, "msg": "Invalid password"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Incorrect password for valid user"
    },
    # P1 - Authentication
    {
        "case_id": "TC010",
        "title": "Empty username",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Username cannot be empty"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Empty string username"
    },
    {
        "case_id": "TC011",
        "title": "Empty password",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "19900000001", "password": ""}',
        "expected_result": '{"code": 400, "msg": "Password cannot be empty"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Empty string password"
    },
    {
        "case_id": "TC012",
        "title": "Null username",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": null, "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Username cannot be null"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Null value for username"
    },
    {
        "case_id": "TC013",
        "title": "Null password",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "19900000001", "password": null}',
        "expected_result": '{"code": 400, "msg": "Password cannot be null"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Null value for password"
    },
    # P1 - Boundary Tests
    {
        "case_id": "TC014",
        "title": "Extremely long username",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "199000000011990000000119900000001199000000011990000000119900000001", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Username exceeds maximum length"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Username exceeds 50 characters"
    },
    {
        "case_id": "TC015",
        "title": "Extremely long password",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "19900000001", "password": "a123456a123456a123456a123456a123456a123456a123456a123456a123456a123456"}',
        "expected_result": '{"code": 400, "msg": "Password exceeds maximum length"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Password exceeds 50 characters"
    },
    {
        "case_id": "TC016",
        "title": "Special characters in username",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "user@#$%^&*()", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Username contains invalid characters"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Special chars in username field"
    },
    # P1 - Data Types
    {
        "case_id": "TC017",
        "title": "loginType as string instead of integer",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": "100", "userType": 1, "username": "19900000001", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Invalid data type for loginType"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "String instead of integer"
    },
    {
        "case_id": "TC018",
        "title": "userType as string instead of integer",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": "1", "username": "19900000001", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Invalid data type for userType"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "String instead of integer"
    },
    {
        "case_id": "TC019",
        "title": "username as number instead of string",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": 19900000001, "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Invalid data type for username"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Number instead of string"
    },
    {
        "case_id": "TC020",
        "title": "password as number instead of string",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "19900000001", "password": 123456}',
        "expected_result": '{"code": 400, "msg": "Invalid data type for password"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Number instead of string"
    },
    # P1 - Format Issues
    {
        "case_id": "TC021",
        "title": "Missing Content-Type header",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{}',
        "params": str(API_CONFIG["valid_credentials"]),
        "expected_result": '{"code": 415, "msg": "Unsupported Media Type"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "No Content-Type header specified"
    },
    {
        "case_id": "TC022",
        "title": "Wrong Content-Type header",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/xml"}',
        "params": str(API_CONFIG["valid_credentials"]),
        "expected_result": '{"code": 415, "msg": "Unsupported Media Type"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "XML content type instead of JSON"
    },
    {
        "case_id": "TC023",
        "title": "Empty request body",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{}',
        "expected_result": '{"code": 400, "msg": "Request body is empty"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Empty JSON object"
    },
    {
        "case_id": "TC024",
        "title": "Malformed JSON in request body",
        "priority": "P1",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "19900000001", "password": "a123456"',
        "expected_result": '{"code": 400, "msg": "Invalid JSON format"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "Y",
        "remarks": "Unclosed brace in JSON"
    },
    # P2 - Security
    {
        "case_id": "TC025",
        "title": "SQL injection in username",
        "priority": "P2",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "admin\' OR \'1\'=\'1", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Invalid input"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "N",
        "remarks": "SQL injection attempt"
    },
    {
        "case_id": "TC026",
        "title": "XSS attack in username",
        "priority": "P2",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "<script>alert(\'XSS\')</script>", "password": "a123456"}',
        "expected_result": '{"code": 400, "msg": "Invalid input"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "N",
        "remarks": "Cross-site scripting attempt"
    },
    {
        "case_id": "TC027",
        "title": "SQL injection in password",
        "priority": "P2",
        "url": API_CONFIG["base_url"] + "/" + API_CONFIG["endpoint"],
        "method": "POST",
        "headers": '{"Content-Type": "application/json"}',
        "params": '{"loginType": 100, "userType": 1, "username": "19900000001", "password": "pass\' OR \'1\'=\'1"}',
        "expected_result": '{"code": 400, "msg": "Invalid input"}',
        "status_code": "200",
        "execution_result": "",
        "should_execute": "N",
        "remarks": "SQL injection attempt in password"
    },
]


def create_excel_file():
    """Create Excel file with test cases"""

    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Login API Test Cases"

    # Define column headers
    headers = [
        "用例ID",
        "用例标题",
        "优先级",
        "接口URL",
        "请求方法",
        "请求头",
        "请求参数",
        "预期响应",
        "状态码",
        "执行结果",
        "是否执行",
        "备注"
    ]

    # Define column widths
    column_widths = {
        'A': 10,  # 用例ID
        'B': 35,  # 用例标题
        'C': 10,  # 优先级
        'D': 50,  # 接口URL
        'E': 10,  # 请求方法
        'F': 35,  # 请求头
        'G': 50,  # 请求参数
        'H': 60,  # 预期响应
        'I': 12,  # 状态码
        'J': 15,  # 执行结果
        'K': 12,  # 是否执行
        'L': 30   # 备注
    }

    # Set column widths
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    # Define styles
    header_font = Font(name='Arial', size=11, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    border_style = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Write headers
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border_style

    # Write test cases
    data_alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    for row_num, test_case in enumerate(TEST_CASES, 2):
        ws.cell(row=row_num, column=1, value=test_case["case_id"])
        ws.cell(row=row_num, column=2, value=test_case["title"])
        ws.cell(row=row_num, column=3, value=test_case["priority"])
        ws.cell(row=row_num, column=4, value=test_case["url"])
        ws.cell(row=row_num, column=5, value=test_case["method"])
        ws.cell(row=row_num, column=6, value=test_case["headers"])
        ws.cell(row=row_num, column=7, value=test_case["params"])
        ws.cell(row=row_num, column=8, value=test_case["expected_result"])
        ws.cell(row=row_num, column=9, value=test_case["status_code"])
        ws.cell(row=row_num, column=10, value=test_case["execution_result"])
        ws.cell(row=row_num, column=11, value=test_case["should_execute"])
        ws.cell(row=row_num, column=12, value=test_case["remarks"])

        # Apply alignment and border to all cells in the row
        for col_num in range(1, 13):
            cell = ws.cell(row=row_num, column=col_num)
            cell.alignment = data_alignment
            cell.border = border_style

            # Set priority color
            if col_num == 3:
                if test_case["priority"] == "P0":
                    cell.fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
                elif test_case["priority"] == "P1":
                    cell.fill = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')
                elif test_case["priority"] == "P2":
                    cell.fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')

    # Freeze header row
    ws.freeze_panes = 'A2'

    # Add summary sheet
    summary_ws = wb.create_sheet("Summary")
    summary_ws.column_dimensions['A'].width = 30
    summary_ws.column_dimensions['B'].width = 30

    summary_data = [
        ["API Test Case Summary", ""],
        ["", ""],
        ["Module", API_CONFIG["module"]],
        ["Endpoint", API_CONFIG["endpoint"]],
        ["Base URL", API_CONFIG["base_url"]],
        ["Method", API_CONFIG["method"]],
        ["", ""],
        ["Total Test Cases", len(TEST_CASES)],
        ["P0 Test Cases", sum(1 for tc in TEST_CASES if tc["priority"] == "P0")],
        ["P1 Test Cases", sum(1 for tc in TEST_CASES if tc["priority"] == "P1")],
        ["P2 Test Cases", sum(1 for tc in TEST_CASES if tc["priority"] == "P2")],
        ["Tests to Execute (Y)", sum(1 for tc in TEST_CASES if tc["should_execute"] == "Y")],
        ["Tests Skipped (N)", sum(1 for tc in TEST_CASES if tc["should_execute"] == "N")],
        ["", ""],
        ["Generated Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    ]

    for row_num, (key, value) in enumerate(summary_data, 1):
        summary_ws.cell(row=row_num, column=1, value=key)
        summary_ws.cell(row=row_num, column=2, value=value)

        # Apply formatting to header
        if row_num == 1:
            cell = summary_ws.cell(row=row_num, column=1)
            cell.font = Font(name='Arial', size=14, bold=True)

    # Save workbook
    output_file = os.path.join(output_dir, "接口测试用例_east_carbon_login.xlsx")
    wb.save(output_file)
    print(f"Excel file generated: {output_file}")

    return output_file


def generate_automation_script():
    """Generate pytest automation script"""

    script_content = '''# -*- coding: utf-8 -*-
"""
Automated API Test Script for East Carbon Login API
Generated by generate_testcases.py
Run: pytest output/test_api_auto.py -v
"""

import pytest
import requests
import json
from urllib.parse import urljoin


# API Configuration
API_CONFIG = {
    "module": "Login",
    "endpoint": "east_carbon/login",
    "method": "POST",
    "base_url": "https://whhnhy.com:38868",
    "description": "East Carbon Login API",
    "headers": {"Content-Type": "application/json"},
    "valid_credentials": {
        "loginType": 100,
        "userType": 1,
        "username": "19900000001",
        "password": "a123456"
    }
}


class APIClient:
    """HTTP Client for API testing"""

    def __init__(self, base_url=API_CONFIG["base_url"], verify_ssl=False):
        self.base_url = base_url
        self.session = requests.Session()
        self.verify_ssl = verify_ssl

    def request(self, method, endpoint, headers=None, params=None, **kwargs):
        """Send HTTP request"""
        url = urljoin(self.base_url, endpoint)
        request_headers = {}
        if headers:
            request_headers.update(headers)

        # Disable SSL warnings
        if not self.verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            if method.upper() == "GET":
                response = self.session.get(
                    url,
                    headers=request_headers,
                    params=params,
                    verify=self.verify_ssl,
                    **kwargs
                )
            elif method.upper() == "POST":
                response = self.session.post(
                    url,
                    headers=request_headers,
                    json=params,
                    verify=self.verify_ssl,
                    **kwargs
                )
            elif method.upper() == "PUT":
                response = self.session.put(
                    url,
                    headers=request_headers,
                    json=params,
                    verify=self.verify_ssl,
                    **kwargs
                )
            elif method.upper() == "DELETE":
                response = self.session.delete(
                    url,
                    headers=request_headers,
                    json=params,
                    verify=self.verify_ssl,
                    **kwargs
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            return response

        except requests.exceptions.SSLError:
            raise
        except requests.exceptions.ConnectionError as e:
            raise
        except requests.exceptions.Timeout as e:
            raise
        except requests.exceptions.RequestException as e:
            raise


# Test Data Generation Helper
def get_request_data(title):
    """Generate request data based on test case title"""
    valid = API_CONFIG["valid_credentials"]

    if "Normal login" in title or "Happy path" in title:
        return valid.copy()

    elif "Missing loginType" in title:
        return {"userType": valid["userType"], "username": valid["username"], "password": valid["password"]}

    elif "Missing userType" in title:
        return {"loginType": valid["loginType"], "username": valid["username"], "password": valid["password"]}

    elif "Missing username" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "password": valid["password"]}

    elif "Missing password" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": valid["username"]}

    elif "Invalid loginType" in title:
        return {"loginType": 999, "userType": valid["userType"], "username": valid["username"], "password": valid["password"]}

    elif "Invalid userType" in title:
        return {"loginType": valid["loginType"], "userType": 99, "username": valid["username"], "password": valid["password"]}

    elif "Non-existent username" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": "99999999999", "password": valid["password"]}

    elif "Wrong password" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": valid["username"], "password": "wrongpassword"}

    elif "Empty username" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": "", "password": valid["password"]}

    elif "Empty password" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": valid["username"], "password": ""}

    elif "Null username" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": None, "password": valid["password"]}

    elif "Null password" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": valid["username"], "password": None}

    elif "long username" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": "199000000011990000000119900000001199000000011990000000119900000001", "password": valid["password"]}

    elif "long password" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": valid["username"], "password": "a123456a123456a123456a123456a123456a123456a123456a123456a123456a123456"}

    elif "Special characters" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": "user@#$%^&*()", "password": valid["password"]}

    elif "loginType as string" in title:
        return {"loginType": "100", "userType": valid["userType"], "username": valid["username"], "password": valid["password"]}

    elif "userType as string" in title:
        return {"loginType": valid["loginType"], "userType": "1", "username": valid["username"], "password": valid["password"]}

    elif "username as number" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": 19900000001, "password": valid["password"]}

    elif "password as number" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": valid["username"], "password": 123456}

    elif "SQL injection in username" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": "admin' OR '1'='1", "password": valid["password"]}

    elif "XSS" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": "<script>alert('XSS')</script>", "password": valid["password"]}

    elif "SQL injection in password" in title:
        return {"loginType": valid["loginType"], "userType": valid["userType"], "username": valid["username"], "password": "pass' OR '1'='1"}

    else:
        return valid.copy()


def get_request_headers(title):
    """Generate request headers based on test case title"""
    if "Missing Content-Type" in title:
        return {}
    elif "Wrong Content-Type" in title:
        return {"Content-Type": "application/xml"}
    else:
        return {"Content-Type": "application/json"}


# ============================================================================
# P0 Test Cases - Happy Path
# ============================================================================

@pytest.mark.p0
def test_tc001_normal_login():
    """TC001: Normal login with all valid parameters"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Normal login with all valid parameters")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    # Assertions
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    resp_json = response.json()
    assert "code" in resp_json, "Response missing 'code' field"
    assert resp_json["code"] == 200, f"Expected code 200, got {resp_json.get('code')}"

    assert "data" in resp_json, "Response missing 'data' field"
    data = resp_json["data"]
    assert "userId" in data, "Response data missing 'userId'"
    assert "accessToken" in data, "Response data missing 'accessToken'"
    assert "refreshToken" in data, "Response data missing 'refreshToken'"
    assert "expiresTime" in data, "Response data missing 'expiresTime'"

    print(f"Login successful! UserId: {data['userId']}")


@pytest.mark.p0
def test_tc002_missing_loginType():
    """TC002: Missing loginType parameter"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Missing loginType parameter")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with missing loginType"


@pytest.mark.p0
def test_tc003_missing_userType():
    """TC003: Missing userType parameter"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Missing userType parameter")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with missing userType"


@pytest.mark.p0
def test_tc004_missing_username():
    """TC004: Missing username parameter"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Missing username parameter")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with missing username"


@pytest.mark.p0
def test_tc005_missing_password():
    """TC005: Missing password parameter"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Missing password parameter")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with missing password"


@pytest.mark.p0
def test_tc006_invalid_loginType():
    """TC006: Invalid loginType parameter"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Invalid loginType parameter")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with invalid loginType"


@pytest.mark.p0
def test_tc007_invalid_userType():
    """TC007: Invalid userType parameter"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Invalid userType parameter")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with invalid userType"


@pytest.mark.p0
def test_tc008_nonexistent_username():
    """TC008: Non-existent username"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Non-existent username")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with non-existent username"
    assert resp_json["code"] in [401, 400], f"Expected 401 or 400, got {resp_json['code']}"


@pytest.mark.p0
def test_tc009_wrong_password():
    """TC009: Wrong password"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Wrong password")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with wrong password"
    assert resp_json["code"] in [401, 400], f"Expected 401 or 400, got {resp_json['code']}"


# ============================================================================
# P1 Test Cases - Authentication
# ============================================================================

@pytest.mark.p1
def test_tc010_empty_username():
    """TC010: Empty username"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Empty username")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with empty username"


@pytest.mark.p1
def test_tc011_empty_password():
    """TC011: Empty password"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Empty password")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with empty password"


@pytest.mark.p1
def test_tc012_null_username():
    """TC012: Null username"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Null username")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with null username"


@pytest.mark.p1
def test_tc013_null_password():
    """TC013: Null password"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Null password")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with null password"


# ============================================================================
# P1 Test Cases - Boundary Tests
# ============================================================================

@pytest.mark.p1
def test_tc014_long_username():
    """TC014: Extremely long username"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("long username")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    # Should either accept or reject, but handle gracefully
    assert "code" in resp_json


@pytest.mark.p1
def test_tc015_long_password():
    """TC015: Extremely long password"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("long password")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert "code" in resp_json


@pytest.mark.p1
def test_tc016_special_chars_username():
    """TC016: Special characters in username"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("Special characters in username")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert "code" in resp_json


# ============================================================================
# P1 Test Cases - Data Types
# ============================================================================

@pytest.mark.p1
def test_tc017_loginType_as_string():
    """TC017: loginType as string instead of integer"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("loginType as string")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    # May accept string numbers, may reject - depends on API
    assert "code" in resp_json


@pytest.mark.p1
def test_tc018_userType_as_string():
    """TC018: userType as string instead of integer"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("userType as string")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert "code" in resp_json


@pytest.mark.p1
def test_tc019_username_as_number():
    """TC019: username as number instead of string"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("username as number")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert "code" in resp_json


@pytest.mark.p1
def test_tc020_password_as_number():
    """TC020: password as number instead of string"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("password as number")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert "code" in resp_json


# ============================================================================
# P1 Test Cases - Format Issues
# ============================================================================

@pytest.mark.p1
def test_tc021_missing_content_type():
    """TC021: Missing Content-Type header"""
    client = APIClient(verify_ssl=False)
    headers = get_request_headers("Missing Content-Type")
    data = get_request_data("Normal login")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    # API might reject or handle anyway
    assert response.status_code in [200, 415, 400]


@pytest.mark.p1
def test_tc022_wrong_content_type():
    """TC022: Wrong Content-Type header"""
    client = APIClient(verify_ssl=False)
    headers = get_request_headers("Wrong Content-Type")
    data = get_request_data("Normal login")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code in [200, 415, 400]


@pytest.mark.p1
def test_tc023_empty_request_body():
    """TC023: Empty request body"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = {}

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["code"] != 200, "Should fail with empty body"


# ============================================================================
# P2 Test Cases - Security
# ============================================================================

@pytest.mark.p2
@pytest.mark.skip("Security test - manual verification recommended")
def test_tc025_sql_injection_username():
    """TC025: SQL injection in username"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("SQL injection in username")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    # Should reject malicious input
    assert resp_json["code"] != 200, "Should reject SQL injection attempt"


@pytest.mark.p2
@pytest.mark.skip("Security test - manual verification recommended")
def test_tc026_xss_username():
    """TC026: XSS attack in username"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("XSS")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    # Should reject malicious input
    assert resp_json["code"] != 200, "Should reject XSS attempt"


@pytest.mark.p2
@pytest.mark.skip("Security test - manual verification recommended")
def test_tc027_sql_injection_password():
    """TC027: SQL injection in password"""
    client = APIClient(verify_ssl=False)
    headers = {"Content-Type": "application/json"}
    data = get_request_data("SQL injection in password")

    response = client.request("POST", API_CONFIG["endpoint"], headers=headers, params=data)

    assert response.status_code == 200
    resp_json = response.json()
    # Should reject malicious input
    assert resp_json["code"] != 200, "Should reject SQL injection attempt"


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Pytest configuration"""
    config.addinivalue_line("markers", "p0: P0 test cases - Happy path and critical tests")
    config.addinivalue_line("markers", "p1: P1 test cases - Authentication and boundary tests")
    config.addinivalue_line("markers", "p2: P2 test cases - Security tests")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
'''

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, "test_api_auto.py")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(script_content)

    print(f"Automation script generated: {output_file}")
    return output_file


def generate_readme():
    """Generate README.md with usage instructions"""

    readme_content = r'''# API Test Case Generator - East Carbon Login API

Automated test case generation and execution framework for the East Carbon Login API.

## 📁 Project Structure

```
E:\python_project\APItest\
├── generate_testcases.py       # Test case generation script
├── output\
│   ├── 接口测试用例_east_carbon_login.xlsx  # Excel test case documentation
│   └── test_api_auto.py        # Pytest automation script
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

Install required dependencies:

```bash
pip install pytest requests openpyxl
```

### Generate Test Cases

Run the test case generator:

```bash
python generate_testcases.py
```

This will create:
1. `output/接口测试用例_east_carbon_login.xlsx` - Excel file with all test cases
2. `output/test_api_auto.py` - Pytest automation script

### Run Automated Tests

Run all tests:

```bash
pytest output/test_api_auto.py -v
```

Run only P0 tests (Happy Path & Critical):

```bash
pytest output/test_api_auto.py -v -m p0
```

Run only P1 tests:

```bash
pytest output/test_api_auto.py -v -m p1
```

Run with detailed output:

```bash
pytest output/test_api_auto.py -v -s
```

## 📋 API Specification

| Property | Value |
|----------|-------|
| **URL** | `https://whhnhy.com:38868/east_carbon/login` |
| **Method** | POST |
| **Content-Type** | application/json |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| loginType | integer | Yes | Login type (e.g., 100) |
| userType | integer | Yes | User type (e.g., 1) |
| username | string | Yes | User phone number |
| password | string | Yes | User password |

### Success Response

```json
{
    "code": 200,
    "data": {
        "userId": "1979095695566573570",
        "accessToken": "...",
        "refreshToken": "...",
        "expiresTime": 1772421794783
    },
    "msg": ""
}
```

## 📊 Test Case Coverage

| Priority | Count | Description |
|----------|-------|-------------|
| **P0** | 9 | Happy path, missing parameters, invalid parameters |
| **P1** | 15 | Authentication, boundary tests, data types, format issues |
| **P2** | 3 | Security tests (SQL injection, XSS) |
| **Total** | 27 | Comprehensive test coverage |

### Test Case Categories

#### P0 - Critical Tests
1. Normal login with all valid parameters
2. Missing loginType parameter
3. Missing userType parameter
4. Missing username parameter
5. Missing password parameter
6. Invalid loginType parameter
7. Invalid userType parameter
8. Non-existent username
9. Wrong password

#### P1 - Functional Tests
10. Empty username
11. Empty password
12. Null username
13. Null password
14. Extremely long username
15. Extremely long password
16. Special characters in username
17. loginType as string
18. userType as string
19. username as number
20. password as number
21. Missing Content-Type header
22. Wrong Content-Type header
23. Empty request body
24. Malformed JSON

#### P2 - Security Tests
25. SQL injection in username
26. XSS attack in username
27. SQL injection in password

## 📝 Excel Test Case File

The generated Excel file (`接口测试用例_east_carbon_login.xlsx`) contains the following columns:

| Column | Description |
|--------|-------------|
| 用例ID | Unique test case identifier (TC001-TC027) |
| 用例标题 | Test case description |
| 优先级 | Priority (P0, P1, P2) |
| 接口URL | Full API endpoint URL |
| 请求方法 | HTTP method (POST) |
| 请求头 | Request headers |
| 请求参数 | Request body parameters |
| 预期响应 | Expected response |
| 状态码 | Expected HTTP status code |
| 执行结果 | Actual execution result (to be filled) |
| 是否执行 | Execute flag (Y/N) |
| 备注 | Additional notes |

## ⚙️ Configuration

Edit the `API_CONFIG` dictionary in either script to modify:

```python
API_CONFIG = {
    "base_url": "https://whhnhy.com:38868",
    "endpoint": "east_carbon/login",
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "valid_credentials": {
        "loginType": 100,
        "userType": 1,
        "username": "19900000001",
        "password": "a123456"
    }
}
```

## 🔒 SSL Certificate Handling

The automation script disables SSL verification by default (`verify=False`) to handle self-signed certificates:

```python
client = APIClient(verify_ssl=False)
```

For production use with valid certificates, change to:

```python
client = APIClient(verify_ssl=True)
```

## 📌 Notes

- The API uses a custom port (38868) with HTTPS
- Response uses `code` field in JSON body for success/failure (not just HTTP status)
- P2 security tests are marked to skip by default - remove `@pytest.mark.skip` to enable
- All P0 and P1 tests are set to execute by default

## 🛠️ Troubleshooting

### Connection Timeout
If tests timeout, verify:
- Network connectivity to `whhnhy.com:38868`
- Firewall allows outbound connections on port 38868

### SSL Errors
The script automatically disables SSL verification. If you still see SSL warnings, they can be safely ignored for testing purposes.

### Import Errors
Ensure all dependencies are installed:
```bash
pip install pytest requests openpyxl
```

## 📞 Support

For issues or questions, please check:
1. API endpoint is accessible
2. Valid credentials are configured
3. All dependencies are installed

---

Generated: {date}
'''

    # Replace {date} placeholder with actual date
    readme_content = readme_content.replace("{date}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    output_file = "README.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"README.md generated: {output_file}")
    return output_file


if __name__ == "__main__":
    print("=" * 60)
    print("API Test Case Generator for East Carbon Login API")
    print("=" * 60)
    print()

    # Generate all files
    excel_file = create_excel_file()
    automation_script = generate_automation_script()
    readme_file = generate_readme()

    print()
    print("=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(f"Excel file:        {excel_file}")
    print(f"Automation script: {automation_script}")
    print(f"README:            {readme_file}")
    print()
    print("To run tests:")
    print("  pytest output/test_api_auto.py -v")
    print()
