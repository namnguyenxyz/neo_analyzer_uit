from __future__ import annotations

from pathlib import Path
from time import perf_counter

import duckdb

from src.analytics.thresholds import describe_hazard_rule
from src.common.logging_utils import get_logger

logger = get_logger(__name__)
DB_PATH = Path("neo_analytics.db")
SQL_PATH = Path(__file__).with_name("sql") / "hazard_classification.sql"


def _table_exists(con: duckdb.DuckDBPyConnection, table_name: str) -> bool:
    row = con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'main' AND table_name = ?",
        [table_name],
    ).fetchone()
    return bool(row and row[0] > 0)


def run_classification() -> dict[str, int | str]:
    started = perf_counter()

    with duckdb.connect(str(DB_PATH)) as con:
        if not _table_exists(con, "neo_typed_staging"):
            raise RuntimeError(
                "Missing required source table 'neo_typed_staging'. "
                "Run python -m src.analytics.transform_raw_to_typed first."
            )

        con.execute("BEGIN")
        try:
            con.execute(SQL_PATH.read_text(encoding="utf-8"))
            total_rows = con.execute("SELECT COUNT(*) FROM neo_hazard_classified").fetchone()[0]
            flagged_rows = con.execute(
                "SELECT COUNT(*) FROM neo_hazard_classified WHERE is_potentially_hazardous"
            ).fetchone()[0]
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            raise

    elapsed_ms = int((perf_counter() - started) * 1000)
    logger.info(
        "Hazard classification complete. rule=%s total_rows=%s flagged_rows=%s db=%s elapsed_ms=%s",
        describe_hazard_rule(),
        total_rows,
        flagged_rows,
        DB_PATH,
        elapsed_ms,
    )
    return {
        "total_rows": total_rows,
        "flagged_rows": flagged_rows,
        "table": "neo_hazard_classified",
        "db_path": str(DB_PATH),
        "elapsed_ms": elapsed_ms,
    }


def main() -> None:
    run_classification()


if __name__ == "__main__":
    main()
