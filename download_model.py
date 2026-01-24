#!/usr/bin/env python3
"""
Voxora.AI Model Downloader
Downloads the trained model file from cloud storage
"""

import os
import sys
import requests
from pathlib import Path
import hashlib

# Model configuration
MODEL_INFO = {
    'filename': 'signity_model.h5',
    'size_mb': 5.0,
    'sha256': 'ee1358ef8ec7f0e94b8fb88facd023aadfc5d89a6f47224493327b059862c639',  # Will be updated with actual hash
    'download_urls': [
        # Primary: GitHub Release
        'https://github.com/ramandeep-singh77/Voxora.ai/releases/download/v1.0/signity_model.h5',
        # Backup: Direct GitHub raw (if release fails)
        'https://github.com/ramandeep-singh77/Voxora.ai/releases/latest/download/signity_model.h5',
        # Backup: Google Drive (will be updated with actual link)
        'https://drive.google.com/uc?export=download&id=1ABC123_PLACEHOLDER_GOOGLE_DRIVE_ID',
    ]
}

def download_file(url, filepath, chunk_size=8192):
    """Download file with progress bar"""
    try:
        print(f"📥 Downloading from: {url}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\r⏳ Progress: {progress:.1f}% ({downloaded/1024/1024:.1f}MB/{total_size/1024/1024:.1f}MB)", end='')
        
        print(f"\n✅ Downloaded: {filepath}")
        return True
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False

def verify_file(filepath, expected_size_mb=None):
    """Verify downloaded file"""
    if not os.path.exists(filepath):
        return False
    
    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
    
    if expected_size_mb and abs(file_size_mb - expected_size_mb) > 5:  # 5MB tolerance
        print(f"⚠️  File size mismatch: {file_size_mb:.1f}MB (expected ~{expected_size_mb}MB)")
        return False
    
    print(f"✅ File verified: {file_size_mb:.1f}MB")
    return True

def main():
    """Main download function"""
    print("\n" + "="*60)
    print("  VOXORA.AI MODEL DOWNLOADER")
    print("="*60)
    
    # Create models directory
    models_dir = Path('models')
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / MODEL_INFO['filename']
    
    # Check if model already exists
    if model_path.exists() and verify_file(model_path, MODEL_INFO['size_mb']):
        print(f"✅ Model already exists: {model_path}")
        print("🚀 You can now run: python web_app.py")
        return True
    
    print(f"📦 Downloading model: {MODEL_INFO['filename']}")
    print(f"📏 Expected size: ~{MODEL_INFO['size_mb']}MB")
    
    # Try each download URL
    for i, url in enumerate(MODEL_INFO['download_urls'], 1):
        print(f"\n🔄 Attempt {i}/{len(MODEL_INFO['download_urls'])}")
        
        if download_file(url, model_path):
            if verify_file(model_path, MODEL_INFO['size_mb']):
                print("\n🎉 Model downloaded successfully!")
                print("🚀 You can now run: python web_app.py")
                return True
            else:
                print("❌ File verification failed, trying next URL...")
                if model_path.exists():
                    os.remove(model_path)
        
        print("⏭️  Trying next download source...")
    
    print("\n❌ All download attempts failed!")
    print("\n📋 Manual Download Instructions:")
    print("1. Go to: https://github.com/ramandeep-singh77/Voxora.ai/releases")
    print("2. Download: signity_model.h5")
    print("3. Place it in: models/signity_model.h5")
    print("4. Run: python web_app.py")
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)