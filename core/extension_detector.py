"""Extension Detection Engine.

Detects file extensions and maps them to the appropriate runtime
using the runtime registry configuration.
"""

import json
import os


DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "configs",
    "runtime_map.json",
)


class ExtensionDetector:
    """Detects file type by extension and resolves the matching runtime."""

    def __init__(self, config_path=None):
        self._config_path = config_path or DEFAULT_CONFIG_PATH
        self._runtime_map = self._load_runtime_map()

    def _load_runtime_map(self):
        """Load the runtime map from the JSON configuration file."""
        with open(self._config_path, "r") as fh:
            return json.load(fh)

    def reload(self):
        """Reload the runtime map from disk."""
        self._runtime_map = self._load_runtime_map()

    def detect_extension(self, filepath):
        """Return the file extension (including the leading dot).

        For compound extensions like ``.tar.gz`` only the last extension
        is returned.  Returns an empty string when there is no extension.
        """
        _, ext = os.path.splitext(filepath)
        return ext

    def select_runtime(self, filepath):
        """Look up the runtime entry for *filepath*.

        Returns the runtime configuration dict from the registry or
        ``None`` when no mapping exists.
        """
        ext = self.detect_extension(filepath)
        return self._runtime_map.get(ext)

    @property
    def supported_extensions(self):
        """Return the list of currently supported extensions."""
        return list(self._runtime_map.keys())
