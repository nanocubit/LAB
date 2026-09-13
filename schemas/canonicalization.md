# LAB-C14N/1 Canonicalization Profile

**Status:** normative  
**Digest algorithm:** BLAKE3-256

## Rules

- Text MUST be UTF-8 without BOM, Unicode NFC, LF line endings, and no trailing whitespace.
- JSON MUST follow RFC 8785 JSON Canonicalization Scheme (JCS).
- NaN, positive infinity, negative infinity, timezone-naive timestamps, and locale-dependent formats are forbidden.
- Negative zero MUST normalize to zero.
- Timestamps MUST be UTC ISO 8601 with microseconds and trailing `Z`.
- UUIDs MUST be lowercase hyphenated strings.
- Digests MUST be lowercase, algorithm-prefixed strings such as `blake3:<hex>`.
- Monetary fields MUST be decimal strings, not binary floats.
- Absent optional fields MUST NOT be serialized as `null`.

## Binary artifacts

```text
storage_digest = BLAKE3-256(raw bytes)
```

Storage digest proves byte integrity, not semantic equivalence.

## Tabular artifacts

Parquet and CSV MUST expose two digests:

```text
storage_digest  = BLAKE3-256(raw file bytes)
semantic_digest = BLAKE3-256(canonical logical table)
```

The logical table includes declared schema, declared column order, row ordering policy, nullability, and typed values. For v0.1, tables without a primary key MUST explicitly declare insertion-order preservation.

## Bundles

A bundle digest is calculated by sorting payload paths byte-wise and hashing path length, NFC UTF-8 path bytes, and each raw file digest. Filesystem metadata MUST NOT affect the digest.

## Versioning

Every persisted object SHOULD declare `c14n_profile: LAB-C14N/1`. Any semantic change requires a new profile version and golden-vector update.
