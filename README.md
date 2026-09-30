# Source

Public, versioned source datasets used by [Koto](https://github.com/TheSunphis/Sunphis).

## Datasets

- [`Expressions/`](Expressions/) — reusable Japanese expression families, their searchable forms, editorial guidance, provenance, and review metadata.

This repository is deliberately data-only. It contains no account records, recognition state, review markers, notes, schedules, credentials, or other personal information.

## Publication model

Production datasets are published as immutable GitHub Releases. A consuming Koto release must pin the dataset release and verify the SHA-256 values declared in its manifest before loading any pack. The default branch may advance, but applications must never treat an unpinned branch snapshot as trusted production data.

The Expressions production manifest still has zero verified families. A reproducible first-pass audit of the 30 September 2026 JMdict snapshot produced 5,000 explicitly non-production source candidates. The first source-backed editorial family review is complete for `よろしくお願いします`, but independent human Japanese-language sign-off is still required before it can enter a production pack.

## Licence

Repository-authored data and documentation are offered under CC BY-SA 4.0 unless a file's provenance states otherwise. Third-party material retains its original licence and must satisfy the per-record attribution requirements described in the dataset source registry.
