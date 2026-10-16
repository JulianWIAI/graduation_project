"""
Build script for daw_processors C++ extension.

Usage:
    pip install pybind11 numpy
    python setup.py build_ext --inplace

Or with pip (preferred):
    pip install .

Compatible with pybind11 2.x and 3.x — uses get_include() directly
instead of the setup_helpers module that was removed in pybind11 3.0.
"""

import sys
from pathlib import Path

try:
    import pybind11
except ImportError:
    raise SystemExit(
        "pybind11 is required to build this extension. "
        "Install it with: pip install pybind11"
    )

from setuptools import Extension, setup

import glob as _glob
import shutil

BASE = Path(__file__).parent

# ---------------------------------------------------------------------------
# Detect optional dependency: sfizz (SFZ instrument engine)
# sfizz.h must be on the include path for SfizzEngine.cpp to compile.
# We probe common install locations; if not found, the two sfizz-specific
# files are excluded and DAW_NO_SFIZZ is defined so bindings.cpp skips them.
# ---------------------------------------------------------------------------
_SFIZZ_SEARCH = [
    "/usr/include",
    "/usr/local/include",
    "/opt/homebrew/include",
    "C:/sfizz/include",
    "C:/tools/sfizz/include",
]

def _sfizz_available():
    for d in _SFIZZ_SEARCH:
        if Path(d, "sfizz.h").exists():
            return True
    # Also accept if sfizz-config or pkg-config reports it
    return shutil.which("sfizz-config") is not None

HAVE_SFIZZ = _sfizz_available()
if not HAVE_SFIZZ:
    print("setup.py: sfizz not found -- building without SFZ engine (DAW_NO_SFIZZ)")

# Auto-discover every .cpp in src/, then exclude sfizz files when unavailable.
_SFIZZ_FILES = {"SfizzEngine.cpp", "bindings_sfz.cpp"}
SOURCES = sorted(
    f for f in _glob.glob(str(BASE / "src" / "*.cpp"))
    if HAVE_SFIZZ or Path(f).name not in _SFIZZ_FILES
)

# Compiler-specific optimisation flags.
if sys.platform == "win32":
    extra_args = [
        "/std:c++17",
        "/O2",
        "/arch:AVX2",
        "/fp:fast",
        "/DNOMINMAX",
    ]
    if not HAVE_SFIZZ:
        extra_args.append("/DDAW_NO_SFIZZ")
    extra_link_args = []
else:
    extra_args = [
        "-O3",
        "-ffast-math",
        "-std=c++17",
        "-mmacosx-version-min=10.15",
    ]
    if not HAVE_SFIZZ:
        extra_args.append("-DDAW_NO_SFIZZ")
    extra_link_args = []

ext = Extension(
    name="daw_processors",
    sources=SOURCES,
    # pybind11.get_include() returns the path to pybind11's headers,
    # which works with every pybind11 version including 3.x.
    include_dirs=[
        str(BASE / "include"),
        pybind11.get_include(),
    ],
    extra_compile_args=extra_args,
    extra_link_args=extra_link_args,
    language="c++",
)

setup(
    name="daw_processors",
    version="1.0.0",
    description="Real-time C++ dynamics processors for a Python DAW",
    ext_modules=[ext],
    python_requires=">=3.8",
    install_requires=["pybind11>=2.10", "numpy"],
    zip_safe=False,
)
