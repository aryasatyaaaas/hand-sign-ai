@echo off
echo ==========================================
echo  Setting up AI Project Environment...
echo ==========================================

REM Check for Python (Prioritize 3.10/3.11 for TensorFlow compatibility)
set "PYTHON_CMD="

REM Try Python 3.10
py -3.10 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py -3.10"
    goto :FoundPython
)

REM Try Python 3.11
py -3.11 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py -3.11"
    goto :FoundPython
)

REM Fallback to standard python/py
where python >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
    goto :FoundPython
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py"
    goto :FoundPython
)

:FoundPython
if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python not found! Please install Python 3.10 or 3.11.
    pause
    exit /b
)

echo Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    %PYTHON_CMD% -m venv venv
) else (
    echo [INFO] Virtual environment already exists.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip

REM Install dependencies
if exist "requirements.txt" (
    echo [INFO] Installing dependencies from requirements.txt...
    venv\Scripts\pip.exe install -r requirements.txt
) else (
    echo [WARNING] requirements.txt not found! Skipping installation.
)

echo.
echo ==========================================
echo  Setup Complete!
echo ==========================================
echo To start working, run: run_console.bat
echo.
pause
