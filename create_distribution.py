#!/usr/bin/env python3
"""
Create distribution package for Voxora.AI
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_distribution():
    """Create a distribution package"""
    print("📦 Creating Voxora.AI distribution package...")
    
    # Create distribution directory
    dist_dir = Path("VoxoraAI_Distribution")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Files to include in distribution
    files_to_copy = [
        # Core application files
        "web_app.py",
        "hand_detector.py",
        "config.py",
        "requirements.txt",
        "README.md",
        
        # Launcher scripts
        "start_simple.py",
        "run.py",
        "RUN.bat",
        
        # EXE launcher
        "dist/VoxoraAI_Launcher.exe",
    ]
    
    # Directories to copy
    dirs_to_copy = [
        "models",
        "processed_data", 
        "confusion_correction",
        "ASL-Hand-sign-language-translator--main",
    ]
    
    # Copy files
    for file_path in files_to_copy:
        src = Path(file_path)
        if src.exists():
            if src.parent.name == "dist":
                # Copy EXE to root of distribution
                dst = dist_dir / src.name
            else:
                dst = dist_dir / src.name
            shutil.copy2(src, dst)
            print(f"✅ Copied: {src} → {dst}")
        else:
            print(f"⚠️  Missing: {src}")
    
    # Copy directories
    for dir_path in dirs_to_copy:
        src = Path(dir_path)
        if src.exists():
            dst = dist_dir / src.name
            shutil.copytree(src, dst)
            print(f"✅ Copied directory: {src} → {dst}")
        else:
            print(f"⚠️  Missing directory: {src}")
    
    # Create a simple README for the distribution
    dist_readme = dist_dir / "README.txt"
    readme_content = """🤟 Voxora.AI - Distribution Package

QUICK START (Choose one method):

METHOD 1 - EXE Launcher (Easiest):
1. Double-click: VoxoraAI_Launcher.exe
2. Click "Start Voxora.AI" in the GUI
3. Browser opens automatically

METHOD 2 - Batch File:
1. Double-click: RUN.bat
2. Browser opens automatically

METHOD 3 - Python Script:
1. Run: python start_simple.py
2. Browser opens automatically

REQUIREMENTS:
- Python 3.8+ with packages: pip install -r requirements.txt
- Node.js 16+ from https://nodejs.org
- Webcam for sign detection

WHAT'S INCLUDED:
- VoxoraAI_Launcher.exe - GUI launcher (no Python needed to run this)
- Trained AI model (5MB) - Ready to use
- React UI - Modern web interface
- Flask backend - AI processing server
- All source code - Fully open source

USAGE:
1. Start the application using any method above
2. Allow camera access when prompted
3. Show ASL signs to the camera (hold for 1 second each)
4. Letters form words automatically
5. Click "Add Space" to complete words
6. Click "Correct & Show" for AI grammar correction

URLs:
- React UI: http://localhost:3000
- Flask API: http://localhost:5000

SUPPORT:
- GitHub: https://github.com/ramandeep-singh77/Voxora.ai
- Issues: https://github.com/ramandeep-singh77/Voxora.ai/issues

Made with 🤟 for the deaf and hard-of-hearing community
"""
    
    dist_readme.write_text(readme_content, encoding='utf-8')
    print(f"✅ Created: {dist_readme}")
    
    # Create ZIP file
    zip_path = Path("VoxoraAI_Complete_Package.zip")
    if zip_path.exists():
        zip_path.unlink()
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(dist_dir)
                zipf.write(file_path, arc_path)
                
    print(f"✅ Created ZIP: {zip_path}")
    
    # Get sizes
    dist_size = sum(f.stat().st_size for f in dist_dir.rglob('*') if f.is_file()) / (1024*1024)
    zip_size = zip_path.stat().st_size / (1024*1024)
    
    print(f"\n📊 Distribution Summary:")
    print(f"   Directory: {dist_dir} ({dist_size:.1f} MB)")
    print(f"   ZIP file: {zip_path} ({zip_size:.1f} MB)")
    print(f"   Files: {len(list(dist_dir.rglob('*')))}")
    
    print(f"\n🎉 Distribution package created successfully!")
    print(f"   Users can download and extract: {zip_path}")
    print(f"   Then double-click: VoxoraAI_Launcher.exe")

if __name__ == "__main__":
    create_distribution()