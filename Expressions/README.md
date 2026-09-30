# Expressions

A planned production library of **3,000–5,000 reusable Japanese expression families** for Koto.

An expression family groups socially or functionally related casual, neutral, polite, and formal forms. Ordinary compositional sentences, inflection-only variants, dialogue lines, responses, and substitution results do not inflate the family count.

## Current state

The repository contains the publication scaffold, schemas, source policy, review policy, one non-production design example, 5,000 non-production JMdict source candidates, and one source-backed reviewed family. The candidates were selected from 13,065 current eligible expression-tagged entries in the 30 September 2026 JMdict snapshot. The production manifest intentionally reports zero families because the reviewed family still requires independent human Japanese-language sign-off. No record may be placed in a production pack or labelled `verified` until every review gate passes.

## Files

- `manifest.json` — versioned production inventory and pack integrity metadata.
- `source-registry.json` — eligible, conditional, and excluded source policy.
- `review-policy.json` — publication gates and Koto Difficulty 1–5 definitions.
- `schema/` — JSON Schemas for manifests, candidates, packs, and expression families.
- `examples/` — non-production examples used to exercise the schema and card design.
- `candidates/` — immutable source-derived editorial work queues; never loaded by the learner-facing app.
- `editorial/` — accept, reject, split, and merge decisions connecting candidates to families.
- `reviewed/` — rich families that passed source-backed editorial review but still await independent human sign-off.
- `audit/` — reproducibility, source-snapshot, and extraction-count reports.
- `packs/` — verified production packs; intentionally empty until final publication review is complete.

## Runtime rules

Koto downloads an immutable release manifest and compressed packs into a session-only temporary cache. It validates version, size, schema, count, and SHA-256 metadata before use. Personal Recognised/Review state and Vocabulary links remain in Koto's account database and are never published here.

## Audio

No recorded audio is stored. Koto uses device Japanese text-to-speech for primary forms, variants, responses, follow-ups, and dialogue lines.
