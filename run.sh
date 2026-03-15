#!/usr/bin/env bash
# run.sh – Launch an application through Fera Vibe OS
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <filepath> [--verbose]"
    echo ""
    echo "Examples:"
    echo "  $0 app.exe"
    echo "  $0 script.py --verbose"
    echo "  $0 --list-extensions"
    exit 1
fi

exec python3 -m ui.launcher "$@"
