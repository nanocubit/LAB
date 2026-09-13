# Immutability Policy

Corrections MUST use new objects or superseding events, never rewrite an existing canonical record.

| Field | Before `registered` | After `registered` | After `complete` |
|---|---|---|---|
| `status` | allowed | declared transitions only | only `superseded` |
| `code.revision` | allowed | `null -> SHA` only | forbidden |
| `verification.expected_result_digest` | allowed | `null -> digest` only | forbidden |
| `parameters`, `dataset`, `protocol_version` | allowed | forbidden | forbidden |

Receipts are immutable from creation. `DECISIONS.md` is append-only. Artifact payloads referenced by receipts are immutable.

CI MUST block modifications of existing receipts, rewrites of existing decisions, forbidden manifest mutations, and protocol edits without a version bump. A human override requires ADR and labeled PR.
