"""Bounded mechanical current442 capture, no original/grade/canonical/Wotan writes."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sqlite3
import datetime

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / 'evaluations/T-0784'
OUT = B / 'mechanical-current442-preparation-v1'
MAIN = ROOT / 'genealogy2/data/research.sqlite'
EXPECTED = '42321e363573c243597aded458e6a10d2d6cd8e4be47da02a227b149bbaed45f'
PEOPLE = ['P-0211', 'P-0003', 'P-0007']
CITATIONS = ['C-0240', 'C-0935', 'C-0008', 'C-0034', 'C-1047', 'C-0910',
             'C-0860', 'C-0720', 'C-0932', 'C-0973', 'C-0882', 'C-0883']
OWNERS = ['T-0214', 'T-0227', 'T-0379', 'T-0237']


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            digest.update(block)
    return digest.hexdigest()


helper = ROOT / 'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py'
assert sha(helper) == 'ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2'
spec = importlib.util.spec_from_file_location('readonly_native_capture', helper)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
assert sha(MAIN) == EXPECTED and not OUT.exists()
OUT.mkdir()
db = OUT / 'baseline-j442.sqlite'
c = h.conn(MAIN)
assert h.state(c) == {'journal_head': 442, 'pending': 0}
before = h.all50(c)
target = sqlite3.connect(db)
c.backup(target)
target.close()
base = h.conn(db)
assert h.all50(base) == before and h.state(base) == h.state(c)
h.write(OUT / 'all50-actual-MAIN442-before-v1.json', before)
backlog_before = (ROOT / 'wotan/backlog.json').read_bytes()
owner_prefixes = {owner: (ROOT / ('wotan/dev-log/' + owner + '.md')).read_bytes() for owner in OWNERS}

views = {}
seed_ids = set()


def add_view_ids(value):
    if isinstance(value, dict):
        if isinstance(value.get('revision_id'), str) and '@' in value['revision_id']:
            seed_ids.add(value['revision_id'].rsplit('@', 1)[0])
        for item in value.values():
            add_view_ids(item)
    elif isinstance(value, list):
        for item in value:
            add_view_ids(item)


for person in PEOPLE:
    results = {}
    for label, command in [('person-json', ['person', person, '--format', 'json']),
                           ('inspect', ['inspect', person])]:
        path = OUT / (person + '-' + label + '.json')
        results[label] = h.run_cli(command + ['--db', str(db)], path)
        add_view_ids(results[label])
    markdown = OUT / (person + '-person-full.md')
    import subprocess
    command = ['node', 'genealogy2/cli.mjs', 'person', person, '--full', '--format', 'markdown', '--db', str(db)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    markdown.write_text(result.stdout)
    (OUT / (person + '-person-full.stderr.txt')).write_text(result.stderr)
    research = OUT / (person + '-complete-current-research.json')
    h.write(research, results['person-json']['research'])
    views[person] = {'person_json_pin': h.pin(OUT / (person + '-person-json.json')),
                     'inspect_pin': h.pin(OUT / (person + '-inspect.json')),
                     'full_markdown_pin': h.pin(markdown), 'full_research_pin': h.pin(research)}
    print('Captured full person/research/inspect', person, flush=True)

citations = {}
for citation in CITATIONS:
    path = OUT / (citation + '-complete-existing-inspect.json')
    result = h.run_cli(['inspect', citation, '--db', str(db)], path)
    add_view_ids(result)
    citations[citation] = h.pin(path)

derived = {}
reused_adam = ROOT / 'evaluations/T-0781/canonical-exact17-controlled-apply-v1/pedigree-verified-P0269.json'
prior_handoff = ROOT / 'evaluations/T-0781/canonical-exact17-controlled-apply-v1/complete-exact17-controlled-canonical-actual442-zero-pending-handoff-v1.json'
old = json.loads(prior_handoff.read_text())
assert old['MAIN_pin'] == {'path': 'genealogy2/data/research.sqlite', 'sha256': EXPECTED}
assert h.pin(reused_adam) in old['validator_pins']
derived['Adam_verified'] = {'pin': h.pin(reused_adam), 'reuse_basis': h.pin(prior_handoff),
                            'exact_same_current_MAIN_hash': True, 'mode': 'default verified'}
for label, args in [('Axel_verified', ['pedigree', 'P-0270']),
                    ('Adam_typed', ['pedigree', 'P-0269', '--mode', 'typed']),
                    ('Axel_typed', ['pedigree', 'P-0270', '--mode', 'typed']),
                    ('full_inventory', ['inventory', '--full']), ('status', ['status'])]:
    path = OUT / (label + '.json')
    h.run_cli(args + ['--db', str(db)], path)
    derived[label] = {'pin': h.pin(path)}

# Complete own person/contract/research fields are enumerated through the domain
# reader, not a title/name regex. Record metadata remains routing, never approval.
direct_ids = sorted(seed_ids)
pool, units, documents, media, histories = {}, {}, {}, {}, {}


def add(rid):
    if rid in pool:
        return
    n = h.native(base, rid)
    pool[rid] = n
    for origin in n['origins']:
        unit = dict(base.execute('select * from unit where id=?', (origin['unit_id'],)).fetchone())
        units[unit['id']] = unit
        document = dict(base.execute('select * from document where path=?', (unit['document_path'],)).fetchone())
        documents[document['path']] = document
    for edge in n['evidence']:
        add(edge['basis_revision_id'])
        basis_oid = edge['basis_revision_id'].rsplit('@', 1)[0]
        add(h.current(base, basis_oid))
    for edge in n.get('assets', []):
        row = dict(base.execute('select * from asset where path=?', (edge['asset_path'],)).fetchone())
        media['asset:' + row['path']] = row
    for edge in n.get('media', []):
        row = dict(base.execute('select * from native_asset where id=?', (edge['asset_id'],)).fetchone())
        media['native:' + row['id']] = row


for oid in direct_ids:
    add(h.current(base, oid))

# Include complete current TR/audits for each routed record and complete history
# for the bounded own/current/support objects. No original image is opened.
for rid, n in list(pool.items()):
    if n['kind'] == 'record':
        for table, field in [('transcription', 'record_id'), ('assessment', 'subject_id')]:
            for row in base.execute('select r.id from current_revision r join ' + table + ' x on x.revision_id=r.id where x.' + field + '=? order by r.object_id', (n['object_id'],)):
                add(row[0])
for oid in sorted({n['object_id'] for n in pool.values()}):
    hs = [r[0] for r in base.execute('select id from revision where object_id=? order by version', (oid,))]
    histories[oid] = hs
    for rid in hs:
        add(rid)

protected_old = ROOT / 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json'
protected42 = json.loads(protected_old.read_text())['objects']
for rid, n in protected42.items():
    assert h.current(base, n['object_id']) == rid and h.native(base, rid) == n
    add(rid)
owner_current = {}
for row in base.execute("select id from current_revision where evidence_status='OWNER_CONFIRMED' order by object_id"):
    add(row[0]); owner_current[row[0]] = pool[row[0]]
selected_relations = {rid: n for rid, n in pool.items() if n['kind'] == 'relation' and
                      (n['data']['from_person'] in PEOPLE or n['data']['to_person'] in PEOPLE)}
selected_reviews = {rid: n for rid, n in pool.items() if n['kind'] == 'assessment' and
                    n['data']['subject_id'] in PEOPLE and
                    (n['data']['criteria'].startswith('legacy_person_contract/') or
                     n['data']['criteria'] in {'legacy_review_header', 'identity_review/1', 'tree_effect/1', 'life_picture_review/1',
                                              'Befintlig person-research/v1; ursprungliga datum och kriterier i body'})}
nativepin = h.write(OUT / 'complete-three-current-history-upstream-native-dictionary-v1.json',
                    {'objects': pool, 'origin_units': units, 'documents': documents, 'media_metadata': media,
                     'native_array_order': 'All evidence/origins/assets/media ORDER BY rowid; raw embedded JSON strings untouched',
                     'source_grade': 'NONE_MECHANICAL_CAPTURE_ONLY'})
historypin = h.write(OUT / 'bounded-current-objects-and-complete-ordered-histories-v1.json', histories)
protectedpin = h.write(OUT / 'protected-OWNER-relations-bases-legacy-review-and-life-history-v1.json',
                       {'prior_protected42_input_pin': h.pin(protected_old), 'prior42_full_current_equality': True,
                        'prior_protected42_objects': protected42, 'all_current_exact_OWNER_CONFIRMED': owner_current,
                        'selected_full_relations_and_histories': selected_relations,
                        'selected_complete_legacy_PK_and_axis_assessments': selected_reviews,
                        'no_automatic_legacy_conversion': True, 'dictionary_pin': nativepin})

per_person = {}
PKS = ['01', '02', '05', '07', '09', '11', '12']
for person in PEOPLE:
    own = views[person]
    p = json.loads((ROOT / own['person_json_pin']['path']).read_text())
    required = {}
    for pk in PKS:
        found = [r for r in p['research']['requirements'] if r['criteria'] == 'legacy_person_contract/PK-' + pk]
        assert len(found) == 1, (person, pk, [(r['object_id'], r['criteria']) for r in p['research']['requirements']])
        r = found[0];n = pool[r['revision_id']]
        required['PK-' + pk] = {'revision_id': r['revision_id'], 'object_id': r['object_id'],
                                 'full_native_pointer': '/objects/' + r['revision_id'].replace('~', '~0').replace('/', '~1'),
                                 'full_view_reading_pointer': '/research/requirements/' + str(p['research']['requirements'].index(r)),
                                 'native_payload': n, 'source_owned_disposition': 'PENDING'}
    per_person[person] = {**own, 'seven_PK_full_current': required,
                          'complete_own_assessments': p['assessments'], 'complete_own_relations': p['relations'],
                          'complete_current_identity_arguments': p['research']['reviews'],
                          'source_grade': 'PENDING_ASTRA_OWN_CURRENT_FIRST_READING'}
pkpin = h.write(OUT / 'all21-current-PK-full-native-and-three-assessment-relation-inputs-v1.json', per_person)

# Exact incoming caller inventory includes historical revisions, separately
# identifies actual current heads and preserves all edge fields/rowid order.
assessment_rids = {n['id'] for n in selected_reviews.values() if not n['data']['criteria'].startswith('legacy_person_contract/')}
caller_rows = []
seen_edges = set()
frontier = set(assessment_rids)
while frontier:
    next_frontier = set()
    for rid in sorted(frontier):
        for edge in base.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid', (rid,)):
            e = dict(edge)
            if e['native_rowid'] in seen_edges:
                continue
            seen_edges.add(e['native_rowid']); caller_rid = e['revision_id']; add(caller_rid)
            add(h.current(base, pool[caller_rid]['object_id']))
            caller_rows.append({'basis_revision_id': rid, 'exact_edge': e, 'caller_revision_id': caller_rid,
                                'caller_is_current': h.current(base, pool[caller_rid]['object_id']) == caller_rid,
                                'caller_current_revision_id': h.current(base, pool[caller_rid]['object_id']),
                                'individual_source_disposition': 'PENDING_NO_AUTO_REBIND'})
            next_frontier.add(caller_rid)
    frontier = next_frontier
callerpin = h.write(OUT / 'complete-assessment-axis-current-and-historical-incoming-caller-edge-inventory-v1.json',
                    {'assessment_seed_revisions': sorted(assessment_rids), 'exact_edges': caller_rows,
                     'source_or_evidence_effect_grade': 'NONE_ROUTING_ONLY'})
# Caller additions must be retained as full payloads without mutating the earlier capture.
additional = {rid: n for rid, n in pool.items() if rid not in json.loads((ROOT / nativepin['path']).read_text())['objects']}
additionpin = h.write(OUT / 'incoming-caller-additive-full-native-context-v1.json',
                      {'objects': additional, 'origin_units': units, 'documents': documents, 'media_metadata': media})
owners = []
for owner, raw in owner_prefixes.items():
    source = ROOT / ('wotan/dev-log/' + owner + '.md')
    capture = OUT / (owner + '-whole-current-owner-log.md')
    capture.write_bytes(raw)
    owners.append({'task_id': owner, 'actual_log_pin': h.pin(source), 'full_capture_pin': h.pin(capture),
                   'prefix_bytes': len(raw), 'backlog_entry': next(t for t in json.loads(backlog_before)['tasks'] if t['id'] == owner)})
ownerpin = h.write(OUT / 'four-existing-owner-full-prefix-and-current-entry-lock-v1.json', owners)

for name, example_path in [('working', ROOT / 'genealogy2/docs/working.md'),
                            ('review-reader', ROOT / 'genealogy2/lib/review.mjs'),
                            ('synthetic-test-examples', ROOT / 'genealogy2/test/review.test.mjs'),
                            ('person-contract', ROOT / 'docs/research/person-contract.md')]:
    assert example_path.exists()
schema = h.write(OUT / 'controlled-operation-and-source-owned-consequence-skeleton-NOT-A-CANDIDATE-v1.json',
                 {'status': 'UNRUN_SOURCE_DECISIONS_REQUIRED', 'criteria': {'identity_review/1': ['passed', 'failed'],
                  'tree_effect/1': ['supporting', 'waiting', 'non_supporting']},
                  'native_assessment_schema': {'id': 'UNSET_ASTRA_APPROVED_STABLE_ID', 'kind': 'assessment',
                    'expectedVersion': 'UNSET_ACTUAL_ABSENCE_OR_CURRENT_HEAD',
                    'data': {'subject_id': 'EXACT_ONE_OF_LOCKED_THREE', 'criteria': 'EXACT_AXIS', 'outcome': 'UNSET_ASTRA', 'body': 'UNSET_FULL_SOURCE_APPROVED_BODY'},
                    'origins': 'UNSET_EXACT_SETTLED_ORDERED_NATIVE_ORIGINS', 'evidence': 'UNSET_SOURCE_APPROVED_EXACT_CURRENT_BASIS_VERSION_ORDER',
                    'disposition': 'UNSET_ASTRA', 'evidenceStatus': 'UNSET_ASTRA', 'rationale': 'UNSET_ASTRA', 'caveat': 'UNSET_ASTRA'},
                  'operation_policy': {'dependencyReviewVersion': 2, 'changes': 'ONLY_AFTER_INDIVIDUAL_ASTRA_SPEC', 'resolve': 'ONLY_ACTUAL_INDIVIDUAL_APPROVED_REQUESTS'},
                  'per_person_source_owned_rows': [{'person': person, 'PK': pk, 'current_input_pointer': '/'+person+'/seven_PK_full_current/PK-'+pk,
                    'source_disposition': 'PENDING', 'sufficient_reuse_or_remaining_scope': 'PENDING_ASTRA',
                    'old_new_full_field_decision': 'PENDING', 'incoming_rebind_or_retain': 'PENDING'} for person in PEOPLE for pk in PKS],
                  'schema_and_examples_pins': [h.pin(p) for p in [ROOT/'genealogy2/docs/working.md',ROOT/'genealogy2/lib/review.mjs',ROOT/'genealogy2/test/review.test.mjs',ROOT/'docs/research/person-contract.md']],
                  'legacy_full_contract_and_life': 'PRESERVE_SEPARATELY_NO_AUTO_CONVERSION', 'actual_draft_operations': 0})
assert h.all50(c) == before and sha(MAIN) == EXPECTED and h.state(c) == {'journal_head': 442, 'pending': 0}
assert h.all50(base) == before
assert (ROOT / 'wotan/backlog.json').read_bytes() == backlog_before
for owner, raw in owner_prefixes.items():
    assert (ROOT / ('wotan/dev-log/' + owner + '.md')).read_bytes() == raw
c.close();base.close()
baselinepin = h.pin(db)
baselineproof = h.write(OUT / 'fresh442-physical-backup-logical-all50-and-live-unchanged-proof-v1.json',
                        {'MAIN_pin': h.pin(MAIN), 'baseline_clone_pin': baselinepin, 'backup_method': 'Readonly SQLite source backup to absent owned clone',
                         'all50_MAIN_before_and_after_and_clone_schema_rows_BLOB_JSON_arrays_equal': True,
                         'all50_pin': h.pin(OUT / 'all50-actual-MAIN442-before-v1.json'),
                         'actual_state': {'journal_head': 442, 'pending': 0}, 'native_writes': 0, 'Wotan_writes': 0,
                         'protected42_exact': True, 'actual_model_usage': 'UNKNOWN_UNTIL_ROOT_COLLECTOR_NOT_ZERO'})
result = h.write(OUT / 'complete-three-person-current442-preparation-index-v1.json',
                 {'task': 'T-0784', 'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'scope_person_ids': PEOPLE,
                  'MAIN_pin': h.pin(MAIN), 'baseline_clone_pin': baselinepin, 'baseline_proof_pin': baselineproof,
                  'full_person_views': views, 'before_derived_views': derived, 'existing_citation_full_inspections': citations,
                  'complete_native_dictionary_pin': nativepin, 'complete_history_pin': historypin,
                  'all21_PK_and_three_current_argument_inputs_pin': pkpin, 'protected_OWNER_relation_review_pin': protectedpin,
                  'incoming_caller_edge_inventory_pin': callerpin, 'additive_caller_payload_pin': additionpin,
                  'four_owner_log_scope_lock_pin': ownerpin, 'operation_schema_and_source_owned_skeleton_pin': schema,
                  'full_native_revision_count': len(pool), 'native_input_capture_is_not_source_grade': True,
                  'current_first_Astra_reads_before_candidate_exposure_required': True,
                  'new_originals_opened': 0, 'candidate_grades_or_operations': 0, 'canonical_or_stage_apply': False,
                  'remaining': 'Exact accepted-source receipt locators additive if required; Astra current/source individual21 PK and3axis decisions; root release/settled mechanics only.'})
print(json.dumps({'preparation_index_pin': result, 'baseline_proof_pin': baselineproof, 'objects': len(pool), 'MAIN_unchanged': True}, indent=2))
