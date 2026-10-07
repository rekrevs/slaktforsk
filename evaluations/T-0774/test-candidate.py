"""Mechanical isolated test of Sol's frozen operations; no canonical writes."""
import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
baseline = json.loads((HERE / 'baseline-lock.json').read_text())
base = Path(baseline['database'])
assert hashlib.sha256(base.read_bytes()).hexdigest() == baseline['sha256']
operations = [Path(p).resolve() for p in sys.argv[1:]]
assert operations
work = Path(tempfile.mkdtemp(prefix='t0774-sol-test-', dir='/private/tmp'))
dbpath = work / 'research.sqlite'
journal = work / 'journal'
original = sqlite3.connect(f'file:{base}?mode=ro', uri=True)
copy = sqlite3.connect(dbpath)
original.backup(copy)
copy.close()
original.close()
results = {'started_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'database': str(dbpath), 'journal': str(journal), 'operations': [],
           'commands': [], 'full_object_mismatches': [], 'state': 'RUNNING'}
expected = {}

def run(args):
    process = subprocess.run(['node', str(ROOT / 'genealogy2/cli.mjs'), *args,
                              '--db', str(dbpath), '--journal', str(journal)],
                             cwd=ROOT, capture_output=True, text=True)
    entry = {'args': args, 'exit_code': process.returncode,
             'stdout': process.stdout, 'stderr': process.stderr}
    results['commands'].append(entry)
    return process.returncode == 0

try:
    for path in operations:
        operation = json.loads(path.read_text())
        assert operation['id'].startswith('T-0774/'), operation['id']
        results['operations'].append({'path': str(path), 'id': operation['id'],
                                     'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        if not run(['apply', str(path)]):
            raise RuntimeError('Isolated apply failed; retain this attempt, decide before retry.')
        for change in operation['changes']:
            expected[change['id']] = change
    db = sqlite3.connect(f'file:{dbpath}?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    actual_objects = {}
    bound = {'record': ['source_id'], 'transcription': ['record_id'],
             'mention': ['record_id'], 'observation': ['record_id', 'mention_id'],
             'identity': ['mention_id'], 'participation': ['event_id', 'mention_id']}
    def normalized(value):
        if isinstance(value, dict):
            return {k: normalized(v) for k, v in value.items()}
        if isinstance(value, list):
            return sorted((normalized(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
        return value
    for oid, change in expected.items():
        revision = dict(db.execute('select * from current_revision where object_id=?', (oid,)).fetchone())
        kind = revision['kind']
        data = dict(db.execute(f'select * from {kind} where revision_id=?', (revision['id'],)).fetchone())
        data.pop('revision_id')
        for key, value in data.items():
            if key.endswith('_json') and value is not None:
                data[key] = json.loads(value)
        evidence = []
        for dep in db.execute('select * from dependency where revision_id=?', (revision['id'],)):
            source, version = dep['basis_revision_id'].rsplit('@', 1)
            evidence.append({'object': source, 'version': int(version), 'role': dep['role'], 'note': dep['note']})
        origins = [{'unit': o['unit_id'], 'coverage': o['coverage'], 'note': o['note']}
                   for o in db.execute('select * from origin where revision_id=?', (revision['id'],))]
        actual = {'kind': kind, 'version': revision['version'], 'data': data,
                  'disposition': revision['disposition'], 'evidenceStatus': revision['evidence_status'],
                  'rationale': revision['rationale'], 'caveat': revision['caveat'],
                  'origins': origins, 'evidence': evidence}
        if kind == 'record':
            actual['assets'] = [{'path': a['asset_path'], 'region': a['region']}
                                for a in db.execute('select * from record_asset where revision_id=?', (revision['id'],))]
        ev = [{**e, 'note': e.get('note', '')} for e in change.get('evidence', [])]
        for field in bound.get(kind, []):
            target = change['data'].get(field)
            if target is not None and not any(e['object'] == target for e in ev):
                version = db.execute('select version from current_revision where object_id=?', (target,)).fetchone()[0]
                ev.append({'object': target, 'version': version, 'role': 'derived_from',
                           'note': f'Versionsbunden strukturreferens: {field}'})
        wanted = {'kind': change['kind'], 'version': (change['expectedVersion'] or 0) + 1,
                  'data': {k: change['data'].get(k) for k in data},
                  'disposition': change['disposition'], 'evidenceStatus': change.get('evidenceStatus'),
                  'rationale': change['rationale'], 'caveat': change.get('caveat', ''),
                  'origins': [{'unit': o['unit'], 'coverage': o.get('coverage', 'partial'), 'note': o.get('note', '')}
                              for o in change.get('origins', [])], 'evidence': ev}
        if kind == 'record':
            wanted['assets'] = [{'path': a['path'], 'region': a.get('region', 'helbild')}
                                for a in change.get('assets', [])]
        actual_objects[oid] = actual
        actual_compare = {k: normalized(v) if k in ('evidence', 'origins', 'assets') else v for k, v in actual.items()}
        wanted_compare = {k: normalized(v) if k in ('evidence', 'origins', 'assets') else v for k, v in wanted.items()}
        if actual_compare != wanted_compare:
            results['full_object_mismatches'].append({'id': oid, 'expected': wanted, 'actual': actual})
    (work / 'actual-full-objects.json').write_text(json.dumps(actual_objects, ensure_ascii=False, indent=2) + '\n')
    results['matched_distinct_objects'] = len(expected) - len(results['full_object_mismatches'])
    results['pending'] = [dict(r) for r in db.execute('select * from pending_review')]
    db.close()
    checks = [run([command]) for command in ['verify', 'verify-assets', 'verify-source', 'inventory']]
    checks.append(run(['pedigree', 'P-0269']))
    results['state'] = ('PASS' if all(checks) and not results['full_object_mismatches'] and not results['pending']
                        else 'REVIEW_REQUIRED')
except Exception as error:
    results['state'] = 'FAILED'
    results['error'] = str(error)
finally:
    results['ended_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = HERE / (work.name + '-receipt.json')
    receipt.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'receipt': str(receipt), 'database': str(dbpath), 'state': results['state'],
                      'matched': results.get('matched_distinct_objects'), 'pending': len(results.get('pending', []))}))
