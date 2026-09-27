"""Read-only documentary reuse inventory for C-0004 family 1 at journal 180."""

import hashlib
import json
import sqlite3
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / "genealogy2/data/research.sqlite"
RID = "R-31970be0126dcd188cd61fd1"
TR = "TR-a8032582dc1ddfcd8e94d243"
READ = "READ-1b6b3b4126358da6e0912cd7"
MEDIA_SHA = "f5052aeb1042aa29cda002060057133f0fc2ef76d20975b69a42b8871938bce1"
CITATION = ROOT / "genealogy/citations/C-0004-zingmark-hushall-folkrakning-1900.md"
T0149 = ROOT / "wotan/dev-log/T-0149.md"
T0154 = ROOT / "wotan/dev-log/T-0154.md"
OUT = HERE / "c0004-documentary-reuse-candidate-20260924.json"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row


def rows(sql, args=()):
    return [dict(row) for row in conn.execute(sql, args)]


def one(sql, args=()):
    result = rows(sql, args)
    assert len(result) == 1, (sql, args)
    return result[0]


def current(oid):
    kind = one("SELECT kind FROM object WHERE id=?", (oid,))["kind"]
    rev = one("SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1", (oid,))
    data = one(f"SELECT * FROM {kind} WHERE revision_id=?", (rev["id"],))
    data.pop("revision_id")
    return {"id": rev["id"], "kind": kind, "data": data,
            "disposition": rev["disposition"], "evidence_status": rev["evidence_status"],
            "rationale": rev["rationale"], "caveat": rev["caveat"],
            "evidence": rows("SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role", (rev["id"],)),
            "origins": rows("SELECT unit_id,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id", (rev["id"],))}


head = one("SELECT sequence,operation_id FROM operation_payload ORDER BY sequence DESC LIMIT 1")
assert head["sequence"] == 180
record = current(RID)
assert record["id"] == RID + "@1" and record["data"]["source_id"] == "S-0005"
assets = rows("SELECT asset_path,region FROM record_asset WHERE revision_id=?", (record["id"],))
assert len(assets) == 1 and "C-0004" in assets[0]["asset_path"]
asset_metadata = one("SELECT path,sha256,bytes,frozen FROM asset WHERE path=?", (assets[0]["asset_path"],))
assert asset_metadata["sha256"] == MEDIA_SHA
assert rows("SELECT * FROM record_media WHERE revision_id=?", (record["id"],)) == []
transcription = current(TR)
reading = current(READ)
assert transcription["id"] == TR + "@1" and transcription["data"]["record_id"] == RID
assert reading["id"] == READ + "@1" and reading["data"]["subject_id"] == RID

own_observation_ids = [r["revision_id"].rsplit("@", 1)[0] for r in rows(
    "SELECT revision_id FROM observation WHERE record_id=? ORDER BY revision_id", (RID,))]
own_mention_ids = [r["revision_id"].rsplit("@", 1)[0] for r in rows(
    "SELECT revision_id FROM mention WHERE record_id=? ORDER BY revision_id", (RID,))]
assert len(own_observation_ids) == 4 and not own_mention_ids
observations = [current(oid) for oid in own_observation_ids]

direct = rows("""SELECT d.revision_id,o.kind,d.role,d.note
                 FROM dependency d JOIN revision r ON r.id=d.revision_id
                 JOIN object o ON o.id=r.object_id
                 WHERE d.basis_revision_id=? ORDER BY o.kind,d.revision_id""", (record["id"],))
assert len(direct) == 14
direct_current = []
for d in direct:
    oid = d["revision_id"].rsplit("@", 1)[0]
    snapshot = current(oid)
    assert snapshot["id"] == d["revision_id"]
    direct_current.append({"basisRole": d["role"], "basisNote": d["note"], "object": snapshot})
counts = dict(Counter(d["kind"] for d in direct))
assert counts == {"assessment": 1, "fact": 1, "observation": 4, "relation": 7, "transcription": 1}
assert not any(d["kind"] in ("event", "participation", "mention") for d in direct)

negative = current("SEARCH-P-0529-C-0004-household")
assert negative["kind"] == "search" and negative["data"]["outcome"] == "negative"
negative_scope = json.loads(negative["data"]["scope_json"])
assert negative_scope["bounds"]["record"] == RID and negative_scope["bounds"]["household_only"] is True
assert negative_scope["bounds"]["whole_book"] is False

person_packs = []
for pid in ("P-0001", "P-0028", "P-0029", "P-0030", "P-0031", "P-0032", "P-0033", "P-0034"):
    path = HERE / f"prestart-person-{pid}.json"
    pack = json.loads(path.read_text())
    assert pack["journal_head"]["sequence"] == 180
    person_packs.append({"person": pid, "display_name": pack["person_full"]["payload"]["person"]["display_name"],
                         "research_inspected": pack["counts"]["research_inspected"],
                         "artifact": str(path.relative_to(ROOT)),
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})

provenance = [{"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
              for path in (CITATION, T0149, T0154)]
citation_text = CITATION.read_text()
assert "fem\nsyskon" in citation_text and "Utdrag ur Församlingsboken för\nDegerfors" in citation_text
assert "`sex syskon`" in citation_text

candidate = {
    "task": "T-0677", "mode": "DOCUMENTARY_REUSE_CANDIDATE_ONLY",
    "journal_head": head, "no_original_opened": True, "no_native_or_wotan_mutation": True,
    "no_current_revision_proposed": True,
    "citation": "C-0004", "primary_family_scope": "Degerfors Rosinedahl s.127 familj 1; Folk_024008-127, index Folk_111886797",
    "provenance_files": provenance,
    "media_metadata_only": {"asset": asset_metadata, "region": assets[0]["region"],
                            "dimensions_documented_in_citation": [800, 1387],
                            "bytes_not_opened_in_this_preparation": True},
    "person_packs": person_packs,
    "current_exact_carriers": {"record": record, "transcription": transcription, "reading": reading},
    "own_observations": observations, "own_mention_ids": own_mention_ids,
    "direct_native_dependents": direct_current,
    "direct_native_dependent_counts": counts,
    "direct_event_participation_mention_links": {"event": 0, "participation": 0, "mention": 0},
    "legacy_claims_literal": "A-0001, A-0002, A-0005, A-0013–A-0017, A-0033–A-0040, A-0160–A-0163, A-0165–A-0167 och A-0169, A-0171, A-0173, A-0175, A-0177; tillägg A-5446 (P-0028).",
    "documented_reading_history": [
        {"event": "Initial preserved citation reading", "date": "2026-08-19", "location": "C-0004 exact locator/diplomatic transcription", "scope": "Eight named household lines under Rosinedahl household 1; full printed column inventory not documented."},
        {"event": "T-0149 sibling-count correction", "date": "2026-09-08", "location": "T-0149 line 90 and C-0004 T-0149 addition", "scope": "Six listed children total imply five siblings for Oskar; older 'six siblings' remains historical and was not propagated to A-0040."},
        {"event": "T-0154 documentary dependence check", "date": "2026-09-08", "location": "T-0154 lines 60–64,92 and C-0004 T-0154 addition", "scope": "Saved document header identified as extract from Degerfors parish book. Census extract/index/parish book are not independent voices for the same field."},
    ],
    "documentation_limits_for_root": {
        "printed_column_headers": "No complete printed column-header inventory in preserved C-0004/TR; only pipe-separated eight-line working transcription.",
        "blank_cells": "No row-by-row explicit blank-cell inventory documented; omitted pipe fields must not be recast as read blanks or negative life facts.",
        "independent_full_read": "No documented independent FIRST/SECOND full-cell comparison for this family; T-0149 is a count correction and T-0154 checks the document header/dependence.",
        "relationship_inference": "Listed family roles are source statements; existing native relations remain separately assessed. This candidate does not adjudicate new kinship.",
    },
    "separate_negative_search": {"object": negative, "scope_bounds": negative_scope["bounds"],
                                 "routing": "T-0732 negative search scope for P-0529; not a positive C-0004 family member or an independent source voice."},
    "next_review": "Root Astra must decide whether documentary reuse suffices for any field and which bounded control reading, if any, is needed; this candidate itself makes no source decision.",
}
assert not OUT.exists()
OUT.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n")
assert one("SELECT sequence,operation_id FROM operation_payload ORDER BY sequence DESC LIMIT 1") == head
print(json.dumps({"artifact": str(OUT.relative_to(ROOT)),
                  "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
                  "persons": len(person_packs), "ownObservations": len(observations),
                  "ownMentions": len(own_mention_ids), "directDependents": counts}, ensure_ascii=False))
