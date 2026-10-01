# Koto Expressions Library Specification

**Status:** Binding visual/product direction; implementation not started  
**Date:** 2026-09-30  
**Related:** `EXPRESSIONS_FAMILY_CARD_SPEC.md`, `EXPRESSIONS_CORPUS_CONSTITUTION.md`, `EXPRESSIONS_FROM_SCRATCH_MASTER_PLAN.md`

---

## 1. Purpose and terminology

The **Library** is the complete searchable Expressions catalogue surface.

It is separate from:

- the **Library Result Tile**, which summarizes one family in results; and
- the **Full Family Card**, which opens the complete instructional experience.

The user requires the replacement Library to preserve the previous product level and interaction model shown in the supplied reference. The old family text and records are not replacement seed data.

---

## 2. Binding learner journey

1. Enter Expressions from Extra.
2. See the verified-corpus identity and personal progress.
3. Understand that the Library finds communicative intention, not only spelling.
4. Search Japanese, reading, meaning, intention, or context.
5. Filter by Difficulty, Category, and Personal status.
6. Sort the verified result set.
7. Scan complete high-quality Library Result Tiles.
8. Mark Recognised or Review directly from a result.
9. Open a Full Family Card.
10. Tap analyzed segments in any published primary/alternate form.

This journey remains recognizable at 10,000–100,000 families.

---

## 3. Page structure

Required order:

1. Expressions navigation/header
2. Hero
3. Verified Source status
4. Personal progress panel
5. Library introduction
6. Search control
7. Filter controls
8. Result/verification summary
9. Loading, error, empty, or result list
10. Source/privacy/audio method section
11. Full Family Card surface
12. Nested segment-explanation surface
13. Status toast/live announcements

---

## 4. Header

Required:

- Koto brand
- Expressions Library identity
- route back to Extra
- Library anchor
- Method/source anchor
- active-theme control where globally supported
- account menu

On mobile:

- preserve Koto identity;
- avoid crowding the viewport;
- hide secondary anchors before removing core account/navigation actions;
- retain accessible labels.

---

## 5. Hero contract

The hero communicates the module’s purpose at the previous editorial level.

Required content concepts:

```text
EXTRA · <VERIFIED FAMILY COUNT> · DIFFICULTY 1–5

Say more than words.
Choose the expression that fits.
```

Required explanation:

- complete current verified-family count;
- all five Koto Difficulty levels;
- primary and alternate forms;
- fixed, verified sentence analysis for every published form;
- learner can tap content, idiom, particle, grammar, or auxiliary segments for explanation.

Required actions:

- browse verified families;
- explicit Japanese device-TTS demonstration.

Required source state:

- pinned Source identity after verification;
- whether the verified data was downloaded or reused from current-tab session cache;
- honest failure state when verification does not pass.

### Dynamic counts

Legacy text such as `260 families` and `429 forms` becomes release-derived data:

```text
<familyCount> verified families
<formCount> published analyzed forms
```

Counts may never be hard-coded independently from the verified manifest.

---

## 6. Personal progress panel

Required statistics:

- Recognised count / complete current family count
- Review-marker count
- published analyzed-form count
- percentage recognised

Rules:

- percentage denominator is the current replacement family count;
- Recognised and Review remain mutually exclusive;
- old progress is zeroed at approved cutover;
- all counts are account-isolated;
- remote Source content never contains personal state;
- count changes announce to assistive technology without moving focus.

The visual treatment may use a progress ring or equivalent treatment at least equal to the previous quality.

---

## 7. Library introduction

Required heading concept:

```text
Find an intention,
not just a spelling.
```

Required explanatory concepts:

- all verified families in the active release are searchable;
- search covers Japanese, reading, meaning, intention, and usage/context;
- opening a family provides complete form analysis;
- every displayed primary/alternate form has passed the analysis gate.

At 100,000 families, “available immediately” means searchable and retrievable from the verified release. It does not mean all rich family records are downloaded or rendered at startup.

---

## 8. Search control

Visible label:

```text
Search Japanese, reading, meaning, intention, or context
```

Example placeholder may combine Japanese and English concepts but cannot copy an old family merely as replacement content authority.

Search requirements:

- Japanese surface forms;
- kana readings;
- normalized kana/width;
- contextual English meaning;
- intentions;
- usage summary;
- category and approved aliases;
- register/context terms;
- case-insensitive English;
- slash keyboard shortcut when focus is not already in an input or modal;
- query retained in URL where safe;
- clear/reset behaviour;
- no search-history leakage across accounts.

Search ranking must prioritize:

1. exact Japanese form;
2. exact reading;
3. normalized exact form;
4. exact/phrase intention or meaning;
5. prefix form/reading;
6. contextual/alias match;
7. fuzzy assistance only when clearly bounded.

No popularity/Commonness field is displayed or used as Koto Difficulty.

---

## 9. Filter controls

Required controls and initial values:

### Difficulty

```text
All Difficulty levels
1 · Essential
2 · Foundational
3 · Intermediate
4 · Advanced
5 · Nuanced
```

### Category

```text
All categories
<dynamic categories from verified release>
```

### Personal status

```text
All expressions
Unmarked
Recognised
Review marker
```

### Sort

```text
Difficulty
Japanese reading
English meaning
```

### Reset

- restores all default values;
- clears query;
- updates results and URL;
- returns focus appropriately;
- does not change personal family state.

---

## 10. Native mobile selector requirement

The supplied screenshot establishes the desired Category interaction on Android:

- system-native full-height selection surface;
- large category rows;
- one selected radio indicator;
- current category visibly marked;
- scrollable long list;
- `All categories` first;
- no cramped custom dropdown;
- theme-compatible system presentation.

**Recommended implementation:** retain semantic native `<select>` controls unless measured platform behaviour requires an accessible equivalent. Native selection provides the screenshot’s system picker, keyboard support, touch sizing, and assistive-technology integration with minimal JavaScript.

Category names come from the new verified corpus taxonomy. Old names may reappear only when independently generated and evidenced in the new corpus—not because they were copied from the former dataset.

---

## 11. Filter semantics

Filters combine with logical AND:

```text
query
AND Difficulty
AND Category
AND Personal status
```

Within the query, matching across indexed fields may use weighted OR.

Requirements:

- result count always reflects the complete filtered verified corpus;
- category counts may be provided but cannot require downloading rich records;
- status filtering uses authenticated personal state;
- filter changes are debounced only where necessary;
- browser Back/Forward restores filter state;
- invalid URL filter values fall back safely to defaults;
- changing filters never destroys personal state.

---

## 12. Result and verification summary

Required information:

```text
<resultCount> families · <active scope>
Every displayed family passed all publication gates.
```

The number of publication gates must come from the replacement constitution/audit manifest. Do not retain an old numeric claim if the new gate count differs.

Summary examples:

- all verified families;
- matching a query;
- Difficulty 3;
- a selected category;
- Recognised;
- multiple active constraints.

The summary uses a live region without announcing every keystroke excessively.

---

## 13. Library Result Tile contract

The result tile remains at least equal to the previous visual/informational level.

Required anatomy:

1. Difficulty tile (`D1`–`D5`)
2. Category
3. Primary Japanese
4. Visible primary reading
5. Complete contextual English meaning
6. One or more intentions, separated clearly
7. Recognised control (`✓` plus accessible label)
8. Review control (`R` plus accessible label)
9. `Open family →`

Conceptual layout:

```text
┌────────────────────────────────────────────────────────────┐
│ [D2]  <CATEGORY>                                  [✓] [R] │
│       <PRIMARY JAPANESE>                                  │
│       <READING>                                           │
│                                                          │
│       <CONTEXTUAL MEANING>                                │
│                                                          │
│       <INTENTION> · <INTENTION>                           │
│                                                          │
│       Open family →                                      │
└────────────────────────────────────────────────────────────┘
```

Rules:

- Japanese remains visually dominant;
- reading is never hidden;
- meaning is contextual, not merely a dictionary gloss;
- intentions explain what the family does;
- no raw confidence score;
- no Commonness;
- state buttons are independent from Open;
- tile hover/focus does not cause layout shift;
- full tile remains keyboard navigable;
- visual state is not communicated by colour alone.

The tile is not the Full Family Card. Opening it invokes the complete contract in `EXPRESSIONS_FAMILY_CARD_SPEC.md`.

---

## 14. Result layout

### Desktop

- high-quality two-column grid where width supports it;
- one column when content would become cramped;
- consistent card rhythm without forcing equal text truncation that removes meaning;
- bounded page/virtual window.

### Mobile

- one complete tile per row;
- Japanese, reading, meaning, and intentions retained;
- state controls remain at least 44×44 CSS pixels;
- no sideways scrolling;
- Open remains explicit;
- no compact-table substitution.

---

## 15. Result-scale architecture

The corpus may contain 100,000 families. The DOM may not.

Required:

- verified compact summary/index shards;
- bounded result windows;
- pagination or carefully accessible virtualization;
- stable result ordering;
- keyed tile reuse without stale personal state;
- family rich record fetched only on Open;
- complete result count derived from index/query response;
- no giant client-side 100,000-record rich payload;
- no persistent remote-corpus storage.

### Recommended result window

Prototype both:

- 48-result accessible pagination; and
- virtualized continuous results with explicit position/count announcements.

**Recommended initial choice:** 48-result pagination, because it is predictable for keyboard, assistive technology, URL restoration, memory, and debugging. Virtualization may be adopted only if it preserves accessibility and state correctness.

---

## 16. Loading state

Required:

- clear message that the manifest/index is being verified;
- no unverified family flashes before integrity passes;
- stable skeletons only after layout is known;
- search and filters disabled or honestly marked until usable;
- progress panel never fabricates counts.

At scale, index shards may become progressively available, but the UI must state scope accurately.

---

## 17. Error state

Required:

- bounded explanation;
- Retry verification action;
- no loss of Recognised/Review state;
- no fallback to unverified content;
- no stale release silently mixed with a new manifest;
- distinguish authentication, network, integrity, and unavailable-shard failures where actionable.

If one detail pack fails, the verified Library remains usable and the family can be retried.

---

## 18. Empty state

Required:

- state that no verified families match;
- suggest broadening search or resetting filters;
- Reset action remains available;
- do not imply the corpus itself is empty unless it truly is.

---

## 19. Full Family Card opening

On `Open family →`:

1. preserve Library query/filter/sort/position;
2. retrieve the exact verified rich family record;
3. retrieve/verify its complete published-form analyses;
4. render the Full Family Card;
5. focus its heading or close control according to accessible-dialog practice;
6. allow nested segment explanation;
7. on close, restore focus and Library position.

Opening a family may update URL state for shareable/back-button behaviour without exposing personal state.

---

## 20. Recognised and Review from Library

- mutually exclusive;
- authenticated API only;
- optimistic visual update only with safe rollback on failure;
- controls disabled while that family update is pending;
- update progress panel and visible tile;
- status filter reacts consistently;
- other accounts unaffected;
- no Vocabulary state write;
- no analysis/content mutation.

At final new-corpus cutover, legacy Expressions progress is deleted as separately approved. New state begins clean.

---

## 21. Source verification and privacy

The Library exposes only content from the active immutable replacement release.

Required verification:

- dataset identity;
- release version;
- immutable commit/tag identity;
- manifest hash/bytes;
- index shard hash/bytes;
- family/detail pack hash/bytes;
- family/form totals;
- Difficulty/category totals;
- publication status and gate manifest.

Privacy:

- verified corpus text is session-only;
- personal state remains authenticated/local Koto account data;
- queries are not written into public Source;
- remote corpus data and personal state never share one payload;
- TTS stays on the device.

---

## 22. Performance contract

Performance must not reduce Library Result Tile or Full Family Card content.

Provisional targets on declared low-memory Android reference hardware:

- Library shell useful without rich-family download;
- native filters interactive promptly after index readiness;
- filter/result window render under 150 ms after required data is local;
- query input remains responsive during shard retrieval;
- 48 complete tiles remain within measured memory budget;
- cached Full Family Card open under 500 ms;
- no 100,000-family DOM or rich-record array;
- no repeated event-listener or speech-object leaks;
- state update round trip never blocks unrelated tiles.

The 1,000- and 10,000-family prototypes must measure these targets on mobile before cutover approval.

---

## 23. Accessibility contract

- visible labels for every search/filter control;
- semantic native select where possible;
- correct Japanese language metadata;
- logical heading order;
- slash shortcut does not steal focus from controls or dialogs;
- Difficulty/category/status conveyed in text;
- state conveyed beyond colour;
- minimum 44×44 touch controls;
- visible focus;
- result count live region with restrained announcements;
- pagination/virtualization exposes position and total;
- focus restoration after Full Family Card close;
- reduced motion;
- theme contrast verification.

---

## 24. Replacement count language

Before cutover, current runtime may still say 260/429 because it serves the temporary legacy release.

The replacement uses verified dynamic language:

```text
EXTRA · <familyCount> VERIFIED FAMILIES · DIFFICULTY 1–5
Browse the <familyCount> families
Recognised <recognisedCount> / <familyCount>
Review markers <reviewCount>
Sentence breakdowns <formCount>
<resultCount> families · <scope>
```

The label `Sentence breakdowns` is valid for the replacement only because every published primary/alternate form is required to have complete passed analysis.

---

## 25. Acceptance criteria

The replacement Library passes only if:

1. It preserves the reference page’s hierarchy and editorial quality.
2. Hero, progress, search, filters, result summary, tiles, method, and card opening are all present.
3. Category uses the native mobile selector experience or an approved accessible equivalent.
4. Search covers Japanese, reading, meaning, intention, and context.
5. Difficulty, Category, Personal status, Sort, and Reset behave correctly together.
6. Every displayed family is verified.
7. Every Result Tile contains Difficulty, category, Japanese, reading, contextual meaning, intentions, state, and Open.
8. Every opened Full Family Card satisfies `EXPRESSIONS_FAMILY_CARD_SPEC.md`.
9. Every published primary/alternate form has complete tappable sentence analysis.
10. Scale is achieved without rendering/downloading all rich families at startup.
11. Personal state is isolated and mutually exclusive.
12. Device Japanese TTS is explicit and local.
13. Desktop and mobile retain the same instructional content.
14. Old family content is not imported into the replacement corpus.

---

## 26. Consequence for planning

The factory must output both:

1. a compact, verified Library summary/index record for every family; and
2. the complete rich family/analysis product opened from that summary.

The new system is not permitted to meet 100,000-family scale by replacing the Library with a plain database table, a thin autocomplete list, or minimal cards.
