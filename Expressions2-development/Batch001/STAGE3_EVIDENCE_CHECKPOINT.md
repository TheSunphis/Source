# Expressions2 Batch 001 — Stage 3 Evidence Checkpoint

**Date:** 2026-09-30  
**Verdict:** PASS with one declared morphology dependency gate  
**Build:** `evidencebuild2:9cd5cd34b9a3ba1232486711636ad10d`  
**Candidate generation:** not started

## Frozen evidence result

Seven pinned sources produced **423,088 deterministic evidence records**:

| Store | Records | Canonical bytes | Compressed bytes | Permission |
|---|---:|---:|---:|---|
| JMdict labelled expressions | 15,516 | 7,202,666 | 2,083,756 | redistributable |
| Tatoeba CC0 Japanese | 2 | 1,061 | 540 | redistributable |
| Tatoeba Japanese CC BY | 248,917 | 91,736,071 | 23,925,231 | evidence-only |
| Japanese Wiktionary structural expressions | 565 | 185,777 | 53,665 | evidence-only |
| Japanese WordNet high-confidence links | 158,068 | 49,039,954 | 12,860,634 | tool-only |
| SudachiDict inventory | 7 | 2,824 | 974 | tool-only |
| UniDic inventory | 13 | 4,269 | 1,484 | tool-only |
| **Total** | **423,088** | **148,172,622** | **38,926,284** | — |

Every adapter rebuilt its output twice from the same pinned raw bytes. All canonical bytes matched. Canonical JSON ordering and GZip `mtime=0` are enforced.

## Evidence characteristics

- JMdict provides 15,501 unique labelled-expression surfaces, with median surface length 5 characters.
- Tatoeba CC BY provides 248,917 unique Japanese sentence texts, median length 16 characters.
- The CC0 snapshot contains only two usable Japanese records, both licence statements. It cannot materially support Batch 001 attestation.
- Wiktionary contributes 565 unique titles under conservative structural expression markers; 255 overlap a JMdict labelled surface.
- WordNet contains 87,997 unique Japanese lemmas across 57,239 synsets.
- JMdict alone provides substantially more than the 2,000-candidate commissioning floor, but admission still requires independent evidence routes and later filtering.

## Safety and licence outcomes

- Legacy contamination audit: PASS, zero findings.
- High-risk Wiktionary text is not retained.
- Evidence-only/tool-only payloads are private and excluded from GitHub.
- Raw source archives and build caches were deleted.
- No candidate, family, analysis, runtime, preview, learner state, or current Source file was created or modified.

## Defects found and fixed at the adapter level

1. The first CC0 parser treated non-Japanese all-language rows as Japanese, causing an interrupted oversized build. No evidence artifact was committed; the stale temporary cache was deleted. The parser now requires the `jpn` language code.
2. Tatoeba `\\N` placeholders were initially retained. The shared adapter now rejects them; the changed-only rebuild reduced CC0 from 14 records to 2.
3. Japanese WordNet can contain repeated synset/lemma rows. Stable zero-padded line identity was added so evidence locators and IDs remain unique.
4. Namespace-free Wiktionary test fixtures exposed an XML lookup edge. The adapter now handles namespaced production XML and namespace-free fixtures without widening retained fields.

## Throughput and rebuild architecture

- Final full source download + two-pass evidence build: approximately 230 seconds.
- Effective final throughput: approximately 1,838 evidence records/second, including downloads, two adapter passes, schema validation, hashing, and compression.
- Changed-only CC0 rebuild: approximately 12 seconds; six unaffected artifacts were re-verified and reused.
- Full persisted private evidence: 38.9 MB.

## GitHub storage correction

The user subsequently directed that durable Batch 001 work use the public `TheSunphis/Source` repository rather than local workspace storage. The temporary application-repository workflow, `.gitattributes`, cache rules, private evidence payloads, and incomplete candidate builder were removed locally.

Only redistribution-safe code, schemas, hashes, counts, licence routing, and manifests may enter a public Source branch. Evidence-only/tool-only payloads must remain unpublished draft-release assets or be regenerated; they must never be committed publicly.

## Final validation

```text
schemas=15 positive=14 negative=14 registry=1 snapshots=7 evidence=7
11 contract tests: OK
8 offline adapter tests: OK
clean-room guard: PASS
GitHub metadata-only checkout simulation: PASS
Stage 3 final integrity: PASS
```

The default local validator fully decompresses, hashes, schema-validates, permission-checks, and contamination-checks all seven private evidence stores. GitHub metadata-only mode verifies the committed manifest and source/snapshot relationships while requiring private payloads to be absent.

## Declared next gate

SudachiPy, MeCab, Fugashi, and UniDic frontends are not installed. The pinned SudachiDict and UniDic archives are verified, but only their inventories can be used until a morphology runtime is explicitly selected and approved.

**Recommended next decision:** approve a pinned, licence-reviewed SudachiPy runtime for deterministic normalization and use UniDic only as an independent dictionary/reading cross-check through an explicitly selected compatible frontend. Candidate generation should begin only after that dependency gate, then produce at least 2,000 normalized candidates without weakening admission rules.
