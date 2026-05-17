# NEO-Light

## What This Is

NEO-Light is an ultra-lightweight end-to-end tracking and analytics system for NASA Near-Earth Object (NEO) data. It ingests close-approach data from CNEOS/JPL APIs, streams events through Redis, stores raw partitions in Parquet, and serves processed analytics from DuckDB. It is designed for low-spec machines (4 GB-8 GB RAM) where heavy distributed stacks are not viable.

## Core Value

Deliver fast, reliable NEO hazard insight on low-resource hardware using a minimal local-first data stack.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Ingest NEO close-approach payloads from NASA APIs on a schedule.
- [ ] Buffer ingestion events via Redis stream/channel for decoupled processing.
- [ ] Persist raw events into daily-partitioned local Parquet files.
- [ ] Detect Potentially Hazardous Asteroids with the specified threshold logic.
- [ ] Serve analytics from a single local DuckDB database file.
- [ ] Expose a Streamlit dashboard with key metrics, explorer table, and charts.
- [ ] Run the system within low CPU/RAM limits and without heavyweight dependencies.

### Out of Scope

- Heavy distributed processing engines (Spark/Flink/Kafka) — violate low-footprint constraint.
- Managed/cloud data warehouses for core flow — local-first architecture is required.
- Advanced 3D visualization pipeline by default — optional/basic only to protect performance.

## Context

- Data source: NASA CNEOS/JPL close-approach API payloads.
- Eventing: Redis Streams or Pub/Sub, lightweight and memory-bounded.
- Storage model: Raw local Parquet partitioned by year/month/day.
- Analytics model: DuckDB transforms and serving from `neo_analytics.db`.
- Frontend: Streamlit + Plotly Express for low-overhead visualization.
- Delivery expectation: Clean modular code, exact dependency pinning, and quick startup guide.

## Constraints

- **Hardware**: Must run on 4 GB-8 GB RAM systems — avoid memory-heavy components.
- **Architecture**: No JVM-heavy services or heavy DB clusters — enforce minimal process footprint.
- **Deployment**: Docker only for Redis service — Python services run natively to reduce overhead.
- **Performance**: Dashboard should load quickly from local DuckDB — optimize query paths and indexing strategy.
- **Data Quality**: Hazard rule is fixed for v1 — Miss Distance < 0.05 AU AND Estimated Diameter > 140m.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use Redis as lightweight event broker | Keeps ingestion and persistence decoupled with tiny operational footprint | — Pending |
| Use local Parquet as raw lake format | Columnar storage and partitioning improve local analytic performance | — Pending |
| Use DuckDB instead of distributed engines | Provides high-performance OLAP on local files without cluster overhead | — Pending |
| Use Streamlit for dashboard | Fastest path to a practical analytics UI with Python-only stack | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-17 after initialization*
