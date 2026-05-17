from __future__ import annotations

from pathlib import Path
from time import perf_counter

import duckdb

from src.common.config import get_runtime_config
from src.common.logging_utils import get_logger

logger = get_logger(__name__)
DB_PATH = Path("neo_analytics.db")
SQL_PATH = Path(__file__).with_name("sql") / "raw_to_typed.sql"


def _escaped_path(value: str) -> str:
    return value.replace("'", "''")


def _create_empty_staging(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE OR REPLACE TABLE neo_typed_staging (
            object_id VARCHAR,
            object_name VARCHAR,
            close_approach_date DATE,
            close_approach_ts TIMESTAMP,
            relative_velocity_km_s DOUBLE,
            miss_distance_au DOUBLE,
            estimated_diameter_m DOUBLE,
            source_payload VARCHAR,
            fetched_at_utc VARCHAR,
            fetched_at_ts TIMESTAMP,
            event_id VARCHAR
        );
        """
    )


def run_transform() -> dict[str, int | str]:
    started = perf_counter()
    cfg = get_runtime_config()
    raw_glob = str(Path(cfg.storage["raw_data_root"]) / "year=*" / "month=*" / "day=*" / "neo_data.parquet")
    parquet_files = sorted(Path().glob(raw_glob))

    with duckdb.connect(str(DB_PATH)) as con:
        con.execute("BEGIN")
        try:
            if parquet_files:
                sql = SQL_PATH.read_text(encoding="utf-8").replace("__RAW_GLOB__", _escaped_path(raw_glob))
                con.execute(sql)
                input_files = len(parquet_files)
            else:
                _create_empty_staging(con)
                input_files = 0

            output_rows = con.execute("SELECT COUNT(*) FROM neo_typed_staging").fetchone()[0]
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            raise

    elapsed_ms = int((perf_counter() - started) * 1000)
    logger.info(
        "Transform complete. input_files=%s output_rows=%s table=neo_typed_staging db=%s elapsed_ms=%s",
        input_files,
        output_rows,
        DB_PATH,
        elapsed_ms,
    )
    return {
        "input_files": input_files,
        "output_rows": output_rows,
        "table": "neo_typed_staging",
        "db_path": str(DB_PATH),
        "elapsed_ms": elapsed_ms,
    }


def main() -> None:
    run_transform()


if __name__ == "__main__":
    main()
