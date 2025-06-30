#!/bin/bash
# Script to run load tests with mocked database for FastAPI
# This script starts both the test server and Locust in a controlled way

echo "FastAPI Load Testing with Mock Database"
echo "--------------------------------------"

# Check if Python and Poetry are available
if ! command -v python &> /dev/null; then
    echo "Python not found! Please install Python and try again."
    exit 1
fi

if ! command -v poetry &> /dev/null; then
    echo "Poetry not found! Please install Poetry and try again."
    exit 1
fi

# Step 1: Start the FastAPI test server with mocked database
echo
echo "Starting FastAPI test server with mocked database..."
echo

# Start the server in the background
export LOAD_TESTING=true
export ALLOW_NO_DB=true
poetry run uvicorn app.core.locust_load_test.custom.test_app:load_test_app --port 8000 &
SERVER_PID=$!

# Wait for the server to start
echo "Waiting for server to start..."
sleep 5

# Step 2: Create test user (this is just informational in mock mode)
echo
echo "Setting up test user..."
poetry run python app/core/locust_load_test/custom/create_test_user.py

# Step 3: Start Locust
echo
echo "Starting Locust..."
echo

# Run Locust
poetry run locust -f app/core/locust_load_test/custom/locustfile.py --host=http://localhost:8000

# Clean up - stop the server when Locust is done
echo
echo "Load testing complete! Shutting down test server..."
kill $SERVER_PID

echo
echo "All done!"

exit 0
