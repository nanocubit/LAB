# Tiny world fixture

`tiny-world-v1` is a deterministic, six-event fixture for end-to-end semantic checks. It covers temporal visibility, retraction, replacement of a preference, and subject isolation.

- `tiny-world.events.jsonl` is the append-only event stream.
- `tiny-world.queries.json` defines four point-in-time retrieval cases.
- `tiny-world.oracle-notes.json` documents the expected semantic outcomes.

Implementations must evaluate each query using only events for the requested subject whose `occurred_at` is not later than `as_of`, then apply retractions before producing results.
