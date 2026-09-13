# Hypothesis

Under the preregistered synthetic condition with `seed=17` and `episodes=400`,
`phase-aware-candidate-v1` has strictly higher `mean_utility` than
`frozen-vector-only-v1`.

The primary estimand is:

```text
delta_17 = mean_utility(candidate, seed=17) - mean_utility(baseline, seed=17)
```

The hypothesis is supported only when `delta_17 > 0`. This is a claim about
the fixed synthetic condition at seed 17, not a claim of cross-seed superiority.
