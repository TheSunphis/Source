# Crow1 due — review and directly repair all 49 Cards

- Exact agent: `Crow1`
- Assignment: `germinal-crow1-review-repair-49-1`
- Launch state: `ACTIVE`
- Scope: `49` Cards
- Role: independent reviewer **and direct repairer**
- Public report: `Germinal/Crow/Crow1/report.md`

Crow is not limited to suggesting fixes. Inspect every Card, apply every repair you can substantiate, rerun validation, and return the corrected full 49-record batch. Do not leave ordinary linguistic, dialogue, segment, form, punctuation, boilerplate, or evidence-boundary defects for Zero, Valkyrie, or the user. Quarantine only a specific Card that cannot be made safe and accurate from the available material.

The user will not mediate Card-by-Card disputes. There is no back-and-forth with Valkyrie. Your output is one bounded, corrected batch.

## Inputs

Seed material:
- Release `401235338`; bytes `8302`
- SHA-256 `ae5587937a6c1baa588ecf1ab1b3920c58857a4fe8a1aecba8747ab687864870`

Valkyrie batch to review and repair:
- Release `401239153`; asset `germinal-valkyrie1-complete-49-v1.tar.gz`; bytes `36357`
- SHA-256 `9b45fcf8be8c2f67efa823eabe478fad8613dc15d32c2ab41c8b7f3c04dd7e1e`
- Records `49`; Valkyrie submitted/quarantined `47/2`

Accepted quality exemplar:
- Compiled Card release `401125726`
- Full prototype release `401210597`

## Required work per Card

Review and, where needed, rewrite:

1. meaning and intentions;
2. specific usage, register, cautions, and relationships;
3. Japanese naturalness;
4. whether each Response actually responds to the target expression;
5. whether each Follow-up naturally continues it;
6. coherent three-or-more-turn dialogue order and meanings;
7. complete, accurate surface-covering segmentation for every displayed Japanese line;
8. evidence boundaries: source anchor versus original editorial teaching;
9. genuine searchable Forms rather than duplicate filler;
10. duplicated boilerplate, doubled punctuation, or generic rationales.

Preserve exact Card IDs and direct JMdict anchors. Keep every `selectedVocabularyId` null. Do not invent source attestation, Commonness, CEFR, JF, or JLPT claims. Use Koto Difficulty only.

Add a `crowReview` object to each record with:
- nine gate booleans after repair;
- `repairsApplied`: concrete JSON pointers and short repair descriptions;
- `finalRationale`: why the resulting Card passes or remains quarantined.

A corrected Card must have `publicationStatus: candidate-complete`. A quarantine must identify its exact unresolved fact and why direct repair was unsafe.

## Validator and output

- Tool: `Germinal/batch49/crow_repair_49_tool.py`
- Tool SHA-256: `577cd989ba4edb2a1bb7df11671f9d4f488fb7f974d339e2d5ffbdd4932da09a`
- Tool version: `germinal-crow-repair-49-tool-v1`
- Manifest format: `germinal-crow-repair-49-output-v1`
- Assignment: `germinal-crow1-review-repair-49-1`
- Files: `manifest.json`, `records.ndjson`
- Bundle: `germinal-crow1-reviewed-repaired-49-v1.tar.gz`
- Private release title: `germinal-crow1-review-repair-49-1`

Run `self-test`, then validate and package the corrected records. Use Zero’s upload core at commit `5eccc8e4c768bce21ff00398cb172f97617d3f24`, SHA-256 `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`.

The safe report must include reviewed, repaired, candidate-complete, quarantined, bundle bytes/SHA-256, and private release IDs. Do not publish content or findings. Then stop.
