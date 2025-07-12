"""
Load test for Model Context Protocol (MCP) Server
Tests MCP-specific endpoints and tools to ensure performance under load.
"""

import json
import random
import time
from typing import Dict, Any

from locust import HttpUser, task, between, events
from locust.env import Environment
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServerUser(HttpUser):
    """
    Load test user for MCP server endpoints.
    Simulates LLM/AI agent interactions with the MCP server.
    """
    
    # Wait time between requests (simulating think time)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts. Setup any required state."""
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "MCP-LoadTest/1.0",
            "Accept": "application/json"
        }
        
        # Test connection to MCP server
        try:
            response = self.client.get("/api/v1/health", headers=self.headers)
            if response.status_code == 200:
                logger.info("MCP Server health check passed")
            else:
                logger.warning(f"MCP Server health check failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")

    @task(3)
    def test_mcp_status(self):
        """Test MCP status endpoint (frequent check)."""
        with self.client.get(
            "/api/v1/mcp/status", 
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "status" in data:
                        response.success()
                    else:
                        response.failure("Missing status in response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status endpoint failed: {response.status_code}")

    @task(2)
    def test_mcp_health(self):
        """Test MCP health endpoint."""
        with self.client.get(
            "/api/v1/mcp/health", 
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health endpoint failed: {response.status_code}")

    @task(2)
    def test_mcp_discovery(self):
        """Test MCP discovery endpoint for available tools and resources."""
        with self.client.get(
            "/api/v1/mcp/discovery", 
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Check if discovery data contains expected fields
                    if isinstance(data, dict) and ("tools" in data or "resources" in data):
                        response.success()
                    else:
                        response.failure("Invalid discovery response format")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON in discovery response")
            else:
                response.failure(f"Discovery endpoint failed: {response.status_code}")

    @task(1)
    def test_mcp_tool_add(self):
        """Test the MCP 'add' tool (demo tool)."""
        # Generate random numbers for the add operation
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        
        payload = {
            "name": "add",
            "arguments": {
                "a": a,
                "b": b
            }
        }
        
        with self.client.post(
            "/api/v1/tools/call",
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Verify the add operation result
                    expected_sum = a + b
                    if isinstance(data, list) and len(data) > 0:
                        result_data = data[0]
                        if "info" in result_data and result_data["info"].get("sum") == expected_sum:
                            response.success()
                        else:
                            response.failure(f"Incorrect sum: expected {expected_sum}")
                    else:
                        response.failure("Invalid tool response format")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON in tool response")
            else:
                response.failure(f"Add tool failed: {response.status_code}")

    @task(1)
    def test_mcp_resource_version(self):
        """Test MCP resource endpoint (app version)."""
        with self.client.get(
            "/api/v1/resources/config://app-version",
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, str) and data:
                        response.success()
                    else:
                        response.failure("Invalid version resource response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON in resource response")
            else:
                response.failure(f"Version resource failed: {response.status_code}")

    @task(1)
    def test_allowed_endpoints(self):
        """Test that only safe endpoints are accessible (security test)."""
        # Test some endpoints that should be accessible
        safe_endpoints = [
            "/api/v1/items",  # Read-only items (if not blocked)
            "/api/v1/health",
            "/api/v1/notes",  # Read-only notes (if not blocked)
        ]
        
        for endpoint in safe_endpoints:
            with self.client.get(
                endpoint,
                headers=self.headers,
                catch_response=True
            ) as response:
                # We expect either 200 (accessible) or 404 (blocked/not found)
                # Both are acceptable - we just don't want 500 errors
                if response.status_code in [200, 404, 401]:
                    response.success()
                else:
                    response.failure(f"Unexpected status {response.status_code} for {endpoint}")

    @task(1)
    def test_blocked_endpoints_security(self):
        """Test that sensitive endpoints are properly blocked."""
        # Test endpoints that should be blocked
        blocked_endpoints = [
            "/api/v1/login/access-token",
            "/api/v1/users/signup",
            "/api/v1/users/me",
            "/api/v1/debug/clear-rate-limits",
            "/api/v1/admin/users",
        ]
        
        for endpoint in blocked_endpoints:
            with self.client.get(
                endpoint,
                headers=self.headers,
                catch_response=True
            ) as response:
                # Blocked endpoints should return 404 (not found) or 403 (forbidden)
                if response.status_code in [404, 403]:
                    response.success()
                elif response.status_code == 401:
                    # 401 is also acceptable - means endpoint exists but requires auth
                    response.success()
                else:
                    response.failure(f"Sensitive endpoint {endpoint} not properly blocked: {response.status_code}")


@events.test_start.add_listener
def on_test_start(environment: Environment, **kwargs):
    """Called when test starts."""
    logger.info("Starting MCP Server load test...")
    logger.info(f"Target host: {environment.host}")


@events.test_stop.add_listener  
def on_test_stop(environment: Environment, **kwargs):
    """Called when test stops."""
    logger.info("MCP Server load test completed.")
    
    # Print summary statistics
    stats = environment.stats
    logger.info(f"Total requests: {stats.total.num_requests}")
    logger.info(f"Total failures: {stats.total.num_failures}")
    logger.info(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    logger.info(f"Max response time: {stats.total.max_response_time:.2f}ms")


# Configuration for different test scenarios
class MCPLightLoad(MCPServerUser):
    """Light load test - simulates normal usage."""
    wait_time = between(2, 5)
    weight = 3


class MCPHeavyLoad(MCPServerUser):
    """Heavy load test - simulates high usage."""
    wait_time = between(0.5, 1.5)  
    weight = 1


if __name__ == "__main__":
    """
    Run the load test directly.
    Usage: poetry run python -m locust -f mcp_server_load_test.py --host=https://your-server.com
    """
    print("MCP Server Load Test")
    print("To run: poetry run python -m locust -f mcp_server_load_test.py --host=https://full-stack-fastapi-template-bvfx.onrender.com")
    print("Or use the web UI: poetry run locust -f mcp_server_load_test.py --host=https://full-stack-fastapi-template-bvfx.onrender.com")
