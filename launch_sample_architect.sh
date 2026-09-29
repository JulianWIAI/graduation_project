#!/usr/bin/env bash
# Launcher: Sample Architect
set -e
cd "$(dirname "$0")/sample_architect"

VENV=".venv/bin/python"
if [ ! -f "$VENV" ]; then
  echo "ERROR: .venv not found in sample_architect. Run setup.sh first." >&2
  exit 1
fi

exec "$VENV" main.py "$@"
