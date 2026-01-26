# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Data files to include
datas = [
    ('models', 'models'),
    ('processed_data', 'processed_data'),
    ('confusion_correction', 'confusion_correction'),
    ('ASL-Hand-sign-language-translator--main', 'ASL-Hand-sign-language-translator--main'),
    ('requirements.txt', '.'),
    ('config.py', '.'),
    ('hand_detector.py', '.'),
    ('web_app.py', '.'),
]

# Hidden imports for TensorFlow and other packages
hiddenimports = [
    'tensorflow',
    'tensorflow.keras',
    'tensorflow.keras.models',
    'tensorflow.keras.layers',
    'cv2',
    'mediapipe',
    'numpy',
    'flask',
    'flask_cors',
    'openai',
    'sklearn',
    'pickle',
    'json',
    'collections',
    'threading',
    'time',
    'os',
    'sys',
    'pathlib',
    'subprocess',
    'webbrowser',
    'tkinter',
    'tkinter.messagebox',
    'tkinter.ttk',
]

a = Analysis(
    ['voxora_launcher.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VoxoraAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for windowed app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)