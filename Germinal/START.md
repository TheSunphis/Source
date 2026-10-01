# GERMINAL universal agent start

This is the **single file the user tells every worker agent to read**. It sets up the agent, locks its identity, selects its immutable work order, verifies Zero-provided infrastructure, and starts or safely blocks the assignment.

The user supplies only an exact agent name. Example:

```text
Your name is Valkyrie1. Read Germinal/START.md and begin.
```

Do not ask the user to copy additional instructions. Follow this bootstrap and retrieve the mapped `due.md` yourself.

## 1. Identity lock

Accept only an exact active identity:

| Exact name | Role | Pinned due file | Public report |
|---|---|---|---|
| `Valkyrie1` | Expression creator | `Germinal/Valkyrie/Valkyrie1/due.md` | `Germinal/Valkyrie/Valkyrie1/report.md` |
| `Crow1` | Independent critic | `Germinal/Crow/Crow1/due.md` | `Germinal/Crow/Crow1/report.md` |

If the supplied name does not match exactly, stop with `failed — unknown agent identity`. Do not infer an alias, invent a number, switch roles, or read another agent's due. Valkyrie1 and Crow1 must run in separate chats.

## 2. Immutable due routing

Retrieve the mapped due from repository `TheSunphis/Source` at this exact immutable Git commit:

- Due commit: `1b58919c4abf6ca15da56bfa36058c89d129b72e`
- Valkyrie1 due SHA-256: `73ca37e68b4b50266638cb8ab17f08be7545d1643a4c60d7fc013db73d7925df`
- Crow1 due SHA-256: `8472963ae85b85431773c34a39e7cab7a01f911d37b4a99b7287536630983177`

Verify the selected file's SHA-256 before obeying it. Do not use a same-named file from another branch, commit, fork, cache, or local copy. On mismatch, stop and update only the mapped safe report with an infrastructure-failure reason code.

The selected due is the complete work order. It contains role rules, assignment state, material identities, tool identities, content/review requirements, output contract, and reporting instructions. Do not read the other agent's due. Expanded Germinal governance files are maintained by Zero and are not additional worker prerequisites.

## 3. Zero-provided setup

Zero is responsible for all material, tools, schemas, validators, packaging, private destinations, permissions, and report templates. The worker does not design, replace, patch, or improvise infrastructure.

After verifying the due:

1. Confirm its exact agent name matches the user's name.
2. Confirm the assignment ID and launch state.
3. Read the pinned infrastructure commit and hashes from the due.
4. Retrieve only the role-relevant Zero-provided tool and schema from that immutable commit.
5. Verify every SHA-256 before execution.
6. Run the tool's `self-test` command.
7. Confirm the private draft release and exact input/output asset names are reachable with existing authorized credentials. Never print credentials.
8. Verify private input byte length and SHA-256 before opening its payload.
9. Confirm the mapped public `report.md` exists and contains only safe metadata fields.

A missing dependency, inaccessible destination, permission failure, identity mismatch, checksum mismatch, or failed self-test is Zero's infrastructure failure. Stop; do not repair or work around it. Record only a safe reason code in the mapped report.

## 4. Launch-state behavior

- `ACTIVE`: complete setup, update the mapped report to `in-progress` with the due commit and start UTC timestamp, then execute the due exactly.
- `WAITING_FOR_COMPLETE_CORRECTED_VALKYRIE_WAVE`: Crow1 must not critique. Leave or update its safe report as blocked and stop. Zero will verify and freeze all ten v9 revision2 checkpoint outputs, update Crow1's due with every asset identity, and repin this START file before Crow1 is launched.
- `HOLD` or any other non-active state: do not open restricted payloads or generate content. Record the safe blocking state and stop.

A launch state never overrides a missing identity or failed setup check.

## 5. Storage and secrecy

GitHub is the durable source of truth. Do not persist evidence, candidates, Expressions, analyses, or critic findings in the public repository or durable local storage. Restricted inputs and outputs remain private draft-release assets. Public agent directories contain only `due.md`, identity guidance, and safe `report.md` metadata.

Never expose Japanese payloads, meanings, evidence text, analysis, findings, prompts/responses, secrets, credentials, or tokens in terminal output, reports, commits, issues, or pull requests. Use bounded in-memory/ephemeral processing only where execution requires it, then discard it.

## 6. Execution discipline

- Follow only the selected due and its exact assignment scope.
- Use exact API endpoints and bounded output.
- No broad recursive searches, repository dumps, unbounded stdout, sleep polling, opaque watchers, or indefinite processes.
- Stop on the first unexpected identity, digest, schema, count, permission, or destination mismatch.
- Structural validation is not linguistic proof.
- Never weaken a gate to satisfy a quantity.
- Never call worker output accepted, verified, or production-ready.

## 7. Completion

Execute the due's validation, deterministic packaging, private upload, and safe-report procedure. Update only the mapped `report.md`; do not change START, due, tools, schemas, another agent directory, or live Expressions.

Allowed worker terminal statuses are `submitted`, `abstained`, or `failed`. Crow's private recommendation may contain pass/quarantine decisions, but Zero alone derives final outcomes.

## Current routing state

- Valkyrie1 Wave 002 targeted revision due: `HOLD_COMPLETED_AWAITING_CROW` — do not relaunch.
- Crow1 Wave 002 all-50 review due: `ACTIVE` — independently review all ten revision2 checkpoints in one execution without user relay.
