from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reference.oracle.engine import active_memory_ids
from reference.validator.validate_tiny_world import validate


def load_events() -> list[dict]:
    path = ROOT / "fixtures" / "tiny-world.events.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def load_queries() -> list[dict]:
    path = ROOT / "fixtures" / "tiny-world.queries.json"
    return json.loads(path.read_text(encoding="utf-8"))["queries"]


def load_golden_answers() -> dict[str, dict]:
    path = ROOT / "golden" / "tiny-world.answers.json"
    answers = json.loads(path.read_text(encoding="utf-8"))["answers"]
    return {answer["query_id"]: answer for answer in answers}


def test_fixture_is_semantically_valid() -> None:
    assert validate() == []


def test_queries_match_reference_oracle() -> None:
    events = load_events()
    for query in load_queries():
        assert active_memory_ids(events, query["subject_id"], query["as_of"]) == query["expected_memory_ids"]


def test_golden_answers_match_queries() -> None:
    golden_answers = load_golden_answers()
    for query in load_queries():
        assert golden_answers[query["query_id"]]["memory_ids"] == query["expected_memory_ids"]


def test_retraction_hides_dark_mode() -> None:
    events = load_events()
    assert "mem-003" in active_memory_ids(events, "user:maya", "2026-01-04T11:59:59Z")
    assert "mem-003" not in active_memory_ids(events, "user:maya", "2026-01-04T12:00:00Z")


def test_subject_isolation() -> None:
    events = load_events()
    assert "mem-005" not in active_memory_ids(events, "user:maya", "2026-01-06T15:00:00Z")
