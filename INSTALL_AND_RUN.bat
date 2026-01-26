@echo off
title Voxora.AI - Install and Run
color 0A
cls

echo.
echo ===============================================
echo   VOXORA.AI - INSTALL AND RUN
echo ===============================================
echo.
echo This will install required packages and start Voxora.AI
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.8+ from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Check if Node.js is available
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js not found!
    echo.
    echo Please install Node.js 16+ from: https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo Node.js found:
node --version
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python packages one by one
echo.
echo Installing Python packages (this may take 5-10 minutes)...
echo Please be patient...
echo.

echo Installing Flask...
python -m pip install flask flask-cors
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Flask installation failed, but continuing...
)

echo Installing OpenCV...
python -m pip install opencv-python
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: OpenCV installation failed, but continuing...
)

echo Installing NumPy...
python -m pip install numpy
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: NumPy installation failed, but continuing...
)

echo Installing MediaPipe...
python -m pip install mediapipe
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: MediaPipe installation failed, but continuing...
)

echo Installing TensorFlow (this may take a while)...
python -m pip install tensorflow
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: TensorFlow installation failed, trying CPU version...
    python -m pip install tensorflow-cpu
)

echo Installing additional packages...
python -m pip install openai scikit-learn

echo.
echo Python packages installation completed!
echo.

REM Install Node.js packages
cd ASL-Hand-sign-language-translator--main
if not exist "node_modules" (
    echo Installing Node.js packages...
    npm install
    if %ERRORLEVEL% NEQ 0 (
        echo WARNING: Node.js packages installation failed
        echo You may need to run: npm install manually
    )
)
cd ..

echo.
echo ===============================================
echo   STARTING VOXORA.AI
echo ===============================================
echo.

REM Kill any existing processes
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)

REM Start Flask backend
echo Starting Flask backend...
start "Voxora.AI - Flask Backend" cmd /c "python web_app.py"

REM Wait for Flask to start
timeout /t 8 /nobreak >nul

REM Start React UI
echo Starting React UI...
cd ASL-Hand-sign-language-translator--main
start "Voxora.AI - React UI" cmd /c "npm run dev"
cd ..

REM Wait for React to start
timeout /t 10 /nobreak >nul

REM Open browser
echo Opening browser...
start http://localhost:3000

echo.
echo ===============================================
echo   VOXORA.AI IS RUNNING!
echo ===============================================
echo.
echo   React UI:  http://localhost:3000
echo   Flask API: http://localhost:5000
echo.
echo   If browser didn't open, go to: http://localhost:3000
echo.
echo   Ready to recognize signs!
echo   Hold each sign for 1 second
echo.

pause