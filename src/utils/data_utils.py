# -*- coding: utf-8 -*-
"""
数据工具类
"""

import os
import openpyxl
from config.constants import TESTDATA_DIR

class DataUtils:
    @staticmethod
    def get_user_ids():
        """从 Excel 读取用户 ID"""
        xls_file = os.path.join(TESTDATA_DIR, '用户数据.xls')
        
        # 如果文件不存在，返回示例数据
        if not os.path.exists(xls_file):
            print(f"警告: Excel文件不存在，使用示例数据")
            return ["2026907072607555586"]
        
        # 尝试使用 openpyxl 读取 xlsx 文件
        try:
            workbook = openpyxl.load_workbook(xls_file)
            sheet = workbook.active
            
            # 查找 ID 列
            id_col = None
            for col_idx, cell in enumerate(sheet[1], 1):
                if cell.value and 'id' in str(cell.value).lower():
                    id_col = col_idx
                    break
            
            if id_col is None:
                id_col = 1  # 默认第一列
            
            # 读取用户 ID（跳过表头）
            user_ids = []
            for row_idx in range(2, sheet.max_row + 1):
                cell_value = sheet.cell(row_idx, id_col).value
                if cell_value:
                    user_ids.append(str(cell_value).strip())
            
            return [uid for uid in user_ids if uid]
        except Exception as e:
            print(f"读取 Excel 文件失败: {e}，使用示例数据")
            return ["2026907072607555586"]
