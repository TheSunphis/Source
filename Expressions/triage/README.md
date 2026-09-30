# Automated candidate triage

This directory contains a deterministic first-pass analysis of every record in `Expressions/candidates/`. It exists to make the 5,000-record editorial queue easier to navigate without changing the immutable source candidates.

Triage scores, categories, cluster hints, and routes are **automation aids, not editorial decisions**. They do not assign Koto Difficulty, prove that a record belongs in the Expressions library, or make any candidate production-eligible. A family can become verified only through the record-level source, deduplication, Japanese, meaning, register, social-use, difficulty, substitution-safety, and final-publication gates in `review-policy.json`.

`editorialAssignment` is populated only from committed candidate-to-family decisions. `editorialDisposition` points to a committed decision or standalone outcome explaining why a reviewed candidate was not assigned. Neither field is inferred by the triage heuristic, and a candidate cannot have both.

All 77 records on `priority-family-review` now have a committed editorial result: 74 assignments and three non-assignment dispositions. Unreviewed work remains on the standard, specialist, and low-priority routes.

Regenerate deterministically from the candidate packs, decisions, and outcomes:

```bash
python3 scripts/triage_expression_candidates.py
```
