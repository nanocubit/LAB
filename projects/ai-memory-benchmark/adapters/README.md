# Backend adapter contract

An adapter maps one backend to canonical data and query contracts. It may use any physical schema, index, language, topology, or materialization, provided results are semantically equivalent to the reference definitions.

## Lifecycle

```python
prepare(dataset_path: str, run_config: dict) -> None
load() -> dict
warmup(query_instances: list[dict]) -> None
execute(query_instance: dict) -> dict
collect_metrics() -> dict
teardown() -> None
```

## Restrictions

An adapter MUST NOT read goldens or private oracle metadata, hard-code event/query IDs, mutate canonical datasets, use unreported query-specific preprocessing, use a non-equivalent mutable current state, or use extensions as semantic truth.

## Canonical result

```json
{
  "instance_id": "Q09-0001",
  "query_id": "Q09",
  "backend": {"name": "backend-name", "version": "backend-version", "configuration_hash": "sha256-or-null"},
  "result": {},
  "execution": {"latency_ns": 0, "backend_query_count": 0, "result_bytes": 0}
}
```

Required empty collections are `[]`; ranked arrays preserve rank.

## Architecture profile

Report services, artifacts, indexes/materializations, schema objects, adapter LOC excluding tests/generated code, median round trips, manual setup, dual-write, storage/RAM amplification, build duration, and startup readiness. Declare closure indexes, reverse edges, snapshots, vector indexes, and reachability materializations.

## Intended implementation order

```text
reference Python
SQLite plus sqlite-vec or FAISS
DuckDB plus Parquet/JSON
ToroidalDB
PostgreSQL plus pgvector
specialist/multi-store stacks
```

Correctness, performance, and architecture remain separate; v0.1 has no single winner score.
