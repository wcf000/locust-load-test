@echo off
REM Script to run load tests with mocked database for FastAPI
REM This script starts both the test server and Locust in a controlled way

echo "FastAPI Load Testing with Mock Database"
echo "--------------------------------------"

REM Check if Python and Poetry are available
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found! Please install Python and try again.
    exit /b 1
)

where poetry >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Poetry not found! Please install Poetry and try again.
    exit /b 1
)

REM Step 1: Start the FastAPI test server with mocked database
echo.
echo Starting FastAPI test server with mocked database...
echo.

REM Start the server in a new Command Prompt window
start cmd /k "title FastAPI Test Server && set LOAD_TESTING=true && set ALLOW_NO_DB=true && poetry run uvicorn app.core.locust_load_test.custom.test_app:load_test_app --port 8000"

REM Wait for the server to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Step 2: Create test user (this is just informational in mock mode)
echo.
echo Setting up test user...
poetry run python app/core/locust_load_test/custom/create_test_user.py

REM Step 3: Start Locust
echo.
echo Starting Locust...
echo.

REM Run Locust in the current window
set LOAD_TESTING=true
poetry run locust -f app/core/locust_load_test/custom/locustfile.py --host=http://localhost:8000

echo.
echo Load testing complete!
echo.
echo Note: The FastAPI test server is still running in a separate window.
echo You can close it when you're done testing.

exit /b 0
