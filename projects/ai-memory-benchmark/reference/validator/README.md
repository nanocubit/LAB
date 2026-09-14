# Validator contract

The validator has structural and semantic layers.

## Structural validation

Structural validation applies JSON Schema to every event and later validates query/golden/manifest schemas.

## Semantic validation

Dataset-wide invariants include:

- unique event IDs and sequences;
- non-decreasing timestamps by sequence and UTC canonical time;
- valid intervals;
- existing, type-correct targets;
- separate entity/event identity domains;
- prior-only, acyclic `previous_event_ids`;
- typed ancestry inclusion;
- relation temporal constraints;
- revision relation requirements;
- direct positive grounding for each claim;
- confidence range;
- 384-dimensional deterministic embeddings and norm tolerance;
- recipient-authored handoffs;
- handoff isolation from support/revision/status;
- hybrid relevance partition invariants;
- bounded exact EvidencePack candidate universes.

## Handoff checks

For `payload.predicate == received_memory_event`:

```text
payload.value matches ^evt_[A-Za-z0-9_-]+$ and exists
agent_id == payload.attributes.recipient_agent_id
entity_id == agent_id
entity_type == agent
provenance.source_type == agent_handoff
provenance.source_id == payload.attributes.sender_agent_id
previous_event_ids contains payload.value
relations contains exactly one derived_from -> payload.value
relations contain no evidence/revision/status relations
```

## CI policy

A dirty generator tree is a local warning and CI failure. Diagnostics are machine-readable and include invariant ID, source, target, and remediation context.
