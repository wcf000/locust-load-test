# Locust Load Testing Module

## Overview

This module contains performance testing infrastructure using [Locust](https://locust.io/), a scalable load testing tool. Tests simulate real user behavior to validate system performance under load.

## Key Features

- **Distributed Testing**: Run tests across multiple workers
- **Real-time Metrics**: Built-in web UI with live statistics
- **Custom Scenarios**: Simulate complex user workflows
- **Integration Ready**: Works with Grafana for advanced monitoring (optional)

## Quick Start

### 1. Installation

```bash
uv pip install locust
2. Running Tests
Single Node:

bash
CopyInsert in Terminal
locust -f app/core/locust_load_test/_tests/locust_performance.py
Distributed Mode:

bash
CopyInsert
# Master node
locust -f app/core/lost_load_test/_tests/locust_performance.py --master

# Worker nodes (run on separate machines)
locust -f app/core/locust_load_test/_tests/locust_performance.py --worker --master-host=<MASTER_IP>
3. Access Web UI
Open: http://localhost:8089 (default port)

Configuration
Environment variables in config.py:

python
CopyInsert
LOCUST_MASTER_HOST = "localhost"  # For distributed tests
LOCUST_MASTER_PORT = 8089        # Web UI port
BASE_URL = "http://localhost:8000"  # Target system
File Structure
CopyInsert
locust_load_test/
├── _tests/
│   ├── locust_performance.py   # Main test scenarios
│   └── run_distributed_locust.py  # Distributed test runner
├── config.py                  # Test configuration
├── health_check.py            # Node monitoring
└── README.md                  # This file
Best Practices
Start with small user counts (10-50) and gradually increase
Use @task decorators to organize test scenarios
Monitor both Locust metrics and system resources
For production tests, use distributed mode with multiple workers
Troubleshooting
Connection Issues: Verify BASE_URL is accessible
Performance Bottlenecks: Check database queries and external dependencies
Distributed Testing: Ensure all workers can connect to master node
For advanced usage, see our Locust Best Practices Guide.

CopyInsert

Would you like me to:
1. Create this file now?
2. Add specific test examples?
3. Include Grafana dashboard integration details?

Let me know if you'd like any modifications to the content or structure.
```
