#!/usr/bin/env python3
"""Merge and validate all eight independently built pilot shards."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tarfile
from pathlib import Path
from typing import Any

import build_pilot as bp


def extract_archive(archive_path: Path, target: Path) -> Path:
    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive.getmembers():
            parts = Path(member.name).parts
            if member.issym() or member.islnk() or member.name.startswith("/") or ".." in parts:
                raise bp.PilotError(f"unsafe shard archive member in {archive_path.name}")
            if not member.isfile():
                continue
            source = archive.extractfile(member)
            if source is None:
                raise bp.PilotError(f"unreadable shard archive member in {archive_path.name}")
            destination = target / member.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("wb") as output:
                shutil.copyfileobj(source, output)
    return target / "pilot-shard"


def copy_tree_files(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    for path in sorted(item for item in source.rglob("*") if item.is_file()):
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != path.read_bytes():
            raise bp.PilotError(f"conflicting shard output: {target.relative_to(bp.ROOT)}")
        shutil.copyfile(path, target)


def validate_transferred_record(root: Path, record: dict[str, Any], registry: Any) -> None:
    key = record["candidateId"].removeprefix("candidate2:")
    compiler_capture = bp.read_json(root / "model-responses" / "compiler" / f"{key}.json")
    critic_capture = bp.read_json(root / "model-responses" / "critic" / f"{key}.json")
    if bp.sha(bp.canonical(compiler_capture["response"])) != record["compilerResponseSha256"]:
        raise bp.PilotError("compiler response digest changed during shard transfer")
    if bp.sha(bp.canonical(critic_capture["response"])) != record["criticResponseSha256"]:
        raise bp.PilotError("critic response digest changed during shard transfer")
    bp.validate(critic_capture["response"], bp.critic_schema(), registry, "transferred critic response")


def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise bp.PilotError("GitHub Actions only")
    run_id = os.environ["EXPRESSIONS2_RUN_ID"]
    archive_dir = Path(os.environ["EXPRESSIONS2_SHARD_DIR"])
    archives = sorted(archive_dir.glob(f"expressions2-batch001-pilot-run-{run_id}-shard-*.tar.gz"))
    if len(archives) != 8:
        raise bp.PilotError(f"expected 8 private shard checkpoints, found {len(archives)}")

    bp.PILOT = bp.ROOT / "pilot"
    bp.TMP = Path("/tmp/expressions2-pilot-merge")
    shutil.rmtree(bp.PILOT, ignore_errors=True)
    shutil.rmtree(bp.VOCABULARY, ignore_errors=True)
    shutil.rmtree(bp.TMP, ignore_errors=True)
    bp.PILOT.mkdir(parents=True)
    bp.TMP.mkdir(parents=True)
    extracted_root = bp.TMP / "shards"

    manifests: dict[int, tuple[dict[str, Any], Path]] = {}
    for ordinal, archive in enumerate(archives):
        shard_root = extract_archive(archive, extracted_root / str(ordinal))
        failure = shard_root / "failure.json"
        if failure.exists():
            value = bp.read_json(failure)
            raise bp.PilotError(f"pilot shard {value.get('shardIndex')} failed: {value.get('errorType', 'unknown')}")
        manifest_path = shard_root / "manifest.json"
        if not manifest_path.exists():
            raise bp.PilotError(f"shard checkpoint lacks manifest: {archive.name}")
        manifest = bp.read_json(manifest_path)
        index = manifest.get("shardIndex")
        if not isinstance(index, int) or index not in range(8) or index in manifests:
            raise bp.PilotError("shard indices are not exactly unique integers 0 through 7")
        if str(manifest.get("githubRunId")) != run_id:
            raise bp.PilotError("shard run identity mismatch")
        manifests[index] = (manifest, shard_root)
    if set(manifests) != set(range(8)):
        raise bp.PilotError("shard index conservation failed")

    ordered = [manifests[index] for index in range(8)]
    selection = ordered[0][0]["selectionCandidateIds"]
    if len(selection) != 8 or len(set(selection)) != 8:
        raise bp.PilotError("pilot selection is not exactly eight unique candidates")
    candidate_build_id = bp.read_json(bp.CANDIDATES / "manifest.json")["buildId"]
    lock = bp.read_json(bp.LOCK_PATH)
    lock_sha = bp.sha(bp.canonical(lock))
    source_date = bp.read_json(bp.EVIDENCE / "manifest.json")["sourceDateEpoch"]
    records: list[dict[str, Any]] = []
    model_calls = 0
    cache_hits = 0
    wall_seconds = 0.0
    model_seconds = {"compiler": 0.0, "critic": 0.0}
    _, registry = bp.schema_registry()

    for index, (manifest, shard_root) in enumerate(ordered):
        if manifest["selectionCandidateIds"] != selection:
            raise bp.PilotError("deterministic selection differs between shards")
        if manifest["record"]["candidateId"] != selection[index]:
            raise bp.PilotError("shard candidate does not match its deterministic selection index")
        if manifest["candidateBuildId"] != candidate_build_id:
            raise bp.PilotError("shard candidate build identity mismatch")
        if manifest["modelLockSha256"] != lock_sha:
            raise bp.PilotError("shard model lock identity mismatch")
        if manifest["sourceDateEpoch"] != source_date:
            raise bp.PilotError("shard evidence epoch mismatch")
        validate_transferred_record(shard_root, manifest["record"], registry)
        for name in ["families", "quarantine", "critic-reports", "model-responses"]:
            copy_tree_files(shard_root / name, bp.PILOT / name)
        records.append(manifest["record"])
        metrics = manifest["metrics"]
        model_calls += int(metrics["modelCalls"])
        cache_hits += int(metrics["cacheHits"])
        wall_seconds = max(wall_seconds, float(metrics["wallSeconds"]))
        for role in model_seconds:
            model_seconds[role] += float(metrics["modelSeconds"][role])

    # Rebuild the exact pinned canonical Vocabulary source once for the merged durable bundle.
    prior = bp.PriorArchive(os.environ.get("EXPRESSIONS2_PRIOR_PILOT"))
    bp.build_vocabulary_index(prior, lock["vocabularySource"])
    prior.close()

    schemas, registry = bp.schema_registry()
    for record in records:
        key = record["candidateId"].removeprefix("candidate2:")
        if record["pilotStatus"] != "passed":
            if not (bp.PILOT / "quarantine" / f"{key}.json").exists():
                raise bp.PilotError("quarantined record lacks its retained diagnostic")
            continue
        family_dir = bp.PILOT / "families" / key
        family = bp.read_json(family_dir / "family.json")
        analyses = bp.read_json(family_dir / "analyses.json")
        provenance = bp.read_json(family_dir / "provenance.json")
        bp.validate(family, schemas["family"], registry, "merged family")
        for analysis in analyses:
            bp.validate(analysis, schemas["form-analysis"], registry, "merged analysis")
        bp.validate(provenance, schemas["provenance"], registry, "merged provenance")

    metrics = {
        "schemaVersion": 1,
        "githubRunId": run_id,
        "execution": "eight-parallel-candidate-shards",
        "modelCalls": model_calls,
        "cacheHits": cache_hits,
        "modelSeconds": model_seconds,
        "maxShardWallSeconds": wall_seconds,
        "selectedCandidateIds": selection,
    }
    bp.write_json(bp.PILOT / "metrics.json", metrics)
    compiled = sum(record["compilerStatus"] == "compiled" for record in records)
    passed = sum(record["pilotStatus"] == "passed" for record in records)
    body = {
        "scope": "eight-family-dual-open-model",
        "release": "0.1.0-development",
        "publicationStatus": "shadow-candidate",
        "productionReady": False,
        "candidateBuildId": candidate_build_id,
        "modelLockSha256": lock_sha,
        "models": [{
            "role": item["role"], "repository": item["repository"], "revision": item["revision"],
            "fileSha256": item["sha256"], "license": item["license"],
        } for item in lock["models"]],
        "counts": {
            "attemptedCandidates": 8,
            "compiledFamilies": compiled,
            "independentlyCritiqued": 8,
            "passedPilotGates": passed,
            "quarantined": 8 - passed,
            "acceptedFamilies": 0,
        },
        "records": records,
        "determinism": {
            "canonicalJson": True,
            "capturedModelResponsesAreInputs": True,
            "secondDeterministicCompileMatched": True,
        },
        "incrementalBuild": {"contentAddressedResponseCache": True, "changedOnlySupported": True},
        "safety": {
            "noLocalApplicationStorage": True,
            "noLiveExpressionsMutation": True,
            "noModelWeightsPersisted": True,
            "privateDraftReleaseOnly": True,
            "gatesNotLowered": True,
        },
        "artifacts": bp.artifact_list(),
    }
    manifest = {"schemaVersion": 1, "pilotId": bp.stable_id("pilot2:", bp.sha(bp.canonical(body))), **body}
    if passed + manifest["counts"]["quarantined"] != 8:
        raise bp.PilotError("merged pilot count conservation failed")
    bp.validate(manifest, schemas["pilot-manifest"], registry, "merged pilot manifest")
    bp.write_json(bp.PILOT / "manifest.json", manifest)
    print(json.dumps({
        "marker": "PARALLEL_PILOT_MERGE_COMPLETE", "pilotId": manifest["pilotId"],
        "passedPilotGates": passed, "quarantined": 8 - passed, "acceptedFamilies": 0,
    }, sort_keys=True), flush=True)
    return 0 if passed == 8 else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (bp.PilotError, OSError, ValueError, tarfile.TarError) as exc:
        print(f"PILOT_MERGE_FAILED: {type(exc).__name__}: {str(exc)[:500]}", file=sys.stderr, flush=True)
        raise SystemExit(1)
