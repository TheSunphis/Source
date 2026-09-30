# Expressions

A planned production library of **3,000–5,000 reusable Japanese expression families** for Koto.

An expression family groups socially or functionally related casual, neutral, polite, and formal forms. Ordinary compositional sentences, inflection-only variants, dialogue lines, responses, and substitution results do not inflate the family count.

## Current state

The repository currently contains the publication scaffold, schemas, source policy, review policy, and one non-production design example. The production manifest intentionally reports zero families. No record may be placed in a production pack or labelled `verified` until it passes the required provenance, licensing, deduplication, difficulty, naturalness, and social-use reviews.

## Files

- `manifest.json` — versioned production inventory and pack integrity metadata.
- `source-registry.json` — eligible, conditional, and excluded source policy.
- `review-policy.json` — publication gates and Koto Difficulty 1–5 definitions.
- `schema/` — JSON Schemas for manifests and expression families.
- `examples/` — non-production examples used to exercise the schema and card design.
- `packs/` — production packs; intentionally empty until review is complete.

## Runtime rules

Koto downloads an immutable release manifest and compressed packs into a session-only temporary cache. It validates version, size, schema, count, and SHA-256 metadata before use. Personal Recognised/Review state and Vocabulary links remain in Koto's account database and are never published here.

## Audio

No recorded audio is stored. Koto uses device Japanese text-to-speech for primary forms, variants, responses, follow-ups, and dialogue lines.
