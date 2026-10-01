# Batch 001 Source Verification and Snapshot Record

**Checked/acquired:** 2026-09-30  
**State:** seven exact source snapshots verified and approved; raw downloads deleted  
**Machine-readable authorities:** `sources.json` and `../snapshots/manifests/*.snapshot.json`

## Approval meanings

- `approved-for-snapshot` means the source and role are approved for a controlled acquisition attempt. It does **not** claim that bytes have been fetched, parsed, or admitted.
- `proposed` means a legal, artifact, or component-notice issue remains. The acquisition tool must refuse it.
- A source reaches `approved` only after the exact bytes, final URL/version, byte length, SHA-256, media type, licence notice, and format checks are recorded.

## Approved snapshot set

| Source ID | Artifact proposal | Batch 001 role | Current state |
|---|---|---|---|
| `source2:jmdict-english` | `https://www.edrdg.org/pub/Nihongo/JMdict_e.gz` | candidate forms, readings, senses, canonical Vocabulary | approved; exact snapshot pinned |
| `source2:tatoeba-cc0` | `https://downloads.tatoeba.org/exports/sentences_CC0.tar.bz2` | attestation and pattern evidence | approved; exact snapshot pinned |
| `source2:tatoeba-japanese-ccby` | `https://downloads.tatoeba.org/exports/per_language/jpn/jpn_sentences.tsv.bz2` | evidence-only attestation | approved; exact snapshot pinned |
| `source2:japanese-wiktionary` | `https://dumps.wikimedia.org/jawiktionary/20260901/jawiktionary-20260901-pages-articles.xml.bz2` | evidence-only form/sense/attestation | approved; official 2026-09-01 snapshot pinned |
| `source2:japanese-wordnet-ok` | `https://github.com/bond-lab/wnja/releases/download/v1.1/wnjpn-ok.tab.gz` | tool-only semantic grouping and duplicate detection | approved; v1.1 snapshot pinned |
| `source2:sudachidict-core` | PyPI wheel `sudachidict_core-20260723.1-py3-none-any.whl` | tool-only morphology | approved; wheel hash and safe archive shape verified |
| `source2:unidic-modern-bsd` | `https://clrd.ninjal.ac.jp/unidic_archive/2302/unidic-cwj-202302.zip` | tool-only morphology and reading cross-check | approved; Contemporary Written Japanese 3.1.0 snapshot pinned under BSD New |

## Endpoint verification

A metadata-only HTTPS HEAD check on 2026-09-30 returned:

| Source ID | HTTP | Reported bytes | Note |
|---|---:|---:|---|
| `source2:jmdict-english` | 200 | 10,580,018 | `www.edrdg.org` is used because the `ftp.edrdg.org` HTTPS certificate does not match that hostname |
| `source2:tatoeba-cc0` | 200 | 7,961,039 | weekly mutable endpoint; acquisition hash will pin the bytes |
| `source2:tatoeba-japanese-ccby` | 200 | 3,417,560 | Japanese per-language TSV/BZip2 endpoint |
| `source2:japanese-wiktionary` | 200 | 93,551,022 | dated 2026-09-01 pages/articles dump |
| `source2:japanese-wordnet-ok` | 200 | 1,079,974 | GitHub release redirects to a time-limited asset URL; registry retains the stable release URL |
| `source2:sudachidict-core` | PyPI metadata | 76,938,227 | exact wheel SHA-256 already published in registry notes; acquisition rechecks it |
| `source2:unidic-modern-bsd` | 200 | 603,549,853 | exact non-full Contemporary Written Japanese 3.1.0 ZIP; process as a temporary stream because of workspace limits |

These lengths were proposal checks. The acquisition-stage identities below are authoritative.

## Pinned acquisition identities

| Source ID | Bytes | SHA-256 |
|---|---:|---|
| `source2:jmdict-english` | 10,580,018 | `749f303d713157be1a4d873011aa32698ef6c633ee503d5cd3fb9f865ec82634` |
| `source2:tatoeba-cc0` | 7,961,039 | `ea567c9c3efef007eac9aecf0b518bd2845a92d16a1564ba40b003811dfca4d1` |
| `source2:tatoeba-japanese-ccby` | 3,417,560 | `1a71f25043f9ecff3f1d1910bb677e99b5bb620b9ed9b22cde60d67790669b11` |
| `source2:japanese-wiktionary` | 93,551,022 | `e2edbd9f0ff5b4f85703da21fdcad76a02ebbb27c2b238a449925cfa4ddb34fa` |
| `source2:japanese-wordnet-ok` | 1,079,974 | `770a3779425b8565d52db9900b49f2ded6526f71b3b996b8f78fb58b5cf52459` |
| `source2:sudachidict-core` | 76,938,227 | `2b711055dca03423869e491eca0ddbe3e17c4d7418ed738fd7c75d4e0eb9e4b1` |
| `source2:unidic-modern-bsd` | 603,549,853 | `601bc4b0af794d3c20c2089771b8771209390e1b35b0f20c85cf0a10c9a98c6d` |
| **Total** | **797,077,693** | — |

Every artifact passed a second SHA-256 read and non-extracting container/prefix inspection. All raw files were deleted after verification. The persisted snapshot manifests and licence notices total about 504 KB.

## Verified licence facts and restrictions

### JMdict

The EDRDG general licence identifies the Japanese/English JMdict components as CC BY-SA 4.0, requires acknowledgement and licence/documentation routing, permits commercial use, and requires software using the data to provide a regular update procedure. Batch 001 pins exact bytes while preserving an explicit later update path.

### Tatoeba

Tatoeba’s official download page identifies the general sentence exports as CC BY 2.0 FR and separately provides a CC0 sentence export. Japanese appears in the CC0 language list. Batch 001 keeps CC BY Japanese sentences evidence-only; it does not copy them into learner-facing examples. CC0 record identity remains in provenance.

### Japanese Wiktionary

The pages/articles dump is evidence-only. Extraction must exclude quotations, media, fair-use content, and externally sourced or separately licensed text. No Wiktionary definition is copied into the family output.

### Japanese WordNet

The official 1.1 download page provides a high-confidence `wnjpn-ok.tab.gz` artifact. The licence permits use, copy, modification, and distribution with preservation of copyright and disclaimer notices. Batch 001 uses it only for internal semantic grouping and duplicate detection; definitions and examples are not published.

### SudachiDict

PyPI metadata checked on 2026-09-30 reports version `20260723.1`, wheel size `76,938,227`, and SHA-256 `2b711055dca03423869e491eca0ddbe3e17c4d7418ed738fd7c75d4e0eb9e4b1`. The official upstream `LEGAL` file states Apache 2.0 coverage and records the UniDic BSD and NEologd/component notices. Acquisition reproduced the published hash and confirmed the exact wheel contains a compiled dictionary and a licence/legal member. No package was installed.

### UniDic

The official NINJAL/UniDic download page identifies UniDic for Contemporary Written Japanese 3.1.0 (`unidic-cwj-202302.zip`) and offers GPL v2.0, LGPL v2.1, or BSD New. Batch 001 selects the BSD New option, whose notice permits source and binary redistribution with preservation of copyright, conditions, and disclaimer and prohibits endorsement. The exact non-full archive is tool-only and is not redistributed.

## Acquisition gate result

`tools/acquire_sources.py` executed the approved gate and:

1. refused redirects outside each source’s HTTPS host allowlist;
2. recorded sanitized final endpoint identity and version/date;
3. streamed each artifact through excluded temporary storage under a source-specific byte ceiling;
4. computed SHA-256 during download and confirmed it with a second complete read;
5. inspected archive members or decompressed prefixes without extraction;
6. persisted each licence notice and its SHA-256;
7. created seven valid `snapshot-manifest.schema.json` records;
8. promoted all seven registry entries atomically only after every artifact passed;
9. deleted every raw artifact and left no acquisition cache file;
10. made no candidate, family, runtime, learner-state, or live-route change.

The first acquisition attempt correctly rolled back atomically when an overly narrow UniDic inspection expected lexical source CSV rather than the archive’s compiled `sys.dic`. The rule was corrected to verify the documented compiled dictionary, notice/readme, and `dicrc`; the full acquisition then passed. No partial manifest or registry state from the failed attempt survived.
