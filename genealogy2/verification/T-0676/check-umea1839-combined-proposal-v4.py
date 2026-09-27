"""Independent exact-field and prospective-review report for the Umeå packet."""

import hashlib
import json
import sqlite3
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = json.loads((HERE / "umea1839-followup-decisions-proposed-v3-20260924.json").read_text())
ADD = json.loads((HERE / "umea1839-followup-v3-addendum-v2-20260924.json").read_text())
ANDERS = json.loads((HERE / "umea1839-anders-exemption-minimum-patch-20260924.json").read_text())
SIGNE = json.loads((HERE / "umea1839-sigrid-name-precision-addendum-proposed-20260924.json").read_text())
CMP = json.loads((HERE / "umea1839-full-comparison-proposed-v2-20260924.json").read_text())
OP_PATH = HERE / "umea1839-combined-proposed-operation-v4-20260924.json"
OP = json.loads(OP_PATH.read_text())
BASE_DB = ROOT / "genealogy2/data/research.sqlite"
TEMP_DB = Path("/tmp/umea1839-proposal-v4.sqlite")
REPORT = HERE / "umea1839-v4-independent-exactness-20260924.json"
PENDING = HERE / "umea1839-v4-prospective-pending-full-20260924.json"
assert len(OP["changes"]) == 177
changes = {c["id"]: c for c in OP["changes"]}
assert len(changes) == 177


def con(path):
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    return c


old = con(BASE_DB)
new = con(TEMP_DB)


def rows(c, sql, p=()):
    return [dict(r) for r in c.execute(sql, p)]


def head(c, oid):
    r = rows(c, "SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1", (oid,))[0]
    k = rows(c, "SELECT kind FROM object WHERE id=?", (oid,))[0]["kind"]
    data = rows(c, f"SELECT * FROM {k} WHERE revision_id=?", (r["id"],))[0]
    del data["revision_id"]
    return {"kind": k, "revision": r, "data": data,
            "evidence": rows(c, "SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role", (r["id"],)),
            "origins": rows(c, "SELECT unit_id,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id", (r["id"],)),
            "assets": rows(c, "SELECT asset_path,region FROM record_asset WHERE revision_id=? ORDER BY asset_path", (r["id"],)) if k == "record" else [],
            "media": rows(c, "SELECT asset_id,region FROM record_media WHERE revision_id=? ORDER BY asset_id", (r["id"],)) if k == "record" else []}


patches = {}
for u in BASE["updates"] + ADD["updates"]:
    assert u["object_id"] not in patches
    patches[u["object_id"]] = {k: v["after"] for k, v in u["fields"].items()}
assert len(patches) == 142
for r in ADD["replace_base_proposed_fields"]:
    assert patches[r["object_id"]][r["field"]] == r["previous_proposed_after"]
    patches[r["object_id"]][r["field"]] = r["after"]
for r in ANDERS["replace_or_add_proposed_fields"]:
    if r["field"] in patches[r["object_id"]]:
        assert patches[r["object_id"]][r["field"]] == r["previous_proposed_after"]
    value = r["after"]
    if r["object_id"] == "THEME-P-0032-HAL":
        phrase = "inskrivningslängden bär längd, bröstvidd och synskärpa"
        assert value.count(phrase) == 1
        value = value.replace(phrase, "den ännu olästa inskrivningslängden kan ge hälsouppgifter")
    patches[r["object_id"]][r["field"]] = value
assert sum(map(len, patches.values())) == 179
for r in SIGNE["patches"]:
    oid, field = r["object_id"], r["field"]
    if oid not in patches:
        patches[oid] = {}
    if field in patches[oid]:
        assert patches[oid][field] == r["v3_proposed_after"]
    else:
        assert r["v3_proposed_after"] is None or r["v3_proposed_after"] == r["current_before"]
    value = r["after"]
    if oid == "P-0033/Q-04" and field == "body":
        assert value.count("- Aktuell precisering:") == 1
        value = value.replace("- Aktuell precisering:",
                              "- Aktuell precisering: Aktuellt slutsatsläge: BESVARAD MED RESERVATION; Sigrid är den föredragna läsningen i de prövade bokposterna, medan egen födelsepost är oläst.", 1)
    patches[oid][field] = value
patches["P-0033/Q-04"]["outcome"] = "BESVARAD MED RESERVATION"
assert len(patches) == 152 and sum(map(len, patches.values())) == 191

field_checks = []
metadata_preserved = []
evidence_changes = []
for oid, fields in patches.items():
    before, after = head(old, oid), head(new, oid)
    assert after["revision"]["version"] == before["revision"]["version"] + 1
    assert after["origins"] == before["origins"], oid
    assert after["assets"] == before["assets"] and after["media"] == before["media"], oid
    for field, expected in fields.items():
        actual = after["revision"].get(field) if field in after["revision"] else after["data"][field]
        if field in ("value_json", "date_json", "scope_json"):
            actual = json.loads(actual) if isinstance(actual, str) else actual
            expected = json.loads(expected) if isinstance(expected, str) else expected
        assert actual == expected, (oid, field)
        field_checks.append({"object": oid, "field": field, "exact": True})
    old_content = {**before["data"], **{k: before["revision"][k] for k in ("disposition", "evidence_status", "rationale", "caveat")}}
    new_content = {**after["data"], **{k: after["revision"][k] for k in ("disposition", "evidence_status", "rationale", "caveat")}}
    changed = {k for k in old_content if old_content[k] != new_content[k]}
    assert changed == set(fields), (oid, changed, set(fields))
    metadata_preserved.append(oid)
    if before["evidence"] != after["evidence"]:
        evidence_changes.append({"object": oid, "before": before["evidence"], "after": after["evidence"]})

source = [c for c in OP["changes"] if c["id"].startswith(("TR-T0676-UMEA1839-SCOPE-", "AUDIT-T0676-UMEA1839-"))]
assert len(source) == 14
source_counts = {}
for c in source:
    if c["kind"] != "transcription":
        continue
    body = json.loads(c["data"]["text"])
    source_counts[c["id"]] = len(body["own_18_column_fields_exact_approved_comparison"])
    own = body["own_18_column_fields_exact_approved_comparison"]
    cmp_own = [f for f in CMP["fields"] if f["scope"] == body["scope"]]
    assert own == cmp_own, c["id"]
    assert len({(f["row"], f["column"]) for f in own}) == len(own)
assert sorted(source_counts.values()) == [18, 18, 18, 18, 36, 36, 144]
assert sum(source_counts.values()) == 288

requests = rows(new, """SELECT q.* FROM review_request q LEFT JOIN review_resolution z ON z.request_id=q.id
                       WHERE z.request_id IS NULL ORDER BY q.id""")
assert len(requests) == 86
pending = []
for i, r in enumerate(requests, 1):
    affected = r["affected_revision_id"].rsplit("@", 1)[0]
    changed = r["changed_revision_id"].rsplit("@", 1)[0]
    pending.append({"index": i, "request": r, "affectedCurrent": head(new, affected),
                    "changedCurrent": head(new, changed)})
PENDING.write_text(json.dumps({"task": "T-0676", "mode": "PROSPECTIVE_ONLY", "operationSha256": hashlib.sha256(OP_PATH.read_bytes()).hexdigest(),
                              "count": len(pending), "index": [{"index": x["index"], "requestId": x["request"]["id"],
                                                                     "affectedCurrent": x["affectedCurrent"]["revision"]["id"],
                                                                     "changedCurrent": x["changedCurrent"]["revision"]["id"]} for x in pending],
                              "requests": pending}, ensure_ascii=False, indent=2) + "\n")

report = {"task": "T-0676", "mode": "INDEPENDENT_PROSPECTIVE_ASSERTION", "canonicalApply": False,
          "operationSha256": hashlib.sha256(OP_PATH.read_bytes()).hexdigest(),
          "exactAfterFields": len(field_checks), "exactAfterFieldChecks": field_checks,
          "revisedObjects": len(metadata_preserved), "unchangedNonpatchedDataAndMetadata": True,
          "originsAssetsMediaPreserved": True, "evidenceChangedObjects": len(evidence_changes),
          "evidenceChanges": evidence_changes,
          "sourceOwnCells": source_counts, "sourceTotal": sum(source_counts.values()),
          "prospectivePending": len(pending), "prospectivePendingFile": str(PENDING.relative_to(ROOT)),
          "prospectivePendingSha256": hashlib.sha256(PENDING.read_bytes()).hexdigest()}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"reportSha256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
                  "pendingSha256": report["prospectivePendingSha256"], "fields": len(field_checks),
                  "sourceCells": report["sourceTotal"], "pending": len(pending)}, ensure_ascii=False))
