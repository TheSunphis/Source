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


def deterministic_bundle(target: Path, roots: list[str], timestamp: str) -> None:
    epoch = int(dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00")).timestamp())
    with target.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for root_name in roots:
                    root = ROOT / root_name
                    if not root.exists():
                        continue
                    for path in sorted(item for item in root.rglob("*") if item.is_file()):
                        info = archive.gettarinfo(str(path), arcname=path.relative_to(ROOT).as_posix())
                        info.uid = 0
                        info.gid = 0
                        info.uname = ""
                        info.gname = ""
                        info.mtime = epoch
                        with path.open("rb") as stream:
                            archive.addfile(info, stream)


def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise SystemExit("GitHub Actions only")
    env = dict(os.environ)
    runtime = Path("/tmp/expressions2-runtime")
    run(
        sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", "--require-hashes",
        "--target", str(runtime), "-r", "runtime/requirements-linux-x86_64.lock", env=env,
    )
    env["PYTHONPATH"] = str(runtime)
    env["EXPRESSIONS2_RUNTIME"] = str(runtime)
    run(sys.executable, "tools/build_evidence_stores.py", env=env)
    run(sys.executable, "tools/run_contract_tests.py", env=env)
    run(sys.executable, "remote/build_candidates.py", env=env)

    tag = "expressions2-0.1.0-development-shadow"
    repository = os.environ["EXPRESSIONS2_REPOSITORY"]
    gh_env = dict(env)
    gh_env["GH_TOKEN"] = os.environ["GH_TOKEN"]
    prior_dir = Path("/tmp/expressions2-prior-pilot")
    prior_dir.mkdir(parents=True, exist_ok=True)
    prior_asset = prior_dir / "expressions2-batch001-pilot.tar.gz"
    download = subprocess.run(
        ["gh", "release", "download", tag, "--repo", repository, "--pattern", prior_asset.name, "--dir", str(prior_dir), "--clobber"],
        cwd=ROOT, env=gh_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if download.returncode == 0 and prior_asset.is_file():
        env["EXPRESSIONS2_PRIOR_PILOT"] = str(prior_asset)

    run(sys.executable, "remote/build_pilot.py", env=env)
    run(sys.executable, "tools/guard_clean_room.py", "--self-test", env=env)
    evidence_manifest = json.loads((ROOT / "evidence" / "manifest.json").read_text())
    bundle = Path("/tmp/expressions2-batch001-pilot.tar.gz")
    deterministic_bundle(bundle, ["evidence", "candidates", "snapshots", "source-registry", "vocabulary", "pilot"], evidence_manifest["sourceDateEpoch"])

    view = subprocess.run(["gh", "release", "view", tag, "--repo", repository], env=gh_env, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if view.returncode:
        run(
            "gh", "release", "create", tag, "--repo", repository, "--target", os.environ["EXPRESSIONS2_BRANCH"],
            "--title", "Expressions2 0.1.0-development shadow", "--notes", "Private commissioning artifacts. Not production.",
            "--draft", str(bundle), env=gh_env,
        )
    else:
        run("gh", "release", "upload", tag, str(bundle), "--repo", repository, "--clobber", env=gh_env)
    manifest = json.loads((ROOT / "pilot" / "manifest.json").read_text())
    print(json.dumps({"marker": "REMOTE_PILOT_STAGE_COMPLETE", "pilotId": manifest["pilotId"], "counts": manifest["counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
