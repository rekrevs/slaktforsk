"""UNRUN. One separately root-authorized same-stage resolution and six final checks.

Never a new clone, canonical write, DB replacement, inferred retain or retry.
"""
import argparse
import importlib.util
import json
import shutil
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
    assert auth['authorization'] == 'ONE_EXACT16_SAME_STAGE_RESOLUTION_AND_READONLY_FINAL_SIX_CHECKS'
    assert auth['root_authorized'] is True and auth['canonical_authorized'] is False
    assert auth['retry_authorized'] is False and auth['newclone_authorized'] is False
    assert auth['helper_pin'] == h.pin(Path(__file__).resolve())
    assert auth['proven_utility_pin'] == h.pin(UTILITY)
    pp, package = h.readpin(auth['package_pin'])
    mp, membership = h.readpin(auth['membership_pin'])
    assert package['membership_pin'] == auth['membership_pin']
    assert package['operations'] == membership['operations'] and len(membership['operations']) == 2
    member = membership['operations'][1]
    op_path, op = h.readpin(auth['resolution_operation_pin'])
    assert member['operation_pin'] == auth['resolution_operation_pin'] and member['operation_id'] == op['id']
    assert op['changes'] == [] and op['dependencyReviewVersion'] == 2 and len(op['resolve']) == 16
    assert set(op) == {'id', 'actor', 'reason', 'changes', 'dependencyReviewVersion', 'resolve'}
    assert [r['request'] for r in op['resolve']] == member['ordered_request_ids']
    assert len(set(member['ordered_request_ids'])) == 16
    source = h.readpin(package['primary_actual_instruction_gate_pin'])[1]
    own = h.readpin(package['independent_actual_instruction_gate_pin'])[1]
    primary_rows = h.pointer(source, auth['primary_instruction_rows_pointer'])
    independent_rows = h.pointer(own, auth['independent_instruction_rows_pointer'])
    primary_literals = [h.pointer(row, auth['primary_resolution_instruction_pointer']) for row in primary_rows]
    independent_literals = [h.pointer(row, auth['independent_resolution_instruction_pointer']) for row in independent_rows]
    primary_requests = [h.pointer(row, auth['primary_actual_request_pointer']) for row in primary_rows]
    independent_requests = [h.pointer(row, auth['independent_actual_request_pointer']) for row in independent_rows]
    assert len(primary_rows) == len(independent_rows) == 16
    fmt = h.readpin(package['native_format_authority_pin'])[1]
    assert op['resolve'] == primary_literals
    assert op['resolve'] == independent_literals
    assert fmt['native_request_fields'] == {k: op[k] for k in ['changes', 'resolve', 'dependencyReviewVersion']}
    pins = [auth['helper_pin'], auth['proven_utility_pin'], auth['package_pin'], auth['membership_pin'],
            auth['resolution_operation_pin'], package['primary_actual_instruction_gate_pin'],
            package['independent_actual_instruction_gate_pin'], package['native_format_authority_pin'],
            package['individual_resolution_consequence_table_pin'], package['resolution_guard_pin'],
            package['native_prefix_package_pin'], membership['operations'][0]['operation_pin'],
            auth['pre_resolution_stage_DB_pin'], auth['pre_resolution_handoff_pin'], auth['protected42_pin'],
            *auth['review_pins'], *auth['media_pins']]
    def recheck(stage_before=False):
        assert h.sha(ap) == args.authorization_sha256
        for pin in pins:
            if not stage_before and pin == auth['pre_resolution_stage_DB_pin']:
                continue
            h.checked_pin_path(pin)
        assert h.pin(M) == auth['main_pin']
        for role in ['primary_built_resolution_gate', 'independent_built_resolution_gate']:
            definition = auth[role]
            _, gate = h.readpin(definition['pin'])
            assert h.pointer(gate, definition['ready_pointer']) is True
            assert h.pointer(gate, definition['package_pin_pointer']) == auth['package_pin']
            assert h.pointer(gate, definition['membership_pin_pointer']) == auth['membership_pin']
            assert h.pointer(gate, definition['operation_pin_pointer']) == auth['resolution_operation_pin']
        assert auth['primary_built_resolution_gate']['pin']['path'] != auth['independent_built_resolution_gate']['pin']['path']
    recheck(True)
    db = h.checked_pin_path(auth['pre_resolution_stage_DB_pin'])
    assert db.is_relative_to(R / 'evaluations/T-0789/exact21-stage-v1') and db.name == 'stage.sqlite'
    journal = db.parent / 'journal'
    snapshot = (R / auth['preservation_snapshot_path']).resolve()
    assert snapshot.parent == db.parent and snapshot != db and not snapshot.exists()
    output = (R / auth['resolution_output_path']).resolve()
    assert output.is_relative_to(db.parent) and not output.exists()
    _, before_handoff = h.readpin(auth['pre_resolution_handoff_pin'])
    assert before_handoff['stage_DB_pin'] == auth['pre_resolution_stage_DB_pin']
    assert before_handoff['actual_state'] == {'journal_head': 453, 'pending': 16}
    h.checked_pin_path(before_handoff['input_binding_projection_proof_pin'])
    assert before_handoff['readonly_continuation_only_no_CLI'] is True
    c, live = h.conn(db), h.conn(M)
    assert h.state(c) == {'journal_head': 453, 'pending': 16}
    assert h.state(live) == {'journal_head': 452, 'pending': 0}
    main_before = h.all50(live)
    before = h.all50(c)
    prefix_operation = h.readpin(membership['operations'][0]['operation_pin'])[1]
    assert json.loads(c.execute('select request_json from operation_payload where operation_id=?',
                      (prefix_operation['id'],)).fetchone()[0]) == prefix_operation
    assert h.current(c, 'P-0007') == 'P-0007@2'
    for change in prefix_operation['changes']:
        if 'bindings' in change:
            assert change['id'] in {'ID-T0789-P0007-own-annual-1945', 'ID-T0789-P0007-own-annual-1946'}
            assert change['bindings'] == {'P-0007': 2}
            assert [e for e in change['evidence'] if e['object'] == 'P-0007'][0]['version'] == 2
            # Explicit ordered evidence is the active guard, bindings is redundant.
    pending = [dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')]
    assert pending == primary_requests == independent_requests
    assert [r['id'] for r in pending] == [r['request'] for r in op['resolve']]
    assert not c.execute('select id from operation where id=?', (op['id'],)).fetchone()
    protected = h.readpin(auth['protected42_pin'])[1]['objects']
    assert len(protected) == 42
    for rid, n in protected.items():
        assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
    c.close()
    output.mkdir()
    step = {'operation_pin': auth['resolution_operation_pin'], 'before': {'journal_head': 453, 'pending': 16}}
    try:
        shutil.copyfile(db, snapshot)
        assert h.sha(snapshot) == auth['pre_resolution_stage_DB_pin']['sha256']
        base = h.conn(snapshot)
        journal_prefix = {str(p.relative_to(journal)): h.sha(p) for p in journal.rglob('*') if p.is_file()}
        h.write(output / 'authorization-preservation-snapshot-and-actual-before-v1.json',
                {'authorization_pin': h.pin(ap), 'snapshot_pin': h.pin(snapshot), 'before_all50': before,
                 'main_before_all50': main_before, 'journal_prefix': journal_prefix, 'actual_state': step['before']})
        recheck(True)
        try:
            h.run_cli(['apply', str(op_path), '--db', str(db), '--journal', str(journal)], output / 'one-resolution-CLI-actual-output.json')
        finally:
            c = h.conn(db)
            step['after'] = h.state(c)
            c.close()
            h.write(output / 'one-resolution-actual-before-after-v1.json', step)
        c = h.conn(db)
        final = h.state(c)
        assert final == {'journal_head': 454, 'pending': 0}
        stored = dict(c.execute('select * from operation_payload where operation_id=?', (op['id'],)).fetchone())
        assert json.loads(stored['request_json']) == op, 'Unexpected native operation representation; stop, no rewrite'
        literal_rows = [dict(r) for r in c.execute('select rowid as native_rowid,* from review_resolution where operation_id=? order by rowid', (op['id'],))]
        assert len(literal_rows) == 16
        assert [{'request': r['request_id'], 'rationale': r['rationale']} for r in literal_rows] == op['resolve']
        assert all(r['operation_id'] == op['id'] for r in literal_rows)
        after = h.all50(c)
        assert before['schema'] == after['schema']
        allowed = {'operation': 1, 'operation_payload': 1, 'review_resolution': 16}
        ordered_proofs = {}
        for name in before['tables']:
            if name not in allowed:
                assert before['tables'][name] == after['tables'][name], ('Unexpected knowledge/metadata table change', name)
            else:
                assert after['tables'][name]['rows'] == before['tables'][name]['rows'] + allowed[name]
            sql = base.execute('select sql from sqlite_master where name=?', (name,)).fetchone()[0]
            if 'WITHOUT ROWID' in sql.upper():
                assert before['tables'][name] == after['tables'][name]
                ordered_proofs[name] = {'whole_table_exact': True}
                continue
            old = h.rows(base, name, True)
            maximum = base.execute('select max(rowid) from "' + name + '"').fetchone()[0]
            actual = h.rows(c, name, True, maximum) if maximum is not None else []
            assert old == actual, ('Old rowid/native array order changed', name)
            ordered_proofs[name] = {'whole_old_rowid_order_exact': True, 'old_order_sha256': h.row_digest(old, True)}
        for name, digest in journal_prefix.items():
            assert h.sha(journal / name) == digest
        for rid, n in protected.items():
            assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
        actual_targets = h.readpin(before_handoff['all21_API_pin'])[1]['objects']
        for rid, n in actual_targets.items():
            assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
        literal_pin = h.write(output / 'entire-stored-operation-and-all16-literal-rowid-resolutions-v1.json',
                              {'operation_pin': auth['resolution_operation_pin'], 'stored': stored, 'rows': literal_rows,
                               'whole_request_JSON_and_all16_literals_order_exact': True})
        compare_pin = h.write(output / 'all50-exact47-knowledge-order-and-three-append-tables-proof-v1.json',
                              {'before': before, 'after': after, 'only_allowed_append_tables': allowed,
                               'all_old_rows_order_exact': ordered_proofs, 'protected42_whole_current_exact': True,
                               'all21_actual_native_targets_unchanged': True, 'no_source_or_metadata_array_normalization': True})
        c.close()
        validators = []
        for cmd in ['verify', 'verify-assets', 'verify-source', 'inventory']:
            out = output / (cmd + '.json')
            actual = h.run_cli([cmd, '--db', str(db), '--journal', str(journal)], out)
            if cmd.startswith('verify'):
                assert actual['ok'] is True
            validators.append(h.pin(out))
        for person in ['P-0269', 'P-0270']:
            out = output / (person + '-default-verified-pedigree.json')
            h.run_cli(['pedigree', person, '--db', str(db)], out)
            validators.append(h.pin(out))
        recheck(False)
        assert h.all50(live) == main_before and h.state(live) == {'journal_head': 452, 'pending': 0}
        c = h.conn(db)
        assert h.state(c) == final
        c.close()
        handoff = h.write(output / 'complete-two-op21-plus16-resolution-actual454-final-stage-handoff-v1.json',
                          {'task': 'T-0789', 'authorization_pin': h.pin(ap), 'package_pin': auth['package_pin'],
                           'membership_pin': auth['membership_pin'], 'resolution_operation_pin': auth['resolution_operation_pin'],
                           'native_prefix_stage_handoff_pin': auth['pre_resolution_handoff_pin'], 'input_binding_projection_proof_pin': before_handoff['input_binding_projection_proof_pin'], 'preservation_snapshot_pin': h.pin(snapshot),
                           'literal16_stored_resolution_pin': literal_pin, 'only_three_append_table_diff_pin': compare_pin,
                           'actual_state': final, 'stage_DB_pin': h.pin(db), 'validators': validators,
                           'protected42_current_metadata_history_order_exact': True, 'all21_native_payloads_unchanged': True,
                           'MAIN_physical_and_all50_unchanged': True, 'canonical_applied': False,
                           'final_source_and_independent_canonical_byte_gates_required': True, 'program_acceptance': False,
                           'usage': 'UNKNOWN pending root collector'})
        print(json.dumps({'handoff_pin': handoff, 'actual_state': final}))
        base.close()
    except BaseException as error:
        c = h.conn(db)
        actual = h.state(c)
        c.close()
        h.write(output / 'STOP-preserved-resolution-failure-and-actual-state-v1.json',
                {'error': repr(error), 'traceback': traceback.format_exc(), 'actual_state': actual,
                 'stage_DB_pin': h.pin(db), 'main_pin': h.pin(M), 'step': step,
                 'no_retry_no_newclone_no_canonical': True})
        raise
    finally:
        live.close()


if __name__ == '__main__':
    main()
