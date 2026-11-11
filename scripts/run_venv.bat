@echo off
setlocal
set "PROJECT_ROOT=%~dp0.."
set "PYTHON=%PROJECT_ROOT%\.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Virtual environment not found: "%PROJECT_ROOT%\.venv"
    echo Create it with: py -3.11 -m venv .venv
    exit /b 1
)

"%PYTHON%" --version
