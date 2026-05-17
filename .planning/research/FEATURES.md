# Feature Research: NEO-Light

## Table Stakes

### Ingestion
- Scheduled polling from NASA CNEOS/JPL API.
- Rate-limit aware retry/backoff behavior.
- Basic API health/error logging.

### Event Stream
- Publish raw payloads to a named stream (`neo:stream`).
- Consumer-group or offset handling for resilience.
- Dead-letter handling for malformed records.

### Raw Storage
- Append raw events to daily Parquet partitions.
- Stable schema normalization for core NEO fields.
- Idempotent write strategy for duplicate fetch windows.

### Analytics
- Typed transformations from raw to analytics-ready model.
- Hazard flag logic for PHA detection.
- Materialized serving tables in `neo_analytics.db`.

### Dashboard
- KPI cards (total NEOs, flagged PHAs, closest approach).
- Filterable searchable table for tracked objects.
- Plotly charts for size and velocity trends.

## Differentiators (Not Required for v1)

- Alerting channels (email/Slack/webhook) for new hazard candidates.
- Forecast/risk scoring beyond binary PHA rule.
- Historical anomaly detection and trend forecasting.
- Advanced 3D orbital rendering.

## Anti-Features

- Full distributed microservice architecture for MVP.
- Heavy BI tooling integration before stable data model exists.
- Complex auth/role management for single-user local deployment.

## Dependencies

- Dashboard depends on DuckDB serving tables.
- DuckDB serving depends on reliable Parquet raw partitions.
- Parquet write path depends on Redis stream consumer continuity.
