@echo off
cd /d "%~dp0"
echo ==========================================
echo   URBAN COOLING STRATEGY ENGINE (UCSE)
echo ==========================================
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10+ and enable Add Python to PATH.
  pause
  exit /b 1
)
if not exist .venv\Scripts\python.exe (
  echo Creating virtual environment...
  python -m venv .venv
)
echo Installing / checking dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed. Check your internet connection and try again.
  pause
  exit /b 1
)
echo Starting UCSE at http://127.0.0.1:8000
echo Keep this window open while using the dashboard.
start "UCSE Dashboard" http://127.0.0.1:8000
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
