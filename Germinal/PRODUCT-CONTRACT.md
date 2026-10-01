# Koto Expressions product and commissioning contract

This is the authoritative shared product context for Zero, Valkyrie agents, and Crow agents. Every agent must read it before opening an assignment. Role files may add restrictions but may not weaken this document.

**Responsibility boundary:** Zero alone owns the learner-facing implementation, including Library and Card rendering, colour assignment, tappable behavior, accessibility, device TTS wiring, caching, and personal-state behavior. Valkyrie supplies structured Expression content and semantic segment explanations. Crow independently critiques that content and analysis. Valkyrie and Crow do not design, colour, render, or implement the user interface.

## 1. Status and safety boundary

- Work is private/shadow commissioning only.
- The current live Expressions release remains operational until an explicit approved cutover.
- No agent may mutate live `Expressions/`, publish a release, replace routes, delete progress, scrub backups, or create a package.
- `productionReady` remains false and accepted count remains zero until Zero derives a valid result.
- Former Expressions content is structural and functional reference only. It is prohibited as replacement-corpus truth or editorial input.
- Restricted evidence, candidate payloads, prompts/responses, Expressions, analyses, and critic payloads must not be committed to this public repository. Durable private payloads belong only in the unpublished draft release.

## 2. Product terminology

- **Expressions**: the complete feature/library.
- **Expression**: one commissioned learner-facing item that may contain a primary form and supported alternate forms.
- **Form**: a primary or alternate Japanese realization belonging to an Expression.
- **Library Result Tile**: the compact selectable result in the Library. It is not the Card.
- **Full Expression Card**: the complete opened Expression sheet.
- **Japanese line**: any Japanese text displayed in the Card, including fragments, responses, dialogue turns, examples, and comparison items.
- **Analysis**: exact colour-linked segment explanation for one Japanese line.
- **Pack**: 25 accepted Expressions.

Some existing technical schemas may retain legacy key names. Agents must follow required JSON keys exactly while using the terminology above in instructions, reports, and learner-facing text.

## 3. Expressions Library contract

The Library must preserve the established rich product level. This is a **Zero implementation responsibility**. Valkyrie supplies the validated content consumed by the Library, and Crow audits that content; neither worker builds the Library.

### 3.1 Header and summary

Show:

- Expressions hero/header;
- verified Source state;
- dynamic Expression total;
- dynamic searchable-form total;
- Recognised, Review, and Unseen progress;
- safe release/source identity.

Totals must be derived from validated data rather than handwritten display constants.

### 3.2 Search

One intention-oriented search must cover:

- Japanese;
- kana reading;
- contextual meaning;
- communicative intention;
- usage and context;
- supported alternate forms.

### 3.3 Controls

Preserve:

- Koto Difficulty 1–5;
- Category;
- Personal status;
- Sort;
- Reset;
- visible result summary.

Never use Commonness, JLPT, CEFR, or JF grading. On mobile, Category selection must behave like a native Android full-height radio-list selector, not a cramped dropdown.

### 3.4 Library Result Tile

Each rich tile must show enough information to choose intelligently:

- primary Japanese Expression;
- reading;
- contextual meaning;
- intention or communicative purpose;
- usage/context summary;
- Koto Difficulty;
- Category;
- verified Source state;
- supported-form count;
- Recognised/Review state;
- clear action to open the Full Expression Card.

## 4. Full Expression Card sequence

The opened Card must retain this information density and order. Zero owns Card composition, rendering, interaction, and learner-facing behavior. Valkyrie supplies the required structured content, and Crow audits its completeness and correctness.

### 4.1 Hero

- primary Japanese form;
- reading;
- contextual meaning;
- concise usage summary;
- Koto Difficulty;
- Category;
- verified state;
- explicit device Japanese TTS control.

### 4.2 Personal state

Recognised and Review controls are mutually exclusive. Personal state is never stored in remote Source content.

### 4.3 Intentions

Explain what the speaker is trying to accomplish and distinguish nearby intentions where needed.

### 4.4 Use when

Give concrete situations where the Expression is appropriate.

### 4.5 Take care

Explain register warnings, social risk, face-threatening force, situations to avoid, and likely learner misinterpretations.

### 4.6 Relationships

Give explicit guidance for relevant contexts such as family/close relationships, peers, strangers, workplace hierarchy, school, service encounters, formal institutions, writing, and group use.

### 4.7 Forms and register

For every important evidence-supported primary or alternate form provide:

- form identity and kind;
- register and label;
- Japanese;
- reading;
- contextual meaning;
- explicit device TTS when fully speakable;
- evidence;
- complete analysis reference.

An important supported form must not be silently omitted. If it cannot receive complete analysis, quarantine the entire Expression.

### 4.8 Coloured tappable explanations

Every Japanese line displayed anywhere on the Card must have complete passed analysis. Section 5 defines the universal interaction.

### 4.9 Responses

Provide natural responses with context, Japanese, reading, meaning, complete analysis, and device TTS.

### 4.10 Follow-ups

Provide natural continuation lines with context, Japanese, reading, meaning, complete analysis, and device TTS.

### 4.11 Dialogue

Provide a realistic exchange with situation, relationship, register, speakers, Japanese, reading, meaning, device TTS, complete analysis for every turn, and exact identification of the target Expression.

### 4.12 Patterns and examples

Only show genuinely productive patterns. Provide template, template reading, function, slot constraints, valid examples, invalid/unsafe substitutions, risk warnings, and complete speakable examples. If no safe productive pattern exists, say so rather than inventing one.

### 4.13 Nearby distinctions

Compare a genuinely nearby Expression with Japanese, reading, pragmatic difference, register contrast, and unsafe-replacement guidance. Link to another published Expression only when it actually exists.

### 4.14 Verification and sources

Show evidence-backed verification state, source locators, licence/attribution route, compiler/reviewer identity, review date, analysis compiler version, and provenance identity. Never display unsupported “verified” claims.

## 5. Universal coloured tappable analysis

Zero alone implements the coloured tappable interface. Valkyrie must provide complete structured segmentation and explanations for every Japanese line so Zero can render it; Crow must audit those segments and explanations. Valkyrie and Crow must not choose presentation colours or produce frontend code.

The Zero-rendered interaction applies to **all Japanese displayed on the Full Expression Card**, including:

- hero and primary form;
- every alternate form;
- every response;
- every follow-up;
- every dialogue turn;
- every pattern and substitution example;
- nearby comparison Expressions;
- any other Japanese instructional example;
- pattern templates, with slot-aware explanation.

### 5.1 Segment completeness

Every line must reconstruct exactly from its segments. Each segment records:

- surface text;
- reading;
- exact Japanese and reading spans;
- contextual meaning;
- grammatical role;
- lemma where applicable;
- inflection where applicable;
- canonical Vocabulary destination when safe;
- explicit unlinked reason when no safe destination exists;
- evidence and review identity.

Japanese reconstruction, reading reconstruction, segment completeness, canonical validity, reverse omission, and ambiguity handling must all pass.

### 5.2 Colour and interaction

Zero derives presentation colours from validated segment data and owns all behavior in this subsection. Colours are presentation metadata, not linguistic claims supplied by Valkyrie.

- Render Japanese as stable colour-coded segments.
- Every segment is tappable and keyboard-focusable.
- Selecting a segment emphasizes both the text segment and its matching explanation panel.
- The explanation panel uses the same colour and exposes all segment fields.
- Punctuation receives neutral treatment where appropriate.
- Switching forms or lines loads that line's complete colour-matched analysis.
- Repeated identical lines may reuse one validated analysis by content-addressed reference.
- Tapping analysis never triggers audio automatically.

### 5.3 Accessibility

Colour is never the only signal. Also provide:

- segment numbering or labels;
- strong visible selected state;
- keyboard focus styling;
- screen-reader text and relationships;
- sufficient contrast;
- comfortable mobile tap targets;
- wrapping that does not overlap or break Japanese text.

### 5.4 TTS

Use device Japanese TTS only and only after explicit user action. Fully speakable Japanese lines receive TTS. Templates containing placeholders are not sent to TTS, but their components and slots still receive tappable explanations.

### 5.5 Hard failure rule

If any displayed Japanese line lacks complete passed coloured analysis, quarantine the entire Expression. Never omit the line, hide an important form, or substitute plain unanalysed text.

## 6. Evidence and Vocabulary-link contract

- Model memory is not source authority.
- Every source-derived claim must retain approved evidence and stable locators.
- Perform global deduplication before acceptance.
- Enumerate all canonical Vocabulary candidates for every linkable segment.
- Audit links bidirectionally: selected destinations and omitted plausible destinations.
- A link must be safe and exact; otherwise retain an explicit reviewed unlinked disposition.
- Sudachi or another tokenizer may support segmentation but is not attestation authority.

## 7. Agent review separation

### Valkyrie

Creates evidence-backed Expression proposals, including complete structured Japanese lines, readings, semantic segments, explanations, and all content required by the Library and Card. Valkyrie supplies data only: it does not assign colours, design screens, render Cards, write frontend code, or implement learner interactions. Valkyrie cannot approve its own output and reports only `submitted`, `abstained`, or `failed`.

### Crow

Independently audits the Expression content, Japanese lines, readings, semantic segmentation, explanations, evidence, and payload completeness without repairing. Crow does not select colours, design screens, render Cards, write frontend code, or judge implementation that Zero has not yet produced. Every finding needs severity, stable code, JSON pointer, evidence locator, and concise explanation. A pass requires every assigned content check to pass and zero findings.

### Zero

Derives the result after deterministic validation. Worker confidence and worker-written gate booleans are not proof. Zero supplies and freezes the source material, evidence packets, schemas, validators, packaging tools, report templates, private output destinations, permissions, immutable identities, and all infrastructure required by workers. Zero tests and pins that infrastructure before activation and owns infrastructure failures; Valkyrie and Crow must never improvise missing tools. Zero enforces count conservation, global deduplication, payload identity, and all contracts. Zero alone transforms accepted structured content into the learner-facing product and implements the Library, Full Expression Card, colour mapping, tappable explanation panels, accessibility, device TTS controls, responsive behavior, session caching, and Recognised/Review interactions.

## 8. Privacy and runtime behavior

- Remote Expressions data uses session-only caching.
- Personal Recognised/Review state stays in Koto's account data and is never published in Source.
- Recognised and Review remain mutually exclusive.
- No recorded audio is stored.
- No private evidence or generated payload may leak through logs, public branches, issues, or pull requests.

## 9. Prohibited shortcuts

- No reduction of Library or Card content for speed.
- No plain-text fallback for missing analysis.
- No important-form omission.
- No inferred verification from valid JSON, checksums, or self-declared booleans.
- No recursive repository dumps, unbounded grep, unbounded stdout, opaque sleep loops, or indefinite watchers.
- No lowering gates to reach a numeric target.
- No legacy IDs, annotations, links, categories, explanations, decisions, or content as replacement input.

## 10. Acceptance law

A proposal may become an accepted Expression only after all evidence, schema, semantic, analysis, reconstruction, Vocabulary-link, deduplication, review, and display-contract gates pass. Failed or incomplete proposals are quarantined. Exact release counts are formed only from fully passed Expressions.
