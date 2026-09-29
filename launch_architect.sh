#!/usr/bin/env bash
# Launcher: Music Architect V7
set -e
cd "$(dirname "$0")/music_architect_v7"

VENV=".venv/bin/python"
if [ ! -f "$VENV" ]; then
  echo "ERROR: .venv not found in music_architect_v7. Run setup.sh first." >&2
  exit 1
fi

# FluidSynth library path
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/fluid-synth/lib:/usr/local/opt/fluid-synth/lib:${DYLD_LIBRARY_PATH}"

exec "$VENV" main.py "$@"
