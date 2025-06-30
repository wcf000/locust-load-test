"""
Script to create a test user for load testing and verify key endpoints.

This script creates a user with the credentials specified in the config
to be used for load testing. It also verifies the availability of essential 
endpoints that will be tested during load testing.

Run this before starting load tests if you're testing endpoints that require authentication.
"""

import os
import sys
import requests
import json
from pathlib import Path

# Add the parent directory to sys.path to allow importing config
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from app.core.locust_load_test.custom.config import (
    BASE_URL,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    TEST_USER_DATA,
    ENDPOINTS,
)


def verify_endpoint_availability(
    endpoint_path,
    method="GET",
    auth_token=None,
    json_data=None,
    data=None,
    extra_headers=None,
):
    """
    Verify that an endpoint is available and responding
    
    Args:
        endpoint_path: The path to the endpoint
        method: HTTP method (GET, POST, PUT, DELETE)
        auth_token: Optional auth token for protected endpoints
        json_data: Optional JSON data for POST/PUT requests
        
    Returns:
        tuple: (success: bool, response_code: int, message: str)
    """
    url = f"{BASE_URL}{endpoint_path}"
    headers = {"Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            if data is not None:
                response = requests.post(url, headers=headers, data=data)
            else:
                response = requests.post(url, headers=headers, json=json_data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=json_data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return False, 0, f"Unsupported method: {method}"
        
        return (
            response.status_code < 500,  # Consider 4xx as "available" for testing
            response.status_code,
            f"{method} {url}: {response.status_code}"
        )
    except Exception as e:
        return False, 0, f"Error checking {method} {url}: {e}"


def get_auth_token(force_refresh=False):
    """
    Get authentication token for the test user
    
    Args:
        force_refresh: Force a new login even if token is cached
    
    Returns:
        str or None: Authentication token if successful, None otherwise
    """
    # Use a simple in-memory cache to avoid multiple logins in the same session
    if hasattr(get_auth_token, 'cached_token') and not force_refresh:
        return get_auth_token.cached_token
        
    login_url = f"{BASE_URL}/api/v1/login/access-token"
    
    login_data = {
        "username": TEST_USER_EMAIL,  # FastAPI OAuth expects 'username'
        "password": TEST_USER_PASSWORD,
    }
    
    try:
        response = requests.post(
            login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            get_auth_token.cached_token = token
            # Verify token has the right permissions by checking user info
            me_url = f"{BASE_URL}/api/v1/users/me"
            me_response = requests.get(
                me_url,
                headers={"Authorization": f"Bearer {token}"}
            )
            if me_response.status_code == 200:
                user_info = me_response.json()
                if not user_info.get('is_superuser', False):
                    print("⚠️ WARNING: User does not have superuser privileges in the token! If you just updated privileges, log out and log in again.")
            return token
        else:
            print(f"Failed to get auth token. Status code: {response.status_code}")
            try:
                print(f"Response: {response.json()}")
            except:
                print(f"Response text: {response.text}")
            return None
    except Exception as e:
        print(f"Error getting auth token: {e}")
        return None


def create_test_user():
    """
    Create a test user for load testing if it doesn't already exist
    and verify that key endpoints are available
    """
    # Check if we're in load testing mode
    if os.getenv("LOAD_TESTING", "").lower() == "true":
        print("Running in load testing mode with mock database")
        print(f"Using pre-configured test user: {TEST_USER_EMAIL}")
        print("Password: (mock password - authentication will be bypassed)")
        return True
    
    # Use the signup endpoint to create a real user
    register_url = f"{BASE_URL}/api/v1/users/signup"
    
    user_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "full_name": "Load Test User",
    }
    
    print(f"Creating test user at {register_url}")
    
    try:
        # First check server health
        health_url = f"{BASE_URL}/api/v1/health"
        try:
            health_response = requests.get(health_url)
            if health_response.status_code == 200:
                print("Server is healthy")
            else:
                print(f"Health check failed: {health_response.text}")
        except Exception as e:
            print(f"Error checking server health: {e}")
            print("Make sure your server is running on the correct URL")
            print(f"Current BASE_URL: {BASE_URL}")
            return False
        
        # Try to create the user
        response = requests.post(
            register_url,
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        user_created = False
        if response.status_code in (200, 201):
            print(f"Successfully created test user: {TEST_USER_EMAIL}")
            user_created = True
        elif response.status_code == 400 and "already exists" in response.text:
            print(f"User {TEST_USER_EMAIL} already exists. This is fine for testing.")
            user_created = True
        else:
            print(f"Failed to create test user. Status code: {response.status_code}")
            try:
                json_response = response.json()
                print(f"Response JSON: {json.dumps(json_response, indent=2)}")
            except:
                print(f"Response text: {response.text}")
            print("\nAlternative approach: Run server in load testing mode")
            print("Start the server with the load testing app:")
            print("poetry run uvicorn app.core.locust_load_test.custom.test_app:load_test_app --port 8000")
            print("This will use a mock database with pre-configured test users")
            return False
        
        # If user creation was successful, verify key endpoints
        if user_created:
            print("\n--- Verifying key endpoints for load testing ---")
            # Get auth token for protected endpoints
            auth_token = get_auth_token()
            if auth_token:
                print(f"✅ Authentication successful (token: {auth_token[:10]}...)")
            else:
                print("⚠️ Failed to authenticate, continuing with endpoint verification")
            # Verify health endpoint
            success, code, message = verify_endpoint_availability("/api/v1/health")
            print(f"{'✅' if success else '❌'} Health endpoint: {message}")
            # Verify login endpoint (already tested via get_auth_token, but check again)
            success, code, message = verify_endpoint_availability(
                "/api/v1/login/access-token",
                method="POST",
                data={
                    "grant_type": "password",
                    "username": TEST_USER_EMAIL,
                    "password": TEST_USER_PASSWORD,
                },
                extra_headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            print(f"{'✅' if success else '❌'} Login endpoint: {message}")
            # Check if user is superuser by making a call to /users/me
            is_superuser = False
            superuser_check_url = f"{BASE_URL}/api/v1/users/me"
            try:
                superuser_response = requests.get(
                    superuser_check_url,
                    headers={"Authorization": f"Bearer {auth_token}"}
                )
                if superuser_response.status_code == 200:
                    user_data = superuser_response.json()
                    is_superuser = user_data.get("is_superuser", False)
                    print(f"✅ User superuser status: {is_superuser}")
                    if not is_superuser:
                        print("\n⚠️ WARNING: The user does not have superuser privileges in the database.")
                        print("If you've recently granted superuser access in Supabase, you need to:")
                        print("1. Logout from the application")
                        print("2. Login again to get a new JWT token with updated privileges")
                        print("3. Run this script again to verify endpoints with the new token")
                else:
                    print(f"❌ Failed to check superuser status: {superuser_response.status_code}")
            except Exception as e:
                print(f"❌ Error checking superuser status: {e}")
            # Verify users endpoints
            success, code, message = verify_endpoint_availability(
                "/api/v1/users/me", 
                auth_token=auth_token
            )
            print(f"{'✅' if success else '❌'} Current user endpoint: {message}")
            # The /users/ endpoint requires superuser privileges
            success, code, message = verify_endpoint_availability("/api/v1/users/", auth_token=auth_token)
            print(f"{'✅' if success else '❌'} Users list endpoint: {message}")
            if code == 401 or code == 403:
                print("   ⚠️ This endpoint requires superuser privileges - check if your JWT token is up-to-date")
            # Verify items endpoints
            success, code, message = verify_endpoint_availability("/api/v1/items/", auth_token=auth_token)
            print(f"{'✅' if success else '❌'} Items list endpoint: {message}")
            if code == 401 and auth_token:
                print("   ⚠️ Authentication token might not have the required permissions")
            # Try to create an item
            # Try to create a test item and capture its ID
            test_item = {
                "title": "Test Item for Load Testing",
                "description": "This is a test item created to verify the items endpoint"
            }
            item_url = f"{BASE_URL}/api/v1/items/"
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"}
            resp = requests.post(item_url, json=test_item, headers=headers)
            if resp.ok:
                created = resp.json()
                item_id = created.get("id")
                print(f"✅ Created test item with id: {item_id}")
            else:
                print(f"❌ Create item failed: {resp.status_code} {resp.text}")
                return False
            # Verify read items endpoint
            success, code, message = verify_endpoint_availability(
                "/api/v1/items/", auth_token=auth_token
            )
            print(f"{'✅' if success else '❌'} Read items endpoint: {message}")
            # Perform update and delete tests if items available
            # Update the created item
            try:
                update_data = {
                    "title": test_item["title"] + " Updated",
                    "description": test_item["description"] + " Updated"
                }
                success, code, message = verify_endpoint_availability(
                    f"/api/v1/items/{item_id}",
                    method="PUT", auth_token=auth_token, json_data=update_data
                )
                print(f"{'✅' if success else '❌'} Update item endpoint: {message}")
                # Delete the created item
                success, code, message = verify_endpoint_availability(
                    f"/api/v1/items/{item_id}", method="DELETE", auth_token=auth_token
                )
                print(f"{'✅' if success else '❌'} Delete item endpoint: {message}")
            except Exception as e:
                print(f"Error during update/delete tests for item {item_id}: {e}")
            print("\nEndpoint verification complete. If any endpoints failed, address the issues before running load tests.")
            return True
    except requests.RequestException as e:
        print(f"Error creating test user: {e}")
        return False


if __name__ == "__main__":
    create_test_user()
