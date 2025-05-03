"""
Test suite for run_distributed_locust.py
Ensures CLI argument parsing and command construction work as expected.

This does NOT start real Locust processes. It uses mocking to verify subprocess and argument handling.

Run with: pytest test_run_distributed_locust.py
"""
import sys
import subprocess
import types
import pytest
from pathlib import Path
from unittest import mock

# Path to the script under test
SCRIPT_PATH = Path(__file__).parent.parent / "run_distributed_locust.py"

@pytest.mark.parametrize(
    "cli_args,expected_in_cmd",
    [
        (["--master", "--users", "50", "--spawn-rate", "5"], ["--master", "--users 50", "--spawn-rate 5"]),
        (["--worker", "--host", "127.0.0.1", "--port", "9000"], ["--worker", "--master-host 127.0.0.1", "--master-port 9000"]),
    ],
)
def test_run_distributed_locust_cli(monkeypatch, cli_args, expected_in_cmd):
    """
    Test that the CLI builds the correct command for master/worker modes.
    """
    # Patch sys.argv
    monkeypatch.setattr(sys, "argv", [str(SCRIPT_PATH)] + cli_args)

    # Patch Path.exists to always return True for locustfile
    with mock.patch("pathlib.Path.exists", return_value=True):
        # Patch subprocess.run to capture the command
        with mock.patch("subprocess.run") as mock_run:
            # Import the script as a module (runs main)
            import importlib.util
            spec = importlib.util.spec_from_file_location("run_distributed_locust", SCRIPT_PATH)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except SystemExit:
                pass  # expected for sys.exit()

            # Ensure subprocess.run was called
            assert mock_run.called, "subprocess.run was not called"
            cmd_str = mock_run.call_args[0][0]
            for fragment in expected_in_cmd:
                assert fragment in cmd_str, f"Expected '{fragment}' in command: {cmd_str}"


def test_run_distributed_locust_no_role(monkeypatch):
    """
    Test that missing --master/--worker exits with error.
    """
    monkeypatch.setattr(sys, "argv", [str(SCRIPT_PATH)])
    with mock.patch("pathlib.Path.exists", return_value=True):
        with mock.patch("subprocess.run") as mock_run:
            import importlib.util
            spec = importlib.util.spec_from_file_location("run_distributed_locust", SCRIPT_PATH)
            mod = importlib.util.module_from_spec(spec)
            with pytest.raises(SystemExit) as excinfo:
                spec.loader.exec_module(mod)
            assert excinfo.value.code == 2
            assert not mock_run.called


def test_run_distributed_locust_missing_locustfile(monkeypatch):
    """
    Test that missing locustfile.py exits with error.
    """
    monkeypatch.setattr(sys, "argv", [str(SCRIPT_PATH), "--master"])
    with mock.patch("pathlib.Path.exists", return_value=False):
        with mock.patch("subprocess.run") as mock_run:
            import importlib.util
            spec = importlib.util.spec_from_file_location("run_distributed_locust", SCRIPT_PATH)
            mod = importlib.util.module_from_spec(spec)
            with pytest.raises(SystemExit) as excinfo:
                spec.loader.exec_module(mod)
            assert excinfo.value.code == 1
            assert not mock_run.called
