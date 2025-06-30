# FastAPI Load Testing with Locust

This directory contains custom load testing scripts for the FastAPI backend using Locust.

## Files

- `config.py`: Configuration settings for the load tests
- `locustfile.py`: Main Locust test definition with user behavior
- `custom_run_distributed_locust.py`: Script to run tests in distributed mode
- `custom_health_check.py`: Script to check the health of Locust nodes
- `create_test_user.py`: Script to create a test user for load testing

## Setup

1. First, install Locust:
   ```bash
   uv pip install locust
   ```

2. Create a test user (required for authenticated endpoints):
   ```bash
   python -m app.core.locust_load_test.custom.create_test_user
   ```

3. Optionally, customize configuration in `config.py` or set environment variables.

## Running the Tests

### Single Node (Local)

```bash
locust -f app/core/locust_load_test/custom/locustfile.py
```
Then open http://localhost:8089 in your browser to start and monitor the test.

### Distributed Mode

**Master Node:**
```bash
python -m app.core.locust_load_test.custom.custom_run_distributed_locust --master --users=100 --spawn-rate=10 --expect-workers=2
```

**Worker Node(s):** (run on separate machines or terminals)
```bash
python -m app.core.locust_load_test.custom.custom_run_distributed_locust --worker --host=<MASTER_HOST> --port=8089
```

## Checking Health

```bash
python -m app.core.locust_load_test.custom.custom_health_check --json
```

## Customizing Tests

To modify the tests:

1. Edit `config.py` to adjust settings like endpoints, wait times, and task weights
2. Edit `locustfile.py` to change user behavior or add new endpoints
3. Add or modify tasks in the `FastAPIUser` class for different API endpoints

## Integration with Monitoring

The FastAPI app already has Prometheus metrics. You can visualize test results alongside system metrics in Grafana:

1. Make sure Prometheus is scraping the `/api/v1/metrics` endpoint
2. Set up Grafana dashboards to show both system metrics and load test results
3. Run the load test while monitoring the dashboards to understand system behavior under load
