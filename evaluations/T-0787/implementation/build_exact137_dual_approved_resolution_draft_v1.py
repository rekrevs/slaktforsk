"""Draft-only exact137 individual instructions. No CLI/runtime/native/Wotan mutation."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
S = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(S)
S.loader.exec_module(h)
OUT = R / 'evaluations/T-0787/implementation/exact136-plus137-resolutions-draft-v1'
P = {'path': 'evaluations/T-0787/source-review/actual137-complete-primary-comparison-and-exact-resolution-instruction-gate-v1.json', 'sha256': 'a7707b9061dd0eee237cbdc6a464c9805a4f4e8ac46dc321ce0d6cd799c8f0fa'}
I = {'path': 'evaluations/T-0787/independent-review/actual137-complete-independent-comparative-instruction-source-gate-v1.json', 'sha256': '9bc0c098870d03007fe4b0a3e53a0dbf25d48899352f585dc028556d77bb3c61'}
F = {'path': 'evaluations/T-0787/source-review/actual137-explicit-native-resolve-array-format-authority-v1.json', 'sha256': 'a8670222e39bfa190614747c008a3cf0f674e818e677fef6519b1ed039ee4591'}


def main():
    assert not OUT.exists(), 'Preserve previous drafts; do not retry/overwrite'
    primary, independent, fmt = [h.readpin(pin)[1] for pin in [P, I, F]]
    assert primary['ready_for_resolution_draft'] is True and primary['unresolved_source_questions'] == []
    assert independent['ready_for_exact_resolution_draft'] is True
    assert primary['stage_DB_pin'] == independent['stage_DB_pin']
    stage_path = h.checked_pin_path(primary['stage_DB_pin'])
    requests = h.readpin(primary['actual_request_pin'])[1]['requests']
    pending = [r['actual_request'] for r in requests]
    c = h.conn(stage_path)
    assert h.state(c) == {'journal_head': 448, 'pending': 137}
    actual = [dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')]
    assert pending == actual
    assert len(primary['rows']) == len(independent['individual_approvals']) == len(actual) == 137
    instructions, individual_rows, native = [], [], {}
    for index, (p, i, request) in enumerate(zip(primary['rows'], independent['individual_approvals'], actual)):
        assert p['index'] == i['index'] == index
        assert p['actual_request'] == i['actual_request'] == request
        instruction = p['resolution_instruction']
        assert instruction == i['approved_resolution_instruction']
        assert set(instruction) == {'request', 'rationale'} and instruction['request'] == request['id'] and instruction['rationale'].strip()
        assert p['retained_current_revision_id'] == i['retained_current_revision_id']
        rid = p['retained_current_revision_id']
        object_id = c.execute('select object_id from revision where id=?', (rid,)).fetchone()[0]
        assert h.current(c, object_id) == rid
        native[rid] = h.native(c, rid)
        instructions.append(copy.deepcopy(instruction))
        individual_rows.append({'index': index, 'actual_request': request, 'resolution_instruction': instruction,
                                'retained_current_revision_id': rid, 'full_current_native_pointer': '/current_native_payloads/' + rid,
                                'primary_pin': P, 'primary_row_pointer': '/rows/' + str(index), 'primary_whole_approved_row': p,
                                'independent_pin': I, 'independent_row_pointer': '/individual_approvals/' + str(index),
                                'independent_whole_approved_row': i, 'literal_instruction_equal': True, 'new_revision_or_rebind': False})
    ids = [r['request'] for r in instructions]
    assert len(set(ids)) == 137
    assert ids == primary['approved_request_ids'] == independent['approved_actual_request_ids']
    opid = 'T-0787/137-individually-dual-approved-actual-dependency-resolutions-v1'
    assert not c.execute('select id from operation where id=?', (opid,)).fetchone()
    native_package_path = R / 'evaluations/T-0787/implementation/exact136-draft-v1/exact136-one-operation-package-proposal-v1.json'
    assert h.sha(native_package_path) == 'b0ab311044a4039476659fd91be648541a39374b14c80c95ff4af03ba0c5aa99'
    native_package = json.loads(native_package_path.read_text())
    native_member = copy.deepcopy(native_package['operations'][0])
    h.readpin(native_member['operation_pin'])
    main_pin = h.pin(R / 'genealogy2/data/research.sqlite')
    assert main_pin['sha256'] == '1b551564c2067226be4083b52ee471c57268d719ad4aaa53b9d2dc2d43275e21'
    assert h.pin(stage_path) == primary['stage_DB_pin']
    for pin in [P, I, F]:
        h.checked_pin_path(pin)
    op = {'id': opid, 'actor': 'Sol; exact individually source-and-independent approved instructions under root draft-only authorization',
          'reason': 'T-0787: resolve the exact137 actual dependency requests using each separately approved literal rationale, retaining every current native payload and historical support edge.',
          'dependencyReviewVersion': 2, 'changes': [], 'resolve': instructions}
    OUT.mkdir(parents=True)
    op_pin = h.write(OUT / 'exact137-resolution-only-operation-v1.json', op)
    table_pin = h.write(OUT / 'all137-dual-literal-instruction-current-scope-and-retain-table-v1.json',
                        {'task': 'T-0787', 'primary_gate_pin': P, 'independent_gate_pin': I, 'native_format_authority_pin': F,
                         'rows': individual_rows, 'current_native_payloads': native, 'count': 137,
                         'stage_DB_pin': primary['stage_DB_pin'], 'actual_request_pin': primary['actual_request_pin'],
                         'all_IDs_once_literal_and_order_equal': True, 'new_revisions_or_rebinds': 0, 'runtime_applied': False})
    resolution_member = {'operation_id': opid, 'operation_pin': op_pin, 'target_ids': [], 'resolution_count': 137, 'ordered_request_ids': ids}
    members = [native_member, resolution_member]
    membership_pin = h.write(OUT / 'full-two-operation-136-target-137-resolution-membership-v1.json',
                             {'task': 'T-0787', 'operations': members, 'operation_count': 2, 'target_count': 136,
                              'revision_count': 130, 'create_count': 6, 'media_count': 1, 'resolution_count': 137,
                              'native_prefix_operation_pin_exact': native_member['operation_pin']})
    guard_pin = h.write(OUT / 'fresh448137-entire-pending-ID-literal-order-and-unchanged-stage-guard-v1.json',
                        {'task': 'T-0787', 'helper_pin': h.pin(Path(__file__).resolve()), 'primary_gate_pin': P, 'independent_gate_pin': I,
                         'native_format_authority_pin': F, 'stage_DB_pin_before': primary['stage_DB_pin'], 'stage_DB_pin_after': h.pin(stage_path),
                         'actual_state': h.state(c), 'actual_pending_IDs': ids, 'all137_literal_instructions_equal': True,
                         'all137_source_and_independent_current_scope_equal': True, 'native_prefix_exact': True,
                         'MAIN_pin_unchanged': main_pin, 'CLI_calls': 0, 'stage_runtime_or_canonical_authority': False,
                         'built_resolution_byte_gate_primary_approved': False, 'built_resolution_byte_gate_independent_approved': False,
                         'usage': 'UNKNOWN pending root collector'})
    package_pin = h.write(OUT / 'full-two-operation136-plus137-package-proposal-v1.json',
                          {'task': 'T-0787', 'membership_pin': membership_pin, 'operations': members, 'operation_count': 2,
                           'target_count': 136, 'existing_revisions': 130, 'new_objects': 6, 'media_count': 1, 'resolution_count': 137,
                           'native_prefix_package_pin': h.pin(native_package_path), 'native_prefix_consequence_table_pin': native_package['consequence_table_pin'],
                           'primary_actual_instruction_gate_pin': P, 'independent_actual_instruction_gate_pin': I, 'native_format_authority_pin': F,
                           'individual_resolution_consequence_table_pin': table_pin, 'resolution_guard_pin': guard_pin,
                           'pre_resolution_stage_DB_pin': primary['stage_DB_pin'], 'stage_actual_request_pin': primary['actual_request_pin'],
                           'built_byte_primary_approved': False, 'built_byte_independent_approved': False,
                           'same_stage_resolution_runtime_authorized': False, 'canonical_authorized': False,
                           'usage': 'UNKNOWN pending root collector'})
    c.close()
    print(json.dumps({'package_pin': package_pin, 'membership_pin': membership_pin, 'resolution_operation_pin': op_pin,
                      'table_pin': table_pin, 'guard_pin': guard_pin, 'count': 137, 'runtime_calls': 0}))


if __name__ == '__main__':
    main()
