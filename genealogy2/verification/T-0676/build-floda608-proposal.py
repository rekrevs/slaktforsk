"""Prepare approved Floda 608 correction against journal 175; no canonical apply."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COMPARISON = HERE / "floda608-comparison-20260924.json"
PROPOSAL = HERE / "floda608-current-followup-proposal-20260924.json"
ADDENDUM = HERE / "floda608-followup-addendum-20260924.json"
APPROVAL = HERE / "floda608-root-preparation-approval-20260924.json"
OUTPUT = HERE / "floda608-proposed-operation.json"
REPORT = HERE / "floda608-proposal-build-20260924.json"
checks = {COMPARISON: "198cd03ce9bdbea69fc3a880b0062de952d1e905557e0c6ec21f8d1b42e28f10", PROPOSAL: "6f3f1ae91117f1588f29a19aaff9c02f975c80efff245da09fc94c7647f898d3", ADDENDUM: "e1c298c6634d5e03188f7e00066f08c5f4ff8e144d8422c3e87237dc90d721a0"}
for path, digest in checks.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
comparison = json.loads(COMPARISON.read_text())
proposal = json.loads(PROPOSAL.read_text())
addendum = json.loads(ADDENDUM.read_text())
approval = json.loads(APPROVAL.read_text())
assert approval["approval"] == "PREPARATION_ONLY"
assert approval["comparison_sha256"] == checks[COMPARISON]
assert approval["proposal_sha256"] == checks[PROPOSAL]
assert approval["addendum_sha256"] == checks[ADDENDUM]

RECORDS = {15: "R-541325e245ca3c49ebe13c72", 17: "R-60acfab3cad1b6e2563fd8f5"}
OLD_TR = {15: "TR-19ba17d654cb1bde6266a616", 17: "TR-6e32d0b6bee0c1362f946533"}
TR = {scope: f"TR-T0676-FLODA608-{scope}" for scope in RECORDS}
AUDIT = {scope: f"AUDIT-T0676-FLODA608-{scope}" for scope in RECORDS}
OBS = {15: "O-T0676-FLODA608-15-own-gap-cells", 17: "O-T0676-FLODA608-17-own-gap-cells"}
FLEN_RECORD = "R-e67bb6868b81121b2d3f0732"
FLEN_TR = "TR-T0676-FLEN914-UPPER-45"


def inspect(object_id):
    return json.loads(subprocess.check_output(["node", "genealogy2/cli.mjs", "inspect", object_id], cwd=ROOT, text=True))


def evidence(current):
    return [{"object": e["basis_revision_id"].rsplit("@", 1)[0], "version": int(e["basis_revision_id"].rsplit("@", 1)[1]), "role": e["role"], "note": e["note"]} for e in current["evidence"]]


def origins(current):
    return [{"unit": o["unit_id"], "coverage": o["coverage"], "note": o["note"]} for o in current["origins"]]


assert comparison["count"]["positions"] == 54 and len(comparison["rows"]) == 3
assert [(r["row"], r["scope"], len(r["columns"])) for r in comparison["rows"]] == [(9, 17, 18), (15, 15, 18), (16, 15, 18)]
assert all([f["column"] for f in r["columns"]] == list(range(1, 19)) for r in comparison["rows"])
assert sum(f["provenance"] == "ny luckläsning FIRST/SECOND" for r in comparison["rows"] for f in r["columns"]) == 27
changes = []
for scope in (15, 17):
    rid = RECORDS[scope]
    record = inspect(rid)
    assert record["kind"] == "record" and record["currentVersion"] == 1
    assert len(record["current"]["media"]) == 1 and record["current"]["media"][0]["sha256"] == comparison["source"]["sha256"]
    old = inspect(OLD_TR[scope])
    assert old["kind"] == "transcription" and old["currentVersion"] == 1 and old["current"]["record_id"] == rid
    own_rows = [r for r in comparison["rows"] if r["scope"] == scope]
    assert len(own_rows) == (2 if scope == 15 else 1)
    body = {"task": "T-0676", "scope": scope, "record_id": rid, "source": comparison["source"], "source_printed_header_inventory_in_approved_comparison": comparison["headers"], "all_18_column_positions_per_own_row": own_rows, "comparison_file": str(COMPARISON.relative_to(ROOT)), "comparison_sha256": checks[COMPARISON], "adjudication": comparison["adjudication"], "limits": comparison["limits"], "method": "Äldre explicita fält återbrukas med proveniens; nya luckceller hämtas från godkänd FIRST/SECOND-jämförelse. Tomma egna celler är inte negativa livsfakta."}
    changes.append({"id": TR[scope], "kind": "transcription", "expectedVersion": None,
                    "data": {"record_id": rid, "text": json.dumps(body, ensure_ascii=False, indent=2), "reading_note": f"Floda AIIa/11 Ökna608 scope{scope}: {len(own_rows)} egna rader ×18 kolumnpositioner, äldre återbruk skilt från ny luckläsning; gamla TR lämnas historiskt."},
                    "disposition": "recorded", "evidenceStatus": None,
                    "rationale": "T-0676: full relevant fälttäckning per avgränsad källpost och bevarat äldre läslager.",
                    "caveat": "Råformer V/W, o.ä.[?], [d/t?] och äldre yrkesditto bevaras med reservation. Egna tomma celler daterar inte resa, omsorg, civilstånd eller död.",
                    "origins": [], "evidence": [
                        {"object": rid, "version": 1, "role": "derived_from", "note": f"Egen avgränsad Floda608-källpost scope{scope} och bevarad originalbild."},
                        {"object": OLD_TR[scope], "version": 1, "role": "context", "note": "Äldre avskrift bevaras som historiskt läslager, inte ytterligare oberoende röst."},
                    ]})
    audit_body = {"task": "T-0676", "scope": scope, "record_id": rid, "source": comparison["source"], "comparison_file": str(COMPARISON.relative_to(ROOT)), "comparison_sha256": checks[COMPARISON], "own_rows": [r["row"] for r in own_rows], "columns_per_row": 18, "positions": 18 * len(own_rows), "limits": comparison["limits"], "duplicate_review": addendum["whole_record_observation_dupecheck"], "no_new_identity_or_pedigree_gate": True}
    changes.append({"id": AUDIT[scope], "kind": "assessment", "expectedVersion": None,
                    "data": {"subject_id": rid, "criteria": "source_record_review/1", "outcome": "reviewed_with_reservations", "body": json.dumps(audit_body, ensure_ascii=False, indent=2)},
                    "disposition": "recorded", "evidenceStatus": None,
                    "rationale": "T-0676: egen rad-/kolumngräns och full relevant fälttäckning sakgranskade med reservations- och dublettgräns.",
                    "caveat": "Samma original i äldre och nya TR; inga tomma celler blir negativa livsfakta, och ingen ny omsorgs-, relations- eller flyttdag härleds.",
                    "origins": [], "evidence": [
                        {"object": rid, "version": 1, "role": "derived_from", "note": "Befintlig egen Floda608-källpost och bild."},
                        {"object": TR[scope], "version": 1, "role": "supports", "note": "Fullt 18-kolumnsprotokoll på egen avgränsad radgrupp."},
                    ]})

for scope in (15, 17):
    allowed = addendum["whole_record_observation_dupecheck"][f"new_scope{scope}_observation_allowed_fields"]
    selected = {str(r["row"]): [c for c in r["columns"] if c["column"] in allowed[f"r{r['row']}"]] for r in comparison["rows"] if r["scope"] == scope}
    assert all(len(selected[row]) == len(allowed[f"r{row}"]) for row in selected)
    payload = {"scope": scope, "record": RECORDS[scope], "own_gap_only_fields": selected, "source_name_reservation": allowed["source_name_reservation"]}
    if scope == 17:
        payload["row9_note"] = allowed["r9_note"]
    changes.append({"id": OBS[scope], "kind": "observation", "expectedVersion": None,
                    "data": {"record_id": RECORDS[scope], "mention_id": None, "property": "newly_reviewed_own_cells", "value_literal": json.dumps(payload, ensure_ascii=False, separators=(",", ":")), "value_json": payload},
                    "disposition": "recorded", "evidenceStatus": "TRANSCRIBED",
                    "rationale": "T-0676: endast nu godkända egna luck-/reservationsceller; befintliga household_membership och parent_field dubbleras inte.",
                    "caveat": "Tomma celler är lokala boktomheter. V/W, o.ä.[?] och [d/t?] bevaras som råreservationer utan ny P/identity, faderskaps-, omsorgs-, rese- eller livshändelseslutsats.",
                    "origins": [], "evidence": [
                        {"object": RECORDS[scope], "version": 1, "role": "derived_from", "note": "Befintlig egen källpost, ingen ny originalkopia."},
                        {"object": TR[scope], "version": 1, "role": "supports", "note": "Precis de egna kolumnpositionerna inom det godkända fullprotokollet."},
                        {"object": AUDIT[scope], "version": 1, "role": "context", "note": "Dublett- och råformsgräns sakgranskad, utan oberoende extra röst."},
                    ]})

data_fields = {"fact": ("subject_id", "property", "value_type", "value_json"), "event": ("event_type", "date_json", "place_id", "place_role"), "participation": ("event_id", "person_id", "mention_id", "role"), "narrative": ("subject_id", "title", "markdown"), "assessment": ("subject_id", "criteria", "outcome", "body")}
rebase = {"BIO-P-0009": 2, "PATH-P-0009-KP-01": 2}
revision_report = []
for decision in proposal["changes"]:
    oid = decision["object_id"]
    view = inspect(oid)
    current = view["current"]
    expected = rebase.get(oid, 1)
    assert view["currentVersion"] == expected and current["revision_id"] == f"{oid}@{expected}"
    patch = decision["after_field_patch"]
    after = dict(current)
    if oid in rebase:
        if oid == "BIO-P-0009":
            before = patch["markdown_exact_replace"]["before"]
            assert current["markdown"].count(before) == 1
            after["markdown"] = current["markdown"].replace(before, patch["markdown_exact_replace"]["after"])
        else:
            assert not current["body"].startswith(patch["body_prepend"])
            after["body"] = patch["body_prepend"] + current["body"]
            after["outcome"] = patch["outcome_prepend"] + current["outcome"]
    else:
        for field, value in patch.items():
            if field in ("evidence_note_patch",):
                continue
            assert field in (*data_fields[view["kind"]], "caveat", "disposition"), (oid, field)
            after[field] = value
        if oid == "F-P-0003-residence-Okna1915-1918":
            old_value = json.loads(current["value_json"])
            assert {k: v for k, v in old_value.items() if k != "registeredDeparture"} == patch["value_json"]
        if oid == "EP-E-departure-P-0003-Floda-1918-P-0003-migrant":
            assert current["disposition"] == "accepted" and after["disposition"] == "retired"
    data = {field: after[field] for field in data_fields[view["kind"]]}
    for field in ("value_json", "date_json"):
        if field in data and isinstance(data[field], str):
            data[field] = json.loads(data[field])
    e = evidence(current)
    if oid == "EP-E-departure-P-0003-Floda-1918-P-0003-migrant":
        assert len(e) == 1 and e[0]["object"] == "E-departure-P-0003-Floda-1918" and e[0]["version"] == 1
        e[0]["version"] = 2
    if oid == "E-arrival-P-0003-Ljungbacka-1918":
        floda = next(v for v in e if v["object"] == RECORDS[15]);assert floda["role"] == "supports"
        floda["role"] = "context";floda["note"] = addendum["arrival_evidence_role_decision"]["after_note"]
        flen = next(v for v in e if v["object"] == FLEN_RECORD);assert flen["role"] == "supports"
        flen["note"] = patch["evidence_note_patch"][f"{FLEN_RECORD}@1"]
        e.append({"object": FLEN_TR, "version": 1, "role": "supports", "note": "Arnes egen Flen914-rad7 ger daterat ankomstankare 1918-10-28; samma bokkedja, inte ny oberoende källa."})
    if oid in ("F-P-0003-residence-Okna1915-1918", "E-departure-P-0003-Floda-1918"):
        e.append({"object": TR[15], "version": 1, "role": "supports", "note": "Floda608 egna r15/16 skiljer Adas daterade utflyttning från Arnes tomma flyttceller."})
    elif oid == "E-arrival-P-0003-Ljungbacka-1918":
        e.append({"object": TR[15], "version": 1, "role": "context", "note": "Floda608 ger kedjekontext och sonroll; Arnes egen ankomstdag står i Flen914."})
    elif oid == "EP-E-departure-P-0003-Floda-1918-P-0003-migrant":
        e.append({"object": TR[15], "version": 1, "role": "supports", "note": "Arnes egna Floda608-r16 kol16/17 är tomma utan ditto; direkt avskrivet deltagande avvecklas."})
    elif oid == "BIO-P-0009":
        e.append({"object": TR[15], "version": 1, "role": "supports", "note": "Adas egen utflyttning och Arnes separata tomma flyttceller på Floda608-r15/16."})
    elif oid == "PATH-P-0009-KP-01":
        for scope in (15, 17):
            e.append({"object": TR[scope], "version": 1, "role": "supports", "note": f"Fullt egna Floda608-fält scope{scope} inom denna avgränsade källvägsbedömning."})
    e.append({"object": AUDIT[15], "version": 1, "role": "context", "note": "Avgränsad källpostgranskning utan extra oberoende röst."})
    if oid == "PATH-P-0009-KP-01":
        e.append({"object": AUDIT[17], "version": 1, "role": "context", "note": "R9:s egna antecknings- och tomfältsgränser sakgranskade."})
    changes.append({"id": oid, "kind": view["kind"], "expectedVersion": expected,
                    "data": data, "disposition": after["disposition"], "evidenceStatus": current["evidence_status"],
                    "rationale": current["rationale"], "caveat": after["caveat"], "origins": origins(current), "evidence": e})
    revision_report.append({"object": oid, "expectedVersion": expected, "fields": sorted(set(after)-{k for k in after if after[k] == current[k]}), "originalEvidencePreserved": True, "newEvidence": [z["object"] for z in e if z["object"] in (TR[15], TR[17], AUDIT[15], AUDIT[17], FLEN_TR)]})

arne = approval["arne_assessment"]
assert inspect(arne["id"]).get("currentVersion") is None
changes.append({"id": arne["id"], "kind": arne["kind"], "expectedVersion": None,
                "data": arne["data"], "disposition": arne["disposition"], "evidenceStatus": None,
                "rationale": "T-0676: avgränsat tillgodoräknande av Arnes egen Floda608-rad och rättad flyttkällkedja, utan ny person- eller PK-/trädstatus.",
                "caveat": arne["caveat"], "origins": [], "evidence": [
                    {"object": RECORDS[15], "version": 1, "role": "derived_from", "note": "Egen Floda608-rad16 i befintlig källpost."},
                    {"object": TR[15], "version": 1, "role": "supports", "note": "Fullt egenradsprotokoll med tomma flyttceller utan ditto."},
                    {"object": AUDIT[15], "version": 1, "role": "context", "note": "Avgränsad sakgranskning utan ny identitets- eller släktgrind."},
                    {"object": FLEN_TR, "version": 1, "role": "supports", "note": "Arnes separata egna Flen914-rad7 med ankomstdag 1918-10-28."},
                ]})
assert len(changes) == 13
event_index = next(i for i, c in enumerate(changes) if c["id"] == "E-departure-P-0003-Floda-1918")
participation_index = next(i for i, c in enumerate(changes) if c["id"] == "EP-E-departure-P-0003-Floda-1918-P-0003-migrant")
assert event_index > participation_index
changes.insert(participation_index, changes.pop(event_index))
operation = {"id": "T-0676/floda608-scopes15-17-proposed", "actor": "Codex", "reason": "T-0676: två egna Floda608-källposter med totalt 54 fält, sex Astra-godkända rättelser, två gap-only observationer och Arnes bounded-adoption; inga nya R/M/P eller identitets-/familjekanter.", "dependencyReviewVersion": 2, "changes": changes}
OUTPUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
report = {"task": "T-0676", "mode": "PROPOSAL_ONLY", "canonicalApply": False,
          "comparisonSha256": checks[COMPARISON], "proposalSha256": checks[PROPOSAL], "addendumSha256": checks[ADDENDUM],
          "operation": str(OUTPUT.relative_to(ROOT)), "operationSha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
          "changeCount": len(changes), "sixRevisions": revision_report, "newTR": list(TR.values()), "newAudit": list(AUDIT.values()), "newGapOnlyObservations": list(OBS.values()), "arneAssessment": arne["id"], "oldTRPreserved": OLD_TR, "sourcePositions": 54, "newGapPositions": 27}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": report["operation"], "sha256": report["operationSha256"], "changes": len(changes)}, ensure_ascii=False))
