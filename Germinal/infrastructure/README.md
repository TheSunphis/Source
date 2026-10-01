# Germinal infrastructure

Zero owns this infrastructure. Worker agents do not design or modify it.

- `germinal_tool.py`: bounded resumable private-asset downloader, structural validator, and deterministic packager.
- `valkyrie-output-v1.schema.json`: machine-readable Valkyrie slot envelope.
- `crow-review-v1.schema.json`: machine-readable Crow review envelope.
- `tool-manifest.json`: immutable file identities.

The validator proves structural conditions only. It is never independent linguistic evidence. Worker `due.md` files pin an immutable commit and SHA-256 identities before activation. Version 2 retrieves large private assets in verified 4 MiB HTTP ranges with bounded per-range retries, so an unexpected EOF resumes from the last complete range.
