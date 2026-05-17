import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd
from redis import Redis

from src.common.config import get_runtime_config
from src.common.logging_utils import get_logger
from src.storage.parquet_layout import build_parquet_file_path

logger = get_logger(__name__)


def _dedupe_by_event_id(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for record in records:
        event_id = str(record.get("event_id", ""))
        if event_id:
            deduped[event_id] = record
    return list(deduped.values())


def _append_parquet(file_path: Path, records: list[dict[str, Any]]) -> None:
    frame = pd.DataFrame(records)
    if file_path.exists():
        previous = pd.read_parquet(file_path)
        frame = pd.concat([previous, frame], ignore_index=True)
    frame.to_parquet(file_path, index=False)


def _parse_stream_entries(entries: list[tuple[str, dict[str, str]]]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for _, fields in entries:
        try:
            payload = json.loads(fields.get("payload_json", "{}"))
        except json.JSONDecodeError:
            logger.warning("Skipping malformed payload_json")
            continue

        payload["event_id"] = fields.get("event_id", "")
        payload["close_approach_date"] = fields.get(
            "close_approach_date", payload.get("close_approach_date", "")
        )
        parsed.append(payload)

    return parsed


def consume_stream_forever() -> None:
    cfg = get_runtime_config()
    client = Redis(
        host=cfg.redis["host"],
        port=cfg.redis["port"],
        db=cfg.redis["db"],
        decode_responses=True,
    )

    stream = cfg.redis["stream"]
    last_id = "$"
    batch_size = int(cfg.redis["read_batch_size"])
    block_ms = int(cfg.redis["read_block_ms"])
    raw_root = cfg.storage["raw_data_root"]

    logger.info("Starting stream consumer for %s", stream)

    while True:
        results = client.xread({stream: last_id}, count=batch_size, block=block_ms)
        if not results:
            continue

        for _, entries in results:
            parsed = _parse_stream_entries(entries)
            records = _dedupe_by_event_id(parsed)

            by_partition: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for record in records:
                approach_date = str(record.get("close_approach_date", ""))
                if not approach_date:
                    continue
                by_partition[approach_date].append(record)

            for approach_date, partition_records in by_partition.items():
                parquet_path = build_parquet_file_path(raw_root, approach_date)
                _append_parquet(parquet_path, partition_records)
                logger.info(
                    "Wrote %s rows to %s",
                    len(partition_records),
                    parquet_path,
                )

            if entries:
                # Acknowledge point for xread-style processing is advancing last seen ID.
                last_id = entries[-1][0]
                logger.info("Advanced stream ack cursor to %s", last_id)


if __name__ == '__main__':
    consume_stream_forever()
