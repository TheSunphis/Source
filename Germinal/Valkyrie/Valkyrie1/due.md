# Valkyrie1 due

This is the **only public instruction file Valkyrie1 must read**. It contains the complete active assignment, operating boundaries, content contract, output contract, and reporting instructions. Do not open other Germinal instruction files.

## Identity and state

- Exact agent name: `Valkyrie1`
- Role: structured Expression creator
- Assignment: `germinal-wave001-valkyrie1-50`
- Launch state: `CLOSED_ABSTAINED`
- Attempted slots: exactly `50`
- Slot IDs: `V1-W001-001` through `V1-W001-050`
- Public status report: `Germinal/Valkyrie/Valkyrie1/report.md`

If the user did not name you exactly `Valkyrie1`, stop. Do not adopt another identity.

## Immutable private input

Retrieve only this private draft-release asset from `TheSunphis/Source`:

- Draft release tag: `expressions2-0.1.0-development-shadow`
- Draft release ID: `400491370`
- Assigned material asset: `germinal-wave001-valkyrie1-material.tar.gz`
- Asset ID: `603086307`
- Byte length: `510189`
- SHA-256: `56c69937ecc6e2a1ae3d01ff16a6e3db319c645eef916d443e5d14816002c364`
- Assignment material format: `germinal-assignment-material-v1`
- Required transport: authenticated `api.github.com` private draft-release bodies; do not call the release-asset download host
- Private chunk format: `germinal-private-body-chunk-v1`
- Private chunk release IDs, in order: `400905253,400905261,400905274,400905281,400905290,400905301,400905309,400905316`
- Assigned reserve: `1000` candidates selected from the unchanged frozen pool
- Parent pool asset: `expressions2-batch001-candidates.tar.gz` (`601941135`, `44861050` bytes, SHA-256 `1cc991839e1184dfce5bdcb3e54747d1873e2dd9c707f7478aa6d5995a52060d`)
- Evidence build: `evidencebuild2:4cc90019ead5aa2e7b2dcbc7e82b1bcb`
- Evidence manifest SHA-256: `849e288d8c05df9d1c9f24566e06c41fa91ed36db8199dd83b197f29a61fb252`
- Candidate build: `candidatebuild2:405c22b24e5835bddf6f33fa4fc0e5d7`
- Normalized candidate records: `20745`
- Normalized candidate canonical SHA-256: `8dc6fec2c14a4f53ecea90439965a15a6aca7ea87e53233098786bb92d5e3995`
- Frozen contamination verdict: `passed` with zero legacy IDs, legacy imports, personal state, and unapproved sources

Use Zero's pinned `fetch-release-body-bundle` command below. It retrieves eight authenticated private draft-release JSON bodies only from `api.github.com`, validates each base64 chunk and its SHA-256, reconstructs the 510,189-byte material shard, and validates the final SHA-256. It does not contact GitHub's release-asset delivery host. The shard is derived from the same frozen pool and contains 1,000 reserved candidates plus 1,124 resolved evidence records with zero unresolved references. Verify final identity before using any member. Do not persist evidence or work payloads in the public repository or durable local storage; delete ephemeral transfer material after private output submission. If final identity differs or bounded retries are exhausted, stop and update only the safe public report with status `failed`.

Four prior bootstrap attempts on 2026-10-01 stopped before content generation. The first three established that the release-asset delivery host was unreachable. The fourth reached the new API metadata transport but exposed a Zero-authored v4 tool defect: `base64` was not imported, and the resulting name error was mislabeled as invalid base64. No candidate or output work was produced. Zero fixed the import and expanded the self-test, then executed the exact v5 eight-release retrieval function against the live private metadata with an in-memory sink; all 510,189 bytes and the final SHA-256 passed. Infrastructure v6 also provides API-only private output storage and remote safe-report publication, preventing the next release-host/local-commit failure. The assignment may restart without duplication.

The archive contains clean-room evidence, source/licence manifests, and extracted candidates. Candidate hypotheses are discovery aids, not editorial truth. Confirm every claim against permitted evidence. Do not inspect live or former `Expressions/`.

## Zero-provided tools and output contracts

Zero has prepared, self-tested, and pinned the infrastructure. Use it; do not rewrite, replace, or improvise a validator or packager.

- Infrastructure commit: `2aff6de22aed2dad510f95b6ff17f8400b0a432d`
- Toolkit: `germinal-infrastructure-v6`
- Runtime: Python 3.11 or newer plus Zero-pinned curl fallback for alternate TLS transport
- Tool path: `Germinal/infrastructure/germinal_tool.py`
- Tool SHA-256: `26321bd1bcb270451ef9cca05272b19dd46c39b330ff18d81ae181974d812515`
- Valkyrie schema: `Germinal/infrastructure/valkyrie-output-v1.schema.json`
- Valkyrie schema SHA-256: `4f3130167991670833355b97ac54017189859dcb6d8c23b8d34d91bc68a87026`
- Crow schema: `Germinal/infrastructure/crow-review-v1.schema.json`
- Crow schema SHA-256: `08d988695931961a7fa7ab5208af766aea3358c3cd19351b9538b7fc0832b6b5`

Fetch those machine files from the pinned commit, verify SHA-256 before execution, and run `python3 germinal_tool.py self-test`. A mismatch or failed self-test is an infrastructure failure: stop and report it to Zero. Workers must not repair Zero's tools.

The relevant commands are:

```text
python3 germinal_tool.py fetch-release-body-bundle TheSunphis Source 400905253,400905261,400905274,400905281,400905290,400905301,400905309,400905316 510189 56c69937ecc6e2a1ae3d01ff16a6e3db319c645eef916d443e5d14816002c364 germinal-wave001-valkyrie1-material.tar.gz
python3 germinal_tool.py validate-valkyrie manifest.json slots.ndjson
python3 germinal_tool.py validate-crow manifest.json reviews.ndjson
python3 germinal_tool.py package valkyrie manifest.json slots.ndjson germinal-valkyrie1-wave001-50.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-wave001-valkyrie1-50 germinal-valkyrie1-wave001-50.tar.gz
python3 germinal_tool.py publish-safe-report TheSunphis Source Germinal Germinal/Valkyrie/Valkyrie1/report.md Germinal/Valkyrie/Valkyrie1/report.md "Valkyrie1 report wave001"
python3 germinal_tool.py package crow manifest.json reviews.ndjson germinal-crow1-wave001-review-50.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-wave001-crow1-review-50 germinal-crow1-wave001-review-50.tar.gz
python3 germinal_tool.py publish-safe-report TheSunphis Source Germinal Germinal/Crow/Crow1/report.md Germinal/Crow/Crow1/report.md "Crow1 report wave001"
python3 germinal_tool.py sha256 FILE
```

Only execute the commands applicable to your role. Tool success proves structural conformance only, never linguistic correctness.

## Continuity and workload rule

An **Expression is the former Family under its new name**. Preserve the established Family grouping, primary/alternate-form relationship, Library fields, complete Card anatomy, internal `familyId`/`formId` concepts, candidate identities, and provenance model. Do not invent a new corpus unit or rebuild/re-normalize the candidate pool.

Use the already frozen `20745`-record normalized candidate pool with candidate build `candidatebuild2:405c22b24e5835bddf6f33fa4fc0e5d7`. Zero has reserved a deterministic 1,000-candidate assignment shard for Valkyrie1 from that unchanged pool: 300 conventional collocations, 200 grammar constructions, 200 idioms, 150 interactional formulas, and 150 proverbs/sayings. Produce 50 proposals only from this reserve. Zero owns cross-agent reservation, merge, and global deduplication. The assignment's `expression` transport object is a handoff wrapper only; its content must map losslessly to the established Family-compatible Expression model. The requirement to analyse every displayed Japanese line extends completeness without changing the Family boundary.

## Mission

This Wave 001 assignment is closed. It produced exactly 50 attempted slot records, all safely abstained. Do not execute it again. A future assignment requires a new due identity and enriched Zero-provided material. Aim for 50 complete, distinct, high-value Japanese Expression proposals. Preserve quality over count: when a slot cannot satisfy every content and analysis gate, emit an `abstained` slot record with reason code instead of inventing content or weakening a gate.

An Expression is one coherent communicative item with a primary form and all important evidence-supported alternate forms. Do not merge items merely because they are similar. Do not split or suppress important forms to escape analysis. Use Koto Difficulty 1–5 only; never use Commonness, JLPT, CEFR, or JF grading.

Select a useful variety of intentions, registers, relationship contexts, and difficulties without forcing unsafe quotas. Perform assignment-wide deduplication. Do not use former IDs, annotations, links, categories, explanations, decisions, or content. Model memory is not source authority.

## Zero/Valkyrie boundary

You create structured content data only. Zero—the original coordinating chat—alone implements the learner-facing Library and Cards, assigns presentation colours, creates tappable behavior, handles accessibility and responsive layout, wires device Japanese TTS, performs session caching, and implements Recognised/Review state.

Do not choose colours, write HTML/CSS/JavaScript, design screens, store audio, or implement user state. Supply complete semantic data so Zero can perform that work later. You cannot approve or independently verify your own output.

## Content required for every submitted Expression

Create complete structured data supporting:

1. Primary Japanese form, reading, contextual meaning, concise usage summary, Koto Difficulty, Category, and evidence-backed verification state.
2. Communicative intentions and important nearby-intention distinctions.
3. Concrete Use when guidance.
4. Take care guidance: register, social risk, face threat, situations to avoid, and likely learner mistakes.
5. Relationship guidance for every relevant family/close, peer, stranger, workplace, school, service, institutional, written, and group context.
6. Every important evidence-supported primary and alternate form with kind, register, Japanese, reading, contextual meaning, TTS eligibility, evidence, and line-analysis reference.
7. Natural responses and follow-ups with context, Japanese, reading, meaning, TTS eligibility, evidence, and line-analysis references.
8. A realistic dialogue with situation, relationship, register, speakers, Japanese, readings, meanings, target identification, evidence, TTS eligibility, and analysis for every turn.
9. Genuinely productive patterns only, with template, reading, function, slot constraints, valid examples, unsafe substitutions, risk notes, and analysed examples. State explicitly when no safe productive pattern exists.
10. A genuinely nearby distinction where supported, with Japanese, reading, pragmatic/register contrast, unsafe-replacement guidance, evidence, and line analysis. Do not invent cross-links to unpublished Expressions.
11. Source locators, licence/attribution route, creator identity, creation date, evidence/candidate build identities, and provenance.
12. Library fields sufficient for intention-oriented search over Japanese, kana, meaning, intention, usage/context, and alternate forms.

Recognised/Review state is not content and must not appear in the private proposal.

### Exact submitted Expression keys

For validator compatibility, each submitted slot's `expression` object uses these exact top-level keys:

- `expressionId`, `primaryLineId`, `category`, `usageSummary`, `verificationState`, `kotoDifficulty`;
- non-empty arrays `intentions`, `useWhen`, `takeCare`, `relationships`, `forms`, `responses`, `followUps`, and `sources`;
- objects `dialogue`, `patterns`, `distinctions`, `library`, `provenance`, and `japaneseLines`.

Set `verificationState` to `candidate`; never self-declare verified. Every Japanese-bearing content entry uses a `lineId` or `lineIds` reference into `japaneseLines` rather than embedding bypass text. Use `primaryLineId`, and suffix all other single/multiple references with `LineId`/`LineIds` so the validator can enforce reference closure. `patterns` and `distinctions` may record `none-supported` with an evidence-backed reason rather than inventing entries.

Evidence locators use exact non-empty keys `sourceId`, `artifact`, `locator`, and `claimScope`. The Zero-provided validator is the executable structural authority for this assignment; the richer semantic rules in this due remain mandatory even where a structural tool cannot prove them.

## Universal Japanese-line analysis

Register **every Japanese string that would be displayed anywhere on the Full Expression Card**, including the hero form, alternate forms, responses, follow-ups, every dialogue turn, pattern templates, examples, unsafe substitutions, comparisons, fragments, and other instructional Japanese. No line may bypass analysis because it appears outside the Forms section.

Every registered line must reconstruct exactly from ordered segments. Unicode span indexes use code-point offsets into the line's Japanese and reading strings, with start inclusive and end exclusive. Each line must contain:

- stable `lineId`;
- `japanese`;
- `reading`;
- contextual `meaning`;
- `ttsEligible` (false for templates with placeholders);
- evidence locators;
- ordered segments.

Each segment must contain:

- `segmentId`;
- surface and reading;
- Japanese start/end;
- reading start/end;
- contextual meaning;
- grammatical role;
- lemma and inflection where relevant, otherwise explicit null;
- all plausible canonical Vocabulary candidates;
- selected canonical destination when safe, otherwise null;
- reviewed disposition and explicit unlinked reason;
- evidence locators.

Audit selected destinations and plausible omissions. A tokenizer may support segmentation but is not attestation authority. Repeated identical lines may reuse one analysis only through a content-addressed reference whose Japanese, reading, and meaning match exactly. Templates still require component and slot analysis.

If any displayed Japanese line lacks complete evidence-backed analysis, abstain that entire slot. Never use plain unanalysed Japanese as fallback.

## Evidence and provenance rules

- Every source-derived claim needs approved evidence and a stable locator.
- Keep evidence distinct from editorial reasoning.
- Preserve source and licence restrictions.
- Do not fabricate quotations, source records, provenance, or review states.
- Do not treat a checksum, schema success, candidate label, or your own confidence as linguistic proof.
- A Vocabulary link must be canonical, exact, contextually safe, and supported; otherwise record an explicit reviewed unlinked disposition.

## Private output contract

Build one deterministic private archive, then store it with the pinned `upload-release-body-bundle` command as authenticated unpublished draft-release metadata. Do not use the unreachable release-asset upload host:

- Exact bundle name: `germinal-valkyrie1-wave001-50.tar.gz`
- Output transport: `germinal-private-body-chunk-v1` draft-release metadata through `api.github.com`
- Record all returned private chunk release IDs in the safe report
- Required archive members, in lexical order:
  - `manifest.json`
  - `slots.ndjson`
- UTF-8, LF line endings, sorted object keys, no insignificant whitespace.
- `slots.ndjson` contains exactly 50 lines ordered by slot ID.
- Gzip timestamp must be zero. Tar member owner/group IDs must be zero and member timestamps must be zero.

`manifest.json` must include assignment ID, agent name, input asset name/length/SHA-256, evidence build, candidate build, attempted count, submitted count, abstained count, failed count, archive format version `germinal-valkyrie-output-v1`, and a SHA-256 for the canonical `slots.ndjson` bytes.

Every slot object must contain `slotId` and `status`. Allowed slot statuses are `submitted`, `abstained`, or `failed`. An abstained/failed record contains only safe reason codes and no invented Expression. A submitted record contains one complete Expression object and all referenced line analyses. Use new temporary IDs scoped to this assignment; do not reuse legacy IDs.

The private Expression object must structurally account for every field required above. Use references by `lineId` from forms, responses, follow-ups, dialogue, patterns, and distinctions into one complete `japaneseLines` map. Source locators must identify source ID, artifact/member, record key or stable locator, and claim scope.

Before storage, validate exact slot count, unique IDs, reference closure, no orphan lines, no unanalysed Japanese, exact Japanese/reading reconstruction, canonical NDJSON, provenance presence, and count conservation. Structural checks remain creator-side checks, not independent proof. Package deterministically, run `upload-release-body-bundle`, and preserve its returned bundle byte length, SHA-256, and ordered private release IDs.

## Terminal discipline

Use exact API endpoints and bounded processing. No broad recursive grep, repository dumps, large payload output, sleep loops, opaque watchers, or indefinite processes. Cap diagnostics at 200 lines and 50 KiB. Default external-command timeout is 120 seconds; a declared asset transfer may use a longer bounded timeout. Never print evidence, candidate text, Expression payloads, credentials, or tokens. Stop on the first unexpected identity, digest, schema, count, or permission mismatch.

## Public report

After private metadata storage succeeds or the assignment terminates, update only `Germinal/Valkyrie/Valkyrie1/report.md`. Do not place Japanese, meanings, evidence, analyses, prompts, findings, or payload excerpts in Git. Publish it with the pinned `publish-safe-report` command so the commit reaches the remote `Germinal` branch; a local-only Git commit is not a report.

Fill the existing safe fields: assignment, agent, status, input identity, output bundle name, output byte length/SHA-256, ordered private chunk release IDs, attempted/submitted/abstained/failed counts, start/completion UTC timestamps, and a short non-content reason code if needed. Run the exact report command above and verify the returned remote commit SHA.

Your terminal status is `submitted`, `abstained`, or `failed`. `submitted` means only that the complete private candidate archive was uploaded; it does not mean passed, accepted, verified, or production-ready.
