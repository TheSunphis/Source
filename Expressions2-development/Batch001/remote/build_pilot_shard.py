#!/usr/bin/env python3
"""Build exactly one deterministic shard of the eight-family pilot."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import build_pilot as bp


def shard_failure(index: int, exc: BaseException) -> None:
    bp.PILOT.mkdir(parents=True, exist_ok=True)
    bp.write_json(bp.PILOT / "failure.json", {
        "schemaVersion": 1,
        "githubRunId": os.environ.get("GITHUB_RUN_ID", "unknown"),
        "shardIndex": index,
        "errorType": type(exc).__name__,
        "message": str(exc)[:1000],
    })


def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise bp.PilotError("GitHub Actions only")
    try:
        index = int(os.environ["EXPRESSIONS2_PILOT_INDEX"])
    except (KeyError, ValueError) as exc:
        raise bp.PilotError("EXPRESSIONS2_PILOT_INDEX must be an integer") from exc
    if index not in range(8):
        raise bp.PilotError("pilot shard index must be between 0 and 7")

    bp.PILOT = bp.ROOT / "pilot-shard"
    bp.TMP = Path(f"/tmp/expressions2-pilot-shard-{index}")
    started = time.monotonic()
    shutil.rmtree(bp.PILOT, ignore_errors=True)
    shutil.rmtree(bp.VOCABULARY, ignore_errors=True)
    shutil.rmtree(bp.TMP, ignore_errors=True)
    bp.PILOT.mkdir(parents=True)
    bp.TMP.mkdir(parents=True)

    prior = bp.PriorArchive(os.environ.get("EXPRESSIONS2_PRIOR_PILOT"))
    schemas, registry = bp.schema_registry()
    lock = bp.read_json(bp.LOCK_PATH)
    lock_sha = bp.sha(bp.canonical(lock))
    source_registry = bp.read_json(bp.ROOT / "source-registry" / "sources.json")
    evidence_manifest = bp.read_json(bp.EVIDENCE / "manifest.json")
    candidate_manifest = bp.read_json(bp.CANDIDATES / "manifest.json")
    reviewed_at = bp.source_timestamp(evidence_manifest["sourceDateEpoch"])
    source_release = "source2:" + bp.sha(bp.canonical({
        "registrySha256": bp.sha((bp.ROOT / "source-registry" / "sources.json").read_bytes()),
        "vocabularySource": lock["vocabularySource"],
    }))

    sys.path.insert(0, os.environ["EXPRESSIONS2_RUNTIME"])
    from sudachipy import Dictionary, SplitMode
    tokenizer = Dictionary(dict="core").tokenizer()
    candidate_store = bp.read_gzip_json(bp.CANDIDATES / "normalized-candidates.json.gz")
    records = bp.evidence_maps()
    selected, contexts, segments = bp.select_candidates(tokenizer, SplitMode, candidate_store["records"], records)
    if len(selected) != 8:
        raise bp.PilotError("deterministic pilot selection did not produce exactly eight candidates")
    selection_ids = [item["candidateId"] for item in selected]
    candidate = selected[index]
    candidate_id = candidate["candidateId"]
    candidate_by_id = {item["candidateId"]: item for item in candidate_store["records"]}
    vocabulary, vocabulary_digest = bp.build_vocabulary_index(prior, lock["vocabularySource"])
    exact_vocab, vocab_by_id = bp.vocabulary_maps(vocabulary)
    metrics: dict[str, Any] = {
        "schemaVersion": 1,
        "githubRunId": os.environ.get("GITHUB_RUN_ID", "unknown"),
        "shardIndex": index,
        "modelCalls": 0,
        "cacheHits": 0,
        "modelSeconds": {"compiler": 0.0, "critic": 0.0},
        "selectedCandidateIds": [candidate_id],
    }

    context = contexts[candidate_id]
    model_schema = bp.editorial_schema(segments[candidate_id], [item["candidateId"] for item in context["approvedNearbyCandidates"]])
    system, user = bp.compiler_prompt(context, segments[candidate_id])
    compiler_capture = bp.run_model_requests("compiler", [{
        "candidateId": candidate_id, "system": system, "user": user, "schema": model_schema,
    }], lock, prior, registry, metrics)[candidate_id]
    compiler_response = compiler_capture["response"]

    package: dict[str, Any] | None = None
    compile_error: str | None = None
    if compiler_response.get("status") == "abstain":
        compile_error = "compiler-abstained"
    else:
        try:
            family, analyses = bp.compile_family(
                candidate, context, compiler_response, segments[candidate_id], candidate_by_id,
                exact_vocab, vocab_by_id, vocabulary_digest, reviewed_at, source_release, tokenizer, SplitMode,
            )
            bp.validate(family, schemas["family"], registry, "family")
            for analysis in analyses:
                bp.validate(analysis, schemas["form-analysis"], registry, "analysis")
            family2, analyses2 = bp.compile_family(
                candidate, context, compiler_response, segments[candidate_id], candidate_by_id,
                exact_vocab, vocab_by_id, vocabulary_digest, reviewed_at, source_release, tokenizer, SplitMode,
            )
            if bp.canonical({"family": family, "analyses": analyses}) != bp.canonical({"family": family2, "analyses": analyses2}):
                raise bp.GateFailure("second deterministic compile mismatch")
            package = {"family": family, "analyses": analyses}
        except Exception as exc:
            compile_error = "deterministic-gate-failed:" + str(exc)[:500]

    critic_system, critic_user = bp.critic_prompt(context, compiler_response, package)
    critic_capture = bp.run_model_requests("critic", [{
        "candidateId": candidate_id, "system": critic_system, "user": critic_user, "schema": bp.critic_schema(),
    }], lock, prior, registry, metrics)[candidate_id]
    critic_response = critic_capture["response"]
    status_pass = bool(package) and bp.critic_passed(critic_response)
    reasons: list[str] = []
    if compile_error:
        reasons.append(compile_error.split(":", 1)[0])
    if not bp.critic_passed(critic_response):
        reasons.extend(item["code"] for item in critic_response.get("findings", []))
        if not reasons:
            reasons.append("critic-quarantine")
    reasons = bp.unique([re.sub(r"[^a-z0-9]+", "-", reason.lower()).strip("-") or "unspecified" for reason in reasons])

    if status_pass and package:
        provenance = bp.compile_provenance(
            candidate, package["family"], source_registry, lock["vocabularySource"],
            reviewed_at, lock_sha, critic_capture,
        )
        bp.validate(provenance, schemas["provenance"], registry, "provenance")
        family_dir = bp.PILOT / "families" / candidate_id.removeprefix("candidate2:")
        bp.write_json(family_dir / "family.json", package["family"])
        bp.write_json(family_dir / "analyses.json", package["analyses"])
        bp.write_json(family_dir / "provenance.json", provenance)
    else:
        bp.write_json(bp.PILOT / "quarantine" / (candidate_id.removeprefix("candidate2:") + ".json"), {
            "candidateId": candidate_id,
            "compilerResponse": compiler_response,
            "compiledArtifacts": package,
            "critic": critic_response,
            "reasonCodes": reasons,
        })
    bp.write_json(bp.PILOT / "critic-reports" / (candidate_id.removeprefix("candidate2:") + ".json"), critic_response)

    record = {
        "candidateId": candidate_id,
        "candidateClass": context["classHypothesis"],
        "compilerStatus": "compiled" if package else ("abstained" if compiler_response.get("status") == "abstain" else "deterministic-gate-failed"),
        "criticStatus": "passed" if bp.critic_passed(critic_response) else "quarantined",
        "pilotStatus": "passed" if status_pass else "quarantined",
        "familyId": package["family"]["familyId"] if package else None,
        "reasonCodes": reasons,
        "compilerResponseSha256": bp.sha(bp.canonical(compiler_response)),
        "criticResponseSha256": bp.sha(bp.canonical(critic_response)),
    }
    metrics["wallSeconds"] = time.monotonic() - started
    bp.write_json(bp.PILOT / "metrics.json", metrics)
    manifest = {
        "schemaVersion": 1,
        "githubRunId": os.environ.get("GITHUB_RUN_ID", "unknown"),
        "shardIndex": index,
        "selectionCandidateIds": selection_ids,
        "candidateBuildId": candidate_manifest["buildId"],
        "sourceDateEpoch": evidence_manifest["sourceDateEpoch"],
        "modelLockSha256": lock_sha,
        "record": record,
        "metrics": metrics,
    }
    bp.write_json(bp.PILOT / "manifest.json", manifest)
    prior.close()
    shutil.rmtree(bp.TMP, ignore_errors=True)
    print(json.dumps({
        "marker": "PILOT_SHARD_COMPLETE", "shardIndex": index, "candidateId": candidate_id,
        "pilotStatus": record["pilotStatus"], "modelCalls": metrics["modelCalls"], "cacheHits": metrics["cacheHits"],
    }, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    shard_index = int(os.environ.get("EXPRESSIONS2_PILOT_INDEX", "-1"))
    bp.PILOT = bp.ROOT / "pilot-shard"
    try:
        raise SystemExit(main())
    except (bp.PilotError, OSError, ValueError, ET.ParseError) as exc:
        shard_failure(shard_index, exc)
        print(f"PILOT_SHARD_FAILED index={shard_index} error={type(exc).__name__}", file=sys.stderr, flush=True)
        raise SystemExit(1)
