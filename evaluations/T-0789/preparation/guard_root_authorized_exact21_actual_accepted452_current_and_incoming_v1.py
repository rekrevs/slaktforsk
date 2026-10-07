"""UNRUN: readonly actual accepted T8/main452 reconciliation for exact T9 inputs.

Requires a separate root readonly authorization; never builds operations or applies.
"""
import argparse
import copy
import importlib.util
import json
import traceback
from pathlib import Path

R = Path(__file__).resolve().parents[3]
UTILITY = R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py'
s = importlib.util.spec_from_file_location('h', UTILITY)
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)
SOURCE = {'path': 'evaluations/T-0789/source-review/complete-exact21-annual-source-union-order-and-conditional-current-reconciliation-v1.json', 'sha256': 'e0e62a6c40b70d548aa221aa203bd84724dcd92a672af7d571da52b59ed32b48'}
OWN = {'path': 'evaluations/T-0789/independent-review/conditional21-source-union-order-and-own-prior-meaning-binding-v1.json', 'sha256': '6c043fa20fa782c222e335f98bb7015fa2cdba0f85f5fd084e47a5727ca5aec2'}
PRIOR20 = {'path': 'evaluations/T-0789/preparation/exact20-readonly-full-old-absence-schema-planned-head-and-incoming-annual-routing-guard-v1.json', 'sha256': 'cd71e4614e422175bb05edc40b0f2c116a88b1323e6b355663402de07eb376fc'}
PRIOR21 = {'path': 'evaluations/T-0789/preparation/exact21-additive-current1944-observation-guard-and-planned-TR2-amendment-v1.json', 'sha256': 'dff301a30c388885eccba75828d11d39d7ec2f5022951076072de3625e0ac27e'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--authorization', type=Path, required=True)
    parser.add_argument('--authorization-sha256', required=True)
    args = parser.parse_args()
    ap = args.authorization.resolve()
    assert ap.is_relative_to(R) and h.sha(ap) == args.authorization_sha256
    auth = json.loads(ap.read_text())
    assert auth['authorization'] == 'ACTUAL_ACCEPTED452_EXACT21_READONLY_GUARDS_ONLY'
    assert auth['root_authorized'] is True
    assert all(auth[k] is False for k in ['operation_build_authorized', 'stage_authorized', 'canonical_authorized'])
    assert auth['helper_pin'] == h.pin(Path(__file__).resolve()) and auth['proven_utility_pin'] == h.pin(UTILITY)
    assert auth['source_union_pin'] == SOURCE and auth['independent_union_pin'] == OWN
    cache = {}

    def load(pin):
        key = (pin['path'], pin['sha256'])
        assert not any(path == key[0] and digest != key[1] for path, digest in cache)
        if key not in cache:
            cache[key] = h.readpin(pin)[1]
        return cache[key]

    accepted = load(auth['accepted_T8_root_receipt_pin'])
    assert h.pointer(accepted, auth['accepted_T8_ready_pointer']) is True
    assert h.pointer(accepted, auth['accepted_T8_main_pin_pointer']) == auth['main_pin']
    assert h.pointer(accepted, auth['accepted_T8_state_pointer']) == {'journal_head': 452, 'pending': 0}
    reviewed = load(auth['reviewed_final_T8_stage_handoff_pin'])
    assert reviewed['actual_state'] == {'journal_head': 452, 'pending': 0}
    c = h.conn(h.checked_pin_path(auth['main_pin']))
    assert h.state(c) == {'journal_head': 452, 'pending': 0}
    out = (R / auth['output_path']).resolve()
    assert out.is_relative_to(R / 'evaluations/T-0789/preparation') and not out.exists()
    out.mkdir()
    try:
        source, own = load(SOURCE), load(OWN)
        assert own['union_order_source_meaning_ready'] is True and own['ready_for_build'] is False
        initial20, initial21 = load(PRIOR20), load(PRIOR21)
        old_inputs = {row['object_id']: row for row in initial20['rows'] if row['full_actual_old_native'] is not None}
        old_inputs[initial21['additional_row']['object_id']] = {'full_actual_old_native': initial21['additional_row']['full_old_native']}
        assert len(old_inputs) == 8
        corrected_T8 = load(reviewed['native_prefix_stage_handoff_pin'])
        all37 = load(corrected_T8['all37_API_pin'])['objects']
        initial_T8_op = load(source['planned_head_amendment']['producer_operation_pin'])
        producers = {api['id']: api for api in initial_T8_op['changes']}
        current_T8_heads = []
        pool, units, documents, assets = {}, {}, {}, {}

        def add(rid):
            if rid in pool:
                return rid
            native = h.native(c, rid)
            pool[rid] = native
            for origin in native['origins']:
                unit = dict(c.execute('select * from unit where id=?', (origin['unit_id'],)).fetchone())
                units[unit['id']] = unit
                document = dict(c.execute('select * from document where path=?', (unit['document_path'],)).fetchone())
                documents[document['path']] = document
            for edge in native.get('assets', []):
                asset = dict(c.execute('select * from asset where path=?', (edge['asset_path'],)).fetchone())
                assets['asset:' + asset['path']] = asset
            for edge in native.get('media', []):
                asset = dict(c.execute('select * from native_asset where id=?', (edge['asset_id'],)).fetchone())
                assets['native:' + asset['id']] = asset
            for edge in native['evidence']:
                add(edge['basis_revision_id'])
            return rid

        for item in source['planned_T0788_heads']:
            rid = item['id'] + '@' + str(item['version'])
            assert h.current(c, item['id']) == rid
            add(rid)
            assert pool[rid] == all37[rid]
            current_T8_heads.append({'object_id': item['id'], 'actual_current_revision_id': rid,
                                     'full_actual_native_pointer': '/objects/' + rid,
                                     'reviewed_T8_full_native_equal': True})
        rows, incoming, issues = [], {}, []
        heads = dict(c.execute('select object_id,max(version) from revision group by object_id'))
        original_heads = dict(heads)
        for index, selector in enumerate(source['ordered_source_rows']):
            literal = h.pointer(load(selector['source_pin']), selector['source_pointer'])
            oid = selector['object_id']
            old_native, old_api, rid = None, None, None
            if 'full_new_API' in literal:
                api = copy.deepcopy(literal['full_new_API'])
                assert api['id'] == oid and api['expectedVersion'] is None
                assert not c.execute('select id from object where id=?', (oid,)).fetchone()
            else:
                rid = oid + '@' + str(selector['expected_version'])
                assert h.current(c, oid) == rid
                add(rid)
                old_native = pool[rid]
                old_api = h.api(old_native)
                old_api['expectedVersion'] = selector['expected_version']
                if selector.get('actual_T0788_successor_required', False):
                    assert rid == 'RESEARCH-P-0007-9d76f0343410@4'
                    assert old_native == all37[rid]
                    producer_API = h.api(old_native)
                    assert producer_API == h.expected_defaults(producers[oid], producer_API)
                    assert h.pointer(load(literal['expected_producer_source_pin']), literal['expected_producer_pointer'])['object_id'] == oid
                else:
                    assert old_native == literal['whole_old_native'] == old_inputs[oid]['full_actual_old_native']
                api = copy.deepcopy(old_api)
                for edit in literal['field_edits']:
                    keys, cursor = edit['field'].split('.'), api
                    for key in keys[:-1]:
                        cursor = cursor[key]
                    assert cursor[keys[-1]] == edit['old'], ('Exact old field mismatch; no replacement', oid, edit['field'])
                    cursor[keys[-1]] = copy.deepcopy(edit['new'])
                for amendment in literal.get('evidence_rebinds', []):
                    positions = [i for i, edge in enumerate(api['evidence']) if edge == amendment['old']]
                    assert len(positions) == 1, ('Zero/multiple old edge matches', oid, amendment)
                    api['evidence'][positions[0]] = copy.deepcopy(amendment['new'])
                for edge in literal.get('evidence_additions', []):
                    assert edge not in api['evidence']
                    api['evidence'].append(copy.deepcopy(edge))
                histories = [v[0] for v in c.execute('select id from revision where object_id=? order by version', (oid,))]
                for historic in histories:
                    add(historic)
                for edge in c.execute('select d.rowid as native_rowid,d.* from dependency d join revision r on r.id=d.basis_revision_id where r.object_id=? order by d.rowid', (oid,)):
                    value = dict(edge)
                    caller_oid = c.execute('select object_id from revision where id=?', (edge['revision_id'],)).fetchone()[0]
                    caller_current = h.current(c, caller_oid)
                    value.update({'changed_target_object_id': oid, 'target_current_revision_id': rid,
                                  'caller_current_revision_id': caller_current, 'caller_is_current': caller_current == edge['revision_id'],
                                  'basis_is_current': edge['basis_revision_id'] == rid,
                                  'individual_source_disposition': 'PENDING_RENEWED_ASTRA_BINDING'})
                    incoming[edge['native_rowid']] = value
                    add(edge['revision_id'])
                    add(caller_current)
            assert api['id'] == oid and api['expectedVersion'] == selector['expected_version']
            columns = [dict(v) for v in c.execute('pragma table_info("' + api['kind'] + '")') if v['name'] != 'revision_id']
            assert set(api['data']).issubset({v['name'] for v in columns})
            assert all(api['data'].get(v['name']) is not None for v in columns if v['notnull'])
            assert api['rationale'].strip()
            for origin in api['origins']:
                assert c.execute('select id from unit where id=?', (origin['unit'],)).fetchone()
            for edge in api['evidence']:
                if heads.get(edge['object']) != edge['version']:
                    issues.append({'consumer': oid, 'ordered_edge': edge, 'actual_or_explicit_sequential_head': heads.get(edge['object']),
                                   'no_automatic_rebind_or_substitution': True})
                if original_heads.get(edge['object']) == edge['version']:
                    add(edge['object'] + '@' + str(edge['version']))
            heads[oid] = (api['expectedVersion'] or 0) + 1
            rows.append({'index': index, **selector, 'full_source_row': literal, 'actual_old_revision_id': rid,
                         'full_actual_old_native': old_native, 'full_actual_old_API': old_api,
                         'source_new_API_projection_NOT_OPERATION': api,
                         'exact_absence_proven': api['expectedVersion'] is None,
                         'prior8_full_old_whole_equal': oid in old_inputs,
                         'actual_RESEARCH4_accepted_T8_full_native_and_API_equal': selector.get('actual_T0788_successor_required', False)})
        assert len(rows) == len({v['object_id'] for v in rows}) == 21
        assert sum(v['full_actual_old_native'] is None for v in rows) == 12
        media = h.pointer(load(source['media_source_pin']), source['media_pointer'])
        for item in media:
            assert item['literal_API'] == load(item['pin'])
            value = item['literal_API']
            blob = R / value['storagePath']
            assert h.sha(blob) == value['sha256'] and blob.stat().st_size == value['bytes']
            assert not c.execute('select id from native_asset where id=?', (value['id'],)).fetchone()
        prior_edges = {v['native_rowid']: v for v in initial21['all21_target_history_incoming']}
        for rowid, old in prior_edges.items():
            current = incoming[rowid]
            assert all(current[key] == old[key] for key in ['native_rowid', 'revision_id', 'basis_revision_id', 'role', 'note'])
        added_edges = [value for rowid, value in incoming.items() if rowid not in prior_edges]
        protected = load(auth['protected42_pin'])['objects']
        assert len(protected) == 42 and not {v['object_id'] for v in rows}.intersection(v['object_id'] for v in protected.values())
        for protected_rid, value in protected.items():
            assert h.current(c, value['object_id']) == protected_rid and h.native(c, protected_rid) == value
        native_pin = h.write(out / 'complete-exact21-current-history-support-and-all-incoming-native-inputs-v1.json',
                             {'objects': pool, 'origin_units': units, 'documents': documents, 'asset_media_metadata': assets,
                              'ordered_native_arrays': 'Native rowid order and exact semantic data-array order; no source grade inferred'})
        for path, digest in cache:
            h.checked_pin_path({'path': path, 'sha256': digest})
        h.checked_pin_path(auth['main_pin'])
        assert h.state(c) == {'journal_head': 452, 'pending': 0}
        result = {'task': 'T-0789', 'root_readonly_authorization_pin': h.pin(ap), 'accepted_T8_root_receipt_pin': auth['accepted_T8_root_receipt_pin'],
                  'reviewed_T8_stage_handoff_pin': auth['reviewed_final_T8_stage_handoff_pin'], 'source_union_pin': SOURCE, 'independent_union_pin': OWN,
                  'actual_main_pin': auth['main_pin'], 'actual_state': h.state(c), 'rows': rows,
                  'actual_T8_four_current_head_bindings': current_T8_heads, 'full_native_input_pin': native_pin,
                  'all_history_incoming': list(incoming.values()), 'additional_post_T8_history_incoming': added_edges,
                  'prior4_exact_native_edge_identity_reused': True, 'all_incoming_current_callers_fully_captured': True,
                  'sequential_support_head_issues': issues, 'literal_media_input_APIs': media,
                  'prior58_routing_pin': PRIOR20, 'prior58_source_dispositions_pin': source['current_relevance_routing']['finite58_source_dispositions_pin'],
                  'source_individual_incoming_dispositions_pending': True,
                  'counts': {'targets': 21, 'revisions': 9, 'creates': 12, 'media': 2, 'incoming_unique': len(incoming),
                             'additional_post_T8_incoming': len(added_edges), 'head_issues': len(issues)},
                  'protected42_whole_current_exact': True, 'source_or_reading_grade_inferred': False,
                  'operation_build_stage_canonical_Wotan_mutation': False, 'usage': 'UNKNOWN pending root collector'}
        result_pin = h.write(out / 'exact21-actual-accepted452-whole-old-schema-support-head-and-full-incoming-guard-v1.json', result)
        print(json.dumps({'guard_pin': result_pin, 'native_pin': native_pin, 'counts': result['counts'], 'support_head_issues': issues}))
    except BaseException as error:
        h.write(out / 'STOP-exact21-readonly-guard-failure-and-preserved-actual-state-v1.json',
                {'error': repr(error), 'traceback': traceback.format_exc(), 'actual_state': h.state(c),
                 'main_pin': h.pin(R / auth['main_pin']['path']), 'helper_pin': h.pin(Path(__file__).resolve()),
                 'no_operations_or_runtime_mutation': True})
        raise
    finally:
        c.close()


if __name__ == '__main__':
    main()
