# Valkyrie1 due — evidence-locked gold Card repair

- Exact agent: `Valkyrie1`
- Assignment: `germinal-goldcard-ii-yo-valkyrie1-repair-1`
- Launch state: `HOLD_COMPLETED_AWAITING_USER_PREVIEW`
- Exact slot: `V1-GOLD-001`
- Scope: repair one proposal; no Vocabulary compilation
- Public report: `Germinal/Valkyrie/Valkyrie1/report.md`

Valkyrie1 completed the evidence-locked repair. Zero reconstructed and validated the immutable proposal and is presenting it to the user. Do not relaunch or revise until the user explicitly approves or requests changes.

## Non-negotiable semantic lock

- Dialogue act: `casual-reassurance-after-minor-apology`
- Excluded act: `affirmative-permission`
- Source constraint: `frozen-candidate-reassurance-boundary`

The target reassures a familiar person after a minor apology, mistake, or inconvenience: there is no serious unresolved harm and no further repair is demanded. It must not grant permission to perform an action.

## Analysis policy

- Target segmentation: `ii-adjective-plus-yo-final-particle`
- Suru-taking nouns: `split-noun-and-support-verb` consistently wherever they occur
- Every displayed Japanese line requires complete meaningful analysis
- All `selectedVocabularyId` values remain null in this preview proposal
- Do not mint or reuse canonical IDs; Zero will link only after user approval

## Inputs

Original one-dossier material:

- Release ID: `401068873`
- Bundle: `germinal-goldcard-ii-yo-material-v1.tar.gz`
- Bytes: `2311`
- SHA-256: `26f5ade563e9f4eca8a1afd1a106c74215961090067e6d48685611a218e0095d`

Rejected prior proposal, for defect comparison only:

- Release ID: `401073594`
- Bytes: `5783`
- SHA-256: `c7289083e48af3f5d06622ddc36cbd9fa0ed4d2f12f18d85e604eb602a7ec914`

Do not preserve its permission scenario or inconsistent repeated-construction analysis merely because it already exists.

## Infrastructure

Retrieve these immutable tools into one directory and verify hashes:

- Core `germinal_tool.py`, commit `5eccc8e4c768bce21ff00398cb172f97617d3f24`, SHA-256 `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`
- Base `goldcard_tool.py`, commit `68102abf9e9aac39989881849d89b12285258959`, SHA-256 `acbd61452325517af2dffb7c57aaa5159dc37a8ff5b95dfb1ef404278fca3aa1`
- Repair `goldcard_repair_tool.py`, commit `5576866e9ffd13528689b24be5c1129ee138e32a`, SHA-256 `b19c05f77bb724fcd3c765f051333c54c9057227e2dca6159de88192c1b74918`
- Repair schema SHA-256: `ff98bd7e9275d28985424c68f57c173eea1ad86dfdb222736473ede94cf9f890`

Run every self-test. Do not patch infrastructure.

## Card requirements

Author concrete, candidate-specific content from the original dossier:

- a primary meaning that clearly conveys reassurance or “no problem / do not worry,” not permission;
- a specific minor-apology situation and appropriate familiar relationship;
- at least two natural responses to the reassurance;
- at least two useful follow-ups by the reassuring speaker;
- at least three coherent dialogue turns and seven distinct analysed lines;
- complete forms, intentions, Use when, Take care, relationships, Library fields, provenance, and honest pattern/distinction decisions;
- specific rationale for every response, follow-up, and dialogue choice;
- no generic Wave 002 boilerplate.

Add exact objects:

```json
"boundaryLock": {
  "dialogueAct": "casual-reassurance-after-minor-apology",
  "excludedDialogueActs": ["affirmative-permission"],
  "sourceConstraint": "frozen-candidate-reassurance-boundary"
},
"analysisPolicy": {
  "targetSegmentation": "ii-adjective-plus-yo-final-particle",
  "suruTakingNounPolicy": "split-noun-and-support-verb"
}
```

## Output

- Manifest format: `germinal-goldcard-valkyrie-v2`
- Assignment: `germinal-goldcard-ii-yo-valkyrie1-repair-1`
- Expected slot IDs: [`V1-GOLD-001`]
- Bundle: `germinal-valkyrie1-goldcard-ii-yo-repair-v2.tar.gz`
- Private release title: `germinal-goldcard-ii-yo-valkyrie1-repair-1`

```text
python3 goldcard_repair_tool.py validate manifest.json record.json
python3 goldcard_repair_tool.py package manifest.json record.json germinal-valkyrie1-goldcard-ii-yo-repair-v2.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-goldcard-ii-yo-valkyrie1-repair-1 germinal-valkyrie1-goldcard-ii-yo-repair-v2.tar.gz
```

Publish one safe report with output bytes, SHA-256, release IDs, and conserved counts. Then stop. Zero will validate and show the unlinked Card to the user. Do not contact Crow1.
