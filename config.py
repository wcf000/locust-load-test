import os
from app.core.config import Settings

class LocustConfig:
    """Configuration settings for Locust load testing."""

    def __init__(self):
        # Distributed/master settings
        self.master_host = Settings.LOCUST_MASTER_HOST if hasattr(Settings, 'LOCUST_MASTER_HOST') else os.getenv("LOCUST_MASTER_HOST", "localhost")
        self.master_port = Settings.LOCUST_MASTER_PORT if hasattr(Settings, 'LOCUST_MASTER_PORT') else int(os.getenv("LOCUST_MASTER_PORT", "8089"))
        self.master_url = f"http://{self.master_host}:{self.master_port}"
        self.timeout = 5.0
        self.expected_workers = 1

        # Load test configuration
        self.wait_time_min = 1
        self.wait_time_max = 3
        self.users = 100
        self.spawn_rate = 10.0

    @property
    def base_url(self):
        """Base URL for the API under test."""
        return os.getenv("BASE_URL", "http://localhost:8000")

# Use Prometheus settings directly from Settings wherever needed:
# Settings.PROMETHEUS_ENABLED
# Settings.PROMETHEUS_PORT
# Settings.PROMETHEUS_SERVICE_URL
