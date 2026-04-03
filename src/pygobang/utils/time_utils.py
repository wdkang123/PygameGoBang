"""Time utilities."""

import time


def get_timestamp_ms() -> int:
    return int(time.time() * 1000)
