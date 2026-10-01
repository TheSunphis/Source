# Crow1 due — Wave 002 one-launch independent review

- Exact agent: `Crow1`
- Assignment: `germinal-wave002-crow1-review-50`
- Launch state: `ACTIVE`
- Expected Valkyrie checkpoints: `10`
- Expected slots: `50`
- Public report: `Germinal/Crow/Crow1/report.md`

Review all ten immutable revision2 bundles in this one execution. Internally process ten checkpoints of five without asking the user to relay, activate, or copy anything. Do not review the rejected v7 or v8 bundles.

## Infrastructure

- Commit: `5eccc8e4c768bce21ff00398cb172f97617d3f24`
- Toolkit: `germinal-infrastructure-v9`
- Tool SHA-256: `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`
- Crow checkpoint schema SHA-256: `775cb4162f09f8c5b6bfcaf6f8f16e2a14c488d7815c163ad910d3fd2a16accc`
- Transport: authenticated `api.github.com` release bodies and Contents API

Retrieve and verify the tool and Crow schema from the immutable infrastructure commit, run `self-test`, and never alter Zero's infrastructure.

## Original dossier/evidence material

- Release ID: `400995823`
- Bytes: `22011`
- SHA-256: `c1297bba768f7510ec0ce05efad0018702ac524e35e78200e520f7534ac3bb4e`
- Bundle: `germinal-wave002-valkyrie1-material-50.tar.gz`

Use this material to verify candidate identity, externally anchored forms/readings/meanings, claim scope, and evidence authorization. It is not finished Card truth.

## Immutable Valkyrie revision2 inputs

| Checkpoint | Bundle | Bytes | SHA-256 | Private release ID |
|---:|---|---:|---|---:|
| 01 | `germinal-valkyrie1-wave002-r2-c01-5.tar.gz` | 6340 | `193c6ec7a6573e04dc57b84d6667422a589c7f8f0eafce5d2be82918a3aa17ed` | `401022679` |
| 02 | `germinal-valkyrie1-wave002-r2-c02-5.tar.gz` | 6240 | `c244bc05978cccddced78976a849890fca8d648dcf126113b4ad9d62bf8c2904` | `401022708` |
| 03 | `germinal-valkyrie1-wave002-r2-c03-5.tar.gz` | 6705 | `2969ca99383446c1ace8560b8ab9ff725df92054f8a6d750744ec2d9289ab62f` | `401022740` |
| 04 | `germinal-valkyrie1-wave002-r2-c04-5.tar.gz` | 6420 | `7043acba31001b8c67cb05c0227249e87e7f91e184fc7fbaddbc0e34e325f986` | `401022769` |
| 05 | `germinal-valkyrie1-wave002-r2-c05-5.tar.gz` | 6304 | `6c185b31d163c4689810eddc112d84a664c8691bc6bed6bb7714b9b2e20e25c0` | `401022805` |
| 06 | `germinal-valkyrie1-wave002-r2-c06-5.tar.gz` | 6289 | `512acac2c9951cee81610ca9e08d18995003787cbf95c5677232979fd3575923` | `401022842` |
| 07 | `germinal-valkyrie1-wave002-r2-c07-5.tar.gz` | 6443 | `17b4475f9006c9fd9b2503f55e69dba12a0e98659a0e0cb06439e081f91716f6` | `401022875` |
| 08 | `germinal-valkyrie1-wave002-r2-c08-5.tar.gz` | 6238 | `4d84375833097baf6ddbf10ff4702d4fc3c88d2ddb953a86276051942cbc1a2e` | `401022906` |
| 09 | `germinal-valkyrie1-wave002-r2-c09-5.tar.gz` | 6278 | `35220fc8419bb38aacf7567b02d60ee7d965b5a9e3c2f7652d4d7a9eeb3aca8b` | `401022940` |
| 10 | `germinal-valkyrie1-wave002-r2-c10-5.tar.gz` | 6405 | `8387ed27f71af3f9dfb423255af680d6359efca6e0304fb7a31eebdb3e03ac37` | `401022976` |

Reconstruct every bundle with `fetch-release-body-bundle`; verify byte length and SHA-256 before opening. Stop on any mismatch.

## Independent critic contract

Critique; do not repair, rewrite, contact Valkyrie1, or negotiate findings. Structural validator success is not linguistic proof. Crow opinion is independent review, not external source attestation.

For each proposal independently inspect:

1. candidate boundary and supported form identity;
2. Japanese line naturalness, exact reading, and meaning;
3. every segment boundary, kind, lemma, inflection, span, contextual meaning, and grammatical role;
4. whether segmentation is linguistically meaningful rather than arbitrary character splitting;
5. response and follow-up naturalness and usefulness;
6. dialogue coherence, target occurrence, register, relationship, and pragmatics;
7. intention, Use when, Take care, relationship guidance, and Koto Difficulty;
8. forms and any omitted/supported alternates;
9. pattern disposition and examples;
10. distinction disposition and unsafe-replacement guidance;
11. Library search fields, provenance, TTS eligibility, and deferred Vocabulary integrity;
12. unsupported factual claims or misuse of editorial evidence.

All 50 Cards use one form, two responses, two follow-ups, and two dialogue turns, and all 50 retain `none-supported` for patterns and distinctions. Minimum counts are not automatically defects, and variety must not be invented. Nevertheless, scrutinize each decision individually; do not pass templating merely because it meets v9 floors.

Canonical Koto Vocabulary IDs are deliberately deferred to Zero. Do not quarantine solely for null selected IDs when the proposed surface/reading/lemma candidates and deferment are sound. Do quarantine invented IDs, missing lexical candidates, or bad segmentation.

## Exact critic record

Each slot record has `slotId`, `recommendation` (`pass` or `quarantine`), `checks`, and `findings`. `checks` must contain exactly these boolean keys:

- `candidateBoundaryEvidence`
- `formsReadingsMeanings`
- `segmentBoundaryCompleteness`
- `segmentKindsLemmasInflections`
- `responseNaturalness`
- `followUpNaturalness`
- `dialogueCoherence`
- `registerPragmaticsRelationship`
- `patternsDisposition`
- `distinctionsDisposition`
- `libraryProvenance`
- `vocabularyDeferralIntegrity`
- `noUnsupportedClaims`

A pass requires every check true and zero findings. Quarantine requires at least one precise finding with severity, stable code, JSON pointer into the Valkyrie record, evidence locator, explanation, and failed gate. The evidence locator may identify the immutable record and independent editorial judgment; it must not falsely portray Crow as an external source. One decisive defect is enough to quarantine, but record all material defects found.

## One-launch checkpoint loop

For checkpoint `NN` from `01` through `10`:

1. Review the five records in exact slot order.
2. Use format `germinal-crow-checkpoint-v2`.
3. Use assignment `germinal-wave002-crow1-checkpointNN-review-5`.
4. Set exact expected slot IDs `V1-W002-CNN-001` through `005`.
5. Set `valkyrieAsset` to that exact input release ID, bytes, SHA-256, and bundle name.
6. Set `evidenceAsset` to the exact original dossier material identity.
7. Conserve `attempted=5`, `reviewed=5`, and pass/quarantine counts.
8. Validate using `validate-crow`.
9. Package as `germinal-crow1-wave002-cNN-review-5.tar.gz`.
10. Upload under release title `germinal-wave002-crow1-checkpointNN-review-5`.
11. Record output identities and continue directly to the next checkpoint.

Command pattern:

```text
python3 germinal_tool.py validate-crow manifest.json reviews.ndjson
python3 germinal_tool.py package crow manifest.json reviews.ndjson germinal-crow1-wave002-cNN-review-5.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-wave002-crow1-checkpointNN-review-5 germinal-crow1-wave002-cNN-review-5.tar.gz
```

## Final safe report

After all ten critic bundles are stored, update `report.md` once with aggregate attempted/reviewed/pass/quarantine counts and one safe output identity row per checkpoint. Include no Japanese, meanings, evidence, analyses, findings, or payload excerpts. Publish with `publish-safe-report`, verify the returned remote commit SHA, then stop. Zero alone derives final outcomes; no Crow pass is acceptance.
