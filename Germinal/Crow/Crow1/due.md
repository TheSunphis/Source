# Crow1 due — one linked gold Card review

- Exact agent: `Crow1`
- Assignment: `germinal-goldcard-ii-yo-crow1-review-1`
- Launch state: `HOLD_COMPLETED_ZERO_REJECTED`
- Exact slot: `V1-GOLD-001`
- Public report: `Germinal/Crow/Crow1/report.md`

Crow1 completed the rationale-bearing review. Zero reconstructed and structurally validated it after correcting an order-sensitive validator defect, but rejected the recommendation at the final semantic gate. Do not relaunch or issue another review unless Zero provides a new immutable due.

## Compiled Card input

- Release ID: `401083675`
- Bundle: `germinal-compiled-goldcard-ii-yo-v1.tar.gz`
- Bytes: `7393`
- SHA-256: `42b35053f5307bc359a2db8ff0a569b6a543870f747414cf257291921455071b`
- Card SHA-256: `70d1f571167d46973ee77acd575bdbc0349df76b6a68ef2ac0bd0104b9f9fde2`
- Links SHA-256: `6326582f8378517acf2fb3351ac16b29a991d3a7af3342a7d96810439f536777`
- Segments: `31`
- Linked: `27`
- Explicitly unlinked punctuation: `4`

## Canonical Vocabulary input

- Release ID: `401083650`
- Bundle: `koto-vocabulary-goldcard-build-v2.tar.gz`
- Bytes: `5599`
- SHA-256: `3c7cca7952704db37236c42f2fe74a8cc66cd8761ec4b8082745409cffaf7e8c`
- Build ID: `vocabularybuild1:af60894aa40e5d8ce58f7b5362ba4514`
- Records: `19`
- Source snapshot: official English JMdict SHA-256 `89777236dbf06f4d7b01c6dbff5e1f707978ddd067061b66bcb782d1f24e6ed3`

## Original proposal identity

- Release ID: `401073594`
- Bytes: `5783`
- SHA-256: `c7289083e48af3f5d06622ddc36cbd9fa0ed4d2f12f18d85e604eb602a7ec914`

Reconstruct all three assets with the pinned core API-body tool and verify every identity before opening.

## Infrastructure

- Core transport commit: `5eccc8e4c768bce21ff00398cb172f97617d3f24`
- Core tool SHA-256: `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`
- Compiled validator commit: `a589778665ea409e4f87f1479176ac2765e4f751`
- Compiled validator SHA-256: `dfa9f8f015cfe7d53b688e3590d954861a8c41842a50e3f187fc3dc356017711`
- Rationale-bearing Crow commit: `c6cc5eaa0cae838d4b75fd9f9d59ee78509e9e90`
- Crow tool SHA-256: `c9c5f30090597f54e6b4c4126327dc808089e17a799a908ff99457afb6cb9717`
- Crow schema SHA-256: `e7b31e000f7f3cace0e9031a05b2b7b5828de0740a0a3d1bbbde7c116b06b46f`

Run every self-test and validate the compiled Card against the exact registry before linguistic review.

## Independent review

Inspect external target evidence and boundary, every Japanese line, reading and meaning, every segment boundary/kind/lemma/inflection, every canonical Vocabulary selection and reverse check, the concrete responses and follow-ups, the three-turn dialogue, register and relationship safety, forms, omissions, patterns, distinctions, Library fields, provenance, and unsupported claims.

Pay special attention to:

- whether the target meaning in the permission situation remains within the externally supported boundary;
- whether the final particle's pragmatic explanation fits this exact utterance;
- whether repeated arrival and contact constructions use defensible, consistent segmentation and canonical records;
- whether the casual continuing-action contraction accurately supports its proposed English meaning;
- whether all responses and follow-ups are natural reactions or next steps for the concrete dialogue, not generic filler.

Canonical IDs and JMdict evidence do not prove sentence naturalness or pragmatic fit. Crow review is not an external source.

## Rationale-bearing output

Use format `germinal-goldcard-crow-v1`. Every one of these exact checks requires `passed`, a distinct rationale of at least 40 characters, a precise JSON pointer, and an evidence locator:

1. `targetEvidenceBoundary`
2. `japaneseNaturalness`
3. `readingMeaningAccuracy`
4. `segmentationLinguisticCorrectness`
5. `vocabularyLinkCorrectness`
6. `responsesContextFit`
7. `followUpsContextFit`
8. `dialogueCoherence`
9. `pragmaticsRegisterRelationship`
10. `formsPatternsDistinctions`
11. `libraryProvenance`
12. `noUnsupportedClaims`

A pass requires all checks true and zero findings. Quarantine requires precise findings. Do not hide a defect merely because another check passes.

Manifest assignment: `germinal-goldcard-ii-yo-crow1-review-1`; expected slot IDs: [`V1-GOLD-001`]; conserve one review and include exact compiled, Vocabulary, and proposal asset identities.

```text
python3 gold_crow_tool.py validate manifest.json review.json
python3 gold_crow_tool.py package manifest.json review.json germinal-crow1-goldcard-ii-yo-review-v1.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-goldcard-ii-yo-crow1-review-1 germinal-crow1-goldcard-ii-yo-review-v1.tar.gz
```

Publish one safe report with output bytes, SHA-256, private release IDs, and pass/quarantine count. Then stop. Zero alone decides acceptance.
