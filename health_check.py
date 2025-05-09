"""
Locust Health Check Module
Provides health monitoring for distributed Locust test environments
"""

import logging
import os
from datetime import datetime, timedelta
from typing , Optional

import requests

logger = logging.getLogger(__name__)


class LocustHealthChecker:
    def __init__(self):
        self.master_host = os.getenv("LOCUST_MASTER_HOST", "localhost")
        self.master_port = int(os.getenv("LOCUST_MASTER_PORT", "8089"))
        self.master_url = f"http://{self.master_host}:{self.master_port}"
        self.timeout = float(os.getenv("LOCUST_HEALTH_TIMEOUT", "5.0"))
        self.expected_workers = int(os.getenv("EXPECTED_WORKERS", "1"))
        self.last_check = datetime.min

    def _make_request(self, endpoint: str) -> dict | None:
        """Helper method for API requests"""
        try:
            response = requests.get(
                f"{self.master_url}{endpoint}",
                timeout=self.timeout,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.warning(f"Health check request failed: {str(e)}")
            return None

    def check_master_health(self) -> dict[str, bool]:
        """Check if master node is responsive"""
        now = datetime.now()
        if now - self.last_check < timedelta(seconds=1):
            return {"healthy": True, "cached": True}

        stats = self._make_request("/stats/requests")
        healthy = stats is not None
        self.last_check = now

        return {
            "healthy": healthy,
            "cached": False,
            "details": {
                "endpoint": f"{self.master_url}/stats/requests",
                "response_time": (now - self.last_check).total_seconds(),
            },
        }

    def check_worker_health(self) -> dict[str, int]:
        """Check worker connectivity"""
        stats = self._make_request("/stats/requests")
        if not stats:
            return {"connected": 0, "expected": self.expected_workers}

        workers = stats.get("workers", [])
        return {
            "connected": len(workers),
            "expected": self.expected_workers,
            "worker_ids": [w["id"] for w in workers],
        }

    def full_health_check(self) -> dict[str, dict]:
        """Comprehensive health status report"""
        return {
            "master": self.check_master_health(),
            "workers": self.check_worker_health(),
            "environment": {
                "host": self.master_host,
                "port": self.master_port,
                "timeout": self.timeout,
            },
        }


def health_check() -> bool:
    """Standard health check endpoint for containers"""
    checker = LocustHealthChecker()
    return (
        checker.check_master_health()["healthy"]
        and checker.check_worker_health()["connected"] >= 1
    )


# CLI support
if __name__ == "__main__":
    import json

    checker = LocustHealthChecker()
    print(json.dumps(checker.full_health_check(), indent=2))
