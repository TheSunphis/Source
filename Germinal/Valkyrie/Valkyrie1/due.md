# Valkyrie1 due — Wave 002 one-launch production

This is the complete continuation work order. The user should not relay ten checkpoints manually. Valkyrie1 processes all 50 dossiers in ten bounded five-item checkpoints during this one execution.

## Identity and state

- Exact agent: `Valkyrie1`
- Assignment: `germinal-wave002-valkyrie1-50`
- Launch state: `HOLD_ZERO_STRUCTURAL_FAILURE`
- Total slots: `50`
- Checkpoints: `10`
- Slots per checkpoint: `5`
- Slot pattern: `V1-W002-C01-001` through `V1-W002-C10-005`
- Public report: `Germinal/Valkyrie/Valkyrie1/report.md`

Zero audited the submitted replacement wave and placed this assignment on hold before Crow. All 300 displayed Japanese lines were represented by one whole-line segment each, so the required complete segment analysis was not delivered. Do not relaunch, revise, or upload anything until Zero issues a new immutable due after the user chooses the next disposition.

## Immutable 50-dossier material

- Private release ID: `400995823`
- Bundle: `germinal-wave002-valkyrie1-material-50.tar.gz`
- Bytes: `22011`
- SHA-256: `c1297bba768f7510ec0ce05efad0018702ac524e35e78200e520f7534ac3bb4e`
- Format: `germinal-wave002-dossier-v2`
- Dossiers: `50`
- Candidate build: `candidatebuild2:405c22b24e5835bddf6f33fa4fc0e5d7`
- Source pool: unchanged frozen 20,745 candidates
- Allocation: ten candidates in each of five major classes, one of each class per checkpoint

## Zero-provided infrastructure

- Commit: `c7160f58990c490c497840e4b5583db63d054051`
- Toolkit: `germinal-infrastructure-v8`
- Tool SHA-256: `11310d21dba3bdb65306e6fcefcf52893369106cc23cb50ded605f7fddd369f9`
- Valkyrie checkpoint schema SHA-256: `81cb1e0c47159017454080d55d974e9466e324c8b5d6c2744548df7e2c860fb1`
- Input/output/report transport: authenticated `api.github.com`

Verify identities and run self-test. The v8 self-test covers Checkpoints 01 and 10 and the complete Card structure. Never repair or replace Zero's tool.

Initial command:

```text
python3 germinal_tool.py fetch-release-body-bundle TheSunphis Source 400995823 22011 c1297bba768f7510ec0ce05efad0018702ac524e35e78200e520f7534ac3bb4e germinal-wave002-valkyrie1-material-50.tar.gz
```

## One-launch checkpoint loop

For checkpoint `NN` from `01` through `10`:

1. Load only the five dossiers whose `checkpoint` equals `NN`.
2. Create exactly five ordered records with IDs `V1-W002-CNN-001` through `005`.
3. Use manifest format `germinal-valkyrie-checkpoint-v2`.
4. Use assignment `germinal-wave002-valkyrie1-checkpointNN-5`.
5. Set `expectedSlotIds` to those exact five IDs.
6. Validate with `validate-valkyrie`.
7. Package as `germinal-valkyrie1-wave002-cNN-5.tar.gz`.
8. Store privately with `upload-release-body-bundle`.
9. Record bundle bytes, SHA-256, counts, and ordered private release IDs in an in-memory wave ledger.
10. Continue directly to the next checkpoint. Do not ask the user to relay or activate it.

Command pattern:

```text
python3 germinal_tool.py validate-valkyrie manifest.json slots.ndjson
python3 germinal_tool.py package valkyrie manifest.json slots.ndjson germinal-valkyrie1-wave002-cNN-5.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-wave002-valkyrie1-checkpointNN-5 germinal-valkyrie1-wave002-cNN-5.tar.gz
```

If one slot must abstain, conserve it and continue the remaining slots/checkpoints. An infrastructure failure stops the wave; a content abstention does not.

## Expression and hybrid editorial contract

Expression is the renamed former Family. Preserve its established boundary, forms, Library fields, complete Card anatomy, and internal family/form concepts.

External evidence anchors the primary form, reading, meaning, boundary, supported alternates, register/history/region facts, and provenance. Valkyrie1 may author usage guidance, responses, follow-ups, dialogue, safe patterns/examples, and distinction explanations as clearly identified editorial proposals. Editorial content is not source attestation; Crow independently audits it. Lack of a copied source sentence is not grounds to abstain.

The canonical Koto Vocabulary index remains a later Zero gate. Do not invent IDs or abstain solely because it is absent. For every segment set `selectedVocabularyId` to null, provide proposed surface/reading/lemma candidates, use disposition `deferred-zero-canonical-index`, and state that Zero resolution is required before acceptance.

## Complete Card structure — mandatory

Each submitted Expression must contain substantive intentions, Use when, Take care, relationships, forms, responses, follow-ups, dialogue, patterns/disposition, distinctions/disposition, Library fields, provenance, sources, and complete analyses.

Minimum structural requirements enforced by v8:

- exactly one primary form matching `primaryLineId`;
- at least two responses with distinct non-primary Japanese lines;
- at least two follow-ups with distinct non-primary lines, different from responses;
- dialogue with situation, relationship, register, at least two turns, and at least two distinct Japanese lines;
- target Expression occurs in the dialogue;
- at least six distinct analysed Japanese lines per Card;
- every Japanese-bearing module references the complete `japaneseLines` map;
- no orphan or unknown line references;
- patterns and distinctions are either supported with entries or `none-supported` with a substantive reason;
- complete Library search arrays and provenance;
- externally evidenced primary line; honestly identified editorial evidence for agent-authored lines.

Every line must reconstruct Japanese and reading exactly from segments. Every segment needs meaning, grammatical role, spans, lemma/inflection disposition, deferred Vocabulary disposition, and evidence identity. Zero later handles colours, tappable UI, accessibility, TTS wiring, caching, and personal state.

## Exact expression keys

Use `expressionId`, `primaryLineId`, `category`, `usageSummary`, `verificationState`=`candidate`, `kotoDifficulty`, arrays `intentions`, `useWhen`, `takeCare`, `relationships`, `forms`, `responses`, `followUps`, `sources`, objects `dialogue`, `patterns`, `distinctions`, `library`, `provenance`, and the complete `japaneseLines` map.

Source locators use `sourceId`, `artifact`, `locator`, and `claimScope`. Agent-authored lines use `sourceId: editorial:Valkyrie1`, `artifact: private-checkpoint-output`, their line ID as locator, and `claimScope: editorial-proposal-not-source-attestation`.

## Final wave report

After all ten private checkpoint bundles are stored, update `report.md` once with:

- total attempted/submitted/abstained/failed counts across all 50;
- one safe row for each checkpoint: bundle name, bytes, SHA-256, private release IDs, and counts;
- start/completion timestamps and terminal status.

No Japanese, meanings, evidence, analyses, or payload excerpts may enter the report. Publish remotely with:

```text
python3 germinal_tool.py publish-safe-report TheSunphis Source Germinal Germinal/Valkyrie/Valkyrie1/report.md Germinal/Valkyrie/Valkyrie1/report.md "Valkyrie1 report wave002 complete"
```

Verify the returned remote commit SHA. Then stop. Crow1 and Zero handle later gates.
