#!/usr/bin/env python3
"""Stage 1 contract test suite for the clean-room Expressions2 factory."""
from __future__ import annotations

import copy
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

import guard_clean_room
import validate_contracts

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
POSITIVE = ROOT / "fixtures" / "contracts" / "positive"


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


class Stage1Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.family = validate_contracts.load_json(POSITIVE / "family.valid.json")
        cls.analysis = validate_contracts.load_json(POSITIVE / "form-analysis.valid.json")
        cls.runtime_card = validate_contracts.load_json(POSITIVE / "runtime-family-card.valid.json")
        cls.compiler = validate_contracts.load_json(POSITIVE / "compiler-manifest.valid.json")
        cls.ledger = validate_contracts.load_json(POSITIVE / "family-ledger.valid.json")
        cls.index = validate_contracts.load_json(POSITIVE / "runtime-library-index.valid.json")
        cls.registry = validate_contracts.load_json(POSITIVE / "source-registry.valid.json")

    def assertInvariantFails(self, name: str, value: dict) -> None:
        self.assertTrue(validate_contracts.invariant_errors(name, value), f"{name} mutation unexpectedly passed")

    def test_complete_validator(self) -> None:
        self.assertEqual(validate_contracts.main(), 0)

    def test_fixture_generation_is_deterministic(self) -> None:
        before = tree_hash(ROOT / "fixtures" / "contracts")
        subprocess.run([sys.executable, str(TOOLS / "generate_contract_fixtures.py")], check=True, cwd=ROOT.parents[1], capture_output=True)
        after = tree_hash(ROOT / "fixtures" / "contracts")
        self.assertEqual(before, after)

    def test_clean_room_guard_and_fixtures(self) -> None:
        self.assertEqual(guard_clean_room.scan_workspace(), [])
        self.assertEqual(guard_clean_room.self_test(), [])

    def test_family_primary_and_dynamic_counts_are_hard_invariants(self) -> None:
        value = copy.deepcopy(self.family)
        value["forms"].append(copy.deepcopy(value["forms"][0]))
        value["forms"][1]["formId"] = "second-primary"
        value["forms"][1]["analysisRef"] = "analysis2:" + "e" * 32
        self.assertInvariantFails("family", value)

    def test_analysis_reconstruction_is_hard_invariant(self) -> None:
        value = copy.deepcopy(self.analysis)
        value["segments"][0]["surface"] = "不一致"
        self.assertInvariantFails("form-analysis", value)

    def test_runtime_card_requires_exact_analysis_bijection(self) -> None:
        value = copy.deepcopy(self.runtime_card)
        value["analyses"] = []
        self.assertInvariantFails("runtime-family-card", value)

    def test_coverage_counts_sum_to_exactly_one_hundred(self) -> None:
        value = copy.deepcopy(self.compiler)
        value["coverage"]["difficultyCounts"]["1"] = 19
        self.assertInvariantFails("compiler-manifest", value)

    def test_ledger_is_contiguous_and_hash_chained(self) -> None:
        value = copy.deepcopy(self.ledger)
        value["events"][0]["sequence"] = 2
        self.assertInvariantFails("family-ledger", value)

    def test_runtime_totals_are_derived(self) -> None:
        value = copy.deepcopy(self.index)
        value["formCount"] = 101
        self.assertInvariantFails("runtime-library-index", value)

    def test_approved_source_requires_acquisition_url(self) -> None:
        value = copy.deepcopy(self.registry)
        value["sources"][0]["acquisitionUrl"] = None
        self.assertInvariantFails("source-registry", value)

    def test_legacy_json_lineage_and_namespace_are_rejected(self) -> None:
        bad = {"familyId": "old-family-123", "oldId": "former"}
        self.assertGreaterEqual(len(guard_clean_room.scan_json_value(Path("fixture.json"), bad)), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
