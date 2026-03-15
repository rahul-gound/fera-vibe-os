#!/usr/bin/env bash
# build.sh – Install dependencies and verify the Fera Vibe OS prototype
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Fera Vibe OS Build ==="

# Ensure Python 3 is available
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required" >&2
    exit 1
fi

echo "[1/3] Checking Python version …"
python3 --version

echo "[2/3] Verifying module imports …"
python3 -c "
from core.extension_detector import ExtensionDetector
from core.sandbox import Sandbox
from core.runtime_manager import RuntimeManager
from vm.vm_manager import VMManager
from runtimes.windows_runtime.runtime import WindowsRuntime
from runtimes.android_runtime.runtime import AndroidRuntime
from runtimes.linux_runtime.runtime import LinuxRuntime
from runtimes.bsd_runtime.runtime import BSDRuntime
print('All modules imported successfully.')
"

echo "[3/3] Running tests …"
python3 -m pytest tests/ -v

echo "=== Build complete ==="
