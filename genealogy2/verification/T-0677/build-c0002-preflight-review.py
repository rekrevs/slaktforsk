"""Read-only canonical comparison of the frozen C-0002 temp operation."""
import hashlib
import json
import sqlite3
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / 'genealogy2/data/research.sqlite'
OP = HERE / 'c0002-combined-preliminary-operation-20260924.json'
BUILD = HERE / 'c0002-combined-preliminary-buildcheck-20260924.json'
PENDING = HERE / 'c0002-preliminary-temp-pending-full-20260924.json'
TEMP_OP = HERE / 'c0002-combined-preliminary-operation-20260924-pre-timeless.json'
TIMELESS_DELTA = HERE / 'c0002-final-timeless-delta-20260924.json'
FIELD_CHECK = HERE / 'c0002-final-approved-fields-independent-check-20260924.json'
FILES = {name: HERE / f'c0002-preliminary-temp-{name}-result-20260924.json'
         for name in ('apply', 'verify', 'verify-assets', 'verify-source')}
DIFF = HERE / 'c0002-preliminary-actual-diff-20260924.json'
SUMMARY = HERE / 'c0002-preliminary-temp-preflight-summary-20260924.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    return json.loads(path.read_text())

op, build, pending = load(OP), load(BUILD), load(PENDING)
timeless_delta, field_check = load(TIMELESS_DELTA), load(FIELD_CHECK)
assert op['id'] == 'T-0677/C0002-source-copy-witness-v1'
assert op['dependencyReviewVersion'] == 2
assert build['operation_sha256'] == sha(OP)
assert timeless_delta['prior_operation_sha256'] == sha(TEMP_OP)
assert timeless_delta['final_operation_sha256'] == sha(OP)
assert len(timeless_delta['only_changed_fields']) == 2
assert pending['operation_sha256'] == sha(TEMP_OP)
assert field_check['operation_sha256'] == sha(OP)
assert field_check['counts']['discrepancies'] == 0
assert len(op['changes']) == 86
conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
conn.row_factory = sqlite3.Row

def rows(sql, args=()):
    return [dict(r) for r in conn.execute(sql, args)]

def current(oid, kind):
    obj = rows('SELECT kind FROM object WHERE id=?', (oid,))
    assert len(obj) == 1 and obj[0]['kind'] == kind, oid
    revs = rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1', (oid,))
    assert len(revs) == 1, oid
    rev = revs[0]
    data = rows(f'SELECT * FROM {kind} WHERE revision_id=?', (rev['id'],))
    assert len(data) == 1, oid
    data = data[0]
    data.pop('revision_id')
    if 'value_json' in data and data['value_json'] is not None:
        data['value_json'] = json.loads(data['value_json'])
    origins = [{'unit': r['unit_id'], 'coverage': r['coverage'], 'note': r['note']}
               for r in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?', (rev['id'],))]
    evidence = []
    for r in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?', (rev['id'],)):
        obj_id, ver = r['basis_revision_id'].rsplit('@', 1)
        evidence.append({'object': obj_id, 'version': int(ver), 'role': r['role'], 'note': r['note']})
    return rev, data, origins, evidence

items = []
data_field_deltas = 0
metadata_field_deltas = 0
for change in op['changes']:
    oid, kind, expected = change['id'], change['kind'], change['expectedVersion']
    after = {k: change[k] for k in ('data', 'disposition', 'evidenceStatus', 'rationale', 'caveat')}
    after['origins'] = change.get('origins', [])
    after['evidence'] = change.get('evidence', [])
    if expected is None:
        assert not rows('SELECT id FROM object WHERE id=?', (oid,)), oid
        items.append({'id': oid, 'kind': kind, 'action': 'create', 'expectedVersion': None,
                      'before': None, 'after': after})
        continue
    rev, data, origins, evidence = current(oid, kind)
    assert rev['version'] == expected, (oid, rev['version'], expected)
    before = {'data': data, 'disposition': rev['disposition'],
              'evidenceStatus': rev['evidence_status'], 'rationale': rev['rationale'],
              'caveat': rev['caveat'], 'origins': origins, 'evidence': evidence}
    assert before['origins'] == after['origins'], oid
    data_deltas = {k: {'before': data[k], 'after': after['data'][k]}
                   for k in sorted(set(data) | set(after['data']))
                   if data.get(k) != after['data'].get(k)}
    metadata_deltas = {k: {'before': before[k], 'after': after[k]}
                       for k in ('disposition', 'evidenceStatus', 'rationale', 'caveat')
                       if before[k] != after[k]}
    evidence_removed = [e for e in evidence if e not in after['evidence']]
    evidence_added = [e for e in after['evidence'] if e not in evidence]
    data_field_deltas += len(data_deltas)
    metadata_field_deltas += len(metadata_deltas)
    items.append({'id': oid, 'kind': kind, 'action': 'revise', 'expectedVersion': expected,
                  'currentRevision': rev['id'], 'before': before, 'after': after,
                  'data_field_deltas': data_deltas, 'metadata_field_deltas': metadata_deltas,
                  'evidence_removed': evidence_removed, 'evidence_added': evidence_added,
                  'origins_preserved': True})

actions = Counter(x['action'] for x in items)
assert actions == {'create': 7, 'revise': 79}, actions
diff = {'task': 'T-0677', 'state': 'TEMP_VALIDATED_FOR_ROOT_REVIEW_NOT_CANONICAL_APPLY',
        'canonical_base_journal': 180, 'operation_id': op['id'], 'operation_sha256': sha(OP),
        'counts': {'objects': len(items), 'creates': actions['create'], 'revisions': actions['revise'],
                   'revised_data_field_deltas': data_field_deltas,
                   'revised_metadata_field_deltas': metadata_field_deltas},
        'items': items}
DIFF.write_text(json.dumps(diff, ensure_ascii=False, indent=2) + '\n')
results = {name: {'path': str(path.relative_to(ROOT)), 'sha256': sha(path), 'result': load(path)}
           for name, path in FILES.items()}
assert results['apply']['result']['changes'] == 86
for name in ('verify', 'verify-assets', 'verify-source'):
    assert results[name]['result']['ok'] is True, name
summary = {
    'task': 'T-0677', 'state': 'FINAL_TEXT_ONLY_DELTA_FROM_TEMP_VALIDATED_OPERATION_FOR_ROOT_REVIEW',
    'canonical_base_journal': 180, 'canonical_pending_at_last_check': 0,
    'operation_id': op['id'], 'operation_path': str(OP.relative_to(ROOT)), 'operation_sha256': sha(OP),
    'buildcheck_path': str(BUILD.relative_to(ROOT)), 'buildcheck_sha256': sha(BUILD),
    'actual_diff_path': str(DIFF.relative_to(ROOT)), 'actual_diff_sha256': sha(DIFF),
    'actual_diff_counts': diff['counts'], 'temp_results': results,
    'temp_validated_operation_sha256': sha(TEMP_OP),
    'final_operation_differs_from_temp_only_in_two_timeless_body_fields': True,
    'timeless_delta_path': str(TIMELESS_DELTA.relative_to(ROOT)),
    'timeless_delta_sha256': sha(TIMELESS_DELTA),
    'independent_field_check_path': str(FIELD_CHECK.relative_to(ROOT)),
    'independent_field_check_sha256': sha(FIELD_CHECK),
    'temp_pending_path': str(PENDING.relative_to(ROOT)), 'temp_pending_sha256': sha(PENDING),
    'temp_pending_count': results['apply']['result']['pendingReviews'],
    'temp_journal_written': results['apply']['result']['journal']['written'],
    'canonical_apply': False, 'pending_resolutions': False,
}
assert summary['temp_pending_count'] == 8 and summary['temp_journal_written'] == 181
SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'diff_sha256': sha(DIFF), 'summary_sha256': sha(SUMMARY),
                  'operation_sha256': sha(OP), 'counts': diff['counts']}, ensure_ascii=False))
