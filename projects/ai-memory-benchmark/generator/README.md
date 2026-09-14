# Generator contract

The generator creates deterministic canonical worlds and workloads; it never obtains truth from a backend.

## Inputs

Generation is parameterized by benchmark version, generator version/commit, profile, scenario configuration, dataset seed, workload seed, and embedding profile.

`dataset_seed` generates entities, event identities, timestamps, causal/provenance topology, confidences, validity intervals, and embeddings. `workload_seed` generates Q01-Q20 bindings, targets, `as_of` boundaries, retrieval partitions, and public/holdout assignment.

## Determinism

Identical complete inputs MUST produce byte-identical canonical output: event order, IDs, timestamps, vectors, queries, manifests, and checksums. Serialization uses UTF-8 JSONL, stable field/relation ordering, UTC times, stable numeric formatting, and no platform-dependent RNG behavior.

## Hybrid generation

Cosine constraints are checked on final normalized vectors. Instances that violate required-versus-ranking-distractor margin or forbidden-exclusion rules are deterministically rejected or regenerated.

## Profiles

```text
tiny: hand-authored inspectable semantic fixture
smoke: 10K events, fixed public development seed
small: 100K events
medium: 1M events
large: 10M events
```

## Manifest

Each corpus records version, git commit, dirty state, dataset/workload seeds, profile, counts, embedding profile, scenario mix, public/holdout split, and SHA-256 checksums.
