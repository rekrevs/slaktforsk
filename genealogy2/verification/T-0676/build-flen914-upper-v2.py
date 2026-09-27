"""Extend the reviewed six-row scope 45 proposal to all eight rows; prepare only."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIX = HERE / "flen914-upper-proposed-operation.json"
GAP = HERE / "flen914-r1-r3-gap-comparison-20260924.json"
ADDENDUM = HERE / "flen914-r1-r3-gap-followup-addendum-20260924.json"
OUT = HERE / "flen914-upper-proposed-operation-v2.json"
REPORT = HERE / "flen914-upper-proposal-build-v2-20260924.json"
assert hashlib.sha256(SIX.read_bytes()).hexdigest() == "0138672cc03c6890c6a04e848ce7001b03cb70c7311d3b237882665dfbf503da"
assert hashlib.sha256(GAP.read_bytes()).hexdigest() == "bcc60fea5e54863cde3989bcd3f3fea5d58694472885efbb15b6a63bb18a8ea5"
assert hashlib.sha256(ADDENDUM.read_bytes()).hexdigest() == "bc0ff35725d5acf527c84dd195993bd68d3ea26bdc1e527a6e8a63df80f3062a"
six = json.loads(SIX.read_text())
gap = json.loads(GAP.read_text())
add = json.loads(ADDENDUM.read_text())
RECORD = "R-e67bb6868b81121b2d3f0732"
TR = "TR-T0676-FLEN914-UPPER-45"
AUDIT = "AUDIT-T0676-FLEN914-UPPER-45"


def inspect(object_id):
    return json.loads(subprocess.check_output(["node", "genealogy2/cli.mjs", "inspect", object_id], cwd=ROOT, text=True))


def evidence(current):
    return [{"object": e["basis_revision_id"].rsplit("@", 1)[0], "version": int(e["basis_revision_id"].rsplit("@", 1)[1]), "role": e["role"], "note": e["note"]} for e in current["evidence"]]


def origins(current):
    return [{"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]} for o in current["origins"]]


assert len(six["changes"]) == 18
assert len(gap["fields"]) == 36 and gap["count"] == {"total_positions": 36, "documentary_reuse": 24, "new_gap_fields": 12}
assert [(r, [f["column"] for f in gap["fields"] if f["row"] == r]) for r in (1, 3)] == [(1, list(range(1, 19))), (3, list(range(1, 19)))]
assert sum(f["mode"] == "återbruk utan ny läsning" for f in gap["fields"]) == 24
assert sum(f["mode"] == "ny avgränsad FIRST/SECOND-luckläsning" for f in gap["fields"]) == 12
assert len([d for d in add["decisions"] if d["decision"] == "REVISE"]) == 1
assert len(add["creates"]) == 2
assert len([d for d in add["decisions"] if d["decision"] == "RETAIN_WITHIN_12_FIELD_IMPACT"]) == 9

changes = json.loads(json.dumps(six["changes"], ensure_ascii=False))
tr = next(c for c in changes if c["id"] == TR)
audit = next(c for c in changes if c["id"] == AUDIT)
tr_body = json.loads(tr["data"]["text"])
six_rows = tr_body["rows_2_4_5_6_7_8_full_fields"]
assert sum(len(r["fields"]) for r in six_rows) == 108
headers = tr_body["printed_headers_18"]
assert len(headers) == 18
for f in gap["fields"]:
    assert f["header"] == headers[str(f["column"])]

gap_rows = [{"row": row, "fields": [f for f in gap["fields"] if f["row"] == row]} for row in (1, 3)]
tr_body["rows_1_and_3_documentary_reuse_plus_new_gaps"] = gap_rows
tr_body["full_eight_row_inventory"] = sorted([*gap_rows, *six_rows], key=lambda r: r["row"])
tr_body["gap_comparison_file"] = str(GAP.relative_to(ROOT))
tr_body["gap_comparison_sha256"] = hashlib.sha256(GAP.read_bytes()).hexdigest()
tr_body["field_counts"] = {"rows": 8, "printed_columns_per_row": 18, "total": 144, "six_row_approved_comparison": 108, "rows_1_3_documentary_reuse": 24, "rows_1_3_new_gap_reading": 12}
tr_body["rows_1_3_adjudication"] = gap["adjudication"]
tr_body["rows_1_3_limits"] = gap["limits"]
tr_body["coverage_boundary"] = "Alla åtta rader 1–8 har nu 18 positioner. Rader1/3 skiljer 24 äldre dokumenterat återbruk från 12 nya tvåpasslästa luckfält. Övriga personer och källor utanför denna egen sidgrupp omfattas inte."
tr["data"]["text"] = json.dumps(tr_body, ensure_ascii=False, indent=2)
tr["data"]["reading_note"] = "Flen AIIa/4c folio914 övre grupp: fulla 8 rader ×18 tryckta kolumner. Rader2,4–8 har godkänd sexradersjämförelse; rader1/3 har 24 fält med äldre explicit dokumentär proveniens och 12 nyprövade luckfält. Inga tomma celler fylls från grannrad; namn/datum/markeringar behåller individuella reservationer."
tr["caveat"] = "Råa namn, datum och tecken står med sina individuella reservationer; återbruk betecknar inte ny bildläsning. Walter föredras men Wattin består som alternativ; Fl.-notens månadsled reserveras. Ingen ny P, identitet, familjekant eller PK-/trädstatus."

audit_body = json.loads(audit["data"]["body"])
audit_body["reviewed_rows"] = list(range(1, 9))
audit_body["reviewed_positions"] = 144
audit_body["row_1_3_gap_file"] = str(GAP.relative_to(ROOT))
audit_body["row_1_3_gap_sha256"] = hashlib.sha256(GAP.read_bytes()).hexdigest()
audit_body["row_1_3_counts"] = gap["count"]
audit_body["row_1_3_limits"] = gap["limits"]
audit_body["full_rows_1_and_3_reviewed_with_documentary_reuse_and_new_gaps"] = True
audit_body.pop("full_rows_1_and_3_not_claimed")
audit["data"]["body"] = json.dumps(audit_body, ensure_ascii=False, indent=2)
audit["rationale"] = "T-0676: alla åtta rader och 144 kolumnpositioner prövade, med explicit äldre proveniens för 24 återbrukade positioner på rader1/3 och 12 nya luckläsningar."
audit["caveat"] = "Återbruk är inte ny läsning. Egen tomcell, svagt spår och osäkert n/u ger inga nya person-, familje-, hälso- eller civilståndsslutsatser. Sexradersbeslutets reservationer består."

decision = next(d for d in add["decisions"] if d["decision"] == "REVISE")
object_id = decision["object_id"]
current_view = inspect(object_id)
current = current_view["current"]
assert current_view["kind"] == "observation" and current_view["currentVersion"] == 1
assert current["revision_id"] == decision["current_revision"] and len(decision["fields"]) == 2
after = dict(current)
for f in decision["fields"]:
    assert f["field"] in ("value_literal", "caveat") and current[f["field"]] == f["before"]
    after[f["field"]] = f["after"]
e = evidence(current)
e.extend([
    {"object": TR, "version": 1, "role": "supports", "note": "Just Astrids egen rad3 kolumn11/12 med a och n[?], inklusive FIRST:s n/u-reservation; r25 ändras inte."},
    {"object": AUDIT, "version": 1, "role": "context", "note": "Avgränsad granskning av rad3:s 18 positioner och skillnad mot äldre r25; ingen extra oberoende röst."},
])
changes.append({"id": object_id, "kind": "observation", "expectedVersion": 1,
                "data": {k: current[k] for k in ("record_id", "mention_id", "property", "value_json")} | {"value_literal": after["value_literal"]},
                "disposition": current["disposition"], "evidenceStatus": current["evidence_status"],
                "rationale": current["rationale"], "caveat": after["caveat"],
                "origins": origins(current), "evidence": e})
if isinstance(changes[-1]["data"]["value_json"], str):
    changes[-1]["data"]["value_json"] = json.loads(changes[-1]["data"]["value_json"])

for created in add["creates"]:
    assert created["kind"] == "assessment" and created["decision"] == "CREATE_BOUNDED_ADOPTION"
    assert inspect(created["object_id"]).get("currentVersion") is None
    changes.append({
        "id": created["object_id"], "kind": "assessment", "expectedVersion": None,
        "data": created["data"], "disposition": created["disposition"],
        "evidenceStatus": None, "rationale": created["rationale"], "caveat": created["caveat"],
        "origins": [], "evidence": [
            {"object": RECORD, "version": 1, "role": "derived_from", "note": "Befintlig egen C-0910-källpost för övre radgrupp, utan ny originalkopia."},
            {"object": TR, "version": 1, "role": "supports", "note": f"Fulla 18 kolumnpositioner på egen rad {'1' if created['data']['subject_id']=='P-0042' else '3'}; äldre återbruk skilt från nya luckfält."},
            {"object": AUDIT, "version": 1, "role": "context", "note": "Avgränsad källpostgranskning; inga nya person-/identitets- eller PK-/trädutfall."},
        ],
    })

assert len(changes) == 21
operation = {"id": "T-0676/flen914-upper-scope45-v2-proposed", "actor": "Codex", "reason": "T-0676: samlat godkänt fullfältprotokoll för 8×18 positioner på Flen914:s övre grupp, 16 individuella befintliga revisioner och tre bounded-adoptioner; inga nya O/M/P eller familjekanter.", "dependencyReviewVersion": 2, "changes": changes}
OUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {"task": "T-0676", "mode": "PROPOSAL_ONLY", "canonicalApply": False,
          "sixRowOperationSha256": hashlib.sha256(SIX.read_bytes()).hexdigest(),
          "gapComparisonSha256": hashlib.sha256(GAP.read_bytes()).hexdigest(),
          "addendumSha256": hashlib.sha256(ADDENDUM.read_bytes()).hexdigest(),
          "operation": str(OUT.relative_to(ROOT)), "operationSha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
          "changes": len(changes), "revisions": 16, "boundedAdoptions": 3,
          "fullFieldPositions": 144, "row1and3Reuse": 24, "row1and3New": 12,
          "addendumRetainsOnlyForTwelveFields": [d["object_id"] for d in add["decisions"] if d["decision"] == "RETAIN_WITHIN_12_FIELD_IMPACT"],
          "sourceBindingForAdditionalObservation": {"object": object_id, "TR": TR, "AUDIT": AUDIT, "specific": "own row3 col11/12, not row25"}}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": report["operation"], "sha256": report["operationSha256"], "changes": len(changes)}, ensure_ascii=False))
