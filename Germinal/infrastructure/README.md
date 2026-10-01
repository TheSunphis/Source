# Germinal infrastructure

Zero owns this infrastructure. Worker agents do not design or modify it.

- `germinal_tool.py`: bounded resumable private-asset downloader, structural validator, and deterministic packager.
- `valkyrie-output-v1.schema.json`: machine-readable Valkyrie slot envelope.
- `crow-review-v1.schema.json`: machine-readable Crow review envelope.
- `tool-manifest.json`: immutable file identities.

The validator proves structural conditions only. It is never independent linguistic evidence. Worker `due.md` files pin an immutable commit and SHA-256 identities before activation. Version 3 retrieves private assets in verified HTTP ranges with bounded retries and resume. If Python TLS fails before a range arrives, the same signed range is retried through a pinned curl HTTP/1.1 TLS 1.2 fallback; neither transport may bypass final size and SHA-256 verification.
