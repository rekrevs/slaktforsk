#!/usr/bin/env python3
"""Read-only independent partition/lock/Wotan check, no database rebuild."""
import collections
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
d = Path(__file__).resolve().parent
read = lambda p: json.loads(p.read_text())
m = read(d / 'manifest.json')
c = read(d / 'cohorts-draft.json')
own = read(d / 'ownership.json')
p = read(d / 'priority.json')
b = read(root / 'wotan/backlog.json')
assert hashlib.sha256((d / 'manifest.json').read_bytes()).hexdigest() == own['manifest_sha256'] == c['manifest_sha256']
assert hashlib.sha256((d / 'cohorts-draft.json').read_bytes()).hexdigest() == own['cohorts_sha256'] == p['cohorts_sha256']
keys = {'citations':'id','legacy_sources':'id','records':'object_id','sources':'object_id','searches':'object_id','imported_assets':'path','native_assets':'id'}
counts = {}
for kind, key in keys.items():
    expected = [r[key] for r in m[kind]]
    actual = [v for g in c['cohorts'] for v in g['members'].get(kind, [])]
    assert len(expected) == len(set(expected))
    assert collections.Counter(actual) == collections.Counter(expected), kind
    counts[kind] = len(actual)
cohorts = {g['cohort_key'] for g in c['cohorts']}
assert set(own['cohort_tasks']) == cohorts
assert {r['cohort_key'] for r in p['recommended_cohort_order']} == cohorts
assert len(p['recommended_cohort_order']) == len(cohorts) == 91
for kind, rows in c['support_association_owners'].items():
    assert sorted(r['manifest_index'] for r in rows) == list(range(len(m[kind])))
    for row in rows:
        assert row['owner_cohort'] in cohorts
        raw = json.dumps(m[kind][row['manifest_index']], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        assert hashlib.sha256(raw).hexdigest() == row['row_sha256']
    counts[kind] = len(rows)
hashes = {a['sha256'] for k in ['imported_assets','native_assets'] for a in m[k]}
assert collections.Counter(r['sha256'] for r in c['content_reading_owners']) == collections.Counter(hashes)
assert all(r['owner_cohort'] in cohorts for r in c['content_reading_owners'])
tasks = {t['id']:t for t in b['tasks']}
assert len(tasks) == len(b['tasks'])
for tid in own['cohort_tasks'].values():
    assert tid in tasks and (root / 'wotan/dev-log' / (tid+'.md')).is_file()
    assert 'T-0673' in tasks[tid]['after']
final = tasks[own['final_audit_task']]
assert set(own['cohort_tasks'].values()).issubset(final['after'])
assert {'T-0671','T-0672'}.issubset(final['after'])
assert b['next_id'] > max(int(t[2:]) for t in tasks)
print(json.dumps({'result':'PASS','counts':counts,'distinct_content_hashes':len(hashes),'cohort_tasks':91,'final_audit':final['id'],'limit':'Exact scope and ownership only, not substantive original verification.'},ensure_ascii=False,indent=2))
