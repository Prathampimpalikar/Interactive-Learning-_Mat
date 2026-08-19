@echo off
title Interactive Learning Mat - Startup
echo ====================================================================
echo ✨ Starting Interactive Learning Mat Setup & Launch ✨
echo ====================================================================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not added to your system PATH!
    echo Please install Python 3.10 or higher from python.org
    echo Make sure to check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

:: Create virtual environment folder if it doesn't exist
if not exist venv (
    echo [INFO] Creating Python virtual environment (this only happens once)...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b
    )
)

:: Activate the virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

:: Install/Upgrade dependencies
echo [INFO] Verifying and installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] There was an issue installing some packages. Trying to run anyway...
)

:: Run the application
echo [INFO] Starting the application...
python main.py

echo.
echo Application closed.
pause
