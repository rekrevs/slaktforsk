"""Build the Astra-approved Umeå 1839 packet for isolated review only."""

import hashlib
import json
import sqlite3
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / "genealogy2/data/research.sqlite"
BASE = HERE / "umea1839-followup-decisions-proposed-v3-20260924.json"
ADD = HERE / "umea1839-followup-v3-addendum-v2-20260924.json"
SKELETON = HERE / "umea1839-source-layer-skeleton-20260924.json"
ANDERS = HERE / "umea1839-anders-exemption-minimum-patch-20260924.json"
STALE = HERE / "umea1839-v2-stale-dependency-manifest-20260924.json"
SIGNE = HERE / "umea1839-sigrid-name-precision-addendum-proposed-20260924.json"
OUT = HERE / "umea1839-combined-proposed-operation-v4-20260924.json"
REPORT = HERE / "umea1839-combined-proposal-build-v4-20260924.json"
EXPECTED = {
    BASE: "e6a4f32b79698965080d8c04b83dd63ebb4503362ebea88ef33c5f61feacca74",
    ADD: "de18c0f0d2d3426ab128d6147adf252b312178790da900a8266fe7614d2f109d",
    ANDERS: "c7bda27d13ce20af5fcb40f4c8f35d817f5116946e4f2a2d547d51c14c0acc00",
    STALE: "7a6b4beddda77f496a9571e2dfdb0b9d14661b30dbae440e9d10187d51bafea3",
    SIGNE: "4217c0b0056dcda83db8123b400eedbc9d44aae8373b20bc2daa44792e83d8ed",
}
for path, digest in EXPECTED.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
base = json.loads(BASE.read_text())
add = json.loads(ADD.read_text())
skeleton = json.loads(SKELETON.read_text())
anders = json.loads(ANDERS.read_text())
stale = json.loads(STALE.read_text())
signe = json.loads(SIGNE.read_text())
assert add["base_sha256"] == EXPECTED[BASE]
assert len(base["updates"]) == 104 and len(add["updates"]) == 38
assert len(base["creates"]) == 11 and len(add["evidence_map"]) == 153
assert len(skeleton["sourceChangesForLaterIntegration"]) == 14

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row


def one(sql, params=()):
    row = conn.execute(sql, params).fetchone()
    assert row is not None, (sql, params)
    return dict(row)


def rows(sql, params=()):
    return [dict(r) for r in conn.execute(sql, params)]


def current(oid):
    kind = one("SELECT kind FROM object WHERE id=?", (oid,))["kind"]
    rev = one("SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1", (oid,))
    data = one(f"SELECT * FROM {kind} WHERE revision_id=?", (rev["id"],))
    data.pop("revision_id")
    origins = [{"unit": r["unit_id"], "coverage": r["coverage"], "note": r["note"]}
               for r in rows("SELECT * FROM origin WHERE revision_id=?", (rev["id"],))]
    evidence = []
    for r in rows("SELECT * FROM dependency WHERE revision_id=?", (rev["id"],)):
        bid, version = r["basis_revision_id"].rsplit("@", 1)
        evidence.append({"object": bid, "version": int(version), "role": r["role"], "note": r["note"]})
    extra = {}
    if kind == "record":
        extra["assets"] = [{"path": r["asset_path"], "region": r["region"]}
                           for r in rows("SELECT * FROM record_asset WHERE revision_id=?", (rev["id"],))]
        extra["media"] = [{"id": r["asset_id"], "region": r["region"]}
                          for r in rows("SELECT * FROM record_media WHERE revision_id=?", (rev["id"],))]
    return kind, rev, data, origins, evidence, extra


alias = {}
for a in skeleton["explicitAliasMapNoPrefixInference"]:
    alias[a["addendum_proposed_TR_alias"] + "@1"] = a["root_specified_TR"] + "@1"
    alias[a["addendum_proposed_AUDIT_alias"] + "@1"] = a["root_specified_AUDIT"] + "@1"
assert len(alias) == 14

emap = {e["object_id"]: e for e in add["evidence_map"]}
assert len(emap) == 153
updates = base["updates"] + add["updates"]
assert len({u["object_id"] for u in updates}) == 142
assert set(emap) == {u["object_id"] for u in updates} | {c["object_id"] for c in base["creates"]}
replacement = {(r["object_id"], r["field"]): r for r in add["replace_base_proposed_fields"]}
assert len(replacement) == 2
for u in updates:
    for field, patch in u["fields"].items():
        key = (u["object_id"], field)
        if key in replacement:
            r = replacement[key]
            assert patch["before"] == r["before"] and patch["after"] == r["previous_proposed_after"]
            patch["after"] = r["after"]
anders_patch = {r["object_id"]: r for r in anders["replace_or_add_proposed_fields"]}
assert len(anders_patch) == 4
for u in updates:
    r = anders_patch.get(u["object_id"])
    if r is None:
        continue
    assert u["current_revision"] == r["current_revision"] and u["kind"] == r["kind"]
    field = r["field"]
    if field in u["fields"]:
        assert u["fields"][field] == {"before": r["before"], "after": r["previous_proposed_after"]}
    else:
        assert r["previous_proposed_after"] is None
    after = r["after"]
    if u["object_id"] == "THEME-P-0032-HAL":
        old = "inskrivningslängden bär längd, bröstvidd och synskärpa"
        assert after.count(old) == 1
        after = after.replace(old, "den ännu olästa inskrivningslängden kan ge hälsouppgifter")
    u["fields"][field] = {"before": r["before"], "after": after}


def mapped_evidence(oid, existing):
    em = emap[oid]
    result = [dict(e) for e in existing]
    for x in result:
        if x["object"] in ("R-ac9bd9bbd4cf62fd811703f3", "R-80948be72f379ba2fb5df81d"):
            assert x["version"] == 1
            x["version"] = 2  # same bounded source, current head; role/note unchanged
    for e in em["evidence"]:
        basis = alias.get(e["basis_revision"], e["basis_revision"])
        bid, version = basis.rsplit("@", 1)
        if oid == "THEME-P-0033-MIL" and basis == "THEME-P-0033-MIL@2":
            continue  # Native forbids an inactive predecessor as its own support.
        role = e["role"]
        note = e.get("note", f"Exakta egna rader {e.get('rows', [])} i godkänd källjämförelse; samma uppslag, ingen oberoende extra röst.")
        if note == "Exact own rows from approved comparison v2; future dependency, no current head claimed.":
            note = "Exakta egna rader i godkänd jämförelse v2; versionsbundet transkriptionsstöd från samma original, ingen ytterligare oberoende källa."
        if oid == "O-T0676-C0916-r13-right-fields" and bid in (
            "F-P-0033-military_registration-737", "THEME-P-0033-MIL"
        ):
            role = "context"
            note = "Tidigare T-0675-reservation förklarar källpostens caveat; inte stöd för denna rads rånot."
        if oid in ("R-ac9bd9bbd4cf62fd811703f3", "R-80948be72f379ba2fb5df81d"):
            assert len(existing) == 1 and existing[0]["object"] == "S-0720"
            assert bid == "S-0720"
            continue  # Keep exactly the pre-existing source-only role and note.
        prior = next((x for x in result if x["object"] == bid and x["version"] == int(version)), None)
        if prior:
            # Structural dependencies may already carry a different role/note. Keep them;
            # add no duplicate source voice for the same exact revision.
            continue
        result.append({"object": bid, "version": int(version), "role": role, "note": note})
    if oid in ("TR-9da30932457fc977d33fd03c", "TR-b8732181ace6188abb2052a6"):
        new_r = next(e["basis_revision"] for e in em["evidence"] if e["basis_revision"].startswith("R-"))
        bid, version = new_r.rsplit("@", 1)
        assert any(x["object"] == bid and x["version"] == int(version) for x in result)
    return result


def json_data(kind, data):
    data = dict(data)
    for key in ("value_json", "date_json", "scope_json"):
        if key in data and isinstance(data[key], str):
            data[key] = json.loads(data[key])
    return data


def revision(u):
    oid = u["object_id"]
    kind, rev, data, origins, evidence, extra = current(oid)
    assert kind == u["kind"] and rev["id"] == u["current_revision"], oid
    expected_fields = set(emap[oid]["fields"])
    if oid in anders_patch:
        expected_fields.add("body")
    assert set(u["fields"]) == expected_fields, oid
    metadata = {"disposition": rev["disposition"], "evidence_status": rev["evidence_status"],
                "rationale": rev["rationale"], "caveat": rev["caveat"]}
    for field, patch in u["fields"].items():
        old = metadata[field] if field in metadata else data[field]
        if field in ("value_json", "date_json", "scope_json") and isinstance(old, str):
            old = json.loads(old)
        expected_before = patch["before"]
        if field in ("value_json", "date_json", "scope_json") and isinstance(expected_before, str):
            expected_before = json.loads(expected_before)
        assert old == expected_before, (oid, field, "before mismatch")
        if field in metadata:
            metadata[field] = patch["after"]
        else:
            data[field] = patch["after"]
    if kind == "transcription":
        assert "text" not in u["fields"]
    return {"id": oid, "kind": kind, "expectedVersion": rev["version"],
            "data": json_data(kind, data), "disposition": metadata["disposition"],
            "evidenceStatus": metadata["evidence_status"], "rationale": metadata["rationale"],
            "caveat": metadata["caveat"], "origins": origins,
            "evidence": mapped_evidence(oid, evidence), **extra}


changes = [revision(u) for u in updates]
for c in base["creates"]:
    oid, kind = c["object_id"], c["kind"]
    assert conn.execute("SELECT 1 FROM object WHERE id=?", (oid,)).fetchone() is None
    if kind == "observation":
        fields = ("record_id", "mention_id", "property", "value_literal", "value_json")
    else:
        fields = ("subject_id", "criteria", "outcome", "body")
    create_evidence = mapped_evidence(oid, [])
    if kind == "observation" and c["mention_id"] is not None:
        mention = current(c["mention_id"])
        assert mention[0] == "mention" and mention[1]["version"] == 1
        create_evidence.append({"object": c["mention_id"], "version": 1,
                                "role": "derived_from", "note": "Versionsbunden strukturreferens: mention_id"})
    changes.append({"id": oid, "kind": kind, "expectedVersion": None,
                    "data": {k: c[k] for k in fields}, "disposition": c["disposition"],
                    "evidenceStatus": c.get("evidence_status"),
                    "rationale": "T-0676: Astra-godkänd avgränsad egenradsadoption eller gap-only-observation; ingen identitetsuppgradering.",
                    "caveat": c["caveat"], "origins": [], "evidence": create_evidence})

source_changes = skeleton["sourceChangesForLaterIntegration"]
for c in source_changes:
    assert conn.execute("SELECT 1 FROM object WHERE id=?", (c["id"],)).fetchone() is None
    # Their raw comparison limits are retained as historical proposal text, while
    # this final review records the approved comparison and subsequent follow-up.
    if c["kind"] == "transcription":
        body = json.loads(c["data"]["text"])
        body["historical_proposal_limits"] = body.pop("limits")
        body["source_comparison_status"] = "Root Astra approved comparison v2 and follow-up v3/addendum v2; full own-row extraction reviewed with reservations."
        body["final_review_status"] = "Full relevant source-unit disposition and individually reviewed dependent knowledge; reservations and older reading layers retained."
        c["data"]["text"] = json.dumps(body, ensure_ascii=False, indent=2)
    else:
        body = json.loads(c["data"]["body"])
        if "limits" in body:
            body["historical_proposal_limits"] = body.pop("limits")
        body["final_review_status"] = "Root Astra approved comparison v2 and follow-up v3/addendum v2; own-row audit reviewed with reservations."
        c["data"]["body"] = json.dumps(body, ensure_ascii=False, indent=2)
changes += source_changes
assert len(changes) == 167
assert len(stale["entries"]) == 84
change_by_id = {c["id"]: c for c in changes}
for entry in stale["entries"]:
    c = change_by_id[entry["consumer"]]
    old_id, old_version = entry["basis"].rsplit("@", 1)
    new_id, new_version = entry["required_head"].rsplit("@", 1)
    assert old_id == new_id
    expected_note = entry["note"]
    if expected_note == "Exact own rows from approved comparison v2; future dependency, no current head claimed.":
        expected_note = "Exakta egna rader i godkänd jämförelse v2; versionsbundet transkriptionsstöd från samma original, ingen ytterligare oberoende källa."
    hits = [e for e in c["evidence"] if e["object"] == old_id and e["version"] == int(old_version)
            and e["role"] == entry["role"] and e["note"] == expected_note]
    assert len(hits) == 1, entry
    hits[0]["version"] = int(new_version)

# Root-approved Sigrid/Signe precision is merged into the *same* revisions.
assert signe["base_operation_sha256"] == "149cf092893fe57def1011443ee061dd2fff68c28bf932507f0375e01e1c02d1"
assert len(signe["patches"]) == 59
before_signe_ids = set(change_by_id)
extra_ids = set()
for patch in signe["patches"]:
    oid, field = patch["object_id"], patch["field"]
    kind, rev, data, origins, evidence, extra = current(oid)
    assert kind == patch["kind"] and rev["id"] == patch["current_revision"]
    old = rev[field] if field in rev else data[field]
    assert old == patch["current_before"], (oid, field, "Signe current")
    c = change_by_id.get(oid)
    if c is None:
        c = {"id": oid, "kind": kind, "expectedVersion": rev["version"],
             "data": json_data(kind, data), "disposition": rev["disposition"],
             "evidenceStatus": rev["evidence_status"], "rationale": rev["rationale"],
             "caveat": rev["caveat"], "origins": origins,
             "evidence": evidence, **extra}
        change_by_id[oid] = c
        changes.append(c)
        extra_ids.add(oid)
        assert patch["v3_proposed_after"] is None
    else:
        prior = c["caveat"] if field == "caveat" else c["data"].get(field)
        assert prior == patch["v3_proposed_after"], (oid, field, "Signe v3")
    after = patch["after"]
    if oid == "P-0033/Q-04" and field == "body":
        assert after.count("- Aktuell precisering:") == 1
        after = after.replace("- Aktuell precisering:",
                              "- Aktuell precisering: Aktuellt slutsatsläge: BESVARAD MED RESERVATION; Sigrid är den föredragna läsningen i de prövade bokposterna, medan egen födelsepost är oläst.", 1)
    if field == "caveat":
        c["caveat"] = after
    else:
        c["data"][field] = after
assert len(extra_ids) == 10
q04 = change_by_id["P-0033/Q-04"]
assert q04["data"]["outcome"] == "OMSTRIDD"
q04["data"]["outcome"] = "BESVARAD MED RESERVATION"

R_SOURCE_ONLY = {"R-35997ad1ebc94017b8342f58", "R-80948be72f379ba2fb5df81d"}
TR_1930 = "TR-229d24d8de11d92ac9e7d9b0"
O_1930 = "O-P-0033-wife1930_economy"
M_SIGNE = "M-P-0033-Signe-Elisabet-Vikner"
M_SIGRID = "M-P-0033-Sigrid-Elisabet-Vikner"
for oid in {p["object_id"] for p in signe["patches"]}:
    c = change_by_id[oid]
    if oid in R_SOURCE_ONLY:
        assert len(c["evidence"]) == 1 and c["evidence"][0]["object"].startswith("S-")
        continue
    if oid == TR_1930:
        assert not any(e["object"] == O_1930 for e in c["evidence"])
        continue
    add_basis = [TR_1930] if oid in (M_SIGNE, M_SIGRID) else [TR_1930, O_1930]
    for bid in add_basis:
        version = 3 if bid == TR_1930 else 2
        assert not any(e["object"] == bid and e["version"] == version for e in c["evidence"]), (oid, bid)
        c["evidence"].append({"object": bid, "version": version, "role": "supports",
                              "note": "T-0675:s föredragna Sigridläsning och äldre Signe som läshistorik; samma bokkedja, ingen ytterligare oberoende källa."})
    assert not (oid == M_SIGNE and any(e["object"] == O_1930 for e in c["evidence"]))

# Only explicitly authorized same-packet version binds; preserve role and note.
authorized_rebinds = {"R-35997ad1ebc94017b8342f58": (1, 2),
                      "R-80948be72f379ba2fb5df81d": (1, 2),
                      M_SIGNE: (2, 3), M_SIGRID: (1, 2),
                      "E-marriage-P-0033-1926": (1, 2), TR_1930: (2, 3)}
same_packet_rebindings = []
for c in changes:
    for e in c["evidence"]:
        rule = authorized_rebinds.get(e["object"])
        if rule and e["version"] == rule[0]:
            same_packet_rebindings.append({"consumer": c["id"], "basis": e["object"],
                                           "fromVersion": rule[0], "toVersion": rule[1],
                                           "role": e["role"], "note": e["note"]})
            e["version"] = rule[1]
assert len(changes) == 177

# All in-packet versioned dependencies must be introduced before their users.
by_id = {c["id"]: c for c in changes}
assert len(by_id) == 177
deps = {}
for c in changes:
    deps[c["id"]] = {e["object"] for e in c["evidence"]
                     if e["object"] in by_id and
                     e["version"] == (by_id[e["object"]]["expectedVersion"] or 0) + 1}
    assert c["id"] not in deps[c["id"]]
for c in changes:
    if c["expectedVersion"] is None:
        continue
    for user in changes:
        if user["id"] == c["id"]:
            continue
        if any(e["object"] == c["id"] and e["version"] == c["expectedVersion"]
               for e in user["evidence"]):
            deps[c["id"]].add(user["id"])
ordered = []
remaining = dict(by_id)
while remaining:
    ready = [oid for oid in remaining if not (deps[oid] & remaining.keys())]
    assert ready, {oid: list(deps[oid] & remaining.keys()) for oid in remaining}
    for oid in ready:
        ordered.append(remaining.pop(oid))
assert len(ordered) == 177

operation = {"id": "T-0676/umea1839-combined-proposed-v4", "actor": "Codex",
             "reason": "T-0676: full primärenhetsdisposition för sju egna Umeå 1839-källposter och individuell följdprövning; 288 fält, källbundna rättelser och avgränsade adoptioner utan nya P/M/identity.",
             "dependencyReviewVersion": 2, "changes": ordered}
OUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {"task": "T-0676", "mode": "PROPOSAL_ONLY", "canonicalApply": False,
          "baselineJournal": 178, "baseSha256": EXPECTED[BASE], "addendumSha256": EXPECTED[ADD],
          "skeletonSha256": hashlib.sha256(SKELETON.read_bytes()).hexdigest(),
          "andersPatchSha256": EXPECTED[ANDERS],
          "approvedStaleDependencyManifestSha256": EXPECTED[STALE],
          "sigridAddendumSha256": EXPECTED[SIGNE],
          "sigridNewRevisionObjects": sorted(extra_ids), "samePacketRebindings": same_packet_rebindings,
          "operation": str(OUT.relative_to(ROOT)), "operationSha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
          "changes": len(ordered), "updates": len(updates) + len(extra_ids), "creates": len(base["creates"]) + len(source_changes),
          "sourceChanges": len(source_changes), "exactAfterFields": sum(len(u["fields"]) for u in updates) + 11 + 1,
          "kinds": dict(Counter(c["kind"] for c in ordered)), "aliasMap": alias,
          "RSourceOnly": all(len(c["evidence"]) == 1 and c["evidence"][0]["object"] == "S-0720"
                             for c in ordered if c["id"] in ("R-ac9bd9bbd4cf62fd811703f3", "R-80948be72f379ba2fb5df81d")),
          "noCanonicalApply": True}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": report["operation"], "sha256": report["operationSha256"],
                  "changes": report["changes"], "fields": report["exactAfterFields"]}, ensure_ascii=False))
