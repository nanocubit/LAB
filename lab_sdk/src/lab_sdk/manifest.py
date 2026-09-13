from __future__ import annotations
from pathlib import Path
import json

REQUIRED = {"schema_version", "experiment_id", "primary_project", "evidence_level", "status", "hypothesis_id", "protocol_version", "code", "environment", "parameters", "verification"}

def validate_manifest_object(value: dict) -> list[str]:
    errors = [f"missing required field: {name}" for name in sorted(REQUIRED - set(value))]
    if value.get("evidence_level") not in {"spike", "registered", "replay_verified", "agent_reproduced", "human_verified"}:
        errors.append("invalid evidence_level")
    if value.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    return errors

def validate_manifest_path(path: str) -> list[str]:
    p=Path(path)
    try:
        import yaml  # type: ignore
        value=yaml.safe_load(p.read_text())
    except ImportError:
        value=json.loads(p.read_text())
    return validate_manifest_object(value)
