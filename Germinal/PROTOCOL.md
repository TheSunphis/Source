# GERMINAL operating protocol

## Force structure

The active operation uses three chats:

- `Zero` — main coordinator;
- `Valkyrie1` — creator;
- `Crow1` — independent critic.

Valkyrie1 and Crow1 must be separate chats. Additional numbered directories require explicit user approval.

## Universal worker bootstrap

The user directs every worker to `Germinal/START.md` and supplies only the exact agent name. START locks identity, retrieves and verifies the mapped immutable `due.md`, checks launch state, verifies Zero's material and infrastructure, runs the tool self-test, and then starts or safely blocks the assignment. Zero supplies and tests the material, schemas, validator, deterministic packager, private storage destination, permissions, and report template. Missing or broken infrastructure is Zero's failure; workers stop rather than inventing replacements. Zero owns learner-facing and coloured-interaction implementation; Valkyrie owns structured content creation; Crow owns independent content critique. No role may take over another role or weaken the contract.

## Information boundaries

- Workers may use only their immutable clean-room task packet, the current schemas, the source registry, and these instructions.
- Workers must not inspect `Expressions/`, former expression JSON, former decisions, former annotations, or former IDs.
- Model memory is not source authority.
- Important attested forms may not be silently omitted. If complete analysis cannot be supplied for every displayed form, abstain or quarantine the slot.
- Personal state, live routes, and current runtime data are out of scope.

## Storage boundary

Source is public. Never commit or expose:

- restricted evidence;
- candidate payloads;
- agent prompts or responses containing evidence;
- expression or analysis payloads;
- critic reports containing retained evidence;
- raw Vocabulary snapshots.

Private payloads go only to the unpublished draft release under the asset name issued by ZERO COMMAND. Public Git data may contain only instructions, schemas, hashes, counts, and non-sensitive status metadata.

## Terminal discipline — mandatory

- Address exact files and API endpoints.
- No `grep -R`, broad recursive dumps, or `find` without an exact root and depth bound.
- No `cat` of large JSON, archives, model logs, or candidate stores.
- Cap diagnostic output at 200 lines and 50 KiB.
- Put a timeout on every external command. Default maximum: 120 seconds.
- Asset transfer may use a separately declared bounded timeout; show start, byte count, digest, and completion.
- Never use `sleep` loops or opaque watchers. Use one bounded wait with a named success/failure condition.
- Stop on the first unexpected identity, digest, schema, or permission mismatch.

## Status vocabulary

Workers may report only:

- `submitted` — required private artifact uploaded and digest reported;
- `abstained` — evidence was insufficient;
- `failed` — infrastructure, identity, or validation failure.

Only ZERO COMMAND may derive `passed-pilot-gates` after deterministic merge validation. No agent may call its own work accepted, verified, or production ready.

## Staged production law

Wave 001 is closed at 50 attempted, 0 submitted, and 50 abstained. Wave 002 uses ten gated checkpoints of five proposals from the same frozen candidate pool. For each checkpoint, Valkyrie must conserve five slot outcomes, Crow independently reviews all submitted proposals, and Zero closes deterministic gates before the next checkpoint opens. Accepted Expressions remain zero until canonical Vocabulary resolution and every final gate pass.
