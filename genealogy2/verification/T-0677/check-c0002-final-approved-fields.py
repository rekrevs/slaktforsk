"""Independent read-only field comparison of C-0002 final operation to approvals."""
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / 'genealogy2/data/research.sqlite'
OP = HERE / 'c0002-combined-preliminary-operation-20260924.json'
OLD = HERE / 'c0002-combined-preliminary-operation-20260924-pre-timeless.json'
SOURCE = HERE / 'c0002-native-source-decisions-proposed-20260924.json'
COPY = HERE / 'c0002-copy-build-input-rootapproved-20260924.json'
WITNESS = HERE / 'c0002-witness-followup-decisions-proposed-20260924.json'
OUT = HERE / 'c0002-final-approved-fields-independent-check-20260924.json'
DELTA = HERE / 'c0002-final-timeless-delta-20260924.json'

def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

op, old = load(OP), load(OLD)
source, copy, witness = load(SOURCE), load(COPY), load(WITNESS)
omap = {c['id']: c for c in op['changes']}
oldmap = {c['id']: c for c in old['changes']}
assert len(omap) == len(oldmap) == 86
delta = []
for oid, before in oldmap.items():
    after = omap[oid]
    if before == after: continue
    top = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    fields = sorted(k for k in set(before['data']) | set(after['data'])
                    if before['data'].get(k) != after['data'].get(k))
    assert top == ['data'] and fields == ['body'], (oid, top, fields)
    delta.append({'id': oid, 'field': 'data.body',
                  'before': before['data']['body'], 'after': after['data']['body']})
assert {x['id'] for x in delta} == {'AUDIT-T0677-C0002', 'ADOPT-T0677-C0002-P-0028'}
DELTA.write_text(json.dumps({'prior_operation_sha256': sha(OLD), 'final_operation_sha256': sha(OP),
                             'only_changed_fields': delta, 'other_operation_changes': 0,
                             'prior_temp_validators_applicable_to_unchanged_structure_and_evidence': True},
                            ensure_ascii=False, indent=2) + '\n')

conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
def current(c):
    if c['expectedVersion'] is None: return None
    rev = conn.execute('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',
                       (c['id'],)).fetchone()
    assert rev is not None and rev['version'] == c['expectedVersion'], c['id']
    row = dict(conn.execute(f'SELECT * FROM {c["kind"]} WHERE revision_id=?',
                            (rev['id'],)).fetchone())
    row.pop('revision_id')
    if 'value_json' in row and row['value_json'] is not None:
        row['value_json'] = json.loads(row['value_json'])
    return {'data': row, 'caveat': rev['caveat'], 'revision': rev['id']}

baselines = {oid: current(c) for oid, c in omap.items()}
expected = {}
source_ids = set()
for c in source['proposed_changes']:
    oid, after = c['id'], c['after']
    source_ids.add(oid)
    data = dict(after['data'])
    if oid == 'AUDIT-T0677-C0002':
        old_text = 'Root v4-copyimpact hanteras separat.'
        new_text = 'Kopierättelserna ingår i samma versionsbundna operation enligt c0002-copy-build-input-rootapproved-20260924.json (SHA-256 f9479ca8092f0d1d79064ea808ee87186102e2ea8cd8a01d6c0ea5341f0e74b4) och c0002-root-substantive-acceptance-20260924.json (SHA-256 bc60e39a02557b547d6656d8dcbb5a2222b6d8c72e7d39f5ceacdbda1a17e2d7).'
        assert data['body'].count(old_text) == 1
        data['body'] = data['body'].replace(old_text, new_text)
    elif oid == 'ADOPT-T0677-C0002-P-0028':
        old_text = 'Aktuella kopior rättas enligt root v4.'
        new_text = 'Aktuella kopior rättas enligt rootgodkänt copy-v5 och dess två PATH-preciseringar, SHA-256 f9479ca8092f0d1d79064ea808ee87186102e2ea8cd8a01d6c0ea5341f0e74b4; rootacceptans SHA-256 bc60e39a02557b547d6656d8dcbb5a2222b6d8c72e7d39f5ceacdbda1a17e2d7.'
        assert data['body'].count(old_text) == 1
        data['body'] = data['body'].replace(old_text, new_text)
    caveat = after['caveat']
    if oid.startswith('M-P-0001-C0002-witness'):
        old_text = 'Fadderkolumnen är kontext, inte identitetsbelägg.'
        assert caveat.count(old_text) == 1
        caveat = caveat.replace(old_text, 'Ingen ny personidentifikation görs från fadderkolumnen i denna granskning.')
    expected[oid] = {'data': data, 'caveat': caveat}

for oid, c in omap.items():
    if oid not in source_ids:
        assert baselines[oid] is not None
        expected[oid] = {'data': dict(baselines[oid]['data']), 'caveat': baselines[oid]['caveat']}

copy_field_keys = set()
for p in copy['changes']:
    oid, field = p['object_id'], p['field']
    copy_field_keys.add((oid, field))
    before = baselines[oid]['data'].get(field, baselines[oid]['caveat'] if field == 'caveat' else None)
    proposal_before = json.loads(p['before']) if field == 'value_json' else p['before']
    proposal_after = json.loads(p['after']) if field == 'value_json' else p['after']
    assert before == proposal_before, (oid, field, 'copy before')
    if field == 'caveat': expected[oid]['caveat'] = proposal_after
    else: expected[oid]['data'][field] = proposal_after

for p in witness['changes']:
    oid, field = p['object_id'], p['field']
    before = baselines[oid]['data'].get(field, baselines[oid]['caveat'] if field == 'caveat' else None)
    proposal_before = json.loads(p['current_before']) if field == 'value_json' else p['current_before']
    proposal_after = json.loads(p['after']) if field == 'value_json' else p['after']
    assert before == proposal_before, (oid, field, 'witness before')
    if (oid, field) in copy_field_keys:
        assert (oid, field) == ('BIO-P-0001', 'caveat')
        assert expected[oid]['caveat'] == p['copy_v5_after']
    if field == 'caveat': expected[oid]['caveat'] = proposal_after
    else: expected[oid]['data'][field] = proposal_after

discrepancies = []
fields_checked = 0
for oid, proposed in expected.items():
    actual = omap[oid]
    for field in sorted(set(proposed['data']) | set(actual['data'])):
        fields_checked += 1
        if proposed['data'].get(field) != actual['data'].get(field):
            discrepancies.append({'id': oid, 'field': 'data.' + field,
                                  'approved': proposed['data'].get(field), 'operation': actual['data'].get(field)})
    fields_checked += 1
    if proposed['caveat'] != actual['caveat']:
        discrepancies.append({'id': oid, 'field': 'caveat',
                              'approved': proposed['caveat'], 'operation': actual['caveat']})

patterns = defaultdict(list)
for oid, c in omap.items():
    if baselines[oid] is None:
        old_edges = []
    else:
        rev = baselines[oid]['revision']
        old_edges = []
        for r in conn.execute('SELECT basis_revision_id, role, note FROM dependency WHERE revision_id=?', (rev,)):
            basis, version = r['basis_revision_id'].rsplit('@', 1)
            old_edges.append({'object': basis, 'version': int(version), 'role': r['role'], 'note': r['note']})
    new_edges = c.get('evidence', [])
    for direction, edges in [('added', [e for e in new_edges if e not in old_edges]),
                             ('removed', [e for e in old_edges if e not in new_edges])]:
        for e in edges:
            key = (direction, e['object'], e['version'], e['role'], e['note'])
            patterns[key].append(oid)
pattern_rows = [{'direction': k[0], 'basis': k[1], 'version': k[2], 'role': k[3],
                 'note': k[4], 'targets': sorted(v)} for k, v in sorted(patterns.items())]
assert not discrepancies, discrepancies[:3]
report = {'task': 'T-0677', 'state': 'INDEPENDENT_FIELD_CHECK_FOR_ROOT_REVIEW',
          'operation_sha256': sha(OP), 'prior_operation_sha256': sha(OLD),
          'input_sha256': {p.name: sha(p) for p in (SOURCE, COPY, WITNESS)},
          'counts': {'objects': len(expected), 'source_objects': len(source_ids),
                     'copy_fields': len(copy['changes']), 'witness_fields': len(witness['changes']),
                     'all_typed_data_and_caveat_fields_checked': fields_checked,
                     'discrepancies': len(discrepancies), 'unique_evidence_patterns': len(pattern_rows)},
          'discrepancies_only': discrepancies, 'deduplicated_evidence_patterns': pattern_rows,
          'timeless_delta_path': str(DELTA.relative_to(ROOT)), 'timeless_delta_sha256': sha(DELTA),
          'canonical_apply': False}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'operation_sha256': sha(OP), 'delta_sha256': sha(DELTA),
                  'check_sha256': sha(OUT), 'counts': report['counts']}))
