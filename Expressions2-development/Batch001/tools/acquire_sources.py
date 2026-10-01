#!/usr/bin/env python3
"""Controlled, atomic source acquisition for Expressions2 Batch 001.

Downloads only registry entries marked approved-for-snapshot, enforces per-source
hosts and byte ceilings, inspects containers without extracting them, verifies
hashes twice, persists compact notices/manifests, deletes raw bytes, and only
then promotes registry entries to approved.
"""
from __future__ import annotations

import bz2
import gzip
import hashlib
import json
import os
import shutil
import ssl
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT.parents[1]
REGISTRY_PATH = ROOT / "source-registry" / "sources.json"
SCHEMA_DIR = ROOT / "schema"
SNAPSHOT_DIR = ROOT / "snapshots"
CACHE_ROOT = APP_ROOT / ".cache" / "expressions2-source-acquisition"
USER_AGENT = "Koto-Expressions2-source-acquirer/0.1 (+private commissioning build)"
CHUNK = 1024 * 1024

VERSION_HINTS = {
    "source2:jmdict-english": "JMdict-English-current",
    "source2:tatoeba-cc0": "Tatoeba-weekly-CC0",
    "source2:tatoeba-japanese-ccby": "Tatoeba-weekly-jpn",
    "source2:japanese-wiktionary": "2026-09-01",
    "source2:japanese-wordnet-ok": "1.1",
    "source2:sudachidict-core": "20260723.1",
    "source2:sudachipy-runtime": "0.7.0-cp310-abi3-manylinux-x86_64",
    "source2:unidic-modern-bsd": "3.1.0-202302",
}

EXTRA_NOTICE_URLS = {
    "source2:sudachidict-core": ["https://raw.githubusercontent.com/WorksApplications/SudachiDict/develop/LEGAL"],
}


class AcquisitionError(RuntimeError):
    pass


class HostGuardRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed_hosts: set[str]):
        super().__init__()
        self.allowed_hosts = allowed_hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urllib.parse.urlparse(newurl)
        if target.scheme != "https" or target.hostname not in self.allowed_hosts:
            raise AcquisitionError(f"redirect to unapproved endpoint: {target.scheme}://{target.hostname}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member_name(name: str) -> bool:
    normalized = name.replace("\\", "/")
    candidate = PurePosixPath(normalized)
    return not candidate.is_absolute() and ".." not in candidate.parts and "" not in candidate.parts


def inspect_zip(path: Path, source_id: str) -> str:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if not infos or len(infos) > 2_000_000:
            raise AcquisitionError(f"{source_id}: implausible ZIP member count {len(infos)}")
        for info in infos:
            if not safe_member_name(info.filename):
                raise AcquisitionError(f"{source_id}: unsafe ZIP member {info.filename!r}")
            if info.file_size > 4_000_000_000:
                raise AcquisitionError(f"{source_id}: ZIP member exceeds safety ceiling")
        names = [info.filename.lower() for info in infos]
        if source_id == "source2:sudachidict-core":
            if not any(name.endswith("system.dic") for name in names):
                raise AcquisitionError("SudachiDict wheel has no system.dic")
            if not any("license" in name or name.endswith("legal") for name in names):
                raise AcquisitionError("SudachiDict wheel has no licence/legal notice")
        elif source_id == "source2:sudachipy-runtime":
            if not any(name.endswith(".so") for name in names):
                raise AcquisitionError("SudachiPy wheel has no Linux extension module")
            if not any(name.endswith(".dist-info/metadata") for name in names):
                raise AcquisitionError("SudachiPy wheel has no package metadata")
            if not any("license" in name for name in names):
                raise AcquisitionError("SudachiPy wheel has no licence notice")
        elif source_id == "source2:unidic-modern-bsd":
            if not any(name.endswith("dicrc") for name in names):
                raise AcquisitionError("UniDic archive has no dicrc")
            if not any(name.endswith("sys.dic") for name in names):
                raise AcquisitionError("UniDic archive has no compiled system dictionary")
            if not any("license" in name or "copy" in name or "readme" in name for name in names):
                raise AcquisitionError("UniDic archive has no visible notice/readme")
        return f"safe ZIP: {len(infos)} members"


def inspect_tar(path: Path, source_id: str) -> str:
    with tarfile.open(path, mode="r:bz2") as archive:
        members = archive.getmembers()
        if not members or len(members) > 2_000_000:
            raise AcquisitionError(f"{source_id}: implausible TAR member count {len(members)}")
        for member in members:
            if not safe_member_name(member.name):
                raise AcquisitionError(f"{source_id}: unsafe TAR member {member.name!r}")
            if member.issym() or member.islnk() or member.isdev():
                raise AcquisitionError(f"{source_id}: links/devices prohibited in source TAR")
        return f"safe TAR/BZip2: {len(members)} members"


def inspect_compressed_text(path: Path, source_id: str) -> str:
    opener = gzip.open if path.name.endswith(".gz") else bz2.open
    with opener(path, "rb") as stream:
        sample = stream.read(65536)
    if not sample:
        raise AcquisitionError(f"{source_id}: compressed file is empty after decompression")
    if source_id == "source2:jmdict-english":
        if b"<JMdict" not in sample and b"JMdict" not in sample:
            raise AcquisitionError("JMdict gzip does not begin as JMdict XML")
        return "valid GZip/XML JMdict prefix"
    if source_id == "source2:tatoeba-japanese-ccby":
        first = sample.splitlines()[0]
        if first.count(b"\t") < 2:
            raise AcquisitionError("Tatoeba Japanese export does not begin as TSV")
        return "valid BZip2/TSV prefix"
    if source_id == "source2:japanese-wiktionary":
        if b"<mediawiki" not in sample and b"<mediawiki" not in sample.lower():
            raise AcquisitionError("Wiktionary dump does not begin as MediaWiki XML")
        return "valid BZip2/MediaWiki XML prefix"
    if source_id == "source2:japanese-wordnet-ok":
        first = sample.splitlines()[0]
        if first.count(b"\t") < 1:
            raise AcquisitionError("Japanese WordNet export does not begin as TSV")
        return "valid GZip/TSV prefix"
    raise AcquisitionError(f"{source_id}: no compressed-text inspection rule")


def inspect_source(path: Path, source_id: str) -> tuple[str, str]:
    if source_id == "source2:tatoeba-cc0":
        return "application/x-bzip2-tar", inspect_tar(path, source_id)
    if source_id in {"source2:sudachidict-core", "source2:sudachipy-runtime", "source2:unidic-modern-bsd"}:
        return "application/zip", inspect_zip(path, source_id)
    if source_id in {"source2:jmdict-english", "source2:japanese-wordnet-ok"}:
        return "application/gzip", inspect_compressed_text(path, source_id)
    if source_id in {"source2:tatoeba-japanese-ccby", "source2:japanese-wiktionary"}:
        return "application/x-bzip2", inspect_compressed_text(path, source_id)
    raise AcquisitionError(f"no inspection rule for {source_id}")


def download_source(source: dict[str, Any], destination: Path) -> tuple[int, str, str, dict[str, str]]:
    policy = source["networkPolicy"]
    allowed_hosts = set(policy["allowedHosts"])
    opener = urllib.request.build_opener(HostGuardRedirectHandler(allowed_hosts), urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    request = urllib.request.Request(source["acquisitionUrl"], headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
    digest = hashlib.sha256()
    total = 0
    with opener.open(request, timeout=180) as response:
        status = getattr(response, "status", None)
        if status != 200:
            raise AcquisitionError(f"{source['sourceId']}: HTTP {status}")
        final_url = response.geturl()
        final = urllib.parse.urlparse(final_url)
        if final.scheme != "https" or final.hostname not in allowed_hosts:
            raise AcquisitionError(f"{source['sourceId']}: final endpoint is not approved")
        header_length = response.headers.get("Content-Length")
        if header_length and int(header_length) > policy["maxBytes"]:
            raise AcquisitionError(f"{source['sourceId']}: Content-Length exceeds maxBytes")
        with destination.open("wb") as output:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if total > policy["maxBytes"]:
                    raise AcquisitionError(f"{source['sourceId']}: streamed bytes exceed maxBytes")
                output.write(chunk)
                digest.update(chunk)
        headers = {key.lower(): value for key, value in response.headers.items()}
    actual_hash = digest.hexdigest()
    if total < 1:
        raise AcquisitionError(f"{source['sourceId']}: empty download")
    if policy["expectedBytes"] is not None and total != policy["expectedBytes"]:
        raise AcquisitionError(f"{source['sourceId']}: expected {policy['expectedBytes']} bytes, received {total}")
    if policy["expectedSha256"] is not None and actual_hash != policy["expectedSha256"]:
        raise AcquisitionError(f"{source['sourceId']}: published SHA-256 mismatch")
    if sha256_file(destination) != actual_hash:
        raise AcquisitionError(f"{source['sourceId']}: independent SHA-256 verification failed")
    # Persist only endpoint identity, never an ephemeral signed query string.
    recorded_final_url = urllib.parse.urlunsplit((final.scheme, final.netloc, final.path, "", ""))
    return total, actual_hash, recorded_final_url, headers


def fetch_notice(url: str) -> bytes:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise AcquisitionError(f"licence notice URL is not HTTPS: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(request, timeout=90) as response:
        final = urllib.parse.urlparse(response.geturl())
        if response.status != 200 or final.scheme != "https":
            raise AcquisitionError(f"licence notice fetch failed: {url}")
        data = response.read(2_000_001)
    if not data or len(data) > 2_000_000:
        raise AcquisitionError(f"licence notice has invalid size: {url}")
    return data


def notice_bundle(source: dict[str, Any]) -> bytes:
    urls = [source["license"]["url"], *EXTRA_NOTICE_URLS.get(source["sourceId"], [])]
    sections: list[bytes] = []
    for url in urls:
        data = fetch_notice(url)
        sections.append(f"SOURCE URL: {url}\n\n".encode() + data)
    return b"\n\n===== NEXT NOTICE =====\n\n".join(sections)


def version_or_date(source_id: str, headers: dict[str, str], retrieved_at: str) -> str:
    hint = VERSION_HINTS[source_id]
    modified = headers.get("last-modified")
    if modified and source_id in {"source2:jmdict-english", "source2:tatoeba-cc0", "source2:tatoeba-japanese-ccby"}:
        try:
            date = parsedate_to_datetime(modified).date().isoformat()
            return f"{hint}-{date}"
        except (TypeError, ValueError, OverflowError):
            pass
    return hint if hint else f"retrieved-{retrieved_at[:10]}"


def redistribution(source: dict[str, Any]) -> str:
    allowed = source["allowed"]
    if allowed["redistributeRaw"]:
        return "raw-and-derived"
    if source["permissionClass"] == "evidence-only":
        return "derived-only"
    if allowed["publishDerivedRecords"]:
        return "tool-output-only"
    return "none"


def schema_registry() -> tuple[dict[str, Any], Registry]:
    schemas = []
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = json.loads(path.read_text())
        schemas.append(schema)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    snapshot = next(item for item in schemas if item["$id"].endswith("snapshot-manifest.schema.json"))
    return snapshot, registry


def validate_manifest(manifest: dict[str, Any], schema: dict[str, Any], registry: Registry) -> None:
    errors = list(Draft202012Validator(schema, registry=registry, format_checker=FormatChecker()).iter_errors(manifest))
    if errors:
        rendered = "; ".join(f"/{'/'.join(map(str, e.absolute_path))}: {e.message}" for e in errors)
        raise AcquisitionError(f"generated snapshot manifest is invalid: {rendered}")


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def main() -> int:
    registry_document = json.loads(REGISTRY_PATH.read_text())
    selected = [source for source in registry_document["sources"] if source["approvalStatus"] == "approved-for-snapshot"]
    if not selected:
        print("No sources are marked approved-for-snapshot; nothing to do.")
        return 0
    unexpected = [source["sourceId"] for source in registry_document["sources"] if source["approvalStatus"] not in {"approved-for-snapshot", "approved"}]
    if unexpected:
        raise AcquisitionError(f"registry still contains unresolved source states: {unexpected}")

    snapshot_schema, reference_registry = schema_registry()
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix="session-", dir=CACHE_ROOT))
    staged_notices: dict[str, bytes] = {}
    manifests: dict[str, dict[str, Any]] = {}
    updated_document = json.loads(json.dumps(registry_document))
    updated_by_id = {source["sourceId"]: source for source in updated_document["sources"]}

    try:
        for ordinal, source in enumerate(selected, 1):
            source_id = source["sourceId"]
            filename = Path(urllib.parse.urlparse(source["acquisitionUrl"]).path).name or f"source-{ordinal}.bin"
            raw_path = staging / f"{ordinal:02d}-{filename}"
            print(f"[{ordinal}/{len(selected)}] acquiring {source_id} (ceiling {source['networkPolicy']['maxBytes']:,} bytes)", flush=True)
            retrieved_at = utc_now()
            total, actual_hash, final_url, headers = download_source(source, raw_path)
            media_type, inspection = inspect_source(raw_path, source_id)
            notice = notice_bundle(source)
            notice_name = source_id.removeprefix("source2:") + ".license"
            notice_hash = hashlib.sha256(notice).hexdigest()
            manifest = {
                "schemaVersion": 1,
                "sourceId": source_id,
                "canonicalUrl": source["canonicalUrl"],
                "acquisitionUrl": source["acquisitionUrl"],
                "finalUrl": final_url,
                "retrievedAt": retrieved_at,
                "bytes": total,
                "sha256": actual_hash,
                "mediaType": media_type,
                "license": {
                    "name": source["license"]["name"],
                    "url": source["license"]["url"],
                    "noticeFile": f"notices/{notice_name}",
                    "noticeSha256": notice_hash,
                },
                "attribution": source["license"]["attribution"],
                "allowedRoles": source["roles"],
                "redistribution": redistribution(source),
                "rawRetention": "temporary-deleted",
                "rawFile": None,
                "verification": {
                    "httpStatus": 200,
                    "registryMatch": True,
                    "hashVerified": True,
                    "expectedIdentityMatch": True,
                    "archiveSafe": True,
                    "unexpectedFormat": False,
                },
            }
            validate_manifest(manifest, snapshot_schema, reference_registry)
            staged_notices[notice_name] = notice
            manifests[source_id] = manifest
            target = updated_by_id[source_id]
            target["approvalStatus"] = "approved"
            target["networkPolicy"]["expectedBytes"] = total
            target["networkPolicy"]["expectedSha256"] = actual_hash
            target["snapshot"] = {
                "versionOrDate": version_or_date(source_id, headers, retrieved_at),
                "retrievedAt": retrieved_at,
                "byteLength": total,
                "sha256": actual_hash,
                "mediaType": media_type,
            }
            print(f"    verified {total:,} bytes sha256={actual_hash} ({inspection})", flush=True)
            raw_path.unlink()

        # Commit only after all sources and all generated manifests passed.
        for notice_name, notice in staged_notices.items():
            atomic_write(SNAPSHOT_DIR / "notices" / notice_name, notice)
        for source_id, manifest in manifests.items():
            name = source_id.removeprefix("source2:") + ".snapshot.json"
            atomic_write(SNAPSHOT_DIR / "manifests" / name, (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
        atomic_write(REGISTRY_PATH, (json.dumps(updated_document, ensure_ascii=False, indent=2) + "\n").encode())

        total_bytes = sum(item["bytes"] for item in manifests.values())
        print(f"PASS: atomically recorded {len(manifests)} verified snapshots ({total_bytes:,} bytes); raw downloads deleted")
        return 0
    finally:
        shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AcquisitionError, urllib.error.URLError, OSError, zipfile.BadZipFile, tarfile.TarError, EOFError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
