# Koto Expressions — First 100 Families Commissioning Plan

**Status:** Authorized; Stages 1–3 complete; morphology runtime and candidate generation not started  
**Date:** 2026-09-30  
**Batch:** New-corpus Batch 001  
**Publication target:** Exactly 100 completely passed families  
**Purpose:** Commission the industrial pipeline, not manually author a small replacement

---

## 1. Binding batch decision

The user selected **100 families for the first from-scratch batch**.

This changes the initial scale ladder:

- first commissioning batch: 100 passed families;
- next scale gate selected after measured Batch 001 results;
- long-term architecture still targets 100,000 families.

The first 100 are a private shadow replacement. They do not trigger public Source deletion, progress deletion, live cutover, or packaging.

---

## 2. What “first 100” means

It does **not** mean:

- pick 100 familiar expressions manually;
- copy the former 100 best families;
- reuse old IDs, categories, forms, explanations, or analysis;
- stop candidate generation when 100 raw candidates exist;
- lower gates so the batch reaches exactly 100;
- publish incomplete family cards.

It means:

1. build the minimum real factory;
2. mine a larger evidence-backed candidate pool;
3. compile, deduplicate, analyze, and audit candidates;
4. quarantine or reject failures;
5. continue through the ranked pool until exactly 100 families pass every gate.

---

## 3. Batch 001 objectives

Batch 001 must prove that the system can:

- ingest pinned approved sources;
- preserve licence and evidence lineage;
- discover candidates without old-corpus input;
- normalize Japanese and readings;
- merge variants and split different functions;
- prevent duplicate-family inflation;
- compile the complete Library summary record;
- compile the complete Full Family Card;
- analyze every displayed primary/alternate form;
- enumerate canonical Vocabulary candidates in both directions;
- abstain/quarantine honestly;
- build verified packs and search indexes;
- render the required Library and Full Family Card in an isolated preview;
- rebuild deterministically;
- measure throughput, cost, acceptance, defects, and bottlenecks.

Learner usefulness matters, but the first batch must also stress every important factory component.

---

## 4. Clean-room start

Create new authorities only after implementation approval:

```text
planning/                         approved specifications
work/expressions2/source-registry/
work/expressions2/snapshots/
work/expressions2/candidates/
work/expressions2/ledger/
work/expressions2/compiled/
work/expressions2/audits/
work/expressions2/preview/
```

These are conceptual paths; exact paths are approved in the implementation plan.

Prohibited inputs:

- current public Expressions packs;
- current family-ID inventory;
- old editorial decisions;
- old candidate files;
- old analysis data;
- old family text pasted as visual reference;
- `.85` or `.86` payload material;
- learner `expression_progress`.

A build check must fail if replacement stages import legacy Expressions paths or IDs.

---

## 5. Minimum source portfolio

### **Recommended commissioning sources**

Start with a deliberately small, legally manageable portfolio:

1. **JMdict/EDRDG** — expression candidates, forms, readings, lexical labels, canonical Vocabulary identities
2. **Tatoeba CC0/Tanaka-identified records** — corpus attestation and pattern evidence
3. **Tatoeba CC BY records** — evidence-only by default, with sentence IDs and licence identity
4. **Wiktionary dump** — phrase/idiom/proverb candidates, evidence-only until extraction rules pass
5. **Japanese WordNet** — semantic grouping and duplicate detection
6. **SudachiDict plus one explicitly approved free UniDic edition** — tool-only independent morphology

Do not use BCCWJ/NINJAL-LWP, NWJC/Bonten, unlicensed subtitles, commercial dictionaries, scraped websites, or social media in Batch 001.

Every acquired file must have:

- canonical URL;
- exact version/date;
- retrieved timestamp;
- byte length;
- SHA-256;
- licence;
- attribution;
- approved role;
- raw/derived redistribution rules.

---

## 6. Candidate-pool size

### **Recommended target: at least 2,000 normalized candidates**

Why not generate only 100:

- duplicates will merge;
- some candidates will be ordinary Vocabulary;
- some will lack evidence;
- some will fail register or safety checks;
- some forms will have unresolved analysis;
- balanced coverage requires choice;
- exactly 100 passes must be reached without lowering quality.

Pipeline funnel target for measurement—not a promised acceptance rate:

```text
raw extracted candidates           unrestricted
normalized candidates              ≥ 2,000
family clusters                    measured
eligible compilation candidates    measured
fully compiled candidates          measured
quarantined/rejected               measured truthfully
Batch 001 accepted                 exactly 100
```

If fewer than 100 pass, expand the approved candidate pool. Never relax gates.

---

## 7. Proposed Batch 001 coverage matrix

Quotas are selection goals, not permission to force weak records. A shortfall is replenished with another strong candidate in the same or adjacent class.

### Family-class targets

| Primary class | Target |
|---|---:|
| Interactional formula | 18 |
| Discourse routine | 12 |
| Grammar construction | 18 |
| Conventional collocation | 15 |
| Idiom | 10 |
| Proverb or saying | 5 |
| Institutional formula | 8 |
| Productive sentence frame | 8 |
| Pragmatic pattern | 6 |
| **Total** | **100** |

### Koto Difficulty targets

| Difficulty | Target |
|---|---:|
| 1 · Essential | 20 |
| 2 · Foundational | 25 |
| 3 · Intermediate | 25 |
| 4 · Advanced | 20 |
| 5 · Nuanced | 10 |
| **Total** | **100** |

### Register and context coverage

Batch 001 should collectively include:

- neutral spoken;
- polite spoken;
- casual/intimate;
- workplace;
- service encounter;
- school/institutional;
- formal written;
- socially sensitive/high-risk;
- idiomatic/non-compositional;
- productive grammar.

No single source, register, category, or surface template should dominate merely because it is easier to extract.

---

## 8. Start sequence

### Step 1 — Freeze decisions

Before code:

- approve C-01–C-16 or record changes;
- approve the Library specification;
- approve the Full Family Card specification;
- approve this Batch 001 plan;
- select exact source snapshots/licences;
- select ID format;
- select initial corpus licence.

Output: one signed/versioned decision record.

### Step 2 — Define strict schemas

Create and test:

- source registry;
- source evidence;
- raw candidate;
- normalized candidate;
- family ledger;
- family v2;
- analysis v2;
- compiler manifest;
- audit manifest;
- runtime Library summary;
- runtime Full Family Card record.

Output: schemas plus positive/negative fixtures, still no real family records.

### Step 3 — Build source adapters

For each approved source:

- download by pinned URL;
- verify hash;
- parse deterministically;
- emit evidence records only within allowed terms;
- retain source identity;
- reject unexpected schema/version changes.

Output: frozen evidence stores and licence report.

### Step 4 — Generate raw candidates

Independent channels:

- explicitly labelled expressions/idioms/proverbs;
- multiword lexical candidates;
- corpus n-grams with dispersion;
- grammar/construction frames;
- collocations;
- interactional formula patterns;
- institutional formula patterns.

Models may propose classifications but cannot provide attestation.

Output: raw candidate ledger.

### Step 5 — Normalize and reject obvious non-families

- Unicode/script normalization;
- reading normalization;
- morphology;
- inflection grouping;
- orthographic variant grouping;
- named-entity filtering;
- arbitrary-sentence filtering;
- single-word Vocabulary filtering;
- prohibited-source filtering.

Output: at least 2,000 normalized candidates or a measured explanation of why not.

### Step 6 — Cluster and deduplicate globally

- exact surface/reading edges;
- lemma/frame edges;
- intention candidates;
- register/politeness variants;
- semantic-neighbour candidates;
- hard split rules;
- merge/split/quarantine reasons.

Output: candidate family graph, not yet published families.

### Step 7 — Rank candidates for commissioning value

Ranking dimensions:

- evidence strength;
- family-boundary confidence;
- learner usefulness;
- class/Difficulty coverage need;
- register diversity;
- analysis tractability;
- duplicate separation;
- safety describability.

No Commonness label is emitted. Evidence frequency may help candidate navigation but does not determine Koto Difficulty.

Output: ranked compilation queue.

### Step 8 — Compile complete family records

Parallel specialized stages produce:

- class/category;
- intentions;
- primary and accepted forms;
- readings;
- contextual meanings;
- usage summary;
- Use When;
- Take Care;
- Relationships;
- responses;
- follow-ups;
- dialogue;
- patterns/examples;
- nearby distinctions;
- Difficulty;
- provenance/review metadata.

A separate critic checks each field against evidence and neighbouring families.

Output: complete candidate Full Family Cards or structured quarantine.

### Step 9 — Compile every published form analysis

For every accepted primary/alternate form:

- segment hypotheses;
- exact Japanese reconstruction;
- exact reading reconstruction;
- roles and contextual meanings;
- lemmas and inflections;
- complete canonical Vocabulary candidate enumeration;
- selected exact links;
- reverse omission check;
- explicit no-link reasons;
- deterministic verification.

A known important form with unresolved analysis quarantines its family.

Output: complete family analysis or quarantine.

### Step 10 — Apply hard gates

No record publishes unless all required checks pass:

- source/legal;
- family admission;
- schema;
- global duplicate;
- Japanese/reading;
- register/safety;
- rich content;
- all accepted forms analyzed;
- canonical-link validity and completeness;
- provenance;
- deterministic identity.

Continue down the ranked queue until exactly 100 pass.

### Step 11 — Audit all 100

Because Batch 001 calibrates the factory, audit 100% of accepted families.

This is not manual production. The compiler creates the records; the commissioning audit evaluates whether the machinery works.

Audit dimensions:

- family inclusion;
- merge/split;
- naturalness;
- meaning/intention;
- register/relationship;
- Difficulty;
- every form/reading;
- every segment;
- canonical links and likely omissions;
- responses/follow-ups/dialogue;
- patterns/comparisons;
- source/licence/provenance;
- Library summary accuracy;
- Full Family Card completeness.

Defects fix the compiler/rule where generalizable, then rebuild affected records. Do not patch release JSON directly.

### Step 12 — Build private runtime artifacts

Recommended commissioning release:

```text
release: 0.1.0-development
publicationStatus: shadow-candidate
productionReady: false
familyCount: 100
```

Exercise sharding from the beginning:

- four family-detail packs of 25;
- compact Library index;
- analysis packs aligned by family pack;
- manifest with bytes/SHA-256;
- source/attribution manifest;
- audit manifest.

Output remains private/local until separately authorized.

### Step 13 — Build isolated preview

The preview must reproduce:

- full Library hero/progress/search/filter/result experience;
- native mobile category selector;
- 100 complete Library Result Tiles;
- Full Family Card for every family;
- tappable analysis for every displayed form;
- TTS controls using device speech;
- synthetic preview accounts only;
- no connection to real learner state.

Do not modify the current live Expressions route during Batch 001 preview work unless separately authorized.

### Step 14 — Measure the factory

Report:

- source bytes and licence classes;
- raw/normalized candidate counts;
- cluster count;
- merge/split/quarantine counts;
- fully compiled count;
- accepted count;
- defects by type;
- candidates needed per accepted family;
- automated acceptance rate;
- human/agent audit effort;
- compute time by stage;
- model calls and cost by accepted family where applicable;
- rebuild time;
- Library and Full Family Card mobile performance;
- peak memory;
- deterministic rebuild result.

These measurements determine the next batch size and realistic path to 100,000.

---

## 9. Batch 001 speed strategy

The first 100 will be slower per family than later batches because the factory, schemas, benchmark, and audits are being commissioned.

Speed comes from:

- candidate extraction in bulk;
- parallel field compilers;
- batch morphology and neighbour search;
- one canonical-link index shared by every family;
- content-hash caching;
- changed-only rebuilds;
- general compiler fixes rather than release-record patches;
- quarantine without blocking unrelated families.

### Required throughput measurements

- candidates extracted per second;
- normalized candidates per second;
- clusters resolved per minute;
- complete families compiled per worker-hour;
- form analyses compiled per worker-hour;
- percent automatic pass;
- percent adjudication;
- percent quarantine/reject;
- audit minutes per accepted family;
- full clean rebuild wall time.

Do not promise the 100,000-family calendar before these measurements exist.

---

## 10. Batch 001 acceptance criteria

The commissioning batch passes only when:

1. Exactly 100 new clean-room families pass.
2. No old family ID or record is imported.
3. Every family satisfies the new inclusion constitution.
4. The coverage matrix is met or every justified deviation is documented.
5. Every family has a complete Library Result Tile.
6. Every family has a complete Full Family Card.
7. Every displayed primary/alternate form has complete passed analysis.
8. Every canonical link is valid and reverse-checked for omissions.
9. Every family has complete source and licence provenance.
10. All 100 receive the commissioning audit.
11. A clean rebuild produces identical canonical artifacts.
12. Library and Full Family Card work on desktop and mobile reference widths.
13. No personal or Vocabulary state is modified.
14. The release remains private, shadow, and non-production.
15. A transparent measurement report is produced.

---

## 11. Stop conditions

Pause and return to design if:

- source terms do not permit the planned outputs;
- candidate evidence is too weak for 100 families;
- duplicate boundaries cannot be calibrated;
- rich content severe-defect rate exceeds the approved gate;
- analysis omission checks fail systematically;
- too many families require manual rewriting;
- compiler outputs cannot rebuild deterministically;
- mobile Library or Full Family Card cannot meet the preserved product level;
- the pipeline begins copying old content;
- cost/throughput makes 100,000 unrealistic.

A stop is a successful quality-control outcome, not permission to lower standards silently.

---

## 12. What Batch 001 does not do

- no public Source publication;
- no deletion of old public Source;
- no deletion of `expression_progress`;
- no backup scrubbing;
- no Koto live-route replacement;
- no standalone Termux package;
- no production-ready claim;
- no promise that Batch 002 repeats the same quota distribution;
- no manual patching as the scaling method.

---

## 13. Decision needed before implementation

### **Recommended approval**

Approve:

- exactly 100 passed families;
- at least 2,000 normalized candidates feeding the selection;
- proposed class and Difficulty matrix;
- conservative six-source commissioning portfolio;
- 100% audit of the commissioning batch;
- four packs of 25;
- private `0.1.0-development` shadow candidate;
- no live cutover or package.

Approval wording:

```text
Approve the First 100 commissioning plan as recommended.
```

This approval would authorize implementation planning and source-snapshot proposals. Bulk acquisition, family generation, public publication, and runtime modification still require the explicit stage authorizations defined in the master plan.
