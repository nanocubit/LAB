# Schema contract

`memory_event.schema.json` is the canonical shape contract for v0.1 events. It uses JSON Schema Draft 2020-12.

## Extensibility

The root event object permits additional properties for forward compatibility. `extensions` is the intended namespace for backend/runtime-specific values:

```json
{
  "extensions": {
    "org.toroidaldb": {
      "partition_hint": "agent_0001/device_0042"
    }
  }
}
```

Extension keys SHOULD be reverse-DNS namespaces. Oracle and scorer semantics ignore all extension values. Canonical data MUST NOT encode precomputed answers or backend-specific semantic shortcuts in extensions.

## Strict envelopes

The following canonical envelopes are strict:

- `payload`: fixed envelope plus extensible `payload.attributes`
- `provenance`: fixed envelope plus extensible `provenance.attributes`
- `relation`
- `embedding`

This permits domain-specific scenario attributes without allowing an adapter to change canonical meaning silently.

## Schema versus semantic validation

JSON Schema validates one record's shape. The semantic validator is responsible for cross-record and policy checks, including unique IDs/sequences, monotonic time, UTC intervals, target consistency, ancestry DAG, handoff isolation, revision constraints, claim grounding, causal time, vector norms, and query/golden invariants.

The validator, not JSON Schema, enforces `received_memory_event` payload-value type and target existence because that rule depends on event predicate and the complete dataset.
