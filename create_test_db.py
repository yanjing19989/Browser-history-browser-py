#!/usr/bin/env python3
"""
创建测试数据库和示例数据
"""

import sqlite3
import time
from pathlib import Path

def create_test_database():
    """创建测试数据库和示例数据"""
    
    # 创建应用数据目录
    app_data_dir = Path.home() / "AppData" / "Local" / "BHB"
    app_data_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = app_data_dir / "history.db"
    
    print(f"创建测试数据库: {db_path}")
    
    # 连接数据库（如果不存在会自动创建）
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS navigation_history (
            url TEXT PRIMARY KEY,
            title TEXT,
            last_visited_time INTEGER,
            num_visits INTEGER DEFAULT 0,
            locale TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_last_visited_time ON navigation_history(last_visited_time)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_num_visits ON navigation_history(num_visits)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON navigation_history(title)")
    
    # 插入示例数据
    current_time = int(time.time())
    
    sample_data = [
        ("https://www.google.com", "Google", current_time - 3600, 50, "zh-CN"),
        ("https://www.github.com", "GitHub", current_time - 7200, 25, "en-US"),
        ("https://www.stackoverflow.com", "Stack Overflow", current_time - 10800, 30, "en-US"),
        ("https://www.baidu.com", "百度一下，你就知道", current_time - 1800, 40, "zh-CN"),
        ("https://www.zhihu.com", "知乎 - 有问题，就会有答案", current_time - 900, 20, "zh-CN"),
        ("https://docs.python.org", "Python Documentation", current_time - 14400, 15, "en-US"),
        ("https://fastapi.tiangolo.com", "FastAPI", current_time - 21600, 10, "en-US"),
        ("https://www.bilibili.com", "哔哩哔哩 (゜-゜)つロ 干杯~", current_time - 5400, 35, "zh-CN"),
        ("https://www.youtube.com", "YouTube", current_time - 12600, 18, "en-US"),
        ("https://www.npmjs.com", "npm", current_time - 18000, 8, "en-US"),
    ]
    
    cursor.executemany(
        "INSERT OR REPLACE INTO navigation_history (url, title, last_visited_time, num_visits, locale) VALUES (?, ?, ?, ?, ?)",
        sample_data
    )
    
    conn.commit()
    conn.close()
    
    print("✅ 测试数据库创建成功！")
    print(f"📍 位置: {db_path}")
    print(f"📊 插入了 {len(sample_data)} 条示例记录")

if __name__ == "__main__":
    create_test_database()
