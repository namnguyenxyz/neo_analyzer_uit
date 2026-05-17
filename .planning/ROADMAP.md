# Roadmap: NEO-Light

**Created:** 2026-05-17
**Mode:** mvp
**Granularity:** coarse

## Summary

- Total phases: 4
- v1 requirements: 16
- Coverage: 100%

### Phase 1: Ingestion Baseline and Raw Capture
**Goal:** Establish reliable NASA ingestion, event streaming, and raw persistence foundation.
**Mode:** mvp
**Requirements:** ING-01, ING-02, ING-03, RAW-01, OPS-01
**Success Criteria**:
1. NASA payloads are fetched on schedule and published to `neo:stream`.
2. Redis-backed consumer writes daily-partitioned Parquet without data loss in nominal runs.
3. Redis service runs via minimal docker compose with memory cap and restart policy.

### Phase 2: Analytics Core and Hazard Classification
**Goal:** Build deterministic transformation pipeline and PHA flagging logic in DuckDB.
**Mode:** mvp
**Requirements:** RAW-02, RAW-03, ANL-01, ANL-02, ANL-03
**Success Criteria**:
1. Raw Parquet can be transformed into typed analytical tables through DuckDB scripts.
2. Hazard logic correctly flags PHA candidates using miss distance and diameter thresholds.
3. `neo_analytics.db` is generated and queryable for dashboard consumption.

### Phase 3: Dashboard Experience
**Goal:** Deliver fast, useful exploration and visualization on local analytics data.
**Mode:** mvp
**Requirements:** DSH-01, DSH-02, DSH-03, DSH-04
**Success Criteria**:
1. Streamlit shows KPI cards for total NEOs, PHAs, and closest approach.
2. Users can search/filter/sort a NEO table by proximity and velocity.
3. Plotly charts render size and velocity trends with acceptable responsiveness on low-spec hardware.

### Phase 4: Hardening and Delivery
**Goal:** Finalize operational docs, packaging, and low-resource reliability posture.
**Mode:** mvp
**Requirements:** OPS-02, OPS-03
**Success Criteria**:
1. `requirements.txt` pins exact versions for required dependencies.
2. README documents startup, run order, and troubleshooting for the full local stack.
3. End-to-end flow validates from NASA API to dashboard without heavy dependencies.

---
*Last updated: 2026-05-17 after initial roadmap creation*
