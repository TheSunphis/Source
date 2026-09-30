# Expressions2 Evidence-Store Licence Report

**Evidence build:** `evidencebuild2:9cd5cd34b9a3ba1232486711636ad10d`  
**Source date epoch:** 2026-09-30T18:43:04Z  
**Scope:** private Batch 001 evidence only; no candidate or learner-facing publication

## Output policy

All `*.evidence.json.gz` payloads are private build inputs and are excluded from GitHub by `.gitignore`. The GitHub-ready checkpoint contains only schemas, code, tests, hashes, counts, manifests, attribution routes, and licence notices.

| Source | Permission class | Evidence retained | Publication restriction |
|---|---|---|---|
| JMdict English | redistributable | labelled expression entry identity, forms, readings, English glosses, structured labels | CC BY-SA 4.0 attribution/share-alike and update route remain mandatory |
| Tatoeba CC0 | redistributable | Japanese sentence identity and text | only two non-placeholder Japanese records exist in this snapshot; both are licence statements and provide no useful expression attestation |
| Tatoeba Japanese CC BY | evidence-only | private sentence ID and normalized Japanese text for attestation/mining | do not copy into learner examples or GitHub; any future publication requires record-level attribution policy |
| Japanese Wiktionary | evidence-only | page/revision identity, title, and structural expression markers only | definitions, quotations, examples, and wikitext are intentionally absent; payload remains private |
| Japanese WordNet 1.1 `ok` | tool-only | line identity, synset, lemma, confidence marker | grouping/deduplication only; no definitions, examples, or evidence payload publication |
| SudachiDict Core | tool-only | ZIP member inventory, sizes, CRC, and compiled-dictionary classification | dictionary bytes are not retained or redistributed; preserve Apache/UniDic/NEologd notices |
| UniDic CWJ 3.1.0 | tool-only | ZIP member inventory, sizes, CRC, and compiled-dictionary classification | dictionary bytes are not retained or redistributed; BSD New notice route remains mandatory |

## Compatibility result

- The intended family dataset remains CC BY-SA 4.0.
- Evidence-only and tool-only stores may support decisions but cannot silently contribute copied learner-facing text.
- Original Koto explanations, dialogue, examples, and guidance must be compiled independently and checked for source-text copying.
- Source locators and hashes remain available for audit without exposing prohibited text.
- No source permission was widened by the adapter stage.
