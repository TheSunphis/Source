#!/usr/bin/env python3
"""Deterministically triage every immutable Expressions source candidate.

The output is an editorial navigation aid. It never verifies, publishes, assigns
Difficulty, or silently changes a source candidate.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPRESSIONS = ROOT / "Expressions"
CANDIDATES = EXPRESSIONS / "candidates"
TRIAGE = EXPRESSIONS / "triage"
GENERATED_AT = "2026-09-30T07:20:00Z"

SOCIAL_GLOSS = (
    "thank", "sorry", "apolog", "excuse me", "welcome", "congrat", "good night",
    "nice to meet", "how are you", "take care", "see you", "goodbye", "certainly",
    "no problem", "you’re welcome", "you're welcome",
)
REQUEST_GLOSS = ("please", "request", "may i", "would you", "won't you", "shall i", "shall we")
INTERACTION_GLOSS = (
    "i see", "is that so", "really", "what's the matter", "what is the matter",
    "wait", "once more", "understood", "all right", "are you ok", "are you okay",
)
HIGH_RISK_FLAGS = {
    "archaic": "archaic",
    "dated term": "dated",
    "vulgar expression or word": "vulgar",
    "derogatory": "derogatory",
    "slang": "slang",
    "Internet slang": "internet-slang",
    "female term or language": "gendered-language",
    "male term or language": "gendered-language",
    "children's language": "child-language",
    "Kansai-ben": "regional-language",
    "Osaka-ben": "regional-language",
    "Kyoto-ben": "regional-language",
    "Ryuukyuu-ben": "regional-language",
    "Kyuushuu-ben": "regional-language",
    "Touhoku-ben": "regional-language",
}
STRONG_PRIORITY = {"ichi1", "news1", "spec1", "gai1"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assignments() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted((EXPRESSIONS / "editorial" / "decisions").glob("*.json")):
        decision = load(path)
        for candidate_id in decision["mergedCandidates"]:
            if candidate_id in result:
                raise SystemExit(f"Candidate assigned twice: {candidate_id}")
            result[candidate_id] = decision["familyId"]
    return result


def dispositions() -> dict[str, str]:
    """Return committed non-assignment outcomes, never heuristic rejections."""
    result: dict[str, str] = {}
    for path in sorted((EXPRESSIONS / "editorial" / "decisions").glob("*.json")):
        decision = load(path)
        for related in decision["relatedCandidatesNotMerged"]:
            candidate_id = related["candidateId"]
            if candidate_id in result:
                raise SystemExit(f"Candidate disposition recorded twice: {candidate_id}")
            result[candidate_id] = decision["decisionId"]
    for path in sorted((EXPRESSIONS / "editorial" / "outcomes").glob("*.json")):
        outcome = load(path)
        candidate_id = outcome["candidateId"]
        if candidate_id in result:
            raise SystemExit(f"Candidate disposition recorded twice: {candidate_id}")
        result[candidate_id] = outcome["outcomeId"]
    return result


def gloss_text(candidate: dict) -> str:
    return " ".join(
        gloss["text"].lower()
        for sense in candidate["senses"]
        if sense["current"]
        for gloss in sense["glosses"]
    )


def category(candidate: dict, gloss: str) -> str:
    flags = set(candidate["sourceFlags"])
    poses = {pos for sense in candidate["senses"] for pos in sense["partsOfSpeech"]}
    japanese = candidate["primary"]["japanese"]
    if "proverb" in flags:
        return "proverb"
    if any(token in gloss for token in SOCIAL_GLOSS):
        return "social-formula"
    if any(token in gloss for token in REQUEST_GLOSS):
        return "request-or-response"
    if any(token in gloss for token in INTERACTION_GLOSS):
        return "interaction-management"
    if "idiomatic expression" in flags:
        return "idiom"
    if "particle" in poses or "auxiliary" in poses or (
        len(japanese) <= 7 and japanese[:1] in "にはのでとからまでより"
    ):
        return "grammar-pattern"
    return "other-expression"


def triage(candidate: dict, assigned: dict[str, str], dispositioned: dict[str, str]) -> dict:
    gloss = gloss_text(candidate)
    flags = set(candidate["sourceFlags"])
    poses = {pos for sense in candidate["senses"] for pos in sense["partsOfSpeech"]}
    score = 40
    signals: list[str] = []
    risk_flags = sorted({HIGH_RISK_FLAGS[flag] for flag in flags if flag in HIGH_RISK_FLAGS})

    priorities = set(candidate["sourcePriority"])
    if priorities & STRONG_PRIORITY:
        score += 20
        signals.append("strong-source-priority")
    elif priorities:
        score += 8
        signals.append("source-priority")
    if "interjection (kandoushi)" in poses:
        score += 15
        signals.append("interjection")
    if flags & {"polite (teineigo) language", "honorific or respectful (sonkeigo) language", "humble (kenjougo) language"}:
        score += 12
        signals.append("register-marked")
    if "idiomatic expression" in flags:
        score += 10
        signals.append("idiomatic")
    if "word usually written using kana alone" in flags:
        score += 3
        signals.append("kana-conventional")
    if any(token in gloss for token in SOCIAL_GLOSS):
        score += 20
        signals.append("social-formula-gloss")
    elif any(token in gloss for token in REQUEST_GLOSS):
        score += 14
        signals.append("request-gloss")
    elif any(token in gloss for token in INTERACTION_GLOSS):
        score += 10
        signals.append("interaction-gloss")
    if any(sense["related"] for sense in candidate["senses"]):
        score += 3
        signals.append("related-entry-links")
    if len(candidate["primary"]["japanese"]) <= 12:
        score += 3
        signals.append("compact-form")

    suggested = category(candidate, gloss)
    if suggested == "grammar-pattern":
        score -= 10
        signals.append("grammar-review-needed")
    if suggested == "proverb":
        signals.append("proverb-context-needed")
    if risk_flags:
        score -= min(24, 8 + 4 * len(risk_flags))
        signals.append("specialist-risk")
    score = max(0, min(100, score))

    if risk_flags:
        route = "specialist-review"
    elif score >= 70:
        route = "priority-family-review"
    elif score >= 55:
        route = "standard-family-review"
    else:
        route = "low-priority-review"

    cluster_hint = re.sub(r"[。！？!?\s]", "", candidate["primary"]["reading"])
    return {
        "candidateId": candidate["candidateId"],
        "sourceSequence": candidate["sourceSequence"],
        "automatedScore": score,
        "automatedRoute": route,
        "suggestedCategory": suggested,
        "clusterHint": cluster_hint,
        "signals": sorted(set(signals)),
        "riskFlags": risk_flags,
        "editorialAssignment": assigned.get(candidate["candidateId"]),
        "editorialDisposition": dispositioned.get(candidate["candidateId"]),
    }


def main() -> None:
    candidate_manifest = load(CANDIDATES / "manifest.json")
    assigned = assignments()
    dispositioned = dispositions()
    if set(assigned) & set(dispositioned):
        raise SystemExit("A candidate cannot have both a family assignment and a non-assignment disposition.")
    records: list[dict] = []
    source_pack_sizes: list[int] = []
    for item in candidate_manifest["packs"]:
        source_pack = load(CANDIDATES / item["file"])
        source_pack_sizes.append(len(source_pack["candidates"]))
        records.extend(triage(candidate, assigned, dispositioned) for candidate in source_pack["candidates"])

    if len(records) != candidate_manifest["candidateCount"]:
        raise SystemExit("Candidate count changed during triage.")
    if len({record["candidateId"] for record in records}) != len(records):
        raise SystemExit("Duplicate candidate in triage input.")
    record_ids = {record["candidateId"] for record in records}
    if set(assigned) - record_ids:
        raise SystemExit("An editorial decision references a candidate outside the triage set.")
    if set(dispositioned) - record_ids:
        raise SystemExit("An editorial disposition references a candidate outside the triage set.")

    packs_dir = TRIAGE / "packs"
    if packs_dir.exists():
        shutil.rmtree(packs_dir)
    packs_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    offset = 0
    for number, size in enumerate(source_pack_sizes, 1):
        subset = records[offset : offset + size]
        offset += size
        pack_id = f"triage-{number:03d}"
        payload = {
            "datasetId": "koto-expression-candidate-triage",
            "schemaVersion": 1,
            "packId": pack_id,
            "recordCount": len(subset),
            "records": subset,
        }
        path = packs_dir / f"{pack_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        entries.append({
            "id": pack_id,
            "file": f"packs/{path.name}",
            "recordCount": len(subset),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })

    route_counts = Counter(record["automatedRoute"] for record in records)
    category_counts = Counter(record["suggestedCategory"] for record in records)
    manifest = {
        "datasetId": "koto-expression-candidate-triage",
        "schemaVersion": 1,
        "generatedAt": GENERATED_AT,
        "methodVersion": "1.0.0",
        "sourceCandidateManifest": "../candidates/manifest.json",
        "candidateCount": len(records),
        "assignedCandidateCount": sum(record["editorialAssignment"] is not None for record in records),
        "dispositionedCandidateCount": sum(record["editorialDisposition"] is not None for record in records),
        "riskFlaggedCount": sum(bool(record["riskFlags"]) for record in records),
        "automatedRouteCounts": dict(sorted(route_counts.items())),
        "suggestedCategoryCounts": dict(sorted(category_counts.items())),
        "nonVerificationNotice": "Automated triage is an editorial navigation aid only. It does not verify a candidate, assign Koto Difficulty, determine family membership, or make a record production-eligible.",
        "packs": entries,
    }
    (TRIAGE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Triaged {len(records)} candidates into {len(entries)} packs; "
        f"{manifest['assignedCandidateCount']} have committed editorial assignments, "
        f"{manifest['dispositionedCandidateCount']} have explicit non-assignment dispositions, and "
        f"{manifest['riskFlaggedCount']} carry specialist-risk flags."
    )

if __name__ == "__main__":
    main()
