# Expressions

A planned production library of **3,000–5,000 reusable Japanese expression families** for Koto.

An expression family groups socially or functionally related casual, neutral, polite, and formal forms. Ordinary compositional sentences, inflection-only variants, dialogue lines, responses, and substitution results do not inflate the family count.

## Current state

The repository contains the publication scaffold, schemas, source policy, review policy, one non-production design example, 5,000 non-production JMdict source candidates, deterministic triage coverage for all 5,000, and 60 verified families spanning Koto Difficulty 1–5. The candidates were selected from 13,065 current eligible expression-tagged entries in the 30 September 2026 JMdict snapshot. Eighty-nine candidates have committed family assignments and seven have explicit non-assignment dispositions. The automated priority route is fully reviewed: all 77 records have either an assignment (74) or a documented non-publication outcome (3). Every verified family passed source-backed editorial review and a separate disclosed AI Japanese-language review. The complete 3,000–5,000-family dataset is still under construction and `productionReady` remains false.

## Files

- `manifest.json` — versioned production inventory and pack integrity metadata.
- `source-registry.json` — eligible, conditional, and excluded source policy.
- `review-policy.json` — publication gates and Koto Difficulty 1–5 definitions.
- `schema/` — JSON Schemas for manifests, candidates, packs, and expression families.
- `examples/` — non-production examples used to exercise the schema and card design.
- `candidates/` — immutable source-derived editorial work queues; never loaded by the learner-facing app.
- `triage/` — deterministic automation aids covering every candidate; scores and routes are not editorial decisions or verification.
- `editorial/` — accept, reject, split, defer, and merge records plus batch-review audits; family assignments live in `decisions/` and standalone non-publication judgments live in `outcomes/`.
- `reviewed/` — rich families that passed source-backed review but still await a separate disclosed language-proficiency sign-off.
- `audit/` — reproducibility, source-snapshot, and extraction-count reports.
- `packs/` — checksummed packs containing families whose record-level verification gates are complete.

## Runtime rules

Koto downloads an immutable release manifest and compressed packs into a session-only temporary cache. It validates version, size, schema, count, and SHA-256 metadata before use. Personal Recognised/Review state and Vocabulary links remain in Koto's account database and are never published here.

## Audio

No recorded audio is stored. Koto uses device Japanese text-to-speech for primary forms, variants, responses, follow-ups, and dialogue lines.
