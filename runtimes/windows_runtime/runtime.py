"""Windows Runtime – runs .exe files via Wine."""

import logging
import os
import shutil
import subprocess

log = logging.getLogger(__name__)

WINE_CONTAINER_IMAGE = "scottyhardy/docker-wine:latest"


class WindowsRuntime:
    """Handle execution of Windows ``.exe`` applications."""

    def launch_native(self, filepath):
        """Attempt to run with a locally installed Wine."""
        wine = shutil.which("wine")
        if wine is None:
            raise RuntimeError("Wine is not installed locally")
        log.info("Running %s with local Wine", filepath)
        return subprocess.run([wine, filepath], check=True)

    def launch_in_container(self, filepath, sandbox):
        """Run inside a Wine container."""
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        mount = f"{directory}:/app"
        log.info("Running %s in Wine container", filepath)
        return sandbox.launch(
            WINE_CONTAINER_IMAGE,
            ["wine", f"/app/{filename}"],
            mounts=[mount],
        )
