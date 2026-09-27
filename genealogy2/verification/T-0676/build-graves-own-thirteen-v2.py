"""Build the bounded 13-card proposal after Astra's five exact corrections.

This only prepares a versioned operation. It never applies it to the canonical
database or resolves a dependency review.
"""

import copy
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ORIGINAL = HERE / "graves-own-thirteen-proposed-operation.json"
OUTPUT = HERE / "graves-own-thirteen-proposed-operation-v2.json"
DECISIONS = HERE / "graves-own-thirteen-root-corrections-20260920.json"

source_bytes = ORIGINAL.read_bytes()
assert hashlib.sha256(source_bytes).hexdigest() == (
    "9d7d9a907c147556d1289f34b597fe01a06e29f16c2c87a2d8478bbad026923b"
)
operation = json.loads(source_bytes)
assert operation["id"] == "T-0676/graves-own-thirteen-v1"
assert len(operation["changes"]) == 133
assert len(operation["media"]) == 13

replacements = {
    "R-31841e54a960c1d066ce0486": (
        "gravsättningsdatum är tomt",
        "gravsättningsfältet visar streck (-), utan datum",
    ),
    "R-bb35194c8e5226cab4d0a8bd": (
        "födelse-/dödsdatum tomma",
        "födelse-/dödsfälten visar streck (-), utan datum",
    ),
    "R-c780069a70fe332c281db67b": (
        "födelse-/dödsdatum tomma",
        "födelse-/dödsfälten visar streck (-), utan datum",
    ),
}
for change in operation["changes"]:
    if change["id"] not in replacements:
        continue
    before, after = replacements[change["id"]]
    assert change["caveat"].count(before) == 1
    change["caveat"] = change["caveat"].replace(before, after, 1)


def inspect(object_id):
    raw = subprocess.check_output(
        ["node", "genealogy2/cli.mjs", "inspect", object_id],
        cwd=ROOT,
        text=True,
    )
    return json.loads(raw)


def preserve_fact(object_id):
    inspected = inspect(object_id)
    assert inspected["kind"] == "fact"
    current = inspected["current"]
    data = {
        "subject_id": current["subject_id"],
        "property": current["property"],
        "value_type": current["value_type"],
        "value_json": json.loads(current["value_json"]),
    }
    return {
        "id": object_id,
        "kind": "fact",
        "expectedVersion": inspected["currentVersion"],
        "data": data,
        "disposition": current["disposition"],
        "evidenceStatus": current["evidence_status"],
        "rationale": current["rationale"],
        "caveat": current["caveat"],
        "origins": [
            {"unit": row["unit_id"], "coverage": row["coverage"], "note": row["note"]}
            for row in current["origins"]
        ],
        "evidence": [
            {
                "object": row["basis_revision_id"].rsplit("@", 1)[0],
                "version": int(row["basis_revision_id"].rsplit("@", 1)[1]),
                "role": row["role"],
                "note": row["note"],
            }
            for row in current["evidence"]
        ],
    }


def add_evidence(change, object_id, version, role, note):
    assert not any(e["object"] == object_id and e["version"] == version for e in change["evidence"])
    change["evidence"].append(
        {"object": object_id, "version": version, "role": role, "note": note}
    )


fredberg = preserve_fact("F-P-0287-sibling_context-separate-households")
old_tail = "gravregistret saknar lokal kopia."
new_tail = (
    "Den exakta äldre registerkopian från 2026-09-06 saknas; egna kort för de tio "
    "Fredbergposterna är bevarade med URL/hash 2026-09-20 och Götas eget kort är "
    "bevarat genom T-0675. Nya fångster innebär ingen gemensam familjeflytt "
    "eller ny släktkant."
)
assert fredberg["expectedVersion"] == 1
assert fredberg["caveat"].endswith(old_tail)
fredberg["caveat"] = fredberg["caveat"][: -len(old_tail)] + new_tail

fredberg_scopes = [7, 9, 18, 23, 27, 29, 35, 36, 39, 50]
for scope in fredberg_scopes:
    audit = next(c for c in operation["changes"] if c["id"] == f"AUDIT-T0676-{scope}")
    source_id = audit["data"]["subject_id"]
    transcript = next(
        e for e in audit["evidence"] if e["object"].startswith("TR-") and e["version"] == 2
    )
    old_sources = [e for e in fredberg["evidence"] if e["object"] == source_id]
    # Göran and Johan Daniel are among the ten own cards but had no direct
    # old R binding in this particular sibling-context fact.
    assert len(old_sources) in (0, 1)
    if old_sources:
        assert old_sources[0]["version"] == 1
        old_sources[0]["version"] = 2
    add_evidence(
        fredberg,
        transcript["object"],
        2,
        "supports",
        f"Eget Fredbergkort i T-0676 scope {scope}, daterad full avskrift; gravplats är ingen ny relation.",
    )

for object_id in ("TR-T0675-GR-1", "AUDIT-T0675-GR-1"):
    assert inspect(object_id)["currentVersion"] == 1
    add_evidence(
        fredberg,
        object_id,
        1,
        "supports",
        "Götas egenkort och avgränsade samgravskontext prövades i T-0675; ingen ny läsning.",
    )

carlman = preserve_fact("F-P-0240-family_context-Carlman")
old_sentence = (
    "Elins egen fullpost/hemortskort är inte bevarat genom dessa andra kort; "
    "att hon nämns i samma gravlista löser inte hennes egenpostsprovenans."
)
new_sentence = (
    "Elins egen fullpost med hemort Stockholm är nu bevarad med URL/hash "
    "2026-09-20; detta är en ny daterad fångst, inte den saknade äldre "
    "registerkopian. De andra kortens medgravsrader ersätter fortfarande inte "
    "hennes eget hemortsfält."
)
assert carlman["expectedVersion"] == 2
assert carlman["caveat"].count(old_sentence) == 1
carlman["caveat"] = carlman["caveat"].replace(old_sentence, new_sentence, 1)
for binding in carlman["evidence"]:
    if binding["object"] in {
        "R-a8370dbf4e1405f70f6bb851",
        "R-f4d105360ebbe9d50156ac10",
    }:
        assert binding["version"] == 1
        binding["version"] = 2
add_evidence(
    carlman,
    "TR-b5dd53d6e0402272b0a0c9d6",
    2,
    "supports",
    "Elins eget nybevarade kort med hemort Stockholm; de andra kortens medgravsrad ersätter inte egenposten.",
)
add_evidence(
    carlman,
    "AUDIT-T0676-37",
    1,
    "supports",
    "Avgränsad full egenkortsaudit för Elin, utan ny identitets- eller familjekant.",
)

operation["id"] = "T-0676/graves-own-thirteen-v2"
operation["reason"] = (
    operation["reason"] + " Astra 2026-09-20: tre gravfältsråformer och två "
    "metadataföljder preciserade; exakt äldre kopia förblir historiskt saknad."
)
operation["changes"].extend([fredberg, carlman])
assert len(operation["changes"]) == 135
assert len({change["id"] for change in operation["changes"]}) == 135

OUTPUT.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
decisions = {
    "task": "T-0676",
    "decisionDate": "2026-09-20",
    "proposalBuildDate": "2026-09-24",
    "originalOperation": str(ORIGINAL.relative_to(ROOT)),
    "originalSha256": hashlib.sha256(source_bytes).hexdigest(),
    "operation": str(OUTPUT.relative_to(ROOT)),
    "operationSha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    "scope9AssetsFinding": "Alla 13 R@1 hade noll äldre assets och noll native assets; assetsPreserved:false var en rapportetikett som testade om den gamla listan var icke-tom.",
    "rawFieldCorrections": replacements,
    "metadataCorrections": [
        {"object": fredberg["id"], "expectedVersion": 1, "old": old_tail, "new": new_tail, "newEvidence": "tio egna TR@2 plus Götas TR/AUDIT@1"},
        {"object": carlman["id"], "expectedVersion": 2, "old": old_sentence, "new": new_sentence, "newEvidence": "Elins TR@2 och AUDIT37@1"},
    ],
    "approvedNormativeV2Decisions": "graves-own-followup-decisions-v2-20260920.json, 107 exakta afterData/afterMetadata bevarade",
    "canonicalApply": False,
    "dependencyResolutions": 0,
}
DECISIONS.write_text(json.dumps(decisions, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": str(OUTPUT), "sha256": decisions["operationSha256"], "changes": len(operation["changes"]), "media": len(operation["media"]), "decisionFile": str(DECISIONS)}, ensure_ascii=False))
