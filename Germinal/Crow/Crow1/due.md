# Crow1 due — substantive repair correction for all 49 Cards

- Exact agent: `Crow1`
- Assignment: `germinal-crow1-substantive-repair-49-2`
- Launch state: `ACTIVE`
- Scope: `49` Cards
- Role: reviewer and direct repairer

Your prior bundle passed structure but made zero substantive Card changes. Adding `/crowReview` metadata is not a repair. The whole batch was rejected objectively. Do not defend or re-review the prior result; perform the actual corrections now.

## Inputs

- Seed material release `401235338`, SHA-256 `ae5587937a6c1baa588ecf1ab1b3920c58857a4fe8a1aecba8747ab687864870`
- Baseline Valkyrie release `401239153`, SHA-256 `9b45fcf8be8c2f67efa823eabe478fad8613dc15d32c2ab41c8b7f3c04dd7e1e`
- Rejected Crow release `401247807`, SHA-256 `6740a587f2c0ae701bf4f13a082980566e8c8dd34aa06f6cbc7dd818f16e0ec5`
- Accepted exemplar releases `401125726` and `401210597`

## Objective defects to eliminate

All 49 retained the same generic intentions, summaries, contextual labels, follow-up labels, dialogue narration, and duplicate-primary Forms. Two retained a Response identical to the target. The two quarantines are ordinary segmentation work and must be repaired, not left aside.

Rewrite every Card’s intentions, usage/register guidance, Forms, Responses, Follow-ups, dialogue, and editorial rationales so they are natural and specific to that expression. Correct all corresponding meanings and complete segment analyses. Every Card must end candidate-complete. Preserve IDs and source anchors; keep canonical Vocabulary IDs null.

## Enforced correction gate

- Tool: `Germinal/batch49/crow_substantive_repair_gate.py`
- SHA-256: `20abfe4b3c80af4b89fc786f357b60e82938a2762cefcf0b503e513bf3e06904`
- Format: `germinal-crow-substantive-repair-49-output-v1`
- Assignment: `germinal-crow1-substantive-repair-49-2`

The gate compares your output with the private Valkyrie baseline. Per Card it requires at least six changed substantive roots, no identified boilerplate, no doubled punctuation, a genuine alternate Form, no Response equal to the target, exactly one target occurrence in dialogue, all nine post-repair gates true, and at least five distinct substantive repair pointers. It also runs the full 49-Card structural validator. Do not patch or bypass it.

Output `manifest.json` and `records.ndjson`; package `germinal-crow1-substantive-repaired-49-v2.tar.gz`; upload to private release `germinal-crow1-substantive-repair-49-2`. The safe report must give reviewed, substantively repaired, candidate-complete, quarantined, bytes, SHA-256, and release IDs. Then stop.
