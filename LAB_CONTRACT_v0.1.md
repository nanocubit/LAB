# LAB Contract v0.1

**Status:** draft for first commit  
**Ratified:** pending D-001  
**Profile:** LAB-C14N/1

## 0. Purpose

`nanocubit/LAB` is a research operating system for a solo researcher working with bounded, auditable agent executors across multiple projects. LAB preserves reproducibility, lineage, evidence, and curated memory independently of replaceable compute backends.

LAB is a stack of contracts, not merely a monorepo.

## 1. Core invariants

**I1 — Replaceable compute, durable evidence.** Local, Codespaces, Actions, Colab, and Kaggle are replaceable. Evidence, lineage, contracts, experiments, decisions, and curated memory are durable.

**I2 — Agent output is not evidence.** Agent output MUST remain a claim until replay and digest validation in a Tier 1 environment.

**I3 — Human merge is promotion.** Agents MUST operate only on namespaced branches. Human review and merge into `main` is the sole promotion event.

**I4 — Verified Evidence is not Curated Memory.** Verified evidence is necessary but insufficient for `MEMORY.md`. A Decision (ADR) and human-reviewed PR are additionally REQUIRED.

**I5 — Layer subordination.** Layer N MUST NOT violate the contract of layer N-1. Execution MUST NOT create an artifact without a manifest; verification MUST NOT approve evidence without digest validation; memory MUST NOT update without verification, ADR, and human promotion; governance MUST NOT be bypassed by an agent.

**I6 — Machine-readable, schema-versioned, canonical.** Every persisted object MUST declare `schema_version`, use LAB-C14N/1 canonicalization, and use BLAKE3-256 where supported by the implementation.

**I7 — Receipts are mandatory.** Every run MUST emit a receipt referencing inputs and outputs by digest. No receipt means no evidence.

**I8 — Agent boundary.** An agent MAY propose, execute in its allowlist, emit receipts, and open namespaced branches. An agent MUST NOT write `main`, edit curated memory, change governance, or silently promote evidence, policy, or architecture.

**I9 — Immutability after registration.** Registered manifests are immutable except permitted transitions. Receipts are immutable. `DECISIONS.md` is append-only. Corrections MUST be additive or superseding.

**I10 — Canonicalization before digest.** A digest has semantic meaning only over LAB-C14N/1 canonical payload. Raw file hashes are storage digests, not evidence digests.

## 2. Layer model

```text
6. Governance      budgets, allowlists, secret policy
5. Memory          MEMORY.md, DECISIONS.md, lineage graph
4. Evidence        artifacts, receipts, digests
3. Verification    replay, conformance, integrity
2. Execution       local, Codespaces, Actions, Colab, Kaggle
1. Contract        schemas, manifests, LAB SDK
```

## 3. Evidence chain

```text
Hypothesis -> preregistered Protocol -> registered Experiment -> Run receipt
-> canonical Artifact -> Tier-1 Replay -> evidence level -> ADR
-> human-reviewed PR -> MEMORY.md
```

```text
Eligibility != Promotion
Candidate != Active
Verified Evidence != Curated Memory
```

## 4. Execution and evidence

Evidence levels are defined in `docs/EVIDENCE_LEVELS.md`. Execution tiers are defined in `docs/EXECUTION_TIERS.md`. Tier 2 outputs from Colab or Kaggle MUST NOT exceed `registered` evidence level until exported and replayed in Tier 1.

## 5. Agents, concurrency, and cost

Executor identity and reproduction levels are defined in `docs/AGENT_IDENTITY_AND_REPRODUCTION.md`. `agent_reproduced` requires independence level L3 or L4.

```text
Experiment branch: experiment/<project>/<experiment-id>/<slug>
Agent branch:      agent/<role>/<task-id>/<slug>
Run directory:     projects/<project>/experiments/<experiment>/runs/<receipt-id>/
```

Each experiment MUST use an experiment branch until human merge. Self-reported LLM cost is telemetry, not a hard-enforced budget measurement.

## 6. Immutability and evolution

Immutability is defined in `docs/IMMUTABILITY_POLICY.md`. Schema evolution is defined in `docs/SCHEMA_EVOLUTION.md`. Canonicalization is defined in `schemas/canonicalization.md`.

## 7. Amendment

Contract amendments REQUIRE a human-reviewed PR and ADR. Agents MAY propose amendments but MUST NOT ratify them.
