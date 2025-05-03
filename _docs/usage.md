# Locust Load Testing Usage Guide

This guide explains how to use the Locust-based load testing suite in this repository. It covers the purpose of each key file, setup instructions, running distributed tests, and best practices for customizing your scenarios.

---

## Overview

This module provides:
- **Distributed load testing** (master/worker mode)
- **Health checks** for Locust nodes
- **Customizable user scenarios**
- **Configurable via environment variables**
- **Integration ready for monitoring (Prometheus/Grafana)**

---

## File Purposes

- `config.py`: Centralizes all configuration (master/worker host/port, user count, spawn rate, base URL, etc.) using environment variables or project settings. Use this to adjust test parameters.
- `health_check.py`: Provides automated health checks for Locust master/worker nodes. Can be used as a CLI tool or imported as a module.
- `locustfile.py`: Main Locust test definition. Defines user behavior, endpoints to hit, and test logic. Edit this file to add or modify test scenarios.
- `run_distributed_locust.py`: CLI tool to launch Locust in distributed mode. Handles master/worker startup and parameter passing. Use this for production-like distributed tests.
- `README.MD`: High-level overview, quick start, and troubleshooting. (See also this file for in-depth usage.)
- `_docs/`: Contains guides, best practices, and advanced examples for load testing.

---

## Setup

1. **Install dependencies** (from project root, with venv activated):
   ```bash
   uv pip install locust
   ```

2. **Set environment variables** (optional, for custom config):
   ```bash
   export LOCUST_MASTER_HOST=localhost
   export LOCUST_MASTER_PORT=8089
   export BASE_URL=http://localhost:8000
   export LOCUST_WAIT_TIME_MIN=1
   export LOCUST_WAIT_TIME_MAX=3
   ```
   Or set them in your `.env` or deployment config.

---

## Running Locust

### Single Node (Local)

```bash
locust -f app/core/locust_load_test/locustfile.py
```
- Open [http://localhost:8089](http://localhost:8089) in your browser.
- Enter user count and spawn rate, then start the test.

### Distributed Mode

**Master Node:**
```bash
python app/core/locust_load_test/run_distributed_locust.py --master --users=100 --spawn-rate=10 --expect-workers=2
```

**Worker Node(s):** (run on separate machines or terminals)
```bash
python app/core/locust_load_test/run_distributed_locust.py --worker --host=<MASTER_HOST> --port=8089
```

---

## Health Checks

You can check master/worker node health with:
```bash
python app/core/locust_load_test/health_check.py
```
- Returns JSON with health status.
- Can be integrated into CI/CD or monitoring scripts.

---

## Customizing Tests

- Edit `locustfile.py` to change user behavior or add new endpoints.
- Use `@task` decorators to set task weights.
- Adjust wait times and user parameters in `config.py` or via environment variables.

---

## Best Practices

- Start with a small number of users and ramp up gradually.
- Validate both status codes and response content.
- Use realistic test data and user flows.
- Monitor system metrics alongside Locust metrics.
- For advanced tips, see `_docs/improve_load_testing.md` and `_docs/guide.md`.

---

## Troubleshooting

- **Connection errors:** Check `BASE_URL` and network/firewall settings.
- **Worker not connecting:** Ensure correct master host/port and network reachability.
- **Test failures:** Review logs, validate endpoints, and check for authentication issues.

---

## References
- [Locust Official Documentation](https://docs.locust.io/en/stable/)
- See `_docs/` for more advanced guides and ML-specific examples.

---

*This guide follows project documentation conventions. For further details, see other markdown files in `_docs/`.*
