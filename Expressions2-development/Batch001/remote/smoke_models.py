#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import time
from pathlib import Path

from build_pilot import LOCK_PATH, ModelServer, TMP, canonical, read_json, sha, stable_id, write_json

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "pilot-smoke"
JAPANESE = re.compile(r"[ぁ-ゖァ-ヺ一-龯々〆ヵヶ]")


def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise SystemExit("GitHub Actions only")
    shutil.rmtree(OUTPUT, ignore_errors=True)
    shutil.rmtree(TMP, ignore_errors=True)
    OUTPUT.mkdir(parents=True)
    TMP.mkdir(parents=True)
    lock = read_json(LOCK_PATH)
    schema = {
        "type": "object", "additionalProperties": False, "required": ["status", "answer"],
        "properties": {"status": {"const": "ok"}, "answer": {"type": "string", "minLength": 1, "maxLength": 40, "pattern": "[ぁ-ゖァ-ヺ一-龯々〆ヵヶ]"}},
    }
    records = []
    for original in lock["models"]:
        spec = dict(original)
        spec["maxOutputTokens"] = 80
        spec["requestTimeoutSeconds"] = 180
        print(f"SMOKE_ROLE_START role={spec['role']}", flush=True)
        server = ModelServer(lock)
        model_path = None
        started = time.monotonic()
        try:
            model_path = server.start(spec)
            value, usage, inference_seconds = server.call(
                spec,
                "Return only the required JSON. This is an inference-path health check.",
                "Give a brief Japanese acknowledgement that the local model is responding.",
                schema,
            )
            print("SMOKE_RESPONSE " + json.dumps(value, ensure_ascii=False, sort_keys=True), flush=True)
            if value.get("status") != "ok" or not isinstance(value.get("answer"), str) or not value["answer"].strip():
                raise RuntimeError("structured smoke response failed envelope check")
            records.append({
                "role": spec["role"], "repository": spec["repository"], "revision": spec["revision"],
                "fileSha256": spec["sha256"], "status": "passed", "responseSha256": sha(canonical(value)),
                "usage": usage, "inferenceSeconds": round(inference_seconds, 3), "wallSeconds": round(time.monotonic() - started, 3),
            })
            print(f"SMOKE_ROLE_PASS role={spec['role']}", flush=True)
        finally:
            server.stop(model_path)
    body = {
        "schemaVersion": 1, "scope": "official-dual-open-model-infrastructure-smoke", "modelLockSha256": sha(canonical(lock)),
        "records": records, "weightsPersisted": False, "networkInference": False, "paidServices": False,
    }
    manifest = {"smokeId": stable_id("smoke2:", sha(canonical(body))), **body}
    write_json(OUTPUT / "manifest.json", manifest)
    shutil.rmtree(TMP, ignore_errors=True)
    print(json.dumps({"marker": "MODEL_SMOKE_PASS", "smokeId": manifest["smokeId"], "roles": len(records)}, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
