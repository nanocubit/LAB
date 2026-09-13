# ASL Contract v0.1

## Serving boundary

```text
AdaptiveState -> PolicyProjection -> CandidatePolicy -> PromotionGate
-> ApprovedPromotionDecision -> PolicySnapshotStore.activate()
-> ActivePolicySnapshot -> ServingRouter
```

Only `ActivePolicySnapshot` MAY serve. `AdaptiveState`, `CandidatePolicy`, Evidence, Verification, EligibilityDecision, and PolicyProjection MUST NOT hold serving capability.

## Core rules

- `Evidence != Verification`.
- `Verified(e) != Eligible(e, s, c)`.
- `AdaptiveState != PolicySnapshot`.
- Updates are scoped, evidence-lined, reversible, and replayable.
- Promotion is explicit; serving never follows a state update implicitly.
- A frozen baseline remains executable.

The v0.1 reference action space is `vector_only`, `bm25_only`, `hybrid`, and `hybrid_rerank`. TTT, LoRA, RL, neural adaptation, and automatic global promotion are outside v0.1.
