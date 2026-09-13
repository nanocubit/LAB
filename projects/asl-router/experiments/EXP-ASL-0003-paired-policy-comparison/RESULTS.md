# Results

**Status:** PENDING EXECUTION

No outcome is recorded until `run.py` has been executed in the project runtime
and the produced artifact has been replay-verified.

## Preregistered decision rule

`phase-aware-candidate-v1` is better for this experiment only when:

```text
delta_17 = candidate.mean_utility - baseline.mean_utility > 0
```

## Interpretation boundary

A completed result applies only to the synthetic condition configured with
`seed=17` and `episodes=400`.
