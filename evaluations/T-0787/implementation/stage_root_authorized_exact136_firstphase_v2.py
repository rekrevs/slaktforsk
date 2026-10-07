"""UNRUN exact136 first-phase clone apply/capture. Requires exact root authorization.

No canonical/resolution writes. All stage mutation uses the controlled CLI once.
"""
import argparse
import copy
import importlib.util
import json
import shutil
import traceback
from pathlib import Path

R = Path(__file__).resolve().parents[3]
M = R / 'genealogy2/data/research.sqlite'
HELPER = R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py'
s = importlib.util.spec_from_file_location('h', HELPER)
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--authorization', type=Path, required=True)
    parser.add_argument('--authorization-sha256', required=True)
    parser.add_argument('--helper-sha256', required=True)
    args = parser.parse_args()
    ap = args.authorization.resolve()
    assert ap.is_relative_to(R) and h.sha(ap) == args.authorization_sha256
    assert h.sha(Path(__file__).resolve()) == args.helper_sha256
    raw_authorization = json.loads(ap.read_text())
    assert raw_authorization['task'] == 'T-0787'
    assert raw_authorization['phase'] == 'clone-first-apply-and-capture-actual-requests'
    assert raw_authorization['root_authorized'] is True
    assert all(raw_authorization[k] is False for k in ['runtime_resolution_authorized', 'canonical_authorized', 'database_replacement_authorized', 'retry_authorized'])
    assert raw_authorization['baseline_state'] == {'journal_head': 447, 'pending': 0}
    assert (raw_authorization['target_count'], raw_authorization['revision_count'], raw_authorization['create_count'], raw_authorization['media_count']) == (136, 130, 6, 1)
    assert raw_authorization['actual_request_count_not_inferred_from94_inputs'] is True
    # Explicit interface adapter only: all source/package/API values stay literal.
    _, package = h.readpin(raw_authorization['package_pin'])
    assert package['operations'][0]['operation_pin'] == raw_authorization['operation_pin']
    gate = lambda pin, package_pointer: {'pin': pin, 'ready_pointer': '/source_ready_for_root_authorized_stage',
            'proposal_pin_pointer': package_pointer, 'membership_pin_pointer': '/membership_pin', 'operation_pin_pointer': '/operation_pin'}
    auth = {'authorization': 'ONE_FRESH_EXACT136_ONE_OPERATION_CLONE_STAGE_ONLY', 'root_authorized': True,
            'canonical_apply_authorized': False, 'resolution_apply_authorized': False,
            'helper_pin': {'path': str(Path(__file__).resolve().relative_to(R)), 'sha256': args.helper_sha256},
            'proven_utility_pin': {'path': str(HELPER.relative_to(R)), 'sha256': 'e36e60ec42a99e5b0dc428ad0666210e59ba76b4ead438f18d89ab42e2f788d6'},
            'proposal_pin': raw_authorization['package_pin'], 'membership_pin': package['membership_pin'],
            'main_pin': raw_authorization['main_baseline_pin'], 'baseline_pin': raw_authorization['baseline_DB_pin'],
            'fresh_baseline_receipt_pin': h.pin(ap),
            'protected42_pin': h.pin(R / 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json'),
            'primary_gate': gate(raw_authorization['primary_gate_pin'], '/proposal_pin'),
            'independent_prestage_gate': gate(raw_authorization['independent_gate_pin'], '/package_pin'),
            'review_pins': raw_authorization['source_code_pins'],
            'media_pins': [{'path': 'evaluations/T-0787/postlogin-originals/00205124_00259.jpg', 'sha256': 'bded3192fc353a3be6114e0c12ff4de05e4feed99f669053e7dc69dd0659db96'}],
            'stage_path': raw_authorization['stage_output_root']}
    assert auth['authorization'] == 'ONE_FRESH_EXACT136_ONE_OPERATION_CLONE_STAGE_ONLY'
    assert auth['root_authorized'] is True
    assert auth['canonical_apply_authorized'] is False and auth['resolution_apply_authorized'] is False
    assert auth['helper_pin'] == h.pin(Path(__file__).resolve())
    assert auth['proven_utility_pin'] == h.pin(HELPER)
    pp, proposal = h.readpin(auth['proposal_pin'])
    mp, membership = h.readpin(auth['membership_pin'])
    assert proposal['membership_pin'] == auth['membership_pin']
    assert proposal['operations'] == membership['operations'] and proposal['operation_count'] == membership['operation_count'] == 1
    assert proposal['target_count'] == membership['target_count'] == 136
    assert proposal['existing_revisions'] == membership['revision_count'] == 130
    assert proposal['new_objects'] == membership['create_count'] == 6
    assert proposal['media_count'] == membership['media_count'] == 1
    member = membership['operations'][0]
    op_path, op = h.readpin(member['operation_pin'])
    assert op['id'] == member['operation_id'] and op['dependencyReviewVersion'] == 2
    assert set(op) == {'id', 'actor', 'reason', 'dependencyReviewVersion', 'media', 'changes'}
    assert len(op['changes']) == 136 and len(op['media']) == 1
    ids = [x['id'] for x in op['changes']]
    assert ids == member['target_ids'] and len(set(ids)) == 136
    _, consequence = h.readpin(proposal['consequence_table_pin'])
    assert [r['full_new_API'] for r in consequence['rows']] == op['changes']
    assert consequence['media_registration_API'] == op['media'][0]
    source_pins = proposal['source_module_pins'] + proposal['individual_incoming_and_amendment_pins']
    mandatory_pins = [auth['helper_pin'], auth['proven_utility_pin'], auth['proposal_pin'], auth['membership_pin'],
                      member['operation_pin'], proposal['source_bundle_pin'], proposal['composition_pin'],
                      proposal['consequence_table_pin'], proposal['mechanical_guard_pin'], auth['baseline_pin'],
                      auth['fresh_baseline_receipt_pin'], auth['protected42_pin'], *source_pins,
                      *auth['review_pins'], *auth['media_pins']]
    def gates():
        for role in ['primary_gate', 'independent_prestage_gate']:
            definition = auth[role]
            _, g = h.readpin(definition['pin'])
            assert h.pointer(g, definition['ready_pointer']) is True
            assert h.pointer(g, definition['proposal_pin_pointer']) == auth['proposal_pin']
            assert h.pointer(g, definition['membership_pin_pointer']) == auth['membership_pin']
            assert h.pointer(g, definition['operation_pin_pointer']) == member['operation_pin']
        assert auth['primary_gate']['pin']['path'] != auth['independent_prestage_gate']['pin']['path']
    def recheck_pins():
        assert h.sha(ap) == args.authorization_sha256
        for pin in mandatory_pins:
            h.checked_pin_path(pin)
        assert h.pin(M) == auth['main_pin']
        gates()
    recheck_pins()
    base_path = h.checked_pin_path(auth['baseline_pin'])
    assert base_path.is_relative_to(R / 'evaluations/T-0787')
    base, live = h.conn(base_path), h.conn(M)
    before = h.all50(base)
    assert h.all50(live) == before and h.state(base) == h.state(live) == {'journal_head': 447, 'pending': 0}
    _, protected_input = h.readpin(auth['protected42_pin'])
    protected = protected_input['objects']
    assert len(protected) == 42
    for rid, n in protected.items():
        assert h.current(base, n['object_id']) == h.current(live, n['object_id']) == rid
        assert h.native(base, rid) == h.native(live, rid) == n
        assert n['object_id'] not in ids
    assert not base.execute('select id from operation where id=?', (op['id'],)).fetchone()
    heads = dict(base.execute('select object_id,max(version) from revision group by object_id'))
    for x, row in zip(op['changes'], consequence['rows']):
        assert heads.get(x['id']) == x['expectedVersion']
        if row['full_old_native']:
            assert h.native(base, row['old_revision_id']) == row['full_old_native']
        else:
            assert not base.execute('select id from object where id=?', (x['id'],)).fetchone()
        for edge in x['evidence']:
            assert heads.get(edge['object']) == edge['version'], (x['id'], edge)
        heads[x['id']] = (x['expectedVersion'] or 0) + 1
    for x in op['changes']:
        for edge in x['evidence']:
            assert heads[edge['object']] == edge['version']
    media = op['media'][0]
    assert h.sha(R / media['storagePath']) == media['sha256'] and (R / media['storagePath']).stat().st_size == media['bytes']
    assert not base.execute('select id from native_asset where id=?', (media['id'],)).fetchone()
    stage = (R / auth['stage_path']).resolve()
    assert stage.is_relative_to(R / 'evaluations/T-0787') and not stage.exists() and stage != base_path
    stage.mkdir()
    db, journal = stage / 'stage.sqlite', stage / 'journal'
    steps = []
    try:
        shutil.copyfile(base_path, db)
        assert h.sha(db) == auth['baseline_pin']['sha256']
        shutil.copytree(R / 'genealogy2/journal', journal)
        journal_prefix = {str(p.relative_to(journal)): h.sha(p) for p in journal.rglob('*') if p.is_file()}
        h.write(stage / 'authorization-and-baseline-v1.json', {'authorization_pin': h.pin(ap), 'raw_authorization': raw_authorization, 'explicit_interface_adapter': auth,
                'baseline_all50': before, 'before': h.state(base), 'journal_prefix': journal_prefix})
        recheck_pins()
        c = h.conn(db)
        prior = h.state(c)
        assert prior == {'journal_head': 447, 'pending': 0}
        c.close()
        step = {'step': 1, 'operation_id': op['id'], 'operation_pin': member['operation_pin'], 'before': prior}
        h.write(stage / 'step-01-actual-before-v1.json', step)
        try:
            h.run_cli(['apply', str(op_path), '--db', str(db), '--journal', str(journal)], stage / 'step-01-actual-CLI-output.json')
        finally:
            c = h.conn(db)
            step['after'] = h.state(c)
            c.close()
            h.write(stage / 'step-01-actual-before-after-v1.json', step)
        steps.append(step)
        c = h.conn(db)
        final = h.state(c)
        assert final['journal_head'] == 448 and final['pending'] >= 0
        stored = dict(c.execute('select * from operation_payload where operation_id=?', (op['id'],)).fetchone())
        assert json.loads(stored['request_json']) == op, 'Stored operation normalization difference; stop, no rewrite'
        stored_pin = h.write(stage / 'entire-submitted-and-stored-exact-operation-v1.json', {'operation_pin': member['operation_pin'], 'stored': stored, 'exact_JSON_and_array_order_equal': True})
        for name, digest in journal_prefix.items():
            assert h.sha(journal / name) == digest
        after = h.all50(c)
        assert before['schema'] == after['schema']
        allowed = {'operation', 'operation_payload', 'object', 'revision', 'origin', 'dependency', 'review_request', 'native_asset', 'record_asset', 'record_media', *[x['kind'] for x in op['changes']]}
        preserved = {}
        for name in before['tables']:
            if name in h.DERIVED:
                continue
            if name not in allowed:
                assert before['tables'][name] == after['tables'][name], ('Unexpected table difference', name)
            sql = base.execute('select sql from sqlite_master where name=?', (name,)).fetchone()[0]
            if 'WITHOUT ROWID' in sql.upper():
                assert before['tables'][name] == after['tables'][name]
                preserved[name] = {'whole_table_exact': True}
                continue
            old = h.rows(base, name, True)
            maximum = base.execute('select max(rowid) from "' + name + '"').fetchone()[0]
            got = h.rows(c, name, True, maximum) if maximum is not None else []
            assert old == got, ('Old rows/order changed', name)
            preserved[name] = {'old_rowid_rows_exact': True, 'old_order_sha256': h.row_digest(old, True)}
        expected_counts = {'operation': 1, 'operation_payload': 1, 'object': 6, 'revision': 136, 'native_asset': 1,
                           'origin': sum(len(x['origins']) for x in op['changes']),
                           'record_asset': sum(len(x.get('assets', [])) for x in op['changes']),
                           'record_media': sum(len(x.get('media', [])) for x in op['changes'])}
        for x in op['changes']:
            expected_counts[x['kind']] = expected_counts.get(x['kind'], 0) + 1
        for name, increment in expected_counts.items():
            assert after['tables'][name]['rows'] == before['tables'][name]['rows'] + increment, (name, increment)
        assert h.rows(c, 'review_resolution', True) == h.rows(base, 'review_resolution', True)
        unchanged_search_before = [list(r) for r in base.execute('select object_id,kind,text from object_search order by object_id') if r['object_id'] not in ids]
        unchanged_search_after = [list(r) for r in c.execute('select object_id,kind,text from object_search order by object_id') if r['object_id'] not in ids]
        assert unchanged_search_before == unchanged_search_after
        pool, units, documents, assets = {}, {}, {}, {}
        def add(rid):
            if rid in pool:
                return rid
            n = h.native(c, rid)
            pool[rid] = n
            for origin in n['origins']:
                unit = dict(c.execute('select * from unit where id=?', (origin['unit_id'],)).fetchone())
                units[unit['id']] = unit
                document = dict(c.execute('select * from document where path=?', (unit['document_path'],)).fetchone())
                documents[document['path']] = document
            for edge in n.get('assets', []):
                value = dict(c.execute('select * from asset where path=?', (edge['asset_path'],)).fetchone())
                assets['asset:' + value['path']] = value
            for edge in n.get('media', []):
                value = dict(c.execute('select * from native_asset where id=?', (edge['asset_id'],)).fetchone())
                assets['native:' + value['id']] = value
            for edge in n['evidence']:
                add(edge['basis_revision_id'])
            return rid
        targets, target_proofs = {}, []
        for index, x in enumerate(op['changes']):
            rid = x['id'] + '@' + str((x['expectedVersion'] or 0) + 1)
            add(rid)
            targets[rid] = pool[rid]
            actual = h.api(pool[rid])
            expected = h.expected_defaults(x, actual)
            assert actual == expected, ('Full ordered API difference; stop', rid)
            history = [r[0] for r in c.execute('select id from revision where object_id=? order by version', (x['id'],))]
            for oldrid in history:
                add(oldrid)
            target_proofs.append({'revision_id': rid, 'input_pointer': '/changes/' + str(index), 'actual_API': actual,
                                  'approved_API': x, 'explicit_native_defaulted_expected_API': expected, 'whole_API_equal': True, 'history': history})
            n = pool[rid]
            expected_search = '\n'.join(str(v) for v in [x['id'], n['disposition'], n['evidence_status'], n['rationale'], n['caveat'], *n['data'].values()] if v is not None)
            assert [list(r) for r in c.execute('select object_id,kind,text from object_search where object_id=?', (x['id'],))] == [[x['id'], x['kind'], expected_search]]
        for rid, n in protected.items():
            assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
        pending = [dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')]
        assert len(pending) == final['pending']
        requests = []
        for q in pending:
            affected, changed = add(q['affected_revision_id']), add(q['changed_revision_id'])
            affected_current = add(h.current(c, pool[affected]['object_id']))
            changed_current = add(h.current(c, pool[changed]['object_id']))
            previous = pool[changed]['previous_id']
            if previous:
                add(previous)
            histories = {}
            for rid in [affected, changed]:
                histories[pool[rid]['object_id']] = [r[0] for r in c.execute('select id from revision where object_id=? order by version', (pool[rid]['object_id'],))]
                for oldrid in histories[pool[rid]['object_id']]:
                    add(oldrid)
            requests.append({'actual_request': q, 'affected_exact_revision_id': affected, 'affected_current_revision_id': affected_current,
                             'changed_exact_revision_id': changed, 'changed_current_revision_id': changed_current, 'changed_previous_revision_id': previous,
                             'full_histories': histories, 'primary_independent_individual_grade': 'PENDING', 'automatic_rebind_or_resolution': False})
        existing = {}
        for rid, n in pool.items():
            if base.execute('select id from revision where id=?', (rid,)).fetchone():
                assert n == h.native(base, rid)
                existing[rid] = n
        native_pin = h.write(stage / 'complete-actual-target-request-history-upstream-native-payloads-v1.json', {'objects': pool, 'origin_units': units, 'documents': documents, 'asset_media_metadata': assets, 'ordered_native_arrays': 'ORDER BY native rowid; all source data arrays preserved'})
        target_pin = h.write(stage / 'all136-actual-whole-native-and-ordered-API-bindings-v1.json', {'objects': targets, 'target_proofs': target_proofs, 'all136_complete': len(targets) == 136})
        requests_pin = h.write(stage / 'all-actual-individual-request-and-complete-dependency-context-v1.json', {'native_pin': native_pin, 'requests': requests, 'actual_pending_count': len(pending), 'full_dependency_subgraph': {rid: n['evidence'] for rid, n in pool.items()}, 'prior94_source_edges_are_not_actual_request_count_or_resolution_approval': True})
        old_pin = h.write(stage / 'all-old-current-support-history-whole-native-baseline-equality-v1.json', {'objects': existing, 'all_fields_and_native_array_order_equal': True})
        diff_pin = h.write(stage / 'all50-old-row-order-metadata-protected-and-derived-search-diff-v1.json', {'before': before, 'after': after, 'old_rows_preserved': preserved, 'authorized_append_tables': sorted(allowed), 'expected_known_row_count_increments': expected_counts, 'narrow_derived_search_touched_only_exact136': True, 'protected42_whole_current_exact': True})
        h.write(stage / 'protected42-after-v1.json', protected)
        h.write(stage / 'all-operation-payloads-v1.json', [dict(r) for r in c.execute('select * from operation_payload order by sequence')])
        c.close()
        validators = []
        # Root authorized first phase only: six final checks follow individual resolutions.
        recheck_pins()
        assert h.all50(live) == before
        c = h.conn(db)
        assert h.state(c) == final
        c.close()
        handoff = h.write(stage / 'complete-exact136-stage-result-and-Astra-handoff-v1.json', {'task': 'T-0787', 'authorization_pin': h.pin(ap),
                         'proposal_pin': auth['proposal_pin'], 'membership_pin': auth['membership_pin'], 'operation_pin': member['operation_pin'],
                         'actual_state': final, 'step_states': steps, 'actual_target_count': 136, 'new_media': 1, 'stored_operation_pin': stored_pin,
                         'actual_native_context_pin': native_pin, 'all136_API_pin': target_pin, 'individual_request_pin': requests_pin,
                         'old_context_baseline_equality_pin': old_pin, 'all50_diff_pin': diff_pin, 'stage_DB_pin': h.pin(db), 'validators': validators,
                         'protected42_exact': True, 'main_physical_and_all50_unchanged': True, 'resolutions_applied': 0,
                         'final_six_validators_status': 'UNRUN_PENDING_INDIVIDUAL_SOURCE_AND_INDEPENDENT_REQUEST_GRADES_AND_ROOT_PHASE_AUTH',
                         'actual_request_source_independent_grades_required': True, 'canonical_applied': False, 'program_acceptance': False,
                         'usage': 'UNKNOWN pending root collector'})
        print(json.dumps({'handoff_pin': handoff, 'actual_state': final}))
    except BaseException as error:
        state = None
        if db.exists():
            c = h.conn(db)
            state = h.state(c)
            c.close()
        h.write(stage / 'STOP-failure-and-actual-state-preserved-v1.json', {'error': repr(error), 'traceback': traceback.format_exc(),
                'actual_state': state, 'stage_DB_pin': h.pin(db) if db.exists() else None, 'main_pin': h.pin(M), 'steps': steps,
                'no_retry_no_newclone_no_resolutions': True})
        raise
    finally:
        base.close()
        live.close()


if __name__ == '__main__':
    main()
