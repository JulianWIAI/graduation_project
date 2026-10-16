#!/usr/bin/env bash
# build_dmg_mac.sh - Full pipeline: C++ compile -> locate dylibs -> PyInstaller -> .dmg
#
# Usage (run from daw_light_version/):
#   chmod +x build_dmg_mac.sh
#   ./build_dmg_mac.sh
#
# Prerequisites (install once before running):
#   xcode-select --install          # Xcode Command Line Tools (compiler)
#   brew install cmake fluid-synth  # CMake + FluidSynth
#   pip install pybind11 numpy      # pybind11 for C++ bindings

set -e  # stop on first error

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
step()  { echo -e "\n${CYAN}==> $1${NC}"; }
ok()    { echo -e "    ${GREEN}OK: $1${NC}"; }
warn()  { echo -e "    ${YELLOW}WARN: $1${NC}"; }
abort() { echo -e "\n${RED}ABORTED: $1${NC}"; exit 1; }

# ---------------------------------------------------------------------------
# Step 1 - Verify Python
# ---------------------------------------------------------------------------
step "Checking Python"
python3 --version || abort "python3 not found. Install from python.org or via brew install python."
ok "$(python3 --version)"

# ---------------------------------------------------------------------------
# Step 2 - Install / verify PyInstaller
# ---------------------------------------------------------------------------
step "Checking PyInstaller"
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "    PyInstaller not found - installing..."
    pip3 install pyinstaller || abort "pip install pyinstaller failed."
fi
ok "PyInstaller $(python3 -c 'import PyInstaller; print(PyInstaller.__version__)')"

# ---------------------------------------------------------------------------
# Step 3 - Compile C++ extension
# ---------------------------------------------------------------------------
step "Compiling C++ extension (daw_processors)"

CPP_DIR="$SCRIPT_DIR/cpp_processors"
cd "$CPP_DIR"
python3 setup.py build_ext --inplace || abort "C++ build failed. Make sure Xcode CLT and cmake are installed."
cd "$SCRIPT_DIR"

# Verify .so was produced
EXT_FILE=$(ls "$CPP_DIR"/daw_processors*.so 2>/dev/null | head -1)
if [ -z "$EXT_FILE" ]; then
    abort "daw_processors*.so not found after build."
fi
ok "Found $(basename "$EXT_FILE")"

# ---------------------------------------------------------------------------
# Step 4 - Locate FluidSynth dylibs and copy them next to the .so
# ---------------------------------------------------------------------------
step "Locating FluidSynth dylibs"

FLUID_FOUND=0
FLUID_LIB=""

# Search Homebrew (Apple Silicon and Intel) + common paths
for dir in \
    /opt/homebrew/lib \
    /usr/local/lib \
    /opt/local/lib \
    /usr/lib
do
    candidate="$dir/libfluidsynth.dylib"
    if [ -f "$candidate" ]; then
        FLUID_LIB="$dir"
        FLUID_FOUND=1
        ok "Found libfluidsynth.dylib in $dir"
        break
    fi
done

if [ $FLUID_FOUND -eq 1 ]; then
    # Copy the main dylib and common dependencies
    for lib in libfluidsynth*.dylib libsndfile*.dylib libglib*.dylib libSDL*.dylib; do
        src=$(ls "$FLUID_LIB/$lib" 2>/dev/null | head -1)
        if [ -n "$src" ]; then
            cp "$src" "$CPP_DIR/" 2>/dev/null && ok "Bundled: $(basename "$src")" || true
        fi
    done
else
    warn "libfluidsynth.dylib not found."
    warn "Audio playback may fail. Install with: brew install fluid-synth"
fi

# ---------------------------------------------------------------------------
# Step 5 - Run PyInstaller
# ---------------------------------------------------------------------------
step "Running PyInstaller (this can take several minutes)"

rm -rf "$SCRIPT_DIR/build" "$SCRIPT_DIR/dist"
python3 -m PyInstaller daw_light.spec || abort "PyInstaller failed."

APP_PATH="$SCRIPT_DIR/dist/SBS-Synth-Master.app"
if [ ! -d "$APP_PATH" ]; then
    abort "SBS-Synth-Master.app not found after PyInstaller."
fi
ok "App bundle created: $APP_PATH"

# ---------------------------------------------------------------------------
# Step 6 - Create .dmg
# ---------------------------------------------------------------------------
step "Creating .dmg"

DMG_PATH="$SCRIPT_DIR/dist/SBS-Synth-Master.dmg"
rm -f "$DMG_PATH"

hdiutil create \
    -volname "SBS-Synth-Master" \
    -srcfolder "$APP_PATH" \
    -ov \
    -format UDZO \
    "$DMG_PATH" || abort "hdiutil failed to create .dmg"

DMG_SIZE=$(du -sh "$DMG_PATH" | cut -f1)
echo ""
echo "============================================================"
echo "  BUILD SUCCESSFUL"
echo "  Output : $DMG_PATH"
echo "  Size   : $DMG_SIZE"
echo "============================================================"
echo ""
echo "Notes:"
echo "  * First launch extracts to a temp folder - expect 5-15 s startup."
echo "  * macOS Gatekeeper will block unsigned apps."
echo "    Users must right-click the .app -> Open -> Open anyway."
echo "  * To distribute cleanly: sign with an Apple Developer account (\$99/yr)."
