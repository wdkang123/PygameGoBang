"""JSON utilities."""

import json
from typing import Any


def pretty_dumps(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)
