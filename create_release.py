#!/usr/bin/env python3
"""
GitHub Release Creator for Voxora.AI
Creates a GitHub release with the model file
"""

import os
import sys
import json
import hashlib
from pathlib import Path

def calculate_file_hash(filepath):
    """Calculate SHA256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def get_file_size_mb(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def main():
    """Main function"""
    print("\n" + "="*60)
    print("  VOXORA.AI RELEASE CREATOR")
    print("="*60)
    
    model_path = Path("models/signity_model.h5")
    
    if not model_path.exists():
        print(f"❌ Model file not found: {model_path}")
        print("   Make sure the trained model exists before creating a release.")
        return False
    
    # Get model info
    file_size_mb = get_file_size_mb(model_path)
    file_hash = calculate_file_hash(model_path)
    
    print(f"\n📊 Model Information:")
    print(f"   File: {model_path}")
    print(f"   Size: {file_size_mb:.1f} MB")
    print(f"   SHA256: {file_hash}")
    
    # Update download_model.py with correct info
    download_script = Path("download_model.py")
    if download_script.exists():
        content = download_script.read_text(encoding='utf-8')
        content = content.replace("'size_mb': 45.2,", f"'size_mb': {file_size_mb:.1f},")
        content = content.replace("'sha256': 'placeholder_hash',", f"'sha256': '{file_hash}',")
        download_script.write_text(content, encoding='utf-8')
        print(f"✅ Updated download_model.py with correct file info")
    
    print(f"\n📋 Next Steps:")
    print(f"1. Commit and push all changes:")
    print(f"   git add .")
    print(f"   git commit -m 'Add model download scripts and setup tools'")
    print(f"   git push origin main")
    print(f"")
    print(f"2. Create a GitHub release:")
    print(f"   - Go to: https://github.com/ramandeep-singh77/Voxora.ai/releases")
    print(f"   - Click 'Create a new release'")
    print(f"   - Tag: v1.0")
    print(f"   - Title: Voxora.AI v1.0")
    print(f"   - Upload: {model_path} ({file_size_mb:.1f}MB)")
    print(f"")
    print(f"3. Or use GitHub CLI:")
    print(f"   gh release create v1.0 {model_path} --title 'Voxora.AI v1.0' --notes 'Initial release with trained model'")
    print(f"")
    print(f"4. Test the download:")
    print(f"   python download_model.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)