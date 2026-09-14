# Fixtures

Fixtures are small version-controlled, human-readable corpora that make semantics observable. They are not performance datasets.

## Tiny world

The first fixture is hand-authored before the generator exists:

```text
tiny-world.events.jsonl
tiny-world.queries.json
tiny-world.golden.json
tiny-world.README.md
```

Each non-trivial semantic choice maps to a query instance and expected assertion.

## Traceability

`tiny-world.README.md` will contain:

| Fixture condition | Event IDs | Query instance | Expected assertion |
|---|---|---|---|
| Example | `evt_...` | `Q13-...` | status is expired, not superseded |

Tiny fixtures and goldens are public development artifacts; holdout begins with smoke and larger profiles.
