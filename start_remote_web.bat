@echo off
title Pierre's Power Scraper - Remote Web Server
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" web_server.py --port 8055
) else (
    python web_server.py --port 8055
)
pause
