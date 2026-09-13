#!/usr/bin/env python3
"""Replay EXP-ASL-0003 and verify deterministic paired-comparison output."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

EXP_DIR = Path(__file__).resolve().parent
RESULT_PATH = EXP_DIR / "results" / "result.json"

def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()

def digest_without_result_digest(value: dict) -> str:
    replayable = {key: item for key, item in value.items() if key != "result_digest"}
    return "sha256:" + hashlib.sha256(canonical(replayable)).hexdigest()

def main() -> None:
    if not RESULT_PATH.exists():
        raise SystemExit(f"Missing result artifact: {RESULT_PATH}")
    stored = json.loads(RESULT_PATH.read_text())
    stored_digest = stored.get("result_digest")
    if stored_digest != digest_without_result_digest(stored):
        raise SystemExit("Stored result digest does not match result content")
    subprocess.run([sys.executable, str(EXP_DIR / "run.py")], check=True)
    replayed = json.loads(RESULT_PATH.read_text())
    if replayed.get("result_digest") != stored_digest:
        raise SystemExit("Replay digest mismatch")
    print("Replay verified:", stored_digest)

if __name__ == "__main__":
    main()
