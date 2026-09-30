# Koto Expressions — From-Scratch Rebuild Instructions

## Controlling user decision

The user has superseded the former Expressions expansion and preservation plan.

The new direction is:

- Rebuild the **Expressions corpus and analysis system from scratch**.
- Retain only the module’s overall structure and working behaviour: searchable expression families, Koto Difficulty, rich family sheets, Japanese device TTS, and mutually exclusive Recognised/Review mechanics.
- The Library must preserve the previous product level: verified hero/source state; personal progress and family/form totals; “Find an intention, not just a spelling”; Japanese/reading/meaning/intention/context search; Difficulty, Category, Personal status, Sort, Reset; native mobile selection like the supplied screenshot; verified result summary; and complete result tiles with Difficulty, category, Japanese, reading, contextual meaning, intentions, Recognised/Review, and Open.
- Terminology correction: **Card** means the complete opened Full Family Card, not the Library Result Tile. It must include close; Difficulty/category/VERIFIED; primary Japanese, reading, contextual meaning, Japanese device TTS and summary; Recognised/Review; intentions; Use When/Take Care/Relationships; all published forms with labels, reading, meaning, TTS and tappable sentence analysis; responses; follow-ups; dialogue; reviewed patterns/examples; nearby distinctions; verification/sources.
- Every displayed primary or alternate form must pass complete new analysis. A known important unresolved form quarantines the family; do not publish it as plain text or omit it merely because analysis is difficult.
- Binding surface specifications: `planning/EXPRESSIONS_LIBRARY_SPEC.md` and `planning/EXPRESSIONS_FAMILY_CARD_SPEC.md`. Obtain scale through sharding, bounded result rendering, one-card-at-a-time rich loading, and parallel compilation—not by reducing Library or Full Family Card content.
- Do not use the current 260-family dataset, its annotations, decisions, segmentations, links, or generated explanations as input truth for the replacement.
- The replacement production method must be industrial rather than family-by-family manual annotation. The selected broad direction remains a confidence-gated batch compiler intended to scale toward **100,000 expression families**.
- The user selected **exactly 100 fully passed families for the first commissioning batch**. Do not manually author only 100 candidates: mine at least 2,000 normalized clean-room candidates, quarantine/reject failures, and continue through the ranked pool until 100 pass. Audit all first 100. Keep them private/shadow; this is not cutover authorization.
- The binding first-batch plan is `planning/EXPRESSIONS_FIRST_100_PLAN.md`.
- An architecture preference or planning approval is not implementation authorization. Explain consequential options, mark one **Recommended**, and wait for the user’s choice before new design or implementation work.

## Explicit destructive decisions

The user selected all of the following:

1. **Public Source:** delete the existing public Expressions dataset from `TheSunphis/Source` at the final cutover.
2. **Learner state:** permanently delete all existing `expression_progress` rows at the final cutover; do not map them to the new corpus.
3. **Timing:** use an **atomic cutover after the replacement passes**. Until then, the current public dataset and runtime must remain operational.
4. **Packages:** the validated `.85` and `.86` standalone packages were explicitly retired and deleted immediately. Do not recreate them.

These decisions have different execution times:

- Package deletion is complete.
- Public Source deletion must **not** happen before the approved replacement passes, because current Koto still downloads that immutable release.
- The `expression_progress` purge must **not** be added to the current runtime. It belongs only to the final approved cutover migration.

## Current transitional runtime

Until cutover, the source tree still serves the temporary legacy catalogue:

- Immutable Source commit: `a05fa6c54e948bfaa9cc943edcc41f2129253a95`
- Release: `0.6.0-development`
- Active boundary: 260 families and 429 distinct forms
- Local state boundary: `src/data/expressions/family-ids.json`
- Current runtime has no sentence-analysis or Vocabulary-link layer.
- Search, family sheets, Japanese device TTS, and Recognised/Review continue working during the transition.

Do not confuse this temporary operational dependency with input authority for the new corpus. The replacement starts from an empty corpus namespace.

## No standalone release during the rebuild

There is currently no designated self-contained Termux package. Do not package or present an intermediate source snapshot.

A future standalone package may be created only after:

- the replacement corpus and compiler have passed the user-approved quality gates;
- the atomic Source/runtime cutover is authorized;
- the destructive progress migration is explicitly included and tested;
- a real preservation/activation/restart/health transaction passes for all non-Expressions account data.

`koto-termux-updater.sh` remains only the transactional updater foundation during this period.

## Industrial quality principles

The old method achieved strong local quality but scaled linearly and its audit checked emitted links more reliably than missing links. Do not reproduce that failure mode.

The future system must be designed around:

- immutable and licensed source inputs;
- deterministic batch compilation;
- exact Japanese and reading reconstruction;
- canonical Vocabulary identity checks;
- bidirectional completeness checks that detect valid candidates the compiler omitted;
- calibrated confidence rather than unverified model certainty;
- explicit abstention and quarantine for ambiguous output;
- reproducible versioned batches;
- bounded quality sampling and adversarial tests;
- separate automated extraction, editorial review, and verification claims;
- rollback before public cutover.

Manual effort may create benchmark material, review samples, and resolve exceptional ambiguity. It must not be the main production path for 100,000 families.

## From-scratch isolation

The new corpus must use new staged authorities and a new namespace selected through user-approved design. Do not silently copy:

- current family records;
- old family IDs;
- old candidate assignments;
- old editorial decisions or batch audits;
- `.85` analysis artifacts;
- generated segment explanations;
- prior Vocabulary resolutions;
- legacy review-status labels.

Historical material may be consulted only if the user later authorizes a narrowly defined benchmark or forensic comparison. It may never be imported wholesale as replacement truth.

## Cutover contract

The final cutover must be one reviewed transaction, not gradual accidental mixing.

At cutover, and only after all gates pass:

1. Publish the approved new immutable Source release.
2. Switch Koto’s Source identity and support inventory atomically.
3. Remove the former public Expressions dataset from the active public Source tree as the user directed. Git history may still retain earlier commits.
4. Purge all rows from `expression_progress` through an explicit, tested migration.
5. Verify that no Expressions operation writes Vocabulary progress, notes, schedules, or history.
6. Preserve every non-Expressions account record and runtime file.
7. Run staged validation, activation, restart, authenticated API checks, browser-shell checks, and rollback assertions.
8. Produce a new self-contained Termux package only after the transaction passes.

## Decisions still required before implementation

Do not infer answers to these remaining design questions:

- authoritative input strategy for the new corpus;
- exact definition and allowed scope of an expression family at 100,000-family scale;
- new IDs and namespace;
- required fields per family;
- publication-gate unit and abstention policy;
- confidence calibration and benchmark construction;
- batch sizes and scale-up gates;
- Source repository layout and release policy;
- whether analysis is part of initial corpus publication or a later compiled layer;
- learner-facing behaviour when a form abstains.

Present options in small consequential groups, include an explicit **Recommended** label, and wait for the user to decide.

## Product and workspace constraints

- The canonical product name is **Koto**. Do not rename it without explicit confirmation.
- The module is **Expressions**, not Phrases.
- “Graded” means Koto Difficulty, not CEFR, JF, or JLPT.
- Do not display Commonness; use Difficulty.
- Japanese audio is device TTS only.
- Work only in `/home/user/japanese-learning-app`.
- Do not create another checkout or duplicate application folder.
- Use bounded commands and concise checkpoints; avoid recursive output floods and opaque long-running command chains.
- Live previews may use only minimal data and must be stopped promptly.
- Never expose credentials. GitHub authorization may exist at `/home/user/.config/gh/hosts.yml`; read it only inside an authorized publishing operation and never print it.
- Do not modify `.github/workflows/*`; available OAuth has no workflow scope.

## Current completion state

Completed:

- Removed the rejected sentence-analysis implementation from current Koto.
- Added and validated the temporary 260-ID runtime inventory.
- Retired and deleted both `.85` and `.86` standalone packages by explicit user choice.
- Recorded that public dataset deletion and learner-state deletion occur only at final atomic cutover.
- Wrote the proposed master plan at `planning/EXPRESSIONS_FROM_SCRATCH_MASTER_PLAN.md`.
- Wrote the proposed corpus constitution and C-01–C-16 decision ballot at `planning/EXPRESSIONS_CORPUS_CONSTITUTION.md`.
- Recorded the binding Library contract at `planning/EXPRESSIONS_LIBRARY_SPEC.md`.
- Recorded the binding complete opened-card contract at `planning/EXPRESSIONS_FAMILY_CARD_SPEC.md`.
- Recorded the exactly-100 commissioning run at `planning/EXPRESSIONS_FIRST_100_PLAN.md`.
- Planning artifacts are not implementation authorization.

Not started:

- New corpus schema
- New source acquisition
- New family generation
- New compiler implementation
- New benchmark
- New public Source release
- Destructive cutover migration

Do not claim that the from-scratch replacement exists until those stages are explicitly designed, authorized, implemented, and verified.
