#!/bin/bash

# Script to run load tests for FastAPI backend
# Usage: ./run_load_test.sh [single|master|worker|health]

MODE=$1
USERS=${2:-10}
SPAWN_RATE=${3:-1}
MASTER_HOST=${4:-localhost}

cd ../../..  # Navigate to backend root directory

# Ensure Locust is installed
if ! command -v locust &> /dev/null; then
    echo "Locust not found. Installing..."
    uv pip install locust
fi

# Create test user if needed
echo "Creating test user for load testing..."
python -m app.core.locust_load_test.custom.create_test_user

case $MODE in
    single)
        echo "Running single-node Locust load test..."
        locust -f app/core/locust_load_test/custom/locustfile.py
        ;;
    master)
        echo "Running Locust master node with $USERS users at $SPAWN_RATE users/sec..."
        python -m app.core.locust_load_test.custom.custom_run_distributed_locust --master --users=$USERS --spawn-rate=$SPAWN_RATE
        ;;
    worker)
        echo "Running Locust worker node connecting to $MASTER_HOST..."
        python -m app.core.locust_load_test.custom.custom_run_distributed_locust --worker --host=$MASTER_HOST
        ;;
    health)
        echo "Checking Locust health..."
        python -m app.core.locust_load_test.custom.custom_health_check --json
        ;;
    *)
        echo "Usage: ./run_load_test.sh [single|master|worker|health] [users] [spawn_rate] [master_host]"
        echo "  single: Run single-node Locust test"
        echo "  master: Run Locust master node"
        echo "  worker: Run Locust worker node"
        echo "  health: Check Locust health"
        exit 1
        ;;
esac
