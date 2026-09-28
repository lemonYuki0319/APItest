# -*- coding: utf-8 -*-
"""
数据工具类
"""

import os
import yaml
from config.constants import TESTDATA_DIR
import pytest



def load_yaml(filename):
    """加载 resources/testdata 下的 yaml 测试数据文件（供各测试模块共享）"""
    path = os.path.join(TESTDATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

MARK_MAP = {
    "slow": pytest.mark.slow,
    "auth": pytest.mark.auth,
    "user": pytest.mark.user,
}
def build_marks(case):
    """把 yaml 中的标签字段转换为 pytest 标记"""
    marks = [MARK_MAP[m] for m in (case.get("marks") or []) if m in MARK_MAP]
    if case.get("skip"):
        marks.append(pytest.mark.skip(reason=case.get("skip_reason", "标记跳过")))
    if case.get("xfail"):
        marks.append(pytest.mark.xfail(reason=case.get("xfail_reason", "标记预期失败")))
    return marks

class DataUtils:
    @staticmethod
    def get_user_ids(limit: int | None = None):
        """
        从 yaml 读取用户 id

        Args:
            limit: 限制返回数量（用于初学者快速运行/调试）。None 表示不限制。
        """
        yaml_path = os.path.join(TESTDATA_DIR, "user_data.yaml")

        try:
            if not os.path.exists(yaml_path):
                print("警告: yaml文件不存在，使用示例数据")
                user_ids = ["2026907072607555586"]
                return user_ids[:limit] if limit else user_ids

            with open(yaml_path, "r", encoding="utf-8") as yaml_file:
                data = yaml.safe_load(yaml_file)

            user_ids = data.get("id", [])
            if not user_ids:
                print("警告: yaml文件中没有找到id数据，使用示例数据")
                user_ids = ["2026907072607555586"]
                return user_ids[:limit] if limit else user_ids

            return user_ids[:limit] if limit else user_ids
        except Exception as e:
            print(f"读取 yaml 文件失败: {e}，使用示例数据")
            user_ids = ["2026907072607555586"]
            return user_ids[:limit] if limit else user_ids
