#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import gzip
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(args, cwd=ROOT, env=env, check=True)


def deterministic_bundle(target: Path, root_name: str) -> None:
    root = ROOT / root_name
    epoch = int(dt.datetime(2026, 10, 1, tzinfo=dt.timezone.utc).timestamp())
    with target.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path in sorted(item for item in root.rglob("*") if item.is_file()):
                    info = archive.gettarinfo(str(path), arcname=path.relative_to(ROOT).as_posix())
                    info.uid = 0; info.gid = 0; info.uname = ""; info.gname = ""; info.mtime = epoch
                    with path.open("rb") as stream:
                        archive.addfile(info, stream)


def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise SystemExit("GitHub Actions only")
    env = dict(os.environ)
    print("MODEL_SMOKE_STAGE_START", flush=True)
    run(sys.executable, "remote/smoke_models.py", env=env)
    tag = "expressions2-0.1.0-development-shadow"
    repository = os.environ["EXPRESSIONS2_REPOSITORY"]
    gh_env = dict(env); gh_env["GH_TOKEN"] = os.environ["GH_TOKEN"]
    bundle = Path("/tmp/expressions2-batch001-model-smoke.tar.gz")
    deterministic_bundle(bundle, "pilot-smoke")
    run("gh", "release", "upload", tag, str(bundle), "--repo", repository, "--clobber", env=gh_env)
    manifest = json.loads((ROOT / "pilot-smoke" / "manifest.json").read_text())
    print(json.dumps({"marker": "REMOTE_MODEL_SMOKE_COMPLETE", "smokeId": manifest["smokeId"]}, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
