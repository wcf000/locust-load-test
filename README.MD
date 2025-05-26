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
## 📁 Folder Structure & Conventions

```
locust_load_test/
├── _docs/           # Markdown docs, best practices, diagrams, usage
├── _tests/          # Unit/integration tests for all core logic
├── config.py        # Singleton config (class-based, imports from global settings)
├── docker/          # Dockerfile, docker-compose, provisioning config, env
├── models/          # Pydantic models or test data schemas
├── exceptions/      # Custom exceptions for load testing
├── <core>.py        # Main implementation (health_check.py, locustfile.py, etc.)
├── README.md        # Main readme (this file)
```

- **_docs/**: All documentation, diagrams, and best practices for this module.
- **_tests/**: All tests for this module, including performance, smoke, and distributed tests.
- **config.py**: Singleton config pattern, imports from global settings, exposes all constants for this module.
- **docker/**: Containerization assets (Dockerfile, docker-compose, provisioning configs, .env.example, etc).
- **models/**: Pydantic models or test data schemas for input/output validation.
- **exceptions/**: Custom exception classes for robust error handling.
- **<core>.py**: Main implementation modules (e.g., health_check.py, locustfile.py, etc).

---

## 🏗️ Singleton & Config Pattern
- Use a single class (e.g., `LocustConfig`) in `config.py` to centralize all env, test, and integration settings.
- Import from global settings to avoid duplication and ensure DRY config.
- Document all config keys in `_docs/usage.md` and in this README.

---

## 📄 Documentation & Testing
- Place all best practices, diagrams, and usage guides in `_docs/`.
- All tests (unit, integration, smoke, distributed) go in `_tests/` with clear naming.
- Use `_tests/_docs/` for test-specific docs if needed.

---

## 🐳 Docker & Distributed Testing
- Place Dockerfile(s), docker-compose, and provisioning configs in `docker/`.
- Provide `.env.example` for local/dev/prod setups.
- Use distributed mode for production-like load tests.


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
