#!/usr/bin/env python3
"""Build deterministic, licence-aware evidence stores from pinned sources.

This stage emits no candidates or families. Raw archives are downloaded into an
excluded temporary directory, verified against the snapshot registry, parsed
without extraction, rebuilt a second time for byte equality, and deleted.
"""
from __future__ import annotations

import argparse
import bz2
import gzip
import hashlib
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

import acquire_sources

ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT.parents[1]
REGISTRY_PATH = ROOT / "source-registry" / "sources.json"
SCHEMA_DIR = ROOT / "schema"
EVIDENCE_DIR = ROOT / "evidence"
CACHE_ROOT = APP_ROOT / ".cache" / "expressions2-evidence-build"
ADAPTER_VERSION = "0.1.0"
JAPANESE = re.compile(r"[ぁ-ゖァ-ヺ一-龯々〆ヵヶ]")
BANNED_TEXT = ("src/data/" + "expressions", "expression_" + "progress", "legacy/" + "expressions")


class EvidenceBuildError(RuntimeError):
    pass


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def evidence_id(source_id: str, locator: str, record_hash: str) -> str:
    value = f"{source_id}\0{locator}\0{record_hash}".encode()
    return "evidence2:" + hashlib.sha256(value).hexdigest()[:32]


def record(source: dict[str, Any], locator: str, record_hash: str, fields: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidenceId": evidence_id(source["sourceId"], locator, record_hash),
        "locator": locator,
        "recordHash": record_hash,
        "fields": fields,
        "permissionClass": source["permissionClass"],
    }


def normalized(value: str) -> str:
    return unicodedata.normalize("NFC", value).replace("\x00", "").strip()


def parse_jmdict(path: Path, source: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    markers = ("expression", "idiomatic", "proverb", "yojijukugo", "collocation")
    with gzip.open(path, "rb") as stream:
        for _, elem in ET.iterparse(stream, events=("end",)):
            if elem.tag != "entry":
                continue
            sequence = elem.findtext("ent_seq") or ""
            forms = [normalized(node.text or "") for node in elem.findall("./k_ele/keb") if normalized(node.text or "")]
            readings = [normalized(node.text or "") for node in elem.findall("./r_ele/reb") if normalized(node.text or "")]
            labels: set[str] = set()
            glosses: list[str] = []
            for sense in elem.findall("sense"):
                for tag in ("pos", "misc", "field", "dial"):
                    labels.update(normalized(node.text or "") for node in sense.findall(tag) if normalized(node.text or ""))
                for gloss in sense.findall("gloss"):
                    text = normalized(gloss.text or "")
                    lang = gloss.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", "eng")
                    if text and lang in {"eng", "en"} and text not in glosses:
                        glosses.append(text)
            label_text = " | ".join(sorted(labels))
            if not any(marker in label_text.lower() for marker in markers):
                elem.clear()
                continue
            surface = forms[0] if forms else (readings[0] if readings else "")
            if not surface or not JAPANESE.search(surface):
                elem.clear()
                continue
            raw_hash = digest_bytes(ET.tostring(elem, encoding="utf-8"))
            locator = f"ent_seq:{sequence}"
            results.append(record(source, locator, raw_hash, {
                "surface": surface,
                "forms": "␟".join(forms),
                "readings": "␟".join(readings),
                "glosses": "␟".join(glosses[:8]),
                "labels": label_text,
            }))
            elem.clear()
    return sorted(results, key=lambda item: item["locator"])


def tatoeba_line(line: bytes, source: dict[str, Any]) -> dict[str, Any] | None:
    stripped = line.rstrip(b"\r\n")
    if not stripped:
        return None
    try:
        columns = stripped.decode("utf-8").split("\t")
    except UnicodeDecodeError:
        return None
    if len(columns) < 2 or not columns[0].isdigit():
        return None
    sentence_id = columns[0]
    if len(columns) >= 3 and re.fullmatch(r"[a-z]{3}", columns[1]):
        if columns[1] != "jpn":
            return None
        language, text = "jpn", columns[2]
    else:
        # Per-language exports may omit the language column.
        language, text = "jpn", columns[1]
    text = normalized(text)
    if not text or text == "\\N":
        return None
    locator = f"sentence:{sentence_id}"
    return record(source, locator, digest_bytes(stripped), {
        "language": language,
        "text": text,
        "normalizedText": text,
    })


def parse_tatoeba_cc0(path: Path, source: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with tarfile.open(path, mode="r:bz2") as archive:
        files = [member for member in archive.getmembers() if member.isfile()]
        if len(files) != 1:
            raise EvidenceBuildError(f"Tatoeba CC0 expected one regular member, got {len(files)}")
        extracted = archive.extractfile(files[0])
        if extracted is None:
            raise EvidenceBuildError("Tatoeba CC0 member could not be streamed")
        for line in extracted:
            item = tatoeba_line(line, source)
            if item and item["fields"]["language"] == "jpn":
                results.append(item)
    return sorted(results, key=lambda item: item["locator"])


def parse_tatoeba_jpn(path: Path, source: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with bz2.open(path, "rb") as stream:
        for line in stream:
            item = tatoeba_line(line, source)
            if item:
                results.append(item)
    return sorted(results, key=lambda item: item["locator"])


def parse_wordnet(path: Path, source: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with gzip.open(path, "rb") as stream:
        for line_number, raw_line in enumerate(stream, 1):
            stripped = raw_line.rstrip(b"\r\n")
            if not stripped:
                continue
            try:
                columns = stripped.decode("utf-8").split("\t")
            except UnicodeDecodeError:
                continue
            if len(columns) < 2:
                continue
            synset = normalized(columns[0])
            lemma = normalized(columns[1])
            confidence = normalized(columns[2]) if len(columns) > 2 else ""
            if not synset or not lemma:
                continue
            locator = f"line:{line_number:07d}:synset:{synset}:lemma:{lemma}"
            results.append(record(source, locator, digest_bytes(stripped), {
                "synset": synset, "lemma": lemma, "confidenceMarker": confidence,
            }))
    return sorted(results, key=lambda item: item["locator"])


WIKTIONARY_MARKERS = {
    "category-expression": re.compile(r"\[\[Category:日本語[_ ](?:成句|慣用句|ことわざ|諺|連語)"),
    "template-expression": re.compile(r"\{\{(?:成句|慣用句|ことわざ|諺|連語)(?:\||\}\})"),
    "heading-expression": re.compile(r"={3,}\s*(?:成句|慣用句|ことわざ|諺|連語)\s*={3,}"),
}


def parse_wiktionary(path: Path, source: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with bz2.open(path, "rb") as stream:
        for _, elem in ET.iterparse(stream, events=("end",)):
            if elem.tag != "page" and not elem.tag.endswith("}page"):
                continue
            title = normalized(elem.findtext("{*}title") or elem.findtext("title") or "")
            namespace = normalized(elem.findtext("{*}ns") or elem.findtext("ns") or "")
            page_id = normalized(elem.findtext("{*}id") or elem.findtext("id") or "")
            revision_id = normalized(elem.findtext("{*}revision/{*}id") or elem.findtext("revision/id") or "")
            text_node = elem.find("{*}revision/{*}text")
            if text_node is None:
                text_node = elem.find("revision/text")
            text = text_node.text if text_node is not None and text_node.text else ""
            if namespace != "0" or not (2 <= len(title) <= 80) or ":" in title or not JAPANESE.search(title):
                elem.clear()
                continue
            if not re.search(r"(?:==\s*日本語\s*==|==\s*\{\{ja\}\}\s*==|\{\{ja-)" , text):
                elem.clear()
                continue
            markers = sorted(name for name, pattern in WIKTIONARY_MARKERS.items() if pattern.search(text))
            if not markers:
                elem.clear()
                continue
            locator = f"page:{page_id}:revision:{revision_id}"
            full_hash = digest_bytes(text.encode("utf-8"))
            # Deliberately retain only page identity and structural markers—never definitions, quotations, or examples.
            results.append(record(source, locator, full_hash, {
                "surface": title,
                "pageId": page_id,
                "revisionId": revision_id,
                "markers": "|".join(markers),
            }))
            elem.clear()
    return sorted(results, key=lambda item: item["locator"])


def parse_dictionary_inventory(path: Path, source: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with zipfile.ZipFile(path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if info.is_dir():
                continue
            locator = f"member:{info.filename}"
            metadata = f"{info.filename}\0{info.file_size}\0{info.compress_size}\0{info.CRC:08x}".encode()
            results.append(record(source, locator, digest_bytes(metadata), {
                "member": info.filename,
                "bytes": info.file_size,
                "compressedBytes": info.compress_size,
                "crc32": f"{info.CRC:08x}",
                "kind": "compiled-dictionary" if info.filename.lower().endswith(("system.dic", "sys.dic")) else "supporting-file",
            }))
    return results


PARSERS: dict[str, tuple[str, Callable[[Path, dict[str, Any]], list[dict[str, Any]]]]] = {
    "source2:jmdict-english": ("jmdict-expression", parse_jmdict),
    "source2:tatoeba-cc0": ("tatoeba-cc0-japanese", parse_tatoeba_cc0),
    "source2:tatoeba-japanese-ccby": ("tatoeba-japanese-evidence", parse_tatoeba_jpn),
    "source2:japanese-wiktionary": ("wiktionary-structural-expression", parse_wiktionary),
    "source2:japanese-wordnet-ok": ("wordnet-high-confidence", parse_wordnet),
    "source2:sudachidict-core": ("sudachidict-inventory", parse_dictionary_inventory),
    "source2:sudachipy-runtime": ("sudachipy-runtime-inventory", parse_dictionary_inventory),
    "source2:unidic-modern-bsd": ("unidic-inventory", parse_dictionary_inventory),
}


def schema_environment() -> tuple[dict[str, Any], dict[str, Any], Registry]:
    schemas: dict[str, dict[str, Any]] = {}
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = json.loads(path.read_text())
        name = path.name.removesuffix(".schema.json")
        schemas[name] = schema
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return schemas["source-evidence"], schemas["evidence-build-manifest"], registry


def validate(value: Any, schema: dict[str, Any], registry: Registry, label: str) -> None:
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    errors = list(validator.iter_errors(value))
    if errors:
        first = errors[0]
        pointer = "/" + "/".join(map(str, first.absolute_path))
        raise EvidenceBuildError(f"{label} schema failure at {pointer}: {first.message}")


def contamination_findings(store: dict[str, Any], expected_permission: str) -> list[str]:
    findings: list[str] = []
    for item in store["records"]:
        if item["permissionClass"] != expected_permission:
            findings.append(f"{item['locator']}: permission mismatch")
        for key, value in item["fields"].items():
            compact_key = re.sub(r"[^a-z0-9]", "", key.lower())
            if compact_key in {"legacyid", "oldid", "familyid", "candidateid"}:
                findings.append(f"{item['locator']}: prohibited lineage key {key}")
            if store["sourceId"] == "source2:japanese-wiktionary" and compact_key in {"text", "definition", "quotation", "quote", "example", "excerpt"}:
                findings.append(f"{item['locator']}: prohibited Wiktionary text field {key}")
            if isinstance(value, str):
                lower = value.lower()
                if any(banned.lower() in lower for banned in BANNED_TEXT):
                    findings.append(f"{item['locator']}: prohibited legacy path text")
                if value.startswith("expression:") and not value.startswith("expression2:"):
                    findings.append(f"{item['locator']}: legacy expression ID")
    return findings


def artifact_filename(source_id: str) -> str:
    return source_id.removeprefix("source2:") + ".evidence.json.gz"


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--only", action="append", default=[], metavar="SOURCE_ID",
                                 help="rebuild only this source and reuse validated unchanged artifacts")
    args = argument_parser.parse_args()

    registry_document = json.loads(REGISTRY_PATH.read_text())
    sources = registry_document["sources"]
    if set(PARSERS) != {source["sourceId"] for source in sources}:
        raise EvidenceBuildError("adapter/source registry mismatch")
    for source in sources:
        if source["approvalStatus"] != "approved" or not source["snapshot"]:
            raise EvidenceBuildError(f"source is not pinned and approved: {source['sourceId']}")

    evidence_schema, manifest_schema, schema_registry = schema_environment()
    source_ids = {source["sourceId"] for source in sources}
    requested = set(args.only)
    unknown = requested - source_ids
    if unknown:
        raise EvidenceBuildError(f"unknown --only source IDs: {sorted(unknown)}")
    selected_sources = [source for source in sources if not requested or source["sourceId"] in requested]

    artifacts: list[dict[str, Any]] = []
    if requested:
        manifest_path = EVIDENCE_DIR / "manifest.json"
        if not manifest_path.is_file():
            raise EvidenceBuildError("changed-only rebuild requires an existing evidence manifest")
        previous_manifest = json.loads(manifest_path.read_text())
        validate(previous_manifest, manifest_schema, schema_registry, "existing evidence manifest")
        for artifact in previous_manifest["artifacts"]:
            if artifact["sourceId"] in requested:
                continue
            source = next(item for item in sources if item["sourceId"] == artifact["sourceId"])
            path = EVIDENCE_DIR / artifact["file"]
            if not path.is_file():
                raise EvidenceBuildError(f"unchanged artifact is missing: {artifact['file']}")
            compressed = path.read_bytes()
            if len(compressed) != artifact["compressedBytes"] or digest_bytes(compressed) != artifact["compressedSha256"]:
                raise EvidenceBuildError(f"unchanged compressed identity mismatch: {artifact['file']}")
            canonical = gzip.decompress(compressed)
            if len(canonical) != artifact["canonicalBytes"] or digest_bytes(canonical) != artifact["canonicalSha256"]:
                raise EvidenceBuildError(f"unchanged canonical identity mismatch: {artifact['file']}")
            if artifact["snapshotSha256"] != source["snapshot"]["sha256"]:
                raise EvidenceBuildError(f"unchanged artifact uses stale snapshot: {artifact['file']}")
            artifacts.append(artifact)

    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix="session-", dir=CACHE_ROOT))
    staged_files: dict[str, bytes] = {}
    try:
        for ordinal, source in enumerate(selected_sources, 1):
            source_id = source["sourceId"]
            adapter_name, parser = PARSERS[source_id]
            raw_name = Path(urllib.parse.urlparse(source["acquisitionUrl"]).path).name
            raw_path = staging / f"{ordinal:02d}-{raw_name}"
            print(f"[{ordinal}/{len(selected_sources)}] {source_id}: download and verify", flush=True)
            total, raw_hash, _, _ = acquire_sources.download_source(source, raw_path)
            pinned = source["snapshot"]
            if total != pinned["byteLength"] or raw_hash != pinned["sha256"]:
                raise EvidenceBuildError(f"{source_id}: download differs from pinned snapshot")

            print(f"    adapter {adapter_name}: deterministic pass 1", flush=True)
            records_one = parser(raw_path, source)
            if not records_one:
                raise EvidenceBuildError(f"{source_id}: adapter emitted zero records")
            store_one = {"schemaVersion": 1, "snapshotSha256": raw_hash, "sourceId": source_id, "records": records_one}
            validate(store_one, evidence_schema, schema_registry, source_id)
            findings = contamination_findings(store_one, source["permissionClass"])
            if findings:
                raise EvidenceBuildError(f"{source_id}: contamination audit failed: {findings[0]}")
            canonical_one = compact_json(store_one)

            print(f"    adapter {adapter_name}: deterministic pass 2", flush=True)
            records_two = parser(raw_path, source)
            store_two = {"schemaVersion": 1, "snapshotSha256": raw_hash, "sourceId": source_id, "records": records_two}
            canonical_two = compact_json(store_two)
            if canonical_one != canonical_two:
                raise EvidenceBuildError(f"{source_id}: second adapter pass did not match")
            compressed = gzip.compress(canonical_one, compresslevel=9, mtime=0)
            filename = artifact_filename(source_id)
            staged_files[filename] = compressed
            artifacts.append({
                "sourceId": source_id,
                "file": filename,
                "snapshotSha256": raw_hash,
                "recordCount": len(records_one),
                "canonicalBytes": len(canonical_one),
                "compressedBytes": len(compressed),
                "canonicalSha256": digest_bytes(canonical_one),
                "compressedSha256": digest_bytes(compressed),
                "adapter": {"name": adapter_name, "version": ADAPTER_VERSION},
                "permissionClass": source["permissionClass"],
                "secondPassMatched": True,
            })
            print(f"    {len(records_one):,} records; {len(canonical_one):,} -> {len(compressed):,} bytes", flush=True)
            raw_path.unlink()

        artifacts.sort(key=lambda item: item["sourceId"])
        totals = {
            "sources": len(artifacts),
            "records": sum(item["recordCount"] for item in artifacts),
            "canonicalBytes": sum(item["canonicalBytes"] for item in artifacts),
            "compressedBytes": sum(item["compressedBytes"] for item in artifacts),
        }
        source_date_epoch = max(source["snapshot"]["retrievedAt"] for source in sources)
        body = {
            "sourceDateEpoch": source_date_epoch,
            "artifacts": artifacts,
            "totals": totals,
            "determinism": {"canonicalJson": True, "gzipMtime": 0, "allSecondPassesMatched": True},
            "contaminationAudit": {"legacyImports": 0, "legacyIds": 0, "prohibitedWiktionaryText": 0,
                                   "permissionMismatches": 0, "verdict": "passed"},
        }
        build_id = "evidencebuild2:" + digest_bytes(compact_json(body))[:32]
        manifest = {"schemaVersion": 1, "buildId": build_id, **body}
        validate(manifest, manifest_schema, schema_registry, "evidence manifest")

        # Commit artifacts first and manifest last; the manifest is the visibility boundary.
        for filename, data in staged_files.items():
            atomic_write(EVIDENCE_DIR / filename, data)
        atomic_write(EVIDENCE_DIR / "manifest.json", (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
        print(f"PASS: {totals['sources']} evidence stores, {totals['records']:,} records, {totals['compressedBytes']:,} persisted bytes")
        return 0
    finally:
        shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (EvidenceBuildError, acquire_sources.AcquisitionError, OSError, EOFError, ET.ParseError, zipfile.BadZipFile, tarfile.TarError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
