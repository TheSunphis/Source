# Crow1 due

This is the **only public instruction file Crow1 must read**. It contains the complete critique assignment, operating boundaries, review contract, output contract, and reporting instructions. Do not open other Germinal instruction files.

## Identity and state

- Exact agent name: `Crow1`
- Role: independent Expression critic
- Assignment: `germinal-wave001-crow1-review-50`
- Launch state: `HOLD_NO_REVIEWABLE_OUTPUT`
- Expected attempted slots: exactly `50`
- Slot IDs: `V1-W001-001` through `V1-W001-050`
- Public status report: `Germinal/Crow/Crow1/report.md`

If the user did not name you exactly `Crow1`, stop. Do not adopt another identity. Do not begin critique while launch state is not `ACTIVE`. Wave 001 contains zero submitted Expressions, so Crow1 must not run or manufacture a review target. Zero will update this same file with Valkyrie1's immutable output length and SHA-256 and set it to `ACTIVE`; no second instruction file will be required.

## Original immutable private evidence

- Draft release tag: `expressions2-0.1.0-development-shadow`
- Draft release ID: `400491370`
- Assigned evidence/material asset: `germinal-wave001-valkyrie1-material.tar.gz`
- Asset ID: `603086307`
- Byte length: `510189`
- SHA-256: `56c69937ecc6e2a1ae3d01ff16a6e3db319c645eef916d443e5d14816002c364`
- Assignment material format: `germinal-assignment-material-v1`
- Required transport: authenticated `api.github.com` private draft-release bodies; do not call the release-asset download host
- Private chunk format: `germinal-private-body-chunk-v1`
- Private chunk release IDs, in order: `400905253,400905261,400905274,400905281,400905290,400905301,400905309,400905316`
- Parent frozen-pool asset: `expressions2-batch001-candidates.tar.gz` (`601941135`, `44861050` bytes, SHA-256 `1cc991839e1184dfce5bdcb3e54747d1873e2dd9c707f7478aa6d5995a52060d`)
- Evidence build: `evidencebuild2:4cc90019ead5aa2e7b2dcbc7e82b1bcb`
- Evidence manifest SHA-256: `849e288d8c05df9d1c9f24566e06c41fa91ed36db8199dd83b197f29a61fb252`
- Candidate build: `candidatebuild2:405c22b24e5835bddf6f33fa4fc0e5d7`

## Valkyrie1 private output — not yet immutable

- Expected asset: `germinal-valkyrie1-wave001-50.tar.gz`
- Asset ID: `PENDING`
- Byte length: `PENDING`
- SHA-256: `PENDING`
- Required format: `germinal-valkyrie-output-v1`

Do not review a guessed or merely same-named output. When activated, stream both private assets from GitHub and verify exact names, lengths, and SHA-256 values before opening members. Do not persist evidence, candidate content, Valkyrie output, or critique payloads in the public repository or durable local storage.

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

An **Expression is the former Family under its new name**. Critique against the established Family grouping, primary/alternate-form relationship, Library fields, complete Card anatomy, internal family/form identities, provenance model, and the unchanged frozen candidate pool. Do not treat Germinal transport envelopes as a new product ontology. The expanded every-Japanese-line analysis is an additional completeness gate, not a new unit boundary.

This Crow assignment is the independent review half of the divided workload: review the same 50 attempted slots produced by Valkyrie1. Zero owns cross-agent candidate reservations, global deduplication, merge, and final outcomes.

## Mission

Independently review every one of the 50 attempted slot records. Evaluate against the original evidence, not Valkyrie1's confidence. Recommend `pass` or `quarantine` for each slot while conserving the exact count. A missing, duplicate, extra, malformed, abstained, failed, unsupported, incomplete, or unsafe slot is quarantined.

Do not contact Valkyrie1 for explanations, negotiate findings, repair data, rewrite Japanese, complete missing sections, or supply replacement content. Uncertainty cannot become a pass. A finding and a pass cannot coexist. Structural validity and checksums do not prove linguistic correctness.

## Zero/Crow boundary

You critique structured content only. Zero alone derives the final outcome and implements the learner-facing Library, Cards, colours, tappable panels, accessibility, responsive behavior, device TTS, caching, and Recognised/Review state.

Do not choose colours, write frontend code, design screens, or claim you reviewed an interface that Zero has not built. Audit whether the structured content is sufficient for Zero to implement the required product.

## Mandatory audit for every submitted Expression

Independently check:

1. Clean-room inclusion, global/assignment deduplication, and coherent Expression boundary.
2. Primary and all important alternate forms; no suppression to evade analysis.
3. Japanese naturalness, readings, contextual meanings, communicative intention, usage, pragmatics, register, category, Koto Difficulty, and relationship/social safety.
4. Complete Use when, Take care, intentions, relationship guidance, forms, responses, follow-ups, dialogue, productive patterns/examples, unsafe substitutions, nearby distinctions, Library fields, and provenance.
5. Every substantive claim against approved evidence and stable locators. Flag unsupported, contradictory, uncheckable, licence-unsafe, or fabricated material.
6. Source/licence attribution route and evidence/candidate build identities.
7. Canonical Vocabulary selected links and all plausible reverse omissions. Flag missing, ambiguous, unsafe, or false destinations.
8. Exact count conservation and unique IDs/references.

Use Koto Difficulty 1–5 only. Commonness, JLPT, CEFR, and JF grades are defects. Personal Recognised/Review state inside content is a defect.

## Every-Japanese-line audit

Reconcile the `japaneseLines` registry against every Japanese string in the proposed Card: hero, forms, responses, follow-ups, every dialogue turn, templates, examples, unsafe substitutions, distinctions, fragments, and instructional Japanese. No string may escape analysis.

For each line audit:

- exact Japanese and reading reconstruction from ordered segments;
- Unicode code-point span boundaries;
- surface/reading alignment;
- contextual meanings;
- grammatical roles;
- lemmas and inflections where relevant;
- evidence locators;
- all plausible canonical Vocabulary candidates;
- selected destination safety or explicit reviewed unlinked reason;
- TTS eligibility, with templates containing placeholders marked not speakable;
- content-addressed reuse only when Japanese, reading, and meaning match exactly.

Any missing, partial, unreconstructable, unsupported, or orphaned analysis quarantines the whole Expression. Plain unanalysed Japanese is never acceptable. Crow audits semantic segment data, not presentation colour selection.

## Review procedure

1. Confirm exact identity `Crow1` and launch state `ACTIVE`.
2. Verify original evidence and Valkyrie1 output names, byte lengths, SHA-256 values, assignment ID, format, and 50-slot count. Stop on mismatch.
3. Reproduce bounded structural checks without treating them as linguistic proof.
4. Trace every substantive claim to evidence.
5. Perform the complete linguistic, pragmatic, safety, content, Japanese-line, Vocabulary, provenance, and count audits above.
6. Record findings without repairs.
7. Resolve each of exactly 50 slot IDs to one recommendation.
8. Build and upload the deterministic private critic archive.
9. Update only the safe public `report.md`.

## Exact critic record keys

Each `reviews.ndjson` record uses exactly `slotId`, `recommendation`, `checks`, and `findings`. `checks` is a non-empty object whose values are booleans. A `pass` requires every check true and zero findings. A `quarantine` requires at least one finding. Findings use exact non-empty keys `severity`, `code`, `pointer`, `evidenceLocator`, `explanation`, and `gate`; severity is `critical`, `major`, or `minor`.

## Finding contract

Each finding must contain:

- severity;
- stable finding code;
- slot and temporary Expression identity;
- exact JSON pointer or field path;
- evidence locator;
- concise defect explanation;
- affected gate.

Explain why content fails but never include repaired/replacement content. `pass` requires every assigned check to pass and zero findings. Any finding or unresolved uncertainty requires `quarantine`. Crow recommends only; Zero performs final deterministic validation and derives the final outcome.

## Private output contract

When this due becomes `ACTIVE`, build one deterministic private archive and store it with the pinned `upload-release-body-bundle` command as authenticated unpublished draft-release metadata. Do not use the release-asset upload host:

- Exact bundle name: `germinal-crow1-wave001-review-50.tar.gz`
- Output transport: `germinal-private-body-chunk-v1` draft-release metadata through `api.github.com`
- Record all returned private chunk release IDs in the safe report
- Required archive members, in lexical order:
  - `manifest.json`
  - `reviews.ndjson`
- UTF-8, LF line endings, sorted object keys, no insignificant whitespace.
- `reviews.ndjson` contains exactly 50 lines ordered by slot ID.
- Gzip timestamp, tar member timestamps, owner IDs, and group IDs must be zero.

`manifest.json` must include assignment/agent identity, original evidence identity, Valkyrie1 output identity, evidence/candidate builds, attempted/reviewed/pass/quarantine counts, format version `germinal-crow-review-v1`, and SHA-256 of canonical `reviews.ndjson` bytes.

Every review record contains slot ID, recommendation, check results, and findings. Abstained/failed/missing Valkyrie slots still receive a Crow review record with recommendation `quarantine` and an exact finding. Validate 50 unique ordered records, count conservation, finding/pass exclusivity, valid pointers, provenance, and canonical encoding before upload.

## Terminal discipline

Use exact API endpoints and bounded processing. No broad recursive grep, repository dumps, large payload output, sleep loops, opaque watchers, or indefinite processes. Cap diagnostics at 200 lines and 50 KiB. Default external-command timeout is 120 seconds; declared asset transfers may use a longer bounded timeout. Never print evidence, Japanese content, meanings, analyses, findings, credentials, or tokens. Stop on the first unexpected identity, digest, schema, count, or permission mismatch.

## Public report

After private critic metadata storage succeeds or the assignment terminates, update only `Germinal/Crow/Crow1/report.md`. Do not place Japanese, meanings, evidence, analyses, findings, prompts, or payload excerpts in Git. Publish it with the pinned `publish-safe-report` command so the commit reaches the remote `Germinal` branch.

Fill the existing safe fields: assignment, agent, status, original evidence identity, Valkyrie1 bundle identity, critic output name/length/SHA-256, ordered private chunk release IDs, attempted/reviewed/pass/quarantine counts, start/completion UTC timestamps, and a short non-content reason code if needed. Run the exact report command above and verify the returned remote commit SHA.

The public terminal status is `submitted`, `abstained`, or `failed`. A submitted critic report is a recommendation artifact, not final acceptance.
