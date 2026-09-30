# Expressions2 Batch 001 — Stage 2 Source-Acquisition Checkpoint

**Date:** 2026-09-30  
**Authorized scope:** all seven registered source artifacts  
**Verdict:** PASS  
**Release impact:** none; source manifests and licence notices only

## Result

Seven exact artifacts totaling **797,077,693 bytes** were securely streamed, independently re-hashed, inspected without extraction, and pinned. All raw downloads were deleted. Persisted manifests and licence notices total approximately 504 KB.

| Source | Bytes | SHA-256 | Inspection |
|---|---:|---|---|
| JMdict English | 10,580,018 | `749f303d713157be1a4d873011aa32698ef6c633ee503d5cd3fb9f865ec82634` | GZip/JMdict XML prefix |
| Tatoeba CC0 | 7,961,039 | `ea567c9c3efef007eac9aecf0b518bd2845a92d16a1564ba40b003811dfca4d1` | safe TAR/BZip2, 1 member |
| Tatoeba Japanese CC BY | 3,417,560 | `1a71f25043f9ecff3f1d1910bb677e99b5bb620b9ed9b22cde60d67790669b11` | BZip2/TSV prefix |
| Japanese Wiktionary 2026-09-01 | 93,551,022 | `e2edbd9f0ff5b4f85703da21fdcad76a02ebbb27c2b238a449925cfa4ddb34fa` | BZip2/MediaWiki XML prefix |
| Japanese WordNet 1.1 `ok` | 1,079,974 | `770a3779425b8565d52db9900b49f2ded6526f71b3b996b8f78fb58b5cf52459` | GZip/TSV prefix |
| SudachiDict Core 20260723.1 | 76,938,227 | `2b711055dca03423869e491eca0ddbe3e17c4d7418ed738fd7c75d4e0eb9e4b1` | safe wheel, 7 members; compiled dictionary and notice present |
| UniDic CWJ 3.1.0 | 603,549,853 | `601bc4b0af794d3c20c2089771b8771209390e1b35b0f20c85cf0a10c9a98c6d` | safe ZIP, 14 members; `dicrc`, compiled `sys.dic`, and notice/readme present |

## Safety controls that passed

- exact registry state required before acquisition;
- HTTPS only;
- per-source redirect-host allowlists;
- per-source byte ceilings;
- known byte-length checks where available;
- published SudachiDict SHA-256 check;
- streaming hash plus independent second hash;
- path traversal, link/device, member-count, and member-size archive checks;
- format-specific prefix/member checks;
- licence-notice capture and hash;
- manifest schema validation before commit;
- all-or-nothing registry/manifest promotion;
- signed redirect query strings excluded from persisted final endpoint identities;
- temporary raw file and acquisition-cache deletion.

## Atomic rollback exercised

The first run reached UniDic and stopped because its inspector expected lexical CSV source while this official archive exposes the compiled `sys.dic`. Because promotion was atomic, all seven registry entries remained `approved-for-snapshot`, no manifests/notices were committed, and no raw file survived.

The check was corrected to match the documented artifact shape (`dicrc`, compiled `sys.dic`, and notice/readme), then the entire seven-source acquisition passed. The successful pass took approximately 52 seconds; both attempts transferred approximately 1.59 GB in total. No package was installed.

## Current validation

```text
schemas=14 positive=13 negative=13 registry=1 snapshots=7
PASS: all contract schemas, fixtures, semantic invariants, and source registry checks passed
11 tests run
OK
```

Validation now cross-checks every persisted snapshot against:

- the source registry’s pinned SHA-256, bytes, URLs, roles, status, and media type;
- the final endpoint host allowlist;
- the corresponding licence-notice file and hash.

## Explicit non-results

No source was parsed into an evidence store. No raw or normalized candidate, family cluster, real family record, form analysis, compiled pack, Library index, preview, or throughput claim exists.

No public Source, live route, current runtime, learner state, backup, or standalone package was modified.

## Next gated stage

The next stage is deterministic source adapters and frozen evidence stores. It is consequential because it will re-download the pinned artifacts, parse source content, and persist permitted normalized evidence. Recommended sequencing:

1. JMdict adapter and canonical lexical evidence;
2. Tatoeba CC0 and CC BY evidence-only adapters;
3. WordNet grouping adapter;
4. morphology adapters for SudachiDict/UniDic;
5. the higher-risk Wiktionary extractor last, with quotation/external-content exclusion tests;
6. stop for evidence counts, licence report, deterministic rebuild, and contamination audit before candidate generation.
