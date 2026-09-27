"""Add the two approved Flen context bindings to the Floda 608 proposal."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OLD = HERE / "floda608-proposed-operation.json"
OUT = HERE / "floda608-proposed-operation-v2.json"
REPORT = HERE / "floda608-proposal-build-v2-20260924.json"
assert hashlib.sha256(OLD.read_bytes()).hexdigest() == "1ca9825ebec93af2c763dc68cc64d56625a104cc67ed7bad435147834e13d9c7"
op = json.loads(OLD.read_text())
op["id"] = "T-0676/floda608-scopes15-17-v2-proposed"
targets = {
    "F-P-0003-residence-Okna1915-1918": "Faktumets nya caveat skiljer Floda608:s tomma egna flyttceller från Arnes egen daterade ankomst i Flen914-rad7; samma bokkedja, ingen extra oberoende källa.",
    "EP-E-departure-P-0003-Floda-1918-P-0003-migrant": "Avvecklat direkt Floda-utflyttningsdeltagande förnekar inte den separata egenregistrerade Flen914-ankomsten; endast kedjekontext.",
}
for change in op["changes"]:
    if change["id"] in targets:
        assert not any(e["object"] == "TR-T0676-FLEN914-UPPER-45" for e in change["evidence"])
        change["evidence"].append({"object": "TR-T0676-FLEN914-UPPER-45", "version": 1, "role": "context", "note": targets[change["id"]]})
assert len(op["changes"]) == 13
OUT.write_text(json.dumps(op, ensure_ascii=False, indent=2) + "\n")
report = {"task": "T-0676", "mode": "PROPOSAL_ONLY", "canonicalApply": False,
          "previousOperationSha256": hashlib.sha256(OLD.read_bytes()).hexdigest(),
          "operation": str(OUT.relative_to(HERE.parents[2])),
          "operationSha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
          "onlyChangedObjects": list(targets), "onlyChange": "Add Flen upper TR@1 as context to two revisions whose exact approved caveats mention the separate Flen arrival."}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"operation": report["operation"], "sha256": report["operationSha256"]}, ensure_ascii=False))
