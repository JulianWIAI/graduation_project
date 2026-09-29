#!/usr/bin/env bash
# Launcher: Music Catalogue Manager V2  (Flask web server)
set -e
cd "$(dirname "$0")/Music_catalogue_manager_v.2"

VENV=".venv/bin/python"
if [ ! -f "$VENV" ]; then
  echo "ERROR: .venv not found in Music_catalogue_manager_v.2. Run setup.sh first." >&2
  exit 1
fi

echo "Starting Music Catalogue Manager..."
echo "Open http://127.0.0.1:5000 in your browser once the server is ready."
echo "Press Ctrl+C to stop."
echo ""

exec "$VENV" main.py "$@"
