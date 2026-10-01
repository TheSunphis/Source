# Koto Expressions Full Family Card Specification

**Status:** Binding visual/product direction; implementation not started  
**Date:** 2026-09-30  
**Parent documents:** `EXPRESSIONS_FROM_SCRATCH_MASTER_PLAN.md`, `EXPRESSIONS_CORPUS_CONSTITUTION.md`

---

## 1. Terminology correction

In this project, **Family Card** means the complete opened Expressions experience—not the compact item used to browse search results.

Two surfaces exist:

1. **Library result tile** — finds and opens a family.
2. **Full Family Card** — the complete editorial, instructional, analytical, audio, state, and verification experience.

The user’s required quality reference is the previous complete Family Card. The replacement must meet or exceed that level while using entirely new corpus content and a new compiler.

The prior example is a layout and capability reference only. Its family text and annotations are not replacement seed data.

---

## 2. Non-negotiable product outcome

Every published family opens a complete Family Card containing:

1. Close control
2. Koto Difficulty
3. Category
4. VERIFIED publication state
5. Primary Japanese expression
6. Primary reading
7. Contextual English meaning
8. Japanese device-TTS Listen control
9. Full editorial usage summary
10. Mutually exclusive Recognised/Review controls
11. Family intentions
12. Use When guidance
13. Take Care guidance
14. Relationship/register guidance
15. Published forms, register, and complete sentence analysis
16. Natural responses
17. Follow-ups
18. Context dialogue
19. Reviewed patterns and examples
20. Nearby expressions and distinctions
21. Verification and sources

No compact/minimal redesign may remove these sections to improve performance.

---

## 3. Full Family Card anatomy

### 3.1 Frame

- Modal or full-height sheet appropriate to viewport
- Explicit `×` close control
- Focus trapped while open
- Escape closes when no nested analysis surface is active
- Scroll position begins at the top for a newly opened family
- Closing cancels active speech
- Background cannot receive accidental pointer or keyboard actions

### 3.2 Verification metadata

Visible header metadata:

```text
DIFFICULTY <1–5>
<CATEGORY>
VERIFIED
```

Rules:

- Use Koto Difficulty only.
- Never display Commonness.
- VERIFIED appears only after all family publication gates pass.
- Raw confidence percentages do not appear in the learner interface.
- Source and compiler details remain available in Verification and Sources.

### 3.3 Primary-expression hero

Required visual hierarchy:

1. Large Japanese expression
2. Visible kana reading
3. Complete contextual meaning
4. Explicit Listen control containing both audio symbolism and text
5. Editorial usage summary

The meaning is not limited to a dictionary gloss. It describes the conventional meaning in the family’s intended context.

TTS requirements:

- explicit user action only;
- Japanese device voice;
- prefer an installed local Japanese voice;
- no autoplay;
- cancel prior speech before starting another line;
- no downloaded recording;
- no Koto speech service.

### 3.4 Personal family state

Two complete controls:

```text
Mark Recognised
Personal library state

Mark Review
Personal marker only
```

Rules:

- mutually exclusive;
- selecting Recognised clears Review;
- selecting Review clears Recognised;
- removing the active marker returns to unmarked;
- visible labels, not colour alone;
- account-isolated;
- no interaction with Vocabulary progress, notes, schedules, or history.

The replacement namespace starts every account with no Expressions markers after the approved cutover deletion.

### 3.5 What This Family Does

- one or more concise intention statements;
- each intention begins with an action-oriented learner concept;
- intentions distinguish nearby families;
- no repetition of the English meaning merely to fill space.

### 3.6 Guidance triad

#### Use When

Concrete contexts where the expression is natural.

#### Take Care

Required to cover, where relevant:

- speaker/listener role;
- relationship risk;
- excessive directness or formality;
- literal versus conventional use;
- context where the same surface has another grammatical function;
- historical, regional, or specialized limits;
- translation traps.

#### Relationships

State suitability across relevant contexts:

- family and close relationships;
- peers;
- strangers;
- workplace hierarchy;
- school;
- service encounters;
- formal/institutional writing;
- group use.

Guidance must be evidence-backed and specific. Generic filler fails publication.

---

## 4. Forms, register, and sentence analysis

### 4.1 Published-form contract

Every displayed primary or alternate form must contain:

- form label;
- register label;
- exact Japanese;
- exact reading;
- contextual meaning;
- Japanese device-TTS control;
- complete passed sentence analysis.

**There is no learner-visible unanalysed published form.**

A family publishes only when the primary and every accepted alternate form pass the complete new analysis gate.

A candidate alternate may be omitted only when the family-boundary/evidence process concludes it is not an accepted form. It may not be silently omitted merely because analysis is difficult. A known important form with unresolved analysis quarantines the family.

Responses, follow-ups, dialogue lines, and pattern examples retain reading, meaning, and TTS but are not automatically counted as family forms. Their analysis policy may be extended later through a separate decision.

### 4.2 Form presentation

Each form block shows:

```text
<FORM / REGISTER LABEL>
<JAPANESE WITH TAPPABLE ANALYSIS SEGMENTS>
<READING>
<CONTEXTUAL MEANING>
<clear analysis interaction hint>
<Listen control>
```

Labels may describe function as well as register, for example:

- Standard
- After a pause
- More deliberate
- Casual
- Formal written
- Workplace
- Softer
- Stronger

Labels must describe an evidenced distinction rather than decorative variation.

### 4.3 Segment presentation

The replacement may use semantic colour, but colour cannot be the only signal.

Each segment must provide:

- focusable/tappable boundary;
- surface;
- reading;
- role label;
- contextual meaning;
- lemma when relevant;
- inflection when relevant;
- exact canonical Vocabulary destination when verified;
- explicit no-link explanation otherwise.

Potential visual roles:

- content/idiom;
- particle/grammar;
- auxiliary/inflection;
- punctuation.

The exact palette must adapt to every Koto theme and pass contrast review.

### 4.4 Segment explanation surface

Selecting a segment opens a nested explanation sheet containing:

1. Segment surface
2. Reading
3. Segment kind
4. Meaning used here
5. Grammatical role
6. Canonical form/lemma when applicable
7. Inflection/form when applicable
8. Review/verification identity stated truthfully
9. Exact Koto Vocabulary record link when verified
10. Explicit reason when no canonical record is linked

Closing the explanation returns focus to the selected segment.

### 4.5 Analysis publication invariants

For every displayed form:

- concatenated surfaces exactly reconstruct Japanese;
- approved reading alignment exactly reconstructs the complete reading;
- every segment has a role and contextual meaning;
- every canonical ID exists;
- written form, reading, lemma, and derivation support the selected ID;
- reverse candidate enumeration checks for omitted valid links;
- no substring-only or approximate links;
- every unlinked segment has a structured reason;
- no unresolved ambiguity remains;
- compiler and verification identities are recorded.

Any failure blocks that form and therefore blocks family publication until resolved or the candidate is validly reclassified.

---

## 5. Conversation support

### 5.1 Natural Responses

Each response contains:

- Japanese;
- reading;
- contextual English meaning;
- Listen.

Responses must be natural reactions to the family’s intended act, not arbitrary sentences containing related words.

### 5.2 Follow-ups

Each follow-up contains:

- Japanese;
- reading;
- contextual English meaning;
- Listen.

A follow-up continues the interaction naturally rather than repeating the family.

### 5.3 In Context

Dialogue requirements:

- at least two turns unless the family class formally marks dialogue inapplicable;
- speaker labels;
- Japanese;
- reading;
- contextual English meaning;
- Listen per line;
- coherent relationship and register across turns;
- target expression used naturally;
- no source sentence copied without compatible licence and attribution.

---

## 6. Expandable editorial sections

### 6.1 Reviewed Patterns and Examples

Collapsed by default to preserve navigability, not to reduce content.

On expansion:

- constrained substitution template;
- template reading;
- function/meaning;
- valid slot definition;
- invalid or risky substitution warning;
- complete examples with Japanese, reading, meaning, and TTS.

### 6.2 Nearby Expressions and Distinctions

On expansion:

- nearby family or form;
- reading;
- concise distinction;
- register/pragmatic contrast;
- when one cannot safely replace the other;
- link to the nearby family when published.

### 6.3 Verification and Sources

On expansion:

- publication status;
- source evidence classes;
- source names and permitted locators;
- corpus/compiler release identity;
- review type stated truthfully;
- analysis compiler version;
- immutable Source commit/release;
- attribution and licence route.

Do not expose model chain-of-thought, private prompts, credentials, or prohibited source text.

---

## 7. Desktop composition

Recommended structure:

- wide but bounded sheet;
- editorial header with primary expression;
- three-column guidance at wide widths;
- full-width forms;
- two-column Responses/Follow-ups;
- full-width dialogue;
- expandable patterns/comparisons/sources;
- sticky close control;
- no nested horizontal scroll.

The Family Card may be visually refined but not simplified below the required content level.

---

## 8. Mobile composition

The same sections remain; only layout changes.

- near-full-screen sheet;
- one-column flow;
- prominent Japanese retained;
- reading and complete meaning retained;
- state controls wrap into full-width accessible buttons;
- guidance triad stacks;
- each form remains complete;
- segment targets remain usable;
- TTS controls at least 44×44 CSS pixels;
- expandable sections remain available;
- nested analysis sheet remains keyboard/screen-reader navigable;
- no tiny metadata or sideways scrolling.

Mobile performance cannot justify deleting intentions, guidance, forms, responses, dialogue, patterns, comparisons, or verification.

---

## 9. Speed architecture without quality reduction

The corpus may contain 100,000 families, but only one Full Family Card is open at a time.

### Library layer

- compact search/facet indexes;
- bounded pages or virtualized result tiles;
- no rich family records embedded in the page;
- visible-state batch retrieval.

### Family Card layer

When opened:

1. fetch one family’s rich record or its small containing pack;
2. verify immutable identity and hash;
3. render the complete card;
4. fetch or reveal analysis data;
5. cache for the current session only.

### Optional lazy sections

Patterns, comparisons, and source detail may be fetched or materialized on expansion only if:

- their section heading and availability are visible immediately;
- opening remains fast;
- content is immutable and verified;
- offline/error states are honest;
- no section disappears merely for performance.

### Provisional performance targets

Measured on declared low-memory Android reference hardware:

- visible library results after required index shard: under 150 ms rendering work;
- cached Full Family Card opening: under 500 ms;
- uncached card displays a stable skeleton immediately;
- interaction-ready after one bounded detail request, excluding uncontrollable network latency;
- segment interaction after analysis load: under 100 ms;
- opening/closing repeatedly does not leak DOM nodes, speech objects, or event handlers;
- only one rich card and one nested segment sheet remain mounted.

These targets must be measured in the prototype and revised only with user approval.

---

## 10. Accessibility contract

- correct `lang="ja"` and reading language metadata;
- logical heading order;
- labelled close, Listen, state, form, and segment controls;
- visible focus;
- analysis usable without colour;
- screen-reader announcement of selected segment and sheet opening;
- Recognised/Review state through `aria-pressed` or equivalent semantics;
- reduced-motion support;
- high-contrast theme checks;
- touch targets at least 44×44 pixels;
- focus restoration after nested sheets and card close.

---

## 11. Data completeness gate for the Full Family Card

A family cannot receive VERIFIED when any required area is missing, generic, contradictory, or fabricated.

Publication checklist:

- [ ] metadata complete
- [ ] primary hero complete
- [ ] contextual summary complete
- [ ] intentions complete
- [ ] Use When complete
- [ ] Take Care complete
- [ ] Relationships complete
- [ ] every accepted form complete
- [ ] every accepted form analysis passes
- [ ] Natural Responses complete or validly inapplicable
- [ ] Follow-ups complete or validly inapplicable
- [ ] dialogue complete or validly inapplicable
- [ ] reviewed pattern complete or validly non-productive
- [ ] nearest-neighbour comparison complete
- [ ] verification/provenance complete
- [ ] Japanese device-TTS text validated
- [ ] global duplicate check passes
- [ ] register and safety gate passes

---

## 12. Acceptance criteria

The replacement Full Family Card passes only if:

1. A learner familiar with the previous card does not experience a reduction in instructional depth.
2. Every section in the required anatomy exists and contains substantive material.
3. Every published form has complete new sentence analysis.
4. Segment explanations are available by pointer, keyboard, and assistive technology.
5. Vocabulary links are exact and omission-audited.
6. Recognised/Review remain mutually exclusive and account-isolated.
7. TTS remains explicit Japanese device speech only.
8. Desktop and mobile retain complete content.
9. Performance comes from retrieval/rendering architecture, not content removal.
10. The card uses only replacement-corpus content and replacement compiler output.

---

## 13. Consequences for the industrial compiler

The factory is not producing short catalogue rows. For every publishable family it must manufacture a complete instructional product:

- rich editorial record;
- all accepted forms;
- complete analysis for every accepted form;
- conversation support;
- pattern and comparison material;
- source and verification record.

This raises per-family computational work, but it does not return to manual family-by-family production. The response is:

- parallel field compilers;
- shared deterministic morphology and canonical-link services;
- batch neighbour search;
- reusable register/safety classifiers;
- independent critique passes;
- confidence gates;
- quarantine rather than manual blocking;
- content-hash reuse for unchanged work.

The quality target is the previous Full Family Card level. The speed target comes from factory parallelism and exception-only review.
