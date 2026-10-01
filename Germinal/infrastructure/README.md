# Germinal infrastructure

Zero owns this infrastructure. Worker agents do not design or modify it.

- `germinal_tool.py`: bounded resumable private-asset downloader, structural validator, and deterministic packager.
- `valkyrie-output-v1.schema.json`: machine-readable Valkyrie slot envelope.
- `crow-review-v1.schema.json`: machine-readable Crow review envelope.
- `tool-manifest.json`: immutable file identities.

The validator proves structural conditions only. It is never independent linguistic evidence. Worker `due.md` files pin an immutable commit and SHA-256 identities before activation. Version 3 retrieves private assets in verified HTTP ranges with bounded retries and resume. If Python TLS fails before a range arrives, the same signed range is retried through a pinned curl HTTP/1.1 TLS 1.2 fallback; neither transport may bypass final size and SHA-256 verification.

Version 4 adds private body-bundle retrieval through authenticated `api.github.com` draft-release metadata. This avoids the release-asset delivery host entirely while preserving private GitHub-only storage and exact per-chunk/final identity checks.

Version 5 fixes the missing base64 import in version 4. Before publication, Zero executed the exact eight-release `fetch_release_body_bundle` function against the live private draft metadata with an in-memory output sink and verified all 510,189 bytes and the final SHA-256.
