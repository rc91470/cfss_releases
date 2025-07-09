# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Get the directory containing this spec file
spec_root = Path(SPECPATH).resolve()

block_cipher = None

# Define data files to include
data_files = [
    # Include sound files  
    ('sounds/*.mp3', 'sounds'),
    # Include additional Python modules
    ('data_manager.py', '.'),
    ('circuit_manager.py', '.'),
    ('scan_controller.py', '.'),
    ('auto_updater.py', '.'),
    # NOTE: Explicitly NOT including data/*.csv files for security
    # The data folder will be created empty in the build
]

# Hidden imports that PyInstaller might miss
hidden_imports = [
    'pygame',
    'customtkinter',
    'natsort',
    'tkinter',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'sqlite3',
    'csv',
    'json',
    'hashlib',
    'difflib',
    'socket',
    'getpass',
    'subprocess',
    'platform',
    'data_manager',
    'circuit_manager',
    'scan_controller',
    'auto_updater',
    'requests',
    'threading',
]

a = Analysis(
    ['cfss_app.py'],
    pathex=[str(spec_root)],
    binaries=[],
    datas=data_files,
    hiddenimports=hidden_imports,
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
    [],
    exclude_binaries=True,
    name='cfss_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='cfss_app',
)

app = BUNDLE(
    coll,
    name='CFSS.app',
    icon=None,  # You can add an icon file here if you have one
    bundle_identifier='com.cfss.scanner',
    version='4.2.3',
    info_plist={
        'CFBundleName': 'Copper/Fiber Serial Scanner',
        'CFBundleDisplayName': 'CFSS',
        'CFBundleVersion': '4.2.3',
        'CFBundleShortVersionString': '4.2.3',
        'CFBundleIdentifier': 'com.cfss.scanner',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',  # macOS High Sierra minimum
        'NSAppleEventsUsageDescription': 'This app needs access to system events for proper operation.',
        'NSMicrophoneUsageDescription': 'This app does not use the microphone.',
        'NSCameraUsageDescription': 'This app does not use the camera.',
        'LSApplicationCategoryType': 'public.app-category.utilities',
    },
)
