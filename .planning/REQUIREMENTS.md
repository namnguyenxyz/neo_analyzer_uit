# Requirements: NEO-Light

**Defined:** 2026-05-17
**Core Value:** Deliver fast, reliable NEO hazard insight on low-resource hardware using a minimal local-first data stack.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Ingestion

- [x] **ING-01**: System can fetch Near-Earth Object close-approach data from NASA CNEOS/JPL API on a schedule.
- [x] **ING-02**: System handles API rate limits and transient failures with retry and backoff.
- [x] **ING-03**: System publishes each fetched payload to Redis stream `neo:stream`.

### Raw Storage

- [x] **RAW-01**: Consumer can read events from Redis and persist raw records to daily-partitioned Parquet files.
- [x] **RAW-02**: Raw records include normalized core fields required for downstream analytics.
- [x] **RAW-03**: Raw write process avoids duplicate inserts for identical ingestion windows.

### Analytics

- [x] **ANL-01**: Transformation job can query raw Parquet via DuckDB and cast fields into analytical schema.
- [x] **ANL-02**: System flags Potentially Hazardous Asteroid when miss distance < 0.05 AU and estimated diameter > 140m.
- [x] **ANL-03**: Serving tables are persisted to local DuckDB file `neo_analytics.db` for fast read access.

### Dashboard

- [ ] **DSH-01**: Streamlit dashboard displays total active NEOs, total flagged PHAs, and closest approach of day.
- [ ] **DSH-02**: Dashboard provides searchable/filterable NEO table sortable by proximity or velocity.
- [ ] **DSH-03**: Dashboard renders Plotly charts for asteroid size distribution and approach velocity over time.
- [ ] **DSH-04**: Dashboard reads `neo_analytics.db` in read-only mode.

### Operations

- [x] **OPS-01**: Repository includes minimal `docker-compose.yml` with Redis memory limit.
- [ ] **OPS-02**: Repository includes `requirements.txt` with exact versions for required Python packages.
- [ ] **OPS-03**: README includes startup steps for Redis, pipeline scripts, and dashboard launch.

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Alerting and Insights

- **ALR-01**: System can send alert notifications when new PHA candidates are detected.
- **ALR-02**: System can compute trend/anomaly insights over historical NEO approach data.

### Visualization

- **VIS-01**: Dashboard supports richer 3D orbital visualization mode.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Spark/Flink/Kafka pipelines | Heavy infrastructure violates low-footprint objective |
| Elastic cluster for serving | Single-machine embedded analytics is sufficient for v1 |
| Full multi-tenant auth model | Not needed for local first MVP analytics tool |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ING-01 | Phase 1 | Complete |
| ING-02 | Phase 1 | Complete |
| ING-03 | Phase 1 | Complete |
| RAW-01 | Phase 1 | Complete |
| RAW-02 | Phase 2 | Complete |
| RAW-03 | Phase 2 | Complete |
| ANL-01 | Phase 2 | Complete |
| ANL-02 | Phase 2 | Complete |
| ANL-03 | Phase 2 | Complete |
| DSH-01 | Phase 3 | Pending |
| DSH-02 | Phase 3 | Pending |
| DSH-03 | Phase 3 | Pending |
| DSH-04 | Phase 3 | Pending |
| OPS-01 | Phase 1 | Complete |
| OPS-02 | Phase 4 | Pending |
| OPS-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 16 total
- Mapped to phases: 16
- Unmapped: 0

---
*Requirements defined: 2026-05-17*
*Last updated: 2026-05-17 after phase 2 execution*
