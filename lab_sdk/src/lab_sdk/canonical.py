from __future__ import annotations

import hashlib
import json
import math
import unicodedata
from decimal import Decimal
from typing import Any


def _normalize(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, bool) or isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("LAB-C14N/1 forbids non-finite floats")
        return 0 if value == 0 else value
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, list):
        return [_normalize(x) for x in value]
    if isinstance(value, tuple):
        return [_normalize(x) for x in value]
    if isinstance(value, dict):
        return {unicodedata.normalize("NFC", str(k)): _normalize(v) for k, v in value.items() if v is not None}
    raise TypeError(f"unsupported canonical type: {type(value)!r}")


def canonical_json_bytes(value: Any) -> bytes:
    normalized = _normalize(value)
    return json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest_bytes(payload: bytes) -> str:
    # BLAKE3 is the LAB normative target. SHA-256 fallback preserves deterministic operation
    # in a zero-dependency bootstrap environment and is explicitly labeled.
    try:
        import blake3  # type: ignore
        return "blake3:" + blake3.blake3(payload).hexdigest()
    except ImportError:
        return "sha256-fallback:" + hashlib.sha256(payload).hexdigest()


def digest_json(value: Any) -> str:
    return digest_bytes(canonical_json_bytes(value))
