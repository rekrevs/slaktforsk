"""Build the settled C0013 specification and test only in a new isolated database."""
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name, value):
    p = HERE / name
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return p

def rows(db, query, args=()):
    return [dict(x) for x in db.execute(query, args)]

def full(db, oid):
    rev = rows(db, 'select * from revision where object_id=? order by version desc limit 1', (oid,))
    if not rev:
        return None
    rev = rev[0]
    kind = rows(db, 'select kind from object where id=?', (oid,))[0]['kind']
    data = rows(db, f'select * from {kind} where revision_id=?', (rev['id'],))[0]
    data.pop('revision_id')
    for k, v in data.items():
        if k.endswith('_json') and v is not None:
            data[k] = json.loads(v)
    origins = [{'unit': x['unit_id'], 'coverage': x['coverage'], 'note': x['note']} for x in rows(db, 'select * from origin where revision_id=?', (rev['id'],))]
    evidence = []
    for x in rows(db, 'select * from dependency where revision_id=?', (rev['id'],)):
        oid, ver = x['basis_revision_id'].rsplit('@', 1)
        evidence.append({'object': oid, 'version': int(ver), 'role': x['role'], 'note': x['note']})
    return {'kind': kind, 'revision': rev, 'data': data, 'origins': origins, 'evidence': evidence}

def evidence(ids):
    return [{'object': x.rsplit('@', 1)[0], 'version': int(x.rsplit('@', 1)[1]), 'role': 'supports', 'note': 'T-0677 C-0013: versionsbundet underlag inom den avgränsade käll- och följdbedömningen.'} for x in ids]

def norm(value):
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    if isinstance(value, list):
        return sorted([norm(v) for v in value], key=lambda x: json.dumps(x, sort_keys=True))
    return value

spec_path = HERE / 'c0024-settled-implementation-spec-20261001.json'
spec = json.loads(spec_path.read_text())
assert spec['canonical_anchor'] == 233
db = sqlite3.connect(f'file:{ROOT}/genealogy2/data/research.sqlite?mode=ro', uri=True)
db.row_factory = sqlite3.Row
assert sorted((ROOT / 'genealogy2/journal').glob('*.json'))[-1].name.startswith('000000233-')
before = {}
def existing(oid, version):
    old = full(db, oid)
    assert old['revision']['version'] == version
    before[oid] = old
    r = old['revision']
    return {'id': oid, 'kind': old['kind'], 'expectedVersion': version, 'disposition': r['disposition'], 'evidenceStatus': r['evidence_status'], 'rationale': r['rationale'], 'caveat': r['caveat'], 'data': copy.deepcopy(old['data']), 'origins': copy.deepcopy(old['origins']), 'evidence': copy.deepcopy(old['evidence'])}
def replace_once(obj, field, old, new):
    assert obj[field].count(old) == 1, (field, old)
    obj[field] = obj[field].replace(old, new, 1)
source = {'id': spec['source_operation_id'], 'actor': 'Codex mechanical implementation of settled Astra C0024 specification', 'reason': 'T-0677 AC1–3: exakt beslutad dokumentär källklass- och proveniensrättelse.', 'dependencyReviewVersion': 2, 'changes': []}
new_objects = copy.deepcopy(spec['source_new_objects'])
for c in new_objects:
    assert full(db, c['id']) is None
    c['expectedVersion'] = None
    c.setdefault('evidenceStatus', None)
    c.setdefault('caveat', '')
    c.setdefault('origins', [])
    c.setdefault('evidence', [])
source['changes'] += [c for c in new_objects if c['kind'] != 'assessment']
for edit in spec['source_existing_edits']:
    c = existing(edit['id'], edit['expectedVersion'])
    c['data'].update(edit.get('data_set', {}))
    c.update(edit.get('metadata_set', {}))
    for r in edit.get('metadata_replacements', []):
        replace_once(c, r['field'], r['old'], r['new'])
    for rebind in edit.get('evidence_rebind', []):
        found = [e for e in c['evidence'] if e['object'] == rebind['old_object'] and e['version'] == rebind['old_version'] and e['role'] == rebind['role']]
        assert len(found) == 1
        found[0].update(object=rebind['new_object'], version=rebind['new_version'])
    for addition in edit.get('evidence_add', []):
        assert not any((e['object'], e['version'], e['role']) == (addition['object'], addition['version'], addition['role']) for e in c['evidence'])
        c['evidence'].append(copy.deepcopy(addition))
    if edit.get('rationale_append'):
        c['rationale'] += ' ' + edit['rationale_append']
    source['changes'].append(c)
source['changes'] += [c for c in new_objects if c['kind'] == 'assessment']
person = {'id': spec['person_operation_id'], 'actor': source['actor'], 'reason': 'T-0677 AC3: exakt individuellt beslutade följdrättelser och begränsade adoptioner.', 'dependencyReviewVersion': 2, 'changes': []}
by_id = {}
for edit in spec['existing_edits']:
    oid = edit['id']
    if oid not in by_id:
        c = existing(oid, edit['expectedVersion'])
        c['rationale'] += ' T-0677 AC3: individuellt beslutade följdrättelser enligt låst C0024-specifikation; övrig evidens och utfall bevaras.'
        for rebind in spec['basis_rules'].get(oid + '_rebind', []):
            found = [e for e in c['evidence'] if e['object'] == rebind['old_object'] and e['version'] == rebind['old_version'] and e['role'] == rebind['role']]
            assert len(found) == 1
            found[0].update(object=rebind['new_object'], version=rebind['new_version'])
        bases = copy.deepcopy(spec['basis_rules']['all_person_changes'])
        subject = c['data'].get('subject_id')
        if subject == 'P-0030':
            bases += copy.deepcopy(spec['basis_rules']['P-0030_additional'])
        bases += copy.deepcopy(spec['basis_rules'].get(oid + '_additional', []))
        for b in bases:
            if not any((e['object'], e['version'], e['role']) == (b['object'], b['version'], b['role']) for e in c['evidence']):
                c['evidence'].append(b)
        by_id[oid] = c
        person['changes'].append(c)
    c = by_id[oid]
    assert c['expectedVersion'] == edit['expectedVersion']
    target = c['data'] if edit['layer'] == 'data' else c
    assert edit['layer'] in ('data', 'metadata')
    if edit['mode'] == 'replace_once':
        replace_once(target, edit['field'], edit['old'], edit['new'])
    elif edit['mode'] == 'set_value':
        assert edit['layer'] == 'data'
        assert target[edit['field']] == edit['old'], (edit['id'], edit['field'])
        target[edit['field']] = copy.deepcopy(edit['new'])
    else:
        raise ValueError(edit['mode'])
for fact in spec['new_person_facts']:
    c = copy.deepcopy(fact)
    assert c['kind'] == 'fact' and full(db, c['id']) is None
    c['expectedVersion'] = None
    c.setdefault('evidenceStatus', None)
    c.setdefault('caveat', '')
    c.setdefault('origins', [])
    c.setdefault('evidence', [])
    person['changes'].append(c)
for pid, body in spec['adoptions'].items():
    oid = 'ADOPT-T0677-C0024-' + pid
    assert full(db, oid) is None
    person['changes'].append({'id': oid, 'kind': 'assessment', 'expectedVersion': None, 'data': {'subject_id': pid, 'criteria': 'bounded_source_adoption/1', 'outcome': 'reviewed_with_limits', 'body': body}, 'disposition': 'recorded', 'evidenceStatus': None, 'rationale': 'T-0677 AC1–3: individuellt beslutad dokumentär adoption inom C-0024.', 'caveat': 'Övriga källskulder och person-/trädutfall bevaras.', 'origins': [], 'evidence': copy.deepcopy(spec['basis_rules']['all_person_changes'])})
source_path = save('c0024-source-proposed-operation-20260930.json', source)
person_path = save('c0024-person-proposed-operation-20260930.json', person)
save('c0024-implementation-before-j233-20260930.json', before)
temp_root = Path(tempfile.mkdtemp(prefix='t0677-c0024-20260930-', dir='/private/tmp'))
temp_db = temp_root / 'research.sqlite'
temp = sqlite3.connect(temp_db)
db.backup(temp)
temp.row_factory = sqlite3.Row
temp.close()
results = {}
for label, args in [('source', ['apply', str(source_path)]), ('person', ['apply', str(person_path)]), ('verify', ['verify']), ('verify-assets', ['verify-assets']), ('verify-source', ['verify-source'])]:
    command = ['node', 'genealogy2/cli.mjs'] + args + ['--db', str(temp_db), '--journal', str(temp_root / 'journal')]
    proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    value = {'command': command, 'exit': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
    save(f'c0024-temp-{label}-20260930.json', value)
    assert proc.returncode == 0, value
    results[label] = json.loads(proc.stdout)
temp = sqlite3.connect(f'file:{temp_db}?mode=ro', uri=True)
temp.row_factory = sqlite3.Row
diffs = []
for change in source['changes'] + person['changes']:
    actual = full(temp, change['id'])
    checks = {key: norm(actual[key]) == norm(change.get(key, [])) for key in ['data', 'origins']}
    expected_evidence = [dict(x, note=x.get('note', '')) for x in change['evidence']]
    checks['evidence'] = norm(actual['evidence']) == norm(expected_evidence)
    for key, field in [('disposition', 'disposition'), ('evidenceStatus', 'evidence_status'), ('rationale', 'rationale'), ('caveat', 'caveat')]:
        checks[key] = actual['revision'][field] == change.get(key)
    checks['version'] = actual['revision']['version'] == (change['expectedVersion'] or 0) + 1
    diffs.append({'id': change['id'], 'checks': checks, 'actual': actual})
    assert all(checks.values()), (change['id'], checks)
pending = rows(temp, 'select q.* from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null order by q.id')
save('c0024-temp-full-object-diff-20260930.json', {'objects': diffs, 'all_exact': True})
save('c0024-temp-pending-full-20260930.json', {'count': len(pending), 'requests': pending})
summary = {'task': 'T-0677', 'state': 'ISOLATED_TEMP_ONLY_AWAITING_ASTRA_REVIEW', 'spec_sha256': sha(spec_path), 'temp_database': str(temp_db), 'canonical_base': 233, 'source_objects': len(source['changes']), 'person_objects': len(person['changes']), 'new_objects': sum(c['expectedVersion'] is None for c in source['changes'] + person['changes']), 'revised_objects': sum(c['expectedVersion'] is not None for c in source['changes'] + person['changes']), 'pending': len(pending), 'full_objects_exact': True, 'operations': {str(p.relative_to(ROOT)): sha(p) for p in [source_path, person_path]}, 'results': results}
save('c0024-temp-preflight-summary-20260930.json', summary)
print(json.dumps({k: v for k, v in summary.items() if k != 'results'}, ensure_ascii=False))
