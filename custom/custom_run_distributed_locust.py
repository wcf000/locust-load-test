"""
Script to run FastAPI Locust load tests in distributed mode.

This script allows running Locust tests for FastAPI in either master or worker mode.
It handles command-line arguments and constructs the proper Locust command.

Usage:
    # Master mode
    python custom_run_distributed_locust.py --master --users=100 --spawn-rate=10

    # Worker mode
    python custom_run_distributed_locust.py --worker --host=localhost
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add the parent directory to sys.path to allow importing config
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from app.core.locust_load_test.custom.config import (
    BASE_URL,
    LOCUST_MASTER_HOST,
    LOCUST_MASTER_PORT,
    LOCUST_USERS,
    LOCUST_SPAWN_RATE,
    LOCUST_RUN_TIME,
    LOCUST_EXPECT_WORKERS,
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run FastAPI load tests with Locust in distributed mode")
    
    # Mode selection arguments
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--master", action="store_true", help="Run in master mode")
    mode_group.add_argument("--worker", action="store_true", help="Run in worker mode")
    
    # Master mode arguments
    parser.add_argument("--users", type=int, default=LOCUST_USERS, 
                        help=f"Number of concurrent users (default: {LOCUST_USERS})")
    parser.add_argument("--spawn-rate", type=int, default=LOCUST_SPAWN_RATE, 
                        help=f"Rate to spawn users per second (default: {LOCUST_SPAWN_RATE})")
    parser.add_argument("--run-time", type=str, default=LOCUST_RUN_TIME, 
                        help=f"Stop after this amount of time (default: {LOCUST_RUN_TIME})")
    parser.add_argument("--expect-workers", type=int, default=LOCUST_EXPECT_WORKERS, 
                        help=f"Number of workers to expect (default: {LOCUST_EXPECT_WORKERS})")
    
    # Worker mode arguments
    parser.add_argument("--host", type=str, default=LOCUST_MASTER_HOST, 
                        help=f"Host for master node in worker mode (default: {LOCUST_MASTER_HOST})")
    parser.add_argument("--port", type=int, default=LOCUST_MASTER_PORT, 
                        help=f"Port for master node in worker mode (default: {LOCUST_MASTER_PORT})")
    
    # Common arguments
    parser.add_argument("--target-host", type=str, default=BASE_URL, 
                        help=f"Target host to load test (default: {BASE_URL})")
    parser.add_argument("--headless", action="store_true", 
                        help="Run in headless mode without web UI")
    
    return parser.parse_args()


def run_master(args):
    """Run Locust in master mode"""
    print(f"Starting Locust master with {args.users} users at {args.spawn_rate} users/sec")
    print(f"Target host: {args.target_host}")
    
    cmd = [
        "locust",
        "-f", "app/core/locust_load_test/custom/locustfile.py",
        "--master",
        "--host", args.target_host,
        "--expect-workers", str(args.expect_workers),
    ]
    
    if args.headless:
        cmd.extend([
            "--headless",
            "--users", str(args.users),
            "--spawn-rate", str(args.spawn_rate),
            "--run-time", args.run_time,
        ])
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)


def run_worker(args):
    """Run Locust in worker mode"""
    print(f"Starting Locust worker connecting to master at {args.host}:{args.port}")
    print(f"Target host: {args.target_host}")
    
    cmd = [
        "locust",
        "-f", "app/core/locust_load_test/custom/locustfile.py",
        "--worker",
        "--master-host", args.host,
        "--master-port", str(args.port),
        "--host", args.target_host,
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)


def main():
    args = parse_arguments()
    
    if args.master:
        run_master(args)
    else:
        run_worker(args)


if __name__ == "__main__":
    main()
