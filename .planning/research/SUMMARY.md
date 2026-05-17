# Research Summary: NEO-Light

## Stack

Use a Python + Redis Streams + Parquet + DuckDB + Streamlit stack for a local-first analytics pipeline optimized for low-resource hardware. This combination keeps operational overhead low while preserving fast analytical reads.

## Table Stakes

- Reliable NASA API ingestion with rate-limit handling.
- Decoupled event transport through Redis stream.
- Partitioned raw Parquet storage.
- Deterministic DuckDB transforms and PHA classification.
- Dashboard with KPI, data explorer, and lightweight charts.

## Watch Out For

- API throttling and transient failures.
- Duplicate records across polling windows.
- Upstream schema changes.
- Query latency growth as local files accumulate.
- Memory pressure on constrained machines.

## Recommendation

Proceed with a coarse 4-phase roadmap emphasizing data integrity first, then analytics quality, then dashboard performance and operability.
