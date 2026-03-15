"""Tests for the VM Manager."""

from unittest.mock import patch

import pytest

from vm.vm_manager import VMManager


class TestVMManager:
    def test_available_when_qemu_found(self):
        vm = VMManager(qemu_bin="/usr/bin/qemu-system-x86_64")
        assert vm.available is True

    def test_unavailable_when_no_qemu(self):
        vm = VMManager(qemu_bin=None)
        # explicitly clear to simulate missing binary
        vm._qemu_bin = None
        assert vm.available is False

    def test_launch_raises_when_unavailable(self):
        vm = VMManager(qemu_bin=None)
        vm._qemu_bin = None
        with pytest.raises(RuntimeError, match="QEMU is not installed"):
            vm.launch("/tmp/binary.obsd", "openbsd-vm")

    @patch("subprocess.run")
    def test_launch_constructs_command(self, mock_run):
        vm = VMManager(qemu_bin="/usr/bin/qemu-system-x86_64", memory="1G", cpus=2)
        vm.launch("/tmp/binary.obsd", "openbsd-vm")
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "/usr/bin/qemu-system-x86_64"
        assert "-m" in args
        assert "1G" in args
        assert "-smp" in args
        assert "2" in args
