"""UNRUN. Exact root-authorized canonical three-op CLI sequence; never DB replacement.

Requires both final source/consequence byte gates and a fresh all50 root baseline.
Preserve partial state and stop; no retry, newclone, source change or Wotan write.
"""
import argparse
import importlib.util
import json
import subprocess
import sys
import traceback
from pathlib import Path

R = Path(__file__).resolve().parents[3]
M = R / 'genealogy2/data/research.sqlite'
UTILITY = R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py'
S = importlib.util.spec_from_file_location('h', UTILITY)
h = importlib.util.module_from_spec(S)
S.loader.exec_module(h)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--authorization', type=Path, required=True)
    parser.add_argument('--authorization-sha256', required=True)
    args = parser.parse_args()
    ap = args.authorization.resolve()
    assert ap.is_relative_to(R) and h.sha(ap) == args.authorization_sha256
    auth = json.loads(ap.read_text())
    assert auth['authorization'] == 'ONE_CONTROLLED_EXACT_THREE_OPERATION37_PLUS27_CANONICAL_SEQUENCE'
    assert auth['root_authorized'] is True and auth['database_replacement_authorized'] is False
    assert auth['retry_authorized'] is False and auth['newclone_authorized'] is False
    assert auth['helper_pin'] == h.pin(Path(__file__).resolve())
    assert auth['proven_utility_pin'] == h.pin(UTILITY)
    _, package = h.readpin(auth['package_pin'])
    _, membership = h.readpin(auth['membership_pin'])
    assert package['membership_pin'] == auth['membership_pin']
    assert package['operations'] == membership['operations'] and package['operation_count'] == 3
    assert membership['target_count'] == 37 and membership['resolution_count'] == 27
    members = membership['operations']
    operations = [h.readpin(m['operation_pin']) for m in members]
    assert operations[0][1]['id'] == members[0]['operation_id']
    assert len(operations[0][1]['changes']) == 36 and len(operations[0][1]['media']) == 1
    assert operations[1][1]['id'] == members[1]['operation_id']
    assert len(operations[1][1]['changes']) == 1 and operations[1][1].get('media', []) == []
    assert operations[1][1]['changes'][0]['id'] == 'F-P-0532-source_assessment-widow-chain'
    assert operations[2][1]['id'] == members[2]['operation_id']
    assert operations[2][1]['changes'] == [] and len(operations[2][1]['resolve']) == 27
    assert all(op['dependencyReviewVersion'] == 2 for _, op in operations)
    _, final_handoff = h.readpin(auth['reviewed_final_stage_handoff_pin'])
    assert final_handoff['package_pin'] == auth['package_pin'] and final_handoff['membership_pin'] == auth['membership_pin']
    assert final_handoff['actual_state'] == {'journal_head': 452, 'pending': 0}
    assert final_handoff['stage_DB_pin'] == auth['reviewed_final_stage_DB_pin']
    _, corrective_handoff = h.readpin(final_handoff['native_prefix_stage_handoff_pin'])
    _, first_handoff = h.readpin(corrective_handoff['initial36_stage_handoff_pin'])
    _, second_state = h.readpin(auth['reviewed_correction_step_state_pin'])
    _, third_state = h.readpin(auth['reviewed_resolution_step_state_pin'])
    stage_states = [first_handoff['step_states'][0], second_state, third_state]
    assert stage_states[0]['before'] == {'journal_head': 449, 'pending': 0}
    assert stage_states[0]['after'] == stage_states[1]['before'] == {'journal_head': 450, 'pending': 27}
    assert stage_states[1]['after'] == stage_states[2]['before'] == {'journal_head': 451, 'pending': 27}
    assert stage_states[2]['after'] == {'journal_head': 452, 'pending': 0}
    _, primary_instructions = h.readpin(package['primary_actual_instruction_gate_pin'])
    _, independent_instructions = h.readpin(package['independent_actual_instruction_gate_pin'])
    primary_rows = h.pointer(primary_instructions, auth['primary_instruction_rows_pointer'])
    independent_rows = h.pointer(independent_instructions, auth['independent_instruction_rows_pointer'])
    primary_literals = [h.pointer(row, auth['primary_resolution_instruction_pointer']) for row in primary_rows]
    independent_literals = [h.pointer(row, auth['independent_resolution_instruction_pointer']) for row in independent_rows]
    primary_requests = [h.pointer(row, auth['primary_actual_request_pointer']) for row in primary_rows]
    independent_requests = [h.pointer(row, auth['independent_actual_request_pointer']) for row in independent_rows]
    assert len(primary_rows) == len(independent_rows) == 27
    assert operations[2][1]['resolve'] == primary_literals
    assert operations[2][1]['resolve'] == independent_literals
    pins = [auth['helper_pin'], auth['proven_utility_pin'], auth['package_pin'], auth['membership_pin'],
            auth['baseline_DB_pin'], auth['fresh_root_baseline_receipt_pin'], auth['protected42_pin'],
            auth['reviewed_final_stage_handoff_pin'], auth['reviewed_final_stage_DB_pin'],
            auth['reviewed_correction_step_state_pin'], auth['reviewed_resolution_step_state_pin'], auth['raw_all50_comparator_pin'],
            package['primary_actual_instruction_gate_pin'], package['independent_actual_instruction_gate_pin'],
            package['native_format_authority_pin'], package['native_prefix_package_pin'],
            package['individual_resolution_consequence_table_pin'], package['resolution_guard_pin'],
            *[m['operation_pin'] for m in members], *auth['review_pins'], *auth['media_pins']]
    def recheck(initial=False):
        assert h.sha(ap) == args.authorization_sha256
        for pin in pins:
            h.checked_pin_path(pin)
        if initial:
            assert h.pin(M) == auth['main_before_pin']
        for role in ['final_primary_source_gate', 'final_independent_source_consequence_gate']:
            definition = auth[role]
            _, gate = h.readpin(definition['pin'])
            assert h.pointer(gate, definition['ready_pointer']) is True
            assert h.pointer(gate, definition['package_pin_pointer']) == auth['package_pin']
            assert h.pointer(gate, definition['membership_pin_pointer']) == auth['membership_pin']
            assert h.pointer(gate, definition['stage_DB_pin_pointer']) == auth['reviewed_final_stage_DB_pin']
        assert auth['final_primary_source_gate']['pin']['path'] != auth['final_independent_source_consequence_gate']['pin']['path']
    recheck(True)
    baseline_path = h.checked_pin_path(auth['baseline_DB_pin'])
    base, live = h.conn(baseline_path), h.conn(M)
    before = h.all50(base)
    assert h.all50(live) == before and h.state(base) == h.state(live) == {'journal_head': 449, 'pending': 0}
    protected = h.readpin(auth['protected42_pin'])[1]['objects']
    assert len(protected) == 42
    for rid, n in protected.items():
        assert h.current(live, n['object_id']) == rid and h.native(live, rid) == n == h.native(base, rid)
    for _, op in operations:
        assert not live.execute('select id from operation where id=?', (op['id'],)).fetchone()
    heads = dict(live.execute('select object_id,max(version) from revision group by object_id'))
    for _, native_op in operations[:2]:
        for change in native_op['changes']:
            assert heads.get(change['id']) == change['expectedVersion']
            for edge in change['evidence']:
                assert heads.get(edge['object']) == edge['version']
            heads[change['id']] = (change['expectedVersion'] or 0) + 1
    output = (R / auth['output_path']).resolve()
    assert output.is_relative_to(R / 'evaluations/T-0788') and not output.exists()
    output.mkdir()
    journal = R / 'genealogy2/journal'
    prefix = {str(p.relative_to(journal)): h.sha(p) for p in journal.rglob('*') if p.is_file()}
    live.close()
    base.close()
    steps = []
    try:
        h.write(output / 'root-authorization-fresh-main-all50-and-original-journal-prefix-v1.json',
                {'authorization_pin': h.pin(ap), 'main_before_pin': auth['main_before_pin'], 'baseline_all50': before,
                 'actual_before': {'journal_head': 449, 'pending': 0}, 'journal_prefix': prefix, 'protected42_exact': True})
        stage = h.conn(R / auth['reviewed_final_stage_DB_pin']['path'])
        for index, (op_path, op) in enumerate(operations):
            recheck(index == 0)
            c = h.conn(M)
            actual_before = h.state(c)
            assert actual_before == stage_states[index]['before']
            for rid, n in protected.items():
                assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
            if index == 2:
                pending = [dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')]
                assert pending == primary_requests
                assert pending == independent_requests
                assert [r['id'] for r in pending] == [r['request'] for r in op['resolve']]
            c.close()
            for name, digest in prefix.items():
                assert h.sha(journal / name) == digest
            step = {'step': index + 1, 'operation_id': op['id'], 'operation_pin': members[index]['operation_pin'], 'before': actual_before}
            h.write(output / f'step-{index+1:02}-actual-before-v1.json', step)
            try:
                h.run_cli(['apply', str(op_path), '--db', str(M), '--journal', str(journal)], output / f'step-{index+1:02}-actual-CLI-output.json')
            finally:
                c = h.conn(M)
                step['after'] = h.state(c)
                c.close()
                h.write(output / f'step-{index+1:02}-actual-before-after-v1.json', step)
            assert step['after'] == stage_states[index]['after']
            c = h.conn(M)
            stored = dict(c.execute('select * from operation_payload where operation_id=?', (op['id'],)).fetchone())
            reviewed = dict(stage.execute('select * from operation_payload where operation_id=?', (op['id'],)).fetchone())
            assert json.loads(stored['request_json']) == op and stored == reviewed
            h.write(output / f'step-{index+1:02}-whole-stored-request-and-reviewed-stage-equality-v1.json', {'actual': stored, 'reviewed': reviewed, 'entire_request_JSON_and_array_order_exact': True})
            for rid, n in protected.items():
                assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
            c.close()
            steps.append(step)
        stage.close()
        compare_gate = output / 'reviewed-final-stage-raw-comparison-input-v1.json'
        h.write(compare_gate, {'operations': members, 'final_state': final_handoff['actual_state']})
        comparator = h.checked_pin_path(auth['raw_all50_comparator_pin'])
        compare_output = output / 'actual-MAIN-vs-reviewed-stage-all50-raw-values-and-order-v1.json'
        command = [sys.executable, str(comparator), '--stage', str(R / auth['reviewed_final_stage_DB_pin']['path']),
                   '--gate', str(compare_gate), '--output', str(compare_output)]
        result = subprocess.run(command, cwd=R, capture_output=True, text=True)
        stdout, stderr = output / 'all50-comparator.stdout.txt', output / 'all50-comparator.stderr.txt'
        stdout.write_text(result.stdout)
        stderr.write_text(result.stderr)
        h.write(output / 'all50-comparator-process-v1.json', {'argv': command, 'returncode': result.returncode,
                'stdout_pin': h.pin(stdout), 'stderr_pin': h.pin(stderr)})
        assert result.returncode == 0
        compared = json.loads(compare_output.read_text())
        assert compared['pass'] is True and compared['all50_schema_and_rows_compared'] is True
        c = h.conn(M)
        resolutions = [dict(r) for r in c.execute('select rowid as native_rowid,* from review_resolution where operation_id=? order by rowid', (operations[2][1]['id'],))]
        assert [{'request': v['request_id'], 'rationale': v['rationale']} for v in resolutions] == operations[2][1]['resolve']
        literal_pin = h.write(output / 'actual27-entire-literal-resolution-rows-and-order-v1.json', {'rows': resolutions, 'literal_and_order_equal': True})
        actual37 = h.readpin(corrective_handoff['all37_API_pin'])[1]['objects']
        for rid, n in actual37.items():
            assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
        for rid, n in protected.items():
            assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
        final = h.state(c)
        assert final == {'journal_head': 452, 'pending': 0}
        c.close()
        validators = []
        for cmd in ['verify', 'verify-assets', 'verify-source', 'inventory']:
            out = output / (cmd + '.json')
            actual = h.run_cli([cmd, '--db', str(M), '--journal', str(journal)], out)
            if cmd.startswith('verify'):
                assert actual['ok'] is True
            validators.append(h.pin(out))
        for person in ['P-0269', 'P-0270']:
            out = output / (person + '-default-verified-pedigree.json')
            h.run_cli(['pedigree', person, '--db', str(M)], out)
            validators.append(h.pin(out))
        for actual_pin, reviewed_pin in zip(validators, final_handoff['validators']):
            assert json.loads((R / actual_pin['path']).read_text()) == h.readpin(reviewed_pin)[1]
        recheck(False)
        for name, digest in prefix.items():
            assert h.sha(journal / name) == digest
        c = h.conn(M)
        assert h.state(c) == final
        c.close()
        handoff = h.write(output / 'complete-exact-three-operation-actual-canonical452-handoff-v1.json',
                          {'task': 'T-0788', 'authorization_pin': h.pin(ap), 'package_pin': auth['package_pin'],
                           'membership_pin': auth['membership_pin'], 'operation_pins': [m['operation_pin'] for m in members],
                           'reviewed_final_stage_handoff_pin': auth['reviewed_final_stage_handoff_pin'], 'actual_state': final,
                           'actual_step_states': steps, 'main_pin': h.pin(M), 'all50_raw_stage_comparison_pin': h.pin(compare_output),
                           'actual27_literal_resolution_pin': literal_pin, 'all37_native_and_protected42_exact_reviewed_stage': True,
                           'validators': validators, 'all_six_results_equal_reviewed_final_stage': True,
                           'database_replacement': False, 'program_receipts_or_owner_administration_applied': False,
                           'usage': 'UNKNOWN pending root collector'})
        print(json.dumps({'handoff_pin': handoff, 'actual_state': final}))
    except BaseException as error:
        c = h.conn(M)
        actual = h.state(c)
        c.close()
        h.write(output / 'STOP-preserved-canonical-partial-state-and-failure-v1.json',
                {'error': repr(error), 'traceback': traceback.format_exc(), 'actual_state': actual,
                 'main_pin': h.pin(M), 'completed_steps': steps, 'no_retry_no_DB_replace_no_newclone': True})
        raise


if __name__ == '__main__':
    main()
