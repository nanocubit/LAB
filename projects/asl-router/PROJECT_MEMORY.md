# ASL-Router Project Memory

## Frozen v0.1 invariants

- Only `ActivePolicySnapshot` may serve.
- Evidence is distinct from Verification.
- Eligibility is target-specific: `Eligibility(e, s, c)`.
- AdaptiveState is distinct from PolicySnapshot.
- Same initial state, events, configuration, projection version, and seed produce the same canonical state.

## Current phase

- Contract frozen.
- Synthetic baseline oracle protocol registered as EXP-ASL-0001.
- Deterministic contextual bandit remains a future replaceable PolicyProjection backend.
