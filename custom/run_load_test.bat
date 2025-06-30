@echo off
REM Script to run load tests for FastAPI backend
REM Usage: run_load_test.bat [single|master|worker|health]

set MODE=%1
set USERS=%2
set SPAWN_RATE=%3
set MASTER_HOST=%4

if "%USERS%"=="" set USERS=10
if "%SPAWN_RATE%"=="" set SPAWN_RATE=1
if "%MASTER_HOST%"=="" set MASTER_HOST=localhost

cd ../../..

REM Ensure Locust is installed
where locust >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Locust not found. Installing...
    uv pip install locust
)

REM Create test user if needed
echo Creating test user for load testing...
python -m app.core.locust_load_test.custom.create_test_user

if "%MODE%"=="single" (
    echo Running single-node Locust load test...
    locust -f ./locustfile.py
) else if "%MODE%"=="master" (
    echo Running Locust master node with %USERS% users at %SPAWN_RATE% users/sec...
    python -m custom_run_distributed_locust --master --users=%USERS% --spawn-rate=%SPAWN_RATE%
) else if "%MODE%"=="worker" (
    echo Running Locust worker node connecting to %MASTER_HOST%...
    python -m custom_run_distributed_locust --worker --host=%MASTER_HOST%
) else if "%MODE%"=="health" (
    echo Checking Locust health...
    python -m custom_health_check --json
) else (
    echo Usage: run_load_test.bat [single^|master^|worker^|health] [users] [spawn_rate] [master_host]
    echo   single: Run single-node Locust test
    echo   master: Run Locust master node
    echo   worker: Run Locust worker node
    echo   health: Check Locust health
    exit /b 1
)
