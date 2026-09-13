# Protocol

## Frozen configuration

- Baseline policy: `frozen-vector-only-v1`
- Candidate policy: `phase-aware-candidate-v1`
- Seed: `17`
- Episodes per policy: `400`
- Candidate exploration rate: `0.1`
- Primary metric: `mean_utility`

## Procedure

1. Run the baseline and candidate with the same frozen configuration.
2. Store each policy's metrics and a BLAKE3 digest of its canonical JSON record.
3. Compute `delta_17 = candidate.mean_utility - baseline.mean_utility`.
4. Store a BLAKE3 digest of the canonical result document.
5. Use `replay.py` to rerun and verify the stored digest.

## Decision rule

The candidate is better in this experiment only if `delta_17 > 0`.

## Scope

This controlled paired comparison removes seed mismatch from the comparison. It
does not estimate performance variability across different seeds.
