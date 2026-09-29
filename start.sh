#!/usr/bin/env bash
# start.sh — Interactive launcher menu for the graduation project suite
ROOT="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║        Graduation Project — Music Suite          ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  1) DAW Light Version        (PySide6 GUI)       ║"
echo "║  2) Music Architect V7       (AI MIDI Generator) ║"
echo "║  3) Music Catalogue Manager  (Web Server :5000)  ║"
echo "║  4) Sample Architect         (Sample Library)    ║"
echo "║  q) Quit                                         ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
read -rp "Choose [1-4/q]: " CHOICE

case "$CHOICE" in
  1) exec "$ROOT/launch_daw.sh" ;;
  2) exec "$ROOT/launch_architect.sh" ;;
  3) exec "$ROOT/launch_catalogue.sh" ;;
  4) exec "$ROOT/launch_sample_architect.sh" ;;
  q|Q) echo "Bye!"; exit 0 ;;
  *) echo "Invalid choice: $CHOICE"; exit 1 ;;
esac
