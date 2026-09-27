"""Read-only current CLI view snapshot for five C-0004 family-1 persons."""

import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PERSONS = ("P-0030", "P-0031", "P-0032", "P-0033", "P-0034")
JOURNAL = max((ROOT / "genealogy2/journal").glob("*.json"))
assert JOURNAL.name.startswith("000000180-"), JOURNAL
journal_head = {"journal_file": str(JOURNAL.relative_to(ROOT)), "sequence": 180,
                "sha256": hashlib.sha256(JOURNAL.read_bytes()).hexdigest()}


def cli(args):
    process = subprocess.run(["node", "genealogy2/cli.mjs", *args], cwd=ROOT,
                             capture_output=True, text=True)
    assert process.returncode == 0, (args, process.stderr)
    return {"command": "node genealogy2/cli.mjs " + " ".join(args),
            "exit": process.returncode, "payload": json.loads(process.stdout),
            "stderr": process.stderr}


for person_id in PERSONS:
    with ThreadPoolExecutor(max_workers=2) as pool:
        person_future = pool.submit(cli, ["person", person_id, "--full", "--format", "json"])
        inspect_future = pool.submit(cli, ["inspect", person_id])
        person = person_future.result()
        inspect = inspect_future.result()
    assert person["payload"]["id"] == person_id
    assert inspect["payload"]["object"] == person_id
    groups = person["payload"]["research"]
    identifiers = sorted({row["object_id"] for group in groups.values() for row in group})
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda oid: (oid, cli(["inspect", oid])), identifiers))
    research_inspects = dict(results)
    assert len(research_inspects) == len(identifiers)
    for oid, result in research_inspects.items():
        assert result["payload"]["object"] == oid
    pack = {"task": "T-0677", "person_id": person_id,
            "purpose": "read_only_prestart_current_cli_views", "journal_head": journal_head,
            "person_full": person, "person_inspect": inspect,
            "research_inspects": research_inspects,
            "counts": {"research_groups": {k: len(v) for k, v in groups.items()},
                       "research_inspected": len(research_inspects)}}
    path = HERE / f"prestart-person-{person_id}.json"
    assert not path.exists(), path
    path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n")
    print(person_id, person["payload"]["person"]["display_name"], len(research_inspects),
          hashlib.sha256(path.read_bytes()).hexdigest(), flush=True)

assert max((ROOT / "genealogy2/journal").glob("*.json")) == JOURNAL
