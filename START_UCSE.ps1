$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python 3.10+ is required. Install it and enable Add Python to PATH.' }
if (-not (Test-Path '.venv/Scripts/python.exe')) { python -m venv .venv }
.venv/Scripts/python.exe -m pip install -r requirements.txt
Start-Process 'http://127.0.0.1:8000'
.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
