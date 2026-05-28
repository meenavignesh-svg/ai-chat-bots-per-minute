# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ["helixmind_bio_ai.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        "bioinformatics_tools",
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "speech_recognition",
        "pyaudio",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="HelixMindBioAI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="HelixMindBioAI",
)
