"""Launcher – CLI entry point for the universal runtime OS.

Usage::

    python -m ui.launcher <filepath>

The launcher automatically detects the file type, selects the
appropriate runtime, and starts the application in a container,
VM, or natively.
"""

import argparse
import logging
import sys

from core.runtime_manager import RuntimeManager

log = logging.getLogger("fera-vibe-os")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Fera Vibe OS – Universal Application Launcher",
    )
    parser.add_argument("file", help="Path to the application file to launch")
    parser.add_argument(
        "--config",
        default=None,
        help="Path to a custom runtime_map.json",
    )
    parser.add_argument(
        "--list-extensions",
        action="store_true",
        help="List supported file extensions and exit",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    manager = RuntimeManager(config_path=args.config)

    if args.list_extensions:
        print("Supported extensions:")
        for ext in manager.supported_extensions:
            print(f"  {ext}")
        return 0

    filepath = args.file
    entry = manager.select_runtime(filepath)
    if entry is None:
        ext = manager.detect_extension(filepath)
        log.error("No runtime found for extension '%s'", ext)
        return 1

    log.info("File     : %s", filepath)
    log.info("Runtime  : %s (%s)", entry["runtime"], entry["description"])
    log.info("Type     : %s", entry["type"])

    try:
        manager.launch(filepath)
    except Exception as exc:
        log.error("Failed to launch: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
