"""Compare protected knowledge layers in an isolated candidate to fixed j227."""
import json
import sqlite3
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
lock = json.loads((here / 'baseline-lock.json').read_text())
assert len(sys.argv) == 2, 'Give isolated receipt path'
receipt = json.loads(Path(sys.argv[1]).read_text())
base = sqlite3.connect(f"file:{lock['database']}?mode=ro", uri=True)
candidate = sqlite3.connect(f"file:{receipt['database']}?mode=ro", uri=True)
for db in [base, candidate]:
    db.row_factory = sqlite3.Row

def current(db, kind, condition='1'):
    return {row['object_id']: dict(row) for row in db.execute(
        f'SELECT r.*, k.* FROM current_revision r JOIN {kind} k ON k.revision_id=r.id WHERE {condition}')}

checks = {}
for kind, condition, label in [('relation', '1', 'all_relation_revisions'),
                                ('assessment', "criteria='legacy_review_header'", 'legacy_gate_reviews')]:
    left, right = current(base, kind, condition), current(candidate, kind, condition)
    checks[label] = {'count_baseline': len(left), 'count_candidate': len(right),
                     'changed_ids': sorted(k for k in left.keys() | right.keys() if left.get(k) != right.get(k))}
left, right = current(base, 'person'), current(candidate, 'person')
checks['person_identity_and_legacy_state'] = {
    'count_baseline': len(left), 'count_candidate': len(right),
    'changed_ids': sorted(k for k in left.keys() | right.keys()
                          if tuple(left.get(k, {}).get(f) for f in ['display_name', 'legacy_state']) !=
                          tuple(right.get(k, {}).get(f) for f in ['display_name', 'legacy_state']))}
owner_query = "SELECT * FROM current_revision WHERE evidence_status='OWNER_CONFIRMED'"
left = {r['object_id']: dict(r) for r in base.execute(owner_query)}
right = {r['object_id']: dict(r) for r in candidate.execute(owner_query)}
checks['all_owner_confirmed_revisions'] = {'count_baseline': len(left), 'count_candidate': len(right),
    'changed_ids': sorted(k for k in left.keys() | right.keys() if left.get(k) != right.get(k))}
output = {'receipt': str(Path(sys.argv[1])), 'checks': checks,
          'state': 'PASS' if all(not c['changed_ids'] for c in checks.values()) else 'REVIEW_REQUIRED',
          'limitation': 'Mechanical layer invariants; does not prove all narrative qualifiers or source readings correct.'}
path = here / (Path(receipt['database']).parent.name + '-preserved-knowledge.json')
path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'path': str(path), 'state': output['state'], 'counts': {k: c['count_baseline'] for k, c in checks.items()}}))
