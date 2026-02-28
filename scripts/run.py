# -*- coding: utf-8 -*-
"""
测试执行入口脚本
"""

import os
import sys
import argparse
import subprocess
from config.constants import PROJECT_ROOT

def run_tests(test_path=None, report_format="allure"):
    """运行测试"""
    # 切换到项目根目录
    os.chdir(PROJECT_ROOT)
    
    # 构建 pytest 命令
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "--tb=short"
    ]
    
    # 添加测试路径
    if test_path:
        pytest_cmd.append(test_path)
    else:
        pytest_cmd.append("tests/")
    
    # 添加报告生成选项
    if report_format == "allure":
        pytest_cmd.extend([
            "--alluredir", "reports/allure-results"
        ])
    
    # 执行测试
    print(f"执行命令: {' '.join(pytest_cmd)}")
    result = subprocess.run(pytest_cmd)
    return result.returncode

def generate_report():
    """生成 Allure 报告"""
    try:
        # 检查 allure 命令是否可用
        subprocess.run(["allure", "--version"], capture_output=True, check=True)
        
        # 生成报告
        report_cmd = [
            "allure", "generate",
            "reports/allure-results",
            "-o", "reports/allure-report",
            "--clean"
        ]
        print(f"生成报告: {' '.join(report_cmd)}")
        subprocess.run(report_cmd)
        
        # 打开报告
        open_cmd = ["allure", "open", "reports/allure-report"]
        subprocess.Popen(open_cmd)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Allure 命令不可用，请安装 allure-commandline")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="运行 API 测试")
    parser.add_argument("--path", help="测试文件或目录路径")
    parser.add_argument("--report", choices=["allure", "html"], default="allure",
                      help="报告格式")
    parser.add_argument("--generate-report", action="store_true",
                      help="生成并打开报告")
    
    args = parser.parse_args()
    
    # 运行测试
    exit_code = run_tests(args.path, args.report)
    
    # 生成报告
    if args.generate_report:
        generate_report()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
