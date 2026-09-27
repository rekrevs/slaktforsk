"""Prepare the approved scope 8 marriage-record correction; no canonical apply."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECISIONS_PATH = HERE / "oskarshamn-marriage-followup-decisions-v2-20260924.json"
COMPARISON_PATH = HERE / "oskarshamn-marriage-comparison-20260924.json"
OUTPUT = HERE / "oskarshamn-marriage-proposed-operation-v2.json"
REPORT = HERE / "oskarshamn-marriage-proposal-build-v2-20260924.json"
assert hashlib.sha256(DECISIONS_PATH.read_bytes()).hexdigest() == (
    "481d1d3ba14c89895b5e8b77e429a6d826cc1cf588f715cae2fa111b81bcff72"
)
assert hashlib.sha256(COMPARISON_PATH.read_bytes()).hexdigest() == (
    "9b83695cb84b2a177ef3d0d39a1c551d96e65b40c69376faf66fc0156cf18ae0"
)
decisions = json.loads(DECISIONS_PATH.read_text())
comparison = json.loads(COMPARISON_PATH.read_text())
revisions = [d for d in decisions["decisions"] if d["decision"] == "REVISE"]
assert len(revisions) == 11
RECORD_ID = "R-301274634b1d64bcd8934ad1"
OLD_TR_ID = "TR-4798f743fce5dba515016363"
TR_ID = "TR-T0676-OSKARSHAMN-08"
AUDIT_ID = "AUDIT-T0676-08"


def inspect(object_id):
    return json.loads(
        subprocess.check_output(
            ["node", "genealogy2/cli.mjs", "inspect", object_id], cwd=ROOT, text=True)
    )


def evidence_from_current(current):
    return [
        {
            "object": e["basis_revision_id"].rsplit("@", 1)[0],
            "version": int(e["basis_revision_id"].rsplit("@", 1)[1]),
            "role": e["role"],
            "note": e["note"],
        }
        for e in current["evidence"]
    ]


def origins_from_current(current):
    return [
        {"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]}
        for o in current["origins"]
    ]


data_fields = {
    "narrative": ("subject_id", "title", "markdown"),
    "assessment": ("subject_id", "criteria", "outcome", "body"),
    "question": ("subject_id", "title", "outcome", "body"),
    "event": ("event_type", "date_json", "place_id", "place_role"),
    "fact": ("subject_id", "property", "value_type", "value_json"),
    "record": ("source_id", "record_type", "locator", "dependence_note"),
}
proposed_revisions = []
exact_checks = []
for decision in revisions:
    object_id = decision["object_id"]
    view = inspect(object_id)
    current = view["current"]
    kind = view["kind"]
    assert kind == decision["kind"] and view["currentVersion"] == decision["currentVersion"]
    assert current["revision_id"] == decision["current_revision"]
    for key in ("revision_id", "object_id", "version", "kind", "disposition", "evidence_status", "rationale", "caveat"):
        assert current[key] == decision["before_data"][key], (object_id, key)
    for key in data_fields[kind]:
        assert current[key] == decision["before_data"][key], (object_id, key)
    updated = dict(current)
    for key, value in decision["exact_after_fields"].items():
        assert key in data_fields[kind] or key == "caveat"
        updated[key] = value
        exact_checks.append((object_id, key))
    data = {key: updated[key] for key in data_fields[kind]}
    if kind in ("event", "fact"):
        for key in ("date_json", "value_json"):
            if key in data and isinstance(data[key], str):
                data[key] = json.loads(data[key])
    evidence = evidence_from_current(current)
    if object_id != RECORD_ID:
        for e in evidence:
            if e["object"] == RECORD_ID:
                assert e["version"] == 1
                e["version"] = 2
        for oid, role, note in (
            (RECORD_ID, "derived_from", "Egen källpost med registrerings-/ortsreservation och bevarad originalbild."),
            (TR_ID, "supports", "Fullt fältprotokoll med 13 rubriker, äldre återbruk och nya råstreck/marginaltecken."),
            (AUDIT_ID, "context", "Avgränsad sakgranskning av den egna äktenskapsposten utan ny oberoende röst."),
        ):
            if not any(e["object"] == oid and e["version"] == (2 if oid == RECORD_ID else 1) for e in evidence):
                evidence.append({"object": oid, "version": 2 if oid == RECORD_ID else 1, "role": role, "note": note})
    change = {
        "id": object_id,
        "kind": kind,
        "expectedVersion": view["currentVersion"],
        "data": data,
        "disposition": current["disposition"],
        "evidenceStatus": current["evidence_status"],
        "rationale": current["rationale"],
        "caveat": updated["caveat"],
        "origins": origins_from_current(current),
        "evidence": evidence,
    }
    if kind == "record":
        change["assets"] = [
            {"path": m["path"], "region": m["region"]}
            for m in current["media"]
            if m["origin"] == "legacy"
        ]
        change["media"] = [
            {"id": m["id"], "region": m["region"]}
            for m in current["media"]
            if m["origin"] == "native"
        ]
        assert len(change["assets"]) == 1 and change["assets"][0]["path"] == comparison["source"]["path"]
    proposed_revisions.append(change)

assert len(proposed_revisions) == 11
historical_fields = comparison["reused_field_dispositions"]
assert any(f["field"] == "church_form" for f in historical_fields)
current_fields = []
for field in historical_fields:
    entry = dict(field)
    if entry["field"] == "church_form":
        entry["historical_status"] = entry["status"]
        entry["status"] = "superseded_interpretation_not_raw_original_field"
        entry["note"] = (
            "Historisk avskrifts-/berättelseform inom svenska kyrkan; ingen synlig separat "
            "originalrubrik eller säker kyrklig/borgerlig klass i detta fält. "
            + entry.get("note", "")
        )
    if entry["field"] == "other_unnamed_printed_columns":
        assert entry["status"] == "oläst"
        entry["historical_status"] = "oläst"
        entry["status"] = "historical_documentation_gap_resolved_by_13_column_inventory"
        entry["note"] = (
            "Äldre avskriftens kolumnlucka är historik. T-0676 inventerar alla 13 "
            "tryckta rubriker och tillför kolumn 8:s råstreck; ingen ytterligare "
            "tryckt kolumn anges som ännu oläst. " + entry.get("note", "")
        )
    current_fields.append(entry)

transcription_body = {
    "scope": 8,
    "source": comparison["source"],
    "printed_headers_13": comparison["headers"],
    "prior_text_layers_exact_not_new_diplomatic_reading": comparison["reused_layers"],
    "prior_field_dispositions_historical": historical_fields,
    "current_field_dispositions": current_fields,
    "newly_read_gap_fields": comparison["added_fields"],
    "clarifications": comparison["clarifications"],
    "comparison": comparison["comparison"],
    "status": "FULL_RELEVANT_EXTRACTION_WITH_DOCUMENTED_REUSE_AND_RESERVATIONS",
}
transcription = {
    "id": TR_ID,
    "kind": "transcription",
    "expectedVersion": None,
    "data": {
        "record_id": RECORD_ID,
        "text": json.dumps(transcription_body, ensure_ascii=False, indent=2),
        "reading_note": "T-0676 scope8: 13 tryckta kolumner, full återbrukad namn-/datum-/attesttext med egen proveniens, ny kol8-streck och svag marginalbock. Kol11 har separata 1/1; kol12 förrättare och kol13 osäkert vigselbevis återbrukas. Äldre formulering inom svenska kyrkan är historisk tolkning, inte rått originalfält. Kyrkoboksförsamling och Växiö förrättarort avgör inte fysisk vigselort; ingen ny kyrklig/borgerlig klass.",
    },
    "disposition": "recorded",
    "evidenceStatus": None,
    "rationale": "T-0676: avgränsad komplettering av saknade markfält och 13-kolumnskarta med ordagranna äldre lager; samma bevarade originalbild, inga nya oberoende källröster.",
    "caveat": "Kol8 visar streck och marginalen v[?] utan avkodad betydelse. Brudens yrkesord och vigselbevis 13/9 eller 13/11 kvarstår reserverade. Historisk kyrkoformulering och generisk rubrik om borgerligt äktenskap fastställer ingen klass eller fysisk ort.",
    "origins": [],
    "evidence": [
        {"object": RECORD_ID, "version": 2, "role": "derived_from", "note": "Samma versionsbundna avgränsade källpost och bevarade helbild."},
        {"object": OLD_TR_ID, "version": 1, "role": "context", "note": "Äldre ordagrant avskriftsskikt bevaras historiskt, inklusive senare T-0147-tillägg."},
    ],
}
audit_body = {
    "scope": 8,
    "record": RECORD_ID,
    "comparison_file": str(COMPARISON_PATH.relative_to(ROOT)),
    "comparison_sha256": hashlib.sha256(COMPARISON_PATH.read_bytes()).hexdigest(),
    "printed_columns": 13,
    "reviewed_fields": "Egen post35:s 13 rubriker och återbrukade positiva fält; ny kol8-streck och svag marginalbock; kol11 separata1/1; kol12/13 fortsatt reserverade enligt tidigare fullfältspass.",
    "limits": comparison["clarifications"],
    "source_copy": comparison["source"],
    "no_new_identity_or_pedigree_gate": True,
}
audit = {
    "id": AUDIT_ID,
    "kind": "assessment",
    "expectedVersion": None,
    "data": {
        "subject_id": RECORD_ID,
        "criteria": "source_record_review/1",
        "outcome": "reviewed_with_reservations",
        "body": json.dumps(audit_body, ensure_ascii=False, indent=2),
    },
    "disposition": "recorded",
    "evidenceStatus": None,
    "rationale": "T-0676: egen postgräns/full relevant fälttäckning och sakreservationer prövade utan identitets- eller livsbildsgrind.",
    "caveat": "Samma källa i historiska och nya avskriftsskikt. Streck, marginalbock, brudens yrkesord, attestdatum och fysisk vigselort förblir reserverade; inga negativa tomfält utanför den prövade posten.",
    "origins": [],
    "evidence": [
        {"object": RECORD_ID, "version": 2, "role": "derived_from", "note": "Versionsbunden post35 med bevarad originalbild."},
        {"object": TR_ID, "version": 1, "role": "supports", "note": "Fullt fältprotokoll med historiskt återbruk och ny råformsgräns."},
    ],
}
record_change = next(c for c in proposed_revisions if c["id"] == RECORD_ID)
other_changes = [c for c in proposed_revisions if c["id"] != RECORD_ID]
operation = {
    "id": "T-0676/oskarshamn-marriage-scope8-v2-proposed",
    "actor": "Codex",
    "reason": "T-0676 scope8: full relevant kolumninventering och avgränsad rättelse av källa/registreringsort/yrkesreservation enligt 11 Astra-godkända objektbeslut. Äldre avskrift bevaras historiskt; ingen ny civil eller kyrklig klass eller personrelation.",
    "dependencyReviewVersion": 2,
    "changes": [record_change, transcription, audit, *other_changes],
}
assert len(operation["changes"]) == 13
OUTPUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {
    "task": "T-0676",
    "scope": 8,
    "mode": "PROPOSAL_ONLY",
    "decisionSha256": hashlib.sha256(DECISIONS_PATH.read_bytes()).hexdigest(),
    "comparisonSha256": hashlib.sha256(COMPARISON_PATH.read_bytes()).hexdigest(),
    "operation": str(OUTPUT.relative_to(ROOT)),
    "operationSha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    "revisions": len(proposed_revisions),
    "newTranscriptions": 1,
    "newAudits": 1,
    "approvedExactAfterFields": exact_checks,
    "legacyOriginalAssetPreserved": True,
    "historicalChurchPhraseNotRawOriginalField": True,
    "canonicalApply": False,
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": str(OUTPUT), "sha256": report["operationSha256"], "changes": 13, "exactAfterFields": len(exact_checks)}, ensure_ascii=False))
