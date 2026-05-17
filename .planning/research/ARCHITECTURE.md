# Architecture Research: NEO-Light

## Component Boundaries

1. Fetcher (`producer`) pulls NASA API payloads and publishes to Redis.
2. Raw consumer (`raw-writer`) reads stream events and writes partitioned Parquet.
3. Transformer (`analytics-builder`) reads Parquet with DuckDB and builds serving tables.
4. Dashboard (`streamlit-app`) reads DuckDB in read-only mode for UI queries.

## Data Flow

NASA API -> Python Fetcher -> Redis `neo:stream` -> Parquet Raw Zone -> DuckDB Transform -> `neo_analytics.db` -> Streamlit Dashboard

## Build Order

1. Stand up Redis and connectivity checks.
2. Implement producer with scheduling and retries.
3. Implement consumer and partitioned Parquet sink.
4. Implement DuckDB transformation and PHA logic.
5. Build dashboard views over serving tables.
6. Add operational hardening (logging, retention, graceful restarts).

## Integration Notes

- Use deterministic event keys to reduce duplicate writes.
- Keep schema contracts explicit between raw and analytics layers.
- Prefer append-only raw zone with periodic compaction.
