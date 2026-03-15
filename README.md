# Fera Vibe OS

A universal runtime operating system platform that can run applications from
multiple ecosystems using the Linux kernel.

## Supported application types

| Extension   | Runtime           | Execution type |
|-------------|-------------------|----------------|
| `.exe`      | Wine              | container      |
| `.apk`      | Android container | container      |
| `.deb`      | Linux native      | native         |
| `.rpm`      | Linux native      | native         |
| `.AppImage` | Linux native      | native         |
| `.py`       | Python 3          | native         |
| `.js`       | Node.js           | native         |
| `.fbsd`     | FreeBSD container | container      |
| `.obsd`     | OpenBSD VM (QEMU) | vm             |

## Project structure

```
/kernel          – Linux kernel (submodule)
/core            – Runtime manager, extension detector, sandbox
/runtimes        – Per-ecosystem runtime wrappers
/vm              – QEMU-based VM manager
/ui              – CLI launcher
/configs         – Runtime registry (runtime_map.json)
/tests           – Unit tests
```

## Quick start

```bash
# Run the test suite
./build.sh

# Launch an application
./run.sh app.exe
./run.sh script.py --verbose

# List supported extensions
./run.sh --list-extensions dummy
```

## Requirements

- Python 3.8+
- pytest (for tests)
- Optional: Docker / Podman, Wine, QEMU, Node.js
