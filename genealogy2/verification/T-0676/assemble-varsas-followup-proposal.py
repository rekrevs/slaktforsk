"""Assemble the Värsås v2 research proposal after the row duplicate decision.

This builder reads current heads and the locked row transcriptions. It prepares
an operation for isolated checking and Astra review; it never applies it.
"""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECISIONS = json.loads((HERE / "varsas-followup-decisions-v2-20260924.json").read_text())
DRAFT = json.loads((HERE / "varsas-followup-revisions-draft.json").read_text())
OUTPUT = HERE / "varsas-followup-proposed-operation-v2.json"
REPORT = HERE / "varsas-followup-proposal-build-v2-20260924.json"
assert len(DRAFT["changes"]) == 153 and len(DRAFT["checks"]) == 241


def inspect(object_id):
    return json.loads(
        subprocess.check_output(
            ["node", "genealogy2/cli.mjs", "inspect", object_id], cwd=ROOT, text=True)
    )


def add_evidence(change, object_id, version, role, note):
    existing = [e for e in change["evidence"] if e["object"] == object_id and e["version"] == version]
    if existing:
        return
    change["evidence"].append(
        {"object": object_id, "version": version, "role": role, "note": note}
    )


row_plan = {p["row"]: p for p in DECISIONS["observation_mention_key_plan"]}
assert set(row_plan) == {1, 5, 6, 7, 8, 9, 23, 24}
role_literals = {
    1: "Hemmansägare",
    5: "s. och Brukare",
    6: "s.",
    7: "d.",
    8: "s.",
    9: "d.",
    23: "Dräng",
    24: "Piga",
}
changes = []
observations = {}
mentions = {}
for row, plan in sorted(row_plan.items()):
    record_id = plan["record_binding"]["record_revision"].rsplit("@", 1)[0]
    assert inspect(record_id)["currentVersion"] == 1
    transcript_id = plan["record_binding"]["transcription_id"]
    transcript_view = inspect(transcript_id)
    assert transcript_view["currentVersion"] == 1
    transcript = json.loads(transcript_view["current"]["text"])
    assert transcript["row"] == row and len(transcript["columns"]) == 18
    audit_id = plan["record_binding"]["audit_id"]
    assert inspect(audit_id)["currentVersion"] == 1
    first_name = transcript["columns"][0]["first"]["raw"]
    adjudicated_name = transcript["columns"][0]["adjudication"].get("raw")
    name_literal = adjudicated_name or first_name
    mention_id = plan["proposed_mention_id"]
    observation_id = (
        "O-P-0027-household-134-fields" if row == 9 else plan["proposed_observation_id"]
    )
    mention = {
        "id": mention_id,
        "kind": "mention",
        "expectedVersion": None,
        "data": {
            "record_id": record_id,
            "name_literal": name_literal,
            "role_literal": role_literals[row],
        },
        "disposition": "recorded",
        "evidenceStatus": "TRANSCRIBED",
        "rationale": f"T-0676: eget namn-/rollomnämnande i Värsås folio 134 rad {row}, utan ny identitetskoppling.",
        "caveat": "Rå namn- och rollform är bunden till egen rad. Osäkra bokstäver, strykning och ditto bevaras i full TR. Mentionen skapar ingen ny P-person eller identity; särskilt raderna 23–24 får ingen personkoppling.",
        "origins": [],
        "evidence": [
            {"object": record_id, "version": 1, "role": "derived_from", "note": f"Egen källpost för Värsås rad {row}."},
            {"object": transcript_id, "version": 1, "role": "supports", "note": "Full 18-kolumnsavskrift med reserverad rånamnsform."},
        ],
    }
    field_values = []
    for col in transcript["columns"]:
        adjudication = col["adjudication"]
        field_values.append(
            {
                "column": col["column"],
                "printed_header": col["printed_header"],
                "raw": adjudication.get("raw") if adjudication.get("raw") is not None else col["first"]["raw"],
                "status": adjudication["status"] if adjudication.get("raw") is not None else col["first"]["status"],
                "first_raw": col["first"]["raw"],
                "second_raw": col["second"]["raw"],
                "adjudication": adjudication,
            }
        )
    observation_data = {
        "record_id": record_id,
        "mention_id": mention_id,
        "property": "parish_register_fields",
        "value_literal": f"Värsås A II a/2, folio 134, egen rad {row}: alla 18 kolumner enligt {transcript_id}, med råreservationer och marginal-/strykningstecken i fullavskriften.",
        "value_json": {
            "row": row,
            "folio": 134,
            "image": "00073285_00141",
            "column_fields": field_values,
            "full_transcription_id": transcript_id,
            "normalised_person_id": None,
        },
    }
    observation_evidence = [
        {"object": record_id, "version": 1, "role": "derived_from", "note": f"Egen rad {row} i avgränsad källpost."},
        {"object": mention_id, "version": 1, "role": "context", "note": "Källradens råa namn-/rollomnämnande utan ny identity."},
        {"object": transcript_id, "version": 1, "role": "supports", "note": "Full 18-kolumnsavskrift, först/andraläsning och adjudikation."},
        {"object": audit_id, "version": 1, "role": "context", "note": "Avgränsad audit av egen rad och återbrukade grannrader."},
    ]
    if row == 9:
        old = inspect(observation_id)
        assert old["currentVersion"] == 1
        c = old["current"]
        assert c["record_id"] == record_id and c["property"] == "personal_fields" and c["mention_id"] is None
        old_evidence = [
            {
                "object": e["basis_revision_id"].rsplit("@", 1)[0],
                "version": int(e["basis_revision_id"].rsplit("@", 1)[1]),
                "role": e["role"],
                "note": e["note"],
            }
            for e in c["evidence"]
        ]
        for e in observation_evidence:
            if not any(x["object"] == e["object"] and x["version"] == e["version"] and x["role"] == e["role"] for x in old_evidence):
                old_evidence.append(e)
        observation = {
            "id": observation_id,
            "kind": "observation",
            "expectedVersion": 1,
            "data": observation_data,
            "disposition": c["disposition"],
            "evidenceStatus": c["evidence_status"],
            "rationale": c["rationale"],
            "caveat": c["caveat"] + " Full egen rad 9 utvunnen i T-0676 med Alva Viktoria, längddag 1904-09-12 och samtliga 18 fält. Kolumnens kunskap/nattvard är tomma egna celler; v är en rå vaccinations-/koppsignal utan säker medicinsk tolkning. Strykningar och flyttditto bevaras i TR; ingen ny personidentitet eller senare livsslutsats.",
            "origins": [
                {"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]}
                for o in c["origins"]
            ],
            "evidence": old_evidence,
        }
    else:
        observation = {
            "id": observation_id,
            "kind": "observation",
            "expectedVersion": None,
            "data": observation_data,
            "disposition": "recorded",
            "evidenceStatus": "TRANSCRIBED",
            "rationale": f"T-0676: full egen rad {row} utvunnen kolumn 1–18 ur bevarad källbild; inga nya person- eller relationsslutsatser.",
            "caveat": "Denna observation återger en enda egen källrad och full avskrift. Två läsningar av samma bild är inte oberoende källor. Rå namn-, datum-, yrkes-, marginal-, stryknings- och dittoförbehåll ligger i TR. Tomma celler är endast denna rads tomma celler; ingen avsaknad i senare liv, död eller tjänst sluts.",
            "origins": [],
            "evidence": observation_evidence,
        }
    changes.extend([mention, observation])
    observations[row] = observation_id
    mentions[row] = mention_id

person_rows = {"P-0020": 1, "P-0023": 5, "P-0024": 6, "P-0025": 7, "P-0026": 8}
for change in DRAFT["changes"]:
    person_id = change["data"].get("subject_id") or (change["id"] if change["kind"] == "person" else None)
    if person_id in person_rows:
        row = person_rows[person_id]
        add_evidence(change, observations[row], 1, "supports", f"Egen fullradobservation Värsås r{row}; ett källled, ingen ny oberoende röst.")
        add_evidence(change, f"TR-T0676-VARSAS-r{row}", 1, "supports", f"Full reserverad 18-kolumnsläsning av egen rad {row}.")
        add_evidence(change, "AUDIT-T0676-22", 1, "context", "Värsås fullfältiga radgranskning och återbruk r2–4.")
    elif person_id == "P-0010":
        add_evidence(change, "O-P-0010-C0917-full-row", 1, "supports", "Befintlig egen Bernhardrad i samma avgränsade källa; ingen ny bildröst.")
        add_evidence(change, "AUDIT-T0676-22", 1, "context", "Värsås auditerad fullfältstäckning och återbrukade familjerader.")
    else:
        raise AssertionError((change["id"], person_id))
    changes.append(change)

assert len(changes) == 169
assert len({c["id"] for c in changes}) == 169
operation = {
    "id": "T-0676/varsas-followup-v2-proposed-revised",
    "actor": "Codex",
    "reason": "T-0676: 241 Astra-godkända fältpreciseringar i 153 objekt efter full egenradsavskrift av Värsås folio 134. Åtta råa radmentions och sju nya plus en reviderad fullradsobservation; r9 återbrukar befintligt O. Ingen ny identity eller person för tjänsterader 23–24.",
    "dependencyReviewVersion": 2,
    "changes": changes,
}
OUTPUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {
    "task": "T-0676",
    "mode": "PROPOSAL_ONLY",
    "rootDecision": "Revidera O-P-0027-household-134-fields@1 till full rad9; åtta M men inga nya identity-objekt. Ingen P för r23/24.",
    "decisionSha256": "e3d1ca97394b88a6be6ad9ed6f01579d6ee2caa6999d0f753e6a7e7132b0fe06",
    "duplicateCheck": "varsas-full-R-observation-mention-duplicate-check-20260924.json",
    "operation": str(OUTPUT.relative_to(ROOT)),
    "operationSha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    "counts": {"researchRevisions": 153, "fieldReplacements": 241, "newMentions": 8, "newObservations": 7, "revisedObservation": 1, "totalChanges": 169},
    "rowObservationIds": observations,
    "rowMentionIds": mentions,
    "canonicalApply": False,
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": str(OUTPUT), "sha256": report["operationSha256"], "counts": report["counts"]}, ensure_ascii=False))
