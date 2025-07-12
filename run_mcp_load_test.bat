@echo off
REM MCP Server Load Test Runner for Windows
REM This script runs load tests against the MCP server

echo 🚀 MCP Server Load Test Runner
echo ================================

REM Default values
set HOST=https://full-stack-fastapi-template-bvfx.onrender.com
set USERS=10
set SPAWN_RATE=2
set TIME=60s
set MODE=web

REM Parse command line arguments
:parse_args
if "%1"=="--host" (
    set HOST=%2
    shift
    shift
    goto parse_args
)
if "%1"=="--users" (
    set USERS=%2
    shift
    shift
    goto parse_args
)
if "%1"=="--spawn-rate" (
    set SPAWN_RATE=%2
    shift
    shift
    goto parse_args
)
if "%1"=="--time" (
    set TIME=%2
    shift
    shift
    goto parse_args
)
if "%1"=="--headless" (
    set MODE=headless
    shift
    goto parse_args
)
if "%1"=="--help" (
    echo Usage: %0 [options]
    echo Options:
    echo   --host URL          Target server URL
    echo   --users N           Number of concurrent users
    echo   --spawn-rate N      User spawn rate per second
    echo   --time DURATION     Test duration
    echo   --headless          Run without web UI
    echo   --help              Show this help
    exit /b 0
)
if "%1"=="" goto start_test
shift
goto parse_args

:start_test
echo Configuration:
echo   Host: %HOST%
echo   Users: %USERS%
echo   Spawn Rate: %SPAWN_RATE%
echo   Duration: %TIME%
echo   Mode: %MODE%
echo.

REM Check if locust is installed
poetry run python -c "import locust" >nul 2>&1
if errorlevel 1 (
    echo ❌ Locust not found. Installing...
    poetry add locust
    echo ✅ Locust installed successfully
)

REM Navigate to the load test directory
cd /d "%~dp0"

echo 🏃 Starting load test...

if "%MODE%"=="headless" (
    REM Run headless mode
    poetry run locust -f mcp_server_load_test.py --host="%HOST%" --users=%USERS% --spawn-rate=%SPAWN_RATE% --run-time=%TIME% --headless --csv=mcp_test_results
    
    echo.
    echo 📊 Test Results:
    if exist "mcp_test_results_stats.csv" (
        echo Stats saved to: mcp_test_results_stats.csv
    )
    if exist "mcp_test_results_failures.csv" (
        echo Failures saved to: mcp_test_results_failures.csv
    )
) else (
    REM Run with web UI
    echo 🌐 Starting Locust web interface...
    echo    Open your browser to: http://localhost:8089
    echo    Use these settings:
    echo      - Number of users: %USERS%
    echo      - Spawn rate: %SPAWN_RATE%
    echo      - Host: %HOST%
    echo.
    echo Press Ctrl+C to stop the test
    
    poetry run locust -f mcp_server_load_test.py --host="%HOST%"
)

echo.
echo 🎉 Load test completed!
pause
