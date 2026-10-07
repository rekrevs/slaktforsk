"""Read-only CLI capture with explicitly documented immutable revision reuse.

Arguments: post journal previous_post previous_journal P-id ...
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
post, sequence, previous, previous_sequence, *persons = sys.argv[1:]
persons_only = "--persons-only" in persons
persons = [p for p in persons if p != "--persons-only"]
head = sorted((ROOT / 'genealogy2/journal').glob('*.json'))[-1]
assert int(head.name[:9]) == int(sequence)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name, data):
    p = HERE / name
    assert not p.exists(), f'Capture already exists: {p}'
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return p

def run(args):
    cmd = ['node', 'genealogy2/cli.mjs'] + args
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, (cmd, r.stderr)
    return {'command': ' '.join(cmd), 'exit': 0, 'payload': json.loads(r.stdout)}

for pid in persons:
    oldpath = HERE / f'{previous}-prestart-person-{pid}-j{previous_sequence}-20260930.json'
    if not oldpath.exists() and (HERE / f'prestart-person-{pid}.json').exists():
        oldpath = HERE / f'prestart-person-{pid}.json'
    old = json.loads(oldpath.read_text()) if oldpath.exists() else {'research_inspects': {}}
    full = run(['person', pid, '--full', '--format', 'json'])
    ins = run(['inspect', pid])
    current = {x['object_id']: x['version'] for xs in full['payload']['research'].values() if isinstance(xs, list) for x in xs if isinstance(x, dict) and 'object_id' in x}
    reuse = {oid: old['research_inspects'][oid] for oid, v in current.items() if oid in old['research_inspects'] and old['research_inspects'][oid]['payload']['currentVersion'] == v}
    need = sorted(set(current) - set(reuse))
    with ThreadPoolExecutor(max_workers=4) as pool:
        new = dict(zip(need, pool.map(lambda x: run(['inspect', x]), need)))
    data = {'task': 'T-0677', 'person_id': pid, 'purpose': 'read_only_current_views_with_exact_immutable_revision_reuse', 'journal_head': {'sequence': int(sequence), 'journal_file': str(head.relative_to(ROOT)), 'sha256': sha(head)}, 'person_full': full, 'person_inspect': ins, 'research_inspects': dict(sorted((reuse | new).items())), 'capture_provenance': {'reused_from': str(oldpath.relative_to(ROOT)) if oldpath.exists() else None, 'reused_from_sha256': sha(oldpath) if oldpath.exists() else None, 'reused_exact_revision_ids': [f'{oid}@{current[oid]}' for oid in sorted(reuse)], 'new_inspect_ids': need, 'rule': 'Fresh full-person view confirms identical immutable object revisions for reused inspect payloads.'}, 'counts': {'research_objects': len(current), 'reused_inspects': len(reuse), 'new_inspects': len(new)}}
    p = save(f'{post}-prestart-person-{pid}-j{sequence}-20260930.json', data)
    print(json.dumps({'path': p.name, 'sha256': sha(p), 'counts': data['counts']}), flush=True)

if persons_only:
    assert sorted((ROOT / 'genealogy2/journal').glob('*.json'))[-1] == head
    sys.exit(0)

impact = run(['impact', post.upper().replace('C', 'C-', 1)])
a = save(f'{post}-impact-j{sequence}-20260930.json', impact)
items = impact['payload']['review']['items']
ids = sorted({x['object_id'] for x in items})
with ThreadPoolExecutor(max_workers=4) as pool:
    ins = dict(zip(ids, pool.map(lambda x: run(['inspect', x]), ids)))
assert all(x['version'] == ins[x['object_id']]['payload']['currentVersion'] for x in items if x.get('current'))
data = {'task': 'T-0677', 'purpose': 'mechanical_capture_not_substantive_review', 'journal': int(sequence), 'input_sha256': sha(a), 'impact': impact['payload'], 'inspects': ins, 'checks': {'items': len(items), 'current_heads_match': True, 'all_cli_exit_zero': True}}
p = save(f'{post}-impact-current-j{sequence}-20260930.json', data)
assert sorted((ROOT / 'genealogy2/journal').glob('*.json'))[-1] == head
print(json.dumps({'path': p.name, 'sha256': sha(p), 'checks': data['checks']}))
