"""
A simple Locust performance test runner for use from the project root.

USAGE:
    python backend/app/core/locust_load_test/_tests/performance_test.py

This will launch the Locust web UI (http://localhost:8089) using the main locustfile.py.
You can also add CLI options (e.g. --headless --users 100 --spawn-rate 10) as needed.

Requirements:
- locust must be installed in your environment (pip install locust)
- The backend must be running and accessible

Author: Ty (following Clean Code & Pragmatic Programmer best practices)
"""
import sys
import subprocess
from pathlib import Path

# Path to the main locustfile.py
LOCUSTFILE = Path(__file__).parent.parent / "locustfile.py"

if not LOCUSTFILE.exists():
    print(f"ERROR: Could not find locustfile.py at {LOCUSTFILE}")
    sys.exit(1)

# Build the base command
cmd = [
    sys.executable, '-m', 'locust',
    '-f', str(LOCUSTFILE),
]

# Pass through any extra CLI args (e.g. --headless --users 100)
cmd += sys.argv[1:]

print("Running Locust with command:", ' '.join(cmd))

try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"Locust exited with error: {e}")
    sys.exit(e.returncode)
