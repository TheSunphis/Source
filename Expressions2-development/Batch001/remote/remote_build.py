#!/usr/bin/env python3
"""GitHub-hosted entrypoint for the Expressions2 shadow build.

This file is intentionally outside .github/workflows so it can be maintained
without changing the manually installed workflow. GitHub runner storage is
ephemeral; durable outputs must go to the Source development branch or an
unpublished draft release.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(*args: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(args, cwd=ROOT, env=env, check=True)

def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise SystemExit("remote_build.py may run only on a GitHub Actions runner")
    metadata_env = dict(os.environ)
    metadata_env["EXPRESSIONS2_EVIDENCE_MODE"] = "metadata-only"
    run(sys.executable, "tools/run_contract_tests.py", env=metadata_env)
    run(sys.executable, "tools/run_evidence_tests.py")
    run(sys.executable, "tools/guard_clean_room.py", "--self-test")
    print("REMOTE_BOOTSTRAP_PASS: Source-only GitHub runner is ready")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
