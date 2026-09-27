#!/usr/bin/env python3
"""Prepare the approved scope-38 native operation without canonical apply."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
comparison = json.loads((HERE / "oskarshamn1208-comparison-20260924.json").read_text())
decisions = json.loads((HERE / "oskarshamn1208-followup-decisions-20260924.json").read_text())
assert decisions["summary"]["revisions"] == 22 and decisions["summary"]["retains"] == 46
record = "R-c66825545c5b93a96a19898a"
tr = "TR-T0676-OSKARSHAMN1208-r1"
new_o = "O-P-0010-C0915-supplementary-fields"
audit = "AUDIT-T0676-38"

# Explicit relevance for each revised object. The record itself is source-only.
SUPPORT = {
    "BIO-P-0010": [tr, new_o], "CONTRACT-P-0012-PK-07": [tr],
    "F-P-0010-household_membership-Oskarshamn1917-1923": [tr, new_o],
    "F-P-0010-military_registration-number": [tr],
    "KEY-P-0010-18e66fcaf655": [tr, new_o], "KEY-P-0010-27d1055ebecc": [tr],
    "KEY-P-0012-99e9b9b479d5": [tr], "O-P-0010-C0915-job": [tr],
    "O-P-0010-C0915-military": [tr], "P-0010/Q-02": [tr, new_o],
    "P-0012/Q-01": [tr], "PATH-P-0010-KP-06": [tr],
    "READ-cfa8d8ef4ef6e8b3d40b5707": [tr, new_o],
    "THEME-P-0010-ARB": [tr], "THEME-P-0010-BO": [tr, new_o],
    "P-0010/Q-04": [tr, new_o], "THEME-P-0010-HAL": [tr, new_o],
    "THEME-P-0010-MIL": [tr], "THEME-P-0010-SAM": [tr, new_o],
    "CONTRACT-P-0010-PK-05": [tr, new_o],
    "CONTRACT-P-0010-PK-12": [tr, new_o],
}
assert len(SUPPORT) == 21
FIELD_SUPPORT = {
    ("READ-cfa8d8ef4ef6e8b3d40b5707", "body"): [tr],
}

for d in decisions["decisions"]:
    live = json.loads(subprocess.check_output(["node", "genealogy2/cli.mjs", "inspect", d["object_id"]], text=True))["current"]
    if live != d["before_current"] or live["revision_id"] != d["current_revision"]:
        raise ValueError(f"Current version/content mismatch: {d['object_id']}")

metadata = {"revision_id", "object_id", "version", "kind", "disposition", "evidence_status",
            "rationale", "caveat", "origins", "evidence", "pending_reviews", "media", "readings", "transcriptions"}
approved = {d["object_id"]: d for d in decisions["decisions"] if d["decision"] == "REVISE_FIELDS"}
assert set(approved) == set(SUPPORT) | {record}
def origins(before):
    return [{"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]} for o in before["origins"]]
def prior_evidence(before):
    out = []
    for e in before["evidence"]:
        object_id, version = e["basis_revision_id"].rsplit("@", 1)
        if object_id in approved:
            version = str(approved[object_id]["before_current"]["version"] + 1)
        out.append({"object": object_id, "version": int(version), "role": e["role"], "note": e["note"]})
    return out

r = approved[record]
before = r["before_current"]
r_data = {k: v for k, v in before.items() if k not in metadata}
r_change = {"id": record, "kind": "record", "expectedVersion": before["version"], "data": r_data,
            "disposition": before["disposition"], "evidenceStatus": before["evidence_status"],
            "rationale": r["rationale"], "caveat": r["exact_after_fields"]["caveat"],
            "origins": origins(before),
            "evidence": prior_evidence(before),
            "assets": [{"path": a["path"], "region": a["region"]} for a in before["media"] if a["origin"] == "legacy"]}
assert len(r_change["assets"]) == len(before["media"]) == 1
assert len(r_change["evidence"]) == 1 and r_change["evidence"][0]["object"] == "S-0719"
assert r_data == {k: v for k, v in before.items() if k not in metadata}

tr_text = {"source": comparison["source"], "row": comparison["row"],
           "inputs": comparison["inputs"], "exposure": comparison["exposure"],
           "headers_note": comparison["headers_note"], "columns": comparison["columns"],
           "adjudication": comparison["adjudication"], "reuse_basis": comparison["reuse_basis"],
           "limits": comparison["limits"]}
assert len(tr_text["columns"]) == 18 and [c["column"] for c in tr_text["columns"]] == list(range(1, 19))
tr_change = {"id": tr, "kind": "transcription", "expectedVersion": None,
             "data": {"record_id": record, "text": json.dumps(tr_text, ensure_ascii=False, indent=2),
                      "reading_note": "Fulla 18 kolumner: återbrukade fält och sex nya luckfält; tre delreservationer. Två läsningar av samma källa ger inte extra oberoende röster."},
             "disposition": "recorded", "evidenceStatus": "TRANSCRIBED",
             "rationale": "T-0676 AK1–2 scope38: rootgodkänd full egenfältsjämförelse av Bernhards rad på uppslag 1208.",
             "caveat": "Tomma celler, b/N, struket 174[?], yrkesparentes och militärårsdel behåller jämförelsens gränser.",
             "origins": [], "evidence": [{"object": record, "version": 2, "role": "derived_from", "note": "Ny versionsbunden källpost med bevarad helbild."}]}

n = decisions["new_object_proposals"][0]
assert n["object_id_proposal"] == new_o and n["decision"] == "CREATE_PROPOSAL_AFTER_FULL_RECORD_DUPLICATE_CHECK"
o_fields = n["fields"]
o_change = {"id": new_o, "kind": "observation", "expectedVersion": None,
            "data": {k: json.loads(v) if k == "value_json" else v for k, v in o_fields.items() if k not in ("rationale", "caveat")},
            "disposition": "recorded", "evidenceStatus": "TRANSCRIBED",
            "rationale": o_fields["rationale"], "caveat": o_fields["caveat"],
            "origins": [], "evidence": [{"object": record, "version": 2, "role": "derived_from", "note": "Avgränsad personrad i ny källpostrevision."},
                                        {"object": tr, "version": 1, "role": "supports", "note": "Kolumner 7, 8, 11, 12, 13, 14 och 18, med reservationer."}]}
audit_change = {"id": audit, "kind": "assessment", "expectedVersion": None,
                "data": {"subject_id": record, "criteria": "source_record_review/1", "outcome": "reviewed_with_reservations",
                         "body": "T-0676 scope38, Oskarshamn A II a/6 uppslag 1208 rad1: 18 fulla egna kolumner i ny TR, med återbruk, sex nya luckfält och tre reserverade deltecken. Jämförelse SHA256 e38425bbdd33986a5061c8ac79bde3ad7552eeb8d45f89089c303b022bc10d9e. " + " ".join(comparison["adjudication"]) + " Gränser: " + " ".join(comparison["limits"])},
                "disposition": "recorded", "rationale": "T-0676 rootgodkänd full källpostgranskning med uttryckliga reservationer.",
                "caveat": "Ingen P-, identitets-, PK- eller trädgrindsändring. Äldre TR och avskriftsavvikelser bevaras historiskt.",
                "origins": [], "evidence": [{"object": record, "version": 2, "role": "derived_from", "note": "Ny källpostrevision med samma bevarade helbild."},
                                            {"object": tr, "version": 1, "role": "supports", "note": "Full 18-kolumners avskrift."},
                                            {"object": new_o, "version": 1, "role": "supports", "note": "Nya avgränsade råfält utan dubblering av äldre O."}]}

changes = [r_change, tr_change, o_change, audit_change]
field_map = []
for d in decisions["decisions"]:
    if d["decision"] != "REVISE_FIELDS" or d["object_id"] == record:
        continue
    b = d["before_current"]
    data = {k: v for k, v in b.items() if k not in metadata}
    for key, value in d["exact_after_fields"].items():
        if key != "caveat":
            data[key] = value
    for key in ("value_json", "date_json", "scope_json"):
        if isinstance(data.get(key), str):
            data[key] = json.loads(data[key])
    evidence = prior_evidence(b)
    for source in SUPPORT[d["object_id"]]:
        evidence.append({"object": source, "version": 1, "role": "supports",
                         "note": "T-0676 scope38 godkänd radbunden källgranskning; samma historiska källa."})
    evidence.append({"object": audit, "version": 1, "role": "supports", "note": "Scope38 full källpostgranskning med reservationer; ingen extra oberoende röst."})
    changes.append({"id": d["object_id"], "kind": d["kind"], "expectedVersion": b["version"],
                    "data": data, "disposition": b["disposition"], "evidenceStatus": b["evidence_status"],
                    "rationale": d["rationale"], "caveat": d["exact_after_fields"].get("caveat", b["caveat"]),
                    "origins": origins(b), "evidence": evidence})
    for field in d["exact_after_fields"]:
        field_sources = FIELD_SUPPORT.get((d["object_id"], field), SUPPORT[d["object_id"]])
        field_map.append({"object_id": d["object_id"], "field": field,
                          "sources": [f"{s}@1" for s in field_sources] + [f"{audit}@1"],
                          "limit": "Stöd endast för denna passages ändrade fält; tidigare biografi/källkedja inte generellt omgranskad."})
field_map.append({"object_id": record, "field": "caveat", "sources": ["S-0719@1"],
                  "limit": "R revideras före TR/O/AUDIT och har ingen bakåtlänk till dem."})
assert len(changes) == 25
operation = {"id": "T-0676/oskarshamn1208-scope38-v2", "actor": "Codex",
             "reason": "T-0676 scope38: rootgodkänd 18-fältsgranskning, en ny avgränsad råobservation och 22 exakta följdrevisioner; 46 retain förblir oförändrade.",
             "dependencyReviewVersion": 2, "changes": changes}
for name, value in [("oskarshamn1208-scope38-proposed-operation-v2.json", operation),
                    ("oskarshamn1208-scope38-evidence-map-v2-20260924.json", field_map)]:
    out = HERE / name
    if out.exists():
        raise FileExistsError(out)
    out.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
print(len(changes), len(field_map))
