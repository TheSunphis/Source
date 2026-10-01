# Expressions2 Batch 001 — Stage 1 Checkpoint

**Date:** 2026-09-30  
**Verdict:** PASS  
**Release impact:** none; private clean-room contracts only

## Completed

- Implemented 14 strict JSON Schema Draft 2020-12 contracts for source registry, snapshots, evidence, raw and normalized candidates, family ledger, full family, complete form analysis, provenance, compiler/audit manifests, Library index, and runtime Full Family Card.
- Generated 13 deterministic positive and 13 deterministic negative synthetic fixtures. Fixture text is not corpus content.
- Implemented semantic validation beyond JSON Schema:
  - one primary form;
  - primary/hero/Library identity;
  - dynamic form, family, and category totals;
  - exact Japanese and reading reconstruction;
  - contiguous analysis spans;
  - one Vocabulary enumeration per segment and exact selected-link consistency;
  - family ↔ analysis bijection;
  - append-only ledger sequence/hash chain;
  - unique IDs, slugs, and artifacts;
  - class and Difficulty totals summing to exactly 100;
  - four family/analysis packs and exactly 25 runtime families per pack.
- Implemented the clean-room guard for prohibited runtime paths, legacy-lineage fields, non-`expression2:` family IDs, and symlinks.
- Created the source registry and source verification report with exact HTTPS acquisition proposals.
- Verified approved endpoints with metadata-only checks and selected the dated Japanese Wiktionary 2026-09-01 dump.
- Selected UniDic for Contemporary Written Japanese 3.1.0 under the BSD New option.
- Reviewed SudachiDict’s upstream Apache 2.0, UniDic BSD, and component notice route and recorded the exact PyPI wheel identity.

## Test result

```text
schemas=14 positive=13 negative=13 registry=1
PASS: all contract schemas, fixtures, semantic invariants, and source registry checks passed
11 tests run
OK
EMPTY_DATA_STAGES=PASS
```

## Source snapshot proposals

All seven registry entries are now `approved-for-snapshot`, which authorizes only a controlled acquisition attempt—not use or publication:

1. JMdict English
2. Tatoeba CC0
3. Tatoeba Japanese CC BY 2.0 FR, evidence-only
4. Japanese Wiktionary dated 2026-09-01, evidence-only
5. Japanese WordNet 1.1 high-confidence links, tool-only
6. SudachiDict Core 20260723.1, tool-only
7. UniDic Contemporary Written Japanese 3.1.0, tool-only

The reported combined download is approximately 795 MB, dominated by the 603,549,853-byte UniDic ZIP. Large raw artifacts must be streamed through excluded temporary storage, verified, parsed later by approved adapters, and not retained in the persisted workspace.

## Explicit non-results

No source corpus bytes, evidence records, candidates, real families, form analyses, compiled packs, runtime index, family preview, or performance claim exist yet.

No public Source, live Expressions route, current 260-family runtime, learner state, backups, or standalone package was modified.

## Next gated stage

The next consequential action is controlled source acquisition. The recommended treatment is to acquire and verify all seven exact proposals, persist only snapshot/licence manifests, and stop for another checkpoint before parsing or candidate extraction.
