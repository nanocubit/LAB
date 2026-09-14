# Reference implementation boundary

The reference implementation has three logically separate roles.

```text
oracle/     Builds golden answers from canonical data and private scenario annotations.
scoring/    Compares a backend result to a golden answer without private annotations.
validator/  Validates canonical datasets, query instances, manifests, and output contracts.
```

## Isolation rule

The oracle may access private scenario metadata needed to determine intended causal chains, candidate EvidencePack universes, and generated query truth. The scorer MUST NOT access hidden scenario metadata, raw oracle state, generator-private annotations, backend internals, or external databases.

The scorer receives only query instance, public benchmark configuration, backend canonical result, and golden answer. This separation prevents it from repairing incomplete backend output with oracle knowledge.

## Reference is not a competitive backend

The initial reference implementation is expected to be an in-memory Python evaluator. It is a semantic oracle, diagnostic tool, and golden generator. Its performance is non-comparable.

## Required tests

1. Schema tests.
2. Semantic validator tests.
3. Oracle self-consistency tests.
4. Scorer tests.
5. Property tests.
6. Targeted negative-adapter tests.
