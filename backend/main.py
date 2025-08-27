from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
import json
import shutil
import os
import subprocess
import sys
from tkinter import filedialog
import tkinter as tk
from .models import HistoryFilters, HistoryResponse, StatsOverview, ConfigModel
from .services import HistoryService
from .database import db

app = FastAPI(title="Browser History Browser API", version="1.0.0")

# 允许跨域请求（用于开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务（前端文件）
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# 配置文件路径
CONFIG_PATH = Path.home() / "AppData" / "Local" / "BHB" / "config.json"

def load_config() -> dict:
    """加载配置文件"""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"theme": "auto"}

def save_config(config: dict):
    """保存配置文件"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

@app.get("/")
async def root():
    """根路径，重定向到前端页面"""
    return RedirectResponse(url="/static/index.html")

@app.post("/api/list_history", response_model=HistoryResponse)
async def list_history(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    filters: HistoryFilters = HistoryFilters()
):
    """获取历史记录列表"""
    try:
        result = HistoryService.list_history(page, pageSize, filters)
        return HistoryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")

@app.get("/api/stats_overview", response_model=StatsOverview)
async def stats_overview(timeRange: str = Query("7d")):
    """获取统计概览"""
    try:
        return HistoryService.get_stats_overview(timeRange)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")

@app.get("/api/get_config")
async def get_config():
    """获取配置信息"""
    try:
        config = load_config()
        return {"db_path": db.db_path, **config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取配置失败: {str(e)}")

@app.post("/api/set_db_path")
async def set_db_path(config: ConfigModel):
    """设置数据库路径"""
    try:
        if config.db_path:
            # 重新初始化数据库连接
            db.__init__(config.db_path)
        
        # 保存配置
        current_config = load_config()
        if config.db_path:
            current_config["db_path"] = config.db_path
        save_config(current_config)
        
        return {"success": True, "message": "数据库路径设置成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"设置数据库路径失败: {str(e)}")

@app.post("/api/validate_db_path")
async def validate_db_path(path: dict):
    """验证数据库路径"""
    try:
        db_path = path.get("path")
        if not db_path:
            return {"valid": False, "message": "路径不能为空"}
        
        if not os.path.exists(db_path):
            return {"valid": False, "message": "文件不存在"}
        
        # 尝试连接数据库验证
        import sqlite3
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='navigation_history'")
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {"valid": True, "message": "数据库验证成功"}
            else:
                return {"valid": False, "message": "不是有效的浏览器历史数据库"}
        except sqlite3.Error:
            return {"valid": False, "message": "无法打开数据库文件"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"验证数据库路径失败: {str(e)}")

@app.post("/api/copy_browser_db_to_app")
async def copy_browser_db_to_app(source: dict):
    """复制浏览器数据库到应用目录"""
    try:
        source_path = source.get("sourcePath")
        if not source_path or not os.path.exists(source_path):
            raise HTTPException(status_code=400, detail="源文件不存在")
        
        # 目标路径
        app_data_dir = Path.home() / "AppData" / "Local" / "BHB"
        app_data_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成唯一的文件名
        import time
        timestamp = int(time.time())
        target_path = app_data_dir / f"browser_history_{timestamp}.db"
        
        # 复制文件
        shutil.copy2(source_path, target_path)

        current_config = load_config()
        if source_path:
            current_config["browser_db_path"] = source_path
        save_config(current_config)
        
        return {"success": True, "path": str(target_path), "message": "数据库复制成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"复制数据库失败: {str(e)}")

@app.post("/api/set_browser_db_path")
async def set_browser_db_path(path_data: dict):
    """设置浏览器数据库为当前数据源"""
    try:
        db_path = path_data.get("path")
        if not db_path:
            raise HTTPException(status_code=400, detail="路径不能为空")
        
        # 重新初始化数据库连接
        db.__init__(db_path)
        
        # 保存配置
        config = load_config()
        config["db_path"] = db_path
        save_config(config)
        
        return {"success": True, "message": "数据库设置成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"设置数据库失败: {str(e)}")

@app.get("/api/open_db_directory")
async def open_db_directory():
    """打开数据库目录（在本地桌面环境中打开文件管理器）"""
    app_data_dir = Path.home() / "AppData" / "Local" / "BHB"
    try:
        app_data_dir.mkdir(parents=True, exist_ok=True)
        
        # 在Windows中打开文件管理器
        if sys.platform == "win32":
            subprocess.run(["explorer", str(app_data_dir)], check=False)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", str(app_data_dir)], check=False)
        else:  # Linux
            subprocess.run(["xdg-open", str(app_data_dir)], check=False)
        
        return {"success": True, "path": str(app_data_dir), "message": "数据库目录已打开"}
    except Exception:
        return {"success": False, "path": str(app_data_dir), "message": f"打开目录失败，路径: {str(app_data_dir)}"}

@app.get("/api/browse_db_file")
async def browse_db_file():
    """打开文件选择对话框选择数据库文件"""
    try:
        # 创建隐藏的根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        root.attributes('-topmost', True)  # 保持在最前面
        
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            title="选择浏览器历史数据库文件",
            filetypes=[
                ("SQLite数据库", "*.db"),
                ("所有文件", "*.*")
            ],
            initialdir=str(Path.home())
        )
        
        # 销毁根窗口
        root.destroy()
        
        if file_path:
            return {"success": True, "path": file_path, "message": "文件选择成功"}
        else:
            return {"success": False, "path": "", "message": "用户取消选择"}
            
    except Exception as e:
        return {"success": False, "path": "", "message": f"文件选择失败: {str(e)}"}

@app.get("/api/browse_browser_db_file")
async def browse_browser_db_file():
    """打开文件选择对话框选择浏览器数据库文件"""
    try:
        # 创建隐藏的根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        root.attributes('-topmost', True)  # 保持在最前面
        
        # 常见浏览器数据库位置作为初始目录
        browser_paths = [
            Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default",
            Path.home() / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default",
            Path.home() / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles"
        ]
        
        initial_dir = str(Path.home())
        for path in browser_paths:
            if path.exists():
                initial_dir = str(path)
                break
        
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            title="选择浏览器历史数据库文件",
            filetypes=[
                ("Chrome/Edge历史", "WebAssistDatabase"),
                ("Firefox历史", "places.sqlite"),
                ("SQLite数据库", "*.db"),
                ("所有文件", "*.*")
            ],
            initialdir=initial_dir
        )
        
        # 销毁根窗口
        root.destroy()
        
        if file_path:
            return {"success": True, "path": file_path, "message": "浏览器数据库文件选择成功"}
        else:
            return {"success": False, "path": "", "message": "用户取消选择"}
            
    except Exception as e:
        return {"success": False, "path": "", "message": f"文件选择失败: {str(e)}"}

@app.post("/api/cleanup_old_dbs")
async def cleanup_old_dbs():
    """清理与当前使用数据库不相关的所有数据库文件"""
    try:
        app_data_dir = Path.home() / "AppData" / "Local" / "BHB"
        if not app_data_dir.exists():
            return {"success": True, "message": "没有需要清理的文件"}
        
        # 获取当前正在使用的数据库文件路径
        current_db_path = Path(db.db_path)
        current_db_name = current_db_path.name
        
        cleaned_files = []
        total_size = 0
        
        for file_path in app_data_dir.glob("*.db*"):
            # 跳过当前正在使用的数据库文件
            if file_path.resolve() == current_db_path.resolve():
                continue
            
            # 跳过与当前数据库相关的 WAL 和 SHM 文件
            if (file_path.name.startswith(current_db_name.replace('.db', '')) and 
                (file_path.name.endswith('.db-wal') or file_path.name.endswith('.db-shm'))):
                continue
            
            try:
                file_size = file_path.stat().st_size
                file_path.unlink()
                cleaned_files.append(file_path.name)
                total_size += file_size
            except Exception as e:
                # 如果删除失败，记录但不中断流程
                print(f"无法删除文件 {file_path.name}: {str(e)}")
        
        # 格式化文件大小
        if total_size > 1024 * 1024:  # MB
            size_str = f"{total_size / (1024 * 1024):.1f} MB"
        elif total_size > 1024:  # KB
            size_str = f"{total_size / 1024:.1f} KB"
        else:  # Bytes
            size_str = f"{total_size} 字节"
        
        message = f"清理了 {len(cleaned_files)} 个文件，释放了 {size_str} 空间"
        if len(cleaned_files) == 0:
            message = "没有需要清理的文件"
        
        return {
            "success": True, 
            "cleaned_files": cleaned_files,
            "message": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清理文件失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
