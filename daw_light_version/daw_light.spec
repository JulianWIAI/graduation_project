# daw_light.spec — PyInstaller build spec for SBS-Synth Master
#
# Works on both Windows (.exe) and macOS (.app + .dmg).
# Run from inside daw_light_version/ with:
#   python -m PyInstaller daw_light.spec
#
# Windows prerequisites:
#   1. Run build_exe_windows.ps1  (compiles C++, copies DLLs, then calls this)
# macOS prerequisites:
#   1. Run build_dmg_mac.sh       (compiles C++, copies dylibs, then calls this)

import glob
import os
import sys

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

IS_MAC = sys.platform == "darwin"
IS_WIN = sys.platform == "win32"

# ---------------------------------------------------------------------------
# Locate the compiled C++ extension (.pyd on Windows, .so on macOS)
# ---------------------------------------------------------------------------
if IS_WIN:
    _ext_matches = glob.glob("cpp_processors/daw_processors*.pyd")
    _ext_hint = "powershell -ExecutionPolicy Bypass -File cpp_processors\\build_win.ps1"
else:
    _ext_matches = glob.glob("cpp_processors/daw_processors*.so")
    _ext_hint = "cd cpp_processors && python setup.py build_ext --inplace"

if not _ext_matches:
    raise FileNotFoundError(
        "daw_processors extension not found in cpp_processors/.\n"
        "Compile it first:  " + _ext_hint
    )
_ext_path = _ext_matches[0]

# ---------------------------------------------------------------------------
# Binaries: C++ extension + audio runtime libraries
# ---------------------------------------------------------------------------
binaries = [
    (_ext_path, "cpp_processors"),
]

if IS_WIN:
    # DLLs copied by build_exe_windows.ps1 (libfluidsynth-3.dll, SDL3.dll, sndfile.dll)
    for _dll in glob.glob("cpp_processors/*.dll"):
        binaries.append((_dll, "."))
else:
    # dylibs copied by build_dmg_mac.sh (libfluidsynth, libsndfile, etc.)
    for _lib in glob.glob("cpp_processors/*.dylib"):
        binaries.append((_lib, "."))

# ---------------------------------------------------------------------------
# Data files
# ---------------------------------------------------------------------------
datas = [
    ("benchmarks", "benchmarks"),
    ("assets",     "assets"),
    ("soundfonts", "soundfonts"),
]

try:
    datas += collect_data_files("librosa")
except Exception:
    pass

try:
    datas += collect_data_files("sklearn")
except Exception:
    pass

# ---------------------------------------------------------------------------
# Hidden imports
# ---------------------------------------------------------------------------
hiddenimports = [
    "PySide6.QtPrintSupport",
    "PySide6.QtOpenGL",
    "PySide6.QtOpenGLWidgets",
    "PySide6.QtMultimedia",
    "PySide6.QtSvg",
    "sounddevice",
    "soundfile",
    "pyfluidsynth",
    "rtmidi",
    "mido.backends.rtmidi",
    "scipy.spatial.transform._rotation_groups",
    "scipy._lib.messagestream",
    "scipy.special.cython_special",
    "sklearn.utils._cython_blas",
    "sklearn.neighbors.typedefs",
    "sklearn.neighbors._partition_nodes",
    "sklearn.tree._utils",
    "sentence_transformers",
    "transformers",
]

try:
    hiddenimports += collect_submodules("sklearn")
except Exception:
    pass

# ---------------------------------------------------------------------------
# Icon
# ---------------------------------------------------------------------------
if IS_WIN:
    _icon_arg = "assets/icons/icon.ico" if os.path.exists("assets/icons/icon.ico") else None
else:
    _icon_arg = "assets/icons/icon.icns" if os.path.exists("assets/icons/icon.icns") else None

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
block_cipher = None

a = Analysis(
    ["main.py"],
    pathex=[".", "cpp_processors"],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["rt_hook_cpp.py"],
    excludes=["tkinter", "matplotlib", "IPython", "jupyter", "notebook"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ---------------------------------------------------------------------------
# Windows: single .exe
# ---------------------------------------------------------------------------
if IS_WIN:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name="SBS-Synth-Master",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=["vcruntime140.dll", "python3*.dll", "Qt6*.dll", "PySide6"],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=_icon_arg,
    )

# ---------------------------------------------------------------------------
# macOS: .app bundle (build_dmg_mac.sh wraps it into a .dmg afterwards)
# ---------------------------------------------------------------------------
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name="SBS-Synth-Master",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=_icon_arg,
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name="SBS-Synth-Master",
    )

    app = BUNDLE(
        coll,
        name="SBS-Synth-Master.app",
        icon=_icon_arg,
        bundle_identifier="com.sbsstudio.sbs-synth-master",
        info_plist={
            "NSHighResolutionCapable": True,
            "NSMicrophoneUsageDescription": "SBS-Synth Master needs microphone access for audio input.",
        },
    )
