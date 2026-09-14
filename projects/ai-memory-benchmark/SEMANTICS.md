# AI Memory Benchmark v0.1 Semantics

This document defines the normative logical semantics used by the reference oracle and required of conforming adapters.

## 1. Immutable facts

A canonical event is immutable. No operation may mutate the payload, provenance, confidence, validity interval, relation set, or canonical fields of an already written event.

A replacement assertion is represented by a new claim and an explicit revision relation. A narrowed validity interval is represented by a new claim with the narrowed interval plus a qualifying `revises` or `supersedes` event; it is never an update to the older claim.

## 2. Canonical time

All canonical times are UTC strings ending in `Z`.

For an event `e`:

- `sequence(e)` is strict total canonical log order.
- `timestamp(e)` is logical availability time.
- `observed_at(e)` is source observation time and may precede timestamp.
- `[valid_from(e), valid_to(e)]` is the world-validity interval; null `valid_to` is open-ended.

For all consecutive canonical events, timestamp is non-decreasing by sequence. Every prior event in `previous_event_ids(e)` has lower sequence than `e`.

Event visibility is inclusive:

```text
timestamp(e) <= T
```

Validity begins inclusively:

```text
valid_from(e) <= T
```

Expiry is strict:

```text
expired iff valid_to(e) is not null and valid_to(e) < T
```

Therefore an event with `valid_to == T` is not expired at `T`.

## 3. Structural ancestry and relation direction

`previous_event_ids` forms a DAG. It includes targets of `derived_from`, `revises`, `supersedes`, and `invalidates` relations, but may additionally contain untyped construction prerequisites.

Direction and temporal expectations:

| Relation | Canonical direction | Constraint |
|---|---|---|
| `caused` | cause -> effect | source.valid_from <= target.valid_from |
| `triggered` | trigger -> effect | source.valid_from <= target.valid_from |
| `executed_from` | decision -> action | source.valid_from <= target.valid_from |
| `result_of` | action -> result | source.valid_from <= target.valid_from |
| `based_on` | decision -> claim/evidence | target.valid_from <= source.valid_from |
| `derived_from` | derived -> source | target.valid_from <= source.valid_from |
| `supports` | evidence -> claim | evidence.valid_from <= claim.timestamp or claim.valid_from |
| `corroborates` | evidence/result -> claim | source.valid_from <= claim.timestamp or claim.valid_from |
| `revises` | revision -> claim | target.sequence < source.sequence |
| `supersedes` | revision -> claim | target.sequence < source.sequence |
| `invalidates` | revision/evidence -> claim | target.sequence < source.sequence |

Other relation types require existing targets but do not add a v0.1 temporal inequality beyond general append-only constraints.

## 4. Agent visibility

Let A be a querying agent and T be `as_of`.

\[
Local(A,T) = \{e \mid e.agent\_id = A \land timestamp(e) \le T\}
\]

A handoff is an observation in `Local(A,T)` with:

```text
payload.predicate = received_memory_event
payload.attributes.recipient_agent_id = A
payload.value = an existing event_id
provenance.source_type = agent_handoff
agent_id = recipient_agent_id
entity_id = agent_id
entity_type = agent
```

The received event must appear in `previous_event_ids`; the handoff has exactly one `derived_from` relation to it.

Let `Closure(e)` be e plus all ancestors reachable by `previous_event_ids` and provenance ancestry relations. Closure is filtered by query time:

\[
Closure_T(e) = \{x \in Closure(e) \mid timestamp(x) \le T\}
\]

Directly shared events are targets received through handoff:

\[
DirectShared(A,T) = \{e \mid \exists h \in Handoff(A,T): e.event\_id = h.payload.value\}
\]

The visible event set is:

\[
VisibleEvents(A,T) = Local(A,T) \cup \bigcup_{e \in DirectShared(A,T)} Closure_T(e)
\]

v0.1 handoff mode is `provenance_closure` and transitivity is `explicit_only`. A handoff to A does not make information visible to C without a recipient-authored handoff to C.

Handoff observations are not evidence about the world. They MUST NOT have `supports`, `corroborates`, `weakens`, `contradicts`, `revises`, `supersedes`, or `invalidates` relations; they MUST NOT contribute to support, status resolution, or hybrid relevance ranking.

## 5. Entity scope

A query may declare `entity_scope`.

```text
primary:
  event.entity_id == query.entity_id

referential:
  event.entity_id == query.entity_id
  OR event has direct relation about -> query.entity_id
```

`referential` does not imply traversal through `affects`, `depends_on`, `same_as`, aliases, or any multi-hop graph relation. Q01, Q03, and Q19 default to `primary`; Q17 defaults to `referential`.

## 6. Confidence

Confidence belongs to an event itself and is immutable.

- It is not automatically propagated to claims, decisions, actions, or results.
- It is not rewritten after supporting or contradicting evidence arrives.
- Derived events may have any explicitly generated confidence in `[0,1]`.
- Confidence does not itself equal claim status.

Two positive supports are independent if their `provenance.source_id` values differ and neither is an ancestor of the other in the structural/provenance DAG.

## 7. Support and claim status

For a claim c, agent A, and time T, let V(A,T) equal `VisibleEvents(A,T)`.

\[
Pos(c,A,T) = \{e \in V(A,T) \mid e \xrightarrow{supports|corroborates} c\}
\]

\[
Neg(c,A,T) = \{e \in V(A,T) \mid e \xrightarrow{weakens|contradicts} c\}
\]

\[
Support(c,A,T) = \sum_{e \in Pos(c,A,T)} confidence(e) - \sum_{e \in Neg(c,A,T)} confidence(e)
\]

`revises`, `supersedes`, and `invalidates` do not contribute numerically to Support. They have explicit status effects only when they meet their thresholds.

A revision is status-effective if visible at T and:

```text
invalidates: confidence >= 0.90
revises:     confidence >= 0.70
supersedes:  confidence >= 0.70
```

A sub-threshold revision remains an immutable audit/provenance event but SHALL NOT alter Support or resolved claim status in v0.1.

Let I(c,A,T) be the count of independent positive support events. Status is:

\[
Status(c,A,T) =
\begin{cases}
invalidated, & \exists e \in V(A,T): e \xrightarrow{invalidates} c \land confidence(e) \ge 0.90 \\
superseded, & \exists e \in V(A,T): e \xrightarrow{supersedes|revises} c \land confidence(e) \ge 0.70 \\
expired, & valid\_to(c) \ne null \land valid\_to(c) < T \\
contested, & Support(c,A,T) < 0 \\
confirmed, & Support(c,A,T) \ge 0.50 \land I(c,A,T) \ge 2 \\
active, & otherwise
\end{cases}
\]

Precedence is fixed:

```text
invalidated > superseded > expired > contested > confirmed > active
```

A claim is grounded structurally because all canonical claims MUST have at least one direct positive support or corroboration edge. A grounded claim with one support can remain `active`; it is not automatically confirmed.

A material contradiction is a visible `weakens` or `contradicts` edge with source confidence at least `0.50`. A material invalidation is a visible `invalidates` edge with source confidence at least `0.90`.

## 8. Q03 state delta

Q03 is agent-scoped and compares `State(A, X, T1)` with `State(A, X, T2)` under `epistemic_as_of` semantics. It is not a mutable row diff.

Allowed delta types are:

```text
claim_added
claim_replaced
claim_invalidated
claim_expired
claim_became_contested
claim_became_confirmed
evidence_added
evidence_became_visible_via_handoff
decision_added
action_added
result_added
```

A confidence difference is represented only as a `claim_replaced` record containing old/new claim IDs, old/new immutable confidences, a revision event ID, relation type, and effective time. `confidence_updated`, `record_overwritten`, and `claim_mutated` are invalid delta types.

## 9. Q15 revision impact

For a status-effective revision R targeting a claim C, downstream impact traverses:

```text
based_on_inverse
caused
triggered
executed_from
result_of
```

`based_on_inverse` is used because a canonical decision points to the claim/evidence on which it is based.

\[
ImpactedBy(R,A,T) = \{x \in VisibleEvents(A,T) \mid \exists c: R \rightarrow c \land x \in Descendants_{ImpactEdges}(c)\}
\]

Primary impacted items are only `decision`, `action`, and `result`. Claims and evidence may appear as explanatory nodes. Sub-threshold revisions are excluded from canonical Q15 impact unless a future non-default query explicitly requests them.

Sort impacted items by:

```text
1. shorter impact path
2. earlier timestamp
3. lower sequence
4. lexicographically smaller event_id
```

## 10. Expired claim inclusion

Expired claims remain visible in episodic history. Default `include_expired` behavior is:

| Query range | Default |
|---|---|
| Q01-Q15 | true |
| Q16-Q18 | false |
| Q19 | true |
| Q20 | conditional when material to verification |

Q16-Q18 default to excluding invalidated, superseded, and expired events while retaining contested events with status annotation.

## 11. EvidencePack

Q08 is provenance-oriented. Its required event categories are `claim`, `supporting_evidence`, and `source_provenance`.

Q20 is verification-oriented. It requires `claim`, `supporting_evidence`, and `source_provenance`, plus material contradiction and applicable revision categories when they exist. Temporal and confidence context are required structured fields, not fake event IDs.

An event is admissible for a category only if it satisfies that category's semantic path requirement. The oracle creates a bounded candidate universe for every pack. It finds the exact minimum-cardinality pack:

\[
P^* = \arg\min_{P \subseteq U_q} (|P|, LexicographicIDs(P))
\]

subject to the union of event-category coverage satisfying all required categories.

Candidate-universe bounds are profile configuration. The generator MUST reject or regenerate an instance exceeding those bounds. Ties are resolved by lexicographically sorted event-ID tuple after cardinality.

## 12. Hybrid retrieval

Each Q16-Q18 golden answer has four disjoint classes:

```text
required_ids
relevant_ids
distractor_ids
forbidden_ids
```

`required_ids` is a subset of `relevant_ids`. Relevant items may have grades 1, 2, or 3; required items have grade 3. Distractors have grade 0. Forbidden items are a hard failure even when semantically close.

\[
RequiredRecall@k = \frac{|TopK \cap Required|}{|Required|}
\]

\[
NormalizedPrecision@k = \frac{|TopK \cap Relevant|}{\min(k, |Relevant|)}
\]

\[
ForbiddenHitRate@k = \frac{|TopK \cap Forbidden|}{k}
\]

A forbidden item can intentionally have higher cosine similarity than a required item when it must be excluded by time, status, agent visibility, or entity constraints.

## 13. Deterministic embeddings

`deterministic-hash-384-v1` uses 384-dimensional L2-normalized vectors:

\[
E_{raw}(e) = 0.45E_{entity} + 0.25E_{predicate} + 0.15E_{scenario} + 0.05E_{agent} + 0.05E_{kind} + 0.05E_{noise}
\]

\[
E(e) = E_{raw}(e) / ||E_{raw}(e)||_2
\]

Each component coordinate is generated from SHA-256 over UTF-8 canonical input:

```text
ai-memory-v0.1|component_type|component_value|dimension_block
```

Digest bytes are interpreted as unsigned big-endian 16-bit values, mapped to `[-1, 1]`; enough SHA-256 blocks are concatenated to fill 384 coordinates. The full vector is L2 normalized.

For required items R and ranking distractors D, the generator validates final normalized vectors:

\[
\min_{r \in R} cos(q,r) \ge \max_{d \in D} cos(q,d) + 0.03
\]

If this fails, the generator MUST deterministically regenerate or reject the instance. This margin does not restrict forbidden items.

## 14. Canonical ordering and empty values

For non-ranked event output, canonical event order is:

```text
(entity_id, payload.predicate or '', valid_from, sequence, event_id)
```

For category-based outputs, categories are ordered:

```text
claims, supporting_evidence, contradictory_evidence, revisions,
decisions, actions, results, observations, handoff_explanatory_nodes
```

Ranked retrieval arrays preserve backend rank and are not reordered by the normalizer. EvidencePack ties use cardinality then lexicographically sorted event-ID tuple.

Empty collections are always `[]`; they are never null, omitted, `{}`, or an empty string. An absent optional scalar/object is `null`.

## 15. Seed derivation

Dataset and workload seeds are separate. Protected conformance/performance runs derive a seed from:

```text
digest = HMAC-SHA256(secret, UTF-8(message)).digest()
seed_int = int.from_bytes(digest[0:8], byteorder='big', signed=false)
seed = seed_int & ((1 << 63) - 1)
```

The canonical message is:

```text
ai-memory-v0.1|run_type={conformance|performance}|backend_name={backend_name}|adapter_commit={adapter_commit}|profile={profile}|run_id={run_id}|seed_kind={dataset|workload}
```

Runners SHOULD publish `SHA-256(secret)` before execution and reveal the secret after completion to allow verification that seeds were not retried opportunistically.
