# AI Memory Benchmark v0.1

AI Memory Benchmark is a database-agnostic, reproducible benchmark for event-sourced AI-agent memory systems.

## Purpose

The benchmark evaluates whether a memory backend can reconstruct what a particular agent knew at a particular time, trace evidence and provenance, explain decisions and actions, resolve revisions and contradictions, and retrieve relevant memory under simultaneous semantic, temporal, trust, graph, and agent-visibility constraints.

It is not a vector-search leaderboard. A backend is useful only when its answers are correct under the benchmark semantics; latency is reported after the correctness gate passes.

The core principle is:

```text
Disk stores facts.
State(A, T) = f(CanonicalFactsVisible(A, T)).
```

Canonical facts are immutable. A current state, claim status, decision rationale, or memory snapshot is derived from the event log rather than stored as an authoritative mutable record.

## Project boundary

This project is hosted in LAB because LAB owns the neutral workload, reference oracle, scorer, datasets, and cross-backend comparisons. ToroidalDB is a first-class adapter, but it does not own benchmark semantics or golden answers.

```text
LAB defines the question.
A backend adapter implements one answer.
```

ToroidalDB should retain its adapter and a pinned tiny-fixture regression in its own repository. Cross-backend runs, public corpus governance, and benchmark releases belong here.

## v0.1 scope

v0.1 models immutable events of these kinds:

```text
observation
evidence
claim
decision
action
result
revision
```

It defines temporal visibility, explicit cross-agent handoff, provenance closure, claim-status resolution, contradiction/revision behavior, causal traversal, deterministic synthetic embeddings, EvidencePack construction, and twenty canonical query templates.

v0.1 does not model automatic confidence propagation, probabilistic belief fusion, implicit replication, mutable current-state records, learned embeddings, bounded context windows, forgetting, memory eviction, distributed consistency, or LLM-as-judge scoring.

## Layout

```text
AI_MEMORY_BENCHMARK_SPEC.md  Normative benchmark contract
SEMANTICS.md                 Normative temporal, visibility, status, and query semantics
schema/                      Versioned canonical schemas
generator/                   Deterministic world and workload generation
fixtures/                    Hand-authored inspectable tiny world
reference/                   Oracle, scorer, and validator boundaries
adapters/                    Backend-neutral adapter contract
runners/                     GitHub Actions and benchmark-run instructions
reports/                     Correctness, performance, architecture, and gap reports
datasets/                    Generated public datasets; not hand-authored state
golden/                      Public reviewed golden answers
```

## Delivery sequence

1. Freeze Phase 0 documents, schema, and contracts.
2. Hand-author a tiny world with all semantic boundary cases.
3. Implement an in-memory Python reference oracle.
4. Produce and manually inspect tiny-world golden answers.
5. Add property tests, a semantic validator, and targeted negative adapters.
6. Freeze `v0.1.0-normative`.
7. Implement deterministic generation and public 10K smoke data.
8. Implement neutral baselines: reference Python, SQLite plus vector support, and DuckDB.
9. Implement the ToroidalDB adapter.
10. Add PostgreSQL plus pgvector and specialist multi-store profiles.
11. Run comparable performance only on pinned self-hosted hardware through GitHub Actions.

## GitHub Actions policy

GitHub Actions is the control plane for reproducibility and governance.

- Pull requests run schema, fixture, oracle/scorer, property, and negative-adapter checks when implemented.
- Public smoke runs use committed, reviewed deterministic data and goldens.
- Holdout goldens never enter an adapter-visible workspace.
- Shared GitHub-hosted runners are valid for correctness and diagnostic timing, not comparative latency claims.
- Performance runs are dispatched to pinned self-hosted runners and include a complete environment profile.

See `runners/README.md` for the execution tiers.
