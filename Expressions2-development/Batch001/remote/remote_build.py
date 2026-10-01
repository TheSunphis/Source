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
TAG = "expressions2-0.1.0-development-shadow"


def run(*args: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(args, cwd=ROOT, env=env, check=True)


def restore_checkpoint(archive_path: Path) -> None:
    allowed = ("evidence/", "candidates/")
    with tarfile.open(archive_path, "r:gz") as archive:
        members = [member for member in archive.getmembers() if member.isfile() and member.name.startswith(allowed)]
        if not members:
            raise RuntimeError("candidate checkpoint contains no private evidence/candidate files")
        for member in members:
            if member.issym() or member.islnk() or member.name.startswith("/") or ".." in Path(member.name).parts:
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


def download_release_asset(repository: str, name: str, directory: Path, env: dict[str, str], required: bool) -> Path | None:
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / name
    result = subprocess.run(
        ["gh", "release", "download", TAG, "--repo", repository, "--pattern", name, "--dir", str(directory), "--clobber"],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if result.returncode or not target.is_file():
        if required:
            raise RuntimeError(f"required private draft asset is unavailable: {name}")
        return None
    return target


def prepare(env: dict[str, str], repository: str, gh_env: dict[str, str]) -> str:
    print("PILOT_CHECKPOINT_RESTORE_START", flush=True)
    checkpoint = download_release_asset(
        repository, "expressions2-batch001-candidates.tar.gz", Path("/tmp/expressions2-checkpoint"), gh_env, True,
    )
    assert checkpoint is not None
    restore_checkpoint(checkpoint)
    frozen_id = json.loads((ROOT / "candidates" / "manifest.json").read_text())["buildId"]
    print(f"PILOT_CHECKPOINT_RESTORE_PASS candidateBuildId={frozen_id}", flush=True)

    print("PILOT_RUNTIME_INSTALL_START", flush=True)
    runtime = Path("/tmp/expressions2-runtime")
    run(
        sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", "--require-hashes",
        "--target", str(runtime), "-r", "runtime/requirements-linux-x86_64.lock", env=env,
    )
    env["PYTHONPATH"] = str(runtime)
    env["EXPRESSIONS2_RUNTIME"] = str(runtime)
    print("PILOT_CONTRACT_TESTS_START", flush=True)
    run(sys.executable, "tools/run_contract_tests.py", env=env)
    print("PILOT_CONTRACT_TESTS_PASS", flush=True)
    print("PILOT_DETERMINISTIC_REBUILD_START", flush=True)
    run(sys.executable, "remote/build_candidates.py", env=env)
    rebuilt_id = json.loads((ROOT / "candidates" / "manifest.json").read_text())["buildId"]
    if rebuilt_id != frozen_id:
        raise RuntimeError("candidate checkpoint deterministic rebuild mismatch")
    print(f"PILOT_DETERMINISTIC_REBUILD_PASS candidateBuildId={rebuilt_id}", flush=True)

    prior = download_release_asset(
        repository, "expressions2-batch001-pilot.tar.gz", Path("/tmp/expressions2-prior-pilot"), gh_env, False,
    )
    if prior:
        env["EXPRESSIONS2_PRIOR_PILOT"] = str(prior)
    return json.loads((ROOT / "evidence" / "manifest.json").read_text())["sourceDateEpoch"]


def shard_mode(env: dict[str, str], repository: str, gh_env: dict[str, str], source_date: str) -> int:
    index = int(os.environ["EXPRESSIONS2_PILOT_INDEX"])
    run_id = os.environ["EXPRESSIONS2_RUN_ID"]
    print(f"PILOT_SHARD_STAGE_START index={index}", flush=True)
    result = subprocess.run([sys.executable, "remote/build_pilot_shard.py"], cwd=ROOT, env=env)
    bundle = Path(f"/tmp/expressions2-batch001-pilot-run-{run_id}-shard-{index}.tar.gz")
    deterministic_bundle(bundle, ["pilot-shard"], source_date)
    run("gh", "release", "upload", TAG, str(bundle), "--repo", repository, "--clobber", env=gh_env)
    print(f"PILOT_SHARD_CHECKPOINT_STORED index={index} result={result.returncode}", flush=True)
    return result.returncode


def merge_mode(env: dict[str, str], repository: str, gh_env: dict[str, str], source_date: str) -> int:
    run_id = os.environ["EXPRESSIONS2_RUN_ID"]
    shard_dir = Path("/tmp/expressions2-pilot-shards")
    shard_dir.mkdir(parents=True, exist_ok=True)
    pattern = f"expressions2-batch001-pilot-run-{run_id}-shard-*.tar.gz"
    print("PILOT_MERGE_DOWNLOAD_START", flush=True)
    download = subprocess.run(
        ["gh", "release", "download", TAG, "--repo", repository, "--pattern", pattern, "--dir", str(shard_dir), "--clobber"],
        cwd=ROOT, env=gh_env,
    )
    if download.returncode:
        raise RuntimeError("private pilot shard checkpoints could not be downloaded")
    env["EXPRESSIONS2_SHARD_DIR"] = str(shard_dir)
    print("PILOT_MERGE_VALIDATION_START", flush=True)
    result = subprocess.run([sys.executable, "remote/merge_pilot_shards.py"], cwd=ROOT, env=env)
    manifest_path = ROOT / "pilot" / "manifest.json"
    if manifest_path.exists():
        run(sys.executable, "tools/guard_clean_room.py", "--self-test", env=env)
        bundle = Path("/tmp/expressions2-batch001-pilot.tar.gz")
        deterministic_bundle(
            bundle, ["evidence", "candidates", "snapshots", "source-registry", "vocabulary", "pilot"], source_date,
        )
        run("gh", "release", "upload", TAG, str(bundle), "--repo", repository, "--clobber", env=gh_env)
        manifest = json.loads(manifest_path.read_text())
        print(json.dumps({
            "marker": "REMOTE_PARALLEL_PILOT_COMPLETE", "pilotId": manifest["pilotId"], "counts": manifest["counts"],
        }, sort_keys=True), flush=True)
    return result.returncode


def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise SystemExit("GitHub Actions only")
    mode = os.environ.get("EXPRESSIONS2_MODE")
    if mode not in {"pilot-shard", "pilot-merge"}:
        raise SystemExit("EXPRESSIONS2_MODE must be pilot-shard or pilot-merge")
    env = dict(os.environ)
    repository = os.environ["EXPRESSIONS2_REPOSITORY"]
    gh_env = dict(env); gh_env["GH_TOKEN"] = os.environ["GH_TOKEN"]
    source_date = prepare(env, repository, gh_env)
    if mode == "pilot-shard":
        return shard_mode(env, repository, gh_env, source_date)
    return merge_mode(env, repository, gh_env, source_date)


if __name__ == "__main__":
    raise SystemExit(main())
