import argparse
import subprocess
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOCUSTFILE = Path(__file__).parent / "locustfile.py"


def main() -> None:
    """
    Distributed Locust runner for master/worker mode.
    All parameters are configurable via CLI or environment variables.
    """
    parser = argparse.ArgumentParser(description="Distributed Locust runner (production ready)")
    parser.add_argument("--master", action="store_true", help="Run as master node")
    parser.add_argument("--worker", action="store_true", help="Run as worker node")
    parser.add_argument("--host", type=str, default="localhost", help="Master host (for worker)")
    parser.add_argument("--port", type=int, default=8089, help="Master port (for worker)")
    parser.add_argument("--users", type=int, default=100, help="Number of users")
    parser.add_argument("--spawn-rate", type=float, default=10.0, help="User spawn rate per second")
    parser.add_argument("--expect-workers", type=int, default=1, help="Expected worker count (master)")
    parser.add_argument("--extra-args", type=str, default="", help="Extra args for locust command")
    args = parser.parse_args()

    if not LOCUSTFILE.exists():
        logger.error(f"Could not find locustfile.py at {LOCUSTFILE}")
        sys.exit(1)

    if args.master:
        cmd = (
            f"locust -f {LOCUSTFILE} --master --expect-workers {args.expect_workers} "
            f"--users {args.users} --spawn-rate {args.spawn_rate} {args.extra_args}"
        )
    elif args.worker:
        cmd = (
            f"locust -f {LOCUSTFILE} --worker --master-host {args.host} "
            f"--master-port {args.port} {args.extra_args}"
        )
    else:
        logger.error("Must specify --master or --worker")
        sys.exit(2)

    logger.info(f"Running command: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Locust process failed: {e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
