# MCP Server Load Testing

This directory contains load tests specifically designed for the Model Context Protocol (MCP) Server component of the FastAPI application.

## Overview

The MCP Server exposes tools and resources for LLM/AI agent interactions while ensuring security by blocking sensitive routes. This load test validates:

1. **Performance**: Response times under various load conditions
2. **Security**: Verification that sensitive endpoints are properly blocked
3. **Functionality**: MCP tools and resources work correctly under load
4. **Stability**: Server remains stable during concurrent requests

## Files

- `mcp_server_load_test.py` - Main load test with various test scenarios
- `run_mcp_load_test.sh` - Unix/Linux/macOS runner script
- `run_mcp_load_test.bat` - Windows runner script
- `README_MCP.md` - This documentation

## Quick Start

### Prerequisites

Ensure you have Poetry installed for dependency management:

```bash
# Install Poetry if needed
curl -sSL https://install.python-poetry.org | python3 -
```

### Running Tests

#### Option 1: Web Interface (Recommended)

```bash
# Unix/Linux/macOS
./run_mcp_load_test.sh

# Windows
run_mcp_load_test.bat
```

This will start the Locust web interface at `http://localhost:8089` where you can:
- Configure number of users and spawn rate
- Start/stop tests
- View real-time metrics and graphs
- Download results

#### Option 2: Headless Mode

```bash
# Unix/Linux/macOS
./run_mcp_load_test.sh --headless --users 20 --spawn-rate 5 --time 120s

# Windows
run_mcp_load_test.bat --headless --users 20 --spawn-rate 5 --time 120s
```

#### Option 3: Direct Locust Command

```bash
# Install locust if needed
poetry add locust

# Run test
poetry run locust -f mcp_server_load_test.py --host=https://your-server.com
```

## Test Scenarios

### MCPServerUser (Default)
- Tests all MCP endpoints with balanced load
- Simulates normal AI agent usage patterns
- Wait time: 1-3 seconds between requests

### MCPLightLoad
- Lighter load simulation for normal usage
- Weight: 3 (more instances)
- Wait time: 2-5 seconds between requests

### MCPHeavyLoad  
- Heavy load simulation for stress testing
- Weight: 1 (fewer instances)
- Wait time: 0.5-1.5 seconds between requests

## Test Coverage

### Functional Tests
- `/api/v1/mcp/status` - MCP server status
- `/api/v1/mcp/health` - Health checks
- `/api/v1/mcp/discovery` - Tool/resource discovery
- `/api/v1/tools/call` - MCP tool execution (add tool)
- `/api/v1/resources/*` - Resource retrieval

### Security Tests
- Verifies blocked endpoints return 404/403/401
- Tests that sensitive routes are inaccessible:
  - Authentication endpoints (`/login`, `/auth`)
  - User management (`/users`, `/signup`)
  - Admin/debug endpoints (`/admin`, `/debug`)
  - Destructive operations (`DELETE`, `PUT`, `PATCH`)

### Performance Tests
- Response time monitoring
- Concurrent user simulation
- Error rate tracking
- Throughput measurement

## Configuration Options

### Runner Script Options
```bash
--host URL          # Target server URL (default: render deployment)
--users N           # Number of concurrent users (default: 10)
--spawn-rate N      # User spawn rate per second (default: 2)
--time DURATION     # Test duration (default: 60s)
--headless          # Run without web UI
--help              # Show help
```

### Environment Variables
You can also set these environment variables:
- `MCP_TEST_HOST` - Target server URL
- `MCP_TEST_USERS` - Number of users
- `MCP_TEST_DURATION` - Test duration

## Interpreting Results

### Key Metrics to Monitor

1. **Response Time**
   - Average: Should be < 200ms for healthy performance
   - 95th percentile: Should be < 500ms
   - Max: Outliers are acceptable but investigate if consistently high

2. **Request Rate**
   - RPS (Requests Per Second): Higher is better
   - Should scale linearly with user count initially

3. **Error Rate**
   - Should be < 1% for normal operations
   - Higher rates indicate server issues

4. **Specific Endpoint Performance**
   - `/mcp/status` and `/mcp/health`: Should be fastest (< 50ms)
   - Tool calls: May be slower depending on complexity
   - Security tests: Blocked endpoints should be fast to reject

### Common Issues

1. **High Error Rates**
   - Check server logs for errors
   - Verify MCP server is running
   - Check network connectivity

2. **Slow Response Times**
   - Server may be overloaded
   - Database connection issues
   - Network latency

3. **Security Test Failures**
   - Sensitive endpoints not properly blocked
   - Route filtering logic needs review

## Production Considerations

### Load Test Guidelines

1. **Start Small**: Begin with 5-10 users and gradually increase
2. **Monitor Resources**: Watch CPU, memory, and database connections
3. **Test Different Scenarios**: Mix of light and heavy load users
4. **Duration**: Run tests for at least 5-10 minutes for meaningful results

### Performance Targets

- **Concurrent Users**: Should handle 100+ concurrent MCP clients
- **Response Time**: < 200ms average for API calls
- **Availability**: 99.9% uptime during normal load
- **Error Rate**: < 0.1% for successful operations

### Scaling Recommendations

Based on load test results:
- Scale horizontally by adding more server instances
- Implement caching for frequently accessed resources
- Use connection pooling for database connections
- Consider CDN for static resources

## Troubleshooting

### Common Installation Issues

```bash
# If locust installation fails
poetry cache clear --all
poetry install --no-cache

# If import errors occur
poetry run pip install locust
```

### Test Execution Issues

```bash
# Check server connectivity
curl https://your-server.com/api/v1/health

# Verify MCP endpoints
curl https://your-server.com/api/v1/mcp/status

# Test blocked endpoints (should return 404/403)
curl https://your-server.com/api/v1/login/access-token
```

### Performance Issues

1. **Check server resources**:
   ```bash
   # CPU and memory usage
   top
   
   # Network connections
   netstat -an | grep :8000
   ```

2. **Review server logs** for errors during load tests

3. **Database performance**: Check for slow queries or connection limits

## Advanced Usage

### Custom Test Scenarios

You can modify `mcp_server_load_test.py` to add custom test scenarios:

```python
@task(1)
def custom_mcp_test(self):
    """Custom test for specific MCP functionality."""
    # Your custom test logic here
    pass
```

### Integration with CI/CD

Add to your CI/CD pipeline:

```yaml
# Example GitHub Actions step
- name: Run MCP Load Test
  run: |
    cd backend/app/core/locust_load_test
    poetry run locust -f mcp_server_load_test.py \
      --host=${{ secrets.MCP_SERVER_URL }} \
      --users=50 --spawn-rate=10 --run-time=300s \
      --headless --csv=results/mcp_load_test
```

### Monitoring Integration

Combine with monitoring tools:
- Prometheus metrics collection during tests
- Grafana dashboards for visualization
- Alert configuration for performance thresholds

## Contributing

When adding new MCP features:
1. Add corresponding load tests
2. Update security test patterns if needed
3. Document performance expectations
4. Test with realistic load scenarios

## Support

For issues with load testing:
1. Check server logs during test execution
2. Verify MCP server configuration
3. Review network connectivity
4. Consult FastAPI and Locust documentation
