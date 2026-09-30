#!/usr/bin/env python3
"""Build a non-production Koto Expressions candidate shortlist from JMdict.

This importer does not create verified expression families. It extracts JMdict
entries whose effective part of speech includes `exp`, removes entries with no
current English expression sense, and orders the remaining pool for human
editorial triage. Difficulty and learner-facing Commonness are never assigned.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from lxml import etree
from wordfreq import zipf_frequency

EXP_POS = "expressions (phrases, clauses, etc.)"
NON_CURRENT = {
    "archaic",
    "obsolete term",
    "dated term",
    "historical term",
    "rare term",
    "poetical term",
}
SEARCH_ONLY_WRITING = "search-only kanji form"
SEARCH_ONLY_READING = "search-only kana form"
USUALLY_KANA = "word usually written using kana alone"
STRONG_PRIORITY = {"news1", "ichi1", "spec1", "gai1"}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def values(parent, path: str) -> list[str]:
    return [node.text for node in parent.findall(path) if node.text]


def unique(items) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def priority_tier(tags: list[str]) -> int:
    if any(tag in STRONG_PRIORITY for tag in tags):
        return 2
    if tags:
        return 1
    return 0


def form_sort_key(form: dict) -> tuple[int, int]:
    return (priority_tier(form["priority"]), -form["sourceOrder"])


def pick_primary(writings: list[dict], readings: list[dict], senses: list[dict]) -> dict:
    flags = {flag for sense in senses for flag in sense["miscellaneous"]}
    usable_writings = [item for item in writings if not item["searchOnly"]]
    usable_readings = [item for item in readings if not item["searchOnly"]]
    if not usable_readings:
        usable_readings = readings

    use_kana = USUALLY_KANA in flags or not usable_writings
    if use_kana:
        chosen_reading = max(usable_readings, key=form_sort_key)
        return {"japanese": chosen_reading["text"], "reading": chosen_reading["text"]}

    chosen_writing = max(usable_writings, key=form_sort_key)
    matching = [
        item for item in usable_readings
        if not item["restrictions"] or chosen_writing["text"] in item["restrictions"]
    ]
    chosen_reading = max(matching or usable_readings, key=form_sort_key)
    return {"japanese": chosen_writing["text"], "reading": chosen_reading["text"]}


def parse_entry(entry) -> tuple[dict | None, str]:
    sequence = int(entry.findtext("ent_seq"))
    writings = []
    for index, node in enumerate(entry.findall("k_ele")):
        information = unique(values(node, "ke_inf"))
        writings.append({
            "text": node.findtext("keb"),
            "information": information,
            "priority": unique(values(node, "ke_pri")),
            "searchOnly": SEARCH_ONLY_WRITING in information,
            "sourceOrder": index,
        })

    readings = []
    for index, node in enumerate(entry.findall("r_ele")):
        information = unique(values(node, "re_inf"))
        readings.append({
            "text": node.findtext("reb"),
            "noKanji": node.find("re_nokanji") is not None,
            "restrictions": unique(values(node, "re_restr")),
            "information": information,
            "priority": unique(values(node, "re_pri")),
            "searchOnly": SEARCH_ONLY_READING in information,
            "sourceOrder": index,
        })

    effective_pos: list[str] = []
    expression_senses = []
    for index, node in enumerate(entry.findall("sense"), start=1):
        explicit_pos = unique(values(node, "pos"))
        if explicit_pos:
            effective_pos = explicit_pos
        if EXP_POS not in effective_pos:
            continue
        miscellaneous = unique(values(node, "misc"))
        glosses = []
        for gloss in node.findall("gloss"):
            if not gloss.text:
                continue
            language = gloss.get(XML_LANG, "eng")
            if language != "eng":
                continue
            glosses.append({"text": gloss.text, "type": gloss.get("g_type")})
        expression_senses.append({
            "sourceSense": index,
            "current": not any(flag in NON_CURRENT for flag in miscellaneous),
            "appliesToWritings": unique(values(node, "stagk")),
            "appliesToReadings": unique(values(node, "stagr")),
            "partsOfSpeech": effective_pos.copy(),
            "fields": unique(values(node, "field")),
            "miscellaneous": miscellaneous,
            "dialects": unique(values(node, "dial")),
            "information": unique(values(node, "s_inf")),
            "related": unique(values(node, "xref")),
            "antonyms": unique(values(node, "ant")),
            "glosses": glosses,
        })

    if not expression_senses:
        return None, "not-expression"
    if not any(sense["current"] and sense["glosses"] for sense in expression_senses):
        return None, "no-current-english-sense"

    primary = pick_primary(writings, readings, expression_senses)
    priority = unique(
        tag for form in writings + readings for tag in form["priority"]
    )
    flags = unique(
        value
        for sense in expression_senses
        for value in sense["miscellaneous"] + sense["dialects"]
    )
    score_forms = unique([
        primary["japanese"],
        primary["reading"],
        *[item["text"] for item in writings if not item["searchOnly"]],
        *[item["text"] for item in readings if not item["searchOnly"]],
    ])
    internal_frequency = max(zipf_frequency(form, "ja") for form in score_forms)

    for item in writings + readings:
        item.pop("sourceOrder")

    record = {
        "candidateId": f"candidate:jmdict:{sequence}",
        "sourceId": "jmdict",
        "sourceSequence": sequence,
        "primary": primary,
        "writings": writings,
        "readings": readings,
        "senses": expression_senses,
        "sourcePriority": priority,
        "sourceFlags": flags,
        "editorial": {
            "status": "unreviewed-source-candidate",
            "familyDecision": None,
            "familyId": None,
            "difficulty": None,
            "notes": [],
            "productionEligible": False,
        },
    }
    # These signals only order the editorial queue and are never serialized.
    record["_selection"] = (
        priority_tier(priority),
        internal_frequency,
        1 if any(USUALLY_KANA in sense["miscellaneous"] for sense in expression_senses) else 0,
        -sequence,
    )
    return record, "eligible"


def write_json(path: Path, payload, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        if compact:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
        else:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--pack-size", type=int, default=250)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--source-last-modified", required=True)
    parser.add_argument("--retrieved-at")
    args = parser.parse_args()

    if args.target < 1 or args.pack_size < 1 or args.pack_size > 500:
        raise SystemExit("Target and pack size must be positive; pack size cannot exceed 500.")
    retrieved_at = args.retrieved_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_sha = digest(args.source)
    counters = Counter()
    misc_counts = Counter()
    dialect_counts = Counter()
    field_counts = Counter()
    candidates = []

    with gzip.open(args.source, "rb") as source:
        stream = etree.iterparse(
            source,
            events=("end",),
            tag="entry",
            load_dtd=True,
            resolve_entities=True,
            huge_tree=True,
        )
        for _, entry in stream:
            counters["jmdictEntries"] += 1
            record, result = parse_entry(entry)
            counters[result] += 1
            if record is not None:
                candidates.append(record)
                for sense in record["senses"]:
                    misc_counts.update(sense["miscellaneous"])
                    dialect_counts.update(sense["dialects"])
                    field_counts.update(sense["fields"])
            entry.clear()
            while entry.getprevious() is not None:
                del entry.getparent()[0]

    if len(candidates) < args.target:
        raise SystemExit(f"Only {len(candidates)} eligible candidates exist; target is {args.target}.")
    candidates.sort(key=lambda item: item["_selection"], reverse=True)
    selected = candidates[:args.target]
    for item in selected:
        item.pop("_selection")

    candidate_root = args.output / "candidates"
    pack_root = candidate_root / "packs"
    if pack_root.exists():
        shutil.rmtree(pack_root)
    pack_root.mkdir(parents=True, exist_ok=True)
    packs = []
    for offset in range(0, len(selected), args.pack_size):
        number = offset // args.pack_size + 1
        pack_id = f"jmdict-candidates-{number:03d}"
        records = selected[offset:offset + args.pack_size]
        payload = {
            "datasetId": "koto-expression-candidates",
            "schemaVersion": 1,
            "packId": pack_id,
            "sourceId": "jmdict",
            "candidateCount": len(records),
            "candidates": records,
        }
        relative = f"packs/{pack_id}.json"
        path = candidate_root / relative
        write_json(path, payload, compact=True)
        packs.append({
            "id": pack_id,
            "file": relative,
            "candidateCount": len(records),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        })

    source_snapshot = {
        "sourceId": "jmdict",
        "downloadUrl": args.source_url,
        "retrievedAt": retrieved_at,
        "lastModified": args.source_last_modified,
        "archiveBytes": args.source.stat().st_size,
        "archiveSha256": source_sha,
        "licence": "CC-BY-SA-4.0",
        "attribution": "Electronic Dictionary Research and Development Group (EDRDG), JMdict Japanese/English data",
        "licenceUrl": "https://www.edrdg.org/edrdg/licence.html",
    }
    manifest = {
        "datasetId": "koto-expression-candidates",
        "schemaVersion": 1,
        "generatedAt": retrieved_at,
        "publicationStatus": "non-production-candidates",
        "productionEligible": False,
        "candidateCount": len(selected),
        "packSize": args.pack_size,
        "sourceSnapshot": source_snapshot,
        "audit": {
            "jmdictEntryCount": counters["jmdictEntries"],
            "expressionTaggedEntryCount": counters["eligible"] + counters["no-current-english-sense"],
            "eligibleCurrentEntryCount": counters["eligible"],
            "excludedNoCurrentEnglishSenseCount": counters["no-current-english-sense"],
            "shortlistedCount": len(selected),
            "reserveEligibleCount": counters["eligible"] - len(selected),
        },
        "selectionMethod": [
            "Resolve inherited JMdict part-of-speech metadata and require an expression-tagged sense.",
            "Require at least one non-archaic, non-obsolete, non-dated, non-historical, non-rare, non-poetical English sense.",
            "Prioritize JMdict source-priority evidence, then use wordfreq only to order editorial review candidates.",
            "Do not assign Koto Difficulty, learner-facing Commonness, verification, or production eligibility automatically."
        ],
        "packs": packs,
    }
    write_json(candidate_root / "manifest.json", manifest)
    audit = {
        "datasetId": "koto-expression-candidate-audit",
        "schemaVersion": 1,
        "generatedAt": retrieved_at,
        "sourceSnapshot": source_snapshot,
        "counts": manifest["audit"],
        "topSourceFlags": [{"label": key, "count": value} for key, value in misc_counts.most_common(50)],
        "dialects": [{"label": key, "count": value} for key, value in dialect_counts.most_common()],
        "topFields": [{"label": key, "count": value} for key, value in field_counts.most_common(50)],
        "warning": "The shortlist is an editorial work queue, not a verified expression library. Candidate count must not be presented as production family count."
    }
    write_json(args.output / "audit" / "jmdict-20260930.audit.json", audit)
    print(json.dumps({
        "candidateCount": len(selected),
        "eligiblePool": counters["eligible"],
        "reserve": counters["eligible"] - len(selected),
        "packCount": len(packs),
        "packBytes": sum(item["bytes"] for item in packs),
        "sourceSha256": source_sha,
    }, indent=2))


if __name__ == "__main__":
    main()
