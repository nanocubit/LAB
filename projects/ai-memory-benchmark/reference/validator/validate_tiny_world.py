"""Validate the tiny-world fixture against the reference oracle."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from reference.oracle.engine import active_memory_ids


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def validate() -> list[str]:
    fixtures = ROOT / "fixtures"
    events = load_jsonl(fixtures / "tiny-world.events.jsonl")
    queries = json.loads(
        (fixtures / "tiny-world.queries.json").read_text(encoding="utf-8")
    )["queries"]

    errors: list[str] = []
    event_ids = [event["event_id"] for event in events]
    query_ids = [query["query_id"] for query in queries]

    if len(event_ids) != len(set(event_ids)):
        errors.append("event_id values must be unique")
    if len(query_ids) != len(set(query_ids)):
        errors.append("query_id values must be unique")

    ordered_events = sorted(
        events, key=lambda event: (_parse_timestamp(event["occurred_at"]), event["event_id"])
    )
    previously_upserted: set[tuple[str, str]] = set()
    for event in ordered_events:
        key = (event["subject_id"], event["memory_id"])
        if event["event_type"] == "memory_upsert":
            previously_upserted.add(key)
        elif event["event_type"] == "memory_retract":
            if key not in previously_upserted:
                errors.append(
                    f"retraction targets memory without prior upsert: {event['memory_id']}"
                )
        else:
            errors.append(f"unsupported event type: {event['event_type']}")

    for query in queries:
        actual = active_memory_ids(events, query["subject_id"], query["as_of"])
        expected = query["expected_memory_ids"]
        if actual != expected:
            errors.append(
                f"{query['query_id']}: expected {expected}, computed {actual}"
            )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("tiny-world validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("tiny-world validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
