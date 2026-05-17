# Phase 2: Analytics Core and Hazard Classification - Research

**Researched:** 2026-05-17
**Domain:** Deterministic local analytics pipeline (Parquet -> DuckDB typed tables -> PHA classification)
**Confidence:** HIGH

<user_constraints>
## User Constraints (from available context)

No explicit phase-level constraints were provided.
Decisions prioritize low-memory, local-first execution.
</user_constraints>

<research_summary>
## Summary

Phase 2 should use a SQL-first DuckDB flow that reads Phase 1 Parquet partitions, applies explicit typing and dedupe, computes PHA flags, and persists serving tables in a single local file (`neo_analytics.db`).

This directly addresses:
- RAW-02: normalized core fields for analytics
- RAW-03: duplicate protection for repeated ingestion windows
- ANL-01: typed transformation via DuckDB
- ANL-02: deterministic PHA logic (`miss_distance_au < 0.05` and `estimated_diameter_m > 140`)
- ANL-03: queryable local DuckDB serving layer

**Primary recommendation:** Keep heavy transformation logic in DuckDB SQL and reserve pandas usage for small validation-only checks.
</research_summary>

<standard_stack>
## Standard Stack

### Core
| Library | Version band | Purpose | Why Standard |
|---------|--------------|---------|--------------|
| duckdb | 1.5.x | SQL transformation and local serving DB | Embedded, fast OLAP on local files |
| pandas | 2.2+ | Lightweight QA and row checks | Minimal glue when SQL-only output checks are not enough |
| pyarrow | 16+ | Parquet interoperability | Stable parquet engine used by upstream writes |

### Supporting
| Library | Version band | Purpose | When to Use |
|---------|--------------|---------|-------------|
| pathlib / argparse | stdlib | file and CLI handling | Always |
| json / datetime | stdlib | metadata and deterministic timestamps | Always |
</standard_stack>

<architecture_patterns>
## Architecture Patterns

### Pattern 1: SQL-first typed staging
**What:** Read partitioned Parquet with DuckDB and cast to analytical schema using explicit types.
**When to use:** Every transformation run to prevent drift in downstream dashboards.

### Pattern 2: Deterministic dedupe before serving
**What:** Dedupe by `event_id` with stable tie-break (`fetched_at_utc` descending).
**When to use:** On each rebuild/replay run to satisfy RAW-03.

### Pattern 3: Single-file serving DB
**What:** Persist final analytical objects into `neo_analytics.db`.
**When to use:** Always for local dashboards and fast startup.

### Suggested module layout
```text
src/
  analytics/
    __init__.py
    transform_raw_to_typed.py
    classify_hazard.py
    build_analytics_db.py
    thresholds.py
    sql/
      raw_to_typed.sql
      hazard_classification.sql
      serving_views.sql
```
</architecture_patterns>

<common_pitfalls>
## Common Pitfalls

### Pitfall 1: Duplicate growth after reruns
**How to avoid:** Enforce dedupe in SQL before writing serving objects and verify duplicate count is zero.

### Pitfall 2: Silent cast failures
**How to avoid:** Use explicit casts and null-rate checks on critical numeric columns.

### Pitfall 3: Non-deterministic hazard outputs
**How to avoid:** Keep threshold constants centralized and apply the exact ANL-02 predicate in SQL.

### Pitfall 4: In-memory DB by accident
**How to avoid:** Always connect with filename path (`neo_analytics.db`) and smoke-test reopen query.
</common_pitfalls>

<verification_guidance>
## Verification Guidance for Execution

- Confirm typed table exists and contains required normalized columns.
- Assert `COUNT(*) - COUNT(DISTINCT event_id) = 0` after dedupe.
- Assert hazard mismatch count is zero using:
  - `is_potentially_hazardous = (miss_distance_au < 0.05 AND estimated_diameter_m > 140)`
- Re-open `neo_analytics.db` in a new process and run select queries to confirm persistence.
</verification_guidance>

<sources>
## Sources

- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- Existing Phase 1 implementation in `src/ingestion/` and `src/storage/`
- Existing Phase 1 planning artifact style in `.planning/phases/01-ingestion-baseline-and-raw-capture/`
</sources>

---
*Phase: 02-analytics-core-and-hazard-classification*
*Research completed: 2026-05-17*
*Ready for planning: yes*
