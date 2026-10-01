# Crow1 due — corrected evidence-matrix review

- Exact agent: `Crow1`
- Assignment: `germinal-goldcard-ii-yo-crow1-correction-1`
- Launch state: `HOLD_COMPLETED_ZERO_REJECTED`
- Expected reviews: `1`
- Exact slot: `V1-GOLD-001`
- Role: independent critic; do not repair
- Public report: `Germinal/Crow/Crow1/report.md`

Crow1 submitted the bounded corrected review. Zero rejected its pass because the line and sense rationales remained templated aggregate assurances rather than substantive independent scrutiny. Do not relaunch until the user decides final disposition.

## Immutable inputs

Original evidence dossier:
- Release `401068873`; bytes `2311`
- SHA-256 `26f5ade563e9f4eca8a1afd1a106c74215961090067e6d48685611a218e0095d`

User-approved clarified proposal:
- Release `401107799`; bytes `6088`
- SHA-256 `eaeeb56978d573e10b8273d764b753106ed05d2ac0d037275df00d1c2e7b7cc7`

Repaired canonical Vocabulary:
- Release `401125715`; bundle `koto-vocabulary-goldcard-link-repair-v1.tar.gz`; bytes `9775`
- SHA-256 `495bdef4db1cc04855e9bfb8ef841dc12fc6165da8c0e40e6308441cf814b855`
- Build `vocabularybuild1:db44e2051a42d45da44d98f2f4757611`; records `37`

Recompiled Card:
- Release `401125726`; bundle `germinal-goldcard-ii-yo-compiled-link-repair-v1.tar.gz`; bytes `8245`
- Bundle SHA-256 `db070cb3e5d7c6b37c54f57881bc67cf33b27c15381075d7b5049476335a6d2d`
- Card SHA-256 `c6f672adfd478cce9df7b6edb4d2d59cd0ad18465196f4f01ae828659f6dc8ce`
- Linked `28`; exact lemma alignments `28`; punctuation exclusions `4`

Rejected prior review, defect comparison only:
- Release `401117372`; bytes `3248`
- SHA-256 `8402af17f9ead0254aadff9038a7f45ebfc7bcaa9a9b4d6eea380da70e431d95`

Verify and reconstruct every private body bundle before review.

## Infrastructure

- Upload core `germinal_tool.py`, commit `5eccc8e4c768bce21ff00398cb172f97617d3f24`, SHA-256 `d55a1d94555ba1a0ad75cd43489380a5c51ede3b2c04a727f1c747c277a9e985`
- Review tool `gold_crow_correction_tool.py`, commit `428368cc148a5948a174c8cd2b001c5cbe746779`, SHA-256 `8557198a43c600e663613ad145d0b3a783077c2f97e1d7092603ad72a008f593`
- Schema SHA-256 `d016e5493cda36426c6e196624e42ed11b7c8cadf8dad2950dffdee5563642dc`

Run every self-test. Do not patch infrastructure.

## Required corrected review

The private review must include:

- all sixteen issue-specific checks with substantive rationales and at least two concrete release/source locators each;
- seven separate line audits covering naturalness, reading, meaning, and analysis completeness;
- twenty-eight ordered link audits covering exact form/reading, exact canonical lemma alignment, and sense fit;
- four exact punctuation exclusions;
- an explicit `applicable: false` decision for the support-verb policy because no instance occurs in this Card;
- three separate evidence classes: lexical anchors, bounded expression anchors, and editorial teaching content that is not source attestation.

Concrete locators must identify actual release payload paths or source entries. Critic-authored labels are invalid. Do not repeat the prior aggregate assertions. Inspect each line and link. If any substantive gate fails, recommend quarantine; do not repair.

## Output

- Manifest format: `germinal-goldcard-crow-correction-v3`
- Assignment: `germinal-goldcard-ii-yo-crow1-correction-1`
- Expected slot IDs: [`V1-GOLD-001`]
- Bundle: `germinal-crow1-goldcard-ii-yo-correction-v3.tar.gz`
- Private release title: `germinal-goldcard-ii-yo-crow1-correction-1`

```text
python3 gold_crow_correction_tool.py validate manifest.json review.json
python3 gold_crow_correction_tool.py package manifest.json review.json germinal-crow1-goldcard-ii-yo-correction-v3.tar.gz
python3 germinal_tool.py upload-release-body-bundle TheSunphis Source germinal-goldcard-ii-yo-crow1-correction-1 germinal-crow1-goldcard-ii-yo-correction-v3.tar.gz
```

Publish one safe report with exact START and due commits, recommendation counts, output release/bytes/SHA-256, and conserved counts. Then stop. Never place findings or restricted content in Git.
