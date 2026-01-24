#!/usr/bin/env python3
"""
Voxora.AI Setup Script
One-click setup for the entire application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_node_version():
    """Check Node.js version"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js version: {version}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found. Please install Node.js 16+ from https://nodejs.org")
    return False

def install_python_dependencies():
    """Install Python dependencies"""
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def install_node_dependencies():
    """Install Node.js dependencies"""
    react_dir = Path("ASL-Hand-sign-language-translator--main")
    if not react_dir.exists():
        print("❌ React UI directory not found")
        return False
    
    original_dir = os.getcwd()
    try:
        os.chdir(react_dir)
        success = run_command("npm install", "Installing Node.js dependencies")
        return success
    finally:
        os.chdir(original_dir)

def download_model():
    """Download the trained model"""
    model_path = Path("models/signity_model.h5")
    if model_path.exists():
        print("✅ Model already exists")
        return True
    
    print("📥 Downloading trained model...")
    try:
        import download_model
        return download_model.main()
    except Exception as e:
        print(f"❌ Model download failed: {e}")
        return False

def create_start_script():
    """Create platform-specific start script"""
    if platform.system() == "Windows":
        script_content = '''@echo off
echo Starting Voxora.AI...
echo.
echo Opening React UI (http://localhost:3000)...
start "" cmd /c "cd ASL-Hand-sign-language-translator--main && npm run dev"

echo.
echo Starting Flask API (http://localhost:5000)...
python web_app.py

pause
'''
        with open("start.bat", "w") as f:
            f.write(script_content)
        print("✅ Created start.bat")
    else:
        script_content = '''#!/bin/bash
echo "Starting Voxora.AI..."
echo ""
echo "Opening React UI (http://localhost:3000)..."
cd ASL-Hand-sign-language-translator--main && npm run dev &

echo ""
echo "Starting Flask API (http://localhost:5000)..."
python3 web_app.py
'''
        with open("start.sh", "w") as f:
            f.write(script_content)
        os.chmod("start.sh", 0o755)
        print("✅ Created start.sh")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  VOXORA.AI SETUP")
    print("="*60)
    print("\n🔍 Checking system requirements...")
    
    # Check requirements
    if not check_python_version():
        return False
    
    if not check_node_version():
        return False
    
    print("\n📦 Installing dependencies...")
    
    # Install Python dependencies
    if not install_python_dependencies():
        return False
    
    # Install Node.js dependencies
    if not install_node_dependencies():
        return False
    
    print("\n🧠 Setting up AI model...")
    
    # Download model
    if not download_model():
        print("⚠️  Model download failed, but you can download it manually later")
    
    print("\n🚀 Creating start scripts...")
    create_start_script()
    
    print("\n" + "="*60)
    print("  SETUP COMPLETE! 🎉")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Double-click start.bat (Windows) or run ./start.sh (Linux/Mac)")
    print("2. Open browser to: http://localhost:3000")
    print("3. Allow camera access when prompted")
    print("4. Start signing! 🤟")
    print("\n📚 Documentation: README.md")
    print("🐛 Issues: https://github.com/ramandeep-singh77/Voxora.ai/issues")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)