@echo off
echo ============================================================
echo   VOXORA.AI - Installation
echo ============================================================
echo.

echo [1/2] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2/2] Installing Node.js dependencies...
cd ASL-Hand-sign-language-translator--main
call npm install
cd ..

echo.
echo ============================================================
echo   Installation Complete!
echo ============================================================
echo.
echo To start the application, run: start.bat
echo.
pause
