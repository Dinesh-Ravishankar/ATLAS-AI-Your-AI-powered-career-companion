@echo off
:: ============================================================
::  Atlas AI — One-Click Startup (CMD)
::  Double-click this file or run:  start.bat
:: ============================================================

title Atlas AI Launcher

echo.
echo   ======================================
echo        ATLAS AI — Starting Up
echo   ======================================
echo.

:: ---------- 1. Backend ----------
echo [1/2] Starting Backend (FastAPI on port 8000)...
cd /d "%~dp0backend"

set PYTHON_EXE=C:\Users\dines\AppData\Roaming\uv\python\cpython-3.11.14-windows-x86_64-none\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=python

start "Atlas-Backend" %PYTHON_EXE% -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo       Backend  -^>  http://localhost:8000
echo       API Docs -^>  http://localhost:8000/docs

:: ---------- 2. Frontend ----------
echo [2/2] Starting Frontend (Next.js on port 3000)...
cd /d "%~dp0frontend"

start "Atlas-Frontend" npm run dev

echo       Frontend -^>  http://localhost:3000

:: ---------- Done ----------
echo.
echo   ======================================
echo     Frontend : http://localhost:3000
echo     Backend  : http://localhost:8000
echo     API Docs : http://localhost:8000/docs
echo   ======================================
echo.

:: Open browser after a short delay
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo   Press any key to exit this launcher...
pause >nul
