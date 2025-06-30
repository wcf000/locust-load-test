"""
Script to monitor health of Locust master and worker nodes.

This script checks if the Locust master is running and responsive
and verifies that the expected number of workers are connected.

Usage:
    python custom_health_check.py --host=localhost --port=8089
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

# Add the parent directory to sys.path to allow importing config
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from app.core.locust_load_test.custom.config import (
    LOCUST_MASTER_HOST,
    LOCUST_MASTER_PORT,
    LOCUST_EXPECT_WORKERS,
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Check health of Locust master and worker nodes")
    
    parser.add_argument("--host", type=str, default=LOCUST_MASTER_HOST, 
                        help=f"Locust master host (default: {LOCUST_MASTER_HOST})")
    parser.add_argument("--port", type=int, default=LOCUST_MASTER_PORT, 
                        help=f"Locust master port (default: {LOCUST_MASTER_PORT})")
    parser.add_argument("--expect-workers", type=int, default=LOCUST_EXPECT_WORKERS, 
                        help=f"Expected number of worker nodes (default: {LOCUST_EXPECT_WORKERS})")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    return parser.parse_args()


def check_master_health(host, port):
    """
    Check if the Locust master is running and responsive
    """
    url = f"http://{host}:{port}/stats/requests"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Master returned status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Error connecting to master: {e}"


def check_workers_health(host, port, expected_workers):
    """
    Check if the expected number of workers are connected
    """
    url = f"http://{host}:{port}/workers"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            workers = data.get("workers", [])
            worker_count = len(workers)
            
            if worker_count >= expected_workers:
                return True, {"count": worker_count, "workers": workers}
            else:
                return False, {
                    "count": worker_count, 
                    "expected": expected_workers,
                    "workers": workers
                }
        else:
            return False, f"Workers check returned status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Error checking workers: {e}"


def main():
    args = parse_arguments()
    
    health_data = {
        "master": {
            "healthy": False,
            "details": None,
        },
        "workers": {
            "healthy": False,
            "details": None,
        },
        "overall": False,
    }
    
    # Check master health
    master_healthy, master_details = check_master_health(args.host, args.port)
    health_data["master"]["healthy"] = master_healthy
    health_data["master"]["details"] = master_details
    
    # Check workers health
    if master_healthy:
        workers_healthy, workers_details = check_workers_health(args.host, args.port, args.expect_workers)
        health_data["workers"]["healthy"] = workers_healthy
        health_data["workers"]["details"] = workers_details
    
    # Determine overall health
    health_data["overall"] = master_healthy and health_data["workers"]["healthy"]
    
    # Output results
    if args.json:
        print(json.dumps(health_data, indent=2))
    else:
        print(f"Locust Master: {'✅ Healthy' if health_data['master']['healthy'] else '❌ Unhealthy'}")
        if master_healthy:
            print(f"Locust Workers: {'✅ Healthy' if health_data['workers']['healthy'] else '❌ Unhealthy'}")
            worker_details = health_data["workers"]["details"]
            if isinstance(worker_details, dict) and "count" in worker_details:
                print(f"  Connected workers: {worker_details['count']}/{args.expect_workers}")
        
        print(f"Overall Health: {'✅ Healthy' if health_data['overall'] else '❌ Unhealthy'}")
    
    # Return exit code based on health
    return 0 if health_data["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
