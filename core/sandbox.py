"""Container / Sandbox engine.

Provides isolation for applications using Linux namespaces, Docker,
Podman, or other containerisation backends.
"""

import logging
import shutil
import subprocess

log = logging.getLogger(__name__)


class Sandbox:
    """Manage containerised execution of applications."""

    BACKENDS = ("podman", "docker")

    def __init__(self, backend=None):
        self._backend = backend or self._detect_backend()

    def _detect_backend(self):
        """Auto-detect the first available container backend."""
        for name in self.BACKENDS:
            if shutil.which(name):
                log.info("Detected container backend: %s", name)
                return name
        log.warning("No container backend found; sandbox will be unavailable")
        return None

    @property
    def available(self):
        """Return True when a usable container backend is present."""
        return self._backend is not None

    def launch(self, image, command, mounts=None):
        """Start a container.

        Parameters
        ----------
        image : str
            Container image name (e.g. ``"wine:latest"``).
        command : list[str]
            Command and arguments to run inside the container.
        mounts : list[str] | None
            Optional bind-mount specifications (``host:container``).

        Returns
        -------
        subprocess.CompletedProcess
        """
        if not self.available:
            raise RuntimeError("No container backend is available")

        cmd = [self._backend, "run", "--rm"]
        for mount in (mounts or []):
            cmd.extend(["-v", mount])
        cmd.append(image)
        cmd.extend(command)

        log.info("Launching container: %s", " ".join(cmd))
        return subprocess.run(cmd, check=True)

    def stop(self, container_id):
        """Stop a running container by its ID."""
        if not self.available:
            raise RuntimeError("No container backend is available")

        cmd = [self._backend, "stop", container_id]
        log.info("Stopping container %s", container_id)
        return subprocess.run(cmd, check=True)
