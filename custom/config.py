"""
Configuration settings for custom FastAPI Locust load tests.
Uses environment variables or default values.
"""
import os
from typing import Dict, Any

# Base URL for the FastAPI application
BASE_URL = os.getenv("BASE_URL", "https://full-stack-fastapi-template-bvfx.onrender.com")

# Authentication credentials for testing protected endpoints
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "password123")

# Locust settings - optimized for free-tier servers
LOCUST_WAIT_TIME_MIN = int(os.getenv("LOCUST_WAIT_TIME_MIN", 3))  # Increased from 1 to 3
LOCUST_WAIT_TIME_MAX = int(os.getenv("LOCUST_WAIT_TIME_MAX", 8))  # Increased from 3 to 8
LOCUST_MASTER_HOST = os.getenv("LOCUST_MASTER_HOST", "localhost")
LOCUST_MASTER_PORT = int(os.getenv("LOCUST_MASTER_PORT", 8089))
LOCUST_USERS = int(os.getenv("LOCUST_USERS", 5))  # Reduced from 20 to 5 for free-tier
LOCUST_SPAWN_RATE = int(os.getenv("LOCUST_SPAWN_RATE", 1))  # Reduced from 5 to 1 for gentler ramp-up
LOCUST_RUN_TIME = os.getenv("LOCUST_RUN_TIME", "5m")  # Increased from 1m to 5m for longer, gentler tests
LOCUST_EXPECT_WORKERS = int(os.getenv("LOCUST_EXPECT_WORKERS", 1))

# Test data for creating users and items
TEST_USER_DATA = {
    "email": "loadtest_user@example.com",
    "password": "securepassword123",
    "full_name": "Load Test User"
}

TEST_ITEM_DATA = {
    "title": "Load Test Item",
    "description": "This is an item created during load testing",
}

# Endpoints to test
ENDPOINTS = {
    "health": "/api/v1/health",
    "login": "/api/v1/login/access-token",
    "users": "/api/v1/users/",
    "items": "/api/v1/items/",
}

# Task weights - reduced frequency for free-tier servers
TASK_WEIGHTS = {
    "health_check": 5,   # Reduced from 10 - Health check less frequent
    "read_users": 2,     # Reduced from 3
    "read_items": 3,     # Reduced from 5
    "create_item": 1,    # Reduced from 2
    "update_item": 1,    # Same
    "delete_item": 1,    # Same
    "login": 3,          # Reduced from 5 - Less frequent login attempts
}
