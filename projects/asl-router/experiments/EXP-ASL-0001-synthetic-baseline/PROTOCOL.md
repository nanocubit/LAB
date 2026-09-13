# Protocol — EXP-ASL-0001

Run 400 deterministic synthetic episodes with seed 7. The oracle has four hidden phases:

- A: `vector_only` is optimal.
- B: `hybrid` is optimal.
- C: `hybrid_rerank` is optimal for graph-like, evidence-heavy queries.
- D: `hybrid` has a small advantage under freshness/budget pressure.

The frozen policy executes `vector_only`. Record utility and oracle regret by phase. This experiment does not promote an ASL policy; it registers the baseline required for future adaptive comparison.
