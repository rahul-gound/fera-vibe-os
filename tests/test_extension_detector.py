"""Tests for the Extension Detection Engine."""

import json
import os
import tempfile

import pytest

from core.extension_detector import ExtensionDetector


@pytest.fixture
def sample_config(tmp_path):
    """Write a minimal runtime_map.json and return its path."""
    data = {
        ".exe": {"runtime": "wine", "type": "container", "description": "Windows"},
        ".py": {"runtime": "python", "type": "native", "description": "Python"},
        ".js": {"runtime": "node", "type": "native", "description": "Node"},
        ".apk": {"runtime": "android-runtime", "type": "container", "description": "Android"},
        ".obsd": {"runtime": "openbsd-vm", "type": "vm", "description": "OpenBSD VM"},
    }
    config = tmp_path / "runtime_map.json"
    config.write_text(json.dumps(data))
    return str(config)


@pytest.fixture
def detector(sample_config):
    return ExtensionDetector(config_path=sample_config)


class TestDetectExtension:
    def test_exe(self, detector):
        assert detector.detect_extension("app.exe") == ".exe"

    def test_py(self, detector):
        assert detector.detect_extension("/home/user/script.py") == ".py"

    def test_js(self, detector):
        assert detector.detect_extension("server.js") == ".js"

    def test_no_extension(self, detector):
        assert detector.detect_extension("Makefile") == ""

    def test_compound_extension(self, detector):
        assert detector.detect_extension("archive.tar.gz") == ".gz"


class TestSelectRuntime:
    def test_known_extension(self, detector):
        entry = detector.select_runtime("game.exe")
        assert entry is not None
        assert entry["runtime"] == "wine"
        assert entry["type"] == "container"

    def test_python(self, detector):
        entry = detector.select_runtime("script.py")
        assert entry["runtime"] == "python"

    def test_unknown_extension(self, detector):
        assert detector.select_runtime("file.xyz") is None

    def test_vm_type(self, detector):
        entry = detector.select_runtime("daemon.obsd")
        assert entry["type"] == "vm"


class TestSupportedExtensions:
    def test_lists_all(self, detector):
        exts = detector.supported_extensions
        assert ".exe" in exts
        assert ".py" in exts
        assert ".js" in exts

    def test_reload(self, detector, sample_config):
        with open(sample_config, "r") as f:
            data = json.load(f)
        data[".rb"] = {"runtime": "ruby", "type": "native", "description": "Ruby"}
        with open(sample_config, "w") as f:
            json.dump(data, f)
        detector.reload()
        assert ".rb" in detector.supported_extensions
