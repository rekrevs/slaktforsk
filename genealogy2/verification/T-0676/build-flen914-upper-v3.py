"""Clarify historical proposal limits versus completed source review; prepare only."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = HERE / "flen914-upper-proposed-operation-v2.json"
OUT = HERE / "flen914-upper-proposed-operation-v3.json"
REPORT = HERE / "flen914-upper-proposal-build-v3-20260924.json"
assert hashlib.sha256(OLD.read_bytes()).hexdigest() == "211fc745ea7d6b1106b2de27c592780281127197a25b73df581145e52a9ecaf3"
operation = json.loads(OLD.read_text())
operation["id"] = "T-0676/flen914-upper-scope45-v3-proposed"
TR = next(c for c in operation["changes"] if c["id"] == "TR-T0676-FLEN914-UPPER-45")
AUDIT = next(c for c in operation["changes"] if c["id"] == "AUDIT-T0676-FLEN914-UPPER-45")
tr_body = json.loads(TR["data"]["text"])
audit_body = json.loads(AUDIT["data"]["body"])


def clarify(body, six_key, gap_key):
    six = list(body[six_key])
    gap = list(body[gap_key])
    proposal_six = [v for v in six if "Förslaget kräver roots slutliga sakbedömning" in v]
    proposal_gap = [v for v in gap if "Samla med redan godkända6r108fält" in v or "Källberoendeprövning av just12nya celler" in v]
    assert len(proposal_six) == 1 and len(proposal_gap) == 2
    body[six_key] = [v for v in six if v not in proposal_six]
    body[gap_key] = [v for v in gap if v not in proposal_gap]
    body["historical_proposal_limits"] = {
        "six_row_comparison_status_at_drafting": proposal_six,
        "row_1_3_gap_comparison_status_at_drafting": proposal_gap,
        "interpretation": "Dessa meningar dokumenterar tidigare förslagsläge, inte en återstående sakgranskning eller ett olöst källberoende i detta v3-förslag.",
    }
    body["final_review_status"] = {
        "reviewer": "root Astra",
        "date": "2026-09-24",
        "six_row_comparison": "approved; 108 field positions and substantive reservations retained",
        "row_1_3_gap_comparison": "approved; 24 explicitly documented reused positions and 12 newly adjudicated gap positions",
        "row_1_3_addendum": "approved; one exact two-field revision, two bounded person adoptions and nine decisions to retain within the twelve-field impact",
        "current_followup_review": "six-row 15 revisions/24 after-fields and row1/3 additional revision/2 after-fields assessed individually by root Astra; 38 prior six-row retains and nine gap-impact retains reviewed",
        "scope": "all eight own rows, 144 printed column positions",
        "canonical_apply": "not yet performed by this proposal; operation requires separate final approval",
    }


clarify(tr_body, "limits", "rows_1_3_limits")
clarify(audit_body, "limits", "row_1_3_limits")
TR["data"]["text"] = json.dumps(tr_body, ensure_ascii=False, indent=2)
AUDIT["data"]["body"] = json.dumps(audit_body, ensure_ascii=False, indent=2)
OUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {
    "task": "T-0676", "mode": "PROPOSAL_ONLY", "canonicalApply": False,
    "previousOperationSha256": hashlib.sha256(OLD.read_bytes()).hexdigest(),
    "operation": str(OUT.relative_to(ROOT)),
    "operationSha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
    "changes": len(operation["changes"]),
    "onlyDataFieldsChangedFromV2": ["TR-T0676-FLEN914-UPPER-45.text", "AUDIT-T0676-FLEN914-UPPER-45.body"],
    "reason": "Historical draft-stage limitations are retained as history while current source and follow-up review status is explicit; all 144 field objects and 26 approved after-fields are unchanged.",
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": report["operation"], "sha256": report["operationSha256"], "changes": report["changes"]}, ensure_ascii=False))
