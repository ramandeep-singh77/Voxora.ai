@echo off
title Voxora.AI - One-Click Launcher
color 0A

echo.
echo ===============================================
echo   🤟 VOXORA.AI - ONE-CLICK LAUNCHER
echo ===============================================
echo.

echo Trying full launcher with dependency installation...
python run.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Full launcher failed. Trying simple launcher...
    echo Make sure you have installed:
    echo - pip install -r requirements.txt
    echo - cd ASL-Hand-sign-language-translator--main ^&^& npm install
    echo.
    python run_simple.py
)

pause