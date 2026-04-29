@echo off
REM Setup script for Swach AI Carbon Agent Backend (Windows)
REM Run this to install dependencies and verify setup

cls
echo ============================================
echo Swach AI Carbon Agent - Backend Setup
echo ============================================
echo.

echo Checking Python version...
python --version
echo.

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt --quiet

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Create .env file:
echo    copy .env.example .env
echo    (Then add your API keys to .env)
echo.
echo 2. Run tests to verify calculator:
echo    pytest test_calculator.py -v
echo.
echo 3. Run a quick test:
echo    python -c "from tools.calculator import *; print('OK: Import successful')"
echo.
pause
