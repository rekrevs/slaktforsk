"""Build the settled C0016 specification and test only in a new isolated database."""
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
    return [{'object': x.rsplit('@', 1)[0], 'version': int(x.rsplit('@', 1)[1]), 'role': 'supports', 'note': 'T-0677 C-0016: versionsbundet underlag inom den avgränsade käll- och följdbedömningen.'} for x in ids]

def norm(value):
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    if isinstance(value, list):
        return sorted([norm(v) for v in value], key=lambda x: json.dumps(x, sort_keys=True))
    return value

spec_path = HERE / 'c0016-settled-implementation-spec-20260930.json'
spec = json.loads(spec_path.read_text())
db = sqlite3.connect(f'file:{ROOT}/genealogy2/data/research.sqlite?mode=ro', uri=True)
db.row_factory = sqlite3.Row
assert sorted((ROOT / 'genealogy2/journal').glob('*.json'))[-1].name.startswith('000000202-')
for oid in ['E-birth-P-0042', 'E-marriage-P-0042-P-0043-1886']:
    assert full(db, oid)['revision']['version'] == 1
source = {'id': spec['source_operation_id'], 'actor': 'Codex Sol implementation of settled Astra C0016 specification', 'reason': 'T-0677 AC1/2: avgränsad fullkolumnavskrift och fyra råobservationer med bevarade reservationer.', 'changes': copy.deepcopy(spec['source_new_objects'])}
for change in source['changes']:
    assert full(db, change['id']) is None
    change['expectedVersion'] = None
    change.setdefault('caveat', '')
    change.setdefault('origins', [])
    change.setdefault('evidenceStatus', None)

tr = 'TR-T0677-C0016-consolidated-control@1'
audit = 'AUDIT-T0677-C0016@1'
facts = {x['subject']: x for x in spec['new_person_facts']}
person = {'id': spec['person_operation_id'], 'actor': source['actor'], 'reason': 'T-0677 AC3: exakt beslutade textföljder, två källjämförelser och fem avgränsade adoptioner; oförändrade person- och trädutfall.', 'changes': []}
before = {}
by_id = {}
for edit in spec['existing_edits']:
    oid = edit['id']
    if oid not in by_id:
        old = full(db, oid)
        before[oid] = old
        rev = old['revision']
        change = {'id': oid, 'kind': old['kind'], 'expectedVersion': rev['version'], 'disposition': rev['disposition'], 'evidenceStatus': rev['evidence_status'], 'rationale': rev['rationale'] + ' T-0677 AC3, C-0016: beslutade fältpreciseringar enligt den låsta individuella följdspecifikationen; övriga uppgifter och utfall bevaras.', 'caveat': rev['caveat'], 'data': copy.deepcopy(old['data']), 'origins': old['origins'], 'evidence': copy.deepcopy(old['evidence'])}
        additions = [tr, audit]
        subject = old['data'].get('subject_id')
        if subject in facts:
            additions += [facts[subject]['id'] + '@1']
        change['evidence'] += evidence(additions)
        by_id[oid] = change
        person['changes'].append(change)
    change = by_id[oid]
    value = change['data'][edit['field']]
    if edit['mode'] == 'replace_once':
        assert value.count(edit['old']) == 1, (oid, edit['field'], value.count(edit['old']))
        value = value.replace(edit['old'], edit['new'], 1)
    else:
        assert edit['mode'] == 'append'
        value += edit['text']
    change['data'][edit['field']] = value

new_facts = []
for fact in spec['new_person_facts']:
    new_facts.append({'id': fact['id'], 'kind': 'fact', 'expectedVersion': None, 'data': {'subject_id': fact['subject'], 'property': fact['property'], 'value_type': 'structured', 'value_json': {'body': fact['body'], 'limits': 'Källjämförelse med uttryckliga reservationer; inga nya normaliserade födelse- eller vigseldatum.'}}, 'disposition': 'recorded', 'evidenceStatus': 'TRANSCRIBED', 'rationale': 'T-0677 AC3: individuellt beslutad källjämförelse; råuppgifter hålls åtskilda från personslutsatser.', 'caveat': 'Befintliga datum, identiteter och person-/trädutfall består.', 'origins': [], 'evidence': evidence(fact['basis'] + [audit])})
# Facts precede consumers so all new bindings exist at application time.
person['changes'] = new_facts + person['changes']
for pid, body in spec['adoptions'].items():
    bases = [tr, audit]
    if pid in facts:
        bases.append(facts[pid]['id'] + '@1')
    person['changes'].append({'id': 'ADOPT-T0677-C0016-' + pid, 'kind': 'assessment', 'expectedVersion': None, 'data': {'subject_id': pid, 'criteria': 'bounded_source_adoption/1', 'outcome': 'adopted_with_limits', 'body': body}, 'disposition': 'recorded', 'evidenceStatus': None, 'rationale': 'T-0677 AC3: individuell adoption inom C-0016, inte full personkontraktsgranskning.', 'caveat': 'Övriga källskulder och person-/trädutfall bevaras.', 'origins': [], 'evidence': evidence(bases)})
for change in person['changes']:
    if change['expectedVersion'] is None:
        assert full(db, change['id']) is None
assert len(source['changes']) == 6 and len(person['changes']) == 15
source_path = save('c0016-source-proposed-operation-20260930.json', source)
person_path = save('c0016-person-proposed-operation-20260930.json', person)
save('c0016-implementation-before-j202-20260930.json', before)
temp_root = Path(tempfile.mkdtemp(prefix='t0677-c0016-20260930-', dir='/private/tmp'))
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
    save(f'c0016-temp-{label}-20260930.json', value)
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
save('c0016-temp-full-object-diff-20260930.json', {'objects': diffs, 'all_exact': True})
save('c0016-temp-pending-full-20260930.json', {'count': len(pending), 'requests': pending})
summary = {'task': 'T-0677', 'state': 'ISOLATED_TEMP_ONLY_AWAITING_ASTRA_REVIEW', 'spec_sha256': sha(spec_path), 'temp_database': str(temp_db), 'canonical_base': 202, 'source_objects': 6, 'person_objects': 15, 'new_objects': 13, 'revised_objects': 8, 'pending': len(pending), 'full_objects_exact': True, 'operations': {str(p.relative_to(ROOT)): sha(p) for p in [source_path, person_path]}, 'results': results}
save('c0016-temp-preflight-summary-20260930.json', summary)
print(json.dumps({k: v for k, v in summary.items() if k != 'results'}, ensure_ascii=False))
