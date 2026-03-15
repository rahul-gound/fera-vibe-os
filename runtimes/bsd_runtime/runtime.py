"""BSD Runtime – handles FreeBSD and OpenBSD binaries."""

import logging
import os

log = logging.getLogger(__name__)

FREEBSD_CONTAINER_IMAGE = "freebsd/freebsd:latest"


class BSDRuntime:
    """Handle execution of BSD binaries."""

    def launch_native(self, filepath):
        """BSD binaries cannot run natively on Linux."""
        raise RuntimeError(
            "BSD binaries require a container or VM; native execution is not supported"
        )

    def launch_in_container(self, filepath, sandbox):
        """Run a FreeBSD binary inside a FreeBSD container."""
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        mount = f"{directory}:/app"
        log.info("Running %s in FreeBSD container", filepath)
        return sandbox.launch(
            FREEBSD_CONTAINER_IMAGE,
            [f"/app/{filename}"],
            mounts=[mount],
        )
