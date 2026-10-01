# GERMINAL commissioning command

## One-file due system

Each worker reads exactly one self-contained file in its own directory:

- Valkyrie1: `Germinal/Valkyrie/Valkyrie1/due.md`
- Crow1: `Germinal/Crow/Crow1/due.md`

Launch prompts:

- `Your name is Valkyrie1. Read Germinal/Valkyrie/Valkyrie1/due.md and do the work.`
- After Zero activates Crow1's due: `Your name is Crow1. Read Germinal/Crow/Crow1/due.md and do the work.`

Each `due.md` contains all instructions, safe input identities, the bounded assignment, private output contract, and public reporting rules. Workers do not need another Germinal instruction file.

## Reports

Each agent updates `report.md` in the same numbered directory. Public reports contain safe status metadata only. Detailed Expressions, analyses, evidence, and critic findings remain private draft-release assets.

## Current state

- `Valkyrie1`: active; assigned 50 attempted Expression slots.
- `Crow1`: waiting for Valkyrie1's immutable output identity; assigned to review all 50 afterward.
- `Zero`: this original chat; coordinator, final gate, and learner-facing implementation. Zero has no directory.

Supporting Germinal documents are maintained by Zero as expanded design/governance sources; workers execute only their own `due.md`.
