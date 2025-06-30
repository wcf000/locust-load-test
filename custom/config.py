"""
Configuration settings for custom FastAPI Locust load tests.
Uses environment variables or default values.
"""
import os
from typing import Dict, Any

# Base URL for the FastAPI application
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Authentication credentials for testing protected endpoints
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "password123")

# Locust settings
LOCUST_WAIT_TIME_MIN = int(os.getenv("LOCUST_WAIT_TIME_MIN", 1))
LOCUST_WAIT_TIME_MAX = int(os.getenv("LOCUST_WAIT_TIME_MAX", 3))
LOCUST_MASTER_HOST = os.getenv("LOCUST_MASTER_HOST", "localhost")
LOCUST_MASTER_PORT = int(os.getenv("LOCUST_MASTER_PORT", 8089))
LOCUST_USERS = int(os.getenv("LOCUST_USERS", 20))  # increased default to 20 users for ramp-up tests
LOCUST_SPAWN_RATE = int(os.getenv("LOCUST_SPAWN_RATE", 5))  # increased default spawn rate
LOCUST_RUN_TIME = os.getenv("LOCUST_RUN_TIME", "1m")
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

# Task weights - higher numbers mean the task will be executed more frequently
TASK_WEIGHTS = {
    "health_check": 10,   # Health check is most frequent
    "read_users": 3,
    "read_items": 5,
    "create_item": 2,
    "update_item": 1,
    "delete_item": 1,
    "login": 5,  # weight for login tasks
}
