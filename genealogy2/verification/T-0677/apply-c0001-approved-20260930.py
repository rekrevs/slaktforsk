"""Apply an exactly Astra-approved post at its fixed head, then verify actual data.

Task-local mechanical executor. Does not decide evidence or approve operations.
Usage: python .../apply-approved-post-20260930.py c0012 208
"""
import ast
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
post, base_text = 'c0001', '212'
assert post.startswith('c') and post[1:].isdigit()
base = int(base_text)

def save(name, value):
    p = HERE / name
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return p

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def journal_head():
    return sorted((ROOT / 'genealogy2/journal').glob('*.json'))[-1]

def connect():
    db = sqlite3.connect(f'file:{ROOT}/genealogy2/data/research.sqlite?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    return db

def pending(db):
    return [dict(r) for r in db.execute('select q.* from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null')]

def cli(label, args):
    command = ['node', 'genealogy2/cli.mjs'] + args
    r = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    save(f'{post}-canonical-{label}-20260930.json', {'command': command, 'exit': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr})
    assert r.returncode == 0, (command, r.stdout, r.stderr)
    return json.loads(r.stdout)

approval_path = HERE / f'{post}-astra-exact-canonical-approval-20260930.json'
approval = json.loads(approval_path.read_text())
assert approval['decision'] == 'APPROVE_EXACT_THREE_CANONICAL_PACKAGES'
assert approval['base_journal'] == base
for name, digest in approval['inputs'].items():
    assert sha(HERE / name) == digest
approval['operations'] = approval['inputs']
assert int(journal_head().name[:9]) == base
db = connect()
assert not pending(db)
db.close()
changes = []
for label in ['source', 'person', 'resolutions']:
    if label == 'resolutions':
        db = connect()
        actual_pending = sorted(pending(db), key=lambda r: r['id'])
        expected_pending = json.loads((HERE / 'c0001-temp-pending-full-20260930.json').read_text())['requests']
        assert actual_pending == sorted(expected_pending, key=lambda r: r['id'])
        save('c0001-canonical-pending-before-resolution-20260930.json', {'requests': actual_pending, 'exact_temp_match': True})
        db.close()
    names = [name for name in approval['operations'] if f'-{label}-proposed-operation-' in name]
    assert len(names) == 1
    path = HERE / names[0]
    assert sha(path) == approval['operations'][path.name]
    operation = json.loads(path.read_text())
    changes.extend(operation['changes'])
    dest = ROOT / 'genealogy2/operations' / (operation['id'].replace('/', '-') + '.json')
    if dest.exists():
        assert dest.read_bytes() == path.read_bytes()
    else:
        dest.write_bytes(path.read_bytes())
    result = cli(f'{label}-apply', ['apply', str(dest)])
    print(json.dumps({'stage': label, 'result': result}), flush=True)

# Load only pure read-only comparison functions, never the builder's top-level writes.
builder = HERE / f'build-{post}-temp-20260930.py'
tree = ast.parse(builder.read_text())
pure = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ['rows', 'full', 'norm']], type_ignores=[])
helpers = {'json': json}
exec(compile(pure, 'read-only-object-helpers', 'exec'), helpers)
expected_path = HERE / f'{post}-temp-full-object-diff-20260930.json'
expected = json.loads(expected_path.read_text())
db = connect()
items = []
for item in expected['objects']:
    actual = helpers['full'](db, item['id'])
    assert helpers['norm'](actual) == helpers['norm'](item['actual']), item['id']
    items.append({'id': item['id'], 'exact': True, 'actual': actual})
assert {x['id'] for x in items} == {x['id'] for x in changes}
assert not pending(db)
actual_resolutions = [dict(r) for r in db.execute('select * from review_resolution where operation_id=? order by request_id', ('T-0677/C0001-resolutions-v1',))]
expected_resolutions = json.loads((HERE / 'c0001-temp-resolutions-receipt-20260930.json').read_text())['actual_resolutions']
assert actual_resolutions == expected_resolutions
resolution_match_path = save('c0001-canonical-resolution-match-20260930.json', {'actual': actual_resolutions, 'all_exact': True})
head = journal_head()
assert int(head.name[:9]) == base + 3
match_path = save(f'{post}-canonical-full-object-match-20260930.json', {'objects': items, 'all_exact': True, 'pending': [], 'head': head.name, 'expected_snapshot_sha256': sha(expected_path)})

def check(name):
    result = cli(name, [name])
    assert result['ok'], (name, result)
    return name, result

with ThreadPoolExecutor(max_workers=3) as pool:
    validators = dict(pool.map(check, ['verify', 'verify-assets', 'verify-source']))
receipt = {'task': 'T-0677', 'scope': post.upper() + ' bounded source and individual current consequences', 'state': 'CANONICAL_IMPLEMENTATION_VERIFIED_AWAITING_ASTRA_COMPLETION', 'verified_at_utc': datetime.now(timezone.utc).isoformat(), 'journal': base + 3, 'journal_head': head.name, 'pending': 0, 'objects': len(items), 'new_objects': sum(x['expectedVersion'] is None for x in changes), 'revised_objects': sum(x['expectedVersion'] is not None for x in changes), 'actual_full_match': True, 'validators': validators, 'artifacts': [{'file': p.name, 'sha256': sha(p)} for p in [match_path, resolution_match_path, approval_path]], 'resolutions': len(actual_resolutions), 'actual_resolution_rows_match': True}
save(f'{post}-canonical-implementation-receipt-20260930.json', receipt)
print(json.dumps(receipt, ensure_ascii=False))
