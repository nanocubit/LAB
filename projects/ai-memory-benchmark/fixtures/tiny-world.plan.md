# Tiny world plan

## Purpose

The tiny world is a hand-authored executable specification. It must remain human-readable and exercise each v0.1 boundary before large-scale generation or backend comparisons.

## Size target

```text
target events: 180-260
hard minimum: 120
hard maximum: 350
agents: 2
entities: 8-12
scenarios: 10-14
```

Coverage matters more than event count. Do not add random filler.

## Required conditions

| Condition | Minimum | Observable through |
|---|---:|---|
| Agents | 2 | Q01, Q12, Q19 |
| Entities | 8-12 | Q01, Q17, Q19 |
| Cross-agent handoff chains | 3 | Q12, Q19 |
| Sub-threshold revisions | 2 | Q13, Q15 audit behavior |
| Effective revisions | 2 | Q02, Q13, Q15 |
| Expired claims | 2 | Q01, Q03, Q04, Q13, Q19 |
| Low-confidence supersede plus expiry | 1 | Q13: expired, not superseded |
| One-support grounded claim | 1 | Q13: active |
| Two independent supports | 1 | Q13: confirmed |
| Negative support dominates | 1 | Q06, Q13: contested |
| Invalidated semantic distractor | 1 | Q16-Q18 forbidden filter |
| Not-visible-at-T distractor | 1 | Q16-Q18 visibility filter |
| Handoff distractor | 1 | Q16-Q18 exclusion from ranking |
| Causal chains | 10 | Q09-Q11 lengths 1, 2, 3, 5 |
| Late observations | 2 | Q04 boundaries |
| `valid_to == as_of` | 1 | Q04: not expired |
| Multi-entity events | 2 | Q17 primary vs referential |
| Claim replacement | 1 | Q03 `claim_replaced` |
| Effective impact path | 1 | Q15 |

## Query minimums

| Query | Minimum | Boundary |
|---|---:|---|
| Q01 | 3 | primary; pre-handoff; post-handoff |
| Q02 | 2 | future invalidation; historical expiry |
| Q03 | 3 | replacement; expiry; handoff delta |
| Q04 | 2 | validity boundary; late observation |
| Q05 | 1 | multi-hop provenance |
| Q06 | 2 | positive and negative support |
| Q07 | 1 | multi-source trace |
| Q08 | 2 | exact minimum; lexical tie |
| Q09 | 2 | single and alternate rationale paths |
| Q10 | 2 | 3+ hop history |
| Q11 | 2 | downstream results |
| Q12 | 3 | before receipt; after receipt; explicit relay |
| Q13 | 4 | active, confirmed, contested, expired/superseded/invalidated |
| Q14 | 1 | contradiction cluster |
| Q15 | 2 | effective and inert revisions |
| Q16 | 3 | invalidated, invisible, handoff distractors |
| Q17 | 2 | referential scope; expiry filter |
| Q18 | 2 | causal neighborhood plus rank |
| Q19 | 3 | pre/post handoff; historical expiry |
| Q20 | 2 | material contradiction; effective revision |

Target: 42-46 tiny golden instances.

## Authoring sequence

1. Define entities and agents.
2. Write causal chains and ancestry by hand.
3. Add revisions, expiry boundaries, and handoffs.
4. Validate structure and semantics.
5. Write Q01-Q20 bindings.
6. Implement oracle.
7. Generate and inspect every golden answer.
8. Add fixture-to-query traceability.
9. Add property and mutation tests.

## Prohibited shortcuts

- Never correct an event by editing it.
- Never grant cross-agent visibility without a receipt event.
- Never use a handoff as evidence or retrieval candidate.
- Never hide fixture semantics solely in private oracle metadata.
- Never accept an unexplained golden answer.
