# FastAPI Backend Load Testing

This guide explains how to use the custom load testing suite to test your FastAPI backend application. The load tests are designed to measure performance, latency, and throughput under various levels of load.

## Overview

The load testing suite uses Locust, a powerful Python-based load testing tool. It allows you to:

- Simulate hundreds or thousands of users simultaneously
- Test both authenticated and unauthenticated endpoints
- Measure response times, throughput, and error rates
- Run tests in distributed mode across multiple machines
- Generate detailed reports for analysis

## Quick Start

1. Install dependencies:
   ```bash
   uv pip install locust requests
   ```

2. Create a test user:
   ```bash
   python -m app.core.locust_load_test.custom.create_test_user
   ```

3. Run a single-node test:
   ```bash
   # Using the convenience script
   cd backend/app/core/locust_load_test/custom
   ./run_load_test.sh single  # On Linux/Mac
   run_load_test.bat single   # On Windows
   
   # Or directly
   locust -f app/core/locust_load_test/custom/locustfile.py
   ```

4. Open http://localhost:8089 in your browser, enter the number of users and spawn rate, then start the test.

## Test Scenarios

The load tests simulate real users performing various actions:

1. **Authentication**: Users log in to obtain access tokens
2. **Health Check**: Tests the `/health` endpoint
3. **User Management**: Retrieves user data
4. **Item Operations**: Creates, reads, updates, and deletes items

Each operation is weighted according to expected usage patterns (configurable in `config.py`).

## Running Distributed Tests

For more realistic load testing, you can run Locust in distributed mode across multiple machines or terminals:

1. Start the master node:
   ```bash
   cd backend/app/core/locust_load_test/custom
   ./run_load_test.sh master 100 10  # 100 users, spawn rate 10
   # Or on Windows
   run_load_test.bat master 100 10
   ```

2. Start worker node(s) in separate terminals:
   ```bash
   cd backend/app/core/locust_load_test/custom
   ./run_load_test.sh worker
   # Or on Windows
   run_load_test.bat worker
   ```

3. Check the health of your Locust cluster:
   ```bash
   cd backend/app/core/locust_load_test/custom
   ./run_load_test.sh health
   # Or on Windows
   run_load_test.bat health
   ```

## Generating Reports

You can generate detailed HTML reports from your load tests:

```bash
python -m app.core.locust_load_test.custom.generate_report --output=my_report.html
```

This will create a comprehensive report with:
- Overall performance statistics
- Endpoint-specific metrics
- Error analysis
- Performance recommendations

## Customizing Tests

To customize the load tests for your specific needs:

1. **Modify Endpoints**: Edit `config.py` to change the target endpoints.
2. **Adjust User Behavior**: Modify the tasks in `locustfile.py` to change user behavior.
3. **Change Authentication**: Update the login process if your authentication flow is different.
4. **Adjust Task Weights**: Change the weight values in `config.py` to simulate different usage patterns.

## Performance Metrics to Monitor

When running load tests, pay attention to these key metrics:

- **Response Time**: Median and 95th percentile response times
- **Error Rate**: Percentage of failed requests
- **Throughput**: Requests per second handled by the system
- **Database Performance**: Query times and connection pool usage
- **Memory Usage**: Watch for memory leaks under sustained load
- **CPU Utilization**: Identify bottlenecks in processing

## Integration with Monitoring

The FastAPI application already has Prometheus metrics. For comprehensive monitoring:

1. Ensure Prometheus is scraping the `/api/v1/metrics` endpoint
2. Set up Grafana dashboards to visualize both system metrics and Locust results
3. Monitor all components (API, database, cache, etc.) during load testing

## Troubleshooting

- **Connection errors**: Ensure the BASE_URL in config.py is correct
- **Authentication failures**: Verify the test user credentials
- **Worker not connecting**: Check network connectivity between master and worker nodes
- **High error rates**: Look for exceptions in the Locust web UI and application logs

## Reference

For more information on Locust and advanced load testing techniques:

- [Locust Documentation](https://docs.locust.io/)
- See additional guides in the `_docs` directory
