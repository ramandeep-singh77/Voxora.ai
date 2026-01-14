@echo off
echo ============================================================
echo   VOXORA.AI - Starting Application
echo ============================================================
echo.
echo [1/2] Starting Flask Backend (Port 5000)...
start "Voxora Backend" cmd /k "python web_app.py"
timeout /t 3 /nobreak > nul

echo [2/2] Starting React Frontend (Port 3000)...
cd ASL-Hand-sign-language-translator--main
start "Voxora Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ============================================================
echo   Application Started!
echo ============================================================
echo.
echo Backend API:  http://localhost:5000
echo Frontend UI:  http://localhost:3000
echo.
echo Wait 5 seconds, then open: http://localhost:3000
echo.
echo To stop: Close both command windows
echo ============================================================
