#!/usr/bin/env python3
"""Validate Koto Source manifests, expression records, counts, and hashes."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
EXPRESSIONS = ROOT / "Expressions"
SCHEMAS = EXPRESSIONS / "schema"


def load_json(path: Path):
    opener = gzip.open if path.suffix == ".gz" else path.open
    with opener("rt", encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validator(name: str) -> Draft202012Validator:
    schema_path = SCHEMAS / name
    schema = load_json(schema_path)
    resources = []
    for path in SCHEMAS.glob("*.schema.json"):
        item = load_json(path)
        resources.append((item["$id"], Resource.from_contents(item)))
        resources.append((path.name, Resource.from_contents(item)))
    registry = Registry().with_resources(resources)
    return Draft202012Validator(schema, registry=registry)


def validate_or_raise(checker: Draft202012Validator, payload, label: str) -> None:
    errors = sorted(checker.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        details = "\n".join(f"- {label} {list(error.path)}: {error.message}" for error in errors)
        raise SystemExit(f"Schema validation failed:\n{details}")


def main() -> None:
    json_paths = sorted(ROOT.rglob("*.json"))
    for path in json_paths:
        load_json(path)

    manifest = load_json(EXPRESSIONS / "manifest.json")
    validate_or_raise(validator("manifest.schema.json"), manifest, "manifest")

    family_validator = validator("expression-family.schema.json")
    for path in sorted((EXPRESSIONS / "examples").glob("*.json")):
        validate_or_raise(family_validator, load_json(path), str(path.relative_to(ROOT)))

    pack_validator = validator("pack.schema.json")
    total = 0
    difficulty_counts = {str(level): 0 for level in range(1, 6)}
    identifiers: set[str] = set()
    for item in manifest["packs"]:
        path = EXPRESSIONS / item["file"]
        if not path.is_file():
            raise SystemExit(f"Missing pack: {item['file']}")
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise SystemExit(f"Integrity mismatch: {item['file']}")
        pack = load_json(path)
        validate_or_raise(pack_validator, pack, item["id"])
        if pack["packId"] != item["id"] or pack["familyCount"] != item["familyCount"]:
            raise SystemExit(f"Pack metadata mismatch: {item['id']}")
        if pack["familyCount"] != len(pack["families"]):
            raise SystemExit(f"Pack count mismatch: {item['id']}")
        for family in pack["families"]:
            if family["id"] in identifiers:
                raise SystemExit(f"Duplicate family id: {family['id']}")
            identifiers.add(family["id"])
            difficulty_counts[str(family["difficulty"])] += 1
            if family["publicationStatus"] != "verified":
                raise SystemExit(f"Production pack contains an unverified family: {family['id']}")
        total += pack["familyCount"]

    if total != manifest["familyCount"]:
        raise SystemExit("Manifest familyCount does not equal the sum of pack counts.")
    if difficulty_counts != manifest["difficultyCounts"]:
        raise SystemExit("Manifest difficultyCounts do not equal production pack contents.")
    if manifest["productionReady"] != (manifest["publicationStatus"] == "production" and total > 0):
        raise SystemExit("Manifest productionReady is inconsistent with its status and count.")
    if manifest["searchIndex"] is not None:
        item = manifest["searchIndex"]
        path = EXPRESSIONS / item["file"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise SystemExit("Search-index integrity mismatch.")

    candidate_total = 0
    candidate_manifest_path = EXPRESSIONS / "candidates" / "manifest.json"
    if candidate_manifest_path.is_file():
        candidate_manifest = load_json(candidate_manifest_path)
        validate_or_raise(validator("candidate-manifest.schema.json"), candidate_manifest, "candidate manifest")
        candidate_pack_validator = validator("candidate-pack.schema.json")
        candidate_ids: set[str] = set()
        source_sequences: set[int] = set()
        for item in candidate_manifest["packs"]:
            path = candidate_manifest_path.parent / item["file"]
            if not path.is_file():
                raise SystemExit(f"Missing candidate pack: {item['file']}")
            if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
                raise SystemExit(f"Candidate integrity mismatch: {item['file']}")
            pack = load_json(path)
            validate_or_raise(candidate_pack_validator, pack, item["id"])
            if pack["packId"] != item["id"] or pack["candidateCount"] != item["candidateCount"]:
                raise SystemExit(f"Candidate pack metadata mismatch: {item['id']}")
            if pack["candidateCount"] != len(pack["candidates"]):
                raise SystemExit(f"Candidate pack count mismatch: {item['id']}")
            for candidate in pack["candidates"]:
                if candidate["candidateId"] in candidate_ids:
                    raise SystemExit(f"Duplicate candidate id: {candidate['candidateId']}")
                if candidate["sourceSequence"] in source_sequences:
                    raise SystemExit(f"Duplicate JMdict source sequence: {candidate['sourceSequence']}")
                candidate_ids.add(candidate["candidateId"])
                source_sequences.add(candidate["sourceSequence"])
            candidate_total += pack["candidateCount"]
        if candidate_total != candidate_manifest["candidateCount"]:
            raise SystemExit("Candidate manifest count does not equal the sum of pack counts.")
        if candidate_total != candidate_manifest["audit"]["shortlistedCount"]:
            raise SystemExit("Candidate shortlist count is inconsistent with its audit.")

    print(
        f"Validated {len(json_paths)} JSON files, {total} production expression families, "
        f"and {candidate_total} non-production candidates."
    )


if __name__ == "__main__":
    main()
