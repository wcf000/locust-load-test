# How to Run Locust Tests in This Folder

## Overview
This folder contains Locust performance/load test scripts for the backend. These are **not** pytest tests and should not be run with `pytest`. Instead, use the Locust CLI or the provided Python runner script for distributed testing.

---

## 1. Local/Standalone Locust Run

From the project root or backend directory:

```sh
locust -f app/core/locust/_tests/locust_performance.py
```

- This will launch the Locust web UI (default: http://localhost:8089) where you can set the number of users and spawn rate.
- Make sure your environment variables (e.g., `GRAFANA_URL`, `GRAFANA_API_KEY`) are set, or edit your `.env`/config files as needed.

---

## 2. Distributed Locust Run (Master/Worker)

**Recommended for simulating high load or running in CI/CD.**

### Start the Master Node
```sh
python app/core/locust/_tests/run_distributed_locust.py --master
```
- You can set users, spawn rate, and expected workers with CLI flags or environment variables:
  - `--users 1000 --spawn-rate 50 --expect-workers 4`

### Start Worker Nodes (in separate terminals or machines)
```sh
python app/core/locust/_tests/run_distributed_locust.py --worker --host <master-ip>
```

---

## 3. Common Issues
- **Do not run these with `pytest`.** Pytest will not find any tests.
- If you see `Could not find 'locust_performance.py'`, make sure you are running from the correct directory (the script expects the locustfile to be in the current working directory, or use the full relative path).
- Ensure all environment variables are set for your test scenario.

---

## 4. References
- [Project Locust Best Practices Guide](../../../_docs/backend_best_practices/locust/guide.md)
- [Locust Documentation](https://docs.locust.io)
- [Pydantic v2 Migration Guide](https://errors.pydantic.dev/2.11/migration/)

---

## 5. Example Environment Variables
```sh
export GRAFANA_URL="http://localhost:3000"
export GRAFANA_API_KEY="your_key_here"
```

---

## 6. CI/CD Integration
- Use the distributed runner and parse Locust's output for performance metrics.
- Do **not** try to run these tests with `pytest` in CI/CD; use the Locust CLI or runner script.

---

For further details, see the Locust best practices guide in the `_docs` folder.
