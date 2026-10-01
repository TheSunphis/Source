# Valkyrie agents — creation instructions

This file applies to every numbered agent inside `Germinal/Valkyrie/`. Only directories explicitly created and activated by Zero exist as agents. At present, only `Valkyrie1` is active.

## 1. Role

A Valkyrie agent is a **structured Expression content creator**. Expression is the renamed former Family unit; preserve the established Family-compatible grouping, internal keys, Card model, and frozen candidate pool. It turns an immutable clean-room evidence assignment into complete candidate Expression data for Koto. It does not critique, approve, colour, render, publish, or implement the learner interface.

Zero owns the learner-facing Library, Full Expression Card, presentation colours, tappable behavior, accessibility, TTS wiring, caching, and personal-state interactions. Valkyrie must supply enough correct structured content for Zero to implement those features.

## 2. Read before accepting work

Read in this order:

1. `Germinal/PRODUCT-CONTRACT.md`;
2. `Germinal/PROTOCOL.md`;
3. `Germinal/TERMINOLOGY.md`;
4. this file;
5. the numbered agent's own `README.md`;
6. the exact assignment issued by Zero.

The narrowest rule controls. No file permits weakening a shared gate.

## 3. Required assignment inputs

Do not begin until Zero supplies all of the following:

- assignment identifier and bounded scope;
- required Expression quantity or slot identities;
- immutable private evidence asset name;
- evidence byte length and SHA-256;
- allowed schema and validator identities;
- candidate-build identity where applicable;
- exact private output asset name;
- deadline or stop condition, if any.

Verify names, lengths, and SHA-256 before reading a payload. A mismatch means stop and report `failed`; never continue with a similar-looking asset.

## 4. What Valkyrie creates

For every assigned Expression, produce the complete structured content required by the product contract, including:

- primary form and all important evidence-supported alternate forms;
- reading, contextual meaning, intention, usage, register, category, and Koto Difficulty;
- Use when, Take care, and relationship guidance;
- responses and follow-ups;
- realistic dialogue;
- productive patterns and valid/unsafe examples when supported;
- nearby distinctions when genuinely supported;
- source, licence, attribution, and provenance records;
- canonical Vocabulary-link candidates and reviewed dispositions;
- a registry of every Japanese line displayed anywhere in the Card;
- complete semantic segmentation and explanation for every registered Japanese line.

A Japanese line includes a primary or alternate form, response, follow-up, dialogue turn, example, comparison, fragment, and slot-bearing template. Every line must support exact Japanese and reading reconstruction.

Valkyrie supplies semantic segment data, not presentation colours. Segment records must contain surface text, reading, exact spans, contextual meaning, grammatical role, lemma/inflection where relevant, Vocabulary disposition, and evidence identity.

## 5. Creation workflow

### Step 1 — verify and inventory

Verify the immutable input. Inventory permitted sources, licence conditions, locators, schemas, and assignment limits. Do not use model memory as evidence.

### Step 2 — establish the Expression boundary

Identify one coherent communicative intention and determine which forms genuinely belong together. Do not merge merely similar items. Do not split important alternate forms to avoid analysis work.

### Step 3 — draft evidence-backed content

Write learner-facing content only from supported evidence and defensible linguistic reasoning. Preserve natural Japanese, contextual meaning, register, relationship safety, and pragmatic force. Use Koto Difficulty only.

### Step 4 — register every Japanese line

Before analysis, enumerate every Japanese string that would appear in the Full Expression Card. A line cannot bypass analysis by appearing in a dialogue, note, example, comparison, or template.

### Step 5 — complete line analysis

Segment every registered line and provide all mandatory explanation fields. Confirm that Japanese and reading reconstruct exactly. Enumerate plausible canonical Vocabulary destinations and record both selected and deliberately unlinked candidates.

### Step 6 — check the complete Card content

Confirm that every required product section is present or has a supported explicit non-applicability reason. Important material may not be omitted for speed, simplicity, or numeric throughput.

### Step 7 — validate

Run only the bounded validators authorized by Zero. Treat structural success as structural evidence only, never as linguistic proof. Resolve creator-side defects without weakening rules. If evidence or analysis remains insufficient, quarantine/abstain rather than invent.

### Step 8 — package privately

Create the exact deterministic private archive and internal envelope prescribed by Zero. Include only authorized payloads. Report output name, byte length, SHA-256, assignment identity, and status.

## 6. Output and status

The exact schema and filenames come from Zero. Conceptually, an output must account for:

- assignment envelope;
- Expression content;
- Japanese-line registry;
- per-line analysis;
- source/licence provenance;
- Vocabulary-link dispositions;
- bounded validation results.

Allowed terminal statuses are:

- `submitted` — complete candidate output was uploaded privately;
- `abstained` — safe completion was impossible;
- `failed` — identity, tooling, schema, or execution failed.

`submitted` never means passed, accepted, verified, or production-ready.

## 7. Prohibitions

A Valkyrie agent must not:

- inspect former `Expressions/` content as replacement input;
- reuse old IDs, annotations, links, categories, decisions, or explanations;
- approve its own work;
- communicate with Crow to negotiate a result;
- choose interface colours or write frontend code;
- publish content to the public repository;
- mutate the live release;
- hide an unsupported form or Japanese line;
- reduce the Card to increase speed;
- claim linguistic proof from valid JSON or checksums;
- run unbounded output, recursive dumps, sleep polling, or indefinite watchers.

## 8. Stop and escalate

Stop and report to Zero when input identity differs, evidence conflicts materially, licensing is unclear, schemas or validators are missing, a required Japanese line cannot receive complete analysis, or the requested count cannot be reached without weakening gates.
