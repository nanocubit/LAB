# Reference oracle contract

The oracle is the only component that computes golden answers. It evaluates normative semantics over canonical events and may consult private scenario annotations. It MUST NOT call a backend adapter to establish truth.

## Inputs and outputs

Inputs: canonical events, entities/relations where present, query instance, public configuration, and private scenario metadata. Outputs: typed canonical JSON golden answers; never LLM-generated prose.

## Implementation conventions

### Entity scope

Query instances carry `entity_scope` where applicable:

```text
primary      event.entity_id == entity_id
referential  primary match OR direct about -> entity_id
```

Defaults are Q01/Q03/Q19 `primary` and Q17 `referential`. No implicit `affects`, `depends_on`, alias, or k-hop expansion is allowed.

### Structural and typed ancestry

`previous_event_ids` is the structural DAG. `derived_from` is typed provenance. `previous_event_ids(E)` contains targets of `derived_from`, `revises`, `supersedes`, and `invalidates`; it may contain additional prerequisites.

### Serialization

Non-ranked event outputs sort by:

```text
(entity_id, payload.predicate or '', valid_from, sequence, event_id)
```

Category output uses category order in `SEMANTICS.md`, then that key. Ranked retrieval preserves rank. Graph edges and paths are canonicalized. Empty collections are `[]`; absent optional scalars/objects are `null`.

### Handoff

Handoffs are recipient-authored visibility/audit records, not evidence. They are excluded from status resolution and retrieval ranking.

## Tiny world first

The first oracle target is the hand-authored tiny fixture. Every non-trivial semantic rule must be observable through at least one Q01-Q20 golden before large-scale generation begins.
