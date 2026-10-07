"""Readonly F532 guard only; no operation construction or runtime mutation."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
s = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)
SOURCE = {'path': 'evaluations/T-0788/source-review/one-F0532-dated-preservation-caveat-full-API-and-exact37-union-amendment-v1.json', 'sha256': 'cfb446e27a862d9afc97a737dc1a7337e3af7f4d1e799554303f6d07e7a9c548'}
HANDOFF = {'path': 'evaluations/T-0788/exact36-stage-v1/complete-exact36-stage-result-and-Astra-handoff-v1.json', 'sha256': 'df43c415d24d0cca24c455c3a1b784238c37f486ab8fad5873eabfddaf4a4db7'}
MAIN = {'path': 'genealogy2/data/research.sqlite', 'sha256': '040e13c47dd6a01a3fa10f470b5685776f92de5c9214e1d5bdd399ba9ef414c7'}


def main():
    source = h.readpin(SOURCE)[1]
    handoff = h.readpin(HANDOFF)[1]
    assert len(source['rows']) == 1 and source['package_amendment']['native_target_union'] == 37
    assert source['package_amendment']['revision_count'] == 32 and source['package_amendment']['new_count'] == 5
    literal = source['rows'][0]
    old, api = literal['whole_old_native'], literal['full_old_API']
    assert literal['object_id'] == 'F-P-0532-source_assessment-widow-chain'
    projected = h.api(old)
    projected['expectedVersion'] = 1
    assert projected == api
    assert isinstance(old['data']['value_json'], str) and isinstance(api['data']['value_json'], dict)
    assert json.loads(old['data']['value_json']) == api['data']['value_json']
    new = copy.deepcopy(api)
    assert literal['evidence_rebinds'] == [] and len(literal['field_edits']) == 1
    edit = literal['field_edits'][0]
    assert edit['field'] == 'caveat' and new['caveat'] == edit['old']
    new['caveat'] = edit['new']
    assert [r['exact_old_edge'] for r in literal['old_evidence_dispositions']] == api['evidence']
    assert all(r['disposition'] == 'retain_exact_old_basis' for r in literal['old_evidence_dispositions'])
    assert len(api['evidence']) == 6 and len(literal['evidence_additions']) == 1
    for edge in literal['evidence_additions']:
        assert edge not in new['evidence']
        new['evidence'].append(copy.deepcopy(edge))
    assert new == literal['full_new_API']
    assert new['data'] == api['data'] and new['origins'] == api['origins']
    for pin in source['inputs']:
        h.checked_pin_path(pin)
    h.checked_pin_path(source['package_amendment']['initial_native_operation_pin'])
    h.checked_pin_path(source['package_amendment']['initial_proposal_pin'])
    prefix_op = h.readpin(source['package_amendment']['initial_native_operation_pin'])[1]
    targets = [v['id'] for v in prefix_op['changes']]
    assert len(targets) == len(set(targets)) == 36 and literal['object_id'] not in targets
    protected_pin = h.pin(R / 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json')
    protected = h.readpin(protected_pin)[1]['objects']
    assert len(protected) == 42 and literal['object_id'] not in [v['object_id'] for v in protected.values()]
    results, pool, issues = {}, {}, []
    expected_states = {'MAIN449': {'journal_head': 449, 'pending': 0}, 'STAGE450': {'journal_head': 450, 'pending': 27}}
    pins = {'MAIN449': MAIN, 'STAGE450': handoff['stage_DB_pin']}
    for label, pin in pins.items():
        c = h.conn(h.checked_pin_path(pin))
        assert h.state(c) == expected_states[label]
        rid = h.current(c, literal['object_id'])
        assert rid == literal['old_revision_id'] == old['id']
        actual = h.native(c, rid)
        assert actual == old
        actual_api = h.api(actual)
        actual_api['expectedVersion'] = 1
        assert actual_api == api
        columns = [dict(v) for v in c.execute('pragma table_info(fact)') if v['name'] != 'revision_id']
        assert set(new['data']).issubset({v['name'] for v in columns})
        assert all(new['data'].get(v['name']) is not None for v in columns if v['notnull'])
        support = []
        for index, edge in enumerate(new['evidence']):
            basis = edge['object'] + '@' + str(edge['version'])
            head = h.current(c, edge['object'])
            is_new_edge = index >= len(api['evidence'])
            present = c.execute('select id from revision where id=?', (basis,)).fetchone() is not None
            item = {'ordered_index': index, 'exact_API_edge': edge, 'actual_current_head': head,
                    'exact_requested_basis_present': present, 'requested_basis_is_current': basis == head,
                    'source_explicit_old_basis_retain': not is_new_edge, 'automatic_rebind': False}
            if label == 'MAIN449' and is_new_edge:
                producers = [v for v in prefix_op['changes'] if v['id'] == edge['object']]
                assert len(producers) == 1 and (producers[0]['expectedVersion'] or 0) + 1 == edge['version']
                item['explicit_preceding_T8_producer_pin'] = source['package_amendment']['initial_native_operation_pin']
                item['not_yet_main_canonical_requires_exact_preceding_operation'] = True
            elif not present or head != basis:
                issues.append({'database': label, 'ordered_edge': edge, 'current_head': head,
                               'requested_basis_present': present, 'source_question': 'Current-head mismatch; no substitution.'})
            for capture in [basis if present else None, head]:
                if capture is not None:
                    value = h.native(c, capture)
                    if capture in pool:
                        assert pool[capture] == value
                    pool[capture] = value
            support.append(item)
        incoming = []
        for edge in c.execute('select d.rowid as native_rowid,d.* from dependency d join revision r on r.id=d.basis_revision_id where r.object_id=? order by d.rowid', (literal['object_id'],)):
            item = dict(edge)
            caller_oid = c.execute('select object_id from revision where id=?', (edge['revision_id'],)).fetchone()[0]
            current = h.current(c, caller_oid)
            item.update({'basis_is_current': edge['basis_revision_id'] == rid,
                         'caller_current_revision_id': current, 'caller_is_current': current == edge['revision_id'],
                         'individual_source_disposition': 'PENDING_ASTRA_NO_AUTOMATIC_RETAIN_REBIND'})
            incoming.append(item)
            for caller in [edge['revision_id'], current]:
                value = h.native(c, caller)
                if caller in pool:
                    assert pool[caller] == value
                pool[caller] = value
        for protected_rid, value in protected.items():
            assert h.current(c, value['object_id']) == protected_rid and h.native(c, protected_rid) == value
        results[label] = {'database_pin': pin, 'actual_state': h.state(c), 'current_revision_id': rid,
                          'whole_old_native': actual, 'whole_old_API': actual_api,
                          'schema_pass': True, 'ordered_support_heads': support,
                          'all_history_incoming': incoming, 'all_history_incoming_count': len(incoming),
                          'current_incoming_count': sum(v['caller_is_current'] for v in incoming),
                          'protected42_whole_current_exact': True}
        c.close()
        h.checked_pin_path(pin)
    for pin in source['inputs']:
        h.checked_pin_path(pin)
    result = {'task': 'T-0788', 'source_spec_pin': SOURCE, 'source_row_pointer': '/rows/0',
              'first36_stage_handoff_pin': HANDOFF, 'helper_pin': h.pin(Path(__file__).resolve()),
              'guard_status': 'EXACT_F532_MAIN449_STAGE450_GUARDS_PASS' if not issues else 'SOURCE_SUPPORT_QUESTIONS_RETURNED',
              'databases': results, 'full_current_exact_support_and_incoming_caller_native': pool,
              'full_source_disposition': literal, 'source_new_API_verified_NOT_OPERATION': new,
              'exact_decoded_JSON_API_projection': True, 'native_raw_structured_text_preserved': old['data']['value_json'],
              'old6_evidence_order_role_note_basis_retained': True,
              'only_caveat_and_explicit_one_context_edge_changed': True,
              'initial36_operation_and_proposal_unchanged_pins': source['package_amendment'],
              'counts': {'target_union': 37, 'revisions': 32, 'creates': 5, 'media': 1, 'additional_target': 1},
              'protected42_pin': protected_pin, 'protected_target_intersection': [], 'support_head_issues': issues,
              'source_grade_or_incoming_retains_inferred': False,
              'operations_constructed_or_stage_canonical_Wotan_mutated': False,
              'usage': 'UNKNOWN pending root collector'}
    pin = h.write(Path(__file__).resolve().parent / 'one-F0532-exact-old-API-main449-stage450-support-head-and-full-incoming-guard-v1.json', result)
    print(json.dumps({'guard_pin': pin, 'incoming': {k: v['all_history_incoming_count'] for k, v in results.items()},
                      'support_head_issues': issues, 'counts': result['counts']}))


if __name__ == '__main__':
    main()
