#!/usr/bin/env python3
"""
🤟 Voxora.AI - Super Simple Launcher
Just starts both services without complex dependency management
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def main():
    print("\n🤟 Starting Voxora.AI...")
    
    # Kill any existing processes on ports 3000 and 5000
    for port in [3000, 5000]:
        try:
            result = subprocess.run(f'netstat -ano | findstr :{port}', 
                                  shell=True, capture_output=True, text=True)
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            if pid.isdigit():
                                subprocess.run(f'taskkill /PID {pid} /F', 
                                             shell=True, capture_output=True)
                                print(f"✅ Killed process using port {port}")
        except:
            pass
    
    # Start Flask backend
    print("🚀 Starting Flask backend...")
    flask_cmd = f'start "Flask Backend" cmd /c "python web_app.py"'
    subprocess.run(flask_cmd, shell=True)
    
    # Wait a moment
    time.sleep(3)
    
    # Start React UI
    print("🎨 Starting React UI...")
    react_dir = Path("ASL-Hand-sign-language-translator--main")
    if react_dir.exists():
        react_cmd = f'start "React UI" cmd /c "cd {react_dir} && npm run dev"'
        subprocess.run(react_cmd, shell=True)
    
    # Wait for services to start
    time.sleep(5)
    
    # Open browser
    print("🌐 Opening browser...")
    try:
        webbrowser.open("http://localhost:3000")
    except:
        pass
    
    print("\n✅ Voxora.AI started!")
    print("   Flask API: http://localhost:5000")
    print("   React UI:  http://localhost:3000")
    print("\n🎯 If browser didn't open, go to: http://localhost:3000")
    print("⚠️  Close the Flask and React windows to stop the app")

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")