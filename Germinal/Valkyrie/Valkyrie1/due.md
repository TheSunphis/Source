# Valkyrie1 due — complete 49 Germinal Cards

- Exact agent: `Valkyrie1`
- Assignment: `germinal-valkyrie1-complete-49-1`
- Launch state: `ACTIVE`
- Scope: `49` source-anchored preview drafts
- Role: complete structured content; do not assign canonical Vocabulary IDs
- Public report: `Germinal/Valkyrie/Valkyrie1/report.md`

This is one bounded production batch. The user wants speed without card-by-card courier work. Complete all 49 in one run. Do not contact Crow1 or ask the user content questions.

## Inputs

Private seed material:
- Release ID: `401235338`
- Bundle: `germinal-49-draft-material-v1.tar.gz`
- Bytes: `8302`
- SHA-256: `ae5587937a6c1baa588ecf1ab1b3920c58857a4fe8a1aecba8747ab687864870`
- Draft seeds: `49`

Accepted quality exemplar:
- Compiled Card release: `401125726`
- Full prototype release: `401210597`
- Acceptance ID: `goldacceptance1:2442ad027b286932a2c59e47417d436d`

The exemplar demonstrates depth, interactional specificity, complete segment analysis, honest evidence boundaries, and accessible learner guidance. Do not copy its scenario or reassurance language into unrelated Cards.

## Infrastructure

- Upload core `germinal_tool.py`, commit `5eccc8e4c768bce21ff00398cb172f97617d3f24`, SHA-256 `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`
- Batch validator `complete_49_tool.py`, commit `419d9454ef273b7b9ade20f0f57213354475c3d6`, SHA-256 `110ef183d81567b2a8c511e57796e1bfe287fa274ff202c95c0a707e1bd48bc0`

Run the validator self-test. Do not patch infrastructure.

## Per-Card completion contract

For every seed ID, preserve the exact ID and direct source anchor, then author candidate-specific content:

- an accurate primary meaning and Koto Difficulty;
- at least two distinct intentions;
- a specific usage summary;
- at least two concrete `useWhen`, `avoidWhen`, and relationship items;
- at least one meaningful form;
- at least two natural responses;
- at least two useful follow-ups;
- at least three coherent dialogue turns in one explicit situation and relationship;
- complete surface-covering segment analysis for every displayed Japanese line;
- one declared segmentation policy applied consistently within the Card;
- specific rationales for forms, responses, follow-ups, dialogue, and segmentation;
- preserved direct source anchor plus `original-editorial` provenance for teaching content;
- honest empty patterns/comparisons when the source does not support them.

All `selectedVocabularyId` fields must remain null. Zero alone mints or selects canonical Vocabulary IDs after validation. Device TTS must remain explicit-action only. Use Koto Difficulty; never add Commonness, CEFR, JF, or JLPT grading.

## Quality and throughput rules

- Do not reuse one dialogue, summary, caution, rationale, or segment explanation across Cards.
- Do not turn dictionary glosses into unsupported social guidance.
- Do not claim draft editorial scenarios are source-attested.
- Do not add a productive pattern merely to fill a field.
- Use natural Japanese appropriate to the stated relationship and register.
- If a Card cannot be completed honestly, mark it quarantined with a safe reason in the private record; still conserve all 49 IDs.

## Output

- Manifest format: `germinal-complete-49-output-v1`
- Assignment: `germinal-valkyrie1-complete-49-1`
- Files before packaging: `manifest.json`, `records.ndjson`
- Bundle: `germinal-valkyrie1-complete-49-v1.tar.gz`
- Private release title: `germinal-valkyrie1-complete-49-1`

```text
python3 complete_49_tool.py validate material.json manifest.json records.ndjson
python3 complete_49_tool.py package material.json manifest.json records.ndjson germinal-valkyrie1-complete-49-v1.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-valkyrie1-complete-49-1 germinal-valkyrie1-complete-49-v1.tar.gz
```

Publish one safe report with exact START/due commits, submitted/quarantined counts, bundle bytes/SHA-256, and private release IDs. Never commit Card payloads, Japanese, meanings, analyses, evidence, or findings publicly. Then stop.
