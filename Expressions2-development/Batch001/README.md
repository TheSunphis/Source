# Expressions2 Clean-Room Workspace

This workspace holds the from-scratch Koto Expressions replacement while the legacy public release remains operational.

## Safety boundary

Nothing beneath this directory is loaded by current Koto runtime routes. No file here may modify public Source, `expression_progress`, Koto backups, or standalone packages.

## Authorities

- `DECISIONS.md` — approved planning decisions
- `schema/` — strict JSON contracts
- `source-registry/` — source permission and snapshot identities
- `snapshots/` — small persisted snapshot metadata; large raw downloads remain temporary and reproducible
- `evidence/` — deterministic compressed evidence stores derived only from pinned approved snapshots
- `candidates/` — raw and normalized clean-room candidates
- `ledger/` — stable IDs and family-boundary decisions
- `compiled/` — candidate family/analysis/runtime artifacts
- `audits/` — deterministic and editorial audit manifests
- `preview/` — private synthetic-account preview only
- `fixtures/` — positive and deliberately invalid contract examples
- `tools/` — isolated validation and build tools; Stage 1 uses the already-available `jsonschema 4.26.0` and installs nothing

## Batch 001 target

Mine at least 2,000 normalized candidates and continue through the ranked queue until exactly 100 complete families pass. Every accepted family needs a complete Library Result Tile, Full Family Card, and complete analysis for every displayed primary/alternate form.

## Legacy prohibition

Tools in this workspace must reject imports from:

- `src/data/expressions/`
- current/legacy public Expressions packs
- former sentence-analysis assets
- legacy `expression:` IDs
- learner `expression_progress`

The supplied screenshots and old family text define product behaviour only; they are not data inputs.

## Current checkpoint

Stages 1–3 passed: contracts/guards are validated, seven exact source snapshots are pinned, and seven deterministic private evidence stores contain 423,088 records. Raw source archives were deleted after verification. No candidate or family exists.

Metadata-only validation command when private payloads are absent:

```bash
EXPRESSIONS2_EVIDENCE_MODE=metadata-only python3 work/expressions2/tools/run_contract_tests.py
```

Durable development storage belongs under the non-live `Expressions2-development/Batch001/` path in `TheSunphis/Source`; the live `Expressions/` tree remains untouched.