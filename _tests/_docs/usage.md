
This guide explains the structure, configuration, and best practices for the Prometheus monitoring and alerting setup in this project. It covers all files in `app/core/prometheus` and their roles in observability, alerting, and metrics exposure.

---

## Directory Structure

```
app/core/prometheus/
├── config.py               # Prometheus configuration for the backend
├── metrics.py              # Metric definitions (counters, histograms, gauges)
├── middleware.py           # FastAPI middleware for exposing metrics
├── prometheus.yml          # Main Prometheus server configuration
├── rules/                  # Alerting and recording rules
│   ├── alerts.yml          # HTTP, FastAPI, and error/latency alerts
│   ├── credits.yml         # Credit usage rules and alerts
│   ├── pulsar_alerts.yml   # Pulsar-specific alerting rules
│   └── redis_alerts.yml    # Redis-specific alerting rules
└── _docs/                  # Prometheus documentation (best practices, SLOs, etc.)
```

---

## File-by-File Usage

### 1. `config.py`
- **Purpose:** Centralizes Prometheus-related settings (enable/disable, port, service URL, scrape interval, default labels, etc.).
- **Usage:** Imported by the backend to configure Prometheus metrics endpoint and service labels.
- **Best Practices:**
  - Keep all Prometheus config here for DRYness.
  - Use environment variables for sensitive or environment-specific values.

### 2. `metrics.py`
- **Purpose:** Defines all Prometheus metrics (counters, histograms, gauges) used throughout the backend.
- **Key Metrics:**
  - `http_requests_total`, `http_request_duration_seconds`: Track API traffic and latency.
  - `celery_tasks_total`, `celery_task_duration_seconds`: Monitor Celery task execution and performance.
  - `system_cpu_usage_percent`: System health.
- **Best Practices:**
  - Use labels for cardinality control (e.g., `method`, `endpoint`).
  - Follow conventions in `_docs/instrumentation.md` and `_docs/dos_donts.md`.

### 3. `middleware.py`
- **Purpose:** FastAPI middleware that automatically collects request metrics and exposes them at `/metrics`.
- **Key Features:**
  - Tracks request count, latency, and credits usage by user/type.
  - Custom counters for VAPI and Stripe API usage.
  - Implements `PrometheusMiddleware` class for easy integration.
- **Usage:** Add `PrometheusMiddleware` to FastAPI’s middleware stack.
- **Best Practices:**
  - Instrument all endpoints for observability.
  - Use middleware for automatic, low-boilerplate metric collection.

### 4. `prometheus.yml`
- **Purpose:** Main Prometheus server config (scraping, alerting, rule files, jobs).
- **Key Sections:**
  - `scrape_configs`: Defines metrics sources (backend, FastAPI, node exporter, etc.).
  - `rule_files`: Loads all YAML rule files in `rules/`.
  - `alerting`: Configures alertmanagers (if any).
- **Best Practices:**
  - Use HTTPS for scraping where possible.
  - Set scrape intervals and timeouts appropriate for your environment.

### 5. `rules/` Directory
- **Purpose:** Contains all alerting and recording rules for Prometheus.
- **Files:**
  - `alerts.yml`: General HTTP/FastAPI error and latency alerts (e.g., high error rate, high latency, elevated error rate).
  - `credits.yml`: Credit usage aggregation and low-credit alerting per user/type.
  - `pulsar_alerts.yml`: Pulsar-specific alerts (DLQ rate, batch latency, queue size, processing health).
  - `redis_alerts.yml`: Redis-specific alerts (down, high memory, high latency, connection limit, replication lag).
- **Best Practices:**
  - Use recording rules to pre-aggregate metrics for efficient alerting.
  - Tune alert thresholds to match production SLOs.
  - See `_docs/alerting.md` and `_docs/recording_rules.md` for advanced patterns.

---

## Example: Adding a New Metric

1. Define the metric in `metrics.py`:
   ```python
   from prometheus_client import Counter
   NEW_FEATURE_COUNT = Counter('new_feature_total', 'Description', ['label1'])
   ```
2. Increment the metric in your business logic:
   ```python
   NEW_FEATURE_COUNT.labels(label1=value).inc()
   ```
3. Expose the metric via FastAPI (handled by middleware).

---

## Example: Adding a New Alert

1. Add a rule to a YAML file in `rules/`:
   ```yaml
   - alert: MyCustomAlert
     expr: my_metric_total > 100
     for: 10m
     labels:
       severity: warning
     annotations:
       summary: "Custom alert triggered"
       description: "my_metric_total exceeded 100 for 10 minutes"
   ```
2. Reload Prometheus or let it pick up changes automatically.

---

## References & Best Practices
- See `_docs/alerting.md`, `_docs/instrumentation.md`, `_docs/dos_donts.md`, and `_docs/recording_rules.md` for guidance.
- Ensure all metrics are labeled and documented.
- Test alert rules in staging before deploying to production.
- Monitor for cardinality explosions and tune as needed.

---

## Troubleshooting
- If metrics do not appear in Prometheus, check scrape configs and `/metrics` endpoint.
- Use Prometheus UI to test alert expressions.
- For advanced patterns (async, Pulsar/Redis-specific), see the respective alert YAMLs and `_docs` best practices.

---

## Maintenance
- Regularly review and prune unused metrics and alerts.
- Update thresholds as production usage evolves.
- Keep documentation in sync with code and rule changes.

---

*This file was auto-generated to provide a clear, DRY, and production-ready reference for using and extending Prometheus monitoring in this project.*
