# Pierre's Power Scraper - Remote Web & Tunnel Launcher
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ⚡ Starting Pierre's Power Scraper Web & ngrok Tunnel..." -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "[!] Virtual environment not found at $VenvPython" -ForegroundColor Red
    Write-Host "Falling back to system python..."
    $VenvPython = "python"
}

& $VenvPython "web_server.py" --port 8055
