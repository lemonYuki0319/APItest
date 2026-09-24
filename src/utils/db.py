# -*- coding: utf-8 -*-
"""
达梦数据库（DM）工具类

连接配置见 config/config.yaml 的 database 节。
便捷方法 exists_by_id / get_by_id / delete_by_id 默认操作文化资产表
（即配置中的 culture_asset_table），如需操作其他表可传 table 参数覆盖。

基础用法（调试时直接用）：
    from src.utils.db import DBHelper
    db = DBHelper()
    db.connect()                  # 建立连接
    row = db.get_by_id(asset_id)  # 查询文化资产表
    db.delete_by_id(asset_id)    # 删除文化资产表记录
    db.commit()                   # 提交事务（删除/更新后需提交才生效）
    db.close()                    # 关闭连接
"""

import dmPython
from config.config import get_database_config
from src.utils.logger import logger


class DBHelper:
    """达梦数据库工具类"""

    def __init__(self):
        cfg = get_database_config()
        self.host = cfg.get("host", "127.0.0.1")
        self.port = int(cfg.get("port", 5236))
        self.user = cfg.get("user", "")
        self.password = cfg.get("password", "")
        self.schema = cfg.get("schema", "")
        # 默认操作的文化资产表（便捷方法使用，可传 table 参数覆盖）
        self.culture_asset_table = cfg.get("culture_asset_table", "DIGITAL_CULTURE_ASSET")
        self._conn = None

    # ---------------- 连接管理 ----------------

    def connect(self):
        """建立连接（重复调用返回同一连接）"""
        if self._conn is None:
            self._conn = dmPython.connect(
                user=self.user,
                password=self.password,
                server=self.host,
                port=self.port,
            )
            logger.info(f"[DB] 已连接 {self.user}@{self.host}:{self.port}")
        return self._conn

    def close(self):
        """关闭连接"""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    # ---------------- 事务控制 ----------------

    def commit(self):
        """提交事务（执行 delete/update 后需调用才生效）"""
        if self._conn is not None:
            self._conn.commit()

    def rollback(self):
        """回滚事务"""
        if self._conn is not None:
            self._conn.rollback()

    # ---------------- 通用查询 / 执行 ----------------

    def query_one(self, sql, params=None):
        """查询单条记录，返回 dict 或 None

        Args:
            sql: SQL 语句，参数用 ? 占位符
            params: 参数列表/元组，按顺序对应 ?
        """
        cur = self.connect().cursor()
        try:
            cur.execute(sql, params)
            cols = [d[0] for d in cur.description] if cur.description else []
            row = cur.fetchone()
            if row is None:
                return None
            return dict(zip(cols, row)) if cols else dict(row)
        finally:
            cur.close()

    def execute(self, sql, params=None):
        """执行 insert/update/delete，返回受影响行数

        Args:
            sql: SQL 语句，参数用 ? 占位符
            params: 参数列表/元组，按顺序对应 ?
        """
        cur = self.connect().cursor()
        try:
            cur.execute(sql, params)
            return cur.rowcount if cur.rowcount is not None else 0
        finally:
            cur.close()

    # ---------------- 文化资产表便捷方法 ----------------
    # 默认操作 self.culture_asset_table，如需其他表传 table 参数覆盖
    # 注意：达梦带参数预编译时双引号标识符会报错，故表名/列名不加引号
    #       （达梦默认按大写匹配，配置中的表名/字段名需为大写）

    def exists_by_id(self, id_value, table=None, id_field="ID"):
        """判断记录是否存在，默认查文化资产表"""
        table = table or self.culture_asset_table
        sql = f'SELECT COUNT(*) AS CNT FROM {self.schema}.{table} WHERE {id_field} = ?'
        result = self.query_one(sql, [id_value])
        return (result or {}).get("CNT", 0) > 0

    def get_by_id(self, id_value, table=None, id_field="ID"):
        """按 ID 查询单条记录，默认查文化资产表"""
        table = table or self.culture_asset_table
        sql = f'SELECT * FROM {self.schema}.{table} WHERE {id_field} = ?'
        return self.query_one(sql, [id_value])

    def delete_by_id(self, id_value, table=None, id_field="ID"):
        """按 ID 删除记录，返回受影响行数，默认删文化资产表"""
        table = table or self.culture_asset_table
        sql = f'DELETE FROM {self.schema}.{table} WHERE {id_field} = ?'
        return self.execute(sql, [id_value])
