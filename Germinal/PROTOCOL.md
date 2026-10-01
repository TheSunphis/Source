# GERMINAL operating protocol

## Force structure

The pilot uses seventeen chats in total:

- one main agent: `GERMINAL // ZERO COMMAND`;
- eight compiler agents: `GERMINAL // VALKYRIE SUBJECT-01` through `SUBJECT-08`;
- eight critic agents: `GERMINAL // DARK-CROW INSPECTOR-01` through `INSPECTOR-08`.

The user creates sixteen additional chats. A compiler and its matching inspector must never be the same chat.

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

## Pilot law

Eight attempted slots must resolve to eight passed-or-quarantined records. Accepted expressions remain zero. Scaling is forbidden unless the merged result is exactly 8/8 passed without weakening any gate.
