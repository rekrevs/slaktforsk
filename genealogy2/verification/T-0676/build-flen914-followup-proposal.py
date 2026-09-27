"""Prepare the three approved Flen 914 scopes without changing canonical data."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECISIONS = HERE / "flen914-followup-decisions-20260924.json"
COMPARISON = HERE / "flen914-missing-fields-comparison-20260924.json"
ROOT_REVIEW = HERE / "flen914-followup-root-review-20260924.json"
OUTPUT = HERE / "flen914-followup-proposed-operation.json"
REPORT = HERE / "flen914-followup-proposal-build-20260924.json"
assert hashlib.sha256(DECISIONS.read_bytes()).hexdigest() == "f35fba44e0179ac714298d3ec90420846963b3c47019b3995aab450c9eadd32f"
assert hashlib.sha256(COMPARISON.read_bytes()).hexdigest() == "5e4712195385cbc5df34bfbf5e1af92cef5cca9f43947d5d7d544e6c14b28dfe"
decisions = json.loads(DECISIONS.read_text())
comparison = json.loads(COMPARISON.read_text())
review = json.loads(ROOT_REVIEW.read_text())
assert review["sha256"] == hashlib.sha256(DECISIONS.read_bytes()).hexdigest()

SCOPE = {
    25: ("R-9ec895e7d357de6e8838f6b7", "TR-ec4b5dbf9a3d993e9c21e7b1", [24, 25, 26]),
    26: ("R-a08263c57fcf29d3c4721deb", None, [15, 16, 17]),
    49: ("R-fadebbf807b34033b5afaea0", "TR-cd9f62e9ca892b586b7c0809", [9, 10, 11, 12]),
}
TR = {scope: f"TR-T0676-FLEN914-{scope}" for scope in SCOPE}
AUDIT = {scope: f"AUDIT-T0676-FLEN914-{scope}" for scope in SCOPE}
RELEVANCE = {
    "CONTRACT-P-0045-PK-05": (49, "r9 K.; r10–12 reserverade kol14-tecken och egna tomfält"),
    "THEME-P-0045-ARB": (49, "Torvalds egen r9 yrkes- och militärtext"),
    "THEME-P-0045-HAL": (49, "Torvalds/Mauds egna r9–12 råmarkeringar; inget medicinskt inferenssteg"),
    "THEME-P-0045-PER": (49, "Torvalds egen r9 yrkesrad och uttryckliga källgräns"),
    "THEME-P-0045-SAM": (49, "r9 K. samt svaga kol14-tecken r10–12"),
    "O-P-0046-A-4307-recorded_daughter_and_legitimation": (26, "Inga Ullas egen r17 och kolumnens v/tomfält"),
    "O-P-0045-A-3428-occupation_marriage_departure": (49, "Torvalds r9 och hushållets r10; K., kol14 och egna tomfält"),
    "O-P-0045-A-4309-daughters_report": (49, "Mauds/Maggis egna r11–12; v/tomfält och reserverade kol14-tecken"),
    "BIO-P-0045": (49, "Torvalds egen r9–12 familje-/yrkes-/militärtext med källgräns"),
}


def inspect(object_id):
    return json.loads(subprocess.check_output(["node", "genealogy2/cli.mjs", "inspect", object_id], cwd=ROOT, text=True))


def evidence(current):
    return [{"object": e["basis_revision_id"].rsplit("@", 1)[0], "version": int(e["basis_revision_id"].rsplit("@", 1)[1]), "role": e["role"], "note": e["note"]} for e in current["evidence"]]


def origins(current):
    return [{"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]} for o in current["origins"]]


rows = comparison["rows"]
assert len(comparison["headers"]) == 18 and len(rows) == 10
assert [(r["row"], r["scope"], r["record"]) for r in rows] == [(9, 49, SCOPE[49][0]), (10, 49, SCOPE[49][0]), (11, 49, SCOPE[49][0]), (12, 49, SCOPE[49][0]), (15, 26, SCOPE[26][0]), (16, 26, SCOPE[26][0]), (17, 26, SCOPE[26][0]), (24, 25, SCOPE[25][0]), (25, 25, SCOPE[25][0]), (26, 25, SCOPE[25][0])]
assert all([f["column"] for f in r["fields"]] == list(range(1, 19)) for r in rows)
new = [f for r in rows for f in r["fields"] if f["mode"] == "ny avgränsad FIRST-komplettering"]
reused = [f for r in rows for f in r["fields"] if f["mode"] == "återbruk utan ny läsprövning"]
assert len(new) == 66 and len(reused) == 114 and comparison["count"]["positions"] == 180
for d in decisions["new_raw_fields_for_required_TR_AUDIT"]:
    f = next(f for r in rows if r["row"] == d["row"] and r["scope"] == d["scope"] and r["record"] == d["record_id"] for f in r["fields"] if f["column"] == d["column"])
    assert f["mode"] == "ny avgränsad FIRST-komplettering"
    assert f["status"] == d["status"] and f["raw_new"] == d["raw"]
    assert comparison["headers"][str(d["column"])] == d["header"]

changes = []
scope_report = {}
for scope, (record_id, old_tr, expected_rows) in SCOPE.items():
    record = inspect(record_id)
    assert record["kind"] == "record" and record["currentVersion"] == 1
    asset = record["current"]["media"]
    assert len(asset) == 1 and asset[0]["sha256"] == comparison["source"]["sha256"]
    if old_tr:
        prior = inspect(old_tr)
        assert prior["kind"] == "transcription" and prior["currentVersion"] == 1 and prior["current"]["record_id"] == record_id
    scope_rows = [r for r in rows if r["scope"] == scope]
    assert [r["row"] for r in scope_rows] == expected_rows
    tr_body = {
        "task": "T-0676", "scope": scope, "record_id": record_id,
        "source": comparison["source"], "printed_headers_18": comparison["headers"],
        "rows_complete_reuse_plus_gaps": scope_rows,
        "geometric_marks": comparison["geometric_marks"], "limits": comparison["limits"],
        "method": "Varje kolumnposition behåller jämförelsens status och adjudikation; återbruk är ingen ny diplomatisk läsning. Rad26 är fortsättning under tryckt rad25.",
    }
    tr_evidence = [{"object": record_id, "version": 1, "role": "derived_from", "note": f"Befintlig egen källpost för scope{scope}, med bevarad bild och radgräns."}]
    if old_tr:
        tr_evidence.append({"object": old_tr, "version": 1, "role": "context", "note": "Äldre avskrift återbrukas med historisk provenance och sina reservationer; ingen ny oberoende källa."})
    changes.append({
        "id": TR[scope], "kind": "transcription", "expectedVersion": None,
        "data": {"record_id": record_id, "text": json.dumps(tr_body, ensure_ascii=False, indent=2), "reading_note": f"Flen AIIa/4c folio914 scope{scope}: 18 tryckta rubriker per rad, {len(scope_rows)} rader; äldre positiva fält återbrukade utan ny läsprövning och luckor kompletterade enligt FIRST/SECOND. Råa K./v/ditton förblir oexpanderade; egna tomceller ger inga negativa livsfakta."},
        "disposition": "recorded", "evidenceStatus": None,
        "rationale": "T-0676: full relevant fälttäckning per avgränsad källa med bevarad äldre avskrift och explicit ny råkomplettering.",
        "caveat": "Råmarkeringar, svaga ditton, namnfortsättningar och egna tomfält har jämförelsens individuella reservationer. Ingen ny identitet, familjekant eller PK-/trädstatus.",
        "origins": [], "evidence": tr_evidence,
    })
    audit_body = {
        "task": "T-0676", "scope": scope, "record_id": record_id,
        "comparison_file": str(COMPARISON.relative_to(ROOT)),
        "comparison_sha256": hashlib.sha256(COMPARISON.read_bytes()).hexdigest(),
        "rows": expected_rows, "printed_columns_per_row": 18,
        "reused_positions": sum(f["mode"] == "återbruk utan ny läsprövning" for r in scope_rows for f in r["fields"]),
        "newly_completed_positions": sum(f["mode"] == "ny avgränsad FIRST-komplettering" for r in scope_rows for f in r["fields"]),
        "limits": comparison["limits"], "source": comparison["source"],
        "no_new_identity_or_pedigree_gate": True,
    }
    changes.append({
        "id": AUDIT[scope], "kind": "assessment", "expectedVersion": None,
        "data": {"subject_id": record_id, "criteria": "source_record_review/1", "outcome": "reviewed_with_reservations", "body": json.dumps(audit_body, ensure_ascii=False, indent=2)},
        "disposition": "recorded", "evidenceStatus": None,
        "rationale": "T-0676: rad- och kolumngränser samt full relevant fälttäckning sakgranskade med bevarade reservationer.",
        "caveat": "En och samma originalbild; äldre och nya läslager är inte oberoende källröster. Inga identitets-/släkt- eller livskontraktsslutsatser från tomma/råa celler.",
        "origins": [], "evidence": [
            {"object": record_id, "version": 1, "role": "derived_from", "note": f"Befintlig egen källpost scope{scope}."},
            {"object": TR[scope], "version": 1, "role": "supports", "note": "Fullt 18-kolumnsprotokoll med separerat historiskt återbruk och nya luckor."},
        ],
    })
    scope_report[str(scope)] = {"record": record_id, "rows": expected_rows, "oldTRPreserved": old_tr, "reused": audit_body["reused_positions"], "new": audit_body["newly_completed_positions"]}

data_fields = {
    "assessment": ("subject_id", "criteria", "outcome", "body"),
    "observation": ("record_id", "mention_id", "property", "value_literal", "value_json"),
    "narrative": ("subject_id", "title", "markdown"),
}
revisions = [d for d in decisions["decisions"] if d["decision"] == "REVISE_FIELDS"]
assert len(revisions) == 9 and {d["object_id"] for d in revisions} == set(review["approved_revisions"]) == set(RELEVANCE)
revision_report = []
for d in revisions:
    object_id = d["object_id"]
    v = inspect(object_id)
    current = v["current"]
    assert v["kind"] == d["kind"] and v["currentVersion"] == 1 and d["current_revision"] == current["revision_id"]
    assert current == d["before_current"], object_id
    assert d["retain_all_unlisted_fields"] is True
    after = dict(current)
    for key, value in d["exact_after_fields"].items():
        assert key in (*data_fields[v["kind"]], "caveat")
        after[key] = value
    data = {key: after[key] for key in data_fields[v["kind"]]}
    if v["kind"] == "observation" and isinstance(data["value_json"], str):
        data["value_json"] = json.loads(data["value_json"])
    e = evidence(current)
    scope, relevance = RELEVANCE[object_id]
    e.extend([
        {"object": TR[scope], "version": 1, "role": "supports", "note": f"Relevant egen fältgrund: {relevance}."},
        {"object": AUDIT[scope], "version": 1, "role": "context", "note": f"Sakgranskad rad-/kolumngräns för {relevance}; ingen ytterligare oberoende röst."},
    ])
    changes.append({
        "id": object_id, "kind": v["kind"], "expectedVersion": 1,
        "data": data, "disposition": current["disposition"],
        "evidenceStatus": current["evidence_status"], "rationale": current["rationale"],
        "caveat": after["caveat"], "origins": origins(current), "evidence": e,
    })
    revision_report.append({"object": object_id, "newTR": TR[scope], "audit": AUDIT[scope], "relevantRows": relevance, "exactAfterFields": sorted(d["exact_after_fields"])})

assert len(changes) == 15
operation = {
    "id": "T-0676/flen914-scopes25-26-49-proposed",
    "actor": "Codex",
    "reason": "T-0676: Astra-godkända nio fälträttelser samt full 18-kolumnsutvinning för tre avgränsade Flen914-poster; 114 historiskt återbrukade och 66 nya råpositioner. Inga O/M, identiteter eller familjekanter tillkommer.",
    "dependencyReviewVersion": 2,
    "changes": changes,
}
OUTPUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {
    "task": "T-0676", "mode": "PROPOSAL_ONLY", "canonicalApply": False,
    "decisionSha256": hashlib.sha256(DECISIONS.read_bytes()).hexdigest(),
    "comparisonSha256": hashlib.sha256(COMPARISON.read_bytes()).hexdigest(),
    "operation": str(OUTPUT.relative_to(ROOT)), "operationSha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    "changeCount": len(changes), "newTranscriptions": 3, "newAudits": 3,
    "newObservations": 0, "newMentions": 0, "revisions": revision_report,
    "scopes": scope_report,
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": report["operation"], "sha256": report["operationSha256"], "changes": len(changes), "scopes": scope_report}, ensure_ascii=False))
