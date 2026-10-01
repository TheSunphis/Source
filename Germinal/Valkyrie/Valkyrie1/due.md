# Valkyrie1 due — Wave 002 targeted quality revision

Valkyrie1 completed the selected quality revision. Zero reconstructed and structurally verified all ten revision2 bundles and released them to Crow1. Do not relaunch, revise, or upload anything unless Zero issues a new immutable due.

## Identity and state

- Exact agent: `Valkyrie1`
- Assignment: `germinal-wave002-valkyrie1-analysis-revision-50`
- Launch state: `HOLD_COMPLETED_AWAITING_CROW`
- Scope: `50 existing proposals; ten internal checkpoints of five`
- Slot pattern: `V1-W002-C01-001` through `V1-W002-C10-005`
- Public report: `Germinal/Valkyrie/Valkyrie1/report.md`

This is a targeted revision, not a clean rewrite. Preserve sound candidate identity, externally anchored form/reading/meaning, and useful editorial material. Correct anything that becomes unsafe or incoherent during analysis. Abstain rather than invent.

## Original dossier material

- Release ID: `400995823`
- Bytes: `22011`
- SHA-256: `c1297bba768f7510ec0ce05efad0018702ac524e35e78200e520f7534ac3bb4e`
- Bundle: `germinal-wave002-valkyrie1-material-50.tar.gz`

Use the original dossier for evidence authorization and candidate identity.

## Immutable revision inputs

| Checkpoint | Private release ID | Bytes | SHA-256 |
|---:|---:|---:|---|
| 01 | `401004191` | 4669 | `49f852d385d9ec90d176f8ba382bb617807bf44578bdb794968dbb288bd7aaf4` |
| 02 | `401004222` | 4613 | `a017ffb8aef0a21702263e87975097ddabb73827988c5b6e4522daf8230acb78` |
| 03 | `401004244` | 4733 | `722d8f1e37dae4950cab51dc4e2ea805c8ac4dc2d125c44a935f67ed8653dc92` |
| 04 | `401004266` | 4701 | `577288eb03752d4101b52b4984300af55b9e03077e429540de38a2df8e603bb3` |
| 05 | `401004299` | 4666 | `8dc2a39e3849ad0e309096f1761ba6855aa760972236318dc6f3675f70bad1df` |
| 06 | `401004322` | 4665 | `f87a092eb6da887ede98a4569230162b44352dd87213acb91272fc3ab00c42c1` |
| 07 | `401004346` | 4634 | `0a589034c8bbf08e7ab90abc8a44d049d8ece4de52f2670d599a4c31c523a04b` |
| 08 | `401004364` | 4584 | `483083d80a24dca78b76411c27b5e8b440d790c4f5fdd1da728b7605eb829fb9` |
| 09 | `401004386` | 4622 | `5da070faa1a36eff8a9f4a103415c986cd21cb4cd6dc58751080750e051ddd80` |
| 10 | `401004412` | 4604 | `1795a60d5c3fdc3ab994cbd7c53e4d8d6d2b686eea96f843f0a2201ae34a8833` |

The bundles are immutable audit evidence. Never overwrite them or represent them as accepted. Reconstruct each with `fetch-release-body-bundle` and verify its exact byte length and digest before opening.

## Zero-provided infrastructure

- Commit: `5eccc8e4c768bce21ff00398cb172f97617d3f24`
- Toolkit: `germinal-infrastructure-v9`
- Tool SHA-256: `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`
- Valkyrie checkpoint schema SHA-256: `81cb1e0c47159017454080d55d974e9466e324c8b5d6c2744548df7e2c860fb1`
- Segmentation contract: `Germinal/infrastructure/SEGMENTATION-CONTRACT-v9.md`

Retrieve tool, schema, and contract from the immutable infrastructure commit; verify hashes; run `self-test`. Do not alter or replace Zero's infrastructure. v9 deterministically rejects the submitted v8 pseudo-segmentation.

## Required correction

Every displayed Japanese line must be decomposed at meaningful lexical, idiomatic, particle/grammar, auxiliary/inflectional, productive-slot, and punctuation boundaries. Arbitrary character slicing is prohibited.

Every segment requires:

- ordered `segmentId` values `s01` through `sNN`;
- exact contiguous Japanese and reading spans;
- `kind`: `content-or-idiom`, `particle-or-grammar`, `auxiliary-or-inflection`, `punctuation`, or `productive-slot`;
- segment-specific contextual meaning and grammatical role;
- a linguistically appropriate lemma except punctuation;
- explicit inflection explanation for auxiliary/inflection segments;
- proposed Vocabulary candidate objects with surface, reading, and lemma for non-punctuation segments;
- null `selectedVocabularyId`, disposition `deferred-zero-canonical-index`, and a substantive Zero-resolution reason;
- honest evidence identity.

Structural anti-placeholder floors:

- a line of 6–9 Japanese characters has at least two meaningful segments;
- a line of 10 or more has at least three meaningful segments;
- each Card has at least twelve segments across all displayed lines;
- each Card identifies at least one grammatical, inflectional, or punctuation segment;
- the six or more displayed Japanese texts are actually distinct.

These floors are not the goal. Use as many linguistically meaningful segments as required. One whole-line segment is permissible only for a genuinely atomic short expression and cannot be the treatment of every line.

## Required quality reassessment

Re-open every Card, not only its segment arrays. All previous Cards used exactly the minimum numbers of forms, responses, follow-ups, and dialogue turns; all 50 marked both patterns and distinctions `none-supported`. Do not change fields merely to create variety, but independently reassess each decision against its candidate and evidence.

- Preserve `none-supported` only when the dossier and Expression genuinely warrant it, with a candidate-specific reason.
- Add a safe pattern, distinction, or alternate form only when genuinely supported; every added Japanese line must be fully analysed and referenced.
- Check that responses, follow-ups, and dialogue are natural, coherent, relationship-safe, and useful rather than template fillers.
- Keep editorial material labeled `editorial:Valkyrie1`; never present it as external attestation.
- Never invent Koto Vocabulary IDs.

## One-launch output loop

For checkpoint `NN` from `01` through `10`:

1. Pair the five existing records with their exact original dossiers.
2. Produce five conserved outcomes using manifest format `germinal-valkyrie-checkpoint-v2`.
3. Set assignment to `germinal-wave002-valkyrie1-revision2-checkpointNN-5`.
4. Preserve exact ordered slot IDs `V1-W002-CNN-001` through `005`.
5. Validate using v9.
6. Package as `germinal-valkyrie1-wave002-r2-cNN-5.tar.gz`.
7. Upload under release title `germinal-wave002-valkyrie1-revision2-checkpointNN-5`.
8. Record bytes, SHA-256, private release IDs, and counts in the wave ledger.
9. Continue directly through all checkpoints without user relay.

Command pattern:

```text
python3 germinal_tool.py validate-valkyrie manifest.json slots.ndjson
python3 germinal_tool.py package valkyrie manifest.json slots.ndjson germinal-valkyrie1-wave002-r2-cNN-5.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-wave002-valkyrie1-revision2-checkpointNN-5 germinal-valkyrie1-wave002-r2-cNN-5.tar.gz
```

## Final report

After all ten corrected bundles are stored, update `report.md` once with total counts and one safe identity row per replacement bundle. Include no Japanese, meanings, evidence, analyses, findings, or excerpts. Publish with the Zero tool, verify its remote commit SHA, then stop. Crow1 remains Zero-controlled.
