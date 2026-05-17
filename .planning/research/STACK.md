# Stack Research: NEO-Light

## Recommended 2026 Stack

- Python 3.11+ for all pipeline scripts and dashboard glue.
- Redis 7.x as lightweight broker (Streams preferred over Pub/Sub for at-least-once replay).
- DuckDB 1.1+ as embedded analytical engine over local Parquet.
- Parquet files partitioned by date for efficient pruning.
- Streamlit 1.45+ with Plotly Express for lightweight interactive analytics.

## Why This Stack Fits

- Low-memory runtime profile compared with distributed alternatives.
- Minimal operational complexity for single-machine deployment.
- High local scan/query performance through DuckDB vectorization.
- Fast implementation cycle using a single primary language (Python).

## What Not To Use

- Spark, Flink, Elasticsearch, or Kafka for v1 due to infrastructure overhead.
- JVM-heavy services unless scaling constraints later justify migration.
- Multi-container orchestration beyond Redis in early milestones.

## Confidence

- Redis + DuckDB + Parquet for local analytics pipelines: High
- Streamlit for low-footprint dashboards: High
- Need for advanced caching before v1: Medium (likely unnecessary initially)
