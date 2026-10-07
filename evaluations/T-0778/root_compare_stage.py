"""Independent read-only comparison of reviewed stage and actual canonical DB.

Compare current revisions globally, plus all rows for each affected object.
SQL row order is normalized; embedded JSON array order is preserved.
"""
import argparse
import datetime
import json
import pathlib
import sqlite3

B = pathlib.Path(__file__).resolve().parent
R = B.parents[1]
p = argparse.ArgumentParser()
p.add_argument("stage")
p.add_argument("operations", nargs="+")
p.add_argument("--output", required=True)
a = p.parse_args()

def connect(path):
    d = sqlite3.connect("file:" + str(pathlib.Path(path).resolve()) + "?mode=ro", uri=True)
    d.row_factory = sqlite3.Row
    return d

stage = connect(a.stage)
live = connect(R / "genealogy2/data/research.sqlite")
changes = {}
for path in a.operations:
    for change in json.loads(pathlib.Path(path).read_text())["changes"]:
        changes[change["id"]] = change["kind"]

def rows(db, sql, args=()):
    result = []
    for row in db.execute(sql, args):
        data = dict(row)
        for key, value in data.items():
            if key.endswith("_json") and value is not None:
                data[key] = json.loads(value)
        result.append(data)
    return sorted(result, key=lambda x: json.dumps(x, sort_keys=True))

current_sql = "select r.* from revision r where r.version=(select max(version) from revision where object_id=r.object_id)"
current_equal = rows(stage, current_sql) == rows(live, current_sql)
checks = []
for oid, kind in changes.items():
    rid = live.execute("select id from revision where object_id=? order by version desc limit 1", (oid,)).fetchone()
    if rid is None:
        checks.append({"id": oid, "pass": False, "missing": True})
        continue
    rid = rid["id"]
    comparisons = {}
    tables = [(kind, "revision_id"), ("dependency", "revision_id"), ("origin", "revision_id")]
    if kind == "record":
        tables += [("record_asset", "revision_id"), ("record_media", "revision_id")]
    for table, column in tables:
        sql = "select * from " + table + " where " + column + "=?"
        comparisons[table] = rows(stage, sql, (rid,)) == rows(live, sql, (rid,))
    checks.append({"id": oid, "revision": rid, "pass": all(comparisons.values()), "fields": comparisons})
pending_sql = "select q.* from review_request q left join review_resolution r on q.id=r.request_id where r.request_id is null"
pending = rows(live, pending_sql)
result = {
    "at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "all_current_revision_records_identical_to_reviewed_stage": current_equal,
    "current_revision_count": len(rows(live, current_sql)),
    "full_current_knowledge_rows_dependency_and_origin_objects_checked": len(checks),
    "checks": checks,
    "pending": len(pending),
    "pass": current_equal and all(x["pass"] for x in checks) and not pending,
}
pathlib.Path(a.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "checks"}, indent=2))
assert result["pass"], "Actual canonical state differs from reviewed stage or has pending reviews"
