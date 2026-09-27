"""Build the approved six grave-card operation without canonical mutation."""

import copy
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
V2 = HERE / "graves-six-followup-decisions-v2-20260924.json"
OWNER = HERE / "p0212-owner-name-followup-decisions-20260924.json"
OUTPUT = HERE / "graves-six-proposed-operation.json"
PREFLIGHT = HERE / "graves-six-proposal-preflight.json"


def read_json(path):
    return json.loads(path.read_text())


def inspect(object_id):
    return json.loads(subprocess.check_output(
        ["node", "genealogy2/cli.mjs", "inspect", object_id],
        cwd=ROOT, text=True,
    ))


def evidence_from_current(current):
    return [
        {
            "object": row["basis_revision_id"].rsplit("@", 1)[0],
            "version": int(row["basis_revision_id"].rsplit("@", 1)[1]),
            "role": row["role"],
            "note": row["note"],
        }
        for row in current.get("evidence", [])
    ]


def origins_from_current(current):
    return [
        {"unit": row["unit_id"], "coverage": row["coverage"], "note": row["note"]}
        for row in current.get("origins", [])
    ]


def add_evidence(change, object_id, version, role, note):
    if not any(e["object"] == object_id and e["version"] == version and e["role"] == role
               for e in change["evidence"]):
        change["evidence"].append({
            "object": object_id, "version": version, "role": role, "note": note,
        })


def current_data(inspected):
    current = inspected["current"]
    revision = inspected["revisions"][-1]
    assert revision["id"] == current["revision_id"]
    data = {k: v for k, v in revision["data"].items() if k != "revision_id"}
    for key, value in list(data.items()):
        if key.endswith("_json") and isinstance(value, str):
            data[key] = json.loads(value)
    return data


def base_change(object_id, expected_version, kind, data, metadata, current=None):
    change = {
        "id": object_id, "kind": kind, "expectedVersion": expected_version,
        "data": copy.deepcopy(data),
        "disposition": metadata["disposition"],
        "evidenceStatus": metadata.get("evidence_status"),
        "rationale": metadata["rationale"], "caveat": metadata["caveat"],
        "origins": origins_from_current(current) if current else [],
        "evidence": evidence_from_current(current) if current else [],
    }
    return change


v2_bytes = V2.read_bytes()
owner_bytes = OWNER.read_bytes()
assert hashlib.sha256(v2_bytes).hexdigest() == "93d581cc19827ce4f89646b0cd790f43b37d747afd8f2b71ca63787f920e71b7"
assert hashlib.sha256(owner_bytes).hexdigest() == "c2186fcdccc471b8260151fecda4627f3839c4b1d5fb73156c491d6a6fbf6f88"
v2, owner = json.loads(v2_bytes), json.loads(owner_bytes)
assert len(v2["updates"]) == 49 and len(v2["creates"]) == 12
assert len(owner["changes"]) == 8
comparison = read_json(HERE / "graves-six-comparison-20260920.json")
staged = read_json(HERE / "graves-six-staged-media-20260920.json")
assert len(comparison["rows"]) == len(staged["staged"]) == 6
rows = {row["scope"]: row for row in comparison["rows"]}
media = {row["scopeNumber"]: row["stageMediaReturn"] for row in staged["staged"]}
assert set(rows) == set(media) == {13, 14, 19, 20, 40, 42}

operation = {
    "id": "T-0676/graves-six-approved-v1",
    "actor": "Codex",
    "reason": "T-0676 six own grave cards: approved v2 decisions, full bounded source audits, and PCD-2026-09-24-001 owner-confirmed name follow-up. No identity, relation, PK or tree-status upgrade.",
    "dependencyReviewVersion": 2,
    "media": [media[s] for s in sorted(media)],
    "changes": [],
}
changes = operation["changes"]
preflight = {"base": "current canonical read only", "versions": [], "exceptions": [], "duplicateChecks": v2["duplicateChecks"]}

# Source records gain the own preserved capture. The old record revision and
# all its origins/evidence remain intact; only the current record is revised.
for scope, row in rows.items():
    object_id = row["recordId"]
    inspected = inspect(object_id)
    assert inspected["kind"] == "record" and inspected["currentVersion"] == 1
    current = inspected["current"]
    data = current_data(inspected)
    provenance = media[scope]["provenance"]
    source_url = provenance.split("exact source URL ", 1)[1].split(";", 1)[0]
    assert source_url.startswith("https://www.svenskagravar.se/")
    assert source_url not in data["locator"]
    data["locator"] += "; " + source_url
    old_copy = "Den exakta äldre 2026-09-06-registerkopian saknas fortfarande; ny daterad fångst 2026-09-20 är bevarad med exakt URL och SHA-256 " + media[scope]["sha256"] + "."
    if scope == 14:
        old_copy += " Endast vald Chrome-DOM-resultatsektion; ingen egen detalj-URL eller full detaljkorts-/medgravslista visas."
    if scope == 40:
        old_copy += " Ingen medgravssektion visas i denna HTML; detta är inget belägg för att ingen annan är gravsatt där."
    revised_caveat = current["caveat"]
    missing_copy = {
        13: "Exakt post-URL/hashkopia saknas.",
        14: "Exakt lokal registerkopia/URL/hash saknas.",
        19: "Exakt post-URL/hashkopia saknas.",
        20: "Exakt post-URL/hashkopia saknas.",
        42: "Exakt post-URL/hashkopia saknas.",
    }
    if scope in missing_copy:
        assert revised_caveat.count(missing_copy[scope]) == 1
        revised_caveat = revised_caveat.replace(missing_copy[scope], old_copy, 1)
    else:
        assert scope == 40
        assert revised_caveat.count("Ingen medgravsatt listas.") == 1
        revised_caveat = revised_caveat.replace(
            "Ingen medgravsatt listas.",
            "Ingen medgravssektion visas i det bevarade HTML-kortet; det visar inte att ingen annan är gravsatt här.", 1,
        )
        revised_caveat = old_copy + "\n" + revised_caveat
    metadata = {
        "disposition": current["disposition"],
        "evidence_status": current["evidence_status"],
        "rationale": current["rationale"] + " T-0676: Egen daterad registerfångst och bevarat medium; ingen ny oberoende historisk röst.",
        "caveat": revised_caveat,
    }
    change = base_change(object_id, 1, "record", data, metadata, current)
    change["media"] = [{"id": media[scope]["id"], "region": "egen post, daterad fångst 2026-09-20"}]
    changes.append(change)
    preflight["versions"].append({"object": object_id, "expected": 1, "actual": 1})

approved = {}
for item in v2["updates"]:
    object_id, scope = item["objectId"], item["scope"]
    inspected = inspect(object_id)
    assert inspected["kind"] == item["kind"]
    assert inspected["currentVersion"] == item["currentVersion"], object_id
    current = inspected["current"]
    actual_data = current_data(inspected)
    assert actual_data == item["beforeData"], object_id
    for field in ("disposition", "evidence_status", "rationale", "caveat"):
        assert current[field] == item["beforeMetadata"][field], (object_id, field)
    change = base_change(object_id, item["currentVersion"], item["kind"],
                         item["afterData"], item["afterMetadata"], current)
    # Old versions of the own source record are replaced by its new revision.
    for e in change["evidence"]:
        if e["object"] == rows[scope]["recordId"] and e["version"] == 1:
            e["version"] = 2
    if item["kind"] not in ("transcription",):
        add_evidence(change, rows[scope]["recordId"], 2, "supports",
                     "Egen daterad registerfångst, inte oberoende historisk röst.")
    changes.append(change)
    approved[object_id] = change
    preflight["versions"].append({"object": object_id, "expected": item["currentVersion"], "actual": inspected["currentVersion"]})

transcriptions = {scope: next(c for c in changes if c["kind"] == "transcription" and
                   c["data"].get("record_id") == row["recordId"])
                  for scope, row in rows.items()}
reads = {scope: next(c for c in changes if c["id"].startswith("READ-") and
          c["data"].get("subject_id") == row["recordId"])
         for scope, row in rows.items()}

for scope, row in rows.items():
    tr = transcriptions[scope]
    rd = reads[scope]
    add_evidence(rd, tr["id"], 2, "supports", "Full egen kortavskrift av samma registerpost.")
    extraction = row["newExtraction"]
    audit_body = {
        "scope": scope, "record": row["recordId"], "capture": {
            "url": media[scope]["provenance"].split("exact source URL ", 1)[1].split(";", 1)[0],
            "sha256": media[scope]["sha256"], "media": media[scope]["id"],
            "storagePath": media[scope]["storagePath"], "date": "2026-09-20",
        },
        "own_card_fields": extraction["ownFields"],
        "other_buried": extraction["otherBuried"],
        "contact_block": extraction["contactBlock"],
        "raw_correction": row["rawCorrection"],
        "reservation": row["reservation"],
        "preservation": row["preservation"],
        "limits": [
            "Den äldre exakta 2026-09-06-kopian är inte återfunnen; den nya fångsten är daterad 2026-09-20.",
            "Ej visade fält är ej visade, inte tomma originalfält eller obegränsade personnoll.",
            "Ingen ny identitets-, släkt-, PK-, livsbilds- eller trädgranskning.",
            "Två läsningar av samma registerpost är inte två oberoende historiska evidensröster.",
        ],
    }
    if scope == 14:
        audit_body["limits"].append("Endast vald sökresultatsektion; ingen egen detalj-URL, full server-HTML eller medgravslista har granskats.")
    if scope == 40:
        audit_body["limits"].append("Ingen medgravssektion visas i bevarad HTML; det betyder inte att ingen annan är gravsatt där.")
    audit = base_change(f"AUDIT-T0676-{scope}", None, "assessment", {
        "subject_id": row["recordId"], "criteria": "source_record_review/1",
        "outcome": "reviewed_with_reservations",
        "body": json.dumps(audit_body, ensure_ascii=False, indent=2),
    }, {
        "disposition": "recorded", "evidence_status": None,
        "rationale": "T-0676: full relevant own-card extraction and bounded source review from two agreed readings.",
        "caveat": row["reservation"] + " Den äldre exakta kopian saknas fortsatt.",
    })
    add_evidence(audit, row["recordId"], 2, "derived_from", "Egen versionsbunden registerpost.")
    add_evidence(audit, tr["id"], 2, "supports", "Full synlig avskrift, samma källkedja.")
    add_evidence(audit, rd["id"], 2, "supports", "Uppdaterad äldre läsbedömning.")
    changes.append(audit)
    for change in approved.values():
        if change["id"] in (tr["id"], rd["id"]):
            continue
        if change["id"] in row["affectedObjects"]:
            add_evidence(change, tr["id"], 2, "supports", "Egen full avskrift för samma administrativa registerpost.")
            add_evidence(change, audit["id"], 1, "supports", "Avgränsad egenkortsaudit med fulla fält och reservationer.")

for item in v2["creates"]:
    scope = item["scope"]
    if inspect(item["objectId"]).get("currentVersion") is not None:
        raise AssertionError("proposed id already exists: " + item["objectId"])
    change = base_change(item["objectId"], None, item["kind"],
                         item["afterData"], item["afterMetadata"])
    add_evidence(change, rows[scope]["recordId"], 2, "derived_from", "Avgränsad synlig medgravsrad på eget kort.")
    add_evidence(change, transcriptions[scope]["id"], 2, "supports", "Full synlig avskrift av samma registerpost.")
    add_evidence(change, f"AUDIT-T0676-{scope}", 1, "supports", "Källpostens avgränsade fullfältsgranskning.")
    changes.append(change)

for edit in owner["changes"]:
    object_id = edit["object_id"]
    if object_id in approved:
        change = approved[object_id]
        assert edit["base"] == "v2 afterData"
    else:
        inspected = inspect(object_id)
        assert inspected["currentVersion"] == edit["expected_version"]
        current = inspected["current"]
        metadata = {"disposition": current["disposition"],
                    "evidence_status": current["evidence_status"],
                    "rationale": current["rationale"], "caveat": current["caveat"]}
        change = base_change(object_id, edit["expected_version"], inspected["kind"],
                             current_data(inspected), metadata, current)
        changes.append(change)
        approved[object_id] = change
        preflight["versions"].append({"object": object_id, "expected": edit["expected_version"], "actual": inspected["currentVersion"]})
    container = change if edit["field"] in ("rationale", "caveat") else change["data"]
    field = edit["field"]
    assert container[field].count(edit["before"]) == edit["match_count"] == 1, (object_id, field)
    container[field] = container[field].replace(edit["before"], edit["after"], 1)

new_fact = owner["new_fact"]
if inspect(new_fact["object_id"]).get("currentVersion") is not None:
    raise AssertionError("owner fact already exists")
fact_data = copy.deepcopy(new_fact["data"])
fact_data["value_json"] = json.loads(fact_data["value_json"])
fact = base_change(new_fact["object_id"], None, "fact", fact_data,
                   new_fact["metadata"])
for e in new_fact["evidence"]:
    object_id, version = e["basis_revision_id"].rsplit("@", 1)
    add_evidence(fact, object_id, int(version), e["role"], e["note"])
owner_obs = inspect("O-P-0212-C0268-own")["current"]
fact["origins"] = [
    {"unit": row["unit_id"], "coverage": row["coverage"], "note": row["note"]}
    for row in owner_obs["origins"]
    if row["document_path"].endswith("C-0268-gunnar-hook-namn-dod-och-syskon.md")
    or (row["document_path"].endswith("P-0212-gunnar-hook.md") and row["start_line"] == 47)
]
assert len(fact["origins"]) == 2
changes.append(fact)
for object_id in ("BIO-P-0212", "RESEARCH-P-0212-9d76f0343410",
                  "THEME-P-0212-ID", "KEY-P-0212-ec3ace4eea5f",
                  "F-P-0212-name_form-source_comparison", "P-0212/Q-03"):
    add_evidence(approved[object_id], fact["id"], 1, "supports",
                 "PCD-2026-09-24-001: owner-confirmed project name only; documentary conflict remains.")

# Two relevant bases have since gained revisions. S-0711@2 is the same
# register with an editorial title correction; C0903's child row retains the
# same literal name while its vaccination/reading scope was corrected.
rebased = {"S-0711": 2, "O-P-0212-C0903-child": 2}
for change in changes:
    for e in change["evidence"]:
        if e["object"] in rebased and e["version"] == 1:
            e["version"] = rebased[e["object"]]
            e["note"] += " Aktuell revision med bevarad relevant råuppgift; tidigare revision står kvar historiskt."
preflight["evidenceVersionUpdates"] = rebased

assert len(changes) == 49 + 6 + 6 + 12 + 6 + 1
assert len({c["id"] for c in changes}) == len(changes)
# Native apply requires referenced new revisions to precede their dependents.
by_id = {c["id"]: c for c in changes}
for change in changes:
    for e in change["evidence"]:
        basis = by_id.get(e["object"])
        if basis:
            e["version"] = (basis["expectedVersion"] or 0) + 1
ordered = []
remaining = dict(by_id)
while remaining:
    ready = [c for c in remaining.values() if all(
        e["object"] not in remaining or e["object"] == c["id"]
        for e in c["evidence"]
    ) and all(
        value not in remaining or value == c["id"]
        for key, value in c["data"].items()
        if key.endswith("_id") and isinstance(value, str)
    )]
    assert ready, "cyclic proposed evidence/structure references"
    for c in ready:
        ordered.append(c)
        del remaining[c["id"]]
operation["changes"] = ordered
OUTPUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
preflight.update({"operation": str(OUTPUT.relative_to(ROOT)),
                  "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  "changes": len(changes), "media": len(operation["media"]),
                  "canonicalApply": False})
PREFLIGHT.write_text(json.dumps(preflight, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": preflight["operation"], "sha256": preflight["sha256"],
                  "changes": len(changes), "media": len(operation["media"])}, ensure_ascii=False))
