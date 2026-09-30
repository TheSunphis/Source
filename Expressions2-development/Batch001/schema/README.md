# Expressions2 Contract Set

All contracts use JSON Schema Draft 2020-12 and reject unknown object properties unless a field explicitly permits a map.

## Schemas

- `source-registry.schema.json` — source licence, permissions, roles, approval, and pinned snapshot identity
- `snapshot-manifest.schema.json` — exact acquired bytes and licence notice identity
- `source-evidence.schema.json` — source-safe normalized evidence store
- `evidence-build-manifest.schema.json` — deterministic compressed evidence artifacts, counts, hashes, and contamination verdict
- `raw-candidate.schema.json` — pre-normalization extraction output
- `candidate.schema.json` — normalized candidate authority
- `family-ledger.schema.json` — append-only merge/split/reject/quarantine/accept decisions
- `family.schema.json` — complete editorial family, Library data, and Full Family Card content
- `form-analysis.schema.json` — complete tappable analysis and bidirectional Vocabulary-link enumeration
- `provenance.schema.json` — field-level derivation, source snapshots, compiler, critic, and review identity
- `compiler-manifest.schema.json` — exact Batch 001 release, pack, input, count, and determinism contract
- `audit-manifest.schema.json` — 100% commissioning audit contract
- `runtime-library-index.schema.json` — compact 100-family searchable Library index
- `runtime-family-card.schema.json` — complete family plus exact analysis set
- `common.schema.json` — shared IDs, evidence, spoken lines, and review definitions

## Invariants beyond JSON Schema

`../tools/validate_contracts.py` also checks constraints that JSON Schema cannot reliably express:

- exactly one primary form;
- hero/Library/primary-form identity;
- dynamic form totals;
- exact Japanese and reading reconstruction from analysis segments;
- contiguous spans;
- one bidirectional Vocabulary enumeration per segment;
- exact family ↔ analysis bijection;
- append-only ledger sequence and hash chain;
- unique IDs/slugs/artifact paths;
- class and Difficulty totals summing to 100;
- four family and analysis packs;
- exactly 25 runtime families per pack;
- dynamic category, family, and form totals;
- acquisition URLs for every source approved for snapshot.

## Contract fixtures

`../fixtures/contracts/positive/` contains 14 synthetic valid documents. `../fixtures/contracts/negative/` contains a corresponding required-field failure for each top-level data schema. Synthetic fixture text is not candidate or family content.

Run:

```bash
python3 work/expressions2/tools/run_contract_tests.py
python3 work/expressions2/tools/run_evidence_tests.py
```
