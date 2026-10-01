# Crow1 due — one concrete review of 49 completed Cards

- Exact agent: `Crow1`
- Assignment: `germinal-crow1-review-49-1`
- Launch state: `ACTIVE`
- Expected reviews: `49`
- Role: critic only; do not repair
- Public report: `Germinal/Crow/Crow1/report.md`

Review all 49 once. The user will not mediate Card-by-Card disputes. A quarantine recommendation is actionable only when it names the exact Card ID, JSON pointer, failed gate, observed problem, and a concrete repair directive. Broad or template criticism will be ignored by Zero.

## Inputs

Seed material:
- Release `401235338`; bytes `8302`
- SHA-256 `ae5587937a6c1baa588ecf1ab1b3920c58857a4fe8a1aecba8747ab687864870`

Valkyrie completed batch:
- Release `401239153`; bundle `germinal-valkyrie1-complete-49-v1.tar.gz`; bytes `36357`
- SHA-256 `9b45fcf8be8c2f67efa823eabe478fad8613dc15d32c2ab41c8b7f3c04dd7e1e`
- Records `49`; Valkyrie submitted/quarantined `47/2`

Accepted quality exemplar:
- Compiled release `401125726`
- Prototype release `401210597`

Reconstruct and verify every private asset before review.

## Required per-Card review

Return exactly 49 ordered review records matching the seed IDs. Each record must contain:

- `id`;
- `decision`: `pass` or `quarantine`;
- exact checks: `meaningAndIntentions`, `usageAndRelationships`, `japaneseNaturalness`, `responseFit`, `followUpFit`, `dialogueCoherence`, `segmentAccuracy`, `evidenceBoundary`, `searchableForms`;
- for every check: boolean `passed`, concrete JSON `pointer`, Card-specific `observedDetail`, and substantive `rationale`;
- for quarantine: one or more findings with `gate`, `pointer`, `problem`, and `repairDirective`.

Explicitly test whether responses actually answer the target expression, dialogue turn order is coherent, meanings avoid doubled punctuation or boilerplate, segment surfaces exactly cover each line, forms are genuinely searchable alternatives, and source claims stay separate from editorial teaching content. Do not pass a Card merely because the structural validator passed.

## Output

- `manifest.json`: format `germinal-crow-review-49-output-v1`, assignment `germinal-crow1-review-49-1`, attempted/reviewed/pass/quarantine counts, and SHA-256 of canonical `reviews.ndjson`
- `reviews.ndjson`: 49 ordered records
- Bundle: `germinal-crow1-review-49-v1.tar.gz`
- Private release title: `germinal-crow1-review-49-1`

Use Zero’s core upload tool at commit `5eccc8e4c768bce21ff00398cb172f97617d3f24`, SHA-256 `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`. Publish only safe count/hash metadata in the report, then stop.
