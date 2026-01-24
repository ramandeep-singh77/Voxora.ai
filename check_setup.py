#!/usr/bin/env python3
"""
Voxora.AI Setup Checker
Verifies that all required files and dependencies are present
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file(filepath, description, required=True):
    """Check if file exists"""
    if os.path.exists(filepath):
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"✅ {description}: {filepath} ({size_mb:.1f}MB)")
        return True
    else:
        status = "❌" if required else "⚠️ "
        print(f"{status} {description}: {filepath} - {'MISSING' if required else 'Optional'}")
        return not required

def check_python_package(package_name):
    """Check if Python package is installed"""
    try:
        __import__(package_name)
        print(f"✅ Python package: {package_name}")
        return True
    except ImportError:
        print(f"❌ Python package: {package_name} - NOT INSTALLED")
        return False

def check_node_modules():
    """Check Node.js modules"""
    react_dir = Path("ASL-Hand-sign-language-translator--main")
    node_modules = react_dir / "node_modules"
    
    if node_modules.exists():
        print(f"✅ Node.js modules: {node_modules}")
        return True
    else:
        print(f"❌ Node.js modules: {node_modules} - NOT INSTALLED")
        return False

def main():
    """Main check function"""
    print("\n" + "="*60)
    print("  VOXORA.AI SETUP CHECKER")
    print("="*60)
    
    all_good = True
    
    print("\n🔍 Checking core files...")
    
    # Core application files
    core_files = [
        ("web_app.py", "Flask backend"),
        ("hand_detector.py", "Hand detection module"),
        ("requirements.txt", "Python dependencies"),
        ("ASL-Hand-sign-language-translator--main/package.json", "React UI config"),
        ("ASL-Hand-sign-language-translator--main/src/App.jsx", "React main component"),
    ]
    
    for filepath, description in core_files:
        if not check_file(filepath, description):
            all_good = False
    
    print("\n🧠 Checking AI model...")
    
    # Model files (most important)
    model_files = [
        ("models/signity_model.h5", "Main trained model"),
        ("processed_data/class_mapping.json", "Class mapping", False),
        ("confusion_correction/confusion_classifiers.pkl", "Confusion correction", False),
    ]
    
    for filepath, description, *required in model_files:
        req = required[0] if required else True
        if not check_file(filepath, description, req):
            if req:
                all_good = False
    
    print("\n📦 Checking Python dependencies...")
    
    # Python packages
    python_packages = [
        "flask", "flask_cors", "cv2", "tensorflow", 
        "numpy", "mediapipe", "openai"
    ]
    
    for package in python_packages:
        if not check_python_package(package):
            all_good = False
    
    print("\n🌐 Checking Node.js setup...")
    
    if not check_node_modules():
        all_good = False
    
    print("\n" + "="*60)
    
    if all_good:
        print("  ✅ ALL CHECKS PASSED! 🎉")
        print("="*60)
        print("\n🚀 Ready to run:")
        print("   Double-click: start.bat (Windows) or ./start.sh (Linux/Mac)")
        print("   Or run: python web_app.py")
        print("\n🌐 Then open: http://localhost:3000")
    else:
        print("  ❌ SETUP INCOMPLETE")
        print("="*60)
        print("\n🔧 To fix issues:")
        print("   1. Run: python setup.py")
        print("   2. Or manually:")
        print("      - python download_model.py")
        print("      - pip install -r requirements.txt")
        print("      - cd ASL-Hand-sign-language-translator--main && npm install")
    
    print("="*60)
    return all_good

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during check: {e}")
        sys.exit(1)