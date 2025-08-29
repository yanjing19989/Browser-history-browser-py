@echo off
echo ================================
echo Browser History Browser - Build Script
echo ================================

echo.
echo [1/5] Installing dependencies...
python -m pip install --upgrade pip
if errorlevel 1 goto error
pip install -r requirements.txt
if errorlevel 1 goto error
pip install -r build_requirements.txt
if errorlevel 1 goto error

echo.
echo [2/5] Cleaning previous build...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo [3/5] Building with PyInstaller...
pyinstaller bhb.spec --clean --noconfirm
if errorlevel 1 goto error

echo.
echo [4/5] Copying static files...
if not exist "dist\BrowserHistoryBrowser\static" mkdir "dist\BrowserHistoryBrowser\static"
xcopy "static\*" "dist\BrowserHistoryBrowser\static\" /E /Y
if errorlevel 1 goto error

echo.
echo [5/5] Creating version info...
echo Browser History Browser > "dist\BrowserHistoryBrowser\VERSION.txt"
echo Build Date: %date% %time% >> "dist\BrowserHistoryBrowser\VERSION.txt"
echo Build Machine: %COMPUTERNAME% >> "dist\BrowserHistoryBrowser\VERSION.txt"

echo.
echo ================================
echo Build completed successfully!
echo ================================
echo.
echo Output directory: dist\BrowserHistoryBrowser\
echo To create ZIP: cd dist && powershell "Compress-Archive -Path BrowserHistoryBrowser -DestinationPath BrowserHistoryBrowser-windows.zip"
echo.
pause
goto end

:error
echo.
echo ================================
echo Build failed!
echo ================================
pause
exit /b 1

:end