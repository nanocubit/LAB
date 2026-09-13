# Protocol

## Objective

Evaluate a deterministic context-rule candidate policy under the preregistered
synthetic evaluation protocol. The policy may use only observable `Context`
fields and must not access `SyntheticWorld.utilities`, `optimal_action`, or
`oracle_utility` when selecting an action.

## Fixed parameters

- Seed: `17`
- Episodes: `400`
- Exploration rate: `0.1`
- Maximum runtime: `10` minutes
- Maximum cost: `0.00` USD
- Maximum memory: `8` GB
- Digest algorithm: `blake3`

## Context rules

When not exploring, select the action from observable query type:

- `semantic` → `vector_only`
- `mixed` → `hybrid`
- `graph_like` → `hybrid_rerank`
- `time_sensitive` → `hybrid`
- `evidence_requirement: strict` overrides the query-type rule and selects
  `hybrid_rerank`.

Exploration is deterministic. For each tick, derive the decision and exploratory
action from SHA-256 of the fixed seed, context fields, tick, and purpose. It must
not use global random state or oracle utilities.

## Execution

```bash
python run.py
python replay.py
```

The run writes canonical JSON artifacts to `artifacts/`:

- `trace.json`
- `metrics.json`
- `artifact-manifest.json`

The replay reads `artifact-manifest.json` and verifies its `result_digest`
against a fresh execution with the preregistered seed, episode count, and
exploration rate.

## Integrity requirements

- Preserve all declared parameters and resource constraints.
- Do not modify this protocol after execution.
- Record a receipt and result digest before changing the experiment status from
  `planned` to `completed`.
- Create a new experiment for any material change to the policy, data,
  parameters, scoring, or evaluation procedure.
