@echo off
title Interactive Learning Mat - Build Standalone Executable
echo ====================================================================
echo ✨ Packaging Interactive Learning Mat into Standalone App ✨
echo ====================================================================

:: Check if virtual environment exists
if not exist venv (
    echo [INFO] No virtual environment found. Creating one...
    python -m venv venv
)

:: Activate the virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

:: Ensure all requirements are installed
echo [INFO] Ensuring all dependencies are installed...
pip install -r requirements.txt
pip install pyinstaller

:: Clean old builds
echo [INFO] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Build the standalone folder using PyInstaller
echo [INFO] Running PyInstaller...
pyinstaller --noconsole --name "InteractiveLearningMat" --add-data "dataset;dataset" --add-data "images;images" --add-data "html;html" --add-data "firebase_key.json;." --collect-all customtkinter main.py

if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller build failed!
    pause
    exit /b
)

echo.
echo ====================================================================
echo 🎉 BUILD SUCCESSFUL! 🎉
echo ====================================================================
echo Your standalone application is ready inside the folder:
echo.
echo    dist\InteractiveLearningMat\
echo.
echo You can zip this folder and share it with anyone.
echo They just need to double-click:
echo.
echo    dist\InteractiveLearningMat\InteractiveLearningMat.exe
echo.
echo (They do not need to install Python, libraries, or anything else!)
echo ====================================================================
echo.
pause
