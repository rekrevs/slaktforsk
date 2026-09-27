"""Prepare only the 86 individually reviewed Umeå follow-up resolutions."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FILES = {
    "actual": ("umea1839-v4-actual-pending-full-20260924.json", "8f1474f6cc99baf428803ba01affae68d9f2f3e9a577fe143f9c881ddb379a01"),
    "v3": ("umea1839-v3-prospective-pending-full-20260924.json", "307870bc6b937e0e1ea52a0ed9956247471a11455ddc0ee0e33b960c14568519"),
    "first40": ("umea1839-v3-root-review-1-40-draft-20260924.json", "a98b1cf38e7e99258b5a9033d5bf836e1bdd6ffa4c5caece3c0213dea4732a23"),
    "last40": ("umi-v3-prospective-review-last40-20260924.json", "4f33f85e878ca2d41012fed86d38944d6fece1f6a9b35dd0b4b59f7cbb3e123a"),
    "new10": ("umea1839-v4-new-pending-review-20260924.json", "2a27d538a44a9cb00c822467d07a90f2a901ccd97a9afef922ae42e6dd0dbf49"),
}
input_data = {}
for key, (name, digest) in FILES.items():
    path = HERE / name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    input_data[key] = json.loads(path.read_text())
actual = input_data["actual"]
v3 = input_data["v3"]
assert actual["count"] == 86 and v3["count"] == 80
assert actual["operationSha256"] == "b5fb7ccbbaeda09dde736d40183a720f6b86ba4290762bc8f4eecb6aa2457c8d"


def key(request):
    return (request["affectedCurrent"]["revision"]["object_id"],
            request["changedCurrent"]["revision"]["object_id"])


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


v3_by_index = {r["index"]: r for r in v3["requests"]}
actual_by_pair = {key(r): r for r in actual["requests"]}
assert len(v3_by_index) == 80 and len(actual_by_pair) == 86
resolved = {}
manifest = []
for entry in input_data["first40"]["entries"]:
    if entry["decision"] != "RETAIN_APPROVED_BY_ROOT_ASTRA":
        assert entry["index"] in (14, 18, 23)
        continue
    old = v3_by_index[entry["index"]]
    assert old["request"]["id"] == entry["requestId"]
    candidate = actual_by_pair[key(old)]
    assert candidate["affectedCurrent"] == old["affectedCurrent"]
    resolved[candidate["request"]["id"]] = entry["individualRationale"]
    manifest.append({"actualIndex": candidate["index"], "v3Index": entry["index"],
                     "requestId": candidate["request"]["id"], "source": "root first40",
                     "affectedCurrentSha256": digest(candidate["affectedCurrent"]),
                     "changedCurrentSha256": digest(candidate["changedCurrent"]),
                     "rationale": entry["individualRationale"]})
assert len(manifest) == 37

for entry in input_data["last40"]["decisions"]:
    if entry["file_index"] == 76:
        assert entry["decision"] == "update"
        continue
    assert entry["decision"] == "retain"
    old = v3_by_index[entry["file_index"]]
    assert old["request"]["id"] == entry["request_id"]
    candidate = actual_by_pair[key(old)]
    assert candidate["affectedCurrent"] == old["affectedCurrent"]
    resolved[candidate["request"]["id"]] = entry["rationale"]
    manifest.append({"actualIndex": candidate["index"], "v3Index": entry["file_index"],
                     "requestId": candidate["request"]["id"], "source": "Astra last40/root approved",
                     "affectedCurrentSha256": digest(candidate["affectedCurrent"]),
                     "changedCurrentSha256": digest(candidate["changedCurrent"]),
                     "rationale": entry["rationale"]})
assert len(manifest) == 76

for entry in input_data["new10"]["reviews"]:
    assert entry["decision"] == "retain"
    candidate = actual["requests"][entry["index"] - 1]
    assert candidate["request"]["id"] == entry["request_id"]
    assert candidate["affectedCurrent"]["revision"]["id"] == entry["affected_revision_id"]
    assert candidate["changedCurrent"]["revision"]["id"] == entry["changed_revision_id"]
    assert candidate["affectedCurrent"] == entry["affected_full_payload"]
    assert candidate["changedCurrent"] == entry["changed_full_payload"]
    resolved[candidate["request"]["id"]] = entry["rationale"]
    manifest.append({"actualIndex": candidate["index"], "v3Index": None,
                     "requestId": candidate["request"]["id"], "source": "Astra new10/root approved",
                     "affectedCurrentSha256": digest(candidate["affectedCurrent"]),
                     "changedCurrentSha256": digest(candidate["changedCurrent"]),
                     "rationale": entry["rationale"]})
assert len(manifest) == len(resolved) == 86
assert set(resolved) == {r["request"]["id"] for r in actual["requests"]}
manifest.sort(key=lambda r: r["actualIndex"])
assert [r["actualIndex"] for r in manifest] == list(range(1, 87))
operation = {"id": "T-0676/umea1839-v4-individual-retains-proposed", "actor": "Codex",
             "reason": "T-0676: 86 faktiska följdbegäranden individuellt sakprövade mot full aktuellt affected/changed-underlag; 76 godkända v3-beslut återbrukas där affectedCurrent är exakt oförändrat och tio nya har egen Astra- och rootbedömning.",
             "dependencyReviewVersion": 2, "changes": [],
             "resolve": [{"request": r["requestId"], "rationale": r["rationale"]} for r in manifest]}
path = HERE / "umea1839-v4-individual-retain-operation-20260924.json"
path.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {"task": "T-0676", "mode": "RETAIN_PROPOSAL_ONLY", "canonicalApply": False,
          "operation": str(path.relative_to(ROOT)), "operationSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
          "sourceOperationSha256": actual["operationSha256"], "actualPendingCount": 86,
          "retains": 86, "reusedV3": 76, "newV4": 10,
          "inputSha256": {k: v[1] for k, v in FILES.items()}, "entries": manifest}
report_path = HERE / "umea1839-v4-individual-retain-review-manifest-20260924.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operationSha256": report["operationSha256"],
                  "manifestSha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
                  "resolves": len(operation["resolve"])}, ensure_ascii=False))
