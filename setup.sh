#!/usr/bin/env bash
# setup.sh — Recreate all virtual environments and install dependencies
# Run this once (or after moving the folder) from graduation_project/
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="python3"

# Check Python
if ! command -v $PYTHON &>/dev/null; then
  echo "ERROR: python3 not found. Install Python 3.11+ first." >&2
  exit 1
fi

# Check / install system deps via Homebrew
check_brew_pkg() {
  if ! brew list "$1" &>/dev/null; then
    echo "Installing system dependency: $1"
    brew install "$1"
  else
    echo "  [ok] $1 already installed"
  fi
}

echo "=== Checking system dependencies ==="
check_brew_pkg fluid-synth
check_brew_pkg ffmpeg
check_brew_pkg sdl2

install_project() {
  local NAME="$1"
  local DIR="$ROOT/$NAME"
  echo ""
  echo "=== Setting up: $NAME ==="

  if [ ! -d "$DIR" ]; then
    echo "  WARNING: $DIR not found, skipping."
    return
  fi

  # Recreate venv
  if [ -d "$DIR/.venv" ]; then
    echo "  Removing old .venv..."
    rm -rf "$DIR/.venv"
  fi
  echo "  Creating .venv..."
  $PYTHON -m venv "$DIR/.venv"

  # Upgrade pip silently
  "$DIR/.venv/bin/pip" install --upgrade pip -q

  if [ -f "$DIR/requirements.txt" ]; then
    echo "  Installing requirements.txt..."
    "$DIR/.venv/bin/pip" install -r "$DIR/requirements.txt"
  else
    echo "  WARNING: No requirements.txt found in $DIR"
  fi

  echo "  Done: $NAME"
}

install_project "daw_light_version"
install_project "music_architect_v7"
install_project "Music_catalogue_manager_v.2"
install_project "sample_architect"

echo ""
echo "=== All projects set up! ==="
echo ""
echo "Launch commands:"
echo "  ./launch_daw.sh              — DAW (drag & drop MIDI, FluidSynth playback)"
echo "  ./launch_architect.sh        — Music Architect V7 (AI beat/MIDI generation)"
echo "  ./launch_catalogue.sh        — Music Catalogue Manager (web server on :5000)"
echo "  ./launch_sample_architect.sh — Sample Architect (sample library manager)"
echo "  ./start.sh                   — Interactive launcher menu"
