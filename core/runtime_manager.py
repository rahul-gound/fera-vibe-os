"""Runtime Manager.

Central orchestrator that ties together the Extension Detector,
Sandbox, VM Manager and individual runtime wrappers to launch an
application in the correct environment.
"""

import logging
import os

from core.extension_detector import ExtensionDetector
from core.sandbox import Sandbox
from vm.vm_manager import VMManager
from runtimes.windows_runtime.runtime import WindowsRuntime
from runtimes.android_runtime.runtime import AndroidRuntime
from runtimes.linux_runtime.runtime import LinuxRuntime
from runtimes.bsd_runtime.runtime import BSDRuntime

log = logging.getLogger(__name__)


RUNTIME_HANDLERS = {
    "wine": WindowsRuntime,
    "android-runtime": AndroidRuntime,
    "linux-native": LinuxRuntime,
    "python": LinuxRuntime,
    "node": LinuxRuntime,
    "freebsd-container": BSDRuntime,
    "openbsd-vm": BSDRuntime,
}


class RuntimeManager:
    """Select and launch the correct runtime for a given file."""

    def __init__(self, config_path=None):
        self._detector = ExtensionDetector(config_path)
        self._sandbox = Sandbox()
        self._vm_manager = VMManager()

    def detect_extension(self, filepath):
        """Convenience proxy to :meth:`ExtensionDetector.detect_extension`."""
        return self._detector.detect_extension(filepath)

    def select_runtime(self, filepath):
        """Return the runtime configuration dict for *filepath*."""
        return self._detector.select_runtime(filepath)

    def launch(self, filepath):
        """Launch *filepath* in the appropriate runtime.

        Steps performed:
        1. detect file type
        2. select runtime
        3. start container or VM as needed
        4. launch application
        """
        filepath = os.path.abspath(filepath)
        entry = self.select_runtime(filepath)
        if entry is None:
            raise ValueError(
                f"Unsupported file type: {self._detector.detect_extension(filepath)}"
            )

        runtime_name = entry["runtime"]
        exec_type = entry["type"]

        handler_cls = RUNTIME_HANDLERS.get(runtime_name)
        if handler_cls is None:
            raise ValueError(f"No handler registered for runtime: {runtime_name}")

        handler = handler_cls()
        log.info(
            "Launching %s with runtime=%s type=%s",
            filepath,
            runtime_name,
            exec_type,
        )

        if exec_type == "vm":
            return self._vm_manager.launch(filepath, runtime_name)
        if exec_type == "container":
            return handler.launch_in_container(filepath, self._sandbox)
        return handler.launch_native(filepath)

    @property
    def supported_extensions(self):
        return self._detector.supported_extensions
