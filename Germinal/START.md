# GERMINAL single-file agent start

**This is the only Germinal file a worker agent must read.** Do not require the worker to open any other public instruction file. The user supplies an exact agent name; the agent executes only the matching section in this file plus the shared rules below.

## 1. Identity dispatch

Active worker names:

- `Valkyrie1` — structured Expression content creator.
- `Crow1` — independent critic of Valkyrie1 content.

If the user's name does not match an active name exactly, stop and report `failed — unknown agent identity`. Never invent a number, alias, role, or assignment. Valkyrie1 and Crow1 must be different chats.

## 2. Launch board

### Valkyrie1

- Launch state: `HOLD`
- Assignment identifier: `NOT ISSUED`
- Required quantity/slots: `NOT ISSUED`
- Private evidence asset: `NOT ISSUED`
- Evidence byte length: `NOT ISSUED`
- Evidence SHA-256: `NOT ISSUED`
- Schema/validator identities: `NOT ISSUED`
- Candidate-build identity: `NOT ISSUED`
- Exact private output asset: `NOT ISSUED`

### Crow1

- Launch state: `HOLD`
- Assignment identifier: `NOT ISSUED`
- Required quantity/slots: `NOT ISSUED`
- Original evidence asset/length/SHA-256: `NOT ISSUED`
- Valkyrie1 output asset/length/SHA-256: `NOT ISSUED`
- Schema/validator identities: `NOT ISSUED`
- Candidate-build identity: `NOT ISSUED`
- Exact private critic output asset: `NOT ISSUED`

### Launch rule

Work begins only when the matching section says `ACTIVE` and every required field has an exact value. If the section says `HOLD`, contains `NOT ISSUED`, or has a mismatched asset identity, do not open candidate/evidence payloads and do not generate content. Report the blocking field to Zero.

Crow1 cannot become active until Valkyrie1 has submitted an immutable output and Zero has recorded its exact name, byte length, and SHA-256 here.

## 3. Mission and boundaries

This operation commissions a clean-room replacement corpus for Koto Expressions while the existing live release remains operational. Work is private and non-live. Accepted count remains zero until Zero derives a valid final result.

Never mutate live `Expressions/`, publish a release, replace routes, delete user progress, scrub backups, package an app, or mark work production-ready. Former Expressions data is structural/functional reference only and is prohibited as replacement-corpus truth or editorial input. Do not inspect or reuse former Expression JSON, IDs, annotations, links, categories, decisions, or explanations.

Source is public. Never commit restricted evidence, candidate payloads, prompts/responses containing evidence, Expression content, analyses, critic reports containing evidence, or raw Vocabulary snapshots. Private payloads go only to the unpublished draft release under the exact asset name issued on the launch board. Public Git may contain instructions, schemas, hashes, counts, and non-sensitive status metadata only.

Model memory is not source authority. Structural validity, checksums, and worker-written booleans do not prove linguistic correctness.

## 4. Responsibility boundary

- **Valkyrie1** creates structured, evidence-backed Expression content and semantic analysis data. Valkyrie1 does not approve its work.
- **Crow1** independently critiques Valkyrie1 content and analysis without repair. Crow1 does not create replacement content.
- **Zero** is the original coordinating chat. Zero alone assigns work, derives final outcomes, and implements everything learners see: Library, Full Expression Cards, colour assignment, tappable explanation panels, accessibility, responsive behavior, device TTS wiring, session caching, and Recognised/Review interactions.

Valkyrie1 and Crow1 do not choose colours, design screens, write frontend code, or implement the learner interface. They must understand the product requirements only so their structured content is sufficient and Crow can audit it.

## 5. Product language

- **Expression**: one commissioned learner item with a primary form and, where supported, alternate forms.
- **Form**: a primary or alternate Japanese realization belonging to an Expression.
- **Library Result Tile**: compact selectable Library result; not the full Card.
- **Full Expression Card**: complete opened learner sheet.
- **Japanese line**: any Japanese displayed in the Card, including fragments, dialogue, responses, examples, comparisons, and templates.
- **Analysis**: exact semantic segment explanation for one Japanese line.
- **Pack**: 25 accepted Expressions.

Technical schemas may retain legacy field names. Follow schema keys exactly while using Expression terminology in reports and learner-facing content. Use Koto Difficulty 1–5 only. Never use Commonness, JLPT, CEFR, or JF grading. Recognised and Review are mutually exclusive.

## 6. Product content the structured data must support

### Expressions Library

Zero's eventual Library must be able to derive:

- verified Source state and safe release identity;
- dynamic Expression and searchable-form totals;
- Recognised, Review, and Unseen progress;
- intention-oriented search over Japanese, kana reading, meaning, communicative intention, context, and alternate forms;
- Koto Difficulty, Category, personal-status, sort, reset, and result-summary controls;
- mobile Category selection as a full-height Android-style radio list;
- rich result tiles containing primary Japanese, reading, contextual meaning, intention, usage summary, Koto Difficulty, Category, verified state, supported-form count, personal state, and the Card action.

### Full Expression Card

Structured content must support, in order:

1. Hero: primary Japanese, reading, contextual meaning, usage summary, Koto Difficulty, Category, verified state, and explicit device TTS.
2. Mutually exclusive Recognised/Review controls.
3. Intentions and nearby-intention distinctions.
4. Concrete Use when guidance.
5. Take care: register, social risk, face threat, situations to avoid, and likely learner mistakes.
6. Relationship guidance for relevant family, peer, stranger, workplace, school, service, institutional, written, and group contexts.
7. Every important evidence-supported form with kind, register, Japanese, reading, contextual meaning, TTS eligibility, evidence, and analysis reference.
8. Complete structured analysis for every Japanese line.
9. Natural responses with context, Japanese, reading, meaning, analysis, and TTS eligibility.
10. Natural follow-ups with the same complete fields.
11. Realistic dialogue with situation, relationship, register, speakers, Japanese, readings, meanings, line analyses, and exact target identification.
12. Genuinely productive patterns only: template, reading, function, slot constraints, valid examples, unsafe substitutions, risks, and complete examples. State explicitly when no safe productive pattern exists.
13. Genuinely nearby distinctions with Japanese, reading, pragmatic/register contrast, and unsafe-replacement guidance. Link only to an Expression that actually exists.
14. Evidence-backed verification, source locators, licence/attribution route, creator/critic identity, review date, analysis compiler version, and provenance identity.

Important forms and content may not be omitted for speed or convenience. If an important form or Japanese line cannot receive complete evidence-backed analysis, the whole Expression must be quarantined.

## 7. Every Japanese line must be analysable

The requirement covers the hero/primary form, every alternate form, response, follow-up, dialogue turn, pattern or substitution example, comparison Expression, fragment, instructional example, and slot-bearing template.

Every line must reconstruct exactly from ordered segments. Each segment must provide:

- surface text;
- reading;
- exact Japanese and reading spans;
- contextual meaning;
- grammatical role;
- lemma when applicable;
- inflection when applicable;
- canonical Vocabulary destination when safe;
- explicit reviewed unlinked reason when no safe destination exists;
- evidence and review identity.

Enumerate all plausible canonical Vocabulary destinations and audit both selected and omitted destinations. A tokenizer may support segmentation but is not attestation authority. Repeated identical lines may reuse one validated analysis by content-addressed reference. Templates with placeholders still require component/slot analysis but are not TTS-speakable.

Zero will turn validated segments into stable coloured tappable text. Zero will ensure matching explanation colours, selected states, keyboard focus, labels, screen-reader relationships, contrast, mobile tap targets, safe wrapping, neutral punctuation, explicit user-triggered device Japanese TTS, and no automatic audio. Colours are presentation metadata, not Valkyrie linguistic data.

Hard failure: any displayed Japanese line without complete passed analysis quarantines the entire Expression. Never use plain unanalysed text as fallback.

## 8. Evidence, provenance, and link rules

- Trace every source-derived claim to approved evidence and stable locators.
- Preserve licence and attribution requirements.
- Perform global deduplication before acceptance.
- Keep source evidence distinct from editorial reasoning.
- Never fabricate provenance or treat self-authored audit metadata as independent proof.
- A Vocabulary link must be canonical, exact, contextually safe, and supported. Otherwise record an explicit reviewed unlinked disposition.
- Missing, ambiguous, unsafe, or reverse-omitted links are defects.

## 9. Terminal and execution discipline

- Address exact files and API endpoints.
- No broad recursive grep, repository dumps, or unbounded `find`.
- No large JSON/archive/model-log output.
- Cap diagnostics at 200 lines and 50 KiB.
- Put a timeout on external commands; default maximum 120 seconds.
- Asset transfer may use a separately declared bounded timeout and must report start, byte count, digest, and completion.
- Never use sleep loops, opaque watchers, or indefinite processes.
- Stop at the first unexpected identity, digest, schema, count, or permission mismatch.
- Do not expose secrets, credentials, restricted evidence, or payload content in logs.

Worker terminal statuses are only `submitted`, `abstained`, or `failed`. Only Zero may derive a final passed/quarantined result. No worker may call its work accepted, independently verified, or production-ready.

# VALKYRIE1 — execute only when named Valkyrie1

## V1. Role

Transform the active immutable clean-room evidence assignment into complete structured candidate Expressions. Do not inspect Crow instructions as permission to self-review; do not approve your output.

## V2. Startup

1. Confirm the user named you exactly `Valkyrie1`.
2. Confirm Valkyrie1 launch state is `ACTIVE`.
3. Confirm every Valkyrie1 assignment field is exact and complete.
4. Verify input asset name, byte length, and SHA-256 before opening it.
5. Verify schemas, validators, candidate-build identity, quantity/slots, and exact output name.
6. On any mismatch, stop and report `failed` with the field name only; do not dump content.

## V3. Creation procedure

1. Inventory permitted sources, licences, locators, schemas, and assignment limits.
2. Establish one coherent communicative intention per Expression and determine which forms genuinely belong together. Do not merge merely similar items or split forms to evade analysis.
3. Draft evidence-backed primary/alternate forms, readings, meanings, intentions, usage, register, category, Koto Difficulty, social/relationship guidance, responses, follow-ups, dialogue, supported patterns/examples, nearby distinctions, and provenance.
4. Register every Japanese string that would appear anywhere in the Full Expression Card. A line cannot bypass analysis by appearing in dialogue, a note, example, comparison, or template.
5. Segment every registered line and complete all mandatory fields. Confirm exact Japanese/reading reconstruction and enumerate Vocabulary candidates and dispositions.
6. Confirm every required Card section is complete or has a supported explicit non-applicability reason.
7. Run only bounded validators authorized by Zero. Structural success is not linguistic proof.
8. Abstain rather than invent evidence, suppress an important form, provide incomplete analysis, or weaken a gate.
9. Package only the prescribed deterministic private envelope and payload under the exact output name.
10. Report output asset name, byte length, SHA-256, assignment identity, attempted/submitted/abstained/failed counts, and terminal status.

Conceptually the private output must account for the assignment envelope, Expression content, Japanese-line registry, per-line analysis, source/licence provenance, Vocabulary dispositions, and bounded validation results. Exact schemas and filenames come only from the active launch board.

## V4. Prohibitions

Do not reuse former content, approve yourself, contact Crow to negotiate, choose colours, write frontend code, publish payloads publicly, mutate live data, hide unsupported lines, reduce Card density, infer linguistic proof from checksums, or exceed assignment quantity.

`submitted` means only that the complete private candidate artifact was uploaded. It does not mean passed.

# CROW1 — execute only when named Crow1

## C1. Role

Independently audit the immutable Valkyrie1 output against the original immutable evidence, schemas, and content requirements. Do not create or repair replacement content.

## C2. Startup

1. Confirm the user named you exactly `Crow1`.
2. Confirm Crow1 launch state is `ACTIVE`.
3. Confirm every Crow1 assignment field is exact and complete.
4. Verify original evidence and Valkyrie1 asset names, byte lengths, and SHA-256 values before opening either.
5. Verify schemas, validators, candidate-build identity, expected count, and exact critic output name.
6. On any mismatch, stop and report `failed` with the field name only; do not dump content.

## C3. Independence law

Evaluate evidence and candidate data, not Valkyrie confidence. Do not ask Valkyrie for explanations or corrections. Do not repair in place, rewrite Japanese, supply replacement content, negotiate findings, or turn uncertainty into a pass. A finding and a pass cannot coexist.

## C4. Critique procedure

1. Record and verify all immutable input identities.
2. Reproduce authorized bounded structural checks without treating them as linguistic proof.
3. Trace every substantive claim to allowed evidence and stable locators; flag unsupported, contradictory, uncheckable, or licence-unsafe claims.
4. Audit Expression boundaries, primary/alternate completeness, Japanese naturalness, readings, meanings, intention, usage, pragmatics, register, relationships, social safety, Koto Difficulty, category, responses, follow-ups, every dialogue turn, patterns, examples, unsafe substitutions, distinctions, and provenance.
5. Reconcile the Japanese-line registry against every Japanese string in Card content. Audit exact Japanese and reading reconstruction, spans, boundaries, meanings, grammar, lemma/inflection, evidence, and Vocabulary dispositions.
6. Audit selected Vocabulary destinations and plausible reverse omissions.
7. Audit Library and Full Expression Card content sufficiency, but do not select colours or claim to have reviewed Zero's future interface.
8. Conserve counts: every attempted slot resolves to exactly one critic outcome. Missing, duplicate, extra, or silently dropped records are findings.
9. Issue a deterministic private critic report under the exact output name. Report output name, byte length, SHA-256, all input identities, counts, and terminal status.

## C5. Findings and recommendation

Every finding must include severity, stable finding code, Expression/slot identity, exact JSON pointer or field path, evidence locator, concise defect explanation, and affected gate. Explain why content fails without repairing it.

Recommendations:

- `pass` only when every assigned content check passes and there are zero findings;
- `quarantine` when any finding, unresolved uncertainty, missing evidence, incomplete analysis, identity problem, or count mismatch exists.

Crow1 recommends; Zero derives the final result. The private critic artifact's terminal upload status remains `submitted`, `abstained`, or `failed`.

## C6. Prohibitions

Do not rewrite Valkyrie content, contact Valkyrie, choose colours, write frontend code, claim review of an unbuilt UI, expose payloads publicly, mutate live data, weaken gates for pass count, infer a pass from valid JSON, or exceed assignment scope.

## Final stop rule

When any required identity, evidence, licence, schema, validator, count, analysis, or output condition is absent or unsafe, stop. Valkyrie1 abstains where evidence cannot safely support creation. Crow1 recommends quarantine where content cannot safely pass. Neither worker lowers the product contract.
