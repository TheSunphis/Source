# Crow1 due — issue-specific repaired gold Card review

- Exact agent: `Crow1`
- Assignment: `germinal-goldcard-ii-yo-crow1-review-repair-1`
- Launch state: `ACTIVE`
- Expected reviews: `1`
- Exact slot: `V1-GOLD-001`
- Role: independent critic; do not repair
- Public report: `Germinal/Crow/Crow1/report.md`

The user approved the evidence-locked Card after one exact learner-facing wording clarification. Review the clarified, canonically linked Card. Earlier broad assurances are not acceptable.

## Immutable restricted inputs

Original evidence dossier:
- Release ID: `401068873`
- Bundle: `germinal-goldcard-ii-yo-material-v1.tar.gz`
- Bytes: `2311`
- SHA-256: `26f5ade563e9f4eca8a1afd1a106c74215961090067e6d48685611a218e0095d`

User-approved clarified proposal:
- Release ID: `401107799`
- Bundle: `germinal-goldcard-ii-yo-zero-clarified-v1.tar.gz`
- Bytes: `6088`
- SHA-256: `eaeeb56978d573e10b8273d764b753106ed05d2ac0d037275df00d1c2e7b7cc7`

Canonical Vocabulary build:
- Release ID: `401110574`
- Bundle: `koto-vocabulary-goldcard-repair-build-v1.tar.gz`
- Bytes: `9267`
- SHA-256: `6f5e6cfb09af286aac36cd069a7ac8127c689632e389f6908736db2218e1e6f1`
- Build ID: `vocabularybuild1:8e6a82612d02c2df724795773cdab8b1`
- Records: `36`

Compiled Card:
- Release ID: `401110587`
- Bundle: `germinal-goldcard-ii-yo-compiled-repair-v1.tar.gz`
- Bytes: `7597`
- Bundle SHA-256: `859b747d4ac3ae53f54230bf5e658b464ecbbd7bcd2f0d7261ea88f26dc63602`
- Card SHA-256: `a637009768152ed225238aba055a5f3182ff4c68ac653c04743641ef68a5e2a0`
- Segments: `32`; linked: `28`; punctuation exclusions: `4`

Reconstruct every asset from authenticated draft-release body chunks. Verify identities before opening payloads.

## Infrastructure

- Upload core `germinal_tool.py`, commit `5eccc8e4c768bce21ff00398cb172f97617d3f24`, SHA-256 `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`
- Review tool `gold_crow_repair_tool.py`, commit `518e995d1f247fc10c4cb68a1092be9ca1fedb1f`, SHA-256 `f05cc5ca70f72962475f77e2512bebf0e5608af2766e054d39d6d72b7f951e4d`
- Schema SHA-256: `480a9cb6b209c8a9047c61cb9525a34a40b1b63a12bf25684e6a58a7cdd30562`

Run every self-test. Do not patch infrastructure.

## Required issue-specific checks

Return all sixteen exact check IDs required by the tool. For each, provide a substantive rationale, one primary JSON pointer, at least two supporting pointers, and a concrete evidence locator. Independently inspect:

1. `reassuranceBoundaryExcludesPermission` — the target is reassurance after apology, never authorization to act.
2. `minorApologyTriggerIsConcrete` — the trigger is a specific low-stakes apology with no concealed serious harm.
3. `primaryAdjectiveFinalParticleSegmentation` — adjective and final particle are separate and complete.
4. `finalParticleForceIsSubstantive` — explain the final particle’s force in this reassurance, not merely that it adds emphasis.
5. `casualContractionAnalysisIsAccurate` — verify the contracted past auxiliary and its accidental/regrettable contribution.
6. `declaredSegmentationPolicyIsConsistent` — apply the declared target and support-verb policies everywhere relevant.
7. `repeatedFormsUseCompatibleAnalysis` — repeated or inflectionally related forms do not receive contradictory analyses.
8. `socialClosureAndPracticalCleanupCoexist` — ending further apology does not deny ordinary cleanup.
9. `allDisplayedLinesAreNaturalAndComplete` — review every line, not a sample.
10. `readingsAndMeaningsAreContextAccurate` — review every line and contextual segment meaning.
11. `responsesFitReassuranceContext` — both responses are natural consequences of reassurance.
12. `followUpsFitMinorAccidentContext` — both follow-ups are coherent and do not reintroduce permission drift.
13. `registerRelationshipAndSafetyAreAligned` — casual relationship and warnings are adequate.
14. `canonicalLinksReverseCheckExactly` — all 28 links have exact form/reading matches and correct senses; all four exclusions are punctuation only.
15. `expressionClaimsDoNotExceedEvidence` — distinguish JMdict lexical anchors from expression-level attestation and editorial teaching content.
16. `patternsAndDistinctionsAreHonestlyDeferred` — unsupported productive patterns or contrasts are not manufactured.

A structural pass is not evidence. Resolve every pointer and test each claim. If any required gate fails, recommend quarantine and report the finding; do not repair it.

## Output

- Manifest format: `germinal-goldcard-crow-repair-v2`
- Assignment: `germinal-goldcard-ii-yo-crow1-review-repair-1`
- Expected slot IDs: [`V1-GOLD-001`]
- Bundle: `germinal-crow1-goldcard-ii-yo-review-repair-v2.tar.gz`
- Private release title: `germinal-goldcard-ii-yo-crow1-review-repair-1`

```text
python3 gold_crow_repair_tool.py validate manifest.json review.json
python3 gold_crow_repair_tool.py package manifest.json review.json germinal-crow1-goldcard-ii-yo-review-repair-v2.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-goldcard-ii-yo-crow1-review-repair-1 germinal-crow1-goldcard-ii-yo-review-repair-v2.tar.gz
```

Publish one safe report with recommendation counts, release IDs, output bytes, SHA-256, and conserved counts. Then stop. Never place findings, Japanese, meanings, evidence, or payload excerpts in Git.
