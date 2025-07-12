#!/bin/bash

# MCP Server Load Test Runner
# This script runs load tests against the MCP server

set -e

echo "🚀 MCP Server Load Test Runner"
echo "================================"

# Default values
HOST="https://full-stack-fastapi-template-bvfx.onrender.com"
USERS=10
SPAWN_RATE=2
TIME="60s"
MODE="web"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST="$2"
            shift 2
            ;;
        --users)
            USERS="$2"
            shift 2
            ;;
        --spawn-rate)
            SPAWN_RATE="$2"
            shift 2
            ;;
        --time)
            TIME="$2"
            shift 2
            ;;
        --headless)
            MODE="headless"
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --host URL          Target server URL (default: $HOST)"
            echo "  --users N           Number of concurrent users (default: $USERS)"
            echo "  --spawn-rate N      User spawn rate per second (default: $SPAWN_RATE)"
            echo "  --time DURATION     Test duration (default: $TIME)"
            echo "  --headless          Run without web UI"
            echo "  --help              Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Configuration:"
echo "  Host: $HOST"
echo "  Users: $USERS"
echo "  Spawn Rate: $SPAWN_RATE"
echo "  Duration: $TIME"
echo "  Mode: $MODE"
echo ""

# Check if locust is installed
if ! poetry run python -c "import locust" 2>/dev/null; then
    echo "❌ Locust not found. Installing..."
    poetry add locust
    echo "✅ Locust installed successfully"
fi

# Navigate to the load test directory
cd "$(dirname "$0")"

echo "🏃 Starting load test..."

if [ "$MODE" = "headless" ]; then
    # Run headless mode
    poetry run locust \
        -f mcp_server_load_test.py \
        --host="$HOST" \
        --users="$USERS" \
        --spawn-rate="$SPAWN_RATE" \
        --run-time="$TIME" \
        --headless \
        --csv=mcp_test_results
    
    echo ""
    echo "📊 Test Results:"
    if [ -f "mcp_test_results_stats.csv" ]; then
        echo "Stats saved to: mcp_test_results_stats.csv"
    fi
    if [ -f "mcp_test_results_failures.csv" ]; then
        echo "Failures saved to: mcp_test_results_failures.csv"
    fi
else
    # Run with web UI
    echo "🌐 Starting Locust web interface..."
    echo "   Open your browser to: http://localhost:8089"
    echo "   Use these settings:"
    echo "     - Number of users: $USERS"
    echo "     - Spawn rate: $SPAWN_RATE"
    echo "     - Host: $HOST"
    echo ""
    echo "Press Ctrl+C to stop the test"
    
    poetry run locust \
        -f mcp_server_load_test.py \
        --host="$HOST"
fi

echo ""
echo "🎉 Load test completed!"
