from __future__ import annotations

import json
import math
import unicodedata
from typing import Any

try:
    import blake3
except ImportError:
    blake3 = None


def normalize(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int)):
        return value

    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("LAB-C14N/1 forbids non-finite float values")
        return 0.0 if value == 0 else value

    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]

    if isinstance(value, dict):
        return {
            str(key): normalize(item)
            for key, item in value.items()
            if item is not None
        }

    raise TypeError(f"unsupported canonical type: {type(value)!r}")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        normalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    if blake3 is None:
        raise RuntimeError("BLAKE3 is required for replay-capable evidence")

    return "blake3:" + blake3.blake3(
        canonical_json_bytes(value)
    ).hexdigest()
