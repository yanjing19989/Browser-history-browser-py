# Browser History Browser - PowerShell Build Script
param(
    [switch]$CreateZip = $false,
    [switch]$Clean = $false
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Browser History Browser - Build Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Error handling
$ErrorActionPreference = "Stop"

try {
    if ($Clean) {
        Write-Host "`n[CLEAN] Removing previous build artifacts..." -ForegroundColor Yellow
        if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
        if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
        if (Test-Path "*.zip") { Remove-Item -Force "*.zip" }
        Write-Host "✅ Cleanup completed" -ForegroundColor Green
    }

    Write-Host "`n[1/5] Installing dependencies..." -ForegroundColor Blue
    & python -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw "Failed to upgrade pip" }
    
    & pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "Failed to install runtime dependencies" }
    
    & pip install -r build_requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "Failed to install build dependencies" }
    Write-Host "✅ Dependencies installed" -ForegroundColor Green

    Write-Host "`n[2/5] Running PyInstaller..." -ForegroundColor Blue
    & pyinstaller bhb.spec --clean --noconfirm
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }
    Write-Host "✅ PyInstaller build completed" -ForegroundColor Green

    Write-Host "`n[3/5] Copying static files..." -ForegroundColor Blue
    $staticDest = "dist\BrowserHistoryBrowser\static"
    if (-not (Test-Path $staticDest)) {
        New-Item -ItemType Directory -Path $staticDest -Force | Out-Null
    }
    Copy-Item -Path "static\*" -Destination $staticDest -Recurse -Force
    Write-Host "✅ Static files copied" -ForegroundColor Green

    Write-Host "`n[4/5] Creating version info..." -ForegroundColor Blue
    $versionFile = "dist\BrowserHistoryBrowser\VERSION.txt"
    $buildInfo = @"
Browser History Browser
Build Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Build Machine: $env:COMPUTERNAME
PowerShell Version: $($PSVersionTable.PSVersion)
OS: $((Get-CimInstance Win32_OperatingSystem).Caption)
"@
    $buildInfo | Out-File -FilePath $versionFile -Encoding UTF8
    Write-Host "✅ Version info created" -ForegroundColor Green

    if ($CreateZip) {
        Write-Host "`n[5/5] Creating ZIP archive..." -ForegroundColor Blue
        $zipPath = "BrowserHistoryBrowser-windows.zip"
        if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
        Compress-Archive -Path "dist\BrowserHistoryBrowser" -DestinationPath $zipPath
        Write-Host "✅ ZIP archive created: $zipPath" -ForegroundColor Green
    } else {
        Write-Host "`n[5/5] Skipping ZIP creation (use -CreateZip to enable)" -ForegroundColor Yellow
    }

    Write-Host "`n================================" -ForegroundColor Green
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host "`nOutput directory: dist\BrowserHistoryBrowser\" -ForegroundColor White
    Write-Host "Executable: dist\BrowserHistoryBrowser\BrowserHistoryBrowser.exe" -ForegroundColor White
    
    if ($CreateZip) {
        Write-Host "ZIP archive: $zipPath" -ForegroundColor White
    } else {
        Write-Host "`nTo create ZIP: .\build.ps1 -CreateZip" -ForegroundColor Cyan
    }

} catch {
    Write-Host "`n================================" -ForegroundColor Red
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Write-Host "================================" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}