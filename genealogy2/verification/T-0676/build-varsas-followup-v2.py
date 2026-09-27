"""Prepare approved Värsås text revisions; no canonical apply.

The row observation/mention choice and evidence additions are finalized only
after full record-level duplicate review and Astra's identity decision.
"""

import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECISIONS = HERE / "varsas-followup-decisions-v2-20260924.json"
OUTPUT = HERE / "varsas-followup-revisions-draft.json"

raw = DECISIONS.read_bytes()
assert hashlib.sha256(raw).hexdigest() == (
    "e3d1ca97394b88a6be6ad9ed6f01579d6ee2caa6999d0f753e6a7e7132b0fe06"
)
decisions = json.loads(raw)
assert len(decisions["changes"]) == 241

grouped = defaultdict(list)
for edit in decisions["changes"]:
    grouped[edit["object_id"]].append(edit)
assert len(grouped) == 153

data_fields = {
    "question": ("subject_id", "title", "outcome", "body"),
    "assessment": ("subject_id", "criteria", "outcome", "body"),
    "narrative": ("subject_id", "title", "markdown"),
    "person": ("display_name", "sex", "legacy_state"),
}
revisions = []
checks = []
for object_id, edits in sorted(grouped.items()):
    inspected = json.loads(
        subprocess.check_output(
            ["node", "genealogy2/cli.mjs", "inspect", object_id],
            cwd=ROOT,
            text=True,
        )
    )
    kind = inspected["kind"]
    current = inspected["current"]
    assert kind in data_fields
    assert all(edit["revision"] == current["revision_id"] for edit in edits)
    assert all(edit["expected_version"] == inspected["currentVersion"] for edit in edits)
    updated = dict(current)
    for edit in edits:
        field = edit["field"]
        assert field in ("caveat", *data_fields[kind]), (object_id, field)
        value = updated[field]
        assert isinstance(value, str)
        assert value.count(edit["before"]) == edit["match_count"] == 1, (object_id, field)
        updated[field] = value.replace(edit["before"], edit["after"], 1)
        checks.append({
            "object": object_id,
            "revision": current["revision_id"],
            "field": field,
            "before": edit["before"],
            "after": edit["after"],
            "reason": edit["reason"],
        })
    revision = {
        "id": object_id,
        "kind": kind,
        "expectedVersion": inspected["currentVersion"],
        "data": {key: updated[key] for key in data_fields[kind]},
        "disposition": current["disposition"],
        "evidenceStatus": current["evidence_status"],
        "rationale": current["rationale"],
        "caveat": updated["caveat"],
        "origins": [
            {"unit": origin["unit_id"], "coverage": origin["coverage"], "note": origin["note"]}
            for origin in current["origins"]
        ],
        "evidence": [
            {
                "object": evidence["basis_revision_id"].rsplit("@", 1)[0],
                "version": int(evidence["basis_revision_id"].rsplit("@", 1)[1]),
                "role": evidence["role"],
                "note": evidence["note"],
            }
            for evidence in current["evidence"]
        ],
    }
    revisions.append(revision)

assert len(checks) == 241
assert len(revisions) == 153
assert len({r["id"] for r in revisions}) == 153
draft = {
    "task": "T-0676",
    "mode": "DRAFT_ONLY_AWAITING_ROW_O_M_DECISION",
    "decisionSha256": hashlib.sha256(raw).hexdigest(),
    "fieldEdits": 241,
    "objectRevisions": 153,
    "checks": checks,
    "changes": revisions,
    "canonicalApply": False,
}
OUTPUT.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"output": str(OUTPUT), "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), "objects": 153, "edits": 241}, ensure_ascii=False))
