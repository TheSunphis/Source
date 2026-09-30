# Koto Expressions Corpus Constitution and Decision Record

**Status:** Proposed for user approval  
**Date:** 2026-09-30  
**Parent plan:** `planning/EXPRESSIONS_FROM_SCRATCH_MASTER_PLAN.md`  
**Effect:** Specification only; this document does not authorize implementation

---

## 1. Purpose

This constitution defines what the new Expressions factory may create, what evidence it must possess, how records become families, how variants merge or split, and what must be proven before publication.

The replacement corpus starts with an empty family ledger. The former Expressions corpus is neither seed data nor editorial authority.

The constitution has three kinds of provisions:

- **Binding prior decisions** — already chosen by the user
- **Recommended decisions** — proposed here for approval
- **Deferred implementation details** — measured during prototypes after approval

---

## 2. Binding prior decisions

These are not reopened by this document:

1. Rebuild Expressions content and analysis from scratch.
2. Preserve only the module’s structural behaviour and learner workflow.
3. Use an industrial, confidence-gated production system capable of scaling toward 100,000 families.
4. Do not use old family records, IDs, annotations, links, decisions, or explanations as replacement truth.
5. Remove the old public Expressions dataset at final atomic cutover.
6. Permanently delete legacy `expression_progress` at final atomic cutover, with no ID mapping.
7. Keep the existing public dataset operational until the replacement passes.
8. The `.85` and `.86` standalone packages remain deleted.
9. Do not create an intermediate standalone package.

---

# Part I — Corpus identity

## 3. Proposed corpus mission

Koto Expressions teaches conventional, reusable Japanese units whose successful use depends on more than recalling isolated Vocabulary.

A family should help a learner answer at least one of these questions:

- What communicative act does this perform?
- In what relationship or register is it suitable?
- What grammatical construction does it instantiate?
- What conventional meaning differs from a literal word-by-word reading?
- What reusable frame can safely accept substitutions?
- What response or follow-up does it naturally invite?

Expressions is not a sentence bank, quotation archive, frequency list, or second Vocabulary library.

### Decision C-01 — Mission

**Recommended:** approve the mission above unchanged.

Alternatives:

- Narrow the module to social formulas only.
- Broaden it into a general sentence corpus.
- Merge Expressions into Vocabulary.

The recommended mission is the only option consistent with the existing learner workflow and a credible 100,000-family target without counting arbitrary sentences.

---

## 4. Family classes

Every family must have exactly one primary class and may have secondary facets.

### Primary classes

1. `interactional-formula`
2. `discourse-routine`
3. `grammar-construction`
4. `conventional-collocation`
5. `idiom`
6. `proverb-or-saying`
7. `institutional-formula`
8. `productive-sentence-frame`
9. `pragmatic-pattern`

### Secondary facets

- greeting
- leave-taking
- gratitude
- apology
- request
- permission
- offer
- invitation
- refusal
- acknowledgement
- reaction
- evaluation
- agreement/disagreement
- topic management
- turn management
- repair/clarification
- sequencing
- cause/reason
- contrast/concession
- condition
- degree/extent
- evidence/hearsay
- stance
- obligation
- possibility
- workplace
- school
- service encounter
- written/formal
- intimate/casual
- literary/historical
- regional

Facets are filters and evidence dimensions, not separate family identities.

### Decision C-02 — Taxonomy

**Recommended:** approve the nine primary classes and extensible secondary facets. Add new facets through schema-controlled vocabulary; add new primary classes only through a corpus-constitution revision.

---

# Part II — Formal family admission

## 5. Mandatory inclusion test

A candidate becomes eligible for family compilation only if it passes every test below.

### I-1 Conventionality

There is evidence that Japanese users reuse the unit or frame as a recognizable pattern. One generated sentence is not evidence.

### I-2 Reusability

The unit can occur across multiple situations, participants, referents, or fillers without becoming a different quotation or event-specific sentence.

### I-3 Functional unity

The candidate has one coherent communicative, pragmatic, grammatical, idiomatic, or collocational function that can be explained independently.

### I-4 Learner value beyond isolated Vocabulary

At least one of these is true:

- usage depends on register or relationship;
- meaning is non-compositional or conventional;
- grammar constrains substitution;
- a learner could choose individually correct words yet produce unnatural Japanese;
- natural responses or discourse consequences matter;
- the construction provides reusable sentence-building value.

### I-5 Evidence admissibility

At least one approved evidence route in section 8 passes. Prohibited or model-generated text cannot satisfy this test.

### I-6 Bounded form

The family has a definable primary form or template and clear limits on what counts as its variant.

### I-7 Non-duplication

No existing new-corpus family already covers the same core intention, construction, substitution behaviour, and social risk.

### I-8 Safety describability

Register, relationship suitability, and significant misuse risks can be stated truthfully from evidence. If they remain unknowable, the candidate is quarantined.

### I-9 Redistributable output

Koto can publish the proposed Japanese form, reading, original explanation, and provenance without violating source terms.

### I-10 Complete minimum record

The candidate can support the minimum schema in section 19 without fabricated filler.

### Decision C-03 — Inclusion rule

**Recommended:** all ten tests are mandatory. No weighted score may compensate for a failed inclusion test.

---

## 6. Automatic exclusions

Reject without model adjudication when any condition is conclusively true:

1. ordinary single-word lexical entry with no expression-level behaviour;
2. proper name or named entity without general conventional use;
3. sentence tied to one person, work, event, or current headline;
4. quotation, lyric, subtitle line, or copyrighted passage presented as a family;
5. punctuation/orthographic variant of an existing form;
6. tense, polarity, or conjugation variant with no functional change;
7. politeness variant with no change beyond the existing family boundary;
8. automatically translated or generated Japanese lacking independent evidence;
9. foreign-language contamination or malformed Japanese;
10. compositional free phrase whose parts explain its full meaning and use;
11. candidate supported only by prohibited evidence;
12. candidate whose licence status is unresolved after the source gate;
13. near-duplicate created to raise corpus totals;
14. arbitrary complete example sentence rather than a reusable unit;
15. unsafe substitution template whose valid slot cannot be bounded.

An automatic rejection must retain a machine-readable reason and source candidate identity to prevent repeated rediscovery.

---

## 7. Candidate evidence levels

Evidence is recorded at form, meaning, register, and family-boundary level. One evidence item may support one property without supporting all properties.

### Level A — Direct authority

Examples:

- approved dictionary explicitly marks the unit as an expression, idiom, proverb, collocation, or construction;
- licensed reference explicitly documents its usage and register;
- approved structured source provides the exact form and reading.

### Level B — Independent attestation

The candidate appears with coherent function across independent approved corpus families or publishers. Two mirrors of the same upstream corpus count as one source.

### Level C — Productive-pattern evidence

A grammatical or sentence frame has:

- a stable structural signature;
- multiple attested fillers;
- consistent function;
- bounded slots;
- independent support for its interpretation.

### Level D — Model proposal

A model proposes a candidate, merge, meaning, register, or pattern. This is navigation evidence only and cannot satisfy admission by itself.

---

## 8. Approved evidence routes

A candidate may enter compilation through one route.

### Route R1 — Direct authority

- At least one Level A source supports existence and core function.
- An independent source or deterministic check supports the reading/form identity.

### Route R2 — Independent corpus evidence

- At least two genuinely independent approved source families support the same normalized unit and compatible function.
- Evidence demonstrates dispersion rather than repetition from one copied document.
- Reading and function receive an independent check.

### Route R3 — Productive construction

- Level C evidence demonstrates multiple fillers and contexts.
- A grammar/reference source or independent construction classifier supports the boundary.
- The substitution slot is mechanically testable.

### Route R4 — Government/institutional formula

- The form occurs in approved reusable public-sector content under verified terms.
- It is demonstrably conventional rather than one document’s wording.
- Register and scope are explicitly labelled.

### Route R5 — Proverb/idiom authority

- An approved lexical/reference source identifies the conventional expression.
- Corpus evidence confirms modern, historical, regional, or literary status.
- Status is shown rather than silently modernized.

### Decision C-04 — Authority model

**Recommended:** approve the evidence-first hybrid routes R1–R5. Models may enrich or challenge candidates but cannot create an evidence route.

---

# Part III — Merge and split constitution

## 9. Family-equivalence dimensions

Two candidates may merge only after comparison on all dimensions:

1. core communicative intention;
2. compositional or idiomatic meaning;
3. grammatical frame;
4. substitution slots;
5. register;
6. social relationship constraints;
7. misuse risk;
8. expected response/follow-up behaviour;
9. polarity and stance;
10. historical/regional scope.

Surface similarity alone never establishes family identity.

---

## 10. Mandatory merge cases

Merge into one family when all functional dimensions remain compatible and the difference is only:

- kana versus kanji spelling;
- approved orthographic variation;
- punctuation;
- spacing;
- conventional contraction;
- politeness/register form already explainable inside one intention;
- inflection, tense, or polarity without pragmatic change;
- honorific/humble form serving the same act and safely describable together;
- fixed lexical substitution explicitly belonging to one bounded pattern.

Each merged form retains its own evidence, reading, register, and label.

---

## 11. Mandatory split cases

Split into separate families when any difference materially changes:

- communicative act;
- semantic scope;
- grammatical construction;
- substitution constraints;
- presupposition;
- stance or emotional force;
- required social relationship;
- misuse severity;
- response expectation;
- regional/historical identity in a way that cannot be represented as a form label;
- productive versus lexicalized use.

Example principle: visually similar strings representing a productive grammar frame and a fixed idiom do not merge merely because their surfaces overlap.

---

## 12. Conditional merge cases

These require adjudication:

- polite and casual forms whose pragmatic force differs;
- affirmative and negative forms that conventionalize different meanings;
- shortened forms that become more abrupt or intimate;
- honorific variants with different participant roles;
- idiom plus literal use;
- written formula versus spoken counterpart;
- regional form with different acceptability or meaning;
- grammar pattern plus lexicalized phrase;
- homographic forms with different readings.

The adjudicator must emit `merge`, `split`, or `quarantine`, plus structured reasons.

### Decision C-05 — Merge policy

**Recommended:** approve sections 9–12. Global duplicate comparison is mandatory before every release; batches are never deduplicated only internally.

---

# Part IV — Source permission constitution

## 13. Source-registry minimum fields

```text
sourceId
name
owner
canonicalUrl
snapshotUrl
retrievedAt
versionOrDate
byteLength
sha256
licenceName
licenceUrl
attributionText
commercialUse
machineAccess
modelProcessing
redistributeRaw
redistributeExtracts
publishDerivedRecords
requiredUpdates
thirdPartyContentRisk
permissionClass
approvedBy
notes
```

`permissionClass` is one of:

- `redistributable`
- `evidence-only`
- `tool-only`
- `prohibited`
- `pending`

Pending sources behave as prohibited.

---

## 14. Initial source permission matrix

| Source | Proposed class | Permitted role | Not permitted without new approval |
|---|---|---|---|
| JMdict/EDRDG | Redistributable/reference | Candidate forms, readings, lexical senses, labels, canonical Vocabulary identity | Ignoring CC BY-SA attribution/update requirements |
| Tatoeba CC0 subset | Redistributable evidence | Attestation, pattern discovery, independently licensed examples | Assuming translations share the same licence without record checks |
| Tatoeba CC BY exports | Evidence-only by default | Attestation and pattern statistics with IDs/attribution | Copying sentences into Koto records before an attribution/output policy passes |
| Tanaka public-domain records | Redistributable after identity verification | Attestation and potential examples | Treating all Japanese Tatoeba records as Tanaka/public domain |
| Wiktionary dumps | Evidence-only by default | Phrase/idiom/proverb candidates and lexical cross-checks | Copying definitions, quotations, or externally licensed material |
| Japanese WordNet | Tool/reference | Semantic clusters and duplicate detection | Publishing source definitions/examples without a record-level licence review |
| SudachiDict | Tool-only | Tokenization, lemmas, morphology | Republishing dictionary content as Koto family content |
| Approved BSD UniDic edition | Tool-only | Independent morphology/reading analysis | Mixing in a non-commercial edition or omitting required notices |
| Government PDL 1.0 pages | Evidence-only per site/page | Formal/institutional formula discovery | Blanket crawling or using third-party/excluded content |
| BCCWJ/NINJAL-LWP | Prohibited pending agreement | None in automated production | Scraping, copying search results, commercial use without permission |
| NWJC/Bonten | Prohibited | None | Programmatic access or scraped content |
| Commercial dictionaries | Prohibited pending contract | None | Any extraction or redistribution without written permission |
| Unlicensed subtitles/social web | Prohibited | None | Acquisition, mining, training, or publication |
| Model output | Proposal-only, not a source | Candidate navigation, drafting, critique | Attestation or provenance authority |

### Decision C-06 — Initial source matrix

**Recommended:** approve the conservative matrix. Promote a source only through a versioned registry amendment.

---

## 15. Corpus licence alternatives

### Option L1 — CC BY-SA 4.0 — **Recommended**

Advantages:

- compatible direction for JMdict/Wiktionary-derived material;
- preserves public availability;
- already familiar in Koto notices;
- supports redistribution and modification with attribution/share-alike.

Costs:

- attribution and derivative-licence obligations;
- per-source compatibility still must be checked;
- cannot absorb incompatible non-commercial or proprietary material.

### Option L2 — Split licensing by record

Advantages:

- could accommodate CC0/public-domain subsets separately.

Costs:

- complex runtime notices;
- difficult pack construction;
- easy to misstate derivative obligations.

### Option L3 — Original-only permissive licence

Advantages:

- potentially simpler reuse.

Costs:

- would exclude important share-alike inputs;
- provenance separation becomes much harder;
- likely reduces evidence and coverage.

### Decision C-07 — Dataset licence

**Recommended:** L1, subject to formal compatibility review after source-registry prototypes.

---

# Part V — Identity and schema constitution

## 16. ID alternatives

### Option ID1 — UUIDv7 in a new namespace — **Recommended**

```text
expression2:019a2f2e-7b1c-7abc-8def-0123456789ab
```

Properties:

- no collision with legacy `expression:` IDs;
- immutable despite Japanese/meaning edits;
- standard format;
- sortable by assignment time;
- human-readable slug remains separate.

Trade-off: IDs are not memorable; the ledger must remain authoritative.

### Option ID2 — Monotonic sequence

```text
expression2:000000000001
```

Properties: compact and simple.

Trade-off: centralized assignment and visible count/order; merges leave gaps.

### Option ID3 — Content hash

Properties: deterministic from canonical signature.

Trade-off: identity changes when family-boundary material changes; dangerous for learner state.

### Option ID4 — Semantic slug

Properties: readable URLs.

Trade-off: English wording becomes identity; collisions and later semantic corrections are difficult.

### Decision C-08 — New IDs

**Recommended:** ID1. Use a separate stable slug for navigation and debugging. Never recycle retired IDs.

---

## 17. Authoring-schema alternatives

### Option S1 — One monolithic family document

Simple, close to the former runtime shape, but expensive to update, deduplicate, and audit at 100,000 families.

### Option S2 — Normalized authoring authorities + compiled runtime record — **Recommended**

Authoring layer separates:

- family identity;
- forms;
- evidence;
- usage/editorial content;
- comparisons/relations;
- analysis;
- review/audits.

Release compiler emits convenient denormalized runtime packs.

Advantages:

- one source of truth per fact;
- efficient revisions;
- strong provenance;
- analysis replacement does not rewrite family authority;
- runtime remains simple.

### Option S3 — Minimal family records

Fast to produce but removes the rich sheets the user wants to preserve.

### Decision C-09 — Schema strategy

**Recommended:** S2.

---

## 18. Publication layers

### Layer P1 — Family core

Identity, class, intention, primary form, forms, meaning, register, usage, relationships, source evidence, Difficulty, provenance.

### Layer P2 — Rich learner support

Responses, follow-ups, dialogue, substitution patterns, comparisons, cautions, search aliases.

### Layer P3 — Compiled form analysis

Segments, readings, roles, contextual meanings, lemmas, inflections, canonical Vocabulary decisions, no-link reasons.

### Decision C-10 — Layer gate

**Binding user correction:** require P1+P2+P3 for every displayed primary and alternate form.

A candidate alternate may be excluded only when evidence/family-boundary adjudication concludes that it is not an accepted family form. It may not be hidden merely because analysis is difficult. A known important form with unresolved analysis quarantines the family.

Responses, follow-ups, dialogue lines, and examples retain Japanese, reading, meaning, and TTS but are not automatically governed by the published-family-form analysis boundary.

---

## 19. Minimum publishable family schema

Required fields:

```text
id
slug
revision
publicationStatus
familyClass
secondaryFacets[]
kotoDifficulty
category
intentions[]
primary {
  formId,
  japanese,
  reading,
  contextualMeaning,
  register,
  deviceTts
}
forms[]
usage {
  summary,
  useWhen[],
  avoidWhen[],
  suitableRelationships[],
  socialRisk,
  limits[]
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

Minimum cardinalities proposed:

- one primary form;
- one intention;
- one use-when statement;
- one avoid/caution statement, including explicit “none known” only when justified;
- one relationship/register statement;
- one response or explicit reason not applicable;
- one follow-up or explicit reason not applicable;
- at least two dialogue turns unless the family class makes dialogue inapplicable;
- one bounded pattern or explicit non-productive status;
- one comparison or explicit “no close comparison identified” after neighbour search;
- one admissible evidence route;
- complete provenance and review metadata.

Machine-readable non-applicability is allowed; fabricated learner content is not.

---

# Part VI — Difficulty constitution

## 20. Koto Difficulty anchors

Difficulty is not frequency, CEFR, JLPT, JF, or Commonness.

### Difficulty 1 — Essential, low-risk conventional use

- transparent or highly constrained;
- common learner need;
- simple substitution;
- low relationship risk;
- little ambiguity.

### Difficulty 2 — Foundational controlled variation

- modest grammar/register load;
- common alternatives;
- some relationship awareness;
- limited substitution risk.

### Difficulty 3 — Intermediate contextual choice

- meaningful register or stance choices;
- productive grammar;
- moderate ambiguity;
- context-sensitive comparison required.

### Difficulty 4 — Advanced social or structural control

- substantial register/relationship burden;
- nuanced contrast;
- advanced grammar or idiomaticity;
- misuse can sound strongly unnatural or inappropriate.

### Difficulty 5 — Nuanced, opaque, specialized, or high-risk

- idiomatic/proverbial opacity;
- literary, historical, institutional, or specialized limits;
- subtle pragmatic force;
- narrow substitution;
- serious social or interpretive risk.

### Difficulty compiler

A rule/model may propose Difficulty from independent dimensions:

- grammatical complexity;
- semantic opacity;
- substitution freedom;
- register burden;
- relationship risk;
- context dependency;
- response consequences;
- historical/regional/specialized limits.

An independent verifier checks the explanation against the selected level. Frequency may inform learner usefulness but cannot determine Difficulty.

### Decision C-11 — Difficulty

**Recommended:** approve the five anchors above.

---

# Part VII — Analysis and canonical-link constitution

## 21. Complete published-form analysis

For every displayed primary or alternate form:

1. Concatenated segment surfaces equal exact Japanese.
2. Concatenated segment readings equal exact form reading under approved alignment rules.
3. Every segment has role and contextual meaning.
4. Lemma/inflection appears when relevant.
5. Every linked Vocabulary ID exists in the pinned canonical catalogue.
6. Surface, reading, lemma, orthography, and inflection evidence support the selected ID.
7. Candidate generation searches for omitted valid IDs.
8. Unlinked segments carry a structured no-link reason.
9. Any unresolved ambiguity causes the entire form analysis to abstain.

A family cannot publish while an accepted important form has unresolved analysis. The family is quarantined while unrelated complete families continue through the pipeline.

---

## 22. Link decision classes

Permitted:

- `exact-surface-reading`
- `exact-lemma-reading`
- `documented-inflection`
- `documented-orthographic-variant`
- `documented-honorific-path`

Not permitted:

- substring-only;
- same spelling with incompatible reading;
- approximate semantic neighbour;
- model-selected ID without deterministic candidate evidence;
- convenient but broader/narrower sense;
- ID inherited from another form without independent validation.

No-link reasons:

- grammar-only segment;
- punctuation;
- productive inflection without standalone catalogue record;
- exact headword outside current canonical catalogue;
- ambiguous candidates;
- no canonical candidate;
- analysis abstained.

### Decision C-12 — Analysis gate

**Binding user correction:** every displayed primary and alternate form requires complete passed analysis. A known important unresolved form quarantines the family; it does not appear as a plain unanalysed published form.

---

# Part VIII — Confidence and release constitution

## 23. Hard gates

Every published family must pass all applicable hard gates:

- source licence;
- evidence route;
- schema;
- family inclusion;
- global deduplication;
- Japanese form;
- reading;
- intention/meaning agreement;
- register and relationship;
- substitution safety;
- source-text leakage;
- provenance;
- deterministic rebuild;
- complete passed analysis for every displayed primary/alternate form.

No numerical average may override a hard-gate failure.

---

## 24. Confidence classes

Raw model confidence is not accepted. Scores must be calibrated against a sealed, independently labelled benchmark.

Classes:

- `A`: automatic publication eligible after all hard gates
- `B`: requires independent adjudication
- `C`: quarantine
- `R`: rejected conclusively

Class A requires every critical dimension to exceed its class-specific calibrated threshold. The minimum dimension controls; dimensions are not averaged.

---

## 25. Proposed quality objectives

| Dimension | Proposed requirement |
|---|---:|
| Schema and provenance completeness | 100% |
| Exact Japanese reconstruction | 100% |
| Exact reading reconstruction | 100% |
| Canonical ID existence | 100% |
| Unresolved critical licence conflicts | 0 |
| Unresolved critical register/safety conflicts | 0 |
| Clean rebuild byte mismatch | 0 |
| Wrong-link sampled defect upper bound | <0.1% at 95% confidence |
| Severe naturalness/meaning sampled defect upper bound | <0.5% at 95% confidence |
| Duplicate-family sampled defect upper bound | <0.5% at 95% confidence |

These are release gates, not claims that unsampled content is infallible.

### Decision C-13 — Quality objectives

**Recommended:** approve these objectives for the 1,000-family pilot. Tighten rather than loosen after measured calibration unless the user explicitly approves a revision.

---

## 26. Benchmark constitution

The benchmark must be newly created from approved evidence and must include:

- all primary classes;
- all Difficulty levels;
- all major registers;
- relationship-risk cases;
- idiomatic and productive constructions;
- merge/split adversaries;
- script and reading ambiguity;
- positive links;
- tempting wrong links;
- valid no-link cases;
- reverse-link omission cases;
- form-analysis abstention cases.

Partitions:

- development;
- calibration;
- sealed holdout;
- post-release audit reserve.

No family or near-duplicate may cross partitions.

The old Expressions dataset is excluded unless the user separately changes the clean-room rule.

---

# Part IX — Scale and launch constitution

## 27. Scale gates

### Gate G0 — Constitution

No source download or compiler implementation until decisions C-01 through C-16 are approved or explicitly deferred.

### Gate G1 — Prototype

- deterministic source freeze;
- candidate lineage;
- resumable stages;
- no public family output.

### Gate G2 — First 100 commissioning batch

- at least 2,000 normalized clean-room candidates;
- exactly 100 completely passed families;
- complete Library Result Tile and Full Family Card for each;
- complete analysis for every displayed form;
- 100% commissioning audit;
- four private packs of 25;
- measured throughput, cost, defects, rebuild time, and mobile performance;
- no learner exposure.

Binding plan: `planning/EXPRESSIONS_FIRST_100_PLAN.md`.

### Gate G3 — 1,000-family expansion validation

- corrections applied to compiler rules rather than patched release records;
- benchmark/confidence calibration;
- broader source, class, Difficulty, and register coverage;
- global duplicate and reverse-link audits;
- no learner exposure unless separately authorized.

### Gate G4 — 10,000-family launch candidate

- full Source packs/indexes;
- Android performance;
- global duplicate graph;
- destructive migration rehearsal;
- 100,000-candidate dry run;
- complete transaction test.

### Gate G5 — 25,000

Source/register diversity and drift audit.

### Gate G6 — 50,000

Index/shard and global duplication stress test.

### Gate G7 — 100,000

Target-scale clean rebuild and release audit.

---

## 28. Launch alternatives

### Option T1 — Cut over at 1,000

Fast but insufficient evidence that the industrial pipeline and runtime scale.

### Option T2 — Cut over at 10,000 plus a 100,000-candidate dry run — **Recommended**

Provides forty times the former family count, proves factory throughput, and avoids withholding value until every target family is complete.

### Option T3 — Cut over at 25,000

More conservative content coverage; longer wait.

### Option T4 — Cut over only at 100,000

Maximum first-release count but delays learner access and makes cutover risk much larger.

### Decision C-14 — Earliest cutover

**Recommended:** T2. Releases after cutover grow immutably through 25,000, 50,000, and 100,000.

---

# Part X — Destructive state and backup constitution

## 29. Live progress deletion

At final cutover:

- delete every row from `expression_progress`;
- do not map old IDs;
- retain the table for new `expression2:` state unless schema design later requires a versioned replacement table;
- verify all non-Expressions account tables are unchanged;
- initialize the new corpus with zero Recognised and zero Review markers for every account.

The purge must not exist in pre-cutover runtime code.

---

## 30. Backup deletion alternatives

The user selected permanent deletion. Old Koto-managed backups may still contain `expression_progress`, so a live database purge is not sufficient.

### Option B1 — Purge live rows only

Simple, but not genuinely permanent while old backups remain.

### Option B2 — Scrub Expressions rows from every Koto-managed backup while preserving all other backup data — **Recommended**

Process:

1. enumerate only Koto-managed backup archives;
2. create a working copy;
3. safely extract and validate paths;
4. open copied SQLite database;
5. delete `expression_progress` rows;
6. checkpoint and integrity-check SQLite;
7. rebuild archive deterministically;
8. compare all non-database files by hash;
9. compare every non-Expressions table by canonical dump;
10. replace original backup atomically only after validation.

Advantages: fulfils permanent Expressions deletion while preserving unrelated recovery data.

Risk: complex archive rewriting requires extensive transaction tests and free-space checks.

### Option B3 — Delete every Koto-managed backup

Strong deletion but destroys unrelated rollback protection.

### External copies

Koto cannot delete manually copied archives, device backups, cloud backups, or third-party snapshots it does not control. The cutover report must state this boundary truthfully.

### Decision C-15 — Backup boundary

**Recommended:** B2.

---

# Part XI — Runtime structural contract

## 31. Behaviour that remains recognizable

- Expressions entry within Extra
- searchable library
- Koto Difficulty 1–5
- Library at least equal to the previous release’s depth: verified hero/source state, progress, intention-oriented search, full filter set, native mobile selectors, verified result summary, and high-quality result tiles
- Library Result Tile contains Difficulty, category, Japanese, reading, contextual meaning, intentions, Recognised/Review, and Open
- **Card** means the complete opened Full Family Card, not the Library Result Tile
- Full Family Card contains close; Difficulty/category/VERIFIED; primary Japanese/reading/meaning/TTS/summary; state; intentions; guidance; analyzed forms; responses; follow-ups; dialogue; patterns; comparisons; verification/sources
- every displayed primary/alternate form has complete tappable sentence analysis
- no stripped-down Library or Full Family Card substitution for performance
- binding contracts: `planning/EXPRESSIONS_LIBRARY_SPEC.md` and `planning/EXPRESSIONS_FAMILY_CARD_SPEC.md`
- forms/register comparison
- use/avoid/relationship guidance
- responses and follow-ups
- dialogue, patterns, and comparisons
- Japanese device TTS only
- mutually exclusive Recognised/Review
- account isolation
- remote immutable content
- session-only content caching

## 32. Internals allowed to change

- Source schema and directory layout
- family IDs
- pack size/count
- search index architecture
- lazy-loading strategy
- backend support inventory encoding
- analysis schema and compiler
- API payload shape when versioned safely
- release and audit manifests

### Decision C-16 — Structural contract

**Recommended:** approve sections 31–32.

---

# Part XII — Approval ballot

## 33. Recommended decision bundle

Approve all recommendations as one coherent foundation:

- **C-01:** broad attested expression-family mission
- **C-02:** nine primary classes plus extensible facets
- **C-03:** ten mandatory inclusion tests
- **C-04:** evidence-first hybrid routes
- **C-05:** global merge/split policy
- **C-06:** conservative source permission matrix
- **C-07:** CC BY-SA 4.0 target licence, subject to compatibility review
- **C-08:** new `expression2:` namespace with UUIDv7 IDs and separate slugs
- **C-09:** normalized authoring authorities plus compiled runtime records
- **C-10:** require complete rich-family layers and analysis for every displayed primary/alternate form (binding correction)
- **C-11:** Koto Difficulty anchors
- **C-12:** unresolved important form analysis quarantines the family; no learner-visible plain published form (binding correction)
- **C-13:** proposed pilot quality objectives
- **C-14:** earliest cutover at 10,000 passed families plus 100,000-candidate dry run
- **C-15:** scrub legacy Expressions progress from Koto-managed backups while preserving other data
- **C-16:** preserve learner behaviour while allowing internal architecture changes

Approval syntax:

```text
Approve C-01 through C-16 as recommended.
```

Or approve with changes:

```text
Approve all except C-08 and C-14.
C-08: use monotonic IDs.
C-14: cut over at 25,000.
```

---

## 34. What approval would authorize

Approval authorizes the next specification artifacts:

1. source-registry JSON schema;
2. family v2 JSON schema;
3. analysis v2 JSON schema;
4. candidate-ledger schema;
5. compiler-stage contracts;
6. audit-manifest schema;
7. deterministic fixture design;
8. implementation work plan with measured prototype checkpoints.

Approval does **not** yet authorize:

- downloading bulk source datasets;
- generating actual families;
- modifying current Koto runtime;
- changing public Source;
- deleting learner state or backups;
- creating a package;
- cutting over production.
