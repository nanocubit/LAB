# Protocol

## Objective

Evaluate the `phase_aware_candidate` routing policy under the preregistered
synthetic evaluation protocol.

## Fixed parameters

- Seed: `17`
- Episodes: `400`
- Maximum runtime: `10` minutes
- Maximum cost: `0.00` USD
- Maximum memory: `8` GB
- Digest algorithm: `blake3`

## Candidate policy

- Early-phase weight: `0.7`
- Late-phase weight: `0.3`
- Exploration rate: `0.1`

## Execution requirements

- Run the entrypoint `asl_router.experiments.phase_aware_candidate`.
- Preserve the declared parameters and constraints.
- Record generated metrics and trace artifacts under `artifacts/`.
- Record a receipt and result digest before changing the experiment status from
  `planned` to `completed`.
- Do not alter this protocol after execution; create a follow-up experiment for
  any material protocol change.
