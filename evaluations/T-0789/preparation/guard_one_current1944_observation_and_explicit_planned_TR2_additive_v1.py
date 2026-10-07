"""Readonly additive21 inputs; preserve prior20 and never fabricate T8 native."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
s = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)
PRIOR = {'path': 'evaluations/T-0789/preparation/exact20-readonly-full-old-absence-schema-planned-head-and-incoming-annual-routing-guard-v1.json', 'sha256': 'cd71e4614e422175bb05edc40b0f2c116a88b1323e6b355663402de07eb376fc'}
ENTRY = {'path': 'evaluations/T-0789/source-review/exact20-source-module-order-and-readonly-guard-request-v2.json', 'sha256': '752ba61ae8f471b20c5587a7fd4fb3c2357fa0ca1c1915b9ceb9925d01fd38cf'}
ADD = {'path': 'evaluations/T-0789/source-review/one-current1944-observation-annual-coverage-caveat-exact-spec-v1.json', 'sha256': '83ff7202667d6f40234600286a0ac893888264f1cd4aaeda4a8bb29a5fda47c1'}


def main():
    prior = h.readpin(PRIOR)[1]
    entry = h.readpin(ENTRY)[1]
    initial = h.readpin(prior['source_entrypoint_pin'])[1]
    assert entry['ordered_source_rows'] == initial['ordered_source_rows']
    assert entry['planned_T0788_heads'][:-1] == initial['planned_T0788_heads']
    additional_head = entry['planned_T0788_heads'][-1]
    assert additional_head == {'id': 'TR-81ff8a207c9e0e37f1c1aeed', 'version': 2}
    producer = h.readpin(prior['planned_T0788_exact_operation_pin'])[1]['changes'][1]
    assert producer['id'] == additional_head['id'] and producer['expectedVersion'] + 1 == additional_head['version']
    assert len(prior['sequential_support_head_issues']) == 1
    assert prior['sequential_support_head_issues'][0]['ordered_edge']['object'] == additional_head['id']
    assert prior['sequential_support_head_issues'][0]['ordered_edge']['version'] == additional_head['version']
    c = h.conn(h.checked_pin_path(prior['frozen449_baseline_pin']))
    assert h.state(c) == {'journal_head': 449, 'pending': 0}
    module = h.readpin(ADD)[1]
    assert len(module['rows']) == 1
    literal = module['rows'][0]
    oid = literal['object_id']
    rid = oid + '@' + str(literal['expected_version'])
    assert h.current(c, oid) == rid
    old = h.native(c, rid)
    assert old == literal['whole_old_native']
    old_api = h.api(old)
    old_api['expectedVersion'] = literal['expected_version']
    api = copy.deepcopy(old_api)
    for edit in literal['field_edits']:
        assert edit['field'] == 'caveat' and api['caveat'] == edit['old']
        api['caveat'] = edit['new']
    assert literal['evidence_rebinds'] == []
    for edge in literal['evidence_additions']:
        assert edge not in api['evidence']
        exact_producers = [row['source_new_API_projection_NOT_OPERATION'] for row in prior['rows'] if row['object_id'] == edge['object']]
        assert len(exact_producers) == 1 and exact_producers[0]['expectedVersion'] is None and edge['version'] == 1
        api['evidence'].append(copy.deepcopy(edge))
    assert api['data'] == old_api['data'] and api['origins'] == old_api['origins']
    assert api['evidence'][:len(old_api['evidence'])] == old_api['evidence']
    for edge in old_api['evidence']:
        assert h.current(c, edge['object']) == edge['object'] + '@' + str(edge['version'])
    full = {rid: old}
    added = []
    for edge in c.execute('select d.rowid as native_rowid,d.* from dependency d join revision r on r.id=d.basis_revision_id where r.object_id=? order by d.rowid', (oid,)):
        value = dict(edge)
        caller_oid = c.execute('select object_id from revision where id=?', (edge['revision_id'],)).fetchone()[0]
        current = h.current(c, caller_oid)
        value.update({'changed_target_object_id': oid, 'target_current_revision_id': rid,
                      'caller_current_revision_id': current, 'caller_is_current': current == edge['revision_id'],
                      'basis_is_current': edge['basis_revision_id'] == rid, 'source_disposition': 'PENDING_ASTRA'})
        added.append(value)
        for caller_rid in [edge['revision_id'], current]:
            full[caller_rid] = h.native(c, caller_rid)
    union = {row['native_rowid']: row for row in prior['all_history_incoming']}
    for row in added:
        assert row['native_rowid'] not in union
        union[row['native_rowid']] = row
    # This is an additive input table, not a final operation order.
    result = {'task': 'T-0789', 'prior20_guard_pin': PRIOR, 'explicit_planned_head_amendment_pin': ENTRY,
              'additional_source_spec_pin': ADD, 'frozen449_baseline_pin': prior['frozen449_baseline_pin'],
              'prior20_rows_all_unchanged_reused': True,
              'exact_one_planned_TR2_question_closed_by_source_declaration': additional_head,
              'planned_TR2_producer_pin': prior['planned_T0788_exact_operation_pin'], 'planned_TR2_producer_pointer': '/changes/1',
              'additional_row': {'object_id': oid, 'source_spec_pin': ADD, 'source_row_pointer': '/rows/0',
                                 'whole_source_row': literal, 'full_old_native': old, 'full_old_API': old_api,
                                 'source_new_API_projection_NOT_OPERATION': api},
              'additive_all_history_incoming': added, 'all21_target_history_incoming': list(union.values()),
              'additional_full_exact_and_current_caller_native': full,
              'remaining_support_head_issues': [],
              'pending_actual_T8_acceptance': 'RESEARCH@4 full native and declared T8 heads must be captured/reconciled after actual accepted T8; no synthetic current or native claim.',
              'counts': {'targets': 21, 'creates': 12, 'revisions': 9, 'actual449_whole_old_exact': 8,
                         'planned_T8_whole_native_pending': 1, 'media': 2, 'additional_incoming': len(added),
                         'incoming_unique': len(union)},
              'final_source_order_not_inferred_from_additive_table': True, 'source_grades_inferred': False,
              'build_stage_canonical_Wotan_authorized': False, 'usage': 'UNKNOWN pending root collector'}
    h.checked_pin_path(prior['frozen449_baseline_pin'])
    pin = h.write(Path(__file__).resolve().parent / 'exact21-additive-current1944-observation-guard-and-planned-TR2-amendment-v1.json', result)
    c.close()
    print(json.dumps({'guard_pin': pin, 'counts': result['counts'], 'remaining_support_head_issues': []}))


if __name__ == '__main__':
    main()
