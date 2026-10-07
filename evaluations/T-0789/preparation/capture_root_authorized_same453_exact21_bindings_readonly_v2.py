"""UNRUN readonly capture after exact21 firstphase apply. No CLI/apply/clone.

Only two source-reviewed redundant input bindings are omitted from native API
projection, while the entire submitted/stored request stays exact and preserved.
The explicit context evidence P-0007@2 is the active current-head guard;
bindings.P-0007 itself is redundant and is not asserted an active identity guard.
"""
import argparse
import copy
import importlib.util
import json
import traceback
from pathlib import Path

R = Path(__file__).resolve().parents[3]
M = R / 'genealogy2/data/research.sqlite'
UTILITY = R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py'
s = importlib.util.spec_from_file_location('h', UTILITY)
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)
BINDING_IDS = {'ID-T0789-P0007-own-annual-1945', 'ID-T0789-P0007-own-annual-1946'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--authorization', type=Path, required=True)
    p.add_argument('--authorization-sha256', required=True)
    args = p.parse_args()
    ap = args.authorization.resolve()
    assert ap.is_relative_to(R) and h.sha(ap) == args.authorization_sha256
    raw_authorization = json.loads(ap.read_text())
    assert raw_authorization['task'] == 'T-0789'
    assert raw_authorization['action'] == 'READONLY_SAME453_EXACT21_BINDINGS_CONTINUATION_CAPTURE'
    assert raw_authorization['root_authorized'] is True
    assert raw_authorization['helper_pin'] == h.pin(Path(__file__).resolve())
    assert raw_authorization['CLI_apply_authorized'] is False
    assert raw_authorization['canonical_authorized'] is False
    assert raw_authorization['clone_or_retry_authorized'] is False
    assert raw_authorization['expected_actual_state'] == {'journal_head': 453, 'pending': 16}
    assert raw_authorization['explicit_input_only_bindings'] == {oid: {'P-0007': 2} for oid in BINDING_IDS}
    original = h.readpin(raw_authorization['original_stage_authorization_and_baseline_pin'])[1]
    original_auth = h.readpin(original['authorization_pin'])[1]
    auth = original['explicit_interface_adapter']
    failure = h.readpin(raw_authorization['preserved_STOP_pin'])[1]
    assert failure['actual_state'] == raw_authorization['expected_actual_state']
    assert failure['stage_DB_pin'] == raw_authorization['actual_stage_DB_pin']
    db = h.checked_pin_path(raw_authorization['actual_stage_DB_pin'])
    assert db == (R / original_auth['stage_output_root'] / 'stage.sqlite').resolve()
    assert h.pin(UTILITY) == auth['proven_utility_pin']
    _, proposal = h.readpin(auth['proposal_pin'])
    _, membership = h.readpin(auth['membership_pin'])
    assert proposal['operations'] == membership['operations'] and len(membership['operations']) == 1
    member = membership['operations'][0]
    _, op = h.readpin(member['operation_pin'])
    assert op['id'] == member['operation_id'] and op['dependencyReviewVersion'] == 2
    assert len(op['changes']) == 21 and len(op['media']) == 2
    ids = [x['id'] for x in op['changes']]
    assert ids == member['target_ids'] and len(set(ids)) == 21
    assert {x['id'] for x in op['changes'] if 'bindings' in x} == BINDING_IDS
    steps = [h.readpin(raw_authorization['step_before_after_pin'])[1]]
    assert steps[0]['after'] == raw_authorization['expected_actual_state']
    mandatory_pins = [raw_authorization['helper_pin'], raw_authorization['actual_stage_DB_pin'],
                      raw_authorization['preserved_STOP_pin'], raw_authorization['original_stage_authorization_and_baseline_pin'],
                      raw_authorization['step_before_after_pin'], original['authorization_pin'],
                      auth['proposal_pin'], auth['membership_pin'], member['operation_pin'], auth['baseline_pin'], auth['main_pin'],
                      auth['protected42_pin'], auth['proven_utility_pin'], *auth['review_pins'], *auth['media_pins']]
    assert set(raw_authorization['representation_dispositions']) == {'primary', 'independent'}
    for role in ['primary', 'independent']:
        definition = raw_authorization['representation_dispositions'][role]
        value = h.readpin(definition['pin'])[1]
        assert h.pointer(value, definition['pointer']) == definition['accepted_value']
        mandatory_pins.append(definition['pin'])
    def recheck_pins():
        assert h.sha(ap) == args.authorization_sha256
        for pin in mandatory_pins:
            h.checked_pin_path(pin)
        assert h.pin(M) == auth['main_pin']
    recheck_pins()
    base, live = h.conn(h.checked_pin_path(auth['baseline_pin'])), h.conn(M)
    before = h.all50(base)
    assert before == original['baseline_all50'] == h.all50(live)
    assert h.state(base) == h.state(live) == {'journal_head': 452, 'pending': 0}
    protected = h.readpin(auth['protected42_pin'])[1]['objects']
    assert len(protected) == 42 and not set(ids).intersection(n['object_id'] for n in protected.values())
    for rid, n in protected.items():
        assert h.current(base, n['object_id']) == h.current(live, n['object_id']) == rid
        assert h.native(base, rid) == h.native(live, rid) == n
    journal = db.parent / 'journal'
    journal_prefix = original['journal_prefix']
    stage = (R / raw_authorization['output_directory']).resolve()
    assert stage.parent == db.parent and not stage.exists()
    stage.mkdir()
    projection_differences = []
    try:
        c = h.conn(db)
        final = h.state(c)
        assert final['journal_head'] == 453 and final['pending'] >= 0
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
        expected_counts = {'operation': 1, 'operation_payload': 1, 'object': 12, 'revision': 21, 'native_asset': 2,
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
            operational_bindings = expected.get('bindings')
            if x['id'] in BINDING_IDS:
                assert x['kind'] == 'identity' and operational_bindings == {'P-0007': 2}
                assert x['data']['person_id'] == 'P-0007'
                assert 'bindings' not in actual
                assert h.current(base, 'P-0007') == h.current(c, 'P-0007') == 'P-0007@2'
                assert h.native(base, 'P-0007@2') == h.native(c, 'P-0007@2')
                person_edges = [e for e in x['evidence'] if e['object'] == 'P-0007']
                assert len(person_edges) == 1 and person_edges[0]['version'] == 2
                projection_differences.append({'revision_id': rid, 'pointer': '/bindings',
                    'submitted_present': True, 'submitted_literal': copy.deepcopy(operational_bindings),
                    'native_API_present': False, 'native_current_person_revision_id': 'P-0007@2',
                    'active_current_head_guard': 'explicit ordered evidence P-0007@2',
                    'bindings_person_key_is_active_guard': False,
                    'ordered_explicit_person_evidence': person_edges,
                    'stored_request_retains_bindings_exact': True})
                del expected['bindings']  # Only two root/source-reviewed redundant request inputs; active guard is evidence.
            else:
                assert operational_bindings is None
            assert actual == expected, ('Full ordered API difference beyond explicit two input-only bindings; stop', rid)
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
        assert len(projection_differences) == 2
        projection_pin = h.write(stage / 'exact-two-operational-bindings-and-native-projection-proof-v1.json', {'operation_pin': member['operation_pin'], 'differences': projection_differences, 'raw_stored_request_exact': True, 'all_other_ordered_API_fields_exact': True, 'representation_dispositions': raw_authorization['representation_dispositions']})
        target_pin = h.write(stage / 'all21-actual-whole-native-and-ordered-API-bindings-v1.json', {'objects': targets, 'target_proofs': target_proofs, 'all21_complete': len(targets) == 21})
        requests_pin = h.write(stage / 'all-actual-individual-request-and-complete-dependency-context-v1.json', {'native_pin': native_pin, 'requests': requests, 'actual_pending_count': len(pending), 'full_dependency_subgraph': {rid: n['evidence'] for rid, n in pool.items()}, 'prior5_source_edges_are_not_actual_request_count_or_resolution_approval': True})
        old_pin = h.write(stage / 'all-old-current-support-history-whole-native-baseline-equality-v1.json', {'objects': existing, 'all_fields_and_native_array_order_equal': True})
        diff_pin = h.write(stage / 'all50-old-row-order-metadata-protected-and-derived-search-diff-v1.json', {'before': before, 'after': after, 'old_rows_preserved': preserved, 'authorized_append_tables': sorted(allowed), 'expected_known_row_count_increments': expected_counts, 'narrow_derived_search_touched_only_exact21': True, 'protected42_whole_current_exact': True})
        h.write(stage / 'protected42-after-v1.json', protected)
        h.write(stage / 'all-operation-payloads-v1.json', [dict(r) for r in c.execute('select * from operation_payload order by sequence')])
        c.close()
        validators = []
        # Root authorized first phase only: six final checks follow individual resolutions.
        recheck_pins()
        assert h.all50(live) == before
        c = h.conn(db)
        assert h.state(c) == final and h.pin(db) == raw_authorization['actual_stage_DB_pin']
        c.close()
        handoff = h.write(stage / 'complete-exact21-stage-result-and-Astra-handoff-v1.json', {'task': 'T-0789', 'authorization_pin': h.pin(ap), 'original_firstphase_authorization_pin': original['authorization_pin'], 'preserved_STOP_pin': raw_authorization['preserved_STOP_pin'], 'input_binding_projection_proof_pin': projection_pin,
                         'proposal_pin': auth['proposal_pin'], 'membership_pin': auth['membership_pin'], 'operation_pin': member['operation_pin'],
                         'actual_state': final, 'step_states': steps, 'actual_target_count': 21, 'new_media': 2, 'stored_operation_pin': stored_pin,
                         'actual_native_context_pin': native_pin, 'all21_API_pin': target_pin, 'individual_request_pin': requests_pin,
                         'old_context_baseline_equality_pin': old_pin, 'all50_diff_pin': diff_pin, 'stage_DB_pin': h.pin(db), 'validators': validators,
                         'protected42_exact': True, 'main_physical_and_all50_unchanged': True, 'readonly_continuation_only_no_CLI': True, 'resolutions_applied': 0,
                         'final_six_validators_status': 'UNRUN_PENDING_INDIVIDUAL_SOURCE_AND_INDEPENDENT_REQUEST_GRADES_AND_ROOT_PHASE_AUTH',
                         'actual_request_source_independent_grades_required': True, 'canonical_applied': False, 'program_acceptance': False,
                         'usage': 'UNKNOWN pending root collector'})
        print(json.dumps({'handoff_pin': handoff, 'actual_state': final}))
    except BaseException as error:
        actual = h.conn(db)
        try:
            h.write(stage / 'STOP-readonly-continuation-and-actual-state-preserved-v1.json', {
                'error': repr(error), 'traceback': traceback.format_exc(), 'actual_state': h.state(actual),
                'stage_DB_pin': h.pin(db), 'main_pin': h.pin(M), 'no_apply_clone_or_retry': True})
        finally:
            actual.close()
        raise
    finally:
        base.close()
        live.close()


if __name__ == '__main__':
    main()
