# Valkyrie1 due — Wave 002 Checkpoint 01

This is Valkyrie1's complete work order. It implements the user-approved hybrid staged method.

## Identity and state

- Exact agent: `Valkyrie1`
- Assignment: `germinal-wave002-valkyrie1-checkpoint01-5`
- Launch state: `ACTIVE`
- Attempted slots: exactly `5`
- Slot IDs: `V1-W002-C01-001`, `V1-W002-C01-002`, `V1-W002-C01-003`, `V1-W002-C01-004`, `V1-W002-C01-005`
- Wave target: 50 proposals through ten gated checkpoints of five
- Public report: `Germinal/Valkyrie/Valkyrie1/report.md`

Do not execute another checkpoint. Zero opens Checkpoint 02 only after Crow1 reviews this checkpoint and Zero closes its gates.

## Immutable private dossiers

- Transport: authenticated `api.github.com` private draft-release body
- Release ID: `400986607`
- Bundle: `germinal-wave002-valkyrie1-checkpoint01-material.tar.gz`
- Bytes: `4083`
- SHA-256: `042fba366d3d0c0df12518a1569b2a70e8507baffa5e6cb58aa7386cbdb69ab1`
- Format: `germinal-wave002-dossier-v1`
- Dossiers: 5
- Candidate build: `candidatebuild2:405c22b24e5835bddf6f33fa4fc0e5d7`
- Source pool: unchanged frozen 20,745-candidate pool
- Classes: one interactional formula, one grammar construction, one conventional collocation, one idiom, and one proverb/saying

Each dossier contains one exact candidate, all resolved evidence records allocated to it, an analysis scaffold, the Family/Expression continuity rule, and the hybrid editorial contract. Verify bundle identity before reading.

## Zero-provided infrastructure

- Commit: `4264939f18b699bb9fc91a7a4fb388dafb999a28`
- Toolkit: `germinal-infrastructure-v7`
- Tool: `Germinal/infrastructure/germinal_tool.py`
- Tool SHA-256: `8a2d169022db17e56b087618a7056819cd8e2d46f208810ef49df0339aa90b44`
- Checkpoint schema: `Germinal/infrastructure/valkyrie-checkpoint-v2.schema.json`
- Schema SHA-256: `00974715344cc5f7bf28740ab612617fb8d36621f4c062a7f64fe58e73f9e9ad`
- Runtime: Python 3.11+

Verify tool/schema hashes and run `python3 germinal_tool.py self-test`. Stop on mismatch; never repair Zero's infrastructure.

Commands:

```text
python3 germinal_tool.py fetch-release-body-bundle TheSunphis Source 400986607 4083 042fba366d3d0c0df12518a1569b2a70e8507baffa5e6cb58aa7386cbdb69ab1 germinal-wave002-valkyrie1-checkpoint01-material.tar.gz
python3 germinal_tool.py validate-valkyrie manifest.json slots.ndjson
python3 germinal_tool.py package valkyrie manifest.json slots.ndjson germinal-valkyrie1-wave002-c01-5.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-wave002-valkyrie1-checkpoint01-5 germinal-valkyrie1-wave002-c01-5.tar.gz
python3 germinal_tool.py publish-safe-report TheSunphis Source Germinal Germinal/Valkyrie/Valkyrie1/report.md Germinal/Valkyrie/Valkyrie1/report.md "Valkyrie1 report wave002 checkpoint01"
```

## Continuity rule

Expression is the renamed former Family. Preserve the established Family boundary, primary/alternate relationship, Library data, complete Card anatomy, and internal family/form concepts. The assignment envelope divides work but does not redefine the product.

## Hybrid editorial law

External evidence anchors:

- the candidate's existence and boundary;
- primary form and reading;
- supported alternate forms;
- candidate meaning and class;
- register, historical, regional, or other factual claims;
- source/licence/provenance statements.

Valkyrie1 is explicitly authorized to author these as **editorial proposals**:

- contextual usage summary;
- Use when, Take care, and relationship guidance;
- responses and follow-ups;
- dialogue;
- productive patterns and constrained examples;
- nearby-distinction explanations.

Editorial material must be natural, coherent, specific, and independently reviewable. It is not source attestation and must never be labeled as such. Lack of a source sentence for an agent-authored dialogue or response is **not** a reason to abstain. Crow1 will independently critique all editorial Japanese and explanations.

## Vocabulary checkpoint rule

The canonical Koto Vocabulary index is not present in Source. Do not invent Koto Vocabulary IDs and do not abstain solely for that reason. For every segment:

- enumerate proposed surface/reading/lemma candidates;
- set `selectedVocabularyId` to null;
- set `vocabularyDisposition` to `deferred-zero-canonical-index`;
- set `unlinkedReason` to `checkpoint proposal; Zero canonical resolution required before acceptance`.

No checkpoint proposal can become accepted until Zero later performs canonical resolution and reverse-omission validation.

## Required Expression content

For each dossier, create one complete candidate Expression containing:

- primary and important supported alternate forms;
- Koto Difficulty 1–5 and Category;
- contextual meaning, intention, usage, register, and relationship guidance;
- Use when and Take care;
- responses and follow-ups;
- realistic dialogue;
- productive pattern/examples when safe, otherwise explicit non-applicability;
- nearby distinction when defensible, otherwise explicit non-applicability;
- Library fields and provenance;
- complete analysis for every Japanese line displayed anywhere on the Card.

Every Japanese line—forms, responses, follow-ups, dialogue turns, templates, examples, comparisons, and fragments—must reconstruct exactly from segments. Each segment needs surface, reading, spans, contextual meaning, grammatical role, lemma/inflection when relevant, deferred Vocabulary disposition, and evidence identity.

Source-anchored lines cite dossier evidence. Agent-authored lines use an honest editorial locator with exact keys such as `sourceId: editorial:Valkyrie1`, `artifact: private-checkpoint-output`, `locator: <lineId>`, and `claimScope: editorial-proposal-not-source-attestation`. This identity does not prove correctness; it tells Crow what must be independently audited.

Zero alone later implements colours, tappable panels, accessibility, TTS, Library/Card UI, caching, and personal state. Do not create frontend code or presentation colours.

## Exact checkpoint envelope

`manifest.json` uses:

- `formatVersion`: `germinal-valkyrie-checkpoint-v2`
- `agent`: `Valkyrie1`
- `assignment`: `germinal-wave002-valkyrie1-checkpoint01-5`
- `expectedSlotIds`: the five ordered slot IDs above
- attempted/submitted/abstained/failed counts
- canonical `recordsSha256`
- input asset identity, evidence build, and candidate build

`slots.ndjson` contains exactly five ordered records. Submitted records contain `expression`; abstained/failed records contain a concise reason code and no invented Expression.

Each submitted `expression` uses the existing checkpoint validator keys: `expressionId`, `primaryLineId`, `category`, `usageSummary`, `verificationState`=`candidate`, `kotoDifficulty`, non-empty arrays `intentions`, `useWhen`, `takeCare`, `relationships`, `forms`, `responses`, `followUps`, `sources`, objects `dialogue`, `patterns`, `distinctions`, `library`, `provenance`, and a complete `japaneseLines` map. Japanese-bearing sections reference `LineId`/`LineIds` entries in that map.

Aim to submit all five. Abstain only when the dossier cannot safely anchor the Expression boundary/form/meaning or when natural editorial completion remains genuinely unsafe. Do not abstain merely because teaching lines are editorial proposals or canonical Vocabulary mapping is deferred by this checkpoint contract.

## Private output and safe report

Validate, package, and store `germinal-valkyrie1-wave002-c01-5.tar.gz` using the API-only commands above. Record output bytes, SHA-256, and ordered private release IDs.

Update the public report with safe metadata only: assignment, due identity, times, input/output identities, five-slot counts, terminal status, and non-content reason code. Never include Japanese, meanings, evidence, analyses, or payload excerpts. Publish with `publish-safe-report` and verify the returned remote commit SHA.

Allowed terminal status: `submitted`, `abstained`, or `failed`. Submitted means private proposal storage succeeded; it is not acceptance.
