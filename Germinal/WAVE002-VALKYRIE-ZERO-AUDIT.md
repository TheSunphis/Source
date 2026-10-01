# GERMINAL Wave 002 Valkyrie Zero audit

## Immutable submission

- Valkyrie report commit: `cd0a6651cbb4423f24a2d62a95311b4e362277c9`
- Checkpoint bundles reconstructed through authenticated API-body transport: `10/10`
- Bundle byte and SHA-256 identities: `10/10 passed`
- Draft-release status: `10/10 passed`
- Package shape and manifest identities: `10/10 passed`
- v8 validation: `10/10 passed`
- Slot conservation: `50 = 50 submitted + 0 abstained + 0 failed`
- Candidate, Expression, and primary-form uniqueness: `50/50`
- Unauthorized external evidence locators: `0`
- Malformed editorial evidence locators: `0`

## Deterministic Full Card failure

- Displayed Japanese lines: `300`
- Lines with exactly one segment: `300`
- Segments whose surface equals the entire line: `300`
- Segments whose reading equals the entire line reading: `300`
- Segment meanings equal to whole-line meanings: `300`
- Null segment lemmas: `300`
- Null segment inflections: `300`

Every Card contains six distinct Japanese strings, but each line is wrapped as one whole-line segment rather than analysed into its meaningful lexical, grammatical, auxiliary/inflectional, and punctuation components. This does not satisfy the user requirement that every displayed Japanese line receive complete analysis with tappable segment explanations. v8 checked reconstruction and presence but did not detect whole-line pseudo-segmentation.

All Cards also use exact minimum module counts, and all 50 report `none-supported` for both patterns and distinctions. Those are not independent deterministic failures, but they require particularly careful independent review after structural correction.

## Disposition

- Zero gate: `failed`
- Crow1: `not launched`
- Accepted Expressions: `0`
- Current state: `hold pending user disposition`

The ten private bundles remain immutable audit evidence and are not accepted or review-ready.

## User disposition

The user selected the recommended one-launch targeted quality revision. Infrastructure v9 and ten replacement revision2 bundles are required before Crow activation.
