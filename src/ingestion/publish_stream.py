import json
from datetime import date, datetime, timezone
from typing import Any

from redis import Redis

from src.common.config import get_runtime_config
from src.common.logging_utils import get_logger
from src.ingestion.fetch_nasa_neos import fetch_close_approach_records

logger = get_logger(__name__)


def _build_event_id(record: dict[str, Any]) -> str:
    object_id = str(record.get("object_id", "unknown"))
    close_date = str(record.get("close_approach_date", "unknown-date"))
    fetched_at = str(record.get("fetched_at_utc", ""))
    try:
        epoch = int(datetime.fromisoformat(fetched_at).timestamp())
    except ValueError:
        epoch = int(datetime.now(timezone.utc).timestamp())
    return f"{object_id}:{close_date}:{epoch}"


def publish_records_to_stream(records: list[dict[str, Any]]) -> tuple[int, int]:
    cfg = get_runtime_config()
    client = Redis(
        host=cfg.redis["host"],
        port=cfg.redis["port"],
        db=cfg.redis["db"],
        decode_responses=True,
    )

    success = 0
    failed = 0

    for record in records:
        try:
            event_id = _build_event_id(record)
            message = {
                "event_id": event_id,
                "object_id": str(record.get("object_id", "")),
                "close_approach_date": str(record.get("close_approach_date", "")),
                "payload_json": json.dumps(record, ensure_ascii=True),
                "fetched_at_utc": str(record.get("fetched_at_utc", "")),
            }
            client.xadd(cfg.redis["stream"], message)
            success += 1
        except Exception as exc:  # noqa: BLE001
            failed += 1
            logger.error("Failed to publish event %s: %s", record.get("object_id"), exc)

    return success, failed


def main() -> None:
    today = date.today().isoformat()
    records = fetch_close_approach_records(today, today)
    published, failed = publish_records_to_stream(records)
    logger.info(
        "Producer run complete. published=%s failed=%s stream=neo:stream",
        published,
        failed,
    )


if __name__ == '__main__':
    main()
