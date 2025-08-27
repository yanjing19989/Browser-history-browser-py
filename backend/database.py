import sqlite3
import json
from typing import Optional
from pathlib import Path

class Database:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # 尝试从配置文件读取db_path
            config_path = Path.home() / "AppData" / "Local" / "BHB" / "config.json"
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        db_path = config.get("db_path")
                except Exception:
                    pass
            
            # 如果配置文件中没有db_path，使用默认路径
            if db_path is None:
                app_data_dir = Path.home() / "AppData" / "Local" / "BHB"
                app_data_dir.mkdir(parents=True, exist_ok=True)
                db_path = str(app_data_dir / "history.db")
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS navigation_history (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    last_visited_time INTEGER,
                    num_visits INTEGER DEFAULT 0,
                    locale TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 创建索引以提高查询性能
            conn.execute("CREATE INDEX IF NOT EXISTS idx_last_visited_time ON navigation_history(last_visited_time)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_num_visits ON navigation_history(num_visits)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON navigation_history(title)")
            
            conn.commit()
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()):
        """执行查询并返回结果"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row  # 返回字典格式的行
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_write(self, query: str, params: tuple = ()):
        """执行写操作"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount

# 全局数据库实例
db = Database()
