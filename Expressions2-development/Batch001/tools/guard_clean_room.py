#!/usr/bin/env python3
"""Fail closed when Expressions2 executable/data paths reference legacy Expressions."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".sh"}
DATA_DIRS = ["evidence", "candidates", "ledger", "compiled", "audits", "source-registry"]
# Constructed in pieces so the guard does not accuse its own source text.
BANNED_TEXT = (
    "src/data/" + "expressions",
    "backend/" + "expressions.py",
    "src/expressions/" + "app.js",
    "expression_" + "progress",
    "expressions-" + "legacy",
    "legacy/" + "expressions",
)
BANNED_KEYS = {"legacyid", "oldid", "previousid", "sourcefamilyid", "legacyfamilyid", "mappedlegacyid"}
FAMILY_ID = re.compile(r"^expression2:[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")


def scan_text(path: Path, text: str) -> list[str]:
    findings: list[str] = []
    normalized = text.replace("\\\\", "/")
    lowered = normalized.lower()
    for banned in BANNED_TEXT:
        if banned.lower() in lowered:
            findings.append(f"{path}: prohibited legacy reference {banned!r}")
    return findings


def compact_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def scan_json_value(path: Path, value: Any, pointer: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f"{pointer}/{key}"
            if compact_key(key) in BANNED_KEYS:
                findings.append(f"{path}{child_pointer}: prohibited legacy-lineage key")
            if key == "familyId" and child is not None and (not isinstance(child, str) or not FAMILY_ID.fullmatch(child)):
                findings.append(f"{path}{child_pointer}: family ID is not in the clean-room namespace")
            findings.extend(scan_json_value(path, child, child_pointer))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(scan_json_value(path, child, f"{pointer}/{index}"))
    elif isinstance(value, str):
        findings.extend(scan_text(Path(f"{path}{pointer}"), value))
    return findings


def scan_workspace() -> list[str]:
    findings: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_symlink():
            findings.append(f"{path}: symlinks are prohibited inside the clean-room workspace")
            continue
        if not path.is_file() or path.resolve() == SELF:
            continue
        if path.suffix.lower() in CODE_SUFFIXES:
            try:
                findings.extend(scan_text(path, path.read_text()))
            except UnicodeDecodeError:
                findings.append(f"{path}: executable source is not UTF-8 text")
    for directory in DATA_DIRS:
        root = ROOT / directory
        for path in sorted(root.rglob("*.json")):
            try:
                value = json.loads(path.read_text())
                findings.extend(scan_json_value(path, value))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                findings.append(f"{path}: unreadable JSON: {exc}")
    return findings


def self_test() -> list[str]:
    failures: list[str] = []
    clean_path = ROOT / "fixtures" / "guard" / "clean.py.fixture"
    forbidden_path = ROOT / "fixtures" / "guard" / "forbidden.py.fixture"
    if scan_text(clean_path, clean_path.read_text()):
        failures.append("clean guard fixture produced a false positive")
    findings = scan_text(forbidden_path, forbidden_path.read_text())
    if not findings:
        failures.append("forbidden guard fixture was not rejected")
    bad_json = {"familyId": "legacy-family-1", "legacyId": "anything"}
    if len(scan_json_value(Path("synthetic.json"), bad_json)) < 2:
        failures.append("legacy JSON identity fixture was not fully rejected")
    good_json = {"familyId": "expression2:00000000-0000-7000-8000-000000000001"}
    if scan_json_value(Path("synthetic.json"), good_json):
        failures.append("clean JSON identity fixture produced a false positive")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="also execute positive and negative guard fixtures")
    args = parser.parse_args()
    findings = scan_workspace()
    if args.self_test:
        findings.extend(f"self-test: {item}" for item in self_test())
    if findings:
        print(f"FAILED: clean-room guard found {len(findings)} issue(s)")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS: clean-room guard found no legacy import, lineage, namespace, or symlink violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
