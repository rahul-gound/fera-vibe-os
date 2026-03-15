"""Tests for the CLI launcher."""

from unittest.mock import patch, MagicMock

import pytest

from ui.launcher import main


class TestLauncherCLI:
    @patch("ui.launcher.RuntimeManager")
    def test_list_extensions(self, mock_mgr_cls, capsys):
        mock_mgr = MagicMock()
        mock_mgr.supported_extensions = [".exe", ".py", ".js"]
        mock_mgr_cls.return_value = mock_mgr

        rc = main(["--list-extensions", "dummy"])
        assert rc == 0
        out = capsys.readouterr().out
        assert ".exe" in out
        assert ".py" in out

    @patch("ui.launcher.RuntimeManager")
    def test_unknown_extension(self, mock_mgr_cls):
        mock_mgr = MagicMock()
        mock_mgr.select_runtime.return_value = None
        mock_mgr.detect_extension.return_value = ".xyz"
        mock_mgr_cls.return_value = mock_mgr

        rc = main(["somefile.xyz"])
        assert rc == 1

    @patch("ui.launcher.RuntimeManager")
    def test_successful_launch(self, mock_mgr_cls):
        mock_mgr = MagicMock()
        mock_mgr.select_runtime.return_value = {
            "runtime": "python",
            "type": "native",
            "description": "Python script",
        }
        mock_mgr_cls.return_value = mock_mgr

        rc = main(["script.py"])
        assert rc == 0
        mock_mgr.launch.assert_called_once()
