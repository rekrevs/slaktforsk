"""Prepare the approved six-row upper Flen 914 correction without canonical apply."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECISIONS = HERE / "flen914-upper-followup-decisions-v2-20260924.json"
COMPARISON = HERE / "flen914-upper-comparison-approved-20260924.json"
OUTPUT = HERE / "flen914-upper-proposed-operation.json"
REPORT = HERE / "flen914-upper-proposal-build-20260924.json"
assert hashlib.sha256(COMPARISON.read_bytes()).hexdigest() == "399db85e6191b36e848f13f187a9647d1e2d1785b14d2396061651cb9cf5c613"
decisions = json.loads(DECISIONS.read_text())
comparison = json.loads(COMPARISON.read_text())
RECORD = "R-e67bb6868b81121b2d3f0732"
OLD_TR = "TR-28c61ea70fcc5bf6c4c7b7fa"
TR = "TR-T0676-FLEN914-UPPER-45"
AUDIT = "AUDIT-T0676-FLEN914-UPPER-45"
ARNE = decisions["arne_adoption_proposed"]["suggested_object_id"]


def inspect(object_id):
    return json.loads(subprocess.check_output(["node", "genealogy2/cli.mjs", "inspect", object_id], cwd=ROOT, text=True))


def evidence(current):
    return [{"object": e["basis_revision_id"].rsplit("@", 1)[0], "version": int(e["basis_revision_id"].rsplit("@", 1)[1]), "role": e["role"], "note": e["note"]} for e in current["evidence"]]


def origins(current):
    return [{"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]} for o in current["origins"]]


headers = comparison["headers"]
rows = comparison["rows"]
assert len(headers) == 18 and len(rows) == 6 and comparison["count"]["fields"] == 108
assert [r["row"] for r in rows] == [2, 4, 5, 6, 7, 8]
assert all([f["column"] for f in r["fields"]] == list(range(1, 19)) for r in rows)
for r in rows:
    assert len(r["fields"]) == 18
    for f in r["fields"]:
        assert f["label"] == headers[str(f["column"])]
record = inspect(RECORD)
assert record["kind"] == "record" and record["currentVersion"] == 1
assert len(record["current"]["media"]) == 1 and record["current"]["media"][0]["sha256"] == comparison["source"]["sha256"]
old = inspect(OLD_TR)
assert old["kind"] == "transcription" and old["currentVersion"] == 1 and old["current"]["record_id"] == RECORD

tr_body = {
    "task": "T-0676", "scope": 45, "record_id": RECORD,
    "source": comparison["source"], "printed_headers_18": headers,
    "rows_2_4_5_6_7_8_full_fields": rows,
    "header_provenance": comparison["header_provenance"],
    "differences": comparison["differences"],
    "preserved_second_local_marks": comparison["preserved_second_local_marks"],
    "limits": comparison["limits"],
    "coverage_boundary": "Six approved rows only. Rader1 och3 har ännu inte fått ett motsvarande 18-kolumnspass; ingen full 8-radersslutsats görs.",
}
changes = [
    {
        "id": TR, "kind": "transcription", "expectedVersion": None,
        "data": {"record_id": RECORD, "text": json.dumps(tr_body, ensure_ascii=False, indent=2), "reading_note": "Flen AIIa/4c folio914 övre grupp: exakt sex godkända rader 2,4–8 ×18 tryckta kolumner; FIRST/SECOND-skillnader och reservationer bevaras. Rader1/3 ingår inte i fullfältspasset."},
        "disposition": "recorded", "evidenceStatus": None,
        "rationale": "T-0676: rootgodkänt fullständigt fältprotokoll för sex avgränsade rader; tidigare avskrift bevaras historiskt.",
        "caveat": "Walter föredras men Wattin står kvar som alternativ; Fl.-notens månadsled reserveras. Namn-, datum- och personkopplingar behåller beslutets individuella reservationer. Ingen fullgranskning av rader1/3 här.",
        "origins": [], "evidence": [
            {"object": RECORD, "version": 1, "role": "derived_from", "note": "Samma bevarade originalbild, avgränsad egen radgrupp."},
            {"object": OLD_TR, "version": 1, "role": "context", "note": "Äldre avskrift bevaras oförändrad med sina ursprungliga läsningar."},
        ],
    },
    {
        "id": AUDIT, "kind": "assessment", "expectedVersion": None,
        "data": {"subject_id": RECORD, "criteria": "source_record_review/1", "outcome": "reviewed_with_reservations", "body": json.dumps({"task": "T-0676", "scope": 45, "record_id": RECORD, "comparison_file": str(COMPARISON.relative_to(ROOT)), "comparison_sha256": hashlib.sha256(COMPARISON.read_bytes()).hexdigest(), "reviewed_rows": [2, 4, 5, 6, 7, 8], "printed_columns": 18, "reviewed_positions": 108, "differences": comparison["differences"], "limits": comparison["limits"], "full_rows_1_and_3_not_claimed": True, "no_new_person_or_family_edge": True}, ensure_ascii=False, indent=2)},
        "disposition": "recorded", "evidenceStatus": None,
        "rationale": "T-0676: sex rader och deras 108 kolumnpositioner prövade med bevarade sakreservationer.",
        "caveat": "Källposten omfattar även rader1/3 som inte fullfältgranskas i denna operation. Råmarkeringar ger inga nya person- eller familjeslutsatser.",
        "origins": [], "evidence": [
            {"object": RECORD, "version": 1, "role": "derived_from", "note": "Befintlig avgränsad övre källpost och bevarad originalbild."},
            {"object": TR, "version": 1, "role": "supports", "note": "Fullt protokoll för godkända sex rader, med gräns mot rader1/3."},
        ],
    },
]

data_fields = {
    "assessment": ("subject_id", "criteria", "outcome", "body"),
    "narrative": ("subject_id", "title", "markdown"),
    "observation": ("record_id", "mention_id", "property", "value_literal", "value_json"),
    "mention": ("record_id", "name_literal", "role_literal"),
    "fact": ("subject_id", "property", "value_type", "value_json"),
}
revisions = [d for d in decisions["decisions"] if d["decision"] == "REVISE"]
assert len(revisions) == 15 and sum(len(d["fields"]) for d in revisions) == 24
revision_report = []
for d in revisions:
    object_id = d["object_id"]
    view = inspect(object_id)
    current = view["current"]
    assert current["revision_id"] == d["current_revision"] and view["currentVersion"] == 1
    after = dict(current)
    for f in d["fields"]:
        assert f["field"] in (*data_fields[view["kind"]], "caveat")
        assert current[f["field"]] == f["before"], (object_id, f["field"])
        after[f["field"]] = f["after"]
    data = {k: after[k] for k in data_fields[view["kind"]]}
    for k in ("value_json",):
        if k in data and isinstance(data[k], str):
            data[k] = json.loads(data[k])
    e = evidence(current)
    rebased = []
    for basis in e:
        if object_id == "O-P-0043-related124-household_role_report" and basis["object"] == "M-P-0043-related124":
            assert basis["version"] == 1
            basis["version"] = 2
            rebased.append("M-P-0043-related124@2")
        if object_id == "F-P-0043-family_context-Karin-Elisabet-sequence" and basis["object"] == "O-C0910-Karin-Elisabet-row6":
            assert basis["version"] == 1
            basis["version"] = 2
            rebased.append("O-C0910-Karin-Elisabet-row6@2")
        if object_id == "F-P-0043-family_context-Karl-Harry-sequence" and basis["object"] == "O-C0910-Karl-Harry-row5":
            assert basis["version"] == 1
            basis["version"] = 2
            rebased.append("O-C0910-Karl-Harry-row5@2")
    e.extend([
        {"object": TR, "version": 1, "role": "supports" if object_id != "O-P-0009-C0918-job-certificate" else "context", "note": "Relevant fält i C-0910:s godkända sexradsprotokoll; C-0918:s egen källpost förblir separat." if object_id == "O-P-0009-C0918-job-certificate" else "Versionsbundet stöd för precis den beslutade C-0910-rättelsen inom rader2,4–8."},
        {"object": AUDIT, "version": 1, "role": "context", "note": "Granskad rad-/kolumngräns för de sex godkända raderna; ingen extra oberoende källa."},
    ])
    changes.append({
        "id": object_id, "kind": view["kind"], "expectedVersion": 1,
        "data": data, "disposition": current["disposition"],
        "evidenceStatus": current["evidence_status"], "rationale": current["rationale"],
        "caveat": after["caveat"], "origins": origins(current), "evidence": e,
    })
    revision_report.append({"object": object_id, "fields": [f["field"] for f in d["fields"]], "rebasedEvidence": rebased, "newTR": TR, "newAudit": AUDIT})

adoption = decisions["arne_adoption_proposed"]
assert inspect(ARNE).get("currentVersion") is None
changes.append({
    "id": ARNE, "kind": "assessment", "expectedVersion": None,
    "data": {"subject_id": adoption["subject_id"], "criteria": adoption["criteria"], "outcome": adoption["outcome"], "body": adoption["body"]},
    "disposition": "recorded", "evidenceStatus": None,
    "rationale": "T-0676: avgränsat tillgodoräknande av redan prövad Arne-rad utan ny person- eller identitetsbedömning.",
    "caveat": "Endast C-0910 rad7 inom sexradsprotokollet; OWNER_CONFIRMED-faderskap kvarstår. Ingen faktisk omsorgsstart, PK-/trädstatus eller familjekant avgörs.",
    "origins": [], "evidence": [
        {"object": RECORD, "version": 1, "role": "derived_from", "note": "Befintlig övre C-0910-källpost med Arnes egen rad7."},
        {"object": TR, "version": 1, "role": "supports", "note": "Rad7:s fulla18-kolumnsunderlag med namn- och modersreservation."},
        {"object": AUDIT, "version": 1, "role": "context", "note": "Avgränsad sakgranskning utan ny identitets- eller släktgrind."},
    ],
})
assert len(changes) == 18
operation = {"id": "T-0676/flen914-upper-scope45-proposed", "actor": "Codex", "reason": "T-0676: Astra-godkända sex övre rader ×18 kolumner, 15 exakta objektändringar och Arnes avgränsade adoption; rader1/3 ännu inte fullfältgranskade.", "dependencyReviewVersion": 2, "changes": changes}
OUTPUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {"task": "T-0676", "mode": "PROPOSAL_ONLY", "canonicalApply": False, "decisionSha256": hashlib.sha256(DECISIONS.read_bytes()).hexdigest(), "comparisonSha256": hashlib.sha256(COMPARISON.read_bytes()).hexdigest(), "operation": str(OUTPUT.relative_to(ROOT)), "operationSha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), "changeCount": len(changes), "newTranscriptions": 1, "newAudits": 1, "newBoundedAdoptions": 1, "revisions": revision_report, "reviewedRows": [2, 4, 5, 6, 7, 8], "reviewedPositions": 108, "rows1and3FullInventoryClaimed": False}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": report["operation"], "sha256": report["operationSha256"], "changes": len(changes)}, ensure_ascii=False))
