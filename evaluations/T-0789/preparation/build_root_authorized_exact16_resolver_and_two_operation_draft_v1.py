"""Exact dual-approved literal16 resolver draft; never apply or infer a retain."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
s = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--authorization', type=Path, required=True)
    p.add_argument('--authorization-sha256', required=True)
    args = p.parse_args()
    ap = args.authorization.resolve()
    assert ap.is_relative_to(R) and h.sha(ap) == args.authorization_sha256
    AUTH = h.pin(ap)
    auth = h.readpin(AUTH)[1]
    assert auth['authorization'] == 'BUILD_EXACT16_LITERAL_RESOLVER_AND_TWO_OPERATION_DRAFT_ONLY'
    assert auth['helper_pin'] == h.pin(Path(__file__).resolve())
    HANDOFF = auth['actual_native_handoff_pin']
    OUT = (R / auth['output_directory']).resolve()
    OPID = auth['resolution_operation_id']
    assert OUT.is_relative_to(R / 'evaluations/T-0789/implementation') and not OUT.exists()

    assert auth['root_authorized'] is True and auth['runtime_authorized'] is auth['canonical_authorized'] is False
    primary = h.readpin(auth['primary_actual_instruction_gate_pin'])[1]
    own = h.readpin(auth['independent_actual_instruction_gate_pin'])[1]
    assert h.pointer(primary, auth['primary_ready_pointer']) is True and h.pointer(own, auth['independent_ready_pointer']) is True
    source_rows = h.pointer(primary, auth['primary_instruction_rows_pointer'])
    own_rows = h.pointer(own, auth['independent_instruction_rows_pointer'])
    literals = [h.pointer(row, auth['primary_resolution_instruction_pointer']) for row in source_rows]
    assert literals == [h.pointer(row, auth['independent_resolution_instruction_pointer']) for row in own_rows]
    native_fields = h.pointer(primary, auth['source_native_request_pointer'])
    assert native_fields == {'changes': [], 'dependencyReviewVersion': 2, 'resolve': literals}
    assert len(literals) == len(source_rows) == len(own_rows) == 16
    ids = [v['request'] for v in literals]
    assert len(set(ids)) == 16 and all(set(v) == {'request', 'rationale'} and v['rationale'].strip() for v in literals)
    requests = h.readpin(auth['actual_request_pin'])[1]
    stage = h.conn(h.checked_pin_path(auth['pre_resolution_stage_DB_pin']))
    live = h.conn(h.checked_pin_path(auth['main_pin']))
    assert h.state(stage) == primary['actual_state'] == own['actual_state'] == {'journal_head': 453, 'pending': 16}
    assert h.state(live) == {'journal_head': 452, 'pending': 0}
    assert not stage.execute('select id from operation where id=?', (OPID,)).fetchone()
    pending = [dict(v) for v in stage.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')]
    assert pending == [v['actual_request'] for v in requests['requests']]
    assert pending == [h.pointer(row, auth['primary_actual_request_pointer']) for row in source_rows]
    assert pending == [h.pointer(row, auth['independent_actual_request_pointer']) for row in own_rows]
    assert [v['id'] for v in pending] == ids
    handoff = h.readpin(HANDOFF)[1]
    assert handoff['stage_DB_pin'] == auth['pre_resolution_stage_DB_pin'] and handoff['individual_request_pin'] == auth['actual_request_pin']
    native_pin = handoff['actual_native_context_pin']
    native = h.readpin(native_pin)[1]['objects']
    table_rows = []
    for index, (q, source_row, own_row, literal) in enumerate(zip(pending, source_rows, own_rows, literals)):
        rid = source_row['retained_current_revision_id']
        assert rid == own_row['retained_current_revision_id']
        current = h.native(stage, rid)
        assert h.current(stage, current['object_id']) == rid and current == native[rid]
        context = requests['requests'][index]
        for key in ['affected_exact_revision_id', 'affected_current_revision_id', 'changed_exact_revision_id', 'changed_current_revision_id']:
            assert h.native(stage, context[key]) == native[context[key]]
        table_rows.append({'index': index, 'actual_request': q, 'resolution_instruction': literal,
                           'retained_current_revision_id': rid, 'whole_retained_current_native': current,
                           'actual_context': context, 'actual_native_context_pin': native_pin,
                           'primary_instruction_gate_pin': auth['primary_actual_instruction_gate_pin'], 'primary_row_pointer': auth['primary_instruction_rows_pointer'] + '/' + str(index),
                           'whole_primary_disposition': source_row,
                           'independent_instruction_gate_pin': auth['independent_actual_instruction_gate_pin'], 'independent_row_pointer': auth['independent_instruction_rows_pointer'] + '/' + str(index),
                           'whole_independent_disposition': own_row, 'literal_full_equality': True, 'source_grade_inferred': False})
    prefix_pin = auth['native_prefix_package_pin']
    prefix = h.readpin(prefix_pin)[1]
    membership = h.readpin(prefix['membership_pin'])[1]
    assert prefix['operations'] == membership['operations'] and len(prefix['operations']) == 1
    assert membership['target_count'] == 21 and membership['revision_count'] == 9 and membership['create_count'] == 12
    for member in prefix['operations']:
        operation = h.readpin(member['operation_pin'])[1]
        assert json.loads(stage.execute('select request_json from operation_payload where operation_id=?', (member['operation_id'],)).fetchone()[0]) == operation
    protected_pin = h.pin(R / 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json')
    protected = h.readpin(protected_pin)[1]['objects']
    assert len(protected) == 42
    for rid, value in protected.items():
        assert h.current(stage, value['object_id']) == rid and h.native(stage, rid) == value
        assert h.current(live, value['object_id']) == rid and h.native(live, rid) == value
    for pin in auth['review_pins']:
        h.checked_pin_path(pin)
    h.checked_pin_path(auth['pre_resolution_stage_DB_pin'])
    h.checked_pin_path(auth['main_pin'])
    assert h.sha(ap) == args.authorization_sha256
    OUT.mkdir(parents=True)
    operation = {'id': OPID, 'actor': 'Sol; exactly dual-approved actual453 individual source instructions under root draft-only authority',
                 'reason': 'T-0789: resolve only the 16 actual requests with each separately source-approved literal rationale and retained current scope; no native revision or rebind.',
                 **copy.deepcopy(native_fields)}
    op_pin = h.write(OUT / 'exact16-resolution-only-operation-v1.json', operation)
    format_pin = h.write(OUT / 'source-authorized-native-resolve-array-format-wrapper-v1.json', {
        'task': 'T-0789', 'original_source_format_authority_pin': auth['native_format_authority_pin'],
        'original_source_pointer': auth['source_native_request_pointer'], 'native_request_fields': native_fields,
        'explicit_source_subset_equal': True, 'no_source_format_or_literal_change': True})
    table_pin = h.write(OUT / 'all16-individual-full-current-literal-source-and-independent-resolution-consequence-table-v1.json', {
        'task': 'T-0789', 'rows': table_rows, 'actual_request_pin': auth['actual_request_pin'],
        'native21_consequence_table_pin': prefix['consequence_table_pin'], 'root_draft_authorization_pin': AUTH,
        'individual_request_and_literal_order_exact': True, 'native_changes': [], 'inferred_retains_or_rebinds': False})
    guard_pin = h.write(OUT / 'fresh45316-and-main452-entire-pending-literal-current-prefix-protected-guard-v1.json', {
        'task': 'T-0789', 'helper_pin': h.pin(Path(__file__).resolve()), 'root_draft_authorization_pin': AUTH,
        'stage_DB_pin': auth['pre_resolution_stage_DB_pin'], 'actual_stage_state': h.state(stage),
        'main_pin': auth['main_pin'], 'actual_main_state': h.state(live), 'actual_pending': pending,
        'ordered_request_ids': ids, 'dual_full_request_and_literal_equality': True,
        'all16_whole_current_native_equal_actual_input': True, 'native_prefix_one_operation_whole_exact': True,
        'protected42_pin': protected_pin, 'protected42_whole_current_exact': True,
        'CLI_SQLite_Wotan_mutation': False, 'usage': 'UNKNOWN pending root collector'})
    resolver_member = {'operation_id': OPID, 'operation_pin': op_pin, 'ordered_request_ids': ids}
    members = copy.deepcopy(prefix['operations']) + [resolver_member]
    member_pin = h.write(OUT / 'exact21-plus16-two-ordered-operation-membership-v1.json', {
        'task': 'T-0789', 'operations': members, 'operation_count': 2, 'target_count': 21, 'revision_count': 9,
        'create_count': 12, 'media_count': 2, 'resolution_count': 16, 'unchanged_native_prefix_membership_pin': prefix['membership_pin']})
    proposal_pin = h.write(OUT / 'exact21-plus16-two-operation-package-proposal-v1.json', {
        'task': 'T-0789', 'membership_pin': member_pin, 'operations': members, 'operation_count': 2, 'target_count': 21,
        'existing_revisions': 9, 'new_objects': 12, 'media_count': 2, 'resolution_count': 16,
        'native_prefix_package_pin': prefix_pin, 'primary_actual_instruction_gate_pin': auth['primary_actual_instruction_gate_pin'],
        'independent_actual_instruction_gate_pin': auth['independent_actual_instruction_gate_pin'],
        'native_format_authority_pin': format_pin, 'original_source_format_authority_pin': auth['native_format_authority_pin'],
        'individual_resolution_consequence_table_pin': table_pin, 'resolution_guard_pin': guard_pin,
        'pre_resolution_actual_handoff_pin': HANDOFF, 'pre_resolution_stage_DB_pin': auth['pre_resolution_stage_DB_pin'],
        'built_byte_primary_approved': False, 'built_byte_independent_approved': False,
        'same_stage_resolution_authorized': False, 'canonical_authorized': False,
        'next': 'Exact full-built source and independent byte gates, then separate root runtime authorization.',
        'usage': 'UNKNOWN pending root collector'})
    stage.close()
    live.close()
    h.checked_pin_path(auth['pre_resolution_stage_DB_pin'])
    h.checked_pin_path(auth['main_pin'])
    print(json.dumps({'proposal_pin': proposal_pin, 'membership_pin': member_pin, 'resolution_operation_pin': op_pin,
                      'table_pin': table_pin, 'guard_pin': guard_pin, 'format_pin': format_pin, 'runtime_UNRUN': True}))


if __name__ == '__main__':
    main()
