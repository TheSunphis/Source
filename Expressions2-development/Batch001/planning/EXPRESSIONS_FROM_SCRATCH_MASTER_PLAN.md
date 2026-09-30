# Koto Expressions: From-Scratch Industrial Rebuild Master Plan

**Plan status:** Proposed; no compiler or replacement corpus implementation has started  
**Planning date:** 2026-09-30  
**Target:** A new, evidence-backed Expressions corpus and confidence-gated compiler that can scale toward 100,000 families  
**Transition:** Atomic replacement after the approved launch gates pass

---

## 1. Decision record

The following user decisions control this plan:

1. The existing Expressions corpus and analysis lineage will not be repaired or extended.
2. The new corpus starts from zero and may retain only the product’s structural behaviour: searchable families, Koto Difficulty, rich family sheets, Japanese device TTS, and mutually exclusive Recognised/Review state.
3. The former 260-family public Source dataset will be removed at final cutover.
4. Existing `expression_progress` rows will be permanently deleted at final cutover, with no old-to-new mapping.
5. Cutover occurs only after the replacement passes its approved gates.
6. The `.85` and `.86` standalone packages have been retired and deleted.
7. The production method must be industrial. Family-by-family manual annotation cannot be the main scaling mechanism.

The current 260-family Source release remains temporarily operational only because current Koto still depends on it. It is not replacement input authority.

---

## 2. Executive strategy

### **Recommended foundation**

Build a **broad, attested expression-family corpus** through an **evidence-first hybrid pipeline**:

- Evidence establishes that a reusable expression exists.
- Deterministic extraction and language tooling produce candidates.
- Models may classify, cluster, draft, compare, and explain candidates.
- Models cannot grant publication authority merely because output sounds plausible.
- Hard invariants, independent checks, calibrated confidence, duplicate detection, and licence gates determine whether a record publishes.
- Ambiguous material is quarantined rather than guessed.
- Human or expert review is concentrated on benchmark creation, sampled audits, high-risk language, and exceptions—not every family.

This turns quality work into factory design and quality control instead of repeating artisanal production 100,000 times.

---

## 3. Product constitution

### 3.1 What may count as a family

A family is one reusable conventional Japanese unit with a stable communicative, grammatical, social, idiomatic, or collocational function.

Included classes:

1. Social and interactional formulas
2. Requests, offers, refusals, permissions, acknowledgements, and reactions
3. Discourse-management routines
4. Productive grammar constructions
5. Conventional collocations
6. Idioms and fixed expressions
7. Proverbs and sayings
8. Register-bound workplace, school, service, written, and institutional formulas
9. Reusable sentence frames with constrained substitution slots
10. Conventional pragmatic patterns whose meaning is not safely reducible to isolated Vocabulary items

Excluded classes:

- arbitrary example sentences;
- one-off quotations;
- isolated ordinary words that belong in Vocabulary;
- spelling variants treated as separate families;
- politeness or conjugation variants counted as separate families;
- generated sentences without independent evidence;
- person-, organization-, product-, or event-specific phrases without general reusable function;
- near-duplicates created solely to inflate totals.

### 3.2 Family identity rule

Forms belong to one family when they share the same core intention and substitution behaviour and differ mainly by register, politeness, orthography, contraction, or conventional wording.

A form becomes a separate family only when at least one of these changes materially:

- pragmatic intention;
- grammatical construction;
- social risk;
- substitution constraints;
- semantic scope;
- expected response behaviour.

### 3.3 Required learner experience

The new system must preserve the recognizable Expressions workflow:

- search by Japanese, reading, meaning, intention, and context;
- filter by Koto Difficulty, category, and personal status;
- open a rich family sheet;
- compare forms and register;
- read use/avoid/relationship guidance;
- view responses, follow-ups, patterns, comparisons, and context;
- listen using a Japanese device voice only;
- mark the new family as either Recognised or Review.

“Same structure and working” does not require retaining old content, IDs, Source schema, pack layout, or internal compiler design.

---

## 4. Clean-room boundary

The replacement begins with an empty family ledger and new authorities.

The compiler must not import:

- old family JSON records;
- old family IDs or slugs;
- former candidate assignments;
- old editorial decisions or batch audits;
- old segment annotations;
- old Vocabulary resolutions;
- old generated explanations;
- old review-status labels.

Build enforcement:

1. New corpus paths and namespaces cannot read legacy Expressions paths.
2. CI scans replacement manifests and provenance for legacy family IDs and prohibited file hashes.
3. A source-lineage record is required for every new candidate.
4. No historical record may enter a benchmark unless the user separately authorizes that use.
5. Historical public Git commits remain history, but they are not compiler inputs.

---

## 5. Source strategy and licence gates

### 5.1 Source classes

Every source receives one of four permissions:

- **Redistributable:** source-derived material may be published under its licence.
- **Evidence-only:** may support existence or usage, but source wording cannot be copied.
- **Tool-only:** may tokenize, normalize, or classify; its dictionary entries are not published as corpus content.
- **Prohibited:** may not be acquired, scraped, processed, or used.

No acquisition starts until a source-registry entry records URL, exact version/date, checksum, licence, attribution, permitted transformations, redistribution status, and update policy.

### 5.2 Recommended initial source portfolio

#### Green: suitable for formal evaluation

- **JMdict/EDRDG:** lexical expressions, readings, senses, labels, and canonical Vocabulary identity. EDRDG states that its covered dictionary files are CC BY-SA 4.0, permits commercial use under the conditions, requires attribution, and requires an update procedure for software using the files. [1](https://www.edrdg.org/edrdg/licence.html)
- **Tatoeba/Tanaka:** attestation and sentence-pattern evidence. Tatoeba’s official downloads page says the distributed files are CC BY 2.0 FR, a subset is CC0, and many Japanese/English sentences originate in the public-domain Tanaka Corpus. Every sentence must retain its own source/licence identity rather than being treated as uniformly public domain. [1](https://tatoeba.org/en/downloads)
- **Wiktionary dumps:** idiom, phrase, proverb, and lexical candidate evidence. Wiktionary text is CC BY-SA 4.0/GFDL, but entries can contain externally sourced material under separate terms, so extraction must exclude quotations and separately licensed media. [1](https://en.wiktionary.org/wiki/Wiktionary:Copyrights)
- **Japanese WordNet:** semantic grouping and duplicate detection. Its project states that the data may be used, copied, modified, and distributed without a fee while preserving its licence. [1](https://bond-lab.github.io/wnja/eng/index.html)
- **Sudachi/SudachiDict:** tool-only tokenization and morphological candidate generation. SudachiDict identifies Apache 2.0 licensing and separately records included components in its legal notices. [1](https://github.com/WorksApplications/SudachiDict)
- **Modern UniDic under an explicitly selected free licence:** tool-only morphology. NINJAL describes free GPL/LGPL/BSD options as well as separate CC BY-NC-SA editions; the exact downloaded edition and licence must be pinned. [2](https://unidic.ninjal.ac.jp/faq)
- **Japanese government open content:** potential formal-register evidence only after per-site rights verification. The Digital Agency’s current Public Data License 1.0 says covered content may be used under CC BY 4.0, while third-party rights and site-specific exclusions remain the user’s responsibility. [1](https://www.digital.go.jp/en/resources/open_data/public_data_license_v1.0)

#### Amber: not approved for automatic ingestion

- **BCCWJ/NINJAL-LWP:** valuable linguistic reference, but the public terms restrict use to research/education, require consultation for commercial use, and prohibit reproducing search results. It must not be scraped or copied into Koto without a separate written licence and approved extraction protocol. [1](https://nlb.ninjal.ac.jp/search/)
- **NWJC/Bonten:** not an ingestion source under its public browser terms; available terms prohibit programmatic access/scraping and demand deletion of content acquired that way. [3](https://masayu-a.github.io/NWJC/bonten-note)
- Any paid or contract corpus until its agreement is reviewed against public redistribution, commercial use, model use, and derivative-output clauses.

#### Red: prohibited by default

- unlicensed subtitle dumps;
- scraped social networks, forums, or search results;
- copyrighted commercial dictionaries without a redistribution agreement;
- content with unclear author rights;
- personal messages or learner data;
- sources whose terms prohibit automated access;
- model-generated material presented as attestation.

### 5.3 Licence output policy

**Recommended:** publish the replacement dataset under CC BY-SA 4.0, with machine-readable per-record provenance and a generated attribution bundle. This is compatible with likely core sources such as JMdict and Wiktionary, but a final licence review is still required.

No model prompt may include evidence that the source registry marks non-transformable or prohibited.

---

## 6. Replacement data architecture

### 6.1 Separate four authorities

1. **Source registry** — what inputs are permitted and pinned
2. **Candidate ledger** — extracted evidence and unresolved candidates
3. **Editorial family records** — learner-facing family meaning and usage
4. **Compiled analysis layer** — deterministic per-form segments and canonical links

The analysis layer is derived and replaceable. It must never become the authority for family existence or learner state.

### 6.2 Recommended identity model

Use a new namespace to make accidental legacy-state attachment impossible.

Provisional format:

```text
expression2:<opaque-stable-id>
```

Keep a human-readable slug as metadata, not primary identity. IDs are assigned once by the candidate ledger and never derived solely from mutable Japanese text.

This remains a decision gate: UUIDv7, monotonic opaque IDs, and content-addressed IDs must be compared before implementation.

### 6.3 Family schema v2

Each publishable family should contain:

```text
id
slug
revision
publicationStatus
familyClass
kotoDifficulty
category
intentions[]
primary { japanese, reading, meaning, deviceTts }
forms[] { id, japanese, reading, meaning, register, label, evidence[] }
usage {
  summary,
  useWhen[],
  avoidWhen[],
  suitableRelationships[],
  socialRisk,
  regionalOrHistoricalLimits[]
}
responses[]
followUps[]
dialogue[]
patterns[]
comparisons[]
searchAliases[]
sourceEvidence[]
provenance
review
compiler
```

Required provenance includes:

- source IDs and immutable checksums;
- extraction rule/model and version;
- evidence locators that do not reproduce prohibited text;
- compiler version;
- confidence calibration version;
- deterministic audit results;
- review type: automated, agent editorial, human editorial, or verified hybrid;
- timestamps and release batch.

### 6.4 Analysis schema v2

For each exact form:

```text
familyId
formId
japanese
reading
segments[] {
  surface,
  reading,
  role,
  contextualMeaning,
  lemma,
  inflection,
  vocabularyCandidateSet[],
  selectedVocabularyId | null,
  noLinkReason | null,
  evidence[],
  confidenceClass
}
reconstructionHash
compilerVersion
verification
```

### Binding published-form analysis requirement

Every primary or alternate form displayed in a VERIFIED Full Family Card must have complete, passed sentence analysis. Never display a partially trusted mixture or a learner-visible unanalysed published form.

A candidate alternate may be excluded only when evidence/family-boundary adjudication concludes it is not an accepted form—not merely because analysis is difficult. A known important form with unresolved analysis quarantines the family until resolved.

Responses, follow-ups, dialogue lines, and examples retain Japanese, reading, meaning, and TTS but are not automatically counted as published family forms.

---

## 7. Industrial pipeline

### Stage A — Acquire and freeze

- Download only approved sources.
- Record source version, date, URL, licence, bytes, and SHA-256.
- Store source snapshots outside runtime payloads.
- Reject changed upstream bytes unless a maintainer explicitly approves a source refresh.

### Stage B — Generate candidates

Independent candidate channels:

1. dictionary phrase/idiom labels;
2. corpus n-grams with dispersion and contextual diversity;
3. syntactic and morphological frames;
4. interactional formula patterns;
5. collocation association measures;
6. proverb/idiom/reference categories;
7. register-specific government/institutional language;
8. model proposals only when they are subsequently grounded by approved evidence.

Each candidate retains all evidence; no early destructive merging.

### Stage C — Normalize

- Unicode and punctuation normalization without losing display form
- orthographic variant grouping
- kana/kanji correspondence
- lemma and inflection normalization
- politeness and register features
- slot detection
- negative-form and tense handling
- named-entity and one-off sentence rejection
- source-language contamination rejection

### Stage D — Cluster families

Use a graph, not one similarity score.

Edges may represent:

- exact normalized form;
- reading identity;
- paraphrase evidence;
- shared grammatical frame;
- shared intention;
- register variant;
- inflection/contraction relation;
- semantic embedding similarity as candidate evidence only.

Hard split rules prevent merging expressions with different intentions, social risk, substitution behaviour, or expected responses.

Every merge records reasons. Every automated merge must be replayable.

### Stage E — Deduplicate

Use multi-pass deduplication:

1. exact string/reading;
2. normalized morphology;
3. template equivalence;
4. semantic/pragmatic nearest neighbours;
5. cross-batch duplicate search;
6. contradiction search;
7. independent adjudicator.

No batch can publish until it is compared with the complete new-corpus ledger, not just its own batch.

### Stage F — Compile family content

Draft the learner-facing record from evidence. Require independent passes for:

- Japanese naturalness;
- reading;
- contextual English meaning;
- intention;
- register and relationship risk;
- substitution safety;
- responses/follow-ups;
- dialogue consistency;
- comparisons;
- Koto Difficulty.

A second process critiques rather than merely regenerates the first output. The verifier receives evidence and candidate output but not the first model’s hidden reasoning.

### Stage G — Compile form analysis

1. Enumerate segmentation hypotheses.
2. Require exact surface reconstruction.
3. Require exact reading reconstruction.
4. Generate all plausible canonical Vocabulary candidates from surface, reading, lemma, inflection, orthography, and approved honorific paths.
5. Validate selected IDs against the pinned canonical Vocabulary catalogue.
6. Run the reverse check: for every segment, ask whether a valid canonical candidate was omitted.
7. Explain or quarantine every unresolved ambiguity.
8. Publish analysis only if the whole form passes.

### Stage H — Score and gate

Do not use one weighted average that can hide a critical failure.

Hard gates must all pass:

- source/legal eligibility;
- schema validity;
- exact Japanese reconstruction;
- exact reading reconstruction;
- canonical ID validity;
- no unresolved contradiction;
- no prohibited source text;
- no duplicate above the adjudication threshold;
- required family content complete;
- safety/register checks complete;
- deterministic rebuild identity.

Calibrated dimensions are evaluated separately:

- attestation confidence;
- family-boundary confidence;
- naturalness confidence;
- reading confidence;
- meaning confidence;
- register/social-risk confidence;
- duplicate-separation confidence;
- analysis confidence;
- canonical-link completeness confidence.

A low score in one critical dimension cannot be offset by high scores elsewhere.

### Stage I — Quarantine

Quarantine reasons are structured, not free-text only:

- insufficient evidence;
- conflicting readings;
- unclear family boundary;
- likely duplicate;
- register conflict;
- unnatural or translation-shaped Japanese;
- ambiguous canonical link;
- licensing uncertainty;
- historical/regional uncertainty;
- unsafe substitution pattern;
- incomplete reverse-link audit.

Quarantined records remain resumable work units. They do not block unrelated high-confidence families.

### Stage J — Publish

- Sort deterministically.
- Partition into immutable packs.
- Generate compact search indexes.
- Produce manifest counts and hashes.
- Emit attribution and licence bundles.
- Rebuild from clean inputs and compare byte-for-byte.
- Sign release identity through immutable Git commit and tag.

---

## 8. Confidence calibration and quality proof

### 8.1 New benchmark only

Construct a new benchmark independently from approved sources. Do not reuse former Expressions records.

Recommended benchmark composition:

- all family classes;
- all five Koto Difficulty levels;
- polite, casual, formal, written, workplace, service, and intimate registers;
- kana-only, kanji-heavy, mixed-script, contraction, idiom, and grammar forms;
- easy and adversarial duplicate pairs;
- positive and negative canonical Vocabulary links;
- no-link cases;
- ambiguous segmentation and reading cases;
- socially risky and context-sensitive expressions.

Keep separate:

1. development set;
2. calibration set;
3. sealed holdout set;
4. post-release audit samples.

### 8.2 Truthful reviewer labels

- Automated checks remain “automated.”
- Agent editorial review remains “agent editorial.”
- Human review may be claimed only when a human actually performed it.
- Verification describes the exact verified properties; it never implies universal correctness.

### 8.3 Provisional service-level objectives

These are recommendations to approve or revise before implementation:

| Property | Proposed gate |
|---|---:|
| Schema/provenance completeness | 100% |
| Exact Japanese reconstruction | 100% |
| Exact reading reconstruction | 100% |
| Invalid canonical Vocabulary IDs | 0 |
| Known unresolved source/licence conflicts | 0 |
| Deterministic rebuild mismatch | 0 |
| Critical register/safety defect in release audit | 0 |
| Wrong canonical-link audit rate | 95% upper confidence bound below 0.1% |
| Duplicate-family audit rate | 95% upper confidence bound below 0.5% |
| Naturalness/meaning severe-defect rate | 95% upper confidence bound below 0.5% |

With zero observed defects, approximately 3,000 independent audited items are needed merely to place the rule-of-three 95% upper bound near 0.1%. Deterministic full-corpus invariants therefore carry most of the scale; sampling estimates properties that cannot be proven mechanically.

### 8.4 Drift checks

Recalibrate whenever any of these changes:

- source version;
- tokenizer or dictionary;
- model or prompt;
- candidate extraction;
- clustering;
- confidence model;
- canonical Vocabulary release;
- schema;
- family taxonomy.

No threshold transfers automatically across a changed pipeline.

---

## 9. Scale and release ladder

The compiler must prove quality and throughput in bounded stages.

### Phase 0 — Constitution and legal registry

Deliverables:

- approved family definition;
- source registry schema;
- licence matrix;
- clean-room policy;
- new namespace decision;
- family and analysis schemas;
- quality objectives.

Exit: all consequential decisions approved; still no family production.

### Phase 1 — Factory prototype

Scope:

- ingest a small approved-source snapshot;
- produce raw candidates;
- test normalization, clustering, and resumability;
- publish nothing.

Exit: deterministic rerun and complete lineage.

### Phase 2 — First 100 commissioning batch

Binding batch plan: `planning/EXPRESSIONS_FIRST_100_PLAN.md`.

Scope:

- mine at least 2,000 normalized clean-room candidates;
- compile exactly 100 fully passed families;
- build complete Library Result Tiles and Full Family Cards;
- require analysis for every displayed primary/alternate form;
- audit all 100;
- build a private `0.1.0-development` shadow candidate in four packs of 25;
- measure acceptance, defects, throughput, cost, rebuild time, and mobile performance;
- no learner exposure or public publication.

Exit: every hard invariant passes, all 100 pass the commissioning audit, and the factory produces a transparent measurement report.

### Phase 3 — 1,000-family expansion validation

- apply measured Batch 001 corrections to the compiler rather than patching release records;
- validate confidence calibration on broader evidence and category coverage;
- repeat global duplicate and reverse-link audits;
- prove changed-only and clean-rebuild behaviour;
- remain shadow/private unless separately authorized.

### Phase 4 — 10,000-family launch candidate

Scope:

- full runtime index/packs;
- browser and backend load tests;
- stratified audit;
- complete clean rebuild;
- cutover rehearsal with synthetic accounts.

### **Recommended earliest cutover threshold**

10,000 passed families, provided:

- the compiler also completes a dry run over a 100,000-candidate pool;
- quality gates remain stable across source classes;
- runtime search and detail retrieval stay responsive;
- destructive migration and remote Source replacement pass a full rehearsal.

This avoids waiting for all 100,000 families before learners receive the new system while proving that the factory—not a 10,000-item manual effort—can scale.

The user must approve the actual launch threshold.

### Phase 5 — 25,000 families

- expand source diversity;
- recalibrate drift;
- audit rare registers and domain language;
- strengthen duplicate graph.

### Phase 6 — 50,000 families

- validate shard/index architecture;
- review category and Difficulty distribution;
- run complete cross-corpus duplicate search.

### Phase 7 — 100,000 families

- final scale objective;
- reproducible clean rebuild;
- complete manifest and attribution audit;
- post-release monitoring and rollback-ready release.

Each scale phase is an immutable release, not an in-place mutation.

---

## 10. Runtime architecture for 100,000 families

Loading all rich records into one browser tab will not scale. Preserve the learner workflow while changing delivery internals.

### **Recommended delivery design**

1. Small immutable root manifest
2. Sharded compact search indexes
3. Difficulty/category/status listing shards
4. Rich family detail packs fetched on demand
5. Analysis packs fetched only when a family sheet opens
6. Session-only in-memory/session caching
7. No personal state in remote content
8. Backend ID support inventory containing no family content

Proposed Source layout:

```text
Expressions/
  manifest.json
  schema/
    family-v2.schema.json
    analysis-v2.schema.json
  provenance/
    source-registry.json
    compiler-manifest.json
    attribution.json
  indexes/
    japanese-*.json
    reading-*.json
    english-*.json
    facets-*.json
  families/
    pack-00001.json
    ...
  analysis/
    pack-00001.json
    ...
  audits/
    release-<id>.json
```

### Binding Library and Full Family Card requirements

The replacement Library must preserve the previous page’s product level: verified-corpus hero and source state; progress counts; “Find an intention, not just a spelling” purpose; Japanese/reading/meaning/intention/context search; Difficulty, Category, Personal status, Sort, and Reset; native mobile selection behaviour; verified result summary; and complete result tiles containing Difficulty, category, Japanese, reading, contextual meaning, intentions, Recognised/Review, and Open.

The user defines **Card** as the complete opened family experience, not the compact Library Result Tile. The Full Family Card must meet or exceed the previous release’s depth and presentation: close control; Difficulty, category, and VERIFIED metadata; primary Japanese, reading, contextual meaning, Japanese device TTS, and editorial summary; Recognised/Review; intentions; Use When, Take Care, and Relationships; every published form with register, reading, meaning, TTS, and complete tappable sentence analysis; Natural Responses; Follow-ups; dialogue; reviewed patterns/examples; nearby distinctions; and verification/sources.

The binding contracts are `planning/EXPRESSIONS_LIBRARY_SPEC.md` and `planning/EXPRESSIONS_FAMILY_CARD_SPEC.md`. Performance must come from sharded retrieval, bounded result rendering, and one-family-at-a-time rich loading—not from removing sections, thinning result tiles, or reducing instructional depth.

### Runtime performance targets

Provisional targets, to be measured on low-memory Android devices:

- initial Expressions shell: no family payload embedded;
- first useful library view without downloading all rich records;
- search response after required shard load: under 150 ms on target hardware;
- family-sheet open after cached index: under 500 ms excluding network latency;
- bounded DOM rows through pagination or virtualization;
- no persistent storage of remote corpus content;
- graceful retry without losing personal state.

Exact budgets require device benchmarking before approval.

---

## 11. Compiler engineering architecture

### 11.1 Work units

Every stage consumes and emits immutable work units addressed by content hash. A failed run resumes from the last verified stage rather than restarting a 100,000-family chain.

### 11.2 Parallelism

Parallelize by source shard and candidate partition, then use global reducers for:

- duplicate graph;
- ID assignment;
- family merges;
- count verification;
- search index construction;
- attribution generation.

### 11.3 Determinism

Record:

- exact input hashes;
- tool versions;
- model identity and configuration;
- prompt/template versions;
- random seeds where supported;
- locale and normalization versions;
- output canonicalization rules.

Model output is normalized into strict schema and independently verified. Raw prose is never accepted directly as release data.

### 11.4 Bounded operations

- visible batch counters;
- per-stage timeout and retry policy;
- no broad recursive output dumps;
- concise checkpoint summaries;
- quarantine rather than infinite retries;
- machine-readable failure manifests.

### 11.5 Cost controls

- deterministic rules before model calls;
- content-hash cache;
- cheap classifier before expensive adjudication;
- batch prompts only for compatible tasks;
- never reprocess unchanged work units;
- record cost/time per accepted and quarantined family;
- halt automatically when quality or cost drifts beyond approved limits.

No calendar or cost promise should be made until the Phase 1 prototype measures actual throughput.

---

## 12. Test matrix

### Source and legal

- every source pinned and checksummed;
- every record’s lineage resolves;
- prohibited source detector;
- attribution bundle completeness;
- source refresh requires explicit approval.

### Candidate and family

- no arbitrary sentence inflation;
- no single-word Vocabulary leakage;
- family merge/split invariants;
- all forms evidence-backed;
- global duplicate search;
- stable ID and revision behaviour.

### Japanese quality

- valid script and punctuation;
- reading alignment;
- form/register consistency;
- intention/meaning agreement;
- substitution safety;
- response/dialogue coherence;
- relationship-risk consistency.

### Analysis and Vocabulary

- exact surface reconstruction;
- exact reading reconstruction;
- canonical ID exists;
- written form/reading/sense evidence agrees;
- inflection path reproducible;
- reverse candidate enumeration detects omissions;
- no approximate or substring-only link;
- complete no-link reason.

### Runtime

- 100,000-ID support boundary;
- sharded search correctness;
- pagination/virtualization;
- device Japanese TTS only;
- session-only remote cache;
- Recognised/Review exclusivity;
- account isolation;
- no Vocabulary-state writes;
- offline/error behaviour;
- accessibility and keyboard/touch behaviour.

### Cutover

- old Source remains available before activation;
- new Source identity verified before switch;
- old Source tree removed in the cutover commit;
- `expression_progress` purged only in final migration;
- every non-Expressions account table unchanged;
- restart and authenticated health checks;
- failure rolls application files back according to the approved deletion policy.

---

## 13. Atomic cutover plan

The old public dataset and the new dataset must never be mixed into one claimed release.

### Cutover rehearsal

1. Mirror the production database into a disposable fixture.
2. Seed multiple accounts and every non-Expressions state type.
3. Seed legacy Expressions progress.
4. Stage the new Source commit and Koto pin.
5. Run the explicit Expressions progress purge.
6. Verify all non-Expressions rows byte-for-byte or by canonical dump.
7. Activate, restart, authenticate, search, open details, use TTS affordances, and exercise new state.
8. Force a failure and verify rollback behaviour.

### Final cutover

1. Freeze replacement inputs.
2. Produce final clean build and audit.
3. In one Source commit, remove the legacy Expressions tree and add the approved replacement tree.
4. Verify the remote commit and every pack hash.
5. Update Koto’s immutable Source pin and new ID inventory.
6. Apply the approved `expression_progress` deletion migration.
7. Run full staged validation.
8. Activate and restart.
9. Run authenticated post-activation checks.
10. Produce the new self-contained Termux package only after this succeeds.

### Unresolved deletion boundary

“Permanently delete all Expressions progress” still requires one explicit decision before cutover:

- delete only live `expression_progress` rows; or
- also remove Expressions rows from Koto-managed historical rollback backups; or
- delete all old backups entirely.

A live-row purge alone does not erase copies already present in backups. This must not be guessed.

---

## 14. Risk register

| Risk | Control |
|---|---|
| Generated but unattested Japanese | Evidence required before candidacy; generation cannot establish existence |
| Duplicate inflation toward 100,000 | Global duplicate graph, merge reasons, sampled audit |
| Valid links omitted | Reverse candidate enumeration and recall-oriented audit |
| Wrong canonical links | Exact ID/form/reading/sense validation, reverse omission audit, and family quarantine on unresolved published forms |
| Register or relationship harm | Separate risk gate; zero critical sampled defects |
| Copyright contamination | Source registry, licence classes, prohibited-source scan |
| Non-reproducible model output | Versioned prompts/models, strict schema, deterministic verification |
| One hard form blocks its family | Quarantine that family while unrelated complete families proceed in parallel |
| Browser cannot handle 100,000 | Sharded indexes, lazy details, bounded DOM |
| Old state attaches to new IDs | New namespace plus final progress purge |
| Destructive cutover damages other data | Disposable full transaction, canonical DB comparison, rollback test |
| Public Source deleted too early | Cutover guard requiring replacement release verification |
| Manual review becomes bottleneck again | Benchmark/sampling/exception lane only |
| Automated quality drifts | Per-release calibration and halt thresholds |

---

## 15. Governance and release truthfulness

Every release report must state separately:

- number of extracted candidates;
- number of clustered candidate families;
- number automatically rejected;
- number quarantined;
- number agent-reviewed;
- number human-reviewed;
- number passing deterministic verification;
- analysis coverage by form;
- audit sample sizes and observed defects;
- confidence calibration version;
- source and licence changes.

Never describe automated output as human reviewed. Never turn “no defect found in a sample” into “error-free.”

---

## 16. Work breakdown

### Epic A — Constitution

- ratify family scope;
- approve source strategy;
- approve exclusions;
- approve launch threshold.

### Epic B — Legal/source registry

- schema;
- first source assessments;
- licence/attribution generator design;
- prohibited-source policy.

### Epic C — Data contracts

- new namespace;
- family schema v2;
- analysis schema v2;
- compiler/audit manifests.

### Epic D — Candidate factory

- adapters;
- normalization;
- extraction channels;
- candidate ledger;
- lineage.

### Epic E — Family compiler

- clustering;
- deduplication;
- editorial field generation;
- independent critique;
- Koto Difficulty.

### Epic F — Analysis compiler

- segmentation;
- reading alignment;
- grammatical roles;
- canonical candidate enumeration;
- reverse completeness check;
- complete-analysis gate for every accepted published form.

### Epic G — Calibration and audit

- new benchmark;
- sealed holdout;
- confidence calibration;
- batch audit;
- drift monitoring.

### Epic H — Runtime at scale

- Source shards;
- search indexes;
- lazy detail loading;
- 100,000-ID backend boundary;
- state isolation;
- mobile performance.

### Epic I — Cutover

- Source replacement commit;
- progress deletion migration;
- transaction fixtures;
- activation/restart/rollback;
- new Termux package.

---

## 17. Remaining decision gates

Before implementation, the user must approve or revise:

1. **Family scope:** recommended broad attested reusable expressions.
2. **Authority:** recommended evidence-first hybrid.
3. **New ID strategy:** opaque stable namespace plus separate slug.
4. **Dataset licence:** recommended CC BY-SA 4.0, subject to source review.
5. **Analysis publication:** every displayed primary/alternate form requires complete passed analysis; unresolved important forms quarantine the family.
6. **Quality targets:** provisional table in section 8.3.
7. **Earliest cutover:** recommended 10,000 passed families plus a 100,000-candidate dry run.
8. **Backup deletion boundary:** live rows versus retained backups.
9. **Source portfolio:** each source approved individually after registry review.

Approval of this plan authorizes specification work only unless the user explicitly authorizes implementation.

---

## 18. Immediate next deliverable

After plan approval, produce a **Corpus Constitution and Decision Record** containing only:

- formal family inclusion/exclusion tests;
- family merge/split rules;
- source permission matrix;
- namespace alternatives;
- schema alternatives;
- quality gates;
- launch threshold alternatives;
- backup-deletion alternatives.

Do not acquire bulk source data, generate candidates, modify Koto runtime, alter public Source, or create a package during that deliverable.
