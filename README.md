# Browser History Browser (BHB) - Python版

一个基于Python后端的浏览器历史记录可视化工具，用于分析和浏览您的浏览器历史数据。

## 📋 项目简介

Browser History Browser (BHB) 是一个强大的浏览器历史记录分析工具，具有以下特色：

- 🔍 **智能搜索**: 支持按标题、URL关键词搜索
- 📊 **数据统计**: 提供访问次数、独立站点数等统计信息
- 🎨 **美观界面**: 现代化的Web界面，支持亮色/暗色主题
- 🌐 **多浏览器支持**: 兼容Chrome、Edge、Firefox等主流浏览器
- ⚡ **高性能**: 基于FastAPI的高性能后端API
- 📱 **响应式设计**: 适配桌面和移动设备

## 🚀 快速开始

### 系统要求

- Python 3.8+
- Windows 操作系统 (主要支持)
- 现代浏览器 (Chrome, Firefox, Edge 等)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd BHB_py
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务器**
   
   方式一：使用Python脚本
   ```bash
   python server.py
   ```
   
   方式二：使用批处理文件（Windows）
   ```bash
   start.bat
   ```

4. **访问应用**
   - 前端界面: http://127.0.0.1:8000
   - API文档: http://127.0.0.1:8000/docs

## 📦 预编译版本 (推荐)

我们提供了基于 GitHub Actions 的自动化 CI/CD，可以直接下载预编译的 Windows 可执行文件：

### 下载方式：
1. **GitHub Releases**: 前往 [Releases 页面](../../releases) 下载最新版本
2. **GitHub Actions**: 前往 [Actions 页面](../../actions) 下载最新构建的 artifacts

### 使用预编译版本：
1. 下载 `BrowserHistoryBrowser-windows.zip`
2. 解压到任意目录
3. 运行 `BrowserHistoryBrowser.exe`
4. 应用会自动启动并打开浏览器

### CI/CD 特性：
- ✅ **自动构建**: 每次代码更新自动构建
- ✅ **Windows 专用**: 仅支持 Windows 系统
- ✅ **目录打包**: 使用目录模式，性能更好
- ✅ **静态资源分离**: Web 文件单独存放，便于自定义
- ✅ **版本信息**: 包含构建时间和版本信息

> 💡 **推荐使用预编译版本**，无需安装 Python 环境，开箱即用！

## 🛠️ 手动构建 (开发者)

如需自行构建或进行开发，请参考 [BUILD.md](BUILD.md) 获取详细的构建说明。

### 构建脚本：
- **Windows 批处理**: `build.bat`
- **PowerShell**: `build.ps1 -CreateZip`

## 📁 项目结构

```
BHB_py/
├── .github/                  # GitHub 配置
│   └── workflows/           # CI/CD 工作流
│       └── build.yml        # 自动构建配置
├── backend/                 # Python后端代码
│   ├── __init__.py         # 包初始化文件
│   ├── main.py             # FastAPI应用主文件
│   ├── models.py           # 数据模型定义
│   ├── services.py         # 业务逻辑层
│   └── database.py         # 数据库操作层
├── static/                  # 前端静态文件
│   ├── index.html          # 主页面
│   ├── settings.html       # 设置页面
│   ├── main.js             # 主要JavaScript逻辑
│   ├── settings.js         # 设置页面逻辑
│   ├── theme.js            # 主题切换功能
│   ├── theme-init.js       # 主题初始化
│   ├── style.css           # 样式文件
│   └── favicon.ico         # 网站图标
├── server.py               # 服务器启动脚本
├── start.bat               # Windows启动脚本
├── build.bat               # 构建脚本 (批处理)
├── build.ps1               # 构建脚本 (PowerShell)
├── bhb.spec                # PyInstaller 配置文件
├── requirements.txt        # Python依赖列表
├── build_requirements.txt  # 构建依赖列表
├── package.json           # 项目配置信息
├── create_test_db.py      # 测试数据库创建脚本
├── BUILD.md               # 构建说明文档
└── README.md              # 项目说明文档
```

## 🔧 功能特性

### 核心功能

- **历史记录浏览**: 分页展示浏览器历史记录
- **智能搜索**: 支持标题和URL的关键词搜索
- **时间过滤**: 支持按时间范围筛选（7天、30天、90天、自定义）
- **数据排序**: 支持按访问时间、访问次数、标题排序
- **统计分析**: 显示总访问量、独立站点数等统计信息

### 数据库支持

- **多浏览器**: 支持Chrome、Edge、Firefox历史数据库
- **数据导入**: 支持导入浏览器数据库文件
- **路径管理**: 智能数据库路径管理和验证
- **文件清理**: 自动清理无用的数据库副本

### 用户界面

- **现代设计**: 简洁美观的Material Design风格
- **主题切换**: 支持亮色、暗色和自动主题
- **响应式布局**: 适配不同屏幕尺寸
- **快捷键支持**: Ctrl+K快速搜索

## 🎯 使用指南

### 1. 设置数据源

首次使用需要设置浏览器数据库：

1. 点击右上角设置按钮 ⚙️
2. 选择"浏览器数据库文件"
3. 找到您的浏览器历史数据库文件：
   - **Chrome**: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\History`
   - **Edge**: `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History`
   - **Firefox**: `%APPDATA%\Mozilla\Firefox\Profiles\[profile]\places.sqlite`

### 2. 浏览历史记录

- 使用搜索框查找特定网站或页面
- 使用过滤器按时间范围筛选
- 点击列标题进行排序
- 点击记录查看详细信息

### 3. 数据分析

- 查看页面顶部的统计卡片
- 分析访问频率和时间分布
- 发现最常访问的网站

## 🛠️ 开发信息

### 技术栈

**后端**:
- [FastAPI](https://fastapi.tiangolo.com/) - 现代高性能Web框架
- [Uvicorn](https://www.uvicorn.org/) - ASGI服务器
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 数据验证
- SQLite - 数据库

**前端**:
- 原生 HTML/CSS/JavaScript
- 现代化响应式设计
- 主题切换功能

### API 端点

主要API端点：

- `GET /` - 前端页面
- `POST /api/list_history` - 获取历史记录列表
- `GET /api/stats_overview` - 获取统计概览
- `GET /api/get_config` - 获取配置信息
- `POST /api/set_db_path` - 设置数据库路径
- `POST /api/validate_db_path` - 验证数据库路径

完整API文档请访问: http://127.0.0.1:8000/docs

### 开发模式

启动开发服务器：
```bash
python server.py
```

服务器将在文件更改时自动重载。

## 📝 配置文件

应用配置存储在：
```
%USERPROFILE%\AppData\Local\BHB\config.json
```

配置项包括：
- `db_path`: 数据库文件路径
- `browser_db_path`: 浏览器数据库路径
- `top_sites_count`: 统计常访问网站数量

## 🔒 隐私和安全

- **本地处理**: 所有数据在本地处理，不上传到外部服务器
- **只读访问**: 只读取浏览器历史数据，不进行修改
- **数据副本**: 复制浏览器数据库到应用目录，避免影响浏览器正常使用

## 🐛 故障排除

### 常见问题

1. **无法读取浏览器数据库**
   - 确保浏览器已关闭
   - 检查数据库文件路径是否正确
   - 确保有文件读取权限

2. **启动失败**
   - 检查Python版本 (需要3.8+)
   - 确保所有依赖已安装: `pip install -r requirements.txt`
   - 检查端口8000是否被占用

3. **界面显示异常**
   - 清除浏览器缓存
   - 尝试使用不同浏览器
   - 检查JavaScript控制台错误

### 日志信息

服务器日志会显示在控制台中，包含：
- 启动信息
- API请求日志
- 错误信息

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -am '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**注意**: 本工具仅用于个人浏览历史分析，请遵守相关法律法规和隐私政策。
