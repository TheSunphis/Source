#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import gzip
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(args, cwd=ROOT, env=env, check=True)


def restore_checkpoint(archive_path: Path) -> None:
    allowed = ("evidence/", "candidates/")
    with tarfile.open(archive_path, "r:gz") as archive:
        members = [member for member in archive.getmembers() if member.isfile() and member.name.startswith(allowed)]
        if not members:
            raise RuntimeError("candidate checkpoint contains no private evidence/candidate files")
        for member in members:
            if member.issym() or member.islnk() or ".." in Path(member.name).parts:
                raise RuntimeError("unsafe candidate checkpoint member")
            target = ROOT / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError("candidate checkpoint member is unreadable")
            with target.open("wb") as output:
                shutil.copyfileobj(source, output)


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
                        info.uid = 0; info.gid = 0; info.uname = ""; info.gname = ""; info.mtime = epoch
                        with path.open("rb") as stream:
                            archive.addfile(info, stream)


def download_release_asset(tag: str, repository: str, name: str, directory: Path, env: dict[str, str], required: bool) -> Path | None:
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / name
    result = subprocess.run(
        ["gh", "release", "download", tag, "--repo", repository, "--pattern", name, "--dir", str(directory), "--clobber"],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if result.returncode or not target.is_file():
        if required:
            raise RuntimeError(f"required private draft asset is unavailable: {name}")
        return None
    return target


def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise SystemExit("GitHub Actions only")
    env = dict(os.environ)
    tag = "expressions2-0.1.0-development-shadow"
    repository = os.environ["EXPRESSIONS2_REPOSITORY"]
    gh_env = dict(env); gh_env["GH_TOKEN"] = os.environ["GH_TOKEN"]

    checkpoint = download_release_asset(tag, repository, "expressions2-batch001-candidates.tar.gz", Path("/tmp/expressions2-checkpoint"), gh_env, True)
    assert checkpoint is not None
    restore_checkpoint(checkpoint)
    frozen_candidate_id = json.loads((ROOT / "candidates" / "manifest.json").read_text())["buildId"]

    runtime = Path("/tmp/expressions2-runtime")
    run(sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", "--require-hashes", "--target", str(runtime), "-r", "runtime/requirements-linux-x86_64.lock", env=env)
    env["PYTHONPATH"] = str(runtime)
    env["EXPRESSIONS2_RUNTIME"] = str(runtime)
    run(sys.executable, "tools/run_contract_tests.py", env=env)
    run(sys.executable, "remote/build_candidates.py", env=env)
    rebuilt_candidate_id = json.loads((ROOT / "candidates" / "manifest.json").read_text())["buildId"]
    if rebuilt_candidate_id != frozen_candidate_id:
        raise RuntimeError("candidate checkpoint deterministic rebuild mismatch")

    prior_asset = download_release_asset(tag, repository, "expressions2-batch001-pilot.tar.gz", Path("/tmp/expressions2-prior-pilot"), gh_env, False)
    if prior_asset:
        env["EXPRESSIONS2_PRIOR_PILOT"] = str(prior_asset)
    run(sys.executable, "remote/build_pilot.py", env=env)
    run(sys.executable, "tools/guard_clean_room.py", "--self-test", env=env)

    evidence_manifest = json.loads((ROOT / "evidence" / "manifest.json").read_text())
    bundle = Path("/tmp/expressions2-batch001-pilot.tar.gz")
    deterministic_bundle(bundle, ["evidence", "candidates", "snapshots", "source-registry", "vocabulary", "pilot"], evidence_manifest["sourceDateEpoch"])
    view = subprocess.run(["gh", "release", "view", tag, "--repo", repository], env=gh_env, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if view.returncode:
        run("gh", "release", "create", tag, "--repo", repository, "--target", os.environ["EXPRESSIONS2_BRANCH"], "--title", "Expressions2 0.1.0-development shadow", "--notes", "Private commissioning artifacts. Not production.", "--draft", str(bundle), env=gh_env)
    else:
        run("gh", "release", "upload", tag, str(bundle), "--repo", repository, "--clobber", env=gh_env)
    manifest = json.loads((ROOT / "pilot" / "manifest.json").read_text())
    print(json.dumps({"marker": "REMOTE_PILOT_STAGE_COMPLETE", "pilotId": manifest["pilotId"], "counts": manifest["counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
