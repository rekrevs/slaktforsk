"""Capture and compare canonical C-0002 pending requests; no resolution."""
import hashlib
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / 'genealogy2/data/research.sqlite'
TEMP = HERE / 'c0002-preliminary-temp-pending-full-20260924.json'
ROOT_DECISIONS = HERE / 'c0002-root-pending-substantive-decisions-20260924.json'
OP = HERE / 'c0002-combined-preliminary-operation-20260924.json'
OUT = HERE / 'c0002-actual-pending-full-20260924.json'
MATCH = HERE / 'c0002-actual-pending-match-20260924.json'

def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

temp, decisions = load(TEMP), load(ROOT_DECISIONS)
assert decisions['input_sha256'] == sha(TEMP)
conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
def rows(sql, args=()): return [dict(x) for x in conn.execute(sql, args)]

def full(rid):
    revs = rows('SELECT * FROM revision WHERE id=?', (rid,))
    assert len(revs) == 1, rid
    rev = revs[0]
    objs = rows('SELECT kind FROM object WHERE id=?', (rev['object_id'],))
    assert len(objs) == 1, rid
    kind = objs[0]['kind']
    data = rows(f'SELECT * FROM {kind} WHERE revision_id=?', (rid,))
    assert len(data) == 1, rid
    data = data[0]
    data.pop('revision_id')
    if 'value_json' in data and data['value_json'] is not None:
        data['value_json'] = json.loads(data['value_json'])
    origins = rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?', (rid,))
    evidence = rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?', (rid,))
    return {'kind': kind, 'revision': rev, 'data': data, 'origins': origins,
            'evidence': evidence}

pending = rows('''SELECT rr.* FROM review_request rr
                  LEFT JOIN review_resolution rs ON rs.request_id=rr.id
                  WHERE rr.operation_id=? AND rs.request_id IS NULL ORDER BY rr.id''',
               ('T-0677/C0002-source-copy-witness-v1',))
assert len(pending) == 8
requests = []
for r in pending:
    requests.append({**r, 'affected_full': full(r['affected_revision_id']),
                     'changed_full': full(r['changed_revision_id'])})
actual = {'task': 'T-0677', 'state': 'CANONICAL_ACTUAL_PENDING_NOT_RESOLVED',
          'operation_path': str(OP.relative_to(ROOT)), 'operation_sha256': sha(OP),
          'count': len(requests), 'requests': requests, 'no_resolution': True}
OUT.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + '\n')

temp_by = {r['id']: r for r in temp['requests']}
actual_by = {r['id']: r for r in requests}
decision_by = {r['request_id']: r for r in decisions['decisions']}
assert set(actual_by) == set(temp_by) == set(decision_by)
discrepancies = []
for rid, r in actual_by.items():
    t = temp_by[rid]
    for key in ('operation_id', 'reason', 'affected_revision_id', 'changed_revision_id',
                'affected_full', 'changed_full'):
        if r[key] != t[key]:
            discrepancies.append({'request_id': rid, 'field': key,
                                  'temp': t[key], 'canonical': r[key]})
    d = decision_by[rid]
    for key in ('affected_revision_id', 'changed_revision_id'):
        if r[key] != d[key]:
            discrepancies.append({'request_id': rid, 'field': 'decision.'+key,
                                  'decision': d[key], 'canonical': r[key]})
assert not discrepancies, discrepancies[:2]
match = {'task': 'T-0677', 'state': 'CANONICAL_ACTUAL_PENDING_MATCHED_NOT_RESOLVED',
         'canonical_journal_head': 181, 'operation_sha256': sha(OP),
         'actual_pending_path': str(OUT.relative_to(ROOT)), 'actual_pending_sha256': sha(OUT),
         'temp_pending_sha256': sha(TEMP), 'root_decisions_sha256': sha(ROOT_DECISIONS),
         'counts': {'actual': 8, 'temp': 8, 'root_decisions': 8, 'discrepancies': 0},
         'request_ids': sorted(actual_by), 'discrepancies_only': discrepancies,
         'no_resolution': True}
MATCH.write_text(json.dumps(match, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'actual_sha256': sha(OUT), 'match_sha256': sha(MATCH),
                  'counts': match['counts']}))
