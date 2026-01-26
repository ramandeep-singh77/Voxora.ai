#!/usr/bin/env python3
"""
Quick fix for MediaPipe compatibility issue
This script will install the correct MediaPipe version
"""

import subprocess
import sys
import os

def fix_mediapipe():
    print("\n" + "="*60)
    print("  VOXORA.AI - MEDIAPIPE FIX")
    print("="*60)
    print("\n🔧 Fixing MediaPipe compatibility issue...")
    
    try:
        # Uninstall current MediaPipe
        print("📦 Uninstalling current MediaPipe...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "mediapipe", "-y"], 
                      capture_output=True)
        
        # Install compatible version
        print("📦 Installing compatible MediaPipe version...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "mediapipe==0.10.9"], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ MediaPipe fixed successfully!")
            print("\n🚀 You can now run the application:")
            print("   python run.py")
            print("   or double-click RUN.bat")
        else:
            print("❌ Failed to install MediaPipe")
            print("Error:", result.stderr)
            print("\n🔧 Try manually:")
            print("   pip uninstall mediapipe")
            print("   pip install mediapipe==0.10.9")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Try manually:")
        print("   pip uninstall mediapipe")
        print("   pip install mediapipe==0.10.9")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    fix_mediapipe()
    input("\nPress Enter to exit...")