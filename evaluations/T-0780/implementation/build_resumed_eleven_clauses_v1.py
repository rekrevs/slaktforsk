"""Build only Astra's exact eleven settled body clauses; no apply or grading."""
import copy
import datetime
import hashlib
import json
import sqlite3
import time
from pathlib import Path

START = time.time()
B = Path('evaluations/T-0780')
W = B / 'implementation/resumed-eleven-clause-queue-v1'
SOURCE = B / 'source-review/resumed-eleven-reviewer-clause-decisions-v1.json'
SOURCE_SHA = 'a7ed63ff0bab331568bdd30efc124f740343354c63c8a1aeef40a852772b5280'
PRIOR = B / 'implementation/C0561-P0437-network-date-structured-copy-queue-v1/concrete-current124-partial-sequence-and-constraint-proposal-v1.json'

def load(p):
    return json.loads(Path(p).read_text())

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def canon(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def save(name, obj):
    p = W / name
    assert not p.exists()
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    return {'path': str(p), 'sha256': sha(p)}

assert sha(SOURCE) == SOURCE_SHA
assert sha(PRIOR) == 'cc529e35a0420b575a26183653f366834bd1490dc14c2cc053bc28a8d42485f5'
d = load(SOURCE)
prior = load(PRIOR)
assert len(d['objects']) == 11
c = sqlite3.connect('file:' + str((B / 'preparation/baseline-j281.sqlite').resolve()) + '?mode=ro', uri=True)
c.row_factory = sqlite3.Row

def native(rid):
    row = c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?', (rid,)).fetchone()
    assert row is not None, rid
    n = dict(row)
    n['data'] = dict(c.execute('select * from ' + n['kind'] + ' where revision_id=?', (rid,)).fetchone())
    n['origins'] = [dict(z) for z in c.execute('select * from origin where revision_id=?', (rid,))]
    n['evidence'] = [dict(z) for z in c.execute('select * from dependency where revision_id=?', (rid,))]
    if n['kind'] == 'record':
        n['assets'] = [dict(z) for z in c.execute('select * from record_asset where revision_id=?', (rid,))]
        n['media'] = [dict(z) for z in c.execute('select * from record_media where revision_id=?', (rid,))]
    return n

def api(n):
    data = {k: v for k, v in n['data'].items() if k != 'revision_id'}
    for k, v in data.items():
        if k.endswith('_json') and isinstance(v, str):
            data[k] = json.loads(v)
    return {'id': n['object_id'], 'kind': n['kind'], 'expectedVersion': n['version'], 'data': data,
            'origins': [{'unit': z['unit_id'], 'coverage': z['coverage'], 'note': z['note']} for z in n['origins']],
            'evidence': [{'object': z['basis_revision_id'].rsplit('@', 1)[0], 'version': int(z['basis_revision_id'].rsplit('@', 1)[1]), 'role': z['role'], 'note': z['note']} for z in n['evidence']],
            'disposition': n['disposition'], 'evidenceStatus': n['evidence_status'], 'rationale': n['rationale'], 'caveat': n['caveat']}

operations = {}
new_revisions = []
proofs = []
field_table = []
changed = {}
originals = {}
for item in d['objects']:
    oid = item['object_id']
    assert oid not in changed
    n = native(oid + '@' + str(item['version']))
    assert not c.execute('select 1 from revision where object_id=? and version>?', (oid, item['version'])).fetchone()
    f = item['full_current']
    for key, value in n.items():
        if key in ('origins', 'evidence'):
            assert sorted(map(canon, value)) == sorted(map(canon, f[key])), (oid, key)
        else:
            assert value == f[key], (oid, key)
    originals[oid] = f
    matches = [(r, x) for r in prior['sequence'] for x in load(r['path'])['changes'] if x['id'] == oid]
    if item['prior_candidate'] is not None:
        assert len(matches) == 1
        member, payload = matches[0]
        assert member['path'] == item['prior_operation']['path']
        assert sha(member['path']) == item['prior_operation']['sha256'] == member['sha256']
        assert payload == item['prior_candidate']
        if member['path'] not in operations:
            operations[member['path']] = copy.deepcopy(load(member['path']))
        old = copy.deepcopy(payload)
        dest = next(x for x in operations[member['path']]['changes'] if x['id'] == oid)
    else:
        assert not matches and item['disposition'] == 'revise_previous_retain'
        old = api(f)
        dest = copy.deepcopy(old)
        new_revisions.append(dest)
    assert old['expectedVersion'] == item['version']
    assert len(item['edits']) == 1 and item['edits'][0]['field'] == 'data.body'
    edit = item['edits'][0]
    assert dest['data']['body'] == edit['old'], oid
    generated = edit['old']
    for repl in item['replacements']:
        assert generated.count(repl['old']) == 1, (oid, repl['old'], generated.count(repl['old']))
        generated = generated.replace(repl['old'], repl['new'])
    assert generated == edit['new'], oid
    dest['data']['body'] = edit['new']
    restored = copy.deepcopy(dest)
    restored['data']['body'] = old['data']['body']
    assert restored == old
    changed[oid] = copy.deepcopy(dest)
    proofs.append({'target': oid, 'source_disposition': item['disposition'], 'original_full_native': f,
                   'old_API_payload': old, 'new_API_payload': copy.deepcopy(dest),
                   'only_changed_field': 'data.body', 'all_other_fields_arrays_metadata_origins_evidence_exact': True,
                   'exact_replacements': item['replacements'], 'source_rationale': item['rationale']})
    for k, v in old.items():
        if k == 'data':
            for field, val in v.items():
                field_table.append({'target': oid, 'native_version': item['version'], 'field': 'data.' + field,
                                    'old': val, 'new': dest['data'][field], 'disposition': 'revise' if field == 'body' else 'retain',
                                    'rationale': item['rationale'], 'support': dest['evidence'], 'source_sha256': SOURCE_SHA})
        else:
            field_table.append({'target': oid, 'native_version': item['version'], 'field': k, 'old': v, 'new': dest[k],
                                'disposition': 'retain', 'rationale': item['rationale'], 'source_sha256': SOURCE_SHA})

assert len(new_revisions) == 3 and len(operations) == 3
assert not W.exists()
W.mkdir()
supersessions = {}
unchanged_other_payloads = []
for number, (path, op) in enumerate(operations.items(), 1):
    oldop = load(path)
    for x, y in zip(oldop['changes'], op['changes']):
        assert x['id'] == y['id']
        if x['id'] not in changed:
            assert x == y
            unchanged_other_payloads.append(x)
    op['id'] += '/resumed-eleven-clause-v1'
    op['reason'] += '; exact settled Astra eleven-clause supersession ' + SOURCE_SHA + '; same native expectedVersions, all other payload fields unchanged.'
    supersessions[path] = save(f'{number:02}-superseding-operation-v1.json', op)
newop = {'id': 'T-0780/resumed-eleven-three-former-retain-path-revisions-v1',
         'actor': 'Codex Sol bounded implementation of settled Astra inputs',
         'reason': 'T-0780 AC3 exact settled Astra body-only corrections ' + SOURCE_SHA + '; no source or review upgrades.',
         'dependencyReviewVersion': 2, 'changes': new_revisions}
newpin = save('04-three-former-retain-path-revisions-operation-v1.json', newop)
seq = copy.deepcopy(prior['sequence'])
for i, row in enumerate(seq):
    if row['path'] in supersessions:
        seq[i] = copy.deepcopy(supersessions[row['path']])
seq.append(newpin)
heads = {z['object_id']: z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')}
updates = {x['id']: {'index': i + 1, 'expectedVersion': x['expectedVersion'], 'newVersion': (x['expectedVersion'] or 0) + 1}
           for i, row in enumerate(seq) for x in load(row['path'])['changes']}
targets = {}
violations = []
constraints = []
for i, row in enumerate(seq):
    assert sha(row['path']) == row['sha256']
    op = load(row['path'])
    row.update(index=i + 1, operation_id=op['id'], targets=[], changes=len(op['changes']))
    for x in op['changes']:
        assert x['id'] not in targets
        assert heads.get(x['id']) == x['expectedVersion'], x['id']
        targets[x['id']] = {'payload': x, 'operation_pin': {'path': row['path'], 'sha256': row['sha256']}}
        row['targets'].append({'id': x['id'], 'expectedVersion': x['expectedVersion'], 'payload_sha256': hashlib.sha256(canon(x).encode()).hexdigest()})
        for edge in x['evidence']:
            assert set(edge) == {'object', 'version', 'role', 'note'}
            if edge['object'] in updates:
                constraints.append({'target': x['id'], 'operation': op['id'], 'index': i + 1, 'edge': edge, 'basis_update': updates[edge['object']]})
            if heads.get(edge['object']) != edge['version'] and not any(q['id'] == edge['object'] and (q['expectedVersion'] or 0) + 1 == edge['version'] for q in op['changes']):
                violations.append({'target': x['id'], 'edge': edge, 'proposed_current_head': heads.get(edge['object'])})
    for x in op['changes']:
        heads[x['id']] = (x['expectedVersion'] or 0) + 1
assert len(seq) == 125 and len(targets) == 828
assert violations == prior['static_head_order_violations'] == []
fan = []
full = {}
bases = {}
for oid, payload in changed.items():
    for r in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)', (oid,)):
        edge = dict(r)
        fan.append({'changed_target': oid, 'edge': edge, 'Astra_individual_disposition': None,
                    'candidate_consumer': targets.get(edge['object_id'])})
        full[edge['revision_id']] = native(edge['revision_id'])
    for e in payload['evidence']:
        rid = e['object'] + '@' + str(e['version'])
        if c.execute('select 1 from revision where id=?', (rid,)).fetchone():
            bases[rid] = native(rid)
        else:
            assert e['object'] in targets
            bases[rid] = {'explicit_future_candidate': targets[e['object']]}
proofpin = save('eleven-full-payload-reconstruction-proof-v1.json', {'source_pin': {'path': str(SOURCE), 'sha256': SOURCE_SHA}, 'proofs': proofs,
    'unchanged_other_full_candidate_payloads': unchanged_other_payloads, 'no_native_version_or_evidence_rebind': True,
    'supersessions': [{'prior_path': p, 'prior_sha256': sha(p), 'new_pin': z} for p, z in supersessions.items()]})
tablepin = save('individual-full-field-consequence-table-v1.json', {'entries': field_table, 'source_pin': {'path': str(SOURCE), 'sha256': SOURCE_SHA}})
inputpin = save('full-current-history-incoming-and-support-input-v1.json', {'eleven_full_current': originals, 'fanouts': fan,
    'incoming_full_native_objects': full, 'full_declared_support_bases': bases, 'candidate_overlaps': proofs,
    'individual_incoming_grading_pending': True, 'no_automatic_rebind_or_resolution': True})
membershippin = save('current125-candidate-membership-inventory-v1.json', {'prior_proposal_pin': {'path': str(PRIOR), 'sha256': sha(PRIOR)},
    'candidate_members': seq, 'unique_targets': len(targets), 'member_count': len(seq), 'new_targets': 3, 'duplicate_targets': 0, 'global_source_approval': False})
proposalpin = save('concrete-current125-partial-sequence-and-constraint-proposal-v1.json', {'sequence': seq, 'members': len(seq), 'unique_targets': len(targets),
    'constraints': constraints, 'static_head_order_violations': violations, 'membership_pin': membershippin,
    'fresh_primary_hash_binding_required': True, 'no_native_PASS_or_stage': True})
receipt = {'task': 'T-0780', 'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_pin': {'path': str(SOURCE), 'sha256': SOURCE_SHA}, 'candidate_modules': list(supersessions.values()) + [newpin],
    'proof_pin': proofpin, 'field_table_pin': tablepin, 'input_pin': inputpin, 'membership_pin': membershippin, 'proposal_pin': proposalpin,
    'body_clauses_revised': 11, 'amended_existing_candidates': 8, 'former_retains_revised': 3,
    'other_whole_candidate_payloads_retained_exact': len(unchanged_other_payloads), 'full_field_entries': len(field_table),
    'all_history_incoming_edges': len(fan), 'current_incoming_edges': sum(z['edge']['is_current'] for z in fan),
    'incoming_distinct_fullobjects': len(full), 'support_fullobjects': len(bases), 'static_head_order_violations': violations,
    'protected_grade_outcome_fields_unchanged': True, 'arrays_evidence_origins_metadata_order_preserved': True,
    'canonical_apply_stage_probe': 'UNRUN', 'independent_actual_and_global_source_binding': 'PENDING',
    'elapsed_build_seconds': time.time() - START, 'failed_attempts': [], 'actual_model_usage': 'Root collects after final; not observable here.'}
receiptpin = save('bounded-eleven-clause-production-receipt-v1.json', receipt)
print(json.dumps({'receipt': receiptpin, 'members': len(seq), 'targets': len(targets), 'current_incoming_edges': receipt['current_incoming_edges'],
    'all_history_incoming_edges': len(fan), 'whole_payload_retains': len(unchanged_other_payloads), 'full_field_entries': len(field_table),
    'membership': membershippin, 'proposal': proposalpin, 'input': inputpin}, ensure_ascii=False, indent=2))
