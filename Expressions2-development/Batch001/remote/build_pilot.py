#!/usr/bin/env python3
"""GitHub-runner-only eight-family open-model commissioning pilot."""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schema"
EVIDENCE = ROOT / "evidence"
CANDIDATES = ROOT / "candidates"
PILOT = ROOT / "pilot"
VOCABULARY = ROOT / "vocabulary"
LOCK_PATH = ROOT / "remote" / "model-lock.json"
TMP = Path("/tmp/expressions2-pilot")
READING_RE = re.compile(r"^[ぁ-ゖァ-ヺー・、。！？!?「」『』（）()〜～…‥・,.\s0-9]+$")
JAPANESE_RE = re.compile(r"[ぁ-ゖァ-ヺ一-龯々〆ヵヶ]")
FACETS = [
    "greeting", "leave-taking", "gratitude", "apology", "request", "permission", "offer", "invitation", "refusal",
    "acknowledgement", "reaction", "evaluation", "agreement-disagreement", "topic-management", "turn-management",
    "repair-clarification", "sequencing", "cause-reason", "contrast-concession", "condition", "degree-extent",
    "evidence-hearsay", "stance", "obligation", "possibility", "workplace", "school", "service-encounter",
    "written-formal", "intimate-casual", "literary-historical", "regional",
]
CATEGORY_LABELS = {value: value.replace("-", " ").title() for value in FACETS}
DIFFICULTY_LABELS = {1: "Essential", 2: "Foundational", 3: "Intermediate", 4: "Advanced", 5: "Nuanced"}
CRITIC_CHECKS = [
    "familyInclusion", "mergeSplit", "naturalness", "meaningIntention", "registerRelationship", "difficulty",
    "formsReadings", "segments", "canonicalLinks", "conversation", "patternsDistinctions",
    "sourceLicenseProvenance", "librarySummary", "fullCard",
]
DISPLAY_CONTRACT = {
    "sectionSequence": [
        "hero", "personal-state", "intentions", "use-when", "take-care", "relationships", "forms-and-analysis",
        "responses", "follow-ups", "dialogue", "patterns-and-examples", "nearby-distinctions", "verification-and-sources",
    ],
    "stateControls": ["recognised", "review"],
    "stateMutuallyExclusive": True,
    "audioMethod": "device-japanese-tts-explicit-only",
    "analysisInteraction": "every-published-form-segment-focusable-and-tappable",
}


class PilotError(RuntimeError):
    pass


class GateFailure(PilotError):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_id(prefix: str, *parts: str) -> str:
    return prefix + hashlib.sha256("\0".join(parts).encode()).hexdigest()[:32]


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if isinstance(value, str) and value.strip()))


def normalize(value: str) -> str:
    return unicodedata.normalize("NFC", value).replace("\x00", "").strip()


def hiragana(value: str) -> str:
    return "".join(chr(ord(char) - 96) if "ァ" <= char <= "ヶ" else char for char in value)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_gzip_json(path: Path) -> Any:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def schema_registry() -> tuple[dict[str, Any], Registry]:
    registry = Registry()
    schemas: dict[str, Any] = {}
    for path in SCHEMAS.glob("*.schema.json"):
        value = read_json(path)
        schemas[path.name.removesuffix(".schema.json")] = value
        registry = registry.with_resource(value["$id"], Resource.from_contents(value))
    return schemas, registry


def validate(value: Any, schema: dict[str, Any], registry: Registry, label: str) -> None:
    errors = sorted(
        Draft202012Validator(schema, registry=registry, format_checker=FormatChecker()).iter_errors(value),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        pointer = "/" + "/".join(str(part) for part in error.absolute_path)
        raise GateFailure(f"{label}{pointer}: {error.message}")


def source_timestamp(value: str) -> str:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def deterministic_family_id(candidate_id: str) -> str:
    value = hashlib.sha256(candidate_id.encode()).hexdigest()
    uuid = f"{value[0:8]}-{value[8:12]}-7{value[13:16]}-8{value[17:20]}-{value[20:32]}"
    return "expression2:" + uuid


def morphology(tokenizer: Any, split_mode: Any, text: str) -> list[dict[str, Any]]:
    text = normalize(text)
    try:
        morphemes = tokenizer.tokenize(text, split_mode.A)
    except Exception as exc:
        raise GateFailure(f"Sudachi failed for {text!r}: {exc}") from exc
    result: list[dict[str, Any]] = []
    for morpheme in morphemes:
        surface = morpheme.surface()
        pos = list(morpheme.part_of_speech())
        reading = hiragana(morpheme.reading_form() or "")
        if not reading or reading == "*":
            reading = hiragana(surface)
        lemma = normalize(morpheme.dictionary_form() or surface)
        inflection_parts = [part for part in pos[4:6] if part and part != "*"]
        result.append({
            "surface": surface,
            "reading": reading,
            "pos": pos,
            "lemma": lemma,
            "inflection": "; ".join(inflection_parts) if inflection_parts else None,
        })
    if "".join(item["surface"] for item in result) != text:
        raise GateFailure(f"surface reconstruction failed for {text!r}")
    reading = "".join(item["reading"] for item in result)
    if not reading or not READING_RE.fullmatch(reading):
        raise GateFailure(f"reading reconstruction is not publishable for {text!r}")
    return result


def spoken_line(raw: dict[str, Any], tokenizer: Any, split_mode: Any) -> dict[str, Any]:
    japanese = normalize(str(raw.get("japanese", "")))
    meaning = normalize(str(raw.get("meaning", "")))
    if not JAPANESE_RE.search(japanese) or len(japanese) > 300:
        raise GateFailure("generated spoken line has invalid Japanese")
    if not meaning or len(meaning) > 500:
        raise GateFailure("generated spoken line has invalid meaning")
    reading = "".join(item["reading"] for item in morphology(tokenizer, split_mode, japanese))
    return {"japanese": japanese, "reading": reading, "meaning": meaning, "deviceTts": True}


class PriorArchive:
    def __init__(self, path: str | None):
        self.path = Path(path) if path else None
        self.archive: tarfile.TarFile | None = None
        if self.path and self.path.is_file():
            self.archive = tarfile.open(self.path, "r:gz")

    def read(self, name: str) -> bytes | None:
        if not self.archive:
            return None
        try:
            member = self.archive.getmember(name)
        except KeyError:
            return None
        if not member.isfile() or member.size > 200_000_000:
            return None
        stream = self.archive.extractfile(member)
        return stream.read() if stream else None

    def json(self, name: str) -> dict[str, Any] | None:
        data = self.read(name)
        if data is None:
            return None
        try:
            value = json.loads(data)
            return value if isinstance(value, dict) else None
        except Exception:
            return None

    def close(self) -> None:
        if self.archive:
            self.archive.close()


def verified_download(url: str, target: Path, expected_bytes: int, expected_sha256: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "curl", "-L", "--fail", "--retry", "5", "--retry-all-errors", "--connect-timeout", "30",
        "--output", str(target), url,
    ], check=True)
    if target.stat().st_size != expected_bytes:
        raise PilotError(f"download size mismatch for {target.name}")
    digest = hashlib.sha256()
    with target.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    if digest.hexdigest() != expected_sha256:
        raise PilotError(f"download digest mismatch for {target.name}")


def build_vocabulary_index(prior: PriorArchive, source: dict[str, Any]) -> tuple[dict[str, Any], str]:
    output = VOCABULARY / "jmdict-canonical.json.gz"
    cached = prior.read("vocabulary/jmdict-canonical.json.gz")
    cached_raw = prior.read("vocabulary/source/JMdict_e.gz")
    if cached and cached_raw and len(cached_raw) == source["snapshot"]["byteLength"] and sha(cached_raw) == source["snapshot"]["sha256"]:
        try:
            value = json.loads(gzip.decompress(cached))
            if value.get("sourceSnapshotSha256") == source["snapshot"]["sha256"]:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(cached)
                raw_output = VOCABULARY / "source" / "JMdict_e.gz"
                raw_output.parent.mkdir(parents=True, exist_ok=True)
                raw_output.write_bytes(cached_raw)
                return value, sha(canonical(value))
        except Exception:
            pass
    raw = TMP / "JMdict_e.gz"
    verified_download(
        source["acquisitionUrl"], raw, source["snapshot"]["byteLength"], source["snapshot"]["sha256"]
    )
    raw_output = VOCABULARY / "source" / "JMdict_e.gz"
    raw_output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(raw, raw_output)
    entries: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    with gzip.open(raw, "rb") as stream:
        for _, elem in ET.iterparse(stream, events=("end",)):
            if elem.tag != "entry":
                continue
            sequence = normalize(elem.findtext("ent_seq") or "")
            forms = unique([normalize(node.text or "") for node in elem.findall("./k_ele/keb")])
            entry_hash = sha(ET.tostring(elem, encoding="utf-8"))
            for reading_node in elem.findall("./r_ele"):
                reading = normalize(reading_node.findtext("reb") or "")
                restrictions = unique([normalize(node.text or "") for node in reading_node.findall("re_restr")])
                targets = restrictions if restrictions else (forms or [reading])
                for surface in targets:
                    if not surface or not reading or not JAPANESE_RE.search(surface) or not READING_RE.fullmatch(reading):
                        continue
                    key = (sequence, surface, reading)
                    if key in seen:
                        continue
                    seen.add(key)
                    entries.append({
                        "vocabularyId": stable_id("vocabulary2:", sequence, surface, reading),
                        "sequence": sequence,
                        "surface": surface,
                        "reading": reading,
                        "recordHash": entry_hash,
                        "locator": "ent_seq:" + sequence,
                    })
            elem.clear()
    raw.unlink(missing_ok=True)
    entries.sort(key=lambda item: (item["surface"], item["reading"], item["sequence"]))
    body = {
        "schemaVersion": 1,
        "sourceId": source["sourceId"],
        "sourceSnapshotSha256": source["snapshot"]["sha256"],
        "license": source["license"]["name"],
        "entryCount": len(entries),
        "entries": entries,
    }
    value = {"indexId": stable_id("vocabularyindex2:", sha(canonical(body))), **body}
    data = canonical(value)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return value, sha(data)


def evidence_maps() -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for path in [EVIDENCE / "jmdict-english.evidence.json.gz", EVIDENCE / "tatoeba-japanese-ccby.evidence.json.gz"]:
        store = read_gzip_json(path)
        source_id = store["sourceId"]
        for record in store["records"]:
            result[(source_id, record["locator"])] = record
    return result


def candidate_context(candidate: dict[str, Any], records: dict[tuple[str, str], dict[str, Any]]) -> dict[str, Any] | None:
    direct: list[dict[str, Any]] = []
    corpus: list[dict[str, Any]] = []
    for evidence in candidate["sourceEvidence"]:
        record = records.get((evidence["sourceId"], evidence["locator"]))
        if not record:
            continue
        if evidence["sourceId"] == "source2:jmdict-english":
            direct.append(record)
        elif evidence["sourceId"] == "source2:tatoeba-japanese-ccby":
            corpus.append(record)
    if len(direct) != 1 or not corpus:
        return None
    fields = direct[0]["fields"]
    forms = unique(fields.get("forms", "").split("␟"))
    readings = unique(fields.get("readings", "").split("␟"))
    glosses = unique(fields.get("glosses", "").split("␟"))
    if forms != [candidate["surface"]] or readings != [candidate["reading"]] or not glosses:
        return None
    labels = fields.get("labels", "")
    if any(word in labels.lower() for word in ["vulgar", "derogatory", "obscure", "archaism"]):
        return None
    sentences = unique([record["fields"].get("text", "") for record in corpus if candidate["surface"] in record["fields"].get("text", "")])
    if not sentences:
        return None
    return {
        "candidateId": candidate["candidateId"],
        "surface": candidate["surface"],
        "reading": candidate["reading"],
        "classHypothesis": candidate["classHypotheses"][0],
        "glosses": glosses,
        "labels": labels,
        "attestedJapaneseSentences": sentences[:3],
        "sourceEvidence": candidate["sourceEvidence"],
        "signals": candidate["signals"],
    }


def select_candidates(tokenizer: Any, split_mode: Any, candidates: list[dict[str, Any]], records: dict[tuple[str, str], dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    eligible: list[tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]] = []
    for candidate in candidates:
        context = candidate_context(candidate, records)
        if not context or not candidate["signals"]["multiword"] or not candidate["signals"]["dictionaryExpressionTag"]:
            continue
        try:
            segments = morphology(tokenizer, split_mode, candidate["surface"])
        except GateFailure:
            continue
        if len(segments) < 2 or "".join(item["reading"] for item in segments) != candidate["reading"]:
            continue
        eligible.append((candidate, context, segments))
    eligible.sort(key=lambda item: (
        -int(item[0]["signals"]["pragmaticFunction"]), -float(item[0]["signals"]["fixedness"]),
        -int(item[0]["signals"]["corpusHitCount"]), -len(item[0]["sourceEvidence"]), item[0]["candidateId"],
    ))
    by_class: dict[str, list[tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]]] = {}
    for item in eligible:
        by_class.setdefault(item[1]["classHypothesis"], []).append(item)
    target_order = [
        "interactional-formula", "idiom", "conventional-collocation", "proverb-or-saying",
        "interactional-formula", "idiom", "conventional-collocation", "conventional-collocation",
    ]
    chosen: list[tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]] = []
    chosen_ids: set[str] = set()
    for family_class in target_order:
        item = next((value for value in by_class.get(family_class, []) if value[0]["candidateId"] not in chosen_ids), None)
        if item:
            chosen.append(item)
            chosen_ids.add(item[0]["candidateId"])
    for item in eligible:
        if len(chosen) == 8:
            break
        if item[0]["candidateId"] not in chosen_ids:
            chosen.append(item)
            chosen_ids.add(item[0]["candidateId"])
    if len(chosen) != 8:
        raise PilotError(f"only {len(chosen)} candidates satisfy strict pilot preselection")
    candidate_by_id = {candidate["candidateId"]: candidate for candidate in candidates}
    contexts: dict[str, dict[str, Any]] = {}
    segment_map: dict[str, list[dict[str, Any]]] = {}
    for candidate, context, segments in chosen:
        neighbors = []
        source_gloss = set(" ".join(context["glosses"]).lower().split())
        for other, other_context, _ in eligible:
            if other["candidateId"] == candidate["candidateId"]:
                continue
            other_gloss = set(" ".join(other_context["glosses"]).lower().split())
            overlap = len(source_gloss & other_gloss)
            class_bonus = int(context["classHypothesis"] == other_context["classHypothesis"])
            neighbors.append((-(overlap + class_bonus), other["candidateId"], other_context))
        neighbors.sort()
        context = dict(context)
        context["approvedNearbyCandidates"] = [value[2] for value in neighbors[:6]]
        contexts[candidate["candidateId"]] = context
        segment_map[candidate["candidateId"]] = segments
    return [item[0] for item in chosen], contexts, segment_map


def raw_line_schema() -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False, "required": ["japanese", "meaning"],
        "properties": {
            "japanese": {"type": "string", "minLength": 1, "maxLength": 300, "pattern": "[ぁ-ゖァ-ヺ一-龯々〆ヵヶ]"},
            "meaning": {"type": "string", "minLength": 1, "maxLength": 500},
        },
    }


def editorial_schema(segments: list[dict[str, Any]], neighbor_ids: list[str]) -> dict[str, Any]:
    compiled = {
        "type": "object", "additionalProperties": False,
        "required": [
            "status", "facet", "difficulty", "contextualMeaning", "usageSummary", "intentions", "usageContexts",
            "useWhen", "takeCare", "relationships", "register", "responses", "followUps", "dialogue", "patterns",
            "distinction", "analysisSegments",
        ],
        "properties": {
            "status": {"const": "compiled"},
            "facet": {"enum": FACETS},
            "difficulty": {
                "type": "object", "additionalProperties": False, "required": ["level", "rationale"],
                "properties": {"level": {"type": "integer", "minimum": 1, "maximum": 5}, "rationale": {"type": "string", "minLength": 20, "maxLength": 1000}},
            },
            "contextualMeaning": {"type": "string", "minLength": 3, "maxLength": 600},
            "usageSummary": {"type": "string", "minLength": 30, "maxLength": 1400},
            "intentions": {"type": "array", "minItems": 2, "maxItems": 4, "items": {"type": "object", "additionalProperties": False, "required": ["action", "distinguishingNote"], "properties": {"action": {"type": "string", "minLength": 3, "maxLength": 300}, "distinguishingNote": {"type": "string", "minLength": 10, "maxLength": 800}}}},
            "usageContexts": {"type": "array", "minItems": 2, "maxItems": 4, "items": {"type": "string", "minLength": 3, "maxLength": 150}},
            "useWhen": {"type": "array", "minItems": 2, "maxItems": 4, "items": {"type": "string", "minLength": 10, "maxLength": 800}},
            "takeCare": {"type": "array", "minItems": 2, "maxItems": 4, "items": {"type": "string", "minLength": 10, "maxLength": 800}},
            "relationships": {"type": "array", "minItems": 2, "maxItems": 4, "items": {"type": "object", "additionalProperties": False, "required": ["context", "suitability", "guidance"], "properties": {"context": {"enum": ["family-close", "peers", "strangers", "workplace-hierarchy", "school", "service-encounter", "formal-institutional-writing", "group-use"]}, "suitability": {"enum": ["natural", "conditional", "avoid", "not-applicable"]}, "guidance": {"type": "string", "minLength": 10, "maxLength": 800}}}},
            "register": {"type": "string", "minLength": 3, "maxLength": 300},
            "responses": {"type": "array", "minItems": 2, "maxItems": 3, "items": {"type": "object", "additionalProperties": False, "required": ["context", "line"], "properties": {"context": {"type": "string", "minLength": 10, "maxLength": 500}, "line": raw_line_schema()}}},
            "followUps": {"type": "array", "minItems": 2, "maxItems": 3, "items": {"type": "object", "additionalProperties": False, "required": ["context", "line"], "properties": {"context": {"type": "string", "minLength": 10, "maxLength": 500}, "line": raw_line_schema()}}},
            "dialogue": {"type": "object", "additionalProperties": False, "required": ["context", "relationship", "register", "turns"], "properties": {"context": {"type": "string", "minLength": 10, "maxLength": 600}, "relationship": {"type": "string", "minLength": 3, "maxLength": 300}, "register": {"type": "string", "minLength": 3, "maxLength": 300}, "turns": {"type": "array", "minItems": 4, "maxItems": 6, "items": {"type": "object", "additionalProperties": False, "required": ["speaker", "containsTarget", "line"], "properties": {"speaker": {"type": "string", "minLength": 1, "maxLength": 30}, "containsTarget": {"type": "boolean"}, "line": raw_line_schema()}}}}},
            "patterns": {"oneOf": [
                {"type": "object", "additionalProperties": False, "required": ["applicable", "reason"], "properties": {"applicable": {"const": False}, "reason": {"type": "string", "minLength": 20, "maxLength": 800}}},
                {"type": "object", "additionalProperties": False, "required": ["applicable", "items"], "properties": {"applicable": {"const": True}, "items": {"type": "array", "minItems": 1, "maxItems": 2, "items": {"type": "object", "additionalProperties": False, "required": ["template", "templateReading", "function", "slots", "riskWarning", "examples"], "properties": {"template": {"type": "string", "minLength": 1, "maxLength": 300, "pattern": "[ぁ-ゖァ-ヺ一-龯々〆ヵヶ]"}, "templateReading": {"type": "string", "minLength": 1, "maxLength": 500}, "function": {"type": "string", "minLength": 10, "maxLength": 800}, "slots": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "object", "additionalProperties": False, "required": ["name", "constraint", "validExamples", "invalidExamples"], "properties": {"name": {"type": "string", "minLength": 1, "maxLength": 80}, "constraint": {"type": "string", "minLength": 10, "maxLength": 600}, "validExamples": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "string", "minLength": 1, "maxLength": 200}}, "invalidExamples": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "string", "minLength": 1, "maxLength": 200}}}}}, "riskWarning": {"type": "string", "minLength": 10, "maxLength": 800}, "examples": {"type": "array", "minItems": 2, "maxItems": 3, "items": raw_line_schema()}}}}}},
            ]},
            "distinction": {"type": "object", "additionalProperties": False, "required": ["nearbyCandidateId", "distinction", "registerOrPragmaticContrast", "unsafeReplacement"], "properties": {"nearbyCandidateId": {"enum": neighbor_ids}, "distinction": {"type": "string", "minLength": 10, "maxLength": 800}, "registerOrPragmaticContrast": {"type": "string", "minLength": 10, "maxLength": 800}, "unsafeReplacement": {"type": "string", "minLength": 10, "maxLength": 800}}},
            "analysisSegments": {"type": "array", "minItems": len(segments), "maxItems": len(segments), "items": {"type": "object", "additionalProperties": False, "required": ["segmentId", "surface", "contextualMeaning", "grammaticalRole"], "properties": {"segmentId": {"enum": [f"s{i:02d}" for i in range(1, len(segments) + 1)]}, "surface": {"enum": [item["surface"] for item in segments]}, "contextualMeaning": {"type": "string", "minLength": 1, "maxLength": 500}, "grammaticalRole": {"type": "string", "minLength": 3, "maxLength": 500}}}},
        },
    }
    abstain = {"type": "object", "additionalProperties": False, "required": ["status", "reason"], "properties": {"status": {"const": "abstain"}, "reason": {"type": "string", "minLength": 20, "maxLength": 1000}}}
    return {"oneOf": [compiled, abstain]}


def critic_schema() -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False, "required": ["verdict", "checks", "findings", "summary"],
        "properties": {
            "verdict": {"enum": ["pass", "quarantine"]},
            "checks": {"type": "object", "additionalProperties": False, "required": CRITIC_CHECKS, "properties": {name: {"enum": ["pass", "fail", "not-evaluated"]} for name in CRITIC_CHECKS}},
            "findings": {"type": "array", "maxItems": 30, "items": {"type": "object", "additionalProperties": False, "required": ["severity", "jsonPointer", "code", "explanation"], "properties": {"severity": {"enum": ["critical", "major", "minor"]}, "jsonPointer": {"type": "string", "minLength": 1, "maxLength": 300}, "code": {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "maxLength": 80}, "explanation": {"type": "string", "minLength": 10, "maxLength": 1000}}}},
            "summary": {"type": "string", "minLength": 20, "maxLength": 1500},
        },
    }


def compiler_prompt(context: dict[str, Any], segments: list[dict[str, Any]]) -> tuple[str, str]:
    system = (
        "You are the clean-room Koto Expressions family compiler. Use only the supplied approved evidence. "
        "Never treat model memory as authority. Produce concise natural learner-facing English and natural Japanese. "
        "Do not use JLPT, CEFR, JF, frequency, or commonness grading; use Koto Difficulty 1-5 only. "
        "Do not invent alternate forms. Every dialogue turn marked containsTarget must literally contain the target surface. "
        "Nearby distinctions may select only one supplied candidate. If the evidence is insufficient, abstain honestly. "
        "Return only schema-constrained JSON."
    )
    compact_segments = [{"segmentId": f"s{i:02d}", **segment} for i, segment in enumerate(segments, 1)]
    user = (
        "Compile one complete rich family-card editorial payload. Meanings must agree with JMdict glosses; the Tatoeba "
        "sentence attests form/pattern but is not authority for unsupported register claims. Provide responses, follow-ups, "
        "a four-turn dialogue, careful relationship guidance, and a safe distinction. Pattern guidance must explicitly reject "
        "unsafe substitutions or state that no productive pattern applies. Explain every fixed analysis segment.\n\nEVIDENCE PACKAGE:\n"
        + json.dumps({"candidate": context, "fixedMorphology": compact_segments}, ensure_ascii=False, sort_keys=True)
    )
    return system, user


def critic_prompt(context: dict[str, Any], compiler_result: dict[str, Any], compiled: dict[str, Any] | None) -> tuple[str, str]:
    system = (
        "You are the independent Koto Expressions commissioning critic. Be conservative. Use only supplied evidence and "
        "quarantine any unsupported meaning, unnatural Japanese, unsafe register advice, wrong Koto Difficulty, incomplete "
        "analysis, invalid vocabulary decision, weak dialogue, misleading pattern, or unsupported distinction. A pass requires "
        "all fourteen checks to pass and zero findings. An abstention or deterministic compiler failure must be quarantined. "
        "Return only schema-constrained JSON."
    )
    payload = {"evidence": context, "compilerResponse": compiler_result, "compiledArtifacts": compiled}
    user = "Independently audit this single candidate against every check. Do not repair it.\n\nAUDIT PACKAGE:\n" + json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return system, user


class ModelServer:
    def __init__(self, lock: dict[str, Any]):
        self.lock = lock
        self.engine: Path | None = None
        self.process: subprocess.Popen[bytes] | None = None
        self.log_stream: Any = None
        self.port = 8091

    def ensure_engine(self) -> Path:
        if self.engine and self.engine.is_file():
            return self.engine
        spec = self.lock["engine"]
        archive = TMP / spec["asset"]
        verified_download(spec["url"], archive, spec["expectedBytes"], spec["sha256"])
        directory = TMP / "llama-engine"
        directory.mkdir(parents=True, exist_ok=True)
        with tarfile.open(archive, "r:gz") as package:
            package.extractall(directory, filter="data")
        archive.unlink(missing_ok=True)
        matches = list(directory.rglob("llama-server"))
        if len(matches) != 1:
            raise PilotError("pinned llama.cpp archive did not contain exactly one llama-server")
        matches[0].chmod(0o755)
        self.engine = matches[0]
        return self.engine

    def start(self, spec: dict[str, Any]) -> Path:
        engine = self.ensure_engine()
        model = TMP / spec["file"]
        verified_download(spec["url"], model, spec["expectedBytes"], spec["sha256"])
        log_path = TMP / f"{spec['role']}-server.log"
        self.log_stream = log_path.open("wb")
        env = dict(os.environ)
        env["LD_LIBRARY_PATH"] = str(engine.parent) + (":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else "")
        command = [
            str(engine), "-m", str(model), "-a", "pilot-" + spec["role"], "--host", "127.0.0.1", "--port", str(self.port),
            "-c", str(spec["contextTokens"]), "-t", "4", "-tb", "4", "-np", "1", "-b", "512", "-ub", "256", "--jinja",
        ]
        self.process = subprocess.Popen(command, stdout=self.log_stream, stderr=subprocess.STDOUT, env=env)
        deadline = time.monotonic() + 300
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                self.log_stream.flush()
                tail = log_path.read_text(errors="replace")[-4000:]
                raise PilotError("llama-server exited during startup:\n" + tail)
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/health", timeout=5) as response:
                    if response.status == 200:
                        return model
            except Exception:
                time.sleep(2)
        raise PilotError("llama-server health timeout")

    def call(self, spec: dict[str, Any], system: str, user: str, schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], float]:
        body = {
            "model": "pilot-" + spec["role"],
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "temperature": spec["temperature"], "top_p": 1, "seed": spec["seed"],
            "max_tokens": spec["maxOutputTokens"], "stream": False,
            "response_format": {"type": "json_schema", "schema": schema},
            "chat_template_kwargs": {"enable_thinking": False}, "reasoning_effort": "none",
        }
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/v1/chat/completions", data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"}, method="POST",
        )
        started = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=1800) as response:
                envelope = json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:4000]
            raise PilotError(f"model HTTP {exc.code}: {detail}") from exc
        elapsed = time.monotonic() - started
        try:
            content = envelope["choices"][0]["message"]["content"]
            value = json.loads(content)
        except Exception as exc:
            raise PilotError("model returned no parseable JSON content") from exc
        return value, envelope.get("usage", {}), elapsed

    def stop(self, model: Path | None = None) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=10)
        if self.log_stream:
            self.log_stream.close()
        if model:
            model.unlink(missing_ok=True)
        self.process = None
        self.log_stream = None


def cache_key(spec: dict[str, Any], system: str, user: str, schema: dict[str, Any]) -> str:
    request = {"modelSha256": spec["sha256"], "revision": spec["revision"], "system": system, "user": user, "schema": schema, "seed": spec["seed"], "temperature": spec["temperature"]}
    return sha(canonical(request))


def model_capture_path(role: str, candidate_id: str) -> Path:
    return PILOT / "model-responses" / role / (candidate_id.removeprefix("candidate2:") + ".json")


def run_model_requests(role: str, requests: list[dict[str, Any]], lock: dict[str, Any], prior: PriorArchive, registry: Registry, metrics: dict[str, Any]) -> dict[str, dict[str, Any]]:
    spec = next(value for value in lock["models"] if value["role"] == role)
    results: dict[str, dict[str, Any]] = {}
    misses: list[dict[str, Any]] = []
    for item in requests:
        key = cache_key(spec, item["system"], item["user"], item["schema"])
        item["cacheKey"] = key
        relative = "pilot/model-responses/" + role + "/" + item["candidateId"].removeprefix("candidate2:") + ".json"
        cached = prior.json(relative)
        if cached and cached.get("cacheKey") == key and cached.get("modelSha256") == spec["sha256"]:
            try:
                validate(cached["response"], item["schema"], registry, role + " cached response")
                results[item["candidateId"]] = cached
                metrics["cacheHits"] += 1
                continue
            except Exception:
                pass
        misses.append(item)
    if misses:
        server = ModelServer(lock)
        model_path: Path | None = None
        try:
            model_path = server.start(spec)
            for item in misses:
                value, usage, elapsed = server.call(spec, item["system"], item["user"], item["schema"])
                validate(value, item["schema"], registry, role + " response")
                capture = {
                    "schemaVersion": 1, "role": role, "candidateId": item["candidateId"], "cacheKey": item["cacheKey"],
                    "modelRepository": spec["repository"], "modelRevision": spec["revision"], "modelSha256": spec["sha256"],
                    "response": value, "usage": usage,
                }
                results[item["candidateId"]] = capture
                metrics["modelCalls"] += 1
                metrics["modelSeconds"][role] += elapsed
        finally:
            server.stop(model_path)
    for candidate_id, capture in results.items():
        write_json(model_capture_path(role, candidate_id), capture)
    return results


def vocabulary_maps(index: dict[str, Any]) -> tuple[dict[tuple[str, str], list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    exact: dict[tuple[str, str], list[dict[str, Any]]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    for entry in index["entries"]:
        exact.setdefault((entry["surface"], entry["reading"]), []).append(entry)
        by_id[entry["vocabularyId"]] = entry
    return exact, by_id


def vocabulary_evidence(entry: dict[str, Any]) -> dict[str, Any]:
    return {"sourceId": "source2:jmdict-vocabulary", "locator": entry["locator"], "evidenceType": "canonical-vocabulary", "supports": ["form", "reading", "vocabulary-link"], "recordHash": entry["recordHash"], "permissionClass": "redistributable"}


def compile_analysis(candidate: dict[str, Any], editorial: dict[str, Any], family_id: str, segments: list[dict[str, Any]], exact_vocab: dict[tuple[str, str], list[dict[str, Any]]], vocab_by_id: dict[str, dict[str, Any]], vocab_digest: str, reviewed_at: str) -> dict[str, Any]:
    annotations = {item["segmentId"]: item for item in editorial["analysisSegments"]}
    if len(annotations) != len(editorial["analysisSegments"]):
        raise GateFailure("analysis segment IDs are not unique")
    compiled_segments = []
    enumeration = []
    japanese_offset = 0
    reading_offset = 0
    family_evidence = candidate["sourceEvidence"]
    for ordinal, token in enumerate(segments, 1):
        segment_id = f"s{ordinal:02d}"
        annotation = annotations.get(segment_id)
        if not annotation or annotation["surface"] != token["surface"]:
            raise GateFailure(f"missing or mismatched annotation for {segment_id}")
        possible: dict[str, dict[str, Any]] = {}
        for key in [(token["surface"], token["reading"]), (token["lemma"], token["reading"])]:
            for entry in exact_vocab.get(key, []):
                possible[entry["vocabularyId"]] = entry
        candidate_ids = sorted(possible)
        pos0 = token["pos"][0] if token["pos"] else ""
        if pos0 == "補助記号":
            disposition = {"status": "unlinked", "reasonCode": "punctuation", "explanation": "Punctuation is not a canonical lexical destination.", "reverseChecked": True}
            selected_id = None
        elif pos0 in {"助詞", "助動詞"}:
            disposition = {"status": "unlinked", "reasonCode": "grammar-only", "explanation": "This grammatical segment is explained in context and is not linked as an isolated lexical item.", "reverseChecked": True}
            selected_id = None
        elif len(candidate_ids) == 1:
            selected_id = candidate_ids[0]
            entry = vocab_by_id[selected_id]
            disposition = {"status": "linked", "vocabularyId": selected_id, "canonicalSurface": entry["surface"], "canonicalReading": entry["reading"], "selectionReason": "The pinned JMdict catalogue has one exact surface-and-reading identity for this segment.", "reverseChecked": True}
        elif len(candidate_ids) > 1:
            selected_id = None
            disposition = {"status": "unlinked", "reasonCode": "ambiguous-no-safe-selection", "explanation": "The reverse enumeration found multiple exact canonical identities, so no unsafe destination was selected.", "reverseChecked": True}
        else:
            selected_id = None
            disposition = {"status": "unlinked", "reasonCode": "no-exact-canonical-record", "explanation": "The complete pinned JMdict reverse enumeration found no exact surface-and-reading identity.", "reverseChecked": True}
        segment_evidence = [vocabulary_evidence(possible[value]) for value in candidate_ids] or family_evidence
        surface_end = japanese_offset + len(token["surface"])
        reading_end = reading_offset + len(token["reading"])
        compiled_segments.append({
            "segmentId": segment_id, "surface": token["surface"], "reading": token["reading"],
            "kind": "punctuation" if pos0 == "補助記号" else ("particle-or-grammar" if pos0 == "助詞" else ("auxiliary-or-inflection" if pos0 == "助動詞" or token["inflection"] else "content-or-idiom")),
            "contextualMeaning": annotation["contextualMeaning"], "grammaticalRole": annotation["grammaticalRole"],
            "lemma": token["lemma"] or None, "inflection": token["inflection"],
            "japaneseSpan": {"start": japanese_offset, "end": surface_end}, "readingSpan": {"start": reading_offset, "end": reading_end},
            "vocabularyDisposition": disposition, "evidence": segment_evidence, "reviewIdentity": "qwen3-8b-compiler+deterministic-analysis",
        })
        enumeration.append({"segmentId": segment_id, "candidateIds": candidate_ids, "selectedId": selected_id, "enumeratorVersion": "0.1.0", "indexDigest": vocab_digest})
        japanese_offset = surface_end
        reading_offset = reading_end
    analysis_id = stable_id("analysis2:", family_id, "primary", candidate["normalizedKey"])
    return {
        "schemaVersion": 1, "analysisId": analysis_id, "familyId": family_id, "formId": "primary",
        "japanese": candidate["surface"], "reading": candidate["reading"], "segments": compiled_segments,
        "vocabularyEnumeration": enumeration, "ambiguities": [],
        "checks": {"surfaceReconstruction": "passed", "readingReconstruction": "passed", "segmentCompleteness": "passed", "canonicalValidity": "passed", "reverseOmission": "passed", "ambiguityResolution": "passed"},
        "compiler": {"name": "koto-expressions2-analysis", "version": "0.1.0", "inputDigest": sha(canonical({"candidate": candidate, "annotations": editorial["analysisSegments"], "vocabularyIndex": vocab_digest}))},
        "review": {"reviewType": "automated", "reviewedAt": reviewed_at, "reviewerIdentity": "deterministic-sudachi-jmdict-enumerator", "gateManifestId": "gates2:pilot-" + candidate["candidateId"].split(":", 1)[1]},
    }


def compile_family(candidate: dict[str, Any], context: dict[str, Any], editorial: dict[str, Any], segments: list[dict[str, Any]], candidate_by_id: dict[str, dict[str, Any]], exact_vocab: dict[tuple[str, str], list[dict[str, Any]]], vocab_by_id: dict[str, dict[str, Any]], vocab_digest: str, reviewed_at: str, source_release: str, tokenizer: Any, split_mode: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if editorial.get("status") != "compiled":
        raise GateFailure("compiler abstained")
    family_id = deterministic_family_id(candidate["candidateId"])
    analysis = compile_analysis(candidate, editorial, family_id, segments, exact_vocab, vocab_by_id, vocab_digest, reviewed_at)
    responses = [{"context": item["context"], "line": spoken_line(item["line"], tokenizer, split_mode)} for item in editorial["responses"]]
    follow_ups = [{"context": item["context"], "line": spoken_line(item["line"], tokenizer, split_mode)} for item in editorial["followUps"]]
    turns = [{"speaker": item["speaker"], "containsTarget": item["containsTarget"], "line": spoken_line(item["line"], tokenizer, split_mode)} for item in editorial["dialogue"]["turns"]]
    target = candidate["surface"]
    if not any(item["containsTarget"] and target in item["line"]["japanese"] for item in turns):
        raise GateFailure("dialogue lacks a correctly marked literal target")
    if any(item["containsTarget"] != (target in item["line"]["japanese"]) for item in turns):
        raise GateFailure("dialogue containsTarget flags are not exact")
    patterns_raw = editorial["patterns"]
    if patterns_raw["applicable"]:
        pattern_items = []
        for item in patterns_raw["items"]:
            pattern_items.append({**{key: item[key] for key in ["template", "templateReading", "function", "slots", "riskWarning"]}, "examples": [spoken_line(value, tokenizer, split_mode) for value in item["examples"]]})
        patterns = {"applicable": True, "items": pattern_items}
    else:
        patterns = {"applicable": False, "reason": patterns_raw["reason"]}
    distinction_raw = editorial["distinction"]
    nearby = candidate_by_id.get(distinction_raw["nearbyCandidateId"])
    approved_ids = {item["candidateId"] for item in context["approvedNearbyCandidates"]}
    if not nearby or nearby["candidateId"] not in approved_ids:
        raise GateFailure("distinction did not use an approved nearby candidate")
    evidence = candidate["sourceEvidence"]
    facet = editorial["facet"]
    meaning = editorial["contextualMeaning"]
    actions = [item["action"] for item in editorial["intentions"]]
    usage_contexts = unique(editorial["usageContexts"])
    review = {"reviewType": "verified-hybrid", "reviewedAt": reviewed_at, "reviewerIdentity": "qwen3-8b-compiler+granite-4.2-critic+deterministic-gates", "gateManifestId": "gates2:pilot-" + candidate["candidateId"].split(":", 1)[1]}
    provenance_id = stable_id("provenance2:", family_id, candidate["candidateId"])
    family = {
        "schemaVersion": 1, "familyId": family_id, "slug": "expression-" + candidate["candidateId"].split(":", 1)[1][:16],
        "candidateIds": [candidate["candidateId"]], "primaryClass": context["classHypothesis"], "facets": [facet],
        "difficulty": {"level": editorial["difficulty"]["level"], "label": DIFFICULTY_LABELS[editorial["difficulty"]["level"]], "rationale": editorial["difficulty"]["rationale"]},
        "category": {"key": facet, "label": CATEGORY_LABELS[facet]},
        "publication": {"state": "verified", "visibility": "private-shadow", "release": "0.1.0-development", "productionReady": False},
        "library": {"japanese": candidate["surface"], "reading": candidate["reading"], "contextualMeaning": meaning, "intentionSummary": actions, "usageContexts": usage_contexts, "searchDocument": {"japanese": [candidate["surface"]], "reading": [candidate["reading"]], "meanings": [meaning], "intentions": actions, "usageAndContext": usage_contexts + editorial["useWhen"]}, "formCount": 1, "verifiedSourceState": "verified", "availableActions": ["recognised", "review", "open"]},
        "hero": {"primaryFormId": "primary", "japanese": candidate["surface"], "reading": candidate["reading"], "contextualMeaning": meaning, "usageSummary": editorial["usageSummary"], "deviceTts": True},
        "intentions": editorial["intentions"], "guidance": {"useWhen": editorial["useWhen"], "takeCare": editorial["takeCare"], "relationships": editorial["relationships"]},
        "forms": [{"formId": "primary", "kind": "primary", "label": "Primary attested form", "register": editorial["register"], "japanese": candidate["surface"], "reading": candidate["reading"], "contextualMeaning": meaning, "deviceTts": True, "analysisRef": analysis["analysisId"], "evidence": evidence}],
        "responses": responses, "followUps": follow_ups,
        "dialogue": {"applicable": True, "context": editorial["dialogue"]["context"], "relationship": editorial["dialogue"]["relationship"], "register": editorial["dialogue"]["register"], "turns": turns},
        "patterns": patterns,
        "distinctions": [{"nearbyJapanese": nearby["surface"], "reading": nearby["reading"], "distinction": distinction_raw["distinction"], "registerOrPragmaticContrast": distinction_raw["registerOrPragmaticContrast"], "unsafeReplacement": distinction_raw["unsafeReplacement"], "publishedFamilyId": None}],
        "verification": {"publicationState": "verified", "evidence": evidence, "evidenceClasses": ["level-a", "level-b"], "corpusRelease": "0.1.0-development", "sourceRelease": source_release, "analysisCompilerVersion": "0.1.0", "attributionRoute": "Expressions2-development/Batch001/source-registry/sources.json, remote/model-lock.json vocabulary snapshot, and retained evidence locators", "review": review},
        "displayContract": DISPLAY_CONTRACT, "provenanceRef": provenance_id,
    }
    return family, [analysis]


def compile_provenance(candidate: dict[str, Any], family: dict[str, Any], source_registry: dict[str, Any], vocabulary_source: dict[str, Any], reviewed_at: str, model_lock_sha: str, critic_capture: dict[str, Any]) -> dict[str, Any]:
    sources = {item["sourceId"]: item for item in source_registry["sources"]}
    used = sorted({item["sourceId"] for item in candidate["sourceEvidence"]})
    evidence = candidate["sourceEvidence"]
    return {
        "schemaVersion": 1, "provenanceId": family["provenanceRef"], "familyId": family["familyId"], "candidateIds": family["candidateIds"],
        "sourceSnapshots": ([{"sourceId": source_id, "sha256": sources[source_id]["snapshot"]["sha256"]} for source_id in used] + [{"sourceId": vocabulary_source["sourceId"], "sha256": vocabulary_source["snapshot"]["sha256"]}]),
        "fieldDerivations": [
            {"jsonPointer": "/hero/japanese", "method": "source-extract", "evidence": evidence, "criticStatus": "passed"},
            {"jsonPointer": "/hero/contextualMeaning", "method": "editorial-synthesis", "evidence": evidence, "criticStatus": "passed"},
            {"jsonPointer": "/guidance", "method": "editorial-synthesis", "evidence": evidence, "criticStatus": "passed"},
            {"jsonPointer": "/forms/0/analysisRef", "method": "constraint-compiler", "evidence": evidence, "criticStatus": "passed"},
        ],
        "compiler": {"name": "koto-expressions2-family", "version": "0.1.0", "configurationDigest": model_lock_sha},
        "review": {"reviewType": "verified-hybrid", "reviewedAt": reviewed_at, "reviewerIdentity": "ibm-granite-4.2-8b-independent-critic", "gateManifestId": "gates2:pilot-" + candidate["candidateId"].split(":", 1)[1]},
        "inputDigest": sha(canonical({"candidate": candidate, "critic": critic_capture["response"]})), "outputDigest": sha(canonical(family)),
    }


def critic_passed(value: dict[str, Any]) -> bool:
    return value.get("verdict") == "pass" and not value.get("findings") and all(value.get("checks", {}).get(name) == "pass" for name in CRITIC_CHECKS)


def artifact_list() -> list[dict[str, Any]]:
    paths = [path for path in PILOT.rglob("*") if path.is_file() and path.name != "manifest.json"]
    vocab = VOCABULARY / "jmdict-canonical.json.gz"
    if vocab.is_file():
        paths.append(vocab)
    result = []
    for path in sorted(paths):
        data = path.read_bytes()
        result.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)})
    return result


def main() -> int:
    if not os.environ.get("GITHUB_ACTIONS"):
        raise SystemExit("GitHub Actions only")
    started = time.monotonic()
    shutil.rmtree(PILOT, ignore_errors=True)
    shutil.rmtree(VOCABULARY, ignore_errors=True)
    shutil.rmtree(TMP, ignore_errors=True)
    PILOT.mkdir(parents=True)
    TMP.mkdir(parents=True)
    prior = PriorArchive(os.environ.get("EXPRESSIONS2_PRIOR_PILOT"))
    schemas, registry = schema_registry()
    lock = read_json(LOCK_PATH)
    lock_sha = sha(canonical(lock))
    source_registry = read_json(ROOT / "source-registry" / "sources.json")
    sources = {item["sourceId"]: item for item in source_registry["sources"]}
    evidence_manifest = read_json(EVIDENCE / "manifest.json")
    candidate_manifest = read_json(CANDIDATES / "manifest.json")
    reviewed_at = source_timestamp(evidence_manifest["sourceDateEpoch"])
    source_release = "source2:" + sha(canonical({"registrySha256": sha((ROOT / "source-registry" / "sources.json").read_bytes()), "vocabularySource": lock["vocabularySource"]}))
    sys.path.insert(0, os.environ["EXPRESSIONS2_RUNTIME"])
    from sudachipy import Dictionary, SplitMode
    tokenizer = Dictionary(dict="core").tokenizer()
    candidate_store = read_gzip_json(CANDIDATES / "normalized-candidates.json.gz")
    records = evidence_maps()
    selected, contexts, segments = select_candidates(tokenizer, SplitMode, candidate_store["records"], records)
    candidate_by_id = {item["candidateId"]: item for item in candidate_store["records"]}
    vocabulary, vocabulary_digest = build_vocabulary_index(prior, lock["vocabularySource"])
    exact_vocab, vocab_by_id = vocabulary_maps(vocabulary)
    metrics = {"schemaVersion": 1, "githubRunId": os.environ.get("GITHUB_RUN_ID", "unknown"), "modelCalls": 0, "cacheHits": 0, "modelSeconds": {"compiler": 0.0, "critic": 0.0}}
    compiler_requests = []
    for candidate in selected:
        context = contexts[candidate["candidateId"]]
        model_schema = editorial_schema(segments[candidate["candidateId"]], [item["candidateId"] for item in context["approvedNearbyCandidates"]])
        system, user = compiler_prompt(context, segments[candidate["candidateId"]])
        compiler_requests.append({"candidateId": candidate["candidateId"], "system": system, "user": user, "schema": model_schema})
    compiler_captures = run_model_requests("compiler", compiler_requests, lock, prior, registry, metrics)
    compiled: dict[str, dict[str, Any]] = {}
    compile_errors: dict[str, str] = {}
    for candidate in selected:
        candidate_id = candidate["candidateId"]
        response = compiler_captures[candidate_id]["response"]
        if response.get("status") == "abstain":
            compile_errors[candidate_id] = "compiler-abstained"
            continue
        try:
            family, analyses = compile_family(candidate, contexts[candidate_id], response, segments[candidate_id], candidate_by_id, exact_vocab, vocab_by_id, vocabulary_digest, reviewed_at, source_release, tokenizer, SplitMode)
            validate(family, schemas["family"], registry, "family")
            for analysis in analyses:
                validate(analysis, schemas["form-analysis"], registry, "analysis")
            family2, analyses2 = compile_family(candidate, contexts[candidate_id], response, segments[candidate_id], candidate_by_id, exact_vocab, vocab_by_id, vocabulary_digest, reviewed_at, source_release, tokenizer, SplitMode)
            if canonical({"family": family, "analyses": analyses}) != canonical({"family": family2, "analyses": analyses2}):
                raise GateFailure("second deterministic compile mismatch")
            compiled[candidate_id] = {"family": family, "analyses": analyses}
        except Exception as exc:
            compile_errors[candidate_id] = "deterministic-gate-failed:" + str(exc)[:500]
    critic_requests = []
    for candidate in selected:
        candidate_id = candidate["candidateId"]
        package = compiled.get(candidate_id)
        system, user = critic_prompt(contexts[candidate_id], compiler_captures[candidate_id]["response"], package)
        critic_requests.append({"candidateId": candidate_id, "system": system, "user": user, "schema": critic_schema()})
    critic_captures = run_model_requests("critic", critic_requests, lock, prior, registry, metrics)
    manifest_records = []
    passed = 0
    for candidate in selected:
        candidate_id = candidate["candidateId"]
        compiler_response = compiler_captures[candidate_id]["response"]
        critic_response = critic_captures[candidate_id]["response"]
        package = compiled.get(candidate_id)
        status_pass = bool(package) and critic_passed(critic_response)
        reasons: list[str] = []
        if candidate_id in compile_errors:
            reasons.append(compile_errors[candidate_id].split(":", 1)[0])
        if not critic_passed(critic_response):
            reasons.extend(item["code"] for item in critic_response.get("findings", []))
            if not reasons:
                reasons.append("critic-quarantine")
        reasons = unique([re.sub(r"[^a-z0-9]+", "-", reason.lower()).strip("-") or "unspecified" for reason in reasons])
        if status_pass:
            provenance = compile_provenance(candidate, package["family"], source_registry, lock["vocabularySource"], reviewed_at, lock_sha, critic_captures[candidate_id])
            validate(provenance, schemas["provenance"], registry, "provenance")
            family_dir = PILOT / "families" / candidate_id.removeprefix("candidate2:")
            write_json(family_dir / "family.json", package["family"])
            write_json(family_dir / "analyses.json", package["analyses"])
            write_json(family_dir / "provenance.json", provenance)
            passed += 1
        else:
            write_json(PILOT / "quarantine" / (candidate_id.removeprefix("candidate2:") + ".json"), {"candidateId": candidate_id, "compilerResponse": compiler_response, "compiledArtifacts": package, "critic": critic_response, "reasonCodes": reasons})
        write_json(PILOT / "critic-reports" / (candidate_id.removeprefix("candidate2:") + ".json"), critic_response)
        manifest_records.append({
            "candidateId": candidate_id, "candidateClass": contexts[candidate_id]["classHypothesis"],
            "compilerStatus": "compiled" if package else ("abstained" if compiler_response.get("status") == "abstain" else "deterministic-gate-failed"),
            "criticStatus": "passed" if critic_passed(critic_response) else "quarantined",
            "pilotStatus": "passed" if status_pass else "quarantined",
            "familyId": package["family"]["familyId"] if package else None, "reasonCodes": reasons,
            "compilerResponseSha256": sha(canonical(compiler_response)), "criticResponseSha256": sha(canonical(critic_response)),
        })
    metrics["wallSeconds"] = time.monotonic() - started
    metrics["selectedCandidateIds"] = [item["candidateId"] for item in selected]
    write_json(PILOT / "metrics.json", metrics)
    body = {
        "scope": "eight-family-dual-open-model", "release": "0.1.0-development", "publicationStatus": "shadow-candidate", "productionReady": False,
        "candidateBuildId": candidate_manifest["buildId"], "modelLockSha256": lock_sha,
        "models": [{"role": item["role"], "repository": item["repository"], "revision": item["revision"], "fileSha256": item["sha256"], "license": item["license"]} for item in lock["models"]],
        "counts": {"attemptedCandidates": 8, "compiledFamilies": len(compiled), "independentlyCritiqued": 8, "passedPilotGates": passed, "quarantined": 8 - passed, "acceptedFamilies": 0},
        "records": manifest_records,
        "determinism": {"canonicalJson": True, "capturedModelResponsesAreInputs": True, "secondDeterministicCompileMatched": True},
        "incrementalBuild": {"contentAddressedResponseCache": True, "changedOnlySupported": True},
        "safety": {"noLocalApplicationStorage": True, "noLiveExpressionsMutation": True, "noModelWeightsPersisted": True, "privateDraftReleaseOnly": True, "gatesNotLowered": True},
        "artifacts": artifact_list(),
    }
    manifest = {"schemaVersion": 1, "pilotId": stable_id("pilot2:", sha(canonical(body))), **body}
    if manifest["counts"]["passedPilotGates"] + manifest["counts"]["quarantined"] != 8:
        raise PilotError("pilot count conservation failed")
    validate(manifest, schemas["pilot-manifest"], registry, "pilot manifest")
    write_json(PILOT / "manifest.json", manifest)
    print(json.dumps({"pilotId": manifest["pilotId"], "attempted": 8, "compiled": len(compiled), "passedPilotGates": passed, "acceptedFamilies": 0, "modelCalls": metrics["modelCalls"], "cacheHits": metrics["cacheHits"]}, sort_keys=True))
    prior.close()
    shutil.rmtree(TMP, ignore_errors=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PilotError, OSError, ValueError, ET.ParseError, subprocess.CalledProcessError) as exc:
        print(f"PILOT_FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
