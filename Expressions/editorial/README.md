# Editorial records

Editorial decision files preserve how source candidates are accepted, rejected, split, or merged into reusable expression families. Candidate source records remain immutable; decisions and reviewed-family or production-pack records carry the evolving editorial judgment.

Final learner publication requires a separate Japanese-language proficiency pass. The reviewer may be human or AI editorial, but reviewer type must be disclosed and AI sign-off must be source-backed and record-specific rather than inferred from automated extraction.

- `decisions/` records candidate-to-family assignments and related candidates explicitly not merged into a family.
- `outcomes/` records standalone, record-specific reasons why reviewed candidates were deferred or excluded instead of assigned.
- `batches/` records distinct source-editorial and final-language passes for multi-family publication batches.

Automated priority routing is complete only when every record on that route has either a committed family assignment or an explicit editorial disposition. A disposition does not verify or publish a candidate.
