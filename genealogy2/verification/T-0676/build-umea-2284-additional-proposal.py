#!/usr/bin/env python3
"""Build only the root-approved exact substitutions against live heads."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
decisions = json.loads((HERE / "umea-2284-additional-decisions-20260924.json").read_text())
assert decisions["summary"] == {"RETAIN": 205, "REVISE": 52}
assert decisions["field_change_count"] == 61
record_id = "R-340d89b7be8bb89cf4a63828"
# Each list entry addresses one approved substitution in order. These are
# source-content bindings, not person-ID routing. Keep the map reviewable.
R = lambda n: f"TR-T0676-UMEA2284-r{n}"
T675 = ["TR-T0675-degerfors1064-21", "TR-2aaf3e0ac0a87c336597ac20"]
TYRA_OLD = ["E-birth-P-0037"]  # Imported correction of T-0177, journal 20.
FIELD_SOURCES = {
    "ASSESSMENT-P-0029": [[R(12), R(13)]],
    "ASSESSMENT-P-0030": [T675],
    "ASSESSMENT-P-0032": [[R(17)]],
    "ASSESSMENT-P-0033": [[R(17), *T675]],
    "BIO-P-0028": [[R(12), R(13)]],
    "BIO-P-0029": [[R(12), R(13)], [R(13)]],
    "BIO-P-0030": [T675],
    "CONTRACT-P-0029-PK-05": [[R(12), R(13)]],
    "CONTRACT-P-0030-PK-01": [T675],
    "CONTRACT-P-0030-PK-09": [T675],
    "CONTRACT-P-0038-PK-03": [[R(23), *T675]],
    "CONTRACT-P-0038-PK-05": [[R(23), *T675]],
    "CONTRACT-P-0529-PK-01": [[R(14)]],
    "E-birth-P-0035": [[R(20), *T675]],
    "EP-E-birth-P-0035-P-0035-principal": [[R(20), *T675]],
    "F-P-0001-household_membership-network-P-0035": [[R(20), *T675]],
    "F-P-0001-household_membership-network-P-0037": [[R(22), *TYRA_OLD], [R(22), *TYRA_OLD]],
    "KEY-P-0001-fd0002ff2190": [[R(22), R(23), *TYRA_OLD, *T675]],
    "KEY-P-0028-469306e9a9e4": [[R(20), R(21), R(22), R(23), *TYRA_OLD, *T675]],
    "KEY-P-0028-676e739e7314": [[R(12), R(13)], [R(12), R(13)]],
    "KEY-P-0029-4dc9f4360eb5": [[R(12), R(13)]],
    "KEY-P-0029-9a8296631b7f": [[R(12), R(13)], [R(12), R(13)], [R(13)]],
    "KEY-P-0032-34f2f0b9c288": [[R(17)]],
    "KEY-P-0032-738b1de73be7": [[R(17)]],
    "KEY-P-0032-8596a5f2ad4f": [[R(17)]],
    "KEY-P-0032-f2cd20d159bb": [[R(17)]],
    "KEY-P-0033-46d5830aa642": [[R(17), *T675]],
    "KEY-P-0034-e7c2942dfdd2": [[R(19)]],
    "KEY-P-0038-fba6f151cc40": [[R(23), *T675]],
    "M-P-0529-C0907-row14": [[R(14)]],
    "O-P-0028-Hildur_unresolved": [[R(14)]],
    "O-P-0028-mantal1917": [[R(12), R(13)]],
    "O-P-0029-Hildur_unresolved": [[R(14)]],
    "O-P-0029-mantal1917_conflict": [[R(12), R(13)], [R(13)], [R(12), R(13)]],
    "O-P-0036-C0907-Hildur-unresolved_household_person": [[R(14)]],
    "O-P-0037-C0907-Hildur-unresolved_household_person": [[R(14)]],
    "P-0028/Q-03": [[R(12), R(13)]],
    "P-0029/Q-01": [[R(12), R(13)]],
    "P-0030/Q-03": [T675, [R(14)]],
    "PATH-P-0029-KP-01": [[R(12), R(13)]],
    "RESEARCH-P-0029-9d76f0343410": [[R(12), R(13)]],
    "RESEARCH-P-0030-9d76f0343410": [T675],
    "THEME-P-0028-EKO": [[R(12)], [R(12), R(13)]],
    "THEME-P-0029-BO": [[R(12), R(13)]],
    "THEME-P-0029-MIL": [[R(12), R(13)]],
    "THEME-P-0030-ID": [T675],
    "THEME-P-0032-BO": [[R(17)]],
    "THEME-P-0034-MIL": [[R(19)]],
    "THEME-P-0035-HAL": [[R(20)]],
    "THEME-P-0038-BO": [[R(23), *T675]],
    "THEME-P-0038-HAL": [[R(23), *T675]],
    "THEME-P-0529-ID": [[R(14)]],
}
metadata = {"revision_id", "object_id", "version", "kind", "disposition", "evidence_status",
            "rationale", "caveat", "origins", "evidence", "pending_reviews"}
changes = []
diff = []
evidence_map = []
approved_revisions = {d["object_id"]: d["revision_id"] for d in decisions["decisions"] if d["decision"] == "REVISE"}

for decision in decisions["decisions"]:
    if decision["decision"] != "REVISE":
        continue
    raw = subprocess.check_output(["node", "genealogy2/cli.mjs", "inspect", decision["object_id"]], text=True)
    current = json.loads(raw)["current"]
    fingerprint = hashlib.sha256(json.dumps(current, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    if current["revision_id"] != decision["revision_id"] or fingerprint != decision["reviewed_current_sha256"]:
        raise ValueError(f"Current revision/hash mismatch: {decision['object_id']}")
    data = {k: v for k, v in current.items() if k not in metadata}
    caveat = current["caveat"]
    field_checks = []
    for edit in decision["changes"]:
        if edit["mode"] != "replace_exact_once":
            raise ValueError(f"Unsupported edit mode: {decision['object_id']}")
        field = edit["field"]
        text = caveat if field == "caveat" else data[field]
        if not isinstance(text, str) or text.count(edit["before"]) != 1:
            raise ValueError(f"Before text does not occur exactly once: {decision['object_id']}.{field}")
        replaced = text.replace(edit["before"], edit["after"], 1)
        if field == "caveat":
            caveat = replaced
        else:
            data[field] = replaced
        field_checks.append({"field": field, "before": edit["before"], "after": edit["after"]})
    for key in ("value_json", "date_json", "scope_json"):
        if isinstance(data.get(key), str):
            data[key] = json.loads(data[key])
    evidence = [{"object": e["basis_revision_id"].rsplit("@", 1)[0],
                 "version": int(e["basis_revision_id"].rsplit("@", 1)[1]),
                 "role": e["role"], "note": e["note"]} for e in current["evidence"]]
    rebound = []
    for link in evidence:
        if link["object"] in approved_revisions and approved_revisions[link["object"]] == f"{link['object']}@{link['version']}":
            link["version"] += 1
            rebound.append(link["object"])
    approved_sources = FIELD_SOURCES[decision["object_id"]]
    if len(approved_sources) != len(decision["changes"]):
        raise ValueError(f"Evidence map length mismatch: {decision['object_id']}")
    relevant = list(dict.fromkeys(source for group in approved_sources for source in group))
    for source in relevant:
        version = 2 if source == "TR-2aaf3e0ac0a87c336597ac20" else 1
        evidence.append({"object": source, "version": version, "role": "supports",
                         "note": "Precist versionsbundet underlag för godkänd fälträttelse; samma historiska källa där bokkedjan återbrukas."})
    if any(source.startswith("TR-T0676-UMEA2284-") for source in relevant):
        evidence.append({"object": "AUDIT-T0676-10", "version": 1, "role": "supports",
                         "note": "Versionsbunden granskning av Umeå 2284 med reservationer; ingen extra oberoende röst."})
    changes.append({
        "id": decision["object_id"], "kind": current["kind"],
        "expectedVersion": current["version"], "data": data,
        "disposition": current["disposition"], "evidenceStatus": current["evidence_status"],
        "rationale": "T-0676 rootgodkänd individuell följdrättelse av Umeå 2284: " + " ".join(decision["reasons"]),
        "caveat": caveat,
        "origins": [{"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]} for o in current["origins"]],
        "evidence": evidence,
    })
    diff.append({"object_id": decision["object_id"], "before_revision": current["revision_id"],
                 "before_sha256": fingerprint, "after_revision": f"{decision['object_id']}@{current['version']+1}",
                 "changes": field_checks, "preserved_origin_count": len(current["origins"]),
                 "preserved_evidence_count": len(current["evidence"]), "added_source_rows": relevant,
                 "added_audit": "AUDIT-T0676-10@1" if any(s.startswith("TR-T0676-UMEA2284-") for s in relevant) else None,
                 "added_sources": relevant, "rebound_to_same_batch_revision": rebound})
    for index, (edit, sources) in enumerate(zip(decision["changes"], approved_sources), 1):
        evidence_map.append({"object_id": decision["object_id"], "field_change_index": index,
                             "field": edit["field"], "before": edit["before"], "after": edit["after"],
                             "source_revisions": [f"{s}@{2 if s == 'TR-2aaf3e0ac0a87c336597ac20' else 1}" for s in sources],
                             "source_limit": "Bokkedjans avskrifter ger inte oberoende extra röster; äldre T-0177-rättelse representeras av aktuell E-birth-P-0037@1 där den används."})

assert len(changes) == 52 and sum(len(d["changes"]) for d in diff) == 61
assert len(evidence_map) == 61 and len(FIELD_SOURCES) == 52
operation = {"id": "T-0676/umea-2284-additional-followup-v2", "actor": "Codex",
             "reason": "T-0676: 52 rootgodkända individuella följdrevisioner och 61 exakta fältbyten efter full Umeå 2284-granskning. Övriga 205 retain ändras inte; inga väntande requests masslöses.",
             "dependencyReviewVersion": 2, "changes": changes}
(HERE / "umea-2284-additional-proposed-operation-v2.json").write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
(HERE / "umea-2284-additional-diff-check-v2-20260924.json").write_text(json.dumps(diff, ensure_ascii=False, indent=2) + "\n")
(HERE / "umea-2284-additional-evidence-map-20260924.json").write_text(json.dumps(evidence_map, ensure_ascii=False, indent=2) + "\n")
print(len(changes), sum(len(d["changes"]) for d in diff))
