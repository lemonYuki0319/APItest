# -*- coding: utf-8 -*-
"""
数据工具类
"""

import os
import yaml
from config.constants import TESTDATA_DIR

class DataUtils:
    @staticmethod
    def get_user_ids():
        """从 yaml 读取用户 id"""
        yaml_path = os.path.join(TESTDATA_DIR, 'user_data.yaml')
        
        try:
            if not os.path.exists(yaml_path):
                print("警告: yaml文件不存在，使用示例数据")
                return ["2026907072607555586"]
            
            with open(yaml_path, 'r', encoding='utf-8') as yaml_file:
                data = yaml.safe_load(yaml_file)
            
            user_ids = data.get("id", [])
            if not user_ids:
                print("警告: yaml文件中没有找到id数据，使用示例数据")
                return ["2026907072607555586"]
            
            return user_ids
        except Exception as e:
            print(f"读取 yaml 文件失败: {e}，使用示例数据")
            return ["2026907072607555586"]
