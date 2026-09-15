"""Deterministic reference oracle for event-sourced memory fixtures."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _event_key(event: dict[str, Any]) -> tuple[datetime, str]:
    return (_parse_timestamp(event["occurred_at"]), event["event_id"])


def active_memories(
    events: Iterable[dict[str, Any]], subject_id: str, as_of: str
) -> list[dict[str, Any]]:
    """Return active memories for one subject at a point in time."""
    cutoff = _parse_timestamp(as_of)
    visible = [
        event
        for event in events
        if event["subject_id"] == subject_id
        and _parse_timestamp(event["occurred_at"]) <= cutoff
    ]
    visible.sort(key=_event_key)

    state: dict[str, dict[str, Any]] = {}
    for event in visible:
        memory_id = event["memory_id"]
        if event["event_type"] == "memory_upsert":
            state[memory_id] = event
        elif event["event_type"] == "memory_retract":
            state.pop(memory_id, None)
        else:
            raise ValueError(f"Unsupported event_type: {event['event_type']}")

    return [state[memory_id] for memory_id in sorted(state)]


def active_memory_ids(
    events: Iterable[dict[str, Any]], subject_id: str, as_of: str
) -> list[str]:
    return [event["memory_id"] for event in active_memories(events, subject_id, as_of)]
