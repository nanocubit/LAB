from __future__ import annotations

def validate_receipt_object(value: dict) -> list[str]:
    required={"schema_version", "receipt_id", "experiment_id", "executor", "backend", "inputs", "outputs", "status"}
    errors=[f"missing required field: {x}" for x in sorted(required-set(value))]
    if value.get("schema_version") != "1.0": errors.append("schema_version must be 1.0")
    return errors
