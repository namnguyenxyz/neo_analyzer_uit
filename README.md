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
