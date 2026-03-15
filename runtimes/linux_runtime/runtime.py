"""Linux Runtime – handles .deb, .rpm, .AppImage, .py and .js files."""

import logging
import os
import shutil
import subprocess

log = logging.getLogger(__name__)


INTERPRETERS = {
    ".py": "python3",
    ".js": "node",
}


class LinuxRuntime:
    """Handle execution of Linux-native applications and scripts."""

    def launch_native(self, filepath):
        """Run the file natively on the host."""
        ext = os.path.splitext(filepath)[1]

        interpreter = INTERPRETERS.get(ext)
        if interpreter:
            binary = shutil.which(interpreter)
            if binary is None:
                raise RuntimeError(f"{interpreter} is not installed")
            log.info("Running %s with %s", filepath, interpreter)
            return subprocess.run([binary, filepath], check=True)

        if ext == ".AppImage":
            os.chmod(filepath, 0o755)
            log.info("Running AppImage %s", filepath)
            return subprocess.run([filepath], check=True)

        if ext == ".deb":
            log.info("Installing deb package %s", filepath)
            return subprocess.run(["dpkg", "-i", filepath], check=True)

        if ext == ".rpm":
            log.info("Installing rpm package %s", filepath)
            return subprocess.run(["rpm", "-i", filepath], check=True)

        raise ValueError(f"Unsupported Linux file type: {ext}")

    def launch_in_container(self, filepath, sandbox):
        """Run inside a Linux container."""
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        mount = f"{directory}:/app"
        ext = os.path.splitext(filepath)[1]

        interpreter = INTERPRETERS.get(ext)
        if interpreter:
            cmd = [interpreter, f"/app/{filename}"]
        else:
            cmd = [f"/app/{filename}"]

        log.info("Running %s in Linux container", filepath)
        return sandbox.launch("ubuntu:latest", cmd, mounts=[mount])
