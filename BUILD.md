# Browser History Browser - Build Instructions

## Automated CI/CD

The project includes automated CI/CD using GitHub Actions that builds Windows executables on every push to main branch and pull requests.

### CI/CD Features:
- ✅ Windows-only builds (as requested)
- ✅ 双重打包模式: 目录版本 + 单文件版本
- ✅ 静态文件直接打包到可执行文件中
- ✅ 自动ZIP压缩 (目录版本)
- ✅ 构件上传便于下载
- ✅ 发布资源自动上传到GitHub Releases

## Manual Building (Windows)

### Prerequisites:
- Python 3.8+ installed on Windows
- Git (to clone the repository)

### Manual Build Steps:

**目录版本 (推荐)**:
```bash
# 1. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r build_requirements.txt

# 2. Build directory version with PyInstaller
pyinstaller bhb.spec --clean --noconfirm

# 3. Create ZIP (optional)
cd dist
powershell "Compress-Archive -Path BrowserHistoryBrowser -DestinationPath BrowserHistoryBrowser-windows-directory.zip"
```

**单文件版本**:
```bash
# 1. Install dependencies (same as above)
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r build_requirements.txt

# 2. Build onefile version with PyInstaller
pyinstaller bhb-onefile.spec --clean --noconfirm

# Result: dist/BrowserHistoryBrowser.exe
```

## Build Output

### 目录版本 (bhb.spec):
- `dist/BrowserHistoryBrowser/` - 主应用程序目录
- `dist/BrowserHistoryBrowser/BrowserHistoryBrowser.exe` - 主可执行文件
- `dist/BrowserHistoryBrowser/_internal/` - PyInstaller打包的依赖文件
- `dist/BrowserHistoryBrowser/_internal/static/` - Web界面文件 (内置)
- `dist/BrowserHistoryBrowser/VERSION.txt` - 构建信息

### 单文件版本 (bhb-onefile.spec):
- `dist/BrowserHistoryBrowser.exe` - 单一可执行文件 (所有文件打包在内)

## Running the Built Application

### 目录版本:
1. 导航到 `dist/BrowserHistoryBrowser/`
2. 运行 `BrowserHistoryBrowser.exe`
3. 应用程序将启动并自动打开浏览器到 `http://127.0.0.1:8000`

### 单文件版本:
1. 直接运行 `dist/BrowserHistoryBrowser.exe`
2. 应用程序将启动并自动打开浏览器到 `http://127.0.0.1:8000`

### 关键修复:
- ✅ **重载循环修复**: 打包版本自动禁用uvicorn自动重载，避免无限重启
- ✅ **静态文件修复**: 静态文件正确打包到可执行文件内部，确保Web界面正常工作

## Packaging Notes

### 目录版本特点:
- **目录结构**: 使用PyInstaller目录模式，性能更好，便于调试
- **静态文件**: HTML/CSS/JS文件内置在_internal/static/目录中
- **依赖项**: 所有Python依赖打包在_internal目录中
- **大小**: 典型构建大小约60MB (未压缩)

### 单文件版本特点:
- **单一文件**: 所有文件打包到一个可执行文件中
- **便携性**: 无需解压，直接运行
- **启动时间**: 首次启动稍慢 (需要解压临时文件)
- **大小**: 约20MB单个文件

### 技术实现:
- **重载检测**: 使用`sys.frozen`检测打包环境，自动禁用开发模式重载
- **静态资源**: 通过PyInstaller spec文件直接打包静态文件，避免路径问题

## CI/CD Workflow

The GitHub Actions workflow (`.github/workflows/build.yml`):

1. **触发条件**: 推送到main分支、Pull Request、发布版本时运行
2. **环境**: 使用`windows-latest`运行器
3. **Python版本**: Python 3.11
4. **双重构建**: 
   - 目录版本: `pyinstaller bhb.spec`
   - 单文件版本: `pyinstaller bhb-onefile.spec`
5. **构件上传**:
   - `BrowserHistoryBrowser-windows-directory` (目录版本)
   - `BrowserHistoryBrowser-windows-onefile` (单文件版本)
6. **版本信息**: 自动生成VERSION.txt包含构建时间和Git提交信息
7. **发布资源**: 自动附加到GitHub Releases:
   - `BrowserHistoryBrowser-windows-directory.zip`
   - `BrowserHistoryBrowser.exe`