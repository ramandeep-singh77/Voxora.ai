#!/usr/bin/env python3
"""
🤟 Voxora.AI - One-Click Launcher
Starts both Flask backend and React frontend automatically
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("📦 Checking dependencies...")
    
    # Check if key packages are already installed
    try:
        import flask, cv2, tensorflow, numpy, mediapipe
        print("✅ Python dependencies already installed")
        python_deps_ok = True
    except ImportError:
        python_deps_ok = False
    
    # Install Python dependencies if needed
    if not python_deps_ok:
        print("📦 Installing Python dependencies...")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  check=True, capture_output=True, text=True)
            print("✅ Python dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Python dependencies:")
            print(f"   Error: {e.stderr}")
            print(f"   Try running manually: pip install -r requirements.txt")
            return False
    
    # Install Node.js dependencies
    react_dir = Path("ASL-Hand-sign-language-translator--main")
    node_modules = react_dir / "node_modules"
    
    if node_modules.exists():
        print("✅ Node.js dependencies already installed")
    else:
        print("📦 Installing Node.js dependencies...")
        if react_dir.exists():
            try:
                result = subprocess.run(["npm", "install"], cwd=react_dir, check=True, capture_output=True, text=True)
                print("✅ Node.js dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install Node.js dependencies:")
                print(f"   Error: {e.stderr}")
                print("   Make sure Node.js is installed: https://nodejs.org")
                return False
    
    return True

def start_flask_server():
    """Start Flask backend server"""
    print("🚀 Starting Flask backend...")
    try:
        # Import and run the Flask app
        from web_app import app, load_model
        load_model()
        app.run(debug=False, threaded=True, host='127.0.0.1', port=5000, use_reloader=False)
    except Exception as e:
        print(f"❌ Flask server error: {e}")

def start_react_ui():
    """Start React frontend"""
    print("🎨 Starting React UI...")
    react_dir = Path("ASL-Hand-sign-language-translator--main")
    
    if not react_dir.exists():
        print("❌ React UI directory not found")
        return
    
    try:
        subprocess.run(["npm", "run", "dev"], cwd=react_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ React UI error: {e}")
    except KeyboardInterrupt:
        print("\n⏹️  React UI stopped")

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "web_app.py",
        "hand_detector.py", 
        "models/signity_model.h5",
        "requirements.txt",
        "ASL-Hand-sign-language-translator--main/package.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("\n" + "="*60)
    print("  🤟 VOXORA.AI - ONE-CLICK LAUNCHER")
    print("="*60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup incomplete. Please ensure all files are present.")
        input("Press Enter to exit...")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed.")
        input("Press Enter to exit...")
        return
    
    print("\n🚀 Starting Voxora.AI...")
    print("   Flask API: http://localhost:5000")
    print("   React UI:  http://localhost:3000")
    print("\n⚠️  Keep this window open while using the app")
    print("   Press Ctrl+C to stop\n")
    
    # Start Flask server in background thread
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(3)
    
    # Open browser
    try:
        webbrowser.open("http://localhost:3000")
    except:
        pass
    
    # Start React UI (this will block until stopped)
    try:
        start_react_ui()
    except KeyboardInterrupt:
        print("\n\n⏹️  Voxora.AI stopped")
        print("   Thank you for using Voxora.AI! 🤟")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Voxora.AI stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")