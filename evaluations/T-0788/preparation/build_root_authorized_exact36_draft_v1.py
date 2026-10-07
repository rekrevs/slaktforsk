"""One immutable source-settled T0788 draft. No CLI or SQLite mutation."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
ds = importlib.util.spec_from_file_location('d', R / 'evaluations/T-0787/preparation/build_root_authorized_exact136_draft_v1.py')
d = importlib.util.module_from_spec(ds)
ds.loader.exec_module(d)
INPUT = {'path': 'evaluations/T-0788/preparation/complete36-accepted449-reconciliation-full-old-new-supports-and-individual-incoming-v1.json', 'sha256': '84e753ac32f0b695678ee8fd1f09ce7cdf8a3a68fda9fd8373b4681736ca67c7'}
OUT = R / 'evaluations/T-0788/implementation/exact36-draft-v1'
OPID = 'T-0788/exact36-full744-source-consequences-and-bounded-adoption-v1'


def main():
    assert not OUT.exists(), 'Preserve existing draft; no overwrite or retry'
    x = h.readpin(INPUT)[1]
    source = h.readpin(x['source_union_pin'])[1]
    own = h.readpin(x['independent_whole36_readiness_pin'])[1]
    assert source['ready_for_draft'] is True and own['ready_for_exact_draft'] is True
    assert x['status'] == 'EXACT36_ACTUAL449_RECONCILIATION_PASS'
    assert x['schema_issues'] == x['current_support_head_issues'] == []
    assert x['counts']['head_issues'] == 0 and x['protected42_whole_exact'] is True
    livepath = h.checked_pin_path(x['main_before_and_after_pin'])
    h.checked_pin_path(x['baseline_pin'])
    live = h.conn(livepath)
    assert h.state(live) == {'journal_head': 449, 'pending': 0}
    assert not live.execute('select id from operation where id=?', (OPID,)).fetchone()
    changes = []
    consequences = []
    schema_checks = []
    for index, (selector, row) in enumerate(zip(source['rows'], x['rows'])):
        assert selector['index'] == row['index'] == index
        for key in ['object_id', 'source_spec_pin', 'source_row_pointer']:
            assert selector[key] == row[key]
        literal = h.pointer(h.readpin(row['source_spec_pin'])[1], row['source_row_pointer'])
        assert literal == row['full_source_disposition_row']
        api = copy.deepcopy(row['exact_full_new_API_NOT_OPERATION'])
        assert api['id'] == row['object_id']
        old = row['full_old_native']
        if old is None:
            assert api['expectedVersion'] is None and literal['full_new_API'] == api
            assert not live.execute('select id from object where id=?', (api['id'],)).fetchone()
            new_version = 1
        else:
            assert h.current(live, api['id']) == old['id']
            assert h.native(live, old['id']) == old == literal['whole_old_native']
            assert api['expectedVersion'] == old['version']
            old_api = h.api(old)
            old_api['expectedVersion'] = old['version']
            assert old_api == row['full_old_API']
            new_version = old['version'] + 1
        changes.append(api)
        edits = d.diff(row['full_old_API'], api) if old else [{'pointer': '', 'old_present': False, 'new_present': True, 'old': None, 'new': api}]
        consequences.append({**copy.deepcopy(row), 'full_new_API': api,
            'old_revision_id': old['id'] if old else None,
            'new_revision_id': api['id'] + '@' + str(new_version),
            'field_differences': edits,
            'unchanged_top_level_fields': [k for k, v in row['full_old_API'].items() if k in api and v == api[k]] if old else [],
            'ordered_array_differences_preserved_as_whole_values': True,
            'source_grade_inferred': False})
        schema_checks.append({'index': index, 'object_id': api['id'], 'whole_old_or_exact_absence': True,
                              'expectedVersion': api['expectedVersion'], 'new_version': new_version})
    ids = [a['id'] for a in changes]
    assert len(changes) == len(set(ids)) == 36
    assert sum(a['expectedVersion'] is None for a in changes) == 5
    media = copy.deepcopy(x['literal_media_registration_API_NOT_OPERATION'])
    assert media == source['media_registration_API']
    blob = R / media['storagePath']
    assert h.sha(blob) == media['sha256'] and blob.stat().st_size == media['bytes']
    assert not live.execute('select id from native_asset where id=?', (media['id'],)).fetchone()
    attached = [(a['id'], e) for a in changes for e in a.get('media', []) if e['id'] == media['id']]
    assert len(attached) == 1 and attached[0][0] == 'R-ab847c1960d02f28801419b3'
    assert len(x['all28_individual_incoming']) == len({e['native_rowid'] for e in x['all28_individual_incoming']}) == 28
    for edge in x['all28_individual_incoming']:
        assert h.pointer(h.readpin(edge['individual_source_disposition_pin'])[1], edge['source_row_pointer']) == edge['whole_individual_source_disposition']
    assert h.pin(livepath) == x['main_before_and_after_pin']
    assert h.state(live) == {'journal_head': 449, 'pending': 0}
    operation = {'id': OPID,
        'actor': 'Sol; exact individually source-settled T0788 consequences under root draft-only authorization',
        'reason': 'T-0788: full own744 source corrections, necessary current semantic copies, four bounded identity/tree assessments and mother-row adoption; historical knowledge, OWNER and life scopes retained.',
        'dependencyReviewVersion': 2, 'media': [media], 'changes': changes}
    OUT.mkdir(parents=True)
    op_pin = h.write(OUT / 'exact36-one-controlled-operation-v1.json', operation)
    table_pin = h.write(OUT / 'all36-individual-full-API-consequence-and-retain-table-v1.json', {
        'task': 'T-0788', 'source_union_pin': x['source_union_pin'], 'reconciliation_pin': INPUT,
        'rows': consequences, 'all28_individual_incoming': x['all28_individual_incoming'],
        'current_and_historical_upstream_native_pool_pointer': '/full_current_history_upstream_native',
        'pool_input_pin': INPUT, 'finite_source_relevance_retains_pin': source['finite_source_relevance_retains_pin'],
        'media_registration_API': media,
        'counts': {'targets': 36, 'revisions': 31, 'creates': 5, 'media': 1, 'incoming_unique': 28},
        'actual_runtime_requests_not_yet_generated_or_approved': True,
        'built_byte_primary_approved': False, 'built_byte_independent_approved': False,
        'stage_canonical_authorized': False, 'source_grade_inferred': False})
    member = {'operation_id': OPID, 'operation_pin': op_pin, 'target_ids': ids}
    membership_pin = h.write(OUT / 'exact36-ordered-operation-membership-v1.json', {
        'task': 'T-0788', 'operations': [member], 'operation_count': 1, 'target_count': 36,
        'revision_count': 31, 'create_count': 5, 'media_count': 1, 'source_union_pin': x['source_union_pin']})
    proof_pin = h.write(OUT / 'fresh449-exact36-draft-wholeold-absence-and-source-byte-binding-proof-v1.json', {
        'task': 'T-0788', 'helper_pin': h.pin(Path(__file__).resolve()), 'reconciliation_pin': INPUT,
        'baseline_proof_pin': x['fresh449_baseline_proof_pin'], 'baseline_pin': x['baseline_pin'],
        'main_before_pin': x['main_before_and_after_pin'], 'main_after_pin': h.pin(livepath),
        'actual_state': h.state(live), 'source_union_pin': x['source_union_pin'],
        'independent_meaning_readiness_pin': x['independent_whole36_readiness_pin'],
        'checks': schema_checks, 'all36_full_API_equal_guarded_source_inputs': True,
        'ordered_support_schema_head_checks_input_pointer': '/ordered_sequential_support_heads',
        'five_v4_vs_v3_only_explicit_body_delta': x['exact_five_v4_vs_v3_single_body_delta'],
        'protected42_whole_native_exact': True, 'acceptedT7_current136_exact': True,
        'one_literal_media_only_on_physical744': True, 'media_blob_pin': h.pin(blob),
        'CLI_or_SQLite_Wotan_mutation': False, 'usage': 'UNKNOWN pending root collector'})
    package_pin = h.write(OUT / 'exact36-one-operation-package-proposal-v1.json', {
        'task': 'T-0788', 'membership_pin': membership_pin, 'operations': [member],
        'operation_count': 1, 'target_count': 36, 'existing_revisions': 31, 'new_objects': 5, 'media_count': 1,
        'source_union_pin': x['source_union_pin'], 'independent_meaning_readiness_pin': x['independent_whole36_readiness_pin'],
        'reconciliation_pin': INPUT, 'baseline_proof_pin': x['fresh449_baseline_proof_pin'], 'baseline_pin': x['baseline_pin'],
        'consequence_table_pin': table_pin, 'mechanical_guard_pin': proof_pin,
        'built_byte_primary_approved': False, 'built_byte_independent_approved': False,
        'stage_authorized': False, 'canonical_authorized': False,
        'next_step': 'Separate primary and independent full built-package byte gates, then root stage authorization.',
        'usage': 'UNKNOWN pending root collector'})
    live.close()
    print(json.dumps({'package_pin': package_pin, 'membership_pin': membership_pin, 'operation_pin': op_pin,
                      'consequence_table_pin': table_pin, 'guard_pin': proof_pin, 'targets': 36,
                      'revisions': 31, 'creates': 5, 'media': 1, 'stage_canonical_UNRUN': True}))


if __name__ == '__main__':
    main()
