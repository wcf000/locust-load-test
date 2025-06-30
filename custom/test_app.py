"""
Load testing entry point for the FastAPI application.
This module creates a modified version of the main app with database operations mocked
to allow testing API performance without a real database connection.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

# Set environment variable to indicate load testing mode
os.environ["LOAD_TESTING"] = "true"
os.environ["ALLOW_NO_DB"] = "true"  # Allow running without a database connection

# Import the main app
from app.main import app
from app.core.locust_load_test.custom.mock_db import enable_load_testing_mode

# Enable load testing mode by overriding dependencies
load_test_app = enable_load_testing_mode(app)

# Override startup event to skip database initialization
@load_test_app.on_event("startup")
async def override_startup_database():
    print("🧪 Database initialization skipped in load testing mode")

# This app can be run with:
# uvicorn app.core.locust_load_test.custom.test_app:load_test_app --host 0.0.0.0 --port 8000
