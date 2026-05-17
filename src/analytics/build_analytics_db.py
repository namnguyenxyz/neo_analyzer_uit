from __future__ import annotations

import argparse
from pathlib import Path
from time import perf_counter

import duckdb

from src.analytics.classify_hazard import run_classification
from src.analytics.transform_raw_to_typed import run_transform
from src.common.logging_utils import get_logger

logger = get_logger(__name__)
DB_PATH = Path("neo_analytics.db")
SERVING_SQL_PATH = Path(__file__).with_name("sql") / "serving_views.sql"


def _apply_serving_views() -> dict[str, int]:
    with duckdb.connect(str(DB_PATH)) as con:
        con.execute("BEGIN")
        try:
            con.execute(SERVING_SQL_PATH.read_text(encoding="utf-8"))
            view_count = con.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.views
                WHERE table_schema = 'main'
                AND table_name IN ('v_neo_latest', 'v_pha_counts', 'v_closest_approach_today')
                """
            ).fetchone()[0]
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            raise
    return {"view_count": view_count}


def run_build(rebuild: bool = False) -> dict[str, int | str]:
    started = perf_counter()

    if rebuild and DB_PATH.exists():
        DB_PATH.unlink()

    transform_stats = run_transform()
    classify_stats = run_classification()
    serving_stats = _apply_serving_views()

    elapsed_ms = int((perf_counter() - started) * 1000)
    logger.info(
        "Analytics DB build complete. db=%s typed_rows=%s flagged_rows=%s views=%s elapsed_ms=%s",
        DB_PATH,
        transform_stats["output_rows"],
        classify_stats["flagged_rows"],
        serving_stats["view_count"],
        elapsed_ms,
    )

    return {
        "db_path": str(DB_PATH),
        "typed_rows": transform_stats["output_rows"],
        "flagged_rows": classify_stats["flagged_rows"],
        "view_count": serving_stats["view_count"],
        "elapsed_ms": elapsed_ms,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build analytics DuckDB artifact for NEO-Light")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Drop existing neo_analytics.db before rebuilding derived tables and views.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    run_build(rebuild=args.rebuild)


if __name__ == "__main__":
    main()
