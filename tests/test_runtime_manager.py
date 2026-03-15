"""Tests for the Runtime Manager."""

import json
import os
from unittest.mock import patch, MagicMock

import pytest

from core.runtime_manager import RuntimeManager


@pytest.fixture
def config_path(tmp_path):
    data = {
        ".exe": {"runtime": "wine", "type": "container", "description": "Windows"},
        ".py": {"runtime": "python", "type": "native", "description": "Python"},
        ".obsd": {"runtime": "openbsd-vm", "type": "vm", "description": "OpenBSD VM"},
        ".deb": {"runtime": "linux-native", "type": "native", "description": "Debian"},
    }
    p = tmp_path / "runtime_map.json"
    p.write_text(json.dumps(data))
    return str(p)


@pytest.fixture
def manager(config_path):
    return RuntimeManager(config_path=config_path)


class TestRuntimeManager:
    def test_detect_extension(self, manager):
        assert manager.detect_extension("app.exe") == ".exe"

    def test_select_runtime_known(self, manager):
        entry = manager.select_runtime("hello.py")
        assert entry["runtime"] == "python"

    def test_select_runtime_unknown(self, manager):
        assert manager.select_runtime("file.xyz") is None

    def test_supported_extensions(self, manager):
        exts = manager.supported_extensions
        assert ".exe" in exts
        assert ".py" in exts

    def test_launch_unsupported_raises(self, manager):
        with pytest.raises(ValueError, match="Unsupported file type"):
            manager.launch("file.unknown")

    @patch("runtimes.linux_runtime.runtime.LinuxRuntime.launch_native")
    def test_launch_native_python(self, mock_launch, manager, tmp_path):
        script = tmp_path / "hello.py"
        script.write_text("print('hello')")
        manager.launch(str(script))
        mock_launch.assert_called_once()

    @patch("core.sandbox.Sandbox.launch")
    @patch("core.sandbox.Sandbox.available", new_callable=lambda: property(lambda self: True))
    def test_launch_container_exe(self, _mock_avail, mock_sandbox_launch, manager, tmp_path):
        exe = tmp_path / "game.exe"
        exe.write_text("")
        manager.launch(str(exe))
        mock_sandbox_launch.assert_called_once()

    @patch("vm.vm_manager.VMManager.launch")
    @patch("vm.vm_manager.VMManager.available", new_callable=lambda: property(lambda self: True))
    def test_launch_vm_obsd(self, _mock_avail, mock_vm_launch, manager, tmp_path):
        binary = tmp_path / "daemon.obsd"
        binary.write_text("")
        manager.launch(str(binary))
        mock_vm_launch.assert_called_once()
