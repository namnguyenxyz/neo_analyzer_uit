# Phase 1: Ingestion Baseline and Raw Capture - Research

**Researched:** 2026-05-17
**Domain:** Lightweight event-driven ingestion pipeline (NASA API -> Redis -> Parquet)
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

No user constraints - all decisions at the agent's discretion.
</user_constraints>

<research_summary>
## Summary

Phase 1 should establish a durable baseline for ingesting NASA NEO close-approach data and capturing raw events without introducing heavy infrastructure. The preferred architecture is a lightweight producer/consumer pair connected through Redis Streams so ingestion and storage can fail/retry independently.

The producer should implement bounded retries and backoff for API reliability. The consumer should normalize incoming payloads and persist daily partitions in Parquet to keep downstream DuckDB reads efficient.

**Primary recommendation:** Implement Redis Stream-based producer/consumer first, with deterministic partitioned Parquet writes and simple observability.
</research_summary>

<standard_stack>
## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| redis | 5.0.x | Redis client for producer/consumer | Stable Python integration and stream support |
| requests | 2.32.x | API fetch and retry wrapping | Minimal overhead HTTP for data pipelines |
| pandas | 2.2.x | Row normalization for parquet writes | Familiar ETL operations with good pyarrow support |
| pyarrow | 16.x | Parquet encoding engine | Required for efficient parquet output |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| tenacity | 8.x | Retry policy ergonomics | If manual retry loops become noisy |
| python-dateutil | 2.9.x | Datetime parsing | For robust timestamp coercion |
</standard_stack>

<architecture_patterns>
## Architecture Patterns

### Recommended Project Structure

```text
src/
  ingestion/
    fetch_nasa_neos.py
    publish_stream.py
  storage/
    consume_stream_to_parquet.py
  common/
    config.py
    logging_utils.py
```

### Pattern 1: Stream decoupling
**What:** Producer writes one event payload per stream message; consumer acknowledges only after parquet write succeeds.
**When to use:** Any ingestion flow where API fetch and storage throughput differ.

### Pattern 2: Date partitioning at write time
**What:** Partition raw output by `year=/month=/day=` using approach/ingest date.
**When to use:** Expected query filters include recency and date windows.

### Anti-Patterns to Avoid
- Writing one parquet file per event (too many tiny files)
- Coupling API fetch directly to DB writes (no buffering/replay)
- Unbounded retries without dead-letter fallback
</architecture_patterns>

<common_pitfalls>
## Common Pitfalls

### Pitfall 1: API throttling causes silent data gaps
**How to avoid:** Add retry + jitter and log skipped windows clearly.

### Pitfall 2: Duplicate events inflate counts
**How to avoid:** Use deterministic event id (`neo_reference_id + close_approach_date + epoch`) and dedupe before write.

### Pitfall 3: Growing memory during writes
**How to avoid:** Flush in bounded batches and avoid keeping full-day payloads in memory.
</common_pitfalls>

<sources>
## Sources

- Existing project planning docs in `.planning/`
- NASA CNEOS NEO API domain conventions (from provided project brief)
</sources>

---
*Phase: 01-ingestion-baseline-and-raw-capture*
*Research completed: 2026-05-17*
*Ready for planning: yes*
