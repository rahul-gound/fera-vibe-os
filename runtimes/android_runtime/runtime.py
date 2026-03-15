"""Android Runtime – runs .apk files in an Android container."""

import logging
import os
import subprocess

log = logging.getLogger(__name__)

ANDROID_CONTAINER_IMAGE = "anbox/anbox:latest"


class AndroidRuntime:
    """Handle execution of Android ``.apk`` applications."""

    def launch_native(self, filepath):
        """Install and run an APK using a local Android emulator / Anbox."""
        log.info("Installing APK %s via adb", filepath)
        subprocess.run(["adb", "install", filepath], check=True)
        # Best-effort: derive package name from filename.  For production
        # use, parse `aapt dump badging <apk>` to get the real package id.
        package = os.path.splitext(os.path.basename(filepath))[0]
        return subprocess.run(
            ["adb", "shell", "monkey", "-p", package, "1"],
            check=True,
        )

    def launch_in_container(self, filepath, sandbox):
        """Run inside an Android container (e.g. Anbox)."""
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        mount = f"{directory}:/data/app"
        log.info("Running %s in Android container", filepath)
        return sandbox.launch(
            ANDROID_CONTAINER_IMAGE,
            ["install-and-run", f"/data/app/{filename}"],
            mounts=[mount],
        )
