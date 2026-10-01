#!/usr/bin/env python3
"""Offline adapter and contamination tests for Expressions2 evidence stores."""
from __future__ import annotations

import bz2
import gzip
import io
import json
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

import build_evidence_stores as build


def source(source_id: str, permission: str = "redistributable") -> dict:
    return {"sourceId": source_id, "permissionClass": permission}


class EvidenceAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_tatoeba_cc0_filters_non_japanese_languages(self) -> None:
        payload = "1\teng\tNot Japanese\n2\tjpn\t日本語です。\n".encode()
        path = self.root / "cc0.tar.bz2"
        with tarfile.open(path, "w:bz2") as archive:
            info = tarfile.TarInfo("sentences_CC0.tsv")
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
        records = build.parse_tatoeba_cc0(path, source("source2:tatoeba-cc0"))
        self.assertEqual([item["locator"] for item in records], ["sentence:2"])
        self.assertEqual(records[0]["fields"]["text"], "日本語です。")

    def test_tatoeba_per_language_accepts_both_supported_shapes(self) -> None:
        path = self.root / "jpn.tsv.bz2"
        path.write_bytes(bz2.compress("3\tjpn\t表現です。\n4\t別の表現です。\n".encode()))
        records = build.parse_tatoeba_jpn(path, source("source2:tatoeba-japanese-ccby", "evidence-only"))
        self.assertEqual(len(records), 2)
        self.assertTrue(all(item["permissionClass"] == "evidence-only" for item in records))

    def test_wordnet_duplicate_rows_keep_unique_stable_locators(self) -> None:
        path = self.root / "wordnet.gz"
        path.write_bytes(gzip.compress("00000001-n\t表現\thand\n00000001-n\t表現\thand\n".encode(), mtime=0))
        records = build.parse_wordnet(path, source("source2:japanese-wordnet-ok", "tool-only"))
        self.assertEqual(len(records), 2)
        self.assertEqual(len({item["locator"] for item in records}), 2)
        self.assertEqual(len({item["evidenceId"] for item in records}), 2)

    def test_wiktionary_retains_identity_not_definition_or_quote_text(self) -> None:
        xml = """<mediawiki><page><title>猫の手も借りたい</title><ns>0</ns><id>10</id><revision><id>20</id><text>==日本語==\n{{ことわざ|ja}}\n# definition\n#: quotation</text></revision></page><page><title>普通語</title><ns>0</ns><id>11</id><revision><id>21</id><text>==日本語==\n# 成句という語を含むだけ</text></revision></page></mediawiki>"""
        path = self.root / "wiki.xml.bz2"
        path.write_bytes(bz2.compress(xml.encode()))
        records = build.parse_wiktionary(path, source("source2:japanese-wiktionary", "evidence-only"))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["fields"]["surface"], "猫の手も借りたい")
        self.assertFalse({"text", "definition", "quotation", "example"} & set(records[0]["fields"]))

    def test_jmdict_requires_expression_level_label(self) -> None:
        xml = """<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>お疲れ様</keb></k_ele><r_ele><reb>おつかれさま</reb></r_ele><sense><pos>expressions (phrases, clauses, etc.)</pos><gloss>thanks for your work</gloss></sense></entry><entry><ent_seq>2</ent_seq><k_ele><keb>普通語</keb></k_ele><r_ele><reb>ふつうご</reb></r_ele><sense><pos>noun</pos><gloss>ordinary word</gloss></sense></entry></JMdict>"""
        path = self.root / "jmdict.gz"
        path.write_bytes(gzip.compress(xml.encode(), mtime=0))
        records = build.parse_jmdict(path, source("source2:jmdict-english"))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["fields"]["surface"], "お疲れ様")

    def test_dictionary_inventory_never_extracts_members(self) -> None:
        path = self.root / "dict.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("dictionary/system.dic", b"binary")
            archive.writestr("LICENSE", b"notice")
        records = build.parse_dictionary_inventory(path, source("source2:sudachidict-core", "tool-only"))
        self.assertEqual(len(records), 2)
        self.assertFalse((self.root / "dictionary").exists())

    def test_contamination_audit_rejects_wiktionary_text(self) -> None:
        store = {"sourceId": "source2:japanese-wiktionary", "records": [{
            "locator": "page:1", "permissionClass": "evidence-only", "fields": {"definition": "copied"}
        }]}
        self.assertTrue(build.contamination_findings(store, "evidence-only"))

    def test_canonical_json_and_gzip_are_deterministic(self) -> None:
        value = {"b": 2, "a": "日本語"}
        first = build.compact_json(value)
        second = build.compact_json(value)
        self.assertEqual(first, second)
        self.assertEqual(gzip.compress(first, mtime=0), gzip.compress(second, mtime=0))
        self.assertEqual(json.loads(first), value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
