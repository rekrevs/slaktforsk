#!/usr/bin/env python3
"""Prepare the approved Floda 592 four-record batch, without canonical apply."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = json.loads((HERE / "floda592-full-comparison-proposed-20260924.json").read_text())
D = json.loads((HERE / "floda592-followup-decisions-20260924.json").read_text())
A = json.loads((HERE / "floda592-root-preparation-approval-20260924.json").read_text())
assert hashlib.sha256((HERE / "floda592-full-comparison-proposed-20260924.json").read_bytes()).hexdigest() == A["comparison_sha256"]
assert hashlib.sha256((HERE / "floda592-followup-decisions-20260924.json").read_bytes()).hexdigest() == A["followup_sha256"]
assert C["count"] == {"positions": 90, "documentary_reuse": 39, "new_gap_positions": 51, "headers": 18, "material_disagreements": 0, "notation_differences": 5}

groups = [
    (4, [11], "R-17d23f9ff2cc4bbb7ff0a612", "TR-T0676-FLODA592-r11", "AUDIT-T0676-4"),
    (12, [5], "R-37e908ab3317bcf79c389d1c", "TR-T0676-FLODA592-r5", "AUDIT-T0676-12"),
    (28, [12], "R-a2f5b5fa3781291a541749f1", "TR-T0676-FLODA592-r12", "AUDIT-T0676-28"),
    (47, [1, 2], "R-f11fd1003f2598b60b9f0fc5", "TR-T0676-FLODA592-r1-r2", "AUDIT-T0676-47"),
]
changes = []
record_map = {}
for scope, rows, record, tr, audit in groups:
    fields = [x for x in C["fields"] if x["row"] in rows]
    assert len(fields) == 18 * len(rows) and all(x["record_id"] == record for x in fields)
    assert len({(x["row"], x["column"]) for x in fields}) == len(fields)
    assert set(x["column"] for x in fields) == set(range(1, 19))
    payload = {"source": C["source"], "scope": scope, "record_revision": record + "@1",
               "rows": rows, "headers": C["headers"], "fields": fields,
               "inputs": C["inputs"], "groups": [g for g in C["groups"] if any(p[0] in rows for p in g["positions"])],
               "differences": [x for x in C["differences"] if x["row"] in rows],
               "limits": C["limits"], "preserved_reuse_transcriptions": [
                   x for x in C["preserved_reuse_transcriptions"] if x["record_id"] == record]}
    changes.append({"id": tr, "kind": "transcription", "expectedVersion": None,
                    "data": {"record_id": record, "text": json.dumps(payload, ensure_ascii=False, indent=2),
                             "reading_note": "18 egna kolumner per rad med explicit återbruk, ny luckläsning, rågruppering och reservationer. Samma källa ger ingen extra oberoende röst."},
                    "disposition": "recorded", "evidenceStatus": "TRANSCRIBED",
                    "rationale": f"T-0676 scope{scope}: rootgodkänd fullfältjämförelse, rader {','.join(map(str,rows))}.",
                    "caveat": "Återbrukade fält, osäkra råtecken och tomma celler normaliseras inte till nya personfakta.",
                    "origins": [], "evidence": [{"object": record, "version": 1, "role": "derived_from", "note": "Egen befintlig källpost och dess bundna helbild."}]})
    changes.append({"id": audit, "kind": "assessment", "expectedVersion": None,
                    "data": {"subject_id": record, "criteria": "source_record_review/1", "outcome": "reviewed_with_reservations",
                             "body": f"T-0676 scope{scope}, Floda A II a/11 uppslag 592, rader {','.join(map(str,rows))}: {len(fields)} egna fält redovisade. " +
                             f"{sum(x['mode']=='DOCUMENTARY_REUSE' for x in fields)} dokumentärt återbruk och {sum(x['mode']!='DOCUMENTARY_REUSE' for x in fields)} nya luckpositioner. " +
                             "Jämförelse SHA256 78252c89deb18a9f7ffd60d4ca4ddb237d2b5b05a5a217a0925b01bd74ca7ed3. " + " ".join(C["limits"])},
                    "disposition": "recorded", "rationale": f"T-0676 scope{scope}: full avgränsad källpostgranskning med reservationer.",
                    "caveat": "Källrapport, inte ny P, relation, status, militärtjänst, religiös händelse eller normaliserat datum.",
                    "origins": [], "evidence": [{"object": record, "version": 1, "role": "derived_from", "note": "Egen källpost med helbild."},
                                                {"object": tr, "version": 1, "role": "supports", "note": "Full 18-kolumners egenfältsavskrift för detta R."}]})
    record_map[record] = (tr, audit)

new_o, new_as = D["creates"]
assert new_o["object_id"] == "O-T0676-C0912-r11-military-raw"
tr_arvid, audit_arvid = record_map[new_o["data"]["record_id"]]
changes.append({"id": new_o["object_id"], "kind": "observation", "expectedVersion": None,
                "data": new_o["data"], "disposition": new_o["disposition"],
                "evidenceStatus": new_o["evidence_status"], "rationale": new_o["rationale"], "caveat": new_o["caveat"],
                "origins": [], "evidence": [{"object": new_o["data"]["record_id"], "version": 1, "role": "supports", "note": "Arvids egen avgränsade källpost."},
                                            {"object": new_o["data"]["mention_id"], "version": 1, "role": "derived_from", "note": "Befintligt eget källomnämnande; ingen ny personidentitet."},
                                            {"object": tr_arvid, "version": 1, "role": "supports", "note": "Arvids eget råfält kolumn 15, reserverat."}]})
assert new_as["object_id"] == "AS-T0676-FLODA592-P-0010"
tr_bernhard, audit_bernhard = record_map["R-a2f5b5fa3781291a541749f1"]
changes.append({"id": new_as["object_id"], "kind": "assessment", "expectedVersion": None,
                "data": new_as["data"], "disposition": new_as["disposition"],
                "rationale": new_as["rationale"], "caveat": new_as["caveat"], "origins": [],
                "evidence": [{"object": tr_bernhard, "version": 1, "role": "supports", "note": "Bernhards egen fulla rad 12."},
                             {"object": audit_bernhard, "version": 1, "role": "supports", "note": "Bernhards eget granskade R."},
                             {"object": tr_arvid, "version": 1, "role": "context", "note": "Separat kontextrad Arvid, ingen personkoppling."},
                             {"object": new_o["object_id"], "version": 1, "role": "context", "note": "Arvids eget råfält hålls skilt från Bernhard."}] +
                            [{"object": tr, "version": 1, "role": "context", "note": "Separat befintlig källkontext på samma blad."} for _, _, _, tr, _ in groups if tr not in (tr_bernhard, tr_arvid)]})

metadata = {"revision_id", "object_id", "version", "kind", "disposition", "evidence_status", "rationale", "caveat", "origins", "evidence", "pending_reviews"}
diff = []
for d in D["decisions"]:
    if d["decision"] != "REVISE":
        continue
    current = json.loads(subprocess.check_output(["node", "genealogy2/cli.mjs", "inspect", d["object_id"]], text=True))["current"]
    if current["revision_id"] != d["current_revision"]:
        raise ValueError(f"Version changed: {d['object_id']}")
    data = {k: v for k, v in current.items() if k not in metadata}
    caveat = current["caveat"]
    for edit in d["fields"]:
        field = edit["field"]
        value = caveat if field == "caveat" else data[field]
        if value != edit["before"]:
            raise ValueError(f"Before mismatch: {d['object_id']}.{field}")
        if field == "caveat":
            caveat = edit["after"]
        else:
            data[field] = edit["after"]
    for key in ("value_json", "date_json", "scope_json"):
        if isinstance(data.get(key), str):
            data[key] = json.loads(data[key])
    evidence = [{"object": e["basis_revision_id"].rsplit("@",1)[0], "version": int(e["basis_revision_id"].rsplit("@",1)[1]),
                 "role": e["role"], "note": e["note"]} for e in current["evidence"]]
    evidence.extend([{"object": tr_bernhard, "version": 1, "role": "supports", "note": "Bernhards egen rad 12 och dess kompletterade råceller."},
                     {"object": audit_bernhard, "version": 1, "role": "supports", "note": "Egen källpostgranskning med reservationer."}])
    if d["object_id"] == "CONTRACT-P-0010-PK-05":
        evidence.extend({"object": tr, "version": 1, "role": "context",
                         "note": "Endast de separata kontextradernas celler; samma historiska källa ger ingen extra oberoende röst."}
                        for _, _, _, tr, _ in groups if tr != tr_bernhard)
    changes.append({"id": d["object_id"], "kind": current["kind"], "expectedVersion": current["version"],
                    "data": data, "disposition": current["disposition"], "evidenceStatus": current["evidence_status"],
                    "rationale": d["reason"], "caveat": caveat,
                    "origins": [{"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]} for o in current["origins"]],
                    "evidence": evidence})
    diff.append({"object_id": d["object_id"], "before_revision": current["revision_id"], "after_revision": f"{d['object_id']}@{current['version']+1}",
                 "fields": d["fields"], "origins_preserved": len(current["origins"]), "evidence_preserved": len(current["evidence"])})

assert len(changes) == 12 and len(diff) == 2
operation = {"id": "T-0676/floda592-scopes4-12-28-47-v2", "actor": "Codex",
             "reason": "T-0676: rootgodkända Floda592-fält för fyra egna R, 90 positioner, en ny Arvid-råobservation och Bernhards avgränsade adoption; två exakta följdrevisioner, tjugo retain orörda.",
             "dependencyReviewVersion": 2, "changes": changes}
for filename, content in [("floda592-scopes4-12-28-47-proposed-operation-v2.json", operation),
                          ("floda592-scopes4-12-28-47-diff-check-v2-20260924.json", diff)]:
    file = HERE / filename
    if file.exists():
        raise FileExistsError(file)
    file.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
print(len(changes), sum(len(x["fields"]) for x in diff))
