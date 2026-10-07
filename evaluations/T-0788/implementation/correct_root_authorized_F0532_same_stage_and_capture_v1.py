"""UNRUN same-stage single F532 correction/capture; root authorization required.

No clone creation, resolution, canonical, retry or Wotan mutation.
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
s = importlib.util.spec_from_file_location('h', UTILITY)
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--authorization', type=Path, required=True)
    parser.add_argument('--authorization-sha256', required=True)
    args = parser.parse_args()
    ap = args.authorization.resolve()
    assert ap.is_relative_to(R) and h.sha(ap) == args.authorization_sha256
    auth = json.loads(ap.read_text())
    assert auth['authorization'] == 'ONE_EXACT_F0532_SAME_STAGE_CORRECTION_AND_ACTUAL_CAPTURE'
    assert auth['root_authorized'] is True
    assert all(auth[k] is False for k in ['canonical_authorized', 'resolution_authorized', 'retry_authorized', 'newclone_authorized'])
    assert auth['helper_pin'] == h.pin(Path(__file__).resolve()) and auth['proven_utility_pin'] == h.pin(UTILITY)
    package = h.readpin(auth['package_pin'])[1]
    membership = h.readpin(auth['membership_pin'])[1]
    assert package['membership_pin'] == auth['membership_pin']
    assert package['operations'] == membership['operations'] and len(membership['operations']) == 2
    prefix, correction = membership['operations']
    first = h.readpin(auth['initial36_stage_handoff_pin'])[1]
    assert prefix['operation_pin'] == first['operation_pin']
    assert first['stage_DB_pin'] == auth['pre_correction_stage_DB_pin']
    assert first['actual_state'] == {'journal_head': 450, 'pending': 27}
    source = h.readpin(auth['correction_source_spec_pin'])[1]
    literal = source['rows'][0]
    op_path, op = h.readpin(correction['operation_pin'])
    assert correction['operation_pin'] == auth['correction_operation_pin'] and correction['operation_id'] == op['id']
    assert op['dependencyReviewVersion'] == 2 and op['changes'] == [literal['full_new_API']]
    assert op.get('resolve', []) == [] and op.get('media', []) == []
    assert set(op).issubset({'id', 'actor', 'reason', 'dependencyReviewVersion', 'changes', 'media'})
    api = op['changes'][0]
    assert api['id'] == 'F-P-0532-source_assessment-widow-chain' and api['expectedVersion'] == 1
    assert source['package_amendment']['initial_native_operation_pin'] == prefix['operation_pin']
    pins = [auth['helper_pin'], auth['proven_utility_pin'], auth['package_pin'], auth['membership_pin'],
            auth['correction_operation_pin'], auth['correction_source_spec_pin'], auth['correction_mechanical_guard_pin'],
            auth['initial36_stage_handoff_pin'], prefix['operation_pin'], auth['protected42_pin'],
            first['all36_API_pin'], first['individual_request_pin'], *auth['review_pins'], *auth['media_pins']]

    def recheck(before=False):
        assert h.sha(ap) == args.authorization_sha256
        for pin in pins:
            h.checked_pin_path(pin)
        if before:
            h.checked_pin_path(auth['pre_correction_stage_DB_pin'])
        assert h.pin(M) == auth['main_pin']
        for role in ['primary_built_correction_gate', 'independent_built_correction_gate']:
            definition = auth[role]
            gate = h.readpin(definition['pin'])[1]
            assert h.pointer(gate, definition['ready_pointer']) is True
            assert h.pointer(gate, definition['package_pin_pointer']) == auth['package_pin']
            assert h.pointer(gate, definition['membership_pin_pointer']) == auth['membership_pin']
            assert h.pointer(gate, definition['operation_pin_pointer']) == auth['correction_operation_pin']
        assert auth['primary_built_correction_gate']['pin']['path'] != auth['independent_built_correction_gate']['pin']['path']

    recheck(True)
    db = h.checked_pin_path(auth['pre_correction_stage_DB_pin'])
    assert db.is_relative_to(R / 'evaluations/T-0788/exact36-stage-v1') and db.name == 'stage.sqlite'
    journal = db.parent / 'journal'
    snapshot = (R / auth['preservation_snapshot_path']).resolve()
    output = (R / auth['correction_output_path']).resolve()
    assert snapshot.parent == db.parent and snapshot != db and not snapshot.exists()
    assert output.is_relative_to(db.parent) and not output.exists()
    c, live = h.conn(db), h.conn(M)
    assert h.state(c) == {'journal_head': 450, 'pending': 27}
    assert h.state(live) == {'journal_head': 449, 'pending': 0}
    before, main_before = h.all50(c), h.all50(live)
    old = literal['whole_old_native']
    assert h.current(c, api['id']) == old['id'] and h.native(c, old['id']) == old
    assert not c.execute('select id from operation where id=?', (op['id'],)).fetchone()
    for edge in api['evidence']:
        assert h.current(c, edge['object']) == edge['object'] + '@' + str(edge['version'])
    protected = h.readpin(auth['protected42_pin'])[1]['objects']
    assert len(protected) == 42 and api['id'] not in [v['object_id'] for v in protected.values()]
    for rid, value in protected.items():
        assert h.current(c, value['object_id']) == rid and h.native(c, rid) == value
    prior_targets = h.readpin(first['all36_API_pin'])[1]['objects']
    assert len(prior_targets) == 36
    for rid, value in prior_targets.items():
        assert h.current(c, value['object_id']) == rid and h.native(c, rid) == value
    pending_sql = 'select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id'
    old_pending = [dict(v) for v in c.execute(pending_sql)]
    assert old_pending == [v['actual_request'] for v in h.readpin(first['individual_request_pin'])[1]['requests']]
    assert len(old_pending) == 27
    c.close()
    output.mkdir()
    step = {'operation_pin': correction['operation_pin'], 'before': {'journal_head': 450, 'pending': 27}}
    try:
        shutil.copyfile(db, snapshot)
        assert h.sha(snapshot) == auth['pre_correction_stage_DB_pin']['sha256']
        base = h.conn(snapshot)
        prefix_journal = {str(p.relative_to(journal)): h.sha(p) for p in journal.rglob('*') if p.is_file()}
        h.write(output / 'authorization-snapshot-before45027-v1.json', {'authorization_pin': h.pin(ap), 'snapshot_pin': h.pin(snapshot),
                'before_all50': before, 'main_all50': main_before, 'old_pending': old_pending, 'journal_prefix': prefix_journal})
        recheck(True)
        try:
            h.run_cli(['apply', str(op_path), '--db', str(db), '--journal', str(journal)], output / 'one-F0532-correction-actual-CLI-output.json')
        finally:
            c = h.conn(db)
            step['after'] = h.state(c)
            c.close()
            h.write(output / 'one-F0532-correction-actual-before-after-v1.json', step)
        c = h.conn(db)
        final = h.state(c)
        assert final['journal_head'] == 451 and final['pending'] >= 27
        stored = dict(c.execute('select * from operation_payload where operation_id=?', (op['id'],)).fetchone())
        assert json.loads(stored['request_json']) == op, 'Unexpected request representation; preserve and stop'
        after = h.all50(c)
        assert before['schema'] == after['schema']
        allowed = {'operation': 1, 'operation_payload': 1, 'revision': 1, 'fact': 1,
                   'origin': len(api['origins']), 'dependency': len(api['evidence'])}
        preserved = {}
        for name in before['tables']:
            if name in h.DERIVED:
                continue
            if name in allowed:
                assert after['tables'][name]['rows'] == before['tables'][name]['rows'] + allowed[name]
            elif name != 'review_request':
                assert before['tables'][name] == after['tables'][name], ('Unexpected table difference', name)
            sql = base.execute('select sql from sqlite_master where name=?', (name,)).fetchone()[0]
            if 'WITHOUT ROWID' in sql.upper():
                assert before['tables'][name] == after['tables'][name]
                preserved[name] = {'whole_table_exact': True}
            else:
                maximum = base.execute('select max(rowid) from "' + name + '"').fetchone()[0]
                prior = h.rows(base, name, True)
                got = h.rows(c, name, True, maximum) if maximum is not None else []
                assert got == prior, ('Old native row order/data changed', name)
                preserved[name] = {'old_order_exact': True, 'old_order_sha256': h.row_digest(prior, True)}
        old_search = [list(v) for v in base.execute('select object_id,kind,text from object_search order by object_id') if v['object_id'] != api['id']]
        new_search = [list(v) for v in c.execute('select object_id,kind,text from object_search order by object_id') if v['object_id'] != api['id']]
        assert old_search == new_search
        rid = api['id'] + '@2'
        actual = h.native(c, rid)
        assert h.current(c, api['id']) == rid and h.api(actual) == h.expected_defaults(api, h.api(actual))
        assert actual['data']['value_json'] == old['data']['value_json'], 'Structured raw JSON representation changed; stop'
        search_text = '\n'.join(str(v) for v in [api['id'], actual['disposition'], actual['evidence_status'], actual['rationale'], actual['caveat'], *actual['data'].values()] if v is not None)
        assert [list(v) for v in c.execute('select object_id,kind,text from object_search where object_id=?', (api['id'],))] == [[api['id'], api['kind'], search_text]]
        for protected_rid, value in protected.items():
            assert h.current(c, value['object_id']) == protected_rid and h.native(c, protected_rid) == value
        for target_rid, value in prior_targets.items():
            assert h.current(c, value['object_id']) == target_rid and h.native(c, target_rid) == value
        pool, units, documents, assets = {}, {}, {}, {}

        def add(capture):
            if capture in pool:
                return capture
            value = h.native(c, capture)
            pool[capture] = value
            for origin in value['origins']:
                unit = dict(c.execute('select * from unit where id=?', (origin['unit_id'],)).fetchone())
                units[unit['id']] = unit
                document = dict(c.execute('select * from document where path=?', (unit['document_path'],)).fetchone())
                documents[document['path']] = document
            for edge in value.get('assets', []):
                asset = dict(c.execute('select * from asset where path=?', (edge['asset_path'],)).fetchone())
                assets['asset:' + asset['path']] = asset
            for edge in value.get('media', []):
                asset = dict(c.execute('select * from native_asset where id=?', (edge['asset_id'],)).fetchone())
                assets['native:' + asset['id']] = asset
            for edge in value['evidence']:
                add(edge['basis_revision_id'])
            return capture

        pending = [dict(v) for v in c.execute(pending_sql)]
        assert len(pending) == final['pending']
        assert all(value in pending for value in old_pending), 'Prior pending requests changed or resolved'
        requests = []
        for value in pending:
            affected, changed = add(value['affected_revision_id']), add(value['changed_revision_id'])
            affected_current = add(h.current(c, pool[affected]['object_id']))
            changed_current = add(h.current(c, pool[changed]['object_id']))
            previous = pool[changed]['previous_id']
            if previous:
                add(previous)
            histories = {}
            for capture in [affected, changed]:
                oid = pool[capture]['object_id']
                histories[oid] = [v[0] for v in c.execute('select id from revision where object_id=? order by version', (oid,))]
                for historic in histories[oid]:
                    add(historic)
            requests.append({'actual_request': value, 'affected_exact_revision_id': affected, 'affected_current_revision_id': affected_current,
                             'changed_exact_revision_id': changed, 'changed_current_revision_id': changed_current,
                             'changed_previous_revision_id': previous, 'full_histories': histories,
                             'primary_independent_individual_grade': 'PENDING_RENEWED_ACTUAL_BINDING', 'automatic_rebind_or_resolution': False})
        targets = {**prior_targets, rid: actual}
        assert len(targets) == 37
        for capture in targets:
            add(capture)
        existing = {}
        for capture, value in pool.items():
            if base.execute('select id from revision where id=?', (capture,)).fetchone():
                assert h.native(base, capture) == value
                existing[capture] = value
        native_pin = h.write(output / 'complete-actual37-request-history-upstream-native-payloads-v1.json',
                             {'objects': pool, 'origin_units': units, 'documents': documents, 'asset_media_metadata': assets,
                              'ordered_native_arrays': 'Native rowid order; raw structured text and semantic arrays retained'})
        target_pin = h.write(output / 'all37-actual-native-and-single-F0532-API-binding-v1.json',
                             {'objects': targets, 'initial36_API_pin': first['all36_API_pin'], 'initial36_whole_native_unchanged': True,
                              'new_API': api, 'actual_new_API': h.api(actual), 'new_whole_API_equal': True})
        request_pin = h.write(output / 'all-actual-individual-requests-after-F0532-with-current-context-v1.json',
                              {'native_pin': native_pin, 'requests': requests, 'actual_pending_count': len(pending),
                               'old27_request_rows_unchanged': True, 'new_request_ids': [v['id'] for v in pending if v not in old_pending],
                               'full_dependency_subgraph': {capture: value['evidence'] for capture, value in pool.items()},
                               'resolutions_or_counts_inferred_from_old27': False})
        old_pin = h.write(output / 'all-old-native-context-exact-before450-v1.json', {'objects': existing, 'all_fields_and_order_equal': True})
        diff_pin = h.write(output / 'all50-before-after-old-row-order-protected-and-F0532-only-search-proof-v1.json',
                           {'before': before, 'after': after, 'old_rows_order_exact': preserved, 'exact_append_counts': allowed,
                            'review_request_increment': after['tables']['review_request']['rows'] - before['tables']['review_request']['rows'],
                            'derived_search_only_F0532_touched': True, 'protected42_exact': True, 'initial36_exact': True})
        stored_pin = h.write(output / 'whole-submitted-stored-correction-request-equality-v1.json', {'operation_pin': correction['operation_pin'], 'stored': stored, 'exact_request_JSON_order_equal': True})
        c.close()
        recheck(False)
        assert h.all50(live) == main_before and h.state(live) == {'journal_head': 449, 'pending': 0}
        for name, digest in prefix_journal.items():
            assert h.sha(journal / name) == digest
        handoff = h.write(output / 'complete-exact37-corrective-stage-actual-request-handoff-v1.json',
                          {'task': 'T-0788', 'authorization_pin': h.pin(ap), 'package_pin': auth['package_pin'], 'membership_pin': auth['membership_pin'],
                           'correction_operation_pin': correction['operation_pin'], 'initial36_stage_handoff_pin': auth['initial36_stage_handoff_pin'],
                           'preservation_snapshot_pin': h.pin(snapshot), 'actual_state': final, 'actual_step_state': step, 'stage_DB_pin': h.pin(db),
                           'all37_API_pin': target_pin, 'actual_native_context_pin': native_pin, 'individual_request_pin': request_pin,
                           'old_context_equality_pin': old_pin, 'all50_diff_pin': diff_pin, 'stored_correction_pin': stored_pin,
                           'main_physical_and_all50_unchanged': True, 'protected42_and_initial36_exact': True,
                           'resolutions_applied': 0, 'validators': [], 'final_six_checks': 'UNRUN_PENDING_INDIVIDUAL_ACTUAL_SOURCE_AND_INDEPENDENT_GRADES_AND_ROOT_AUTH',
                           'canonical_applied': False, 'usage': 'UNKNOWN pending root collector'})
        print(json.dumps({'handoff_pin': handoff, 'actual_state': final}))
        base.close()
    except BaseException as error:
        c = h.conn(db)
        actual_state = h.state(c)
        c.close()
        h.write(output / 'STOP-preserved-F0532-correction-failure-and-actual-state-v1.json',
                {'error': repr(error), 'traceback': traceback.format_exc(), 'actual_state': actual_state, 'stage_DB_pin': h.pin(db),
                 'main_pin': h.pin(M), 'step': step, 'no_retry_no_newclone_no_resolution_no_canonical': True})
        raise
    finally:
        live.close()


if __name__ == '__main__':
    main()
