# Automated candidate triage

This directory contains a deterministic first-pass analysis of every record in `Expressions/candidates/`. It exists to make the 5,000-record editorial queue easier to navigate without changing the immutable source candidates.

Triage scores, categories, cluster hints, and routes are **automation aids, not editorial decisions**. They do not assign Koto Difficulty, prove that a record belongs in the Expressions library, or make any candidate production-eligible. A family can become verified only through the record-level source, deduplication, Japanese, meaning, register, social-use, difficulty, substitution-safety, and final-publication gates in `review-policy.json`.

`editorialAssignment` is populated only from committed editorial-decision files. A non-null value records an existing decision; it is not inferred by the triage heuristic.

Regenerate deterministically from the candidate packs and decisions:

```bash
python3 scripts/triage_expression_candidates.py
```
