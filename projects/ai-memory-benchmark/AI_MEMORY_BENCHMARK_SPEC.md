# AI Memory Benchmark Specification v0.1

## 1. Status and normative language

This document is the normative contract for AI Memory Benchmark v0.1. The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

`SEMANTICS.md` is part of this specification. Where implementation guidance conflicts with `SEMANTICS.md`, the normative semantics prevail.

## 2. Scope

AI Memory Benchmark evaluates event-sourced memory systems for AI agents. It measures semantic correctness first and performance second. The benchmark is backend-neutral: it does not prescribe SQL, Cypher, TQL, storage layout, index type, deployment topology, or a mutable current-state table.

A conforming backend MUST consume canonical facts and answer canonical query instances without reading oracle-private metadata or golden answers.

## 3. Core model

A canonical dataset is an append-only log of immutable `MemoryEvent` records. Each record has an event identity, logical availability time, world-validity interval, owning agent, primary entity, kind, payload, provenance, confidence, prior-event links, typed graph relations, deterministic embedding, and extensions.

```text
Disk stores facts.
State(A, T) = f(VisibleEvents(A, T)).
```

A backend MAY materialize indexes, closure tables, snapshots, or caches, but all such materializations MUST be equivalent to the reference semantics for every valid query input and MUST be reported in its architecture profile.

## 4. Event kinds

The v0.1 canonical `kind` enum is fixed:

```text
observation
evidence
claim
decision
action
result
revision
```

No event is updated in place. Corrections, revised validity, changed confidence, or replacement assertions are represented by new events and explicit relations.

## 5. Canonical event contract

The canonical JSON Schema is `schema/memory_event.schema.json`.

Required logical fields are:

```text
event_id, world_id, sequence
timestamp, observed_at, valid_from, valid_to
agent_id, entity_id, entity_type
kind, payload, provenance, confidence
previous_event_ids, relations, embedding, extensions
```

The root event object is extensible for forward compatibility. `extensions` is the explicit vendor/runtime namespace. Canonical nested envelopes are strict, with domain-specific attributes carried through their `attributes` maps.

Only canonical fields affect oracle and golden-answer semantics. Extensions MUST NOT affect benchmark semantics, directly or indirectly.

## 6. Time and identity

All canonical time fields MUST use UTC canonical form ending in `Z`:

```text
timestamp
observed_at
valid_from
valid_to
as_of
from
to
effective_at
```

`sequence` defines strict total log order. `timestamp` is logical availability/ingestion time and MUST be non-decreasing by sequence. `observed_at` may be earlier than timestamp. `valid_from` and `valid_to` describe a world-validity interval; `valid_to = null` means open-ended or unknown.

`event_id` and `entity_id` belong to different identity domains. `entity_id` MUST NOT equal an event ID. Event references use `target_type = event`; entity references use `target_type = entity`.

## 7. Relations

The canonical relation vocabulary is:

```text
about
observed_by
derived_from
extracted_from
supports
corroborates
weakens
contradicts
revises
supersedes
invalidates
based_on
caused
triggered
executed_from
result_of
affects
depends_on
mentions
same_as
```

All relations are directed and carry their source in the enclosing event. Relation direction and temporal constraints are defined in `SEMANTICS.md`.

`result_of` reads as the role of the target: `action -> result_of -> result` means the target is the result of the source action.

## 8. Structural ancestry

`previous_event_ids` is structural ancestry. It forms a directed acyclic graph and contains only prior event IDs. For every event E, it MUST include targets of `derived_from`, `revises`, `supersedes`, and `invalidates` relations. It MAY include additional construction prerequisites that have no typed relation.

A semantic validator MUST reject self-reference, missing targets, targets with sequence not lower than the source sequence, and cycles.

## 9. Agent visibility and handoff

An agent sees locally authored events and explicitly received handoffs. A handoff is an `observation` whose `agent_id` is the recipient; its payload predicate is `received_memory_event`; its value is an existing event ID; and it contains `derived_from` to that received event.

v0.1 uses provenance-closure handoff visibility and explicit-only transitivity. A recipient receives the target event plus its temporal provenance closure. Knowledge does not automatically transit through other agents without another explicit recipient-authored handoff.

Handoff observations are visibility/audit events only. They MUST NOT participate in support, contradiction, revision, status resolution, or hybrid semantic relevance scoring.

## 10. Confidence and status

Confidence is an immutable attribute of its own event. It is not automatically inherited, propagated, recalculated, or written back to another event.

Claim status is a derived function of visible positive/negative evidence, effective revisions, and expiry. v0.1 statuses are:

```text
active
confirmed
contested
expired
superseded
invalidated
```

The status function, revision thresholds, independent-support rule, and precedence are defined in `SEMANTICS.md`.

Every canonical `claim` MUST have at least one direct `supports` or `corroborates` relation from an evidence, observation, or result event. A handoff cannot ground a claim.

## 11. Dataset generation

Generation MUST be deterministic from the complete configuration, including benchmark version, generator version, profile, dataset seed, workload seed, embedding profile, and scenario configuration.

The dataset seed generates entities, events, graph/provenance, timestamps, confidences, and embeddings. The workload seed generates query bindings, `as_of` values, public/holdout assignment, and retrieval candidate classes.

Public development datasets use fixed reviewed seeds. Holdout conformance and performance workloads use independently derived seeds and keep golden answers outside the adapter-visible workspace.

A manifest MUST record generator version, git commit, dirty state, both seeds, embedding profile, checksums, dataset/workload sizes, and public/holdout split. Dirty state is a warning locally and a failure in CI, conformance, and performance runs.

## 12. Deterministic embeddings

v0.1 uses `deterministic-hash-384-v1`, not a learned external embedding model. The profile is specified in `SEMANTICS.md` and MUST define byte-level component generation, component weights, dimensionality, and L2 normalization.

Hybrid query generation MUST validate cosine constraints on final normalized vectors. The generator MUST deterministically reject or regenerate an instance that violates required margins.

## 13. Canonical query classes

v0.1 defines twenty canonical templates:

| ID | Class | Template |
|---|---|---|
| Q01 | Temporal | `agent_knowledge_as_of` |
| Q02 | Temporal | `facts_later_refuted` |
| Q03 | Temporal | `state_delta` |
| Q04 | Temporal | `validity_interval_lookup` |
| Q05 | Provenance | `claim_provenance` |
| Q06 | Evidence | `evidence_support_set` |
| Q07 | Provenance | `source_trace` |
| Q08 | Evidence | `minimal_evidence_pack` |
| Q09 | Graph/Causality | `decision_rationale` |
| Q10 | Graph/Causality | `action_causal_history` |
| Q11 | Graph/Causality | `outcome_consequences` |
| Q12 | Graph/Causality | `cross_agent_handoff` |
| Q13 | Revision | `active_vs_superseded_claims` |
| Q14 | Revision | `contradiction_clusters` |
| Q15 | Revision | `revision_impact_analysis` |
| Q16 | Hybrid retrieval | `time_confidence_semantic_retrieval` |
| Q17 | Hybrid retrieval | `entity_scoped_hybrid_retrieval` |
| Q18 | Hybrid retrieval | `causal_semantic_retrieval` |
| Q19 | Reconstruction | `reconstruct_agent_memory_state` |
| Q20 | Verification | `verification_evidence_pack` |

Query contracts MUST explicitly identify agent scope, time scope, knowledge mode, entity scope where applicable, result contract, and default inclusion of expired claims.

Q01, Q03, and Q19 use `entity_scope = primary` by default. Q17 uses `entity_scope = referential`, which means primary entity match or one direct `about -> entity` relation; it does not include `affects`, `depends_on`, aliases, or arbitrary graph expansion.

## 14. Golden answers and oracle

The reference oracle computes golden answers from canonical data and private scenario annotations. Golden answers are typed structured outputs, not prose judgments.

The oracle MAY use hidden metadata. The scorer MUST NOT read hidden metadata, raw oracle state, or generator-private annotations. It may consume only query contract, public benchmark configuration, a backend result, and the corresponding golden answer.

Public golden changes MUST be reviewed in source control; CI MUST NOT silently commit regenerated goldens.

## 15. Correctness scoring

Scoring uses result-contract-specific metrics, including event precision/recall, status accuracy, edge F1, path recall, reachability, groundedness, EvidencePack coverage/minimality, required recall at k, normalized precision at k, NDCG, forbidden hit rate, and state equivalence.

A backend MUST pass correctness thresholds before performance data is considered comparable. Exact thresholds are versioned with each workload profile.

Hybrid retrieval uses four disjoint item classes: `required_ids`, `relevant_ids`, `distractor_ids`, and `forbidden_ids`, with `required_ids` a subset of `relevant_ids`. A forbidden hit is a hard failure.

## 16. Performance protocol

Performance reports MUST separate ingest/index build, cold queries, warm queries, single-query latency, concurrency, resource use, and storage size. Shared GitHub-hosted runners MAY provide diagnostic timing but MUST NOT support comparative performance claims. Comparable latency requires a pinned self-hosted environment profile.

## 17. Architectural cost

Every backend report MUST publish an architecture profile. At minimum it reports services, storage artifacts, indexes/materializations, schema objects, adapter LOC, query round trips, manual setup steps, dual-write requirement, storage amplification, RAM amplification, build duration, and startup readiness.

No single architecture score is normative in v0.1.

## 18. Conformance and anti-gaming

Public tiny data is for inspection and development. Smoke and larger conformance workloads support public/holdout query splits. Holdout golden answers MUST NOT be committed or exposed to adapter jobs.

Dataset and workload seeds are distinct. For protected conformance/performance runs, seed derivation uses HMAC-SHA256 as specified in `SEMANTICS.md`; runners SHOULD publish a pre-run SHA-256 commitment and reveal the run secret after completion.

The benchmark MUST include targeted negative adapters that independently ignore revisions, visibility, temporal `as_of`, provenance, hybrid filtering, or EvidencePack minimality. Their expected failure profiles validate scorer sensitivity.

## 19. Adapter contract

Each backend adapter MUST implement prepare/load/warmup/execute/collect-metrics/teardown behavior and return canonical normalized JSON results. It MUST NOT hard-code public event/query IDs, inspect goldens, read hidden metadata, mutate canonical inputs, or use unreported query-specific preprocessing.

See `adapters/README.md`.

## 20. Versioning and non-goals

Breaking semantic changes require a new benchmark version and reviewed golden corpus. v0.1 deliberately excludes learned embeddings, automatic confidence propagation, implicit agent replication, mutable authoritative current state, memory capacity, forgetting/decay, distributed consistency, and LLM-based correctness judging.
