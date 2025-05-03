"""
Basic Locust Performance Test Example (No Grafana)

This script defines a simple Locust user that hits a health check and a sample API endpoint.
Edit the endpoints and authentication as needed for your backend.

How to run:
    locust -f app/core/locust/_tests/locust_performance.py

Environment variables:
    BASE_URL: The base URL for your backend (default: http://localhost:8000)
"""

import logging
import os
from typing import Any

from locust import HttpUser, between, events, task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
WAIT_TIME_MIN = int(os.getenv("LOCUST_WAIT_TIME_MIN", "1"))
WAIT_TIME_MAX = int(os.getenv("LOCUST_WAIT_TIME_MAX", "3"))

class BasicUser(HttpUser):
    """
    Simulates a basic user hitting health and sample endpoints.
    """
    host = BASE_URL
    wait_time = between(WAIT_TIME_MIN, WAIT_TIME_MAX)

    @task(2)
    def health_check(self) -> None:
        """Check the /health endpoint."""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                logger.info("Health check success.")
            else:
                response.failure(f"Health check failed: {response.status_code} {response.text}")
                logger.error(f"Health check failed: {response.status_code} {response.text}")

    @task(1)
    def sample_api(self) -> None:
        """Call a sample API endpoint (edit as needed)."""
        with self.client.get("/api/sample", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                logger.info("Sample API success.")
            else:
                response.failure(f"Sample API failed: {response.status_code} {response.text}")
                logger.error(f"Sample API failed: {response.status_code} {response.text}")

# Optional: Add Locust event hooks for test lifecycle logging
def on_locust_init(environment: Any, **kwargs: Any) -> None:
    logger.info("Locust environment initialized.")
def on_test_start(environment: Any, **kwargs: Any) -> None:
    logger.info("Locust test started.")
def on_test_stop(environment: Any, **kwargs: Any) -> None:
    logger.info("Locust test stopped.")

events.init.add_listener(on_locust_init)
events.test_start.add_listener(on_test_start)
events.test_stop.add_listener(on_test_stop)
