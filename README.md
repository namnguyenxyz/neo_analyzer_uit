# NEO-Light

Ultra-lightweight NEO tracking and analytics pipeline designed for low-spec machines.

## Phase 1 Scope

- Redis runtime foundation with memory constraints.
- NASA close-approach fetch and Redis stream publisher.
- Redis stream consumer that writes daily partitioned raw Parquet files.

## Prerequisites

- Python 3.11+
- Docker + Docker Compose plugin
- `redis-cli` (optional, for smoke checks)

## Start Redis

```bash
docker compose up -d redis
docker compose ps
```

## Run Producer

```bash
python -m src.ingestion.publish_stream
```

## Run Consumer

```bash
python -m src.storage.consume_stream_to_parquet
```

Stop with `Ctrl+C` after the first successful write log.

## Phase 1 Smoke Check

Run producer and verify stream messages exist:

```bash
python -m src.ingestion.publish_stream
redis-cli XLEN neo:stream
```

Expected: stream length greater than `0` indicates producer publish success.

Verify raw parquet output exists:

```bash
find data/raw -name neo_data.parquet
```

Expected partition pattern:

`data/raw/year=YYYY/month=MM/day=DD/neo_data.parquet`

## Notes

- Stream name defaults to `neo:stream`.
- Configure runtime via environment variables in `src/common/config.py`.

## Phase 2 Transform Smoke Check

Run typed transformation against local raw parquet partitions:

```bash
python -m src.analytics.transform_raw_to_typed
```

Verify output artifact and typed row count:

```bash
test -f neo_analytics.db
python -c "import duckdb; con=duckdb.connect('neo_analytics.db'); print(con.execute('select count(*) from neo_typed_staging').fetchone()[0])"
```

Expected: command succeeds and returns a non-negative integer.

## Phase 2 Analytics Build

Build the full analytics serving layer (transform + hazard classification + views):

```bash
python -m src.analytics.build_analytics_db --rebuild
```

Verify queryability for totals, hazardous counts, and closest approach today:

```bash
python -c "import duckdb; con=duckdb.connect('neo_analytics.db'); print(con.execute('select * from v_pha_counts').fetchall())"
python -c "import duckdb; con=duckdb.connect('neo_analytics.db'); print(con.execute('select * from v_closest_approach_today').fetchall())"
python -c "import duckdb; con=duckdb.connect('neo_analytics.db'); print(con.execute('select count(*) from v_neo_latest').fetchone()[0])"
```

Expected: each query runs without error and returns a scalar or row tuple result.

## Phase 3 Dashboard Smoke Check

Launch the Streamlit dashboard against the local DuckDB file:

```bash
streamlit run src/dashboard/app.py
```

Expected behavior:
- KPI cards show total NEOs, total PHAs, and the closest approach object for today.
- The explorer supports search, hazard-only filtering, sort direction, and pagination.
- Plotly charts render size distribution and approach velocity vs miss distance from `neo_hazard_classified`.

## Full End-to-End Run Order

For a complete local pipeline run:

1. **Start infrastructure:**
   ```bash
   docker compose up -d redis
   ```

2. **Optional: Generate sample data** (requires valid NASA API key):
   ```bash
   export NASA_API_KEY=your_key
   python -m src.ingestion.publish_stream
   ```

3. **Build analytics from local raw data:**
   ```bash
   python -m src.analytics.build_analytics_db --rebuild
   ```

4. **Launch dashboard:**
   ```bash
   streamlit run src/dashboard/app.py
   ```

## Troubleshooting

### Database errors / DB file locked
- Ensure no other process has a write connection to `neo_analytics.db`
- Rebuild with `python -m src.analytics.build_analytics_db --rebuild` to reset

### Dashboard: "No data available"
- Run the analytics build first: `python -m src.analytics.build_analytics_db --rebuild`
- Verify the `neo_analytics.db` file exists in the repo root

### Missing packages / Import errors
- Ensure you're using the workspace Python: `.venv/bin/python`
- Reinstall dependencies: `.venv/bin/pip install -r requirements.txt`

### Redis connection errors
- Verify Redis is running: `docker compose ps redis`
- Restart if needed: `docker compose down && docker compose up -d redis`
