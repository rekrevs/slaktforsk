"""UNRUN: root-authorized exact-nine controlled MAIN CLI apply; no retry/DB replacement.

Authorization must pin this helper, both FINAL source/consequence gates and a
fresh all50 baseline check. Preparation or a stage approval cannot authorize it.
"""
import argparse
import datetime
import importlib.util
import json
import subprocess
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / 'evaluations/T-0784'
MAIN = ROOT / 'genealogy2/data/research.sqlite'
JOURNAL = ROOT / 'genealogy2/journal'
READ_HELPER = ROOT / 'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py'
READ_HELPER_SHA = 'ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2'
PROPOSAL_SHA = 'fd438f10ba90901ab1171868c00e8acebb86de19979bcc1c64b3d0ac393b3ee9'
MEMBERSHIP_SHA = '33afa563644ee34c07147006cae92e4e7a54dfd92871611dac84dad94ff8c176'
BASELINE_MAIN_SHA = '42321e363573c243597aded458e6a10d2d6cd8e4be47da02a227b149bbaed45f'


def main():
    if not __debug__:
        raise RuntimeError('Assertions must remain enabled')
    parser = argparse.ArgumentParser()
    parser.add_argument('--authorization', type=Path, required=True)
    parser.add_argument('--authorization-sha256', required=True)
    args = parser.parse_args()
    # Import pure readonly/native functions only; imported main is never invoked.
    import hashlib
    assert hashlib.sha256(READ_HELPER.read_bytes()).hexdigest() == READ_HELPER_SHA
    spec = importlib.util.spec_from_file_location('t0781_readonly_native_functions', READ_HELPER)
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    auth_path = args.authorization.resolve()
    assert auth_path.is_relative_to(TASK)
    assert h.sha(auth_path) == args.authorization_sha256
    auth = json.loads(auth_path.read_text())
    assert auth['task'] == 'T-0784'
    assert auth['authorization'] == 'CONTROLLED_MAIN_EXACT_ONE_NINE_CLI_APPLY_ONCE'
    assert auth['root_authorized'] is True and auth['canonical_apply_authorized'] is True
    assert auth['retry_authorized'] is False and auth['database_replacement_authorized'] is False
    assert auth['helper_pin'] == h.pin(Path(__file__).resolve())
    assert auth['readonly_helper_pin'] == h.pin(READ_HELPER)
    assert auth['main_pin'] == {'path': 'genealogy2/data/research.sqlite', 'sha256': BASELINE_MAIN_SHA}
    assert auth['journal_path'] == 'genealogy2/journal'
    assert auth['baseline_state'] == {'journal_head': 442, 'pending': 0}
    assert auth['final_state'] == {'journal_head': 443, 'pending': 0}
    out = (ROOT / auth['output_path']).resolve()
    assert out.is_relative_to(TASK) and not out.exists()
    out.mkdir()
    completed, attempted = [], 0

    def save(name, value):
        return h.write(out / name, value)

    def checked(pin):
        path = (ROOT / pin['path']).resolve()
        assert path.is_relative_to(ROOT) and h.sha(path) == pin['sha256'], pin
        return path

    def loaded(pin):
        return json.loads(checked(pin).read_text())

    immutable_pins = [auth['helper_pin'], auth['readonly_helper_pin'],
                      auth['proposal_pin'], auth['membership_pin'],
                      auth['actual_step_state_index_pin'], auth['reviewed_final_stage_DB_pin'],
                      auth['baseline_DB_pin'], auth['fresh_baseline_receipt_pin'],
                      auth['protected42_pin'], auth['actual_native_context_pin'], auth['actual_native9_pin'],
                      auth['actual_request_pin'], auth['stage_handoff_pin'], auth['baseline_person_context_pin'], auth['root_all50_comparator_pin'],
                      *auth['media_pins'], *auth['review_pins'], *auth['code_pins'],
                      auth['primary_final_gate']['pin'], auth['independent_final_gate']['pin']]

    def recheck():
        assert h.sha(auth_path) == args.authorization_sha256
        by_path = {}
        for p in immutable_pins:
            assert by_path.setdefault(p['path'], p['sha256']) == p['sha256']
        for path, digest in by_path.items():
            checked({'path': path, 'sha256': digest})

    def protected_check(c, protected):
        for rid, n in protected.items():
            assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n

    def gatecheck(role):
        gspec = auth[role]
        g = loaded(gspec['pin'])
        assert h.pointer(g, gspec['ready_pointer']) is True
        assert h.pointer(g, gspec['proposal_pin_pointer']) == auth['proposal_pin']
        assert h.pointer(g, gspec['membership_pin_pointer']) == auth['membership_pin']
        assert h.pointer(g, gspec['stage_DB_pin_pointer']) == auth['reviewed_final_stage_DB_pin']

    try:
        recheck()
        assert auth['proposal_pin']['sha256'] == PROPOSAL_SHA
        assert auth['membership_pin']['sha256'] == MEMBERSHIP_SHA
        assert auth['primary_final_gate']['pin']['path'] != auth['independent_final_gate']['pin']['path']
        gatecheck('primary_final_gate')
        gatecheck('independent_final_gate')
        assert h.pointer(loaded(auth['fresh_baseline_receipt_pin']),
                         auth['fresh_baseline_ready_pointer']) is True
        proposal, membership = loaded(auth['proposal_pin']), loaded(auth['membership_pin'])
        members = membership['operations']
        assert proposal['operations'] == members and proposal['membership_pin'] == auth['membership_pin']
        assert len(members) == 1 and sum(m['changes'] for m in members) == 9
        steps = loaded(auth['actual_step_state_index_pin'])
        assert steps['membership_pin'] == auth['membership_pin']
        assert steps['actual_final_state'] == auth['final_state'] and steps['no_state_counts_inferred'] is True
        assert len(steps['steps']) == 1
        operations = []
        for m, s in zip(members, steps['steps']):
            assert m['operation_id'] == s['operation_id']
            actual_receipt = loaded(s['actual_step_receipt_pin'])
            assert actual_receipt['before'] == s['expected_before']
            assert actual_receipt['after'] == s['expected_after']
            immutable_pins.extend([{'path': m['path'], 'sha256': m['sha256']}, s['actual_step_receipt_pin']])
            operations.append({**m, 'expected_before': s['expected_before'], 'expected_after': s['expected_after']})
        assert auth['operations'] == operations
        assert auth['operations'][0]['expected_before'] == auth['baseline_state']
        assert auth['operations'][-1]['expected_after'] == auth['final_state']
        for left, right in zip(operations, operations[1:]):
            assert left['expected_after'] == right['expected_before']
        ops = [loaded(m) for m in members]
        assert len({op['id'] for op in ops}) == 1
        for i, (m, op) in enumerate(zip(members, ops)):
            assert op['id'] == m['operation_id'] and op['dependencyReviewVersion'] == 2
            assert len(op['changes']) == m['changes']
            assert not set(op).intersection({'resolve', 'media', 'spans', 'mappings', 'unitDecisions'})
        actual_requests = loaded(auth['actual_request_pin'])
        assert actual_requests['actual_pending_count'] == 0 and actual_requests['requests'] == []
        stage_handoff = loaded(auth['stage_handoff_pin'])
        assert stage_handoff['actual_state'] == auth['final_state']
        assert stage_handoff['stage_DB_pin'] == auth['reviewed_final_stage_DB_pin']
        assert stage_handoff['proposal_pin'] == auth['proposal_pin'] and stage_handoff['membership_pin'] == auth['membership_pin']
        # Unexpected pending requires explicit separate source/independent disposition and a new runner review.
        # Pin actual CLI implementation, not a modified preparation wrapper.
        code_paths = {p['path'] for p in auth['code_pins']}
        assert {'genealogy2/cli.mjs', 'genealogy2/lib/recovery.mjs',
                'genealogy2/lib/domain.mjs', 'genealogy2/lib/store.mjs'} <= code_paths
        assert h.sha(MAIN) == BASELINE_MAIN_SHA
        journal_prefix = [h.pin(p) for p in sorted(JOURNAL.glob('*.json'))]
        assert len(journal_prefix) == 442
        save('original442-canonical-journal-file-prefix-pins-v1.json', journal_prefix)
        baseline_path = checked(auth['baseline_DB_pin'])
        stage_path = checked(auth['reviewed_final_stage_DB_pin'])
        assert baseline_path.is_relative_to(TASK) and stage_path.is_relative_to(TASK)
        assert baseline_path != MAIN and stage_path != MAIN
        base, live, stage = h.conn(baseline_path), h.conn(MAIN), h.conn(stage_path)
        try:
            before = h.all50(base)
            assert h.all50(live) == before and h.state(base) == h.state(live) == auth['baseline_state']
            assert h.state(stage) == auth['final_state']
            protected = loaded(auth['protected42_pin'])['objects']
            assert len(protected) == 42
            protected_check(base, protected)
            protected_check(live, protected)
            protected_check(stage, protected)
            heads = dict(base.execute('select object_id,max(version) from revision group by object_id'))
            ids = set()
            for op in ops:
                assert base.execute('select count(*) from operation where id=?', (op['id'],)).fetchone()[0] == 0
                for x in op['changes']:
                    assert x['id'] not in ids and heads.get(x['id']) == x['expectedVersion']
                    assert x['id'] not in {n['object_id'] for n in protected.values()}
                    ids.add(x['id'])
                    for e in x['evidence']:
                        assert heads.get(e['object']) == e['version'], (x['id'], e)
                    heads[x['id']] = (x['expectedVersion'] or 0) + 1
            assert len(ids) == 9
            save('fresh-live442-all50-and-protected42-before-v1.json',
                 {'authorization_pin': h.pin(auth_path), 'fresh_root_receipt_pin': auth['fresh_baseline_receipt_pin'],
                  'baseline_DB_pin': auth['baseline_DB_pin'], 'MAIN_pin': h.pin(MAIN), 'all50': before,
                  'protected42': True, 'actual_state': h.state(live), 'CLI_invocations': 0})
        finally:
            base.close()
            live.close()
            stage.close()
        for i, (m, op) in enumerate(zip(operations, ops), 1):
            recheck()
            for p in journal_prefix:
                checked(p)
            gatecheck('primary_final_gate')
            gatecheck('independent_final_gate')
            c = h.conn(MAIN)
            try:
                actual_before = h.state(c)
                assert actual_before == m['expected_before']
                assert c.execute('select count(*) from operation where id=?', (op['id'],)).fetchone()[0] == 0
                protected_check(c, protected)
                actual_pending = [dict(r) for r in c.execute('select * from pending_review order by id')]
                assert actual_pending == []
            finally:
                c.close()
            receipt = {'index': i, 'authorization_pin': h.pin(auth_path), 'operation_pin': h.pin(ROOT / m['path']),
                       'operation_id': op['id'], 'before': actual_before,
                       'reviewed_stage_step_pin': steps['steps'][i - 1]['actual_step_receipt_pin'],
                       'started_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
            save(f'step-{i:02}-actual-before-v1.json', receipt)
            command = ['node', 'genealogy2/cli.mjs', 'apply', m['path']]
            receipt['argv'] = command
            attempted += 1
            try:
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
                (out / f'step-{i:02}-apply.stdout.json').write_text(result.stdout)
                (out / f'step-{i:02}-apply.stderr.txt').write_text(result.stderr)
                receipt['exit_code'] = result.returncode
            finally:
                c = h.conn(MAIN)
                try:
                    receipt['after'] = h.state(c)
                finally:
                    c.close()
                receipt['MAIN_pin_after'] = h.pin(MAIN)
                receipt['finished_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                save(f'step-{i:02}-actual-before-after-CLI-receipt-v1.json', receipt)
            assert result.returncode == 0, ('STOP no retry', i, result.stderr)
            assert receipt['after'] == m['expected_after']
            output = json.loads(result.stdout)
            assert output['operation'] == op['id'] and output['unchanged'] is False
            assert output['changes'] == len(op['changes'])
            c = h.conn(MAIN)
            try:
                journal = dict(c.execute('select p.*,o.request_hash,o.recorded_at from operation_payload p join operation o on o.id=p.operation_id where p.operation_id=?', (op['id'],)).fetchone())
                assert json.loads(journal['request_json']) == op
                assert journal['sequence'] == receipt['after']['journal_head']
                journal_file = JOURNAL / (str(journal['sequence']).zfill(9) + '-' + journal['request_hash'] + '.json')
                envelope = json.loads(journal_file.read_text())
                assert envelope['format'] == 'genealogy2-journal/1' and envelope['sequence'] == journal['sequence']
                assert envelope['requestHash'] == journal['request_hash'] and envelope['request'] == op
                assert envelope['policy'] == journal['policy']
                assert envelope['recordedAt'] == journal['recorded_at']
                assert len(list(JOURNAL.glob('*.json'))) == receipt['after']['journal_head']
                protected_check(c, protected)
                save(f'step-{i:02}-entire-stored-request-json-exact-v1.json',
                     {'stored_operation_payload': journal, 'submitted_operation_pin': h.pin(ROOT / m['path']),
                      'durable_journal_file_pin': h.pin(journal_file), 'durable_journal_envelope': envelope,
                      'structural_request_equality': True, 'all_array_order_preserved': True})
            finally:
                c.close()
            completed.append(receipt)
            print(json.dumps({'completed': i, 'of': 1, 'actual_state': receipt['after']}), flush=True)
        recheck()
        for p in journal_prefix:
            checked(p)
        # Root's separate comparator has NO derived-search exemption. Its only
        # allowed difference is recorded_at on these exact-nine new operations.
        comparator = checked(auth['root_all50_comparator_pin'])
        assert comparator == (TASK / 'implementation/compare_actual_stage_exact_nine_v1.py').resolve()
        comp_command = ['python3', str(comparator), '--stage', str(stage_path), '--gate', str(auth_path),
                        '--output', str(out / 'root-all50-reviewed-stage-versus-actual-MAIN-v1.json')]
        process = subprocess.run(comp_command, cwd=ROOT, capture_output=True, text=True)
        (out / 'root-all50-comparison.stdout.txt').write_text(process.stdout)
        (out / 'root-all50-comparison.stderr.txt').write_text(process.stderr)
        save('root-all50-comparison-process-receipt-v1.json', {'argv': comp_command, 'exit_code': process.returncode})
        assert process.returncode == 0
        comparison = json.loads((out / 'root-all50-reviewed-stage-versus-actual-MAIN-v1.json').read_text())
        assert comparison['pass'] is True and comparison['actual_canonical_state'] == auth['final_state']
        base, c = h.conn(baseline_path), h.conn(MAIN)
        try:
            after = h.all50(c)
            assert after['schema'] == before['schema']
            preserved = {}
            for name in before['tables']:
                if name in h.DERIVED:
                    continue  # Final whole stage comparison above still checks these raw tables.
                sql = base.execute('select sql from sqlite_master where name=?', (name,)).fetchone()[0]
                if 'WITHOUT ROWID' in sql.upper():
                    assert after['tables'][name] == before['tables'][name]
                else:
                    limit = base.execute('select max(rowid) from "' + name + '"').fetchone()[0]
                    old = h.rows(base, name, True)
                    assert (h.rows(c, name, True, limit) if limit is not None else []) == old
                preserved[name] = {'old_full_rows_and_native_order_exact': True}
            for pin_name, count in [('actual_native_context_pin', None), ('actual_native9_pin', 9)]:
                full = loaded(auth[pin_name])['objects']
                assert count is None or len(full) == count
                for rid, n in full.items():
                    assert h.native(c, rid) == n
            protected_check(c, protected)
            assert h.rows(c, 'review_resolution', True) == h.rows(base, 'review_resolution', True)
            save('exact-old-native-history-row-order-protected42-and-nine-context-proof-v1.json',
                 {'old_tables': preserved, 'all9_and_context_full_native_equal_reviewed_stage': True,
                  'protected42_current_and_full_native_exact': True, 'review_resolution_baseline_exact': True,
                  'asset_and_native_asset_baseline_exact': after['tables']['asset'] == before['tables']['asset'] and after['tables']['native_asset'] == before['tables']['native_asset']})
            assert after['tables']['asset'] == before['tables']['asset'] and after['tables']['native_asset'] == before['tables']['native_asset']
            save('actual-canonical443-all50-post-state-v1.json', after)
        finally:
            base.close()
            c.close()
        validators = []
        for name, command in [('verify', ['verify']), ('verify-assets', ['verify-assets']),
                              ('verify-source', ['verify-source']), ('inventory', ['inventory']),
                              ('pedigree-verified-P0269', ['pedigree', 'P-0269'])]:
            output = out / (name + '.json')
            result = h.run_cli(command, output)
            if name.startswith('verify'):
                assert result['ok'] is True
            validators.append(h.pin(output))
        for label, command in [('pedigree-verified-P0270', ['pedigree','P-0270']),
                               ('pedigree-typed-P0269', ['pedigree','P-0269','--mode','typed']),
                               ('pedigree-typed-P0270', ['pedigree','P-0270','--mode','typed']),
                               *[(person+'-whole-person',['person',person,'--full','--format','json']) for person in ['P-0211','P-0003','P-0007']]]:
            output = out / (label+'.json')
            h.run_cli(command, output)
            validators.append(h.pin(output))
        c = h.conn(MAIN)
        try:
            axis_rows = [dict(r) for r in c.execute("select a.*,r.object_id,r.version from assessment a join current_revision r on r.id=a.revision_id where a.subject_id in ('P-0211','P-0003','P-0007') and a.criteria in ('identity_review/1','tree_effect/1') order by a.subject_id,a.criteria")]
            assert len(axis_rows)==6
            save('three-current-native-identity-tree-axes-coremetrics-NO-PROMOTION-v1.json', {'axes':axis_rows,'source_grade_inferred':False,'Wotan_priority_or_status_changed':False,'before_input_pin':auth['baseline_person_context_pin']})
        finally:
            c.close()
        recheck()
        c = h.conn(MAIN)
        try:
            assert h.state(c) == auth['final_state'] and h.all50(c) == after
        finally:
            c.close()
        final_pin = save('complete-exact-nine-controlled-canonical-actual443-zero-pending-handoff-v1.json',
                         {'task': 'T-0784', 'authorization_pin': h.pin(auth_path), 'MAIN_pin': h.pin(MAIN),
                          'actual_state': auth['final_state'], 'reviewed_final_stage_DB_pin': auth['reviewed_final_stage_DB_pin'],
                          'proposal_pin': auth['proposal_pin'], 'membership_pin': auth['membership_pin'],
                          'completed_operations': completed, 'actual_CLI_invocations': attempted,
                          'root_all50_comparison_pin': h.pin(out / 'root-all50-reviewed-stage-versus-actual-MAIN-v1.json'),
                          'native_protected_history_proof_pin': h.pin(out / 'exact-old-native-history-row-order-protected42-and-nine-context-proof-v1.json'),
                          'validator_pins': validators, 'actual_three_person_identity_acceptance': False,
                          'five_owner_administration_applied': False,
                          'actual_worker_usage': 'Root collects after worker final; unknown here, not zero.'})
        print(json.dumps({'final_handoff_pin': final_pin}), flush=True)
    except BaseException as error:
        c = h.conn(MAIN)
        try:
            actual = h.state(c)
        finally:
            c.close()
        save('failure-stop-preserved-actual-canonical-state-no-retry-v1.json',
             {'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(),
              'actual_state': actual, 'MAIN_pin': h.pin(MAIN), 'attempted_CLI_invocations': attempted,
              'completed_operations': completed, 'no_retry_no_DB_replace_no_admin_or_acceptance': True})
        raise


if __name__ == '__main__':
    main()
