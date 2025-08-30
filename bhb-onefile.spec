# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Get the directory where the spec file is located
spec_dir = Path(SPECPATH)

# Define the main entry point
entry_point = spec_dir / 'server.py'

# Analysis of the main script
a = Analysis(
    [str(entry_point)],
    pathex=[str(spec_dir)],
    binaries=[],
    datas=[
        # Include backend module
        (str(spec_dir / 'backend'), 'backend'),
        (str(spec_dir / 'static'), 'static'),
    ],
    hiddenimports=[
        'backend',
        'backend.main',
        'backend.models', 
        'backend.services',
        'backend.database',
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets.websockets_impl',
        'uvicorn.protocols.http.httptools_impl',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.loops.auto',
        'uvicorn.loops.asyncio',
        'uvicorn.logging'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Generate the PYZ archive
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Generate the onefile executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BrowserHistoryBrowser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
