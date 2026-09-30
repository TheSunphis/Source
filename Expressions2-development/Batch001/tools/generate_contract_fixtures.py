#!/usr/bin/env python3
"""Generate deterministic synthetic JSON fixtures for Expressions2 contracts.

These records are contract-only test data. They are not corpus candidates, family
truth, or publishable content.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSITIVE = ROOT / "fixtures" / "contracts" / "positive"
NEGATIVE = ROOT / "fixtures" / "contracts" / "negative"
A = "a" * 64
B = "b" * 64
C = "c" * 64
D = "d" * 64
TS = "2026-09-30T00:00:00Z"
FAMILY_ID = "expression2:00000000-0000-7000-8000-000000000001"
CANDIDATE_ID = "candidate2:" + "a" * 32
FORM_ID = "primary"
ANALYSIS_ID = "analysis2:" + "b" * 32
PROVENANCE_ID = "provenance2:" + "c" * 32


def family_id(number: int) -> str:
    return f"expression2:00000000-0000-7000-8000-{number:012x}"


def evidence(source: str = "source2:jmdict-english", digest: str = A, locator: str = "entry:fixture") -> dict:
    return {
        "sourceId": source,
        "locator": locator,
        "evidenceType": "direct-authority" if "jmdict" in source else "corpus-attestation",
        "supports": ["existence", "form", "reading"],
        "recordHash": digest,
        "permissionClass": "redistributable",
    }


E1 = evidence()
E2 = evidence("source2:tatoeba-cc0", B, "sentence:fixture")
LINE = {
    "japanese": "テスト表現です。",
    "reading": "てすとひょうげんです。",
    "meaning": "This is synthetic contract-test text.",
    "deviceTts": True,
}

SOURCE_REGISTRY = {
    "schemaVersion": 1,
    "targetDatasetLicense": "CC-BY-SA-4.0",
    "sources": [{
        "sourceId": "source2:fixture-source",
        "name": "Synthetic fixture source",
        "owner": "Koto contract tests",
        "canonicalUrl": "https://example.invalid/source",
        "acquisitionUrl": "https://example.invalid/source.dat",
        "networkPolicy": {"allowedHosts": ["example.invalid"], "maxBytes": 1024, "expectedBytes": 12, "expectedSha256": None},
        "roles": ["candidate-forms"],
        "permissionClass": "redistributable",
        "approvalStatus": "approved-for-snapshot",
        "license": {
            "name": "CC0-1.0", "url": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
            "commercialUse": True, "redistribution": True, "shareAlike": False,
            "attribution": "Synthetic fixture; no attribution required.", "notes": "Not real source data."
        },
        "allowed": {
            "machineAccess": True, "modelProcessing": True, "redistributeRaw": True,
            "redistributeExtracts": True, "publishDerivedRecords": True
        },
        "thirdPartyContentRisk": "low", "notes": "Fixture only.", "snapshot": None,
    }],
}

SNAPSHOT = {
    "schemaVersion": 1, "sourceId": "source2:fixture-source",
    "canonicalUrl": "https://example.invalid/source", "acquisitionUrl": "https://example.invalid/source.dat",
    "finalUrl": "https://example.invalid/source.dat", "retrievedAt": TS, "bytes": 12, "sha256": A, "mediaType": "application/octet-stream",
    "license": {"name": "CC0-1.0", "url": "https://creativecommons.org/publicdomain/zero/1.0/legalcode", "noticeFile": "notices/fixture-source.license", "noticeSha256": B},
    "attribution": "Synthetic fixture.", "allowedRoles": ["contract-test"],
    "redistribution": "raw-and-derived", "rawRetention": "temporary-deleted", "rawFile": None,
    "verification": {"httpStatus": 200, "registryMatch": True, "hashVerified": True, "expectedIdentityMatch": True, "archiveSafe": True, "unexpectedFormat": False},
}

SOURCE_EVIDENCE = {
    "schemaVersion": 1, "snapshotSha256": A, "sourceId": "source2:jmdict-english",
    "records": [{"evidenceId": "evidence2:" + "a" * 32, "locator": "entry:fixture", "recordHash": A,
                 "fields": {"surface": "テスト表現", "reading": "てすとひょうげん"}, "permissionClass": "redistributable"}],
}

EVIDENCE_BUILD_MANIFEST = {
    "schemaVersion": 1, "buildId": "evidencebuild2:" + "a" * 32, "sourceDateEpoch": TS,
    "artifacts": [{"sourceId": "source2:jmdict-english", "file": "jmdict-english.evidence.json.gz",
                   "snapshotSha256": A, "recordCount": 1, "canonicalBytes": 100, "compressedBytes": 80,
                   "canonicalSha256": B, "compressedSha256": C,
                   "adapter": {"name": "jmdict-expression", "version": "0.1.0"},
                   "permissionClass": "redistributable", "secondPassMatched": True}],
    "totals": {"sources": 1, "records": 1, "canonicalBytes": 100, "compressedBytes": 80},
    "determinism": {"canonicalJson": True, "gzipMtime": 0, "allSecondPassesMatched": True},
    "contaminationAudit": {"legacyImports": 0, "legacyIds": 0, "prohibitedWiktionaryText": 0,
                           "permissionMismatches": 0, "verdict": "passed"},
}

RAW_CANDIDATE = {
    "schemaVersion": 1, "rawCandidateId": "rawcandidate2:" + "a" * 32,
    "channel": "labelled-expression", "surface": "テスト表現", "reading": "てすとひょうげん",
    "sourceEvidence": [E1],
    "extractor": {"name": "fixture-extractor", "version": "0.1.0", "sourceSnapshotSha256": A, "ruleId": "fixture-rule"},
    "createdAt": TS,
}

CANDIDATE = {
    "schemaVersion": 1, "candidateId": CANDIDATE_ID, "surface": "テスト表現", "reading": "てすとひょうげん",
    "normalizedKey": "テスト表現|てすとひょうげん", "senseGlosses": ["synthetic contract-test expression"],
    "sourceEvidence": [E1], "classHypotheses": ["interactional-formula"],
    "signals": {"multiword": True, "fixedness": 1.0, "productiveSlots": 0, "formulaic": True,
                "pragmaticFunction": True, "dictionaryExpressionTag": True, "corpusHitCount": 2},
    "normalization": {"pipelineVersion": "0.1.0", "unicodeForm": "NFC", "sourceRecordIds": ["entry:fixture"], "inputDigest": A},
    "createdAt": TS,
}

CANDIDATE_STORE = {
    "schemaVersion": 1, "kind": "raw", "records": [RAW_CANDIDATE],
}

CANDIDATE_BUILD_MANIFEST = {
    "schemaVersion": 1, "buildId": "candidatebuild2:" + "a" * 32, "sourceDateEpoch": TS,
    "inputs": {"evidenceBuildId": "evidencebuild2:" + "b" * 32, "evidenceManifestSha256": A},
    "runtime": {"sudachiPyVersion": "0.7.0", "sudachiPySha256": B,
                "dictionaryVersion": "20260723.1", "dictionarySha256": C, "splitMode": "C-with-A-features"},
    "artifacts": [
        {"kind": "raw", "file": "raw-candidates.json.gz", "records": 2500, "canonicalBytes": 1000,
         "compressedBytes": 500, "canonicalSha256": A, "compressedSha256": B},
        {"kind": "normalized", "file": "normalized-candidates.json.gz", "records": 2000, "canonicalBytes": 1000,
         "compressedBytes": 500, "canonicalSha256": C, "compressedSha256": D},
    ],
    "counts": {"rawCandidates": 2500, "normalizedCandidates": 2000,
               "rawByChannel": {"labelled-expression": 2000, "corpus-ngram": 400, "wiktionary-structural": 100},
               "normalizedByPrimaryHypothesis": {"conventional-collocation": 2000},
               "corpusAttestedNormalized": 500, "duplicatesMerged": 500},
    "determinism": {"canonicalJson": True, "gzipMtime": 0, "secondBuildMatched": True, "stableOrdering": True},
    "contaminationAudit": {"legacyImports": 0, "legacyIds": 0, "unapprovedSources": 0, "personalState": 0, "verdict": "passed"},
    "familyGenerationStarted": False,
}

ANALYSIS = {
    "schemaVersion": 1, "analysisId": ANALYSIS_ID, "familyId": FAMILY_ID, "formId": FORM_ID,
    "japanese": "テスト表現", "reading": "てすとひょうげん",
    "segments": [
        {
            "segmentId": "s01", "surface": "テスト", "reading": "てすと", "kind": "content-or-idiom",
            "contextualMeaning": "test", "grammaticalRole": "noun modifier", "lemma": "テスト", "inflection": None,
            "japaneseSpan": {"start": 0, "end": 3}, "readingSpan": {"start": 0, "end": 3},
            "vocabularyDisposition": {"status": "linked", "vocabularyId": "fixture-vocab-1", "canonicalSurface": "テスト",
                                      "canonicalReading": "てすと", "selectionReason": "Exact fixture identity.", "reverseChecked": True},
            "evidence": [E1], "reviewIdentity": "fixture-reviewer",
        },
        {
            "segmentId": "s02", "surface": "表現", "reading": "ひょうげん", "kind": "content-or-idiom",
            "contextualMeaning": "expression", "grammaticalRole": "head noun", "lemma": "表現", "inflection": None,
            "japaneseSpan": {"start": 3, "end": 5}, "readingSpan": {"start": 3, "end": 8},
            "vocabularyDisposition": {"status": "unlinked", "reasonCode": "no-exact-canonical-record",
                                      "explanation": "No real Vocabulary data is used by synthetic fixtures.", "reverseChecked": True},
            "evidence": [E1], "reviewIdentity": "fixture-reviewer",
        },
    ],
    "vocabularyEnumeration": [
        {"segmentId": "s01", "candidateIds": ["fixture-vocab-1"], "selectedId": "fixture-vocab-1", "enumeratorVersion": "0.1.0", "indexDigest": C},
        {"segmentId": "s02", "candidateIds": [], "selectedId": None, "enumeratorVersion": "0.1.0", "indexDigest": C},
    ],
    "ambiguities": [],
    "checks": {"surfaceReconstruction": "passed", "readingReconstruction": "passed", "segmentCompleteness": "passed",
               "canonicalValidity": "passed", "reverseOmission": "passed", "ambiguityResolution": "passed"},
    "compiler": {"name": "koto-expressions2-analysis", "version": "0.1.0", "inputDigest": D},
    "review": {"reviewType": "automated", "reviewedAt": TS, "reviewerIdentity": "fixture-reviewer", "gateManifestId": "gates2:fixture"},
}

FAMILY = {
    "schemaVersion": 1, "familyId": FAMILY_ID, "slug": "synthetic-contract-fixture", "candidateIds": [CANDIDATE_ID],
    "primaryClass": "interactional-formula", "facets": ["reaction"],
    "difficulty": {"level": 1, "label": "Essential", "rationale": "Synthetic fixture value for contract validation only."},
    "category": {"key": "reaction", "label": "Reaction"},
    "publication": {"state": "verified", "visibility": "private-shadow", "release": "0.1.0-development", "productionReady": False},
    "library": {
        "japanese": "テスト表現", "reading": "てすとひょうげん", "contextualMeaning": "Synthetic contract-test expression.",
        "intentionSummary": ["Exercise the runtime contract."], "usageContexts": ["Contract validation only"],
        "searchDocument": {"japanese": ["テスト表現"], "reading": ["てすとひょうげん"],
                           "meanings": ["Synthetic contract-test expression."], "intentions": ["Exercise the runtime contract."],
                           "usageAndContext": ["Used only in isolated contract fixtures."]},
        "formCount": 1, "verifiedSourceState": "verified", "availableActions": ["recognised", "review", "open"],
    },
    "hero": {"primaryFormId": FORM_ID, "japanese": "テスト表現", "reading": "てすとひょうげん",
             "contextualMeaning": "Synthetic contract-test expression.",
             "usageSummary": "This deliberately synthetic text exercises every required family-card field.", "deviceTts": True},
    "intentions": [{"action": "Exercise the complete family contract.", "distinguishingNote": "This is not learner-facing corpus content."}],
    "guidance": {
        "useWhen": ["Use only while validating isolated contract fixtures."],
        "takeCare": ["Never treat this synthetic fixture as Japanese teaching content."],
        "relationships": [{"context": "peers", "suitability": "not-applicable", "guidance": "Relationship guidance is synthetic and not instructional."}],
    },
    "forms": [{"formId": FORM_ID, "kind": "primary", "label": "Synthetic primary", "register": "Fixture only",
               "japanese": "テスト表現", "reading": "てすとひょうげん", "contextualMeaning": "Synthetic contract-test expression.",
               "deviceTts": True, "analysisRef": ANALYSIS_ID, "evidence": [E1]}],
    "responses": [{"context": "Synthetic response for contract validation.", "line": LINE}],
    "followUps": [{"context": "Synthetic follow-up for contract validation.", "line": LINE}],
    "dialogue": {"applicable": True, "context": "Synthetic two-turn context used only by contract tests.", "relationship": "fixture",
                 "register": "fixture", "turns": [
                     {"speaker": "A", "containsTarget": True, "line": LINE},
                     {"speaker": "B", "containsTarget": False, "line": LINE},
                 ]},
    "patterns": {"applicable": True, "items": [{
        "template": "テスト＋表現", "templateReading": "てすと＋ひょうげん", "function": "Exercises the required pattern contract.",
        "slots": [{"name": "fixture", "constraint": "Accept only synthetic values in this contract fixture.",
                   "validExamples": ["テスト"], "invalidExamples": ["実データ"]}],
        "riskWarning": "Do not interpret substitutions as natural Japanese usage guidance.", "examples": [LINE, LINE],
    }]},
    "distinctions": [{"nearbyJapanese": "試験表現", "reading": "しけんひょうげん",
                      "distinction": "A synthetic nearby form included to validate the distinction schema.",
                      "registerOrPragmaticContrast": "No genuine register claim is made by this test fixture.",
                      "unsafeReplacement": "Neither synthetic string is approved for learner-facing replacement guidance.",
                      "publishedFamilyId": None}],
    "verification": {"publicationState": "verified", "evidence": [E1, E2], "evidenceClasses": ["level-a", "level-b"],
                     "corpusRelease": "0.1.0-development", "sourceRelease": "source2:" + D,
                     "analysisCompilerVersion": "0.1.0", "attributionRoute": "Synthetic fixture-only attribution route.",
                     "review": {"reviewType": "automated", "reviewedAt": TS, "reviewerIdentity": "fixture-reviewer", "gateManifestId": "gates2:fixture"}},
    "displayContract": {
        "sectionSequence": ["hero", "personal-state", "intentions", "use-when", "take-care", "relationships", "forms-and-analysis",
                            "responses", "follow-ups", "dialogue", "patterns-and-examples", "nearby-distinctions", "verification-and-sources"],
        "stateControls": ["recognised", "review"], "stateMutuallyExclusive": True,
        "audioMethod": "device-japanese-tts-explicit-only", "analysisInteraction": "every-published-form-segment-focusable-and-tappable",
    },
    "provenanceRef": PROVENANCE_ID,
}

LEDGER = {
    "schemaVersion": 1, "ledgerId": "ledger2:" + "a" * 32, "createdAt": TS,
    "events": [{"sequence": 1, "eventId": "ledgerevent2:" + "a" * 32, "candidateIds": [CANDIDATE_ID], "familyId": FAMILY_ID,
                "action": "admit", "reasonCodes": ["fixture-contract"],
                "explanation": "Synthetic event exercises the append-only decision ledger contract.",
                "evidence": [E1], "actor": "fixture-generator", "occurredAt": TS, "previousEventHash": None}],
}

PROVENANCE = {
    "schemaVersion": 1, "provenanceId": PROVENANCE_ID, "familyId": FAMILY_ID, "candidateIds": [CANDIDATE_ID],
    "sourceSnapshots": [{"sourceId": "source2:jmdict-english", "sha256": A}],
    "fieldDerivations": [{"jsonPointer": "/hero/japanese", "method": "source-extract", "evidence": [E1], "criticStatus": "passed"}],
    "compiler": {"name": "koto-expressions2-family", "version": "0.1.0", "configurationDigest": B},
    "review": {"reviewType": "automated", "reviewedAt": TS, "reviewerIdentity": "fixture-reviewer", "gateManifestId": "gates2:fixture"},
    "inputDigest": C, "outputDigest": D,
}

ARTIFACTS = []
for number in range(1, 5):
    ARTIFACTS.append({"path": f"family-pack-{number:02d}.json", "kind": "family-pack", "bytes": 1, "sha256": A})
for number in range(1, 5):
    ARTIFACTS.append({"path": f"analysis-pack-{number:02d}.json", "kind": "analysis-pack", "bytes": 1, "sha256": B})
ARTIFACTS += [
    {"path": "library-index.json", "kind": "library-index", "bytes": 1, "sha256": C},
    {"path": "source-attribution.json", "kind": "source-attribution", "bytes": 1, "sha256": D},
    {"path": "audit-manifest.json", "kind": "audit-manifest", "bytes": 1, "sha256": A},
    {"path": "provenance-pack.json", "kind": "provenance-pack", "bytes": 1, "sha256": B},
]

COMPILER_MANIFEST = {
    "schemaVersion": 1, "buildId": "build2:" + "a" * 32, "release": "0.1.0-development",
    "publicationStatus": "shadow-candidate", "productionReady": False, "sourceDateEpoch": 1790726400,
    "inputs": [{"kind": "schema", "id": "fixture-schema-set", "sha256": A}],
    "counts": {"normalizedCandidates": 2000, "acceptedFamilies": 100, "publishedForms": 100,
               "analysisRecords": 100, "familyPacks": 4, "familiesPerPack": 25},
    "coverage": {
        "classCounts": {"interactional-formula": 18, "discourse-routine": 12, "grammar-construction": 18,
                        "conventional-collocation": 15, "idiom": 10, "proverb-or-saying": 5,
                        "institutional-formula": 8, "productive-sentence-frame": 8, "pragmatic-pattern": 6},
        "difficultyCounts": {"1": 20, "2": 25, "3": 25, "4": 20, "5": 10},
        "documentedDeviations": [],
    },
    "artifacts": ARTIFACTS,
    "determinism": {"canonicalJson": True, "stableOrdering": True, "secondCleanBuildMatched": True},
    "incrementalBuild": {"contentAddressedCache": True, "changedOnlySupported": True},
}

GATES = {key: "passed" for key in [
    "familyInclusion", "mergeSplit", "naturalness", "meaningIntention", "registerRelationship", "difficulty",
    "formsReadings", "segments", "canonicalLinks", "conversation", "patternsDistinctions",
    "sourceLicenseProvenance", "librarySummary", "fullCard",
]}
AUDIT = {
    "schemaVersion": 1, "auditId": "audit2:" + "a" * 32, "release": "0.1.0-development",
    "scope": "all-100-accepted-families",
    "families": [{"familyId": family_id(i), "auditor": "fixture-auditor", "auditedAt": TS,
                  "gates": GATES, "defects": [], "status": "passed"} for i in range(1, 101)],
    "summary": {"auditedFamilies": 100, "passedFamilies": 100, "unresolvedDefects": 0, "auditCoveragePercent": 100},
    "verdict": "passed-private-shadow-only",
}

INDEX_ENTRIES = []
for i in range(1, 101):
    INDEX_ENTRIES.append({
        "familyId": family_id(i), "slug": f"synthetic-fixture-{i:03d}", "pack": f"family-pack-{((i - 1) // 25) + 1:02d}",
        "difficulty": ((i - 1) % 5) + 1, "category": {"key": "fixture", "label": "Fixture"},
        "japanese": "テスト表現", "reading": "てすとひょうげん", "contextualMeaning": "Synthetic fixture only.",
        "intentions": ["Exercise runtime indexing."], "usageContexts": ["Contract validation only"],
        "searchText": "テスト表現 てすとひょうげん synthetic fixture contract validation", "formCount": 1,
        "verifiedSourceState": "verified", "availableActions": ["recognised", "review", "open"],
    })
RUNTIME_INDEX = {
    "schemaVersion": 1, "release": "0.1.0-development", "publicationStatus": "shadow-candidate",
    "familyCount": 100, "formCount": 100,
    "categories": [{"key": "fixture", "label": "Fixture", "count": 100}], "entries": INDEX_ENTRIES,
}

RUNTIME_CARD = {
    "schemaVersion": 1, "release": "0.1.0-development", "family": FAMILY, "analyses": [ANALYSIS],
    "integrity": {"allPublishedFormsAnalyzed": True, "allAnalysisRefsResolved": True, "noPersonalState": True, "deviceTtsOnly": True},
}

FIXTURES = {
    "source-registry": SOURCE_REGISTRY,
    "snapshot-manifest": SNAPSHOT,
    "source-evidence": SOURCE_EVIDENCE,
    "evidence-build-manifest": EVIDENCE_BUILD_MANIFEST,
    "raw-candidate": RAW_CANDIDATE,
    "candidate": CANDIDATE,
    "candidate-store": CANDIDATE_STORE,
    "candidate-build-manifest": CANDIDATE_BUILD_MANIFEST,
    "form-analysis": ANALYSIS,
    "family": FAMILY,
    "family-ledger": LEDGER,
    "provenance": PROVENANCE,
    "compiler-manifest": COMPILER_MANIFEST,
    "audit-manifest": AUDIT,
    "runtime-library-index": RUNTIME_INDEX,
    "runtime-family-card": RUNTIME_CARD,
}


def main() -> None:
    POSITIVE.mkdir(parents=True, exist_ok=True)
    NEGATIVE.mkdir(parents=True, exist_ok=True)
    for name, value in FIXTURES.items():
        positive_path = POSITIVE / f"{name}.valid.json"
        positive_path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        invalid = copy.deepcopy(value)
        invalid.pop("schemaVersion", None)
        negative_path = NEGATIVE / f"{name}.invalid.json"
        negative_path.write_text(json.dumps(invalid, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(f"wrote {len(FIXTURES)} positive and {len(FIXTURES)} negative contract fixtures")


if __name__ == "__main__":
    main()
