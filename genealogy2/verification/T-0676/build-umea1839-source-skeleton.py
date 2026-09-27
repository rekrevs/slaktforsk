"""Build seven Umeå 1839 source-layer pairs; incomplete, never apply alone."""

import hashlib
import json
import sqlite3
import subprocess
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COMPARISON = HERE / "umea1839-full-comparison-proposed-v2-20260924.json"
SOURCE_APPROVAL = HERE / "umea1839-comparison-v2-root-approval-20260924.json"
BASE_FOLLOWUP = HERE / "umea1839-followup-decisions-proposed-v3-20260924.json"
ADDENDUM = HERE / "umea1839-followup-v3-addendum-v2-20260924.json"
SCOPE = HERE / "scope.json"
OUTPUT = HERE / "umea1839-source-layer-skeleton-20260924.json"
assert hashlib.sha256(COMPARISON.read_bytes()).hexdigest() == "88effca2d2b0e6d012a03de5f38762ba47abbaff15c3e5e03458ee1111f0d555"
assert hashlib.sha256(BASE_FOLLOWUP.read_bytes()).hexdigest() == "e6a4f32b79698965080d8c04b83dd63ebb4503362ebea88ef33c5f61feacca74"
comparison = json.loads(COMPARISON.read_text())
approval = json.loads(SOURCE_APPROVAL.read_text())
addendum = json.loads(ADDENDUM.read_text())
scope = json.loads(SCOPE.read_text())
assert approval["comparison_sha256"] == hashlib.sha256(COMPARISON.read_bytes()).hexdigest()
assert approval["status"] == "SOURCE_COMPARISON_APPROVED_CURRENT_FOLLOWUPS_PENDING"
assert addendum["base_sha256"] == hashlib.sha256(BASE_FOLLOWUP.read_bytes()).hexdigest()

SCOPE_NUMBERS = (5, 6, 21, 30, 33, 41, 46)
REVISED_RECORDS = {21, 33}
record_by_scope = {n: next(r for r in scope["records"] if r["number"] == n) for n in SCOPE_NUMBERS}
assert len({r["record"] for r in record_by_scope.values()}) == 7
assert len(comparison["fields"]) == 288 and len(comparison["headers"]) == 18
assert len({f["row"] for f in comparison["fields"]}) == 16
assert all(f["header"] == comparison["headers"][f["column"] - 1]["proposed"] for f in comparison["fields"])

db = sqlite3.connect(ROOT / "genealogy2/data/research.sqlite")
db.row_factory = sqlite3.Row
changes = []
alias_map = []
count_by_scope = {}
for n in SCOPE_NUMBERS:
    rid = record_by_scope[n]["record"]
    current = json.loads(subprocess.check_output(["node", "genealogy2/cli.mjs", "inspect", rid], cwd=ROOT, text=True))
    assert current["kind"] == "record" and current["currentVersion"] == 1
    assert len(current["current"]["media"]) == 1
    assert current["current"]["media"][0]["sha256"] == comparison["source"]["sha256"]
    target_revision = 2 if n in REVISED_RECORDS else 1
    own_fields = [f for f in comparison["fields"] if f["scope"] == n]
    rows = sorted({f["row"] for f in own_fields})
    assert len(own_fields) == len(rows) * 18
    assert all([f["column"] for f in own_fields if f["row"] == row] == list(range(1, 19)) for row in rows)
    assert all(f["record_revision"] == f"{rid}@1" for f in own_fields)
    old_tr = [r["revision_id"] for r in db.execute("select t.revision_id from transcription t join revision v on v.id=t.revision_id where t.record_id=? and v.version=(select max(v2.version) from revision v2 where v2.object_id=v.object_id)", (rid,))]
    own_reserved = [v for v in comparison["reserved_problem_positions"] if v.get("row") in rows]
    own_differences = [v for v in comparison["differences"] if v.get("row") in rows]
    own_non_grid = [v for v in comparison["extra_non_grid_reuse"] if v.get("row") in rows]
    tr_id = f"TR-T0676-UMEA1839-SCOPE-{n}"
    audit_id = f"AUDIT-T0676-UMEA1839-{n}"
    prior_evidence = [{"object": rev.rsplit("@", 1)[0], "version": int(rev.rsplit("@", 1)[1]), "role": "context", "note": "Äldre avskrift bevaras historiskt med ursprunglig proveniens; ingen ytterligare oberoende källa."} for rev in old_tr]
    body = {
        "task": "T-0676", "scope": n, "record_id": rid,
        "source": comparison["source"], "printed_headers_18": comparison["headers"],
        "own_rows": rows, "own_18_column_fields_exact_approved_comparison": own_fields,
        "comparison_file": str(COMPARISON.relative_to(ROOT)), "comparison_sha256": hashlib.sha256(COMPARISON.read_bytes()).hexdigest(),
        "locked_read_inputs": comparison["inputs"],
        "own_differences_with_FIRST_SECOND_and_adjudication": own_differences,
        "own_reserved_problem_positions": own_reserved,
        "own_extra_non_grid_documentary_reuse": own_non_grid,
        "source_comparison_status": "approved by root Astra; current follow-up and evidence integration remain pending",
        "record_binding_after_followup": f"{rid}@{target_revision}",
        "record_revision_in_comparison": f"{rid}@1",
        "limits": approval["limits"],
        "historical_layers": "Existing TR revisions remain unchanged; DOCUMENTARY_REUSE fields retain their individual evidence and do not become new original readings.",
    }
    changes.append({"id": tr_id, "kind": "transcription", "expectedVersion": None,
                    "data": {"record_id": rid, "text": json.dumps(body, ensure_ascii=False, indent=2), "reading_note": f"Umeå stad AIIa/5e fol1839 scope{n}: {len(rows)} egna rader ×18 kolumner; återbruk, FIRST/SECOND, radplacering och kvarvarande råreservationer bevarade. Ingen rad utanför egen R räknas in."},
                    "disposition": "recorded", "evidenceStatus": None,
                    "rationale": "T-0676: rootgodkänd full egen fältjämförelse för avgränsad källpost, utan ny oberoende historisk röst.",
                    "caveat": "Färgade årsmarkeringar, n/u och v/F-lika tecken samt svaga gränsnoter kvarstår reserverade. Tomma/dittotecken ger inga negativa livsfakta eller obruten vistelse.",
                    "origins": [], "evidence": [{"object": rid, "version": target_revision, "role": "derived_from", "note": f"Egen befintlig källpost scope{n}; R@{target_revision} måste skapas före denna TR om R revideras."}, *prior_evidence]})
    audit_body = {"task": "T-0676", "scope": n, "record_id": rid, "record_revision": f"{rid}@{target_revision}", "comparison_sha256": hashlib.sha256(COMPARISON.read_bytes()).hexdigest(), "rows": rows, "printed_columns_per_row": 18, "positions": len(own_fields), "reserved_problem_positions": own_reserved, "differences": own_differences, "non_grid_reuse": own_non_grid, "limits": approval["limits"], "no_new_identity_or_pedigree_gate": True}
    changes.append({"id": audit_id, "kind": "assessment", "expectedVersion": None,
                    "data": {"subject_id": rid, "criteria": "source_record_review/1", "outcome": "reviewed_with_reservations", "body": json.dumps(audit_body, ensure_ascii=False, indent=2)},
                    "disposition": "recorded", "evidenceStatus": None,
                    "rationale": "T-0676: egna rader och 18 kolumnpositioner per rad källgranskade med separata återbruks- och FIRST/SECOND-lager.",
                    "caveat": "Samma originalbild och historiska TR är en informationsväg; inga nytolkade identiteter, datumintervall eller personrelationer följer av blanka celler.",
                    "origins": [], "evidence": [
                        {"object": rid, "version": target_revision, "role": "derived_from", "note": "Egen källposts avgränsning och bevarad originalbild."},
                        {"object": tr_id, "version": 1, "role": "supports", "note": "Fullt, versionsbundet egenradsprotokoll med äldre återbruk och godkänd jämförelse."},
                    ]})
    proposed = next(item for item in addendum["future_transcription_and_audit_plan"] if item["record_id"] == rid)
    assert proposed["required_record_revision"] == f"{rid}@{target_revision}" and proposed["rows"] == rows
    alias_map.append({"scope": n, "record": rid, "rows": rows,
                      "root_specified_TR": tr_id, "root_specified_AUDIT": audit_id,
                      "addendum_proposed_TR_alias": proposed["proposed_transcription_id"],
                      "addendum_proposed_AUDIT_alias": proposed["proposed_audit_id"],
                      "current_followup_evidence_map_must_use": {"TR": f"{tr_id}@1", "AUDIT": f"{audit_id}@1"}})
    count_by_scope[str(n)] = {"rows": rows, "positions": len(own_fields), "oldTRPreserved": old_tr, "recordRevisionForFutureOperation": target_revision}

assert len(changes) == 14 and sum(v["positions"] for v in count_by_scope.values()) == 288
assert sum(len(v["rows"]) for v in count_by_scope.values()) == 16
out = {
    "task": "T-0676", "status": "INCOMPLETE_SOURCE_LAYER_SKELETON_DO_NOT_APPLY_OR_PREFLIGHT",
    "baseline": "canonical journal178, pending0 at skeleton preparation; no operation mutation performed",
    "sourceComparisonSha256": hashlib.sha256(COMPARISON.read_bytes()).hexdigest(),
    "sourceComparisonApprovalSha256": hashlib.sha256(SOURCE_APPROVAL.read_bytes()).hexdigest(),
    "followupV3Sha256": hashlib.sha256(BASE_FOLLOWUP.read_bytes()).hexdigest(),
    "unapprovedAddendumV2Sha256": hashlib.sha256(ADDENDUM.read_bytes()).hexdigest(),
    "sourceChangesForLaterIntegration": changes,
    "explicitAliasMapNoPrefixInference": alias_map,
    "countsByScope": count_by_scope,
    "integrationRequirements": ["Astra final approval of merged follow-up decisions/addendum and explicit 153-object evidence map", "Place R33@2 and R21@2 before their TR; keep record evidence source-only so no R→TR cycle", "Rebind all proposed evidence-map heads to explicit root-specified TR/AUDIT IDs above", "Only then form complete operation and run isolated apply plus verify, verify-assets, verify-source and full prospective pending review"],
    "canonicalApply": False, "tempApply": False,
}
OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"file": str(OUTPUT.relative_to(ROOT)), "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), "sourceChanges": len(changes), "positions": 288}, ensure_ascii=False))
