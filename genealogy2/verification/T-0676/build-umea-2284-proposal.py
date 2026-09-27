#!/usr/bin/env python3
"""Build the bounded, root-approved Umeå 2284 native proposal."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
comparison = json.loads((HERE / "umea-2284-comparison-20260924.json").read_text())
decisions = json.loads((HERE / "umea-2284-followup-decisions-20260924.json").read_text())
record = comparison["record_revision"].split("@")[0]
changes = []

for row in comparison["rows"]:
    n = row["row"]
    payload = {
        "source": {"locator": comparison["locator"], "record_revision": comparison["record_revision"],
                   "media": comparison["source"], "row": n},
        "inputs": comparison["inputs"], "exposure": comparison["exposure"],
        "headers": comparison["headers"], "fields": row["fields"],
        "first_marginalia": row.get("first_marginalia"),
        "second_row_marks": row.get("second_row_marks"),
        "ditto_limit": row.get("ditto_limit"),
        "margins": [m for m in comparison["margins"] if m["row"] == n],
        "limits": comparison["limits"],
    }
    assert len(payload["fields"]) == 18 and [f["column"] for f in payload["fields"]] == list(range(1, 19))
    changes.append({
        "id": f"TR-T0676-UMEA2284-r{n}", "kind": "transcription", "expectedVersion": None,
        "data": {"record_id": record, "text": json.dumps(payload, ensure_ascii=False, indent=2),
                 "reading_note": "Två låsta läsningar och rootgodkänd jämförelse; alla 18 egna fält, råformer och reservationer. Ingen ny oberoende evidensröst."},
        "disposition": "recorded", "evidenceStatus": "TRANSCRIBED",
        "rationale": f"T-0676 AK1–2: full egenfältsavskrift av Umeå A II a/23 folio 2284 rad {n}; båda läsningar och varje adjudikering bevaras.",
        "caveat": "Råditton, svaga tecken, strykningar och tomma celler behåller jämförelsens gränser; texten ensam fastställer inte personfakta eller status.",
        "origins": [], "evidence": [{"object": record, "version": 1, "role": "derived_from", "note": "Samma versionsbundna källpost och bevarade helbild; ingen extra oberoende röst."}],
    })

assert len(changes) == 12 and sum(len(r["fields"]) for r in comparison["rows"]) == 216
audit_id = "AUDIT-T0676-10"
changes.append({
    "id": audit_id, "kind": "assessment", "expectedVersion": None,
    "data": {"subject_id": record, "criteria": "source_record_review/1", "outcome": "reviewed_with_reservations",
             "body": "T-0676 AK1–2: Umeå landsförsamling A II a/23 folio 2284 rader 12–23; 12 fulla radavskrifter, vardera 18 egna tryckta kolumner (216 fält). Två låsta läsningar och rootgodkänd jämförelse: " +
             "; ".join(f"{i['path']} SHA256 {i['sha256']}" for i in comparison["inputs"]) +
             "; jämförelse SHA256 605536a392ad6b55ca98855aca801f8dfd27edbb35a0a22de36d61a3fc8800cc. Media SHA256 " + comparison["source"]["sha256"] +
             ". Läsarnas exponeringshistoria, alla marginalia, fulla rubriker, råditton, separata strykningar och fältreservationer finns i respektive TR. Gränser: " + " ".join(comparison["limits"])},
    "disposition": "recorded", "rationale": "T-0676 full källpostgranskning av avgränsad passage, med uttryckliga läs- och tolkningsreservationer.",
    "caveat": "Samma historiska källa ger ingen extra oberoende evidensröst. Ingen personcore, relation, ägarkunskap eller identitetsgrind avgörs.",
    "origins": [], "evidence": [{"object": record, "version": 1, "role": "derived_from", "note": "Versionsbunden källpost och dess redan bundna helbild."}] +
    [{"object": f"TR-T0676-UMEA2284-r{n}", "version": 1, "role": "supports", "note": f"Full 18-fältsavskrift, rad {n}."} for n in range(12, 24)],
})

metadata = {"revision_id", "object_id", "version", "kind", "disposition", "evidence_status", "rationale", "caveat", "origins", "evidence", "pending_reviews"}
for decision in decisions["decisions"]:
    if decision["decision"] != "REVISE":
        continue
    before = decision["before_data"]
    data = {k: v for k, v in before.items() if k not in metadata}
    for key, value in decision["exact_after_fields"].items():
        if key != "caveat":
            data[key] = value
    for key in ("value_json", "date_json", "scope_json"):
        if isinstance(data.get(key), str):
            data[key] = json.loads(data[key])
    evidence = [{"object": e["basis_revision_id"].rsplit("@", 1)[0],
                 "version": int(e["basis_revision_id"].rsplit("@", 1)[1]),
                 "role": e["role"], "note": e["note"]} for e in before["evidence"]]
    # New transcription and audit support the precise source-bound correction.
    row = 14 if "0529" in decision["object_id"] else 20 if "0035" in decision["object_id"] else 23
    evidence.extend([
        {"object": f"TR-T0676-UMEA2284-r{row}", "version": 1, "role": "supports", "note": "Full egenfältsavskrift; samma historiska källa."},
        {"object": audit_id, "version": 1, "role": "supports", "note": "Källpostgranskning med reservationer; ingen extra oberoende röst."},
    ])
    changes.append({"id": decision["object_id"], "kind": decision["kind"],
                    "expectedVersion": decision["currentVersion"], "data": data,
                    "disposition": before["disposition"], "evidenceStatus": before["evidence_status"],
                    "rationale": decision["rationale"],
                    "caveat": decision["exact_after_fields"].get("caveat", before["caveat"]),
                    "origins": [{"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]} for o in before["origins"]],
                    "evidence": evidence})

assert len(changes) == 24 and sum(d["decision"] == "REVISE" for d in decisions["decisions"]) == 11
operation = {"id": "T-0676/umea-2284-full-fields-followup-v1", "actor": "Codex",
             "reason": "T-0676 AK1–2: rootgodkänd 216-fältsavskrift och källpostgranskning av Umeå 2284 samt elva individuellt godkända följdrevisioner. Tjugo RETAIN-beslut är villkorliga och löses inte i denna operation.",
             "dependencyReviewVersion": 2, "changes": changes}
out = HERE / "umea-2284-proposed-operation.json"
out.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
print(out, len(changes))
