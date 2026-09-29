#!/usr/bin/env bash
# Launcher: DAW Light Version
set -e
cd "$(dirname "$0")/daw_light_version"

VENV=".venv/bin/python"
if [ ! -f "$VENV" ]; then
  echo "ERROR: .venv not found in daw_light_version. Run setup.sh first." >&2
  exit 1
fi

# FluidSynth library path (Homebrew on Apple Silicon / Intel)
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/fluid-synth/lib:/usr/local/opt/fluid-synth/lib:${DYLD_LIBRARY_PATH}"
export FLUIDSYNTH_LIB="$(ls /opt/homebrew/opt/fluid-synth/lib/libfluidsynth.dylib 2>/dev/null || ls /usr/local/opt/fluid-synth/lib/libfluidsynth.dylib 2>/dev/null || echo '')"

exec "$VENV" main.py "$@"
