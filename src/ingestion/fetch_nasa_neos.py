import json
import random
import time
from datetime import datetime, timezone
from typing import Any

import requests

from src.common.config import get_runtime_config
from src.common.logging_utils import get_logger

logger = get_logger(__name__)


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_record(raw_row: list[Any]) -> dict[str, Any]:
    # JPL CAD row order follows the API docs and can vary by fields parameter.
    object_id = str(raw_row[0]) if len(raw_row) > 0 else ""
    object_name = str(raw_row[1]) if len(raw_row) > 1 else ""
    close_approach_date = str(raw_row[3]) if len(raw_row) > 3 else ""
    relative_velocity_km_s = _safe_float(raw_row[7] if len(raw_row) > 7 else None)
    miss_distance_au = _safe_float(raw_row[4] if len(raw_row) > 4 else None)

    # CAD endpoint does not always include diameter, keep nullable fallback.
    estimated_diameter_m = _safe_float(raw_row[10] if len(raw_row) > 10 else None)

    return {
        "object_id": object_id,
        "object_name": object_name,
        "close_approach_date": close_approach_date,
        "relative_velocity_km_s": relative_velocity_km_s,
        "miss_distance_au": miss_distance_au,
        "estimated_diameter_m": estimated_diameter_m,
        "source_payload": json.dumps(raw_row, ensure_ascii=True),
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def fetch_close_approach_records(start_date: str, end_date: str) -> list[dict[str, Any]]:
    cfg = get_runtime_config()
    session = requests.Session()

    params = {
        "date-min": start_date,
        "date-max": end_date,
        "sort": "date",
    }

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            response = session.get(cfg.nasa_api["base_url"], params=params, timeout=30)

            if response.status_code == 429 or 500 <= response.status_code < 600:
                raise requests.HTTPError(
                    f"Transient status code {response.status_code}",
                    response=response,
                )

            response.raise_for_status()
            payload = response.json()
            data_rows = payload.get("data", [])
            normalized = [_normalize_record(row) for row in data_rows]
            logger.info(
                "Fetched %s records from NASA CAD between %s and %s",
                len(normalized),
                start_date,
                end_date,
            )
            return normalized

        except (requests.RequestException, ValueError, KeyError) as exc:
            if attempt == max_attempts:
                logger.error("NASA fetch failed after %s attempts: %s", max_attempts, exc)
                raise

            backoff = (2 ** (attempt - 1)) + random.uniform(0, 0.5)
            logger.warning(
                "NASA fetch attempt %s/%s failed (%s). Retrying in %.2fs",
                attempt,
                max_attempts,
                exc,
                backoff,
            )
            time.sleep(backoff)

    return []
