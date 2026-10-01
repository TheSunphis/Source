# GERMINAL commissioning command

## One-file worker launch

Every worker reads exactly one public instruction file:

- `Germinal/START.md`

The user supplies only the exact worker name and the instruction to read that file. Examples:

- `Your name is Valkyrie1. Read Germinal/START.md and begin.`
- `Your name is Crow1. Read Germinal/START.md and begin.`

`START.md` contains identity dispatch, launch state, safe assignment metadata, shared product context, execution rules, and both role procedures. A worker does not need to open the supporting Germinal documents.

## Active structure

- `Zero` — this original chat; coordinator, final gate, and learner-facing implementation. Zero has no directory.
- `Germinal/Valkyrie/Valkyrie1/` — creator identity directory.
- `Germinal/Crow/Crow1/` — critic identity directory.

Only Valkyrie1 and Crow1 are active worker identities. No content work begins while the matching `START.md` launch state is `HOLD`.

## Zero-maintained supporting sources

The remaining shared and role documents preserve expanded governance and product design for Zero. Workers do not need to read them separately; Zero compiles all executable requirements into `START.md` before activation.
