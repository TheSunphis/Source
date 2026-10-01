# Valkyrie1 due — one gold Card

- Exact agent: `Valkyrie1`
- Assignment: `germinal-goldcard-ii-yo-valkyrie1-1`
- Launch state: `ACTIVE`
- Exact slot: `V1-GOLD-001`
- Output scope: one candidate-specific Full Expression Card
- Public report: `Germinal/Valkyrie/Valkyrie1/report.md`

Wave 002 is failed audit evidence and is not a content source. Rebuild the selected target from the exact original dossier and the new bounded Vocabulary seed. Do not reuse the rejected generic intentions, contexts, five-line support template, or dialogue frame.

## Private gold material

- Release ID: `401068873`
- Bundle: `germinal-goldcard-ii-yo-material-v1.tar.gz`
- Bytes: `2311`
- SHA-256: `26f5ade563e9f4eca8a1afd1a106c74215961090067e6d48685611a218e0095d`
- Contents: exact original dossier plus Zero's one-slot assignment contract

## Canonical Vocabulary seed

- Release ID: `401067757`
- Bundle: `koto-vocabulary-goldcard-seed-v1.tar.gz`
- Bytes: `1947`
- SHA-256: `382de490cbc26463c98fd6837856cecbb019233fa17f4818723e0dd6ad207d1c`
- Build ID: `vocabularybuild1:e43cee2b001e9fd512f2ccd5e66deb88`
- Zero-provided identities: `vocabulary2:9388217c802184c295872c8415e616c2`, `vocabulary2:0c6dad3ba8bac1f9b07660f354af8b13`

The seed is evidence and identity input. The proposal validator deliberately keeps every `selectedVocabularyId` null. Supply surface/reading/lemma candidates; Zero alone expands the registry and compiles real links after the proposal passes. Never mint an ID.

## Infrastructure

Core transport and expression validation:

- Commit: `5eccc8e4c768bce21ff00398cb172f97617d3f24`
- Tool: `Germinal/infrastructure/germinal_tool.py`
- SHA-256: `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`

Gold validator and packager:

- Commit: `68102abf9e9aac39989881849d89b12285258959`
- Tool: `Germinal/goldcard/goldcard_tool.py`
- SHA-256: `acbd61452325517af2dffb7c57aaa5159dc37a8ff5b95dfb1ef404278fca3aa1`
- Schema SHA-256: `e0c51d3409b503f4ba9524d0a01981c1af4a4995ef00d09a36cbc7695b8c0999`

Place the verified core and gold tools together so `goldcard_tool.py` imports the pinned core. Run both self-tests. Do not patch or replace them.

## Authoring contract

Create a concrete Card for the target Expression in a specific believable interaction. External dossier evidence anchors the target form, reading, meaning boundary, and factual claims. Editorial teaching material is permitted only as `editorial:Valkyrie1` proposal content and remains independently reviewable.

Required:

- substantive candidate-specific intention, Use when, Take care, and relationship guidance;
- at least two context-fitting responses and two context-fitting follow-ups;
- a concrete dialogue with at least three turns and three distinct analysed lines;
- at least seven distinct Japanese lines across the Card;
- complete meaningful segmentation for every displayed line;
- exact target segmentation into `いい` and final particle `よ`;
- complete forms, Library fields, provenance, source identities, and Koto Difficulty;
- honest alternate-form, pattern, and distinction decisions;
- a `specificityAudit` explaining why every response/follow-up fits, the dialogue is coherent, and each omission is justified.

Do not write generic placeholders such as “dossier-anchored meaning” or a context that merely says one speaker uses the target. Do not add unsupported variety. Do not use Commonness, CEFR/JF/JLPT grades, or external TTS.

## Output format

Manifest:

- `formatVersion`: `germinal-goldcard-valkyrie-v1`
- `agent`: `Valkyrie1`
- `assignment`: `germinal-goldcard-ii-yo-valkyrie1-1`
- `expectedSlotIds`: [`V1-GOLD-001`]
- exact attempted/submitted/abstained/failed conservation for one slot
- `recordSha256`: canonical Gold-tool record digest
- exact `inputAsset`, `vocabularySeedAsset`, `evidenceBuild`, and `candidateBuild` identities

Record: `slotId`, `status`, and either the Full Expression object or an honest `reasonCode`.

Commands:

```text
python3 goldcard_tool.py validate manifest.json record.json
python3 goldcard_tool.py package manifest.json record.json germinal-valkyrie1-goldcard-ii-yo-v1.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-goldcard-ii-yo-valkyrie1-1 germinal-valkyrie1-goldcard-ii-yo-v1.tar.gz
```

## Completion

Update the safe public report with one output bundle's bytes, SHA-256, and private release IDs. Include no Japanese, meanings, evidence, analyses, or payload excerpts. Publish the report with the pinned core tool and stop. Zero will validate, expand the registry, compile links, and only then decide whether Crow receives the Card.
