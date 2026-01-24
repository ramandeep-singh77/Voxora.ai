@echo off
title Voxora.AI - Quick Start
color 0A

echo.
echo ===============================================
echo   VOXORA.AI - QUICK START
echo ===============================================
echo.

echo Checking setup...
python check_setup.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Setup incomplete. Running automatic setup...
    echo.
    python setup.py
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Setup failed. Please check the errors above.
        pause
        exit /b 1
    )
)

echo.
echo ===============================================
echo   STARTING VOXORA.AI
echo ===============================================
echo.
echo Opening React UI at: http://localhost:3000
echo Starting Flask API at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the application
echo.

start "" cmd /c "cd ASL-Hand-sign-language-translator--main && npm run dev"
timeout /t 3 /nobreak >nul
python web_app.py

pause