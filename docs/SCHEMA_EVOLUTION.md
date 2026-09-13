# Schema Evolution

1. Every persisted object MUST declare `schema_version`.
2. Versions remain readable after they cease being writable.
3. Breaking semantic changes require a new major version.
4. Additive fields SHOULD be optional with defaults.
5. Existing immutable objects MUST NOT be rewritten in place.
6. Migration MUST create a derived migration record that references the source digest.
7. Replay MUST use original schema semantics, or explicitly report `replay_incompatible`.
8. Schema changes REQUIRE human-reviewed PR, SDK reader updates, and golden-vector updates where canonicalization is affected.

Version form is `major.minor`. Old semantic readers are part of replay support; a new reader MUST NOT silently reinterpret an older object under new semantics.
