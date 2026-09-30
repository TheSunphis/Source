#!/usr/bin/env python3
"""Validate Expressions2 schemas, registry, fixtures, and semantic invariants."""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schema"
FIXTURES = ROOT / "fixtures" / "contracts"
REGISTRY_FILE = ROOT / "source-registry" / "sources.json"
SNAPSHOT_DIR = ROOT / "snapshots"
EVIDENCE_DIR = ROOT / "evidence"


class DuplicateKey(ValueError):
    pass


def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=no_duplicate_keys)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def build_registry(schemas: dict[str, dict]) -> Registry:
    registry = Registry()
    for schema in schemas.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry


def json_pointer(error) -> str:
    return "/" + "/".join(str(part) for part in error.absolute_path)


def schema_errors(instance: Any, schema: dict, registry: Registry) -> list[str]:
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    return [f"{json_pointer(e)}: {e.message}" for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))]


def invariant_errors(name: str, value: Any) -> list[str]:
    errors: list[str] = []
    if name == "source-registry":
        source_ids = [item["sourceId"] for item in value["sources"]]
        if len(source_ids) != len(set(source_ids)):
            errors.append("sourceId values must be unique")
        for item in value["sources"]:
            if item["approvalStatus"] == "approved-for-snapshot" and not item["acquisitionUrl"]:
                errors.append(f"{item['sourceId']} is approved but has no acquisitionUrl")
            if item["snapshot"] and item["snapshot"]["sha256"] == "0" * 64:
                errors.append(f"{item['sourceId']} has a placeholder snapshot hash")
            policy = item["networkPolicy"]
            acquisition_host = urlparse(item["acquisitionUrl"]).hostname if item["acquisitionUrl"] else None
            if acquisition_host and acquisition_host not in policy["allowedHosts"]:
                errors.append(f"{item['sourceId']} acquisition host is absent from allowedHosts")
            if policy["expectedBytes"] is not None and policy["expectedBytes"] > policy["maxBytes"]:
                errors.append(f"{item['sourceId']} expectedBytes exceeds maxBytes")

    elif name == "snapshot-manifest":
        if value["rawRetention"] == "temporary-deleted" and value["rawFile"] is not None:
            errors.append("temporary-deleted snapshots must not claim a persisted rawFile")
        if value["rawRetention"] == "persisted-private" and value["rawFile"] is None:
            errors.append("persisted-private snapshots must identify rawFile")
        final_url = urlparse(value["finalUrl"])
        if final_url.query or final_url.fragment or final_url.username or final_url.password:
            errors.append("finalUrl must be sanitized to endpoint identity without query, fragment, or user-info")

    elif name == "evidence-build-manifest":
        artifacts = value["artifacts"]
        source_ids = [item["sourceId"] for item in artifacts]
        files = [item["file"] for item in artifacts]
        if len(source_ids) != len(set(source_ids)) or len(files) != len(set(files)):
            errors.append("evidence artifact source IDs and files must be unique")
        expected = {
            "sources": len(artifacts),
            "records": sum(item["recordCount"] for item in artifacts),
            "canonicalBytes": sum(item["canonicalBytes"] for item in artifacts),
            "compressedBytes": sum(item["compressedBytes"] for item in artifacts),
        }
        if value["totals"] != expected:
            errors.append("evidence totals must be derived from artifacts")
        if source_ids != sorted(source_ids):
            errors.append("evidence artifacts must use stable sourceId ordering")

    elif name == "form-analysis":
        segments = value["segments"]
        if "".join(segment["surface"] for segment in segments) != value["japanese"]:
            errors.append("segment surfaces do not reconstruct japanese")
        if "".join(segment["reading"] for segment in segments) != value["reading"]:
            errors.append("segment readings do not reconstruct reading")
        expected_japanese_start = 0
        expected_reading_start = 0
        segment_ids: list[str] = []
        for segment in segments:
            segment_ids.append(segment["segmentId"])
            js = segment["japaneseSpan"]
            rs = segment["readingSpan"]
            if js["start"] != expected_japanese_start or value["japanese"][js["start"]:js["end"]] != segment["surface"]:
                errors.append(f"{segment['segmentId']} has an invalid Japanese span")
            if rs["start"] != expected_reading_start or value["reading"][rs["start"]:rs["end"]] != segment["reading"]:
                errors.append(f"{segment['segmentId']} has an invalid reading span")
            if js["end"] <= js["start"] or rs["end"] <= rs["start"]:
                errors.append(f"{segment['segmentId']} has a non-positive span")
            expected_japanese_start = js["end"]
            expected_reading_start = rs["end"]
        if expected_japanese_start != len(value["japanese"]):
            errors.append("Japanese spans do not cover the full form")
        if expected_reading_start != len(value["reading"]):
            errors.append("reading spans do not cover the full reading")
        if len(segment_ids) != len(set(segment_ids)):
            errors.append("segmentId values must be unique")
        enumerations = {item["segmentId"]: item for item in value["vocabularyEnumeration"]}
        if set(enumerations) != set(segment_ids) or len(enumerations) != len(value["vocabularyEnumeration"]):
            errors.append("vocabulary enumeration must contain exactly one item per segment")
        for segment in segments:
            enumeration = enumerations.get(segment["segmentId"])
            if not enumeration:
                continue
            disposition = segment["vocabularyDisposition"]
            selected = enumeration["selectedId"]
            if disposition["status"] == "linked":
                if selected != disposition["vocabularyId"] or selected not in enumeration["candidateIds"]:
                    errors.append(f"{segment['segmentId']} linked ID is inconsistent with enumeration")
            elif selected is not None:
                errors.append(f"{segment['segmentId']} is unlinked but enumeration selects a record")

    elif name == "family":
        forms = value["forms"]
        form_ids = [item["formId"] for item in forms]
        if len(form_ids) != len(set(form_ids)):
            errors.append("formId values must be unique")
        primaries = [item for item in forms if item["kind"] == "primary"]
        if len(primaries) != 1:
            errors.append("family must contain exactly one primary form")
        else:
            primary = primaries[0]
            hero = value["hero"]
            library = value["library"]
            for key in ("japanese", "reading", "contextualMeaning"):
                if hero[key] != primary[key]:
                    errors.append(f"hero.{key} does not match the primary form")
                if library[key] != hero[key]:
                    errors.append(f"library.{key} does not match hero.{key}")
            if hero["primaryFormId"] != primary["formId"]:
                errors.append("hero.primaryFormId does not identify the primary form")
        if value["library"]["formCount"] != len(forms):
            errors.append("library.formCount is not dynamic from forms")
        labels = {1: "Essential", 2: "Foundational", 3: "Intermediate", 4: "Advanced", 5: "Nuanced"}
        if labels[value["difficulty"]["level"]] != value["difficulty"]["label"]:
            errors.append("difficulty label does not match Koto Difficulty level")
        if value["dialogue"]["applicable"] and not any(turn["containsTarget"] for turn in value["dialogue"]["turns"]):
            errors.append("applicable dialogue does not identify a target-expression turn")
        analysis_refs = [item["analysisRef"] for item in forms]
        if len(analysis_refs) != len(set(analysis_refs)):
            errors.append("each published form must have its own analysisRef")

    elif name == "family-ledger":
        events = value["events"]
        for index, event in enumerate(events):
            if event["sequence"] != index + 1:
                errors.append("ledger sequence must be contiguous from 1")
            expected = None if index == 0 else digest(events[index - 1])
            if event["previousEventHash"] != expected:
                errors.append(f"ledger event {index + 1} has an invalid previousEventHash")
        ids = [item["eventId"] for item in events]
        if len(ids) != len(set(ids)):
            errors.append("ledger eventId values must be unique")

    elif name == "compiler-manifest":
        classes = value["coverage"]["classCounts"]
        difficulties = value["coverage"]["difficultyCounts"]
        accepted = value["counts"]["acceptedFamilies"]
        if sum(classes.values()) != accepted:
            errors.append("class coverage counts do not sum to acceptedFamilies")
        if sum(difficulties.values()) != accepted:
            errors.append("Difficulty coverage counts do not sum to acceptedFamilies")
        artifacts = value["artifacts"]
        paths = [item["path"] for item in artifacts]
        if len(paths) != len(set(paths)):
            errors.append("artifact paths must be unique")
        if sum(item["kind"] == "family-pack" for item in artifacts) != 4:
            errors.append("Batch 001 must contain four family packs")
        if sum(item["kind"] == "analysis-pack" for item in artifacts) != 4:
            errors.append("Batch 001 must contain four analysis packs")

    elif name == "audit-manifest":
        ids = [item["familyId"] for item in value["families"]]
        if len(ids) != len(set(ids)):
            errors.append("all 100 audited family IDs must be unique")
        if len(value["families"]) != value["summary"]["auditedFamilies"]:
            errors.append("audit summary count does not match family audit records")

    elif name == "runtime-library-index":
        entries = value["entries"]
        ids = [item["familyId"] for item in entries]
        slugs = [item["slug"] for item in entries]
        if len(ids) != len(set(ids)) or len(slugs) != len(set(slugs)):
            errors.append("runtime family IDs and slugs must be unique")
        if value["familyCount"] != len(entries):
            errors.append("familyCount must be derived from runtime entries")
        if value["formCount"] != sum(item["formCount"] for item in entries):
            errors.append("formCount must be derived from runtime entries")
        actual_categories = Counter(item["category"]["key"] for item in entries)
        declared_categories = {item["key"]: item["count"] for item in value["categories"]}
        if dict(actual_categories) != declared_categories:
            errors.append("category counts must be derived from runtime entries")
        packs = Counter(item["pack"] for item in entries)
        if set(packs.values()) != {25} or len(packs) != 4:
            errors.append("runtime index must map exactly 25 families to each of four packs")

    elif name == "runtime-family-card":
        family = value["family"]
        analyses = value["analyses"]
        analysis_by_id = {item["analysisId"]: item for item in analyses}
        if len(analysis_by_id) != len(analyses):
            errors.append("runtime analyses IDs must be unique")
        form_refs = {item["analysisRef"] for item in family["forms"]}
        if set(analysis_by_id) != form_refs:
            errors.append("runtime card must resolve exactly one analysis for every published form")
        for form in family["forms"]:
            analysis = analysis_by_id.get(form["analysisRef"])
            if not analysis:
                continue
            for key in ("familyId", "formId", "japanese", "reading"):
                expected = family["familyId"] if key == "familyId" else form[key]
                if analysis[key] != expected:
                    errors.append(f"analysis {analysis['analysisId']} has mismatched {key}")
            errors.extend(f"analysis {analysis['analysisId']}: {item}" for item in invariant_errors("form-analysis", analysis))
        errors.extend(f"family: {item}" for item in invariant_errors("family", family))

    return errors


def main() -> int:
    failures: list[str] = []
    schemas: dict[str, dict] = {}
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        try:
            schema = load_json(path)
            Draft202012Validator.check_schema(schema)
            schemas[path.stem.removesuffix(".schema")] = schema
        except Exception as exc:
            failures.append(f"schema {path.name}: {exc}")
    registry = build_registry(schemas)

    positive_count = 0
    negative_count = 0
    for path in sorted((FIXTURES / "positive").glob("*.valid.json")):
        name = path.name.removesuffix(".valid.json")
        if name not in schemas:
            failures.append(f"positive fixture has no schema: {path}")
            continue
        try:
            value = load_json(path)
            errors = schema_errors(value, schemas[name], registry)
            errors.extend(invariant_errors(name, value))
            if errors:
                failures.extend(f"positive {path.name}: {error}" for error in errors)
            positive_count += 1
        except Exception as exc:
            failures.append(f"positive {path.name}: {exc}")

    for path in sorted((FIXTURES / "negative").glob("*.invalid.json")):
        name = path.name.removesuffix(".invalid.json")
        if name not in schemas:
            failures.append(f"negative fixture has no schema: {path}")
            continue
        try:
            value = load_json(path)
            errors = schema_errors(value, schemas[name], registry)
            if not errors:
                failures.append(f"negative {path.name}: unexpectedly passed")
            negative_count += 1
        except Exception as exc:
            failures.append(f"negative {path.name}: fixture could not be read: {exc}")

    snapshot_count = 0
    evidence_count = 0
    evidence_mode = os.environ.get("EXPRESSIONS2_EVIDENCE_MODE", "full")
    if evidence_mode not in {"full", "metadata-only"}:
        failures.append(f"invalid EXPRESSIONS2_EVIDENCE_MODE: {evidence_mode}")
    try:
        source_registry = load_json(REGISTRY_FILE)
        for error in schema_errors(source_registry, schemas["source-registry"], registry):
            failures.append(f"registry sources.json: {error}")
        for error in invariant_errors("source-registry", source_registry):
            failures.append(f"registry sources.json: {error}")

        sources_by_id = {source["sourceId"]: source for source in source_registry["sources"]}
        manifests_by_id: dict[str, dict] = {}
        for path in sorted((SNAPSHOT_DIR / "manifests").glob("*.snapshot.json")):
            manifest = load_json(path)
            snapshot_count += 1
            for error in schema_errors(manifest, schemas["snapshot-manifest"], registry):
                failures.append(f"snapshot {path.name}: {error}")
            for error in invariant_errors("snapshot-manifest", manifest):
                failures.append(f"snapshot {path.name}: {error}")
            source_id = manifest.get("sourceId")
            if source_id in manifests_by_id:
                failures.append(f"snapshot {path.name}: duplicate manifest for {source_id}")
            manifests_by_id[source_id] = manifest
            source = sources_by_id.get(source_id)
            if not source:
                failures.append(f"snapshot {path.name}: source is absent from registry")
                continue
            if source["approvalStatus"] != "approved":
                failures.append(f"snapshot {path.name}: source is not in approved state")
            expected_snapshot = source.get("snapshot")
            if not expected_snapshot:
                failures.append(f"snapshot {path.name}: registry has no pinned snapshot")
            else:
                comparisons = {
                    "retrievedAt": manifest["retrievedAt"], "byteLength": manifest["bytes"],
                    "sha256": manifest["sha256"], "mediaType": manifest["mediaType"],
                }
                for key, actual in comparisons.items():
                    if expected_snapshot.get(key) != actual:
                        failures.append(f"snapshot {path.name}: registry {key} mismatch")
            if manifest["acquisitionUrl"] != source["acquisitionUrl"] or manifest["canonicalUrl"] != source["canonicalUrl"]:
                failures.append(f"snapshot {path.name}: source URLs do not match registry")
            if manifest["allowedRoles"] != source["roles"]:
                failures.append(f"snapshot {path.name}: allowedRoles do not match registry")
            final_host = urlparse(manifest["finalUrl"]).hostname
            if final_host not in source["networkPolicy"]["allowedHosts"]:
                failures.append(f"snapshot {path.name}: final URL host is not approved")
            if source["networkPolicy"]["expectedBytes"] != manifest["bytes"] or source["networkPolicy"]["expectedSha256"] != manifest["sha256"]:
                failures.append(f"snapshot {path.name}: pinned network identity does not match manifest")
            notice_path = SNAPSHOT_DIR / manifest["license"]["noticeFile"]
            if not notice_path.is_file():
                failures.append(f"snapshot {path.name}: licence notice is missing")
            elif hashlib.sha256(notice_path.read_bytes()).hexdigest() != manifest["license"]["noticeSha256"]:
                failures.append(f"snapshot {path.name}: licence notice hash mismatch")

        for source_id, source in sources_by_id.items():
            if source["approvalStatus"] == "approved" and source_id not in manifests_by_id:
                failures.append(f"registry sources.json: approved source {source_id} has no snapshot manifest")
            if source["approvalStatus"] != "approved" and source_id in manifests_by_id:
                failures.append(f"registry sources.json: unapproved source {source_id} has a snapshot manifest")

        evidence_manifest_path = EVIDENCE_DIR / "manifest.json"
        if evidence_manifest_path.is_file():
            evidence_manifest = load_json(evidence_manifest_path)
            for error in schema_errors(evidence_manifest, schemas["evidence-build-manifest"], registry):
                failures.append(f"evidence manifest: {error}")
            for error in invariant_errors("evidence-build-manifest", evidence_manifest):
                failures.append(f"evidence manifest: {error}")
            body = {key: value for key, value in evidence_manifest.items() if key not in {"schemaVersion", "buildId"}}
            expected_build_id = "evidencebuild2:" + digest(body)[:32]
            if evidence_manifest["buildId"] != expected_build_id:
                failures.append("evidence manifest: buildId is not derived from canonical manifest body")
            expected_epoch = max(source["snapshot"]["retrievedAt"] for source in sources_by_id.values())
            if evidence_manifest["sourceDateEpoch"] != expected_epoch:
                failures.append("evidence manifest: sourceDateEpoch does not match pinned snapshots")
            declared_files = set()
            for artifact in evidence_manifest["artifacts"]:
                evidence_count += 1
                declared_files.add(artifact["file"])
                source = sources_by_id.get(artifact["sourceId"])
                path = EVIDENCE_DIR / artifact["file"]
                if not source:
                    failures.append(f"evidence {artifact['file']}: unknown sourceId")
                    continue
                if artifact["snapshotSha256"] != source["snapshot"]["sha256"]:
                    failures.append(f"evidence {artifact['file']}: snapshot is not current registry pin")
                if artifact["permissionClass"] != source["permissionClass"]:
                    failures.append(f"evidence {artifact['file']}: permission class mismatch")
                if evidence_mode == "metadata-only":
                    continue
                if not path.is_file():
                    failures.append(f"evidence {artifact['file']}: artifact is missing")
                    continue
                compressed = path.read_bytes()
                if len(compressed) != artifact["compressedBytes"] or hashlib.sha256(compressed).hexdigest() != artifact["compressedSha256"]:
                    failures.append(f"evidence {artifact['file']}: compressed identity mismatch")
                    continue
                if len(compressed) < 10 or int.from_bytes(compressed[4:8], "little") != 0:
                    failures.append(f"evidence {artifact['file']}: gzip mtime is not deterministic zero")
                canonical = gzip.decompress(compressed)
                if len(canonical) != artifact["canonicalBytes"] or hashlib.sha256(canonical).hexdigest() != artifact["canonicalSha256"]:
                    failures.append(f"evidence {artifact['file']}: canonical identity mismatch")
                    continue
                store = json.loads(canonical, object_pairs_hook=no_duplicate_keys)
                if canonical != canonical_bytes(store):
                    failures.append(f"evidence {artifact['file']}: payload is not canonical JSON")
                for error in schema_errors(store, schemas["source-evidence"], registry):
                    failures.append(f"evidence {artifact['file']}: {error}")
                if store["sourceId"] != artifact["sourceId"] or store["snapshotSha256"] != artifact["snapshotSha256"]:
                    failures.append(f"evidence {artifact['file']}: source/snapshot identity mismatch")
                records = store["records"]
                if len(records) != artifact["recordCount"]:
                    failures.append(f"evidence {artifact['file']}: record count mismatch")
                locators = [item["locator"] for item in records]
                ids = [item["evidenceId"] for item in records]
                if locators != sorted(locators) or len(locators) != len(set(locators)) or len(ids) != len(set(ids)):
                    failures.append(f"evidence {artifact['file']}: records are not uniquely and stably ordered")
                for item in records:
                    if item["permissionClass"] != source["permissionClass"]:
                        failures.append(f"evidence {artifact['file']}: record permission mismatch")
                        break
                    compact_keys = {re.sub(r"[^a-z0-9]", "", key.lower()) for key in item["fields"]}
                    if compact_keys & {"legacyid", "oldid", "familyid", "candidateid"}:
                        failures.append(f"evidence {artifact['file']}: prohibited lineage key")
                        break
                    if artifact["sourceId"] == "source2:japanese-wiktionary" and compact_keys & {"text", "definition", "quotation", "quote", "example", "excerpt"}:
                        failures.append(f"evidence {artifact['file']}: prohibited Wiktionary text field")
                        break
            if evidence_mode == "full":
                actual_files = {path.name for path in EVIDENCE_DIR.glob("*.evidence.json.gz")}
                if actual_files != declared_files:
                    failures.append("evidence manifest: declared artifact set differs from persisted stores")
        elif any(EVIDENCE_DIR.glob("*.evidence.json.gz")):
            failures.append("evidence stores exist without a visibility-boundary manifest")
    except Exception as exc:
        failures.append(f"registry/snapshots/evidence: {exc}")

    print(f"schemas={len(schemas)} positive={positive_count} negative={negative_count} registry=1 snapshots={snapshot_count} evidence={evidence_count}")
    if failures:
        print(f"FAILED ({len(failures)} errors)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: all contract schemas, fixtures, semantic invariants, and source registry checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
