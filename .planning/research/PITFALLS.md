# Pitfalls Research: NEO-Light

## Common Pitfalls

### 1. API Burst or Throttle Failures
- Warning signs: Frequent 429/5xx responses, missing intervals in raw data.
- Prevention: Exponential backoff, jitter, bounded retries, and checkpointed polling windows.
- Phase to address: Phase 1 (ingestion baseline).

### 2. Duplicate and Inconsistent Event Records
- Warning signs: Repeated object IDs with conflicting timestamps; inflated counts.
- Prevention: Normalize identifiers, enforce dedupe keys, and idempotent write logic.
- Phase to address: Phase 1-2 (raw storage and transform).

### 3. Schema Drift From Upstream API
- Warning signs: Parse errors, null spikes in key metrics, failed transforms.
- Prevention: Defensive parsing, schema versioning, and fallback default handling.
- Phase to address: Phase 2 (analytics pipeline).

### 4. Slow Dashboard Queries on Larger Local Data
- Warning signs: Streamlit interactions lag over time; high CPU during table filtering.
- Prevention: Pre-aggregate serving tables, limit default row windows, and add derived summary tables.
- Phase to address: Phase 3 (dashboard and performance hardening).

### 5. Resource Saturation on Low-Spec Machines
- Warning signs: Swap usage rises, container restarts, long response times.
- Prevention: Redis memory cap, bounded batch sizes, and small scheduled processing windows.
- Phase to address: Cross-cutting (all phases).
