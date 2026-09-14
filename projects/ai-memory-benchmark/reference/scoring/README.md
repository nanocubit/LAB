# Scorer contract

The scorer compares a normalized backend result with a golden answer and is deliberately separated from the oracle.

## Allowed inputs

A scorer may read only the query instance, golden answer, backend canonical result, and public benchmark configuration. It MUST NOT read hidden scenario metadata, generator-private annotations, raw oracle state, adapter filesystem state, or an external backend.

## Comparison modes

| Result type | Comparison |
|---|---|
| Semantic event set | Precision, recall, F1, required-item checks |
| Ordered non-ranked list | Canonical normalized order |
| Ranked retrieval | RequiredRecall@k, NormalizedPrecision@k, NDCG@k, ForbiddenHitRate@k |
| Graph edges | Canonical edge-set precision/recall/F1 |
| Causal paths | Requirement satisfaction, path recall, node reachability |
| Claim state | Status accuracy and temporal correctness |
| State snapshot | State equivalence |
| EvidencePack | Coverage, admissibility, exact cardinality, tie-break order |

Forbidden hybrid-retrieval hits are hard failures. Performance is non-comparable if the required correctness gate fails.

## Normalization

The normalizer may sort semantic sets according to canonical rules. It MUST NOT reorder ranked results, invent omitted nodes/edges, infer provenance, or repair backend output from a golden answer. Required empty collections are `[]`; missing required fields are contract errors.

## Negative adapters

The scorer suite contains targeted mutants: ignore revisions, visibility, `as_of`, provenance, hybrid filters, or EvidencePack minimality. Each has an expected failure profile.
