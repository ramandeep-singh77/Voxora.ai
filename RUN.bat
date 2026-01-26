@echo off
title Voxora.AI - One-Click Launcher
color 0A

echo.
echo ===============================================
echo   🤟 VOXORA.AI - ONE-CLICK LAUNCHER
echo ===============================================
echo.

echo Starting Voxora.AI...
python run.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Launcher failed. Trying alternative method...
    echo.
    echo Starting Flask backend...
    start "Flask Backend" cmd /c "python web_app.py"
    
    timeout /t 5 /nobreak >nul
    
    echo Starting React UI...
    cd ASL-Hand-sign-language-translator--main
    start "React UI" cmd /c "npm run dev"
    cd ..
    
    echo.
    echo ✅ Started manually. Open http://localhost:3000 in your browser
    echo.
)

echo.
echo Press any key to exit...
pause >nul