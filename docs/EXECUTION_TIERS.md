# Execution Tiers

## Tier 1 — replay-verified

- `local`: only when run in a pinned container with lockfiles and pinned revision.
- `codespaces`: unified development and review environment.
- `actions`: deterministic automation, CI, replay, and integrity checks.

Tier 1 receipts MUST record container digest, dependency lock, code SHA, input digests, and replay metadata.

## Tier 2 — best-effort

- `colab`: GPU/TPU exploration and visual analysis.
- `kaggle`: external versioned notebook benchmarks.

Tier 2 is an accelerator. It is not final evidence. Access to private LAB from Tier 2 MUST use an immutable export bundle; notebook JSON MUST NOT contain deploy keys or long-lived tokens.

## Cross-tier transfer

```text
Tier 2 receipt -> exported bundle -> Tier 1 replay -> new Tier 1 receipt
```
