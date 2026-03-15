"""Tests for the Sandbox (container engine)."""

from unittest.mock import patch, MagicMock

import pytest

from core.sandbox import Sandbox


class TestSandboxDetection:
    @patch("shutil.which", return_value="/usr/bin/podman")
    def test_detects_podman(self, _mock):
        s = Sandbox()
        assert s.available is True

    @patch("shutil.which", return_value=None)
    def test_no_backend(self, _mock):
        s = Sandbox()
        assert s.available is False

    def test_explicit_backend(self):
        s = Sandbox(backend="docker")
        assert s.available is True


class TestSandboxLaunch:
    def test_launch_no_backend_raises(self):
        s = Sandbox(backend=None)
        # Force unavailable
        s._backend = None
        with pytest.raises(RuntimeError, match="No container backend"):
            s.launch("image:latest", ["cmd"])

    @patch("subprocess.run")
    def test_launch_command(self, mock_run):
        s = Sandbox(backend="podman")
        s.launch("myimage:latest", ["echo", "hello"], mounts=["/host:/guest"])
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "podman"
        assert "myimage:latest" in args
        assert "-v" in args
        assert "/host:/guest" in args


class TestSandboxStop:
    @patch("subprocess.run")
    def test_stop(self, mock_run):
        s = Sandbox(backend="docker")
        s.stop("abc123")
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args == ["docker", "stop", "abc123"]
