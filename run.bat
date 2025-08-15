@echo off
REM Preserv Archive Integrity Checker - Windows Launcher
REM ===================================================

echo.
echo Preserv - Archive Integrity Checker
echo ===================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Found virtual environment, activating...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found.
    echo Installing dependencies globally...
    pip install -r requirements.txt
)

REM Run Preserv
echo.
echo Starting Preserv...
python main.py

REM Pause to show any error messages
if errorlevel 1 (
    echo.
    echo Preserv exited with an error.
    pause
)
