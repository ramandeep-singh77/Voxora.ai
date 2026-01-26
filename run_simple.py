#!/usr/bin/env python3
"""
🤟 Voxora.AI - Simple Launcher (No Dependency Installation)
For users who already have dependencies installed
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path

def start_flask_server():
    """Start Flask backend server"""
    print("🚀 Starting Flask backend...")
    try:
        from web_app import app, load_model
        load_model()
        app.run(debug=False, threaded=True, host='127.0.0.1', port=5000, use_reloader=False)
    except Exception as e:
        print(f"❌ Flask server error: {e}")

def start_react_ui():
    """Start React frontend"""
    print("🎨 Starting React UI...")
    react_dir = Path("ASL-Hand-sign-language-translator--main")
    
    try:
        subprocess.run(["npm", "run", "dev"], cwd=react_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ React UI error: {e}")
    except KeyboardInterrupt:
        print("\n⏹️  React UI stopped")

def main():
    """Main launcher function"""
    print("\n" + "="*60)
    print("  🤟 VOXORA.AI - SIMPLE LAUNCHER")
    print("="*60)
    
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