# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\Files\\Documents\\Project\\yancheng_playground\\MultiScreenMateHost\\server.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\Files\\Documents\\Project\\yancheng_playground\\MultiScreenMateHost\\functions', 'functions/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['opencv-python', 'cv2', 'tkinter', 'matplotlib', 'PyQt5', 'PIL'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='server',
)
