"""VM Manager.

Manages lightweight QEMU virtual machines for binaries that cannot
run natively or inside a Linux container (e.g. OpenBSD binaries).
"""

import logging
import os
import shutil
import subprocess

log = logging.getLogger(__name__)


class VMManager:
    """Start, stop and manage QEMU-based lightweight VMs."""

    def __init__(self, qemu_bin=None, memory="512M", cpus=1):
        self._qemu_bin = qemu_bin or shutil.which("qemu-system-x86_64")
        self._memory = memory
        self._cpus = cpus

    @property
    def available(self):
        """Return True when QEMU is installed."""
        return self._qemu_bin is not None

    def launch(self, filepath, runtime_name, disk_image=None):
        """Boot a lightweight VM and inject *filepath* for execution.

        Parameters
        ----------
        filepath : str
            Path to the binary to run inside the VM.
        runtime_name : str
            Name of the runtime (used to select the VM image).
        disk_image : str | None
            Optional path to a QEMU disk image.  When ``None`` a
            default image based on *runtime_name* is used.

        Returns
        -------
        subprocess.CompletedProcess
        """
        if not self.available:
            raise RuntimeError("QEMU is not installed")

        image = disk_image or f"/var/lib/fera-vibe-os/images/{runtime_name}.qcow2"

        cmd = [
            self._qemu_bin,
            "-m", self._memory,
            "-smp", str(self._cpus),
            "-drive", f"file={image},format=qcow2",
            "-virtfs",
            f"local,path={os.path.dirname(filepath)},mount_tag=hostshare,security_model=mapped-xattr",
            "-nographic",
        ]
        log.info("Starting VM: %s", " ".join(cmd))
        return subprocess.run(cmd, check=True)
