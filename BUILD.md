# Browser History Browser - Build Instructions

## Automated CI/CD

The project includes automated CI/CD using GitHub Actions that builds Windows executables on every push to main branch and pull requests.

### CI/CD Features:
- ✅ Windows-only builds (as requested)
- ✅ PyInstaller directory-based packaging (not onefile)
- ✅ Static files copied separately (not embedded in executable)
- ✅ Automatic ZIP compression
- ✅ Artifact upload for easy download
- ✅ Release asset upload for tagged releases

## Manual Building (Windows)

### Prerequisites:
- Python 3.8+ installed on Windows
- Git (to clone the repository)

### Quick Build:
```bash
# Clone the repository
git clone https://github.com/yanjing19989/Browser-history-browser-py.git
cd Browser-history-browser-py

# Run the build script
build.bat
```

### Manual Build Steps:
```bash
# 1. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r build_requirements.txt

# 2. Build with PyInstaller
pyinstaller bhb.spec --clean --noconfirm

# 3. Copy static files
xcopy static dist\BrowserHistoryBrowser\static\ /E /I /Y

# 4. Create ZIP (optional)
cd dist
powershell "Compress-Archive -Path BrowserHistoryBrowser -DestinationPath BrowserHistoryBrowser-windows.zip"
```

## Build Output

The build process creates:
- `dist/BrowserHistoryBrowser/` - Main application directory
- `dist/BrowserHistoryBrowser/BrowserHistoryBrowser.exe` - Main executable
- `dist/BrowserHistoryBrowser/static/` - Web interface files
- `dist/BrowserHistoryBrowser/VERSION.txt` - Build information

## Running the Built Application

1. Navigate to `dist/BrowserHistoryBrowser/`
2. Run `BrowserHistoryBrowser.exe`
3. The application will start and open a web browser to `http://127.0.0.1:8000`

## Packaging Notes

- **Directory Structure**: Uses PyInstaller's directory mode (not onefile) for better performance and easier debugging
- **Static Files**: HTML/CSS/JS files are copied separately to maintain web server functionality
- **Dependencies**: All Python dependencies are bundled in the executable directory
- **Size**: Typical build size is ~50-80MB uncompressed

## CI/CD Workflow

The GitHub Actions workflow (`/github/workflows/build.yml`):

1. **Triggers**: Runs on push to main, pull requests, and releases
2. **Environment**: Uses `windows-latest` runner
3. **Python**: Uses Python 3.11
4. **Build**: Runs PyInstaller with custom spec file
5. **Package**: Creates ZIP archive with version info
6. **Artifacts**: Uploads build as GitHub Action artifact
7. **Releases**: Automatically attaches ZIP to GitHub releases