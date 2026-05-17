import os
from dataclasses import dataclass
from pathlib import Path

NASA_CLOSE_APPROACH_API = os.getenv(
    "NASA_CLOSE_APPROACH_API",
    "https://ssd-api.jpl.nasa.gov/cad.api",
)
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_STREAM_NAME = os.getenv("REDIS_STREAM_NAME", "neo:stream")
REDIS_CONSUMER_GROUP = os.getenv("REDIS_CONSUMER_GROUP", "neo-raw-writers")
REDIS_CONSUMER_NAME = os.getenv("REDIS_CONSUMER_NAME", "consumer-1")

POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))
READ_BLOCK_MS = int(os.getenv("READ_BLOCK_MS", "5000"))
READ_BATCH_SIZE = int(os.getenv("READ_BATCH_SIZE", "100"))

RAW_DATA_ROOT = os.getenv("RAW_DATA_ROOT", "data/raw")


@dataclass
class RuntimeConfig:
    redis: dict
    nasa_api: dict
    storage: dict
    pipeline: dict


def get_runtime_config() -> RuntimeConfig:
    return RuntimeConfig(
        redis={
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "db": REDIS_DB,
            "stream": REDIS_STREAM_NAME,
            "consumer_group": REDIS_CONSUMER_GROUP,
            "consumer_name": REDIS_CONSUMER_NAME,
            "read_block_ms": READ_BLOCK_MS,
            "read_batch_size": READ_BATCH_SIZE,
        },
        nasa_api={
            "base_url": NASA_CLOSE_APPROACH_API,
            "api_key": NASA_API_KEY,
            "poll_interval_seconds": POLL_INTERVAL_SECONDS,
        },
        storage={
            "raw_data_root": str(Path(RAW_DATA_ROOT)),
        },
        pipeline={
            "poll_interval_seconds": POLL_INTERVAL_SECONDS,
        },
    )
