from datetime import datetime
from pathlib import Path


def resolve_partition_path(base_dir: str, approach_date: str) -> Path:
    parsed = datetime.fromisoformat(approach_date)
    return (
        Path(base_dir)
        / f"year={parsed.year:04d}"
        / f"month={parsed.month:02d}"
        / f"day={parsed.day:02d}"
    )


def ensure_partition_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def build_parquet_file_path(base_dir: str, approach_date: str) -> Path:
    partition = resolve_partition_path(base_dir, approach_date)
    ensure_partition_dir(partition)
    return partition / "neo_data.parquet"
