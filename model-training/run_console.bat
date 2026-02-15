@echo off
if not exist "venv" (
    echo [ERROR] Virtual environment not found.
    echo Please run 'setup_env.bat' first.
    pause
    exit /b
)

call venv\Scripts\activate.bat
echo ==========================================
echo  AI Project Environment Activated
echo ==========================================
echo.
cmd /k
