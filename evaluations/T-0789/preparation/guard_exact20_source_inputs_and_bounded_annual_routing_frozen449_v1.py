"""Readonly T9 source-input guards. Planned T8 successors are not actual native."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
s = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)
ENTRY = {'path': 'evaluations/T-0789/source-review/exact20-source-module-order-and-readonly-guard-request-v1.json', 'sha256': 'c3f0299fd9b38f1b87512301b20b522653ce602b292830a9622102bf044bcba2'}
BASE = {'path': 'evaluations/T-0788/preparation/baseline-j449.sqlite', 'sha256': 'ea35b3d3bc782c7537da0dbf5fa89089945df8ae319543a0f7d5b061fe945b8e'}
T8 = {'path': 'evaluations/T-0788/implementation/exact36-draft-v1/exact36-one-controlled-operation-v1.json', 'sha256': 'f6e2709c21542736c330288868e404b4b300a6c0a2013e9df83d564a4dc3d07a'}
INPUTS = [
    {'path': 'evaluations/T-0789/preparation/Maj-current-native-PK-review-register-source-and-accepted-grave-inputs-v1.json', 'sha256': '3871911bd8c4813c2810a2fabbc1d609e8d3628c5dab21094f8e9efa3ab8868e'},
    {'path': 'evaluations/T-0788/preparation/complete-bounded-current744-two-person-and-accepted-support-native-inputs-v1.json', 'sha256': '03e4ecb85c5437a66ffc28418421adeba4d5d2098772497154e191f1317ab14d'}]
OUT = Path(__file__).resolve().parent / 'exact20-readonly-full-old-absence-schema-planned-head-and-incoming-annual-routing-guard-v1.json'
cache = {}


def load(pin):
    key = (pin['path'], pin['sha256'])
    if key not in cache:
        cache[key] = h.readpin(pin)[1]
    return cache[key]


def leaves(value, pointer=''):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from leaves(item, pointer + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from leaves(item, pointer + '/' + str(index))
    elif isinstance(value, str):
        yield pointer, value


def main():
    assert not OUT.exists(), 'Preserve prior guard; no overwrite'
    entry = load(ENTRY)
    assert entry['ready_for_build'] is False
    c = h.conn(h.checked_pin_path(BASE))
    assert h.state(c) == {'journal_head': 449, 'pending': 0}
    planned = {api['id']: api for api in load(T8)['changes']}
    heads = dict(c.execute('select object_id,max(version) from revision group by object_id'))
    declared_t8 = {row['id']: row['version'] for row in entry['planned_T0788_heads']}
    for oid, version in declared_t8.items():
        assert (planned[oid]['expectedVersion'] or 0) + 1 == version
    sequence_heads = {**heads, **declared_t8}
    rows, incoming, native, issues = [], {}, {}, []
    ids = [item['object_id'] for item in entry['ordered_source_rows']]
    assert len(ids) == len(set(ids)) == 20
    for index, selector in enumerate(entry['ordered_source_rows']):
        literal = h.pointer(load(selector['source_pin']), selector['source_pointer'])
        oid, old = selector['object_id'], None
        current_rid = h.current(c, oid) if heads.get(oid) is not None else None
        future = selector.get('actual_T0788_successor_required', False)
        if 'full_new_API' in literal:
            api = copy.deepcopy(literal['full_new_API'])
            assert api['id'] == oid and api['expectedVersion'] is None
            assert not c.execute('select id from object where id=?', (oid,)).fetchone()
            old_api = None
        else:
            if future:
                assert selector['expected_version'] == declared_t8[oid]
                assert h.pointer(load(literal['expected_producer_source_pin']), literal['expected_producer_pointer'])['object_id'] == oid
                old_api = copy.deepcopy(planned[oid])
                old_api['expectedVersion'] = selector['expected_version']
                assert current_rid != oid + '@' + str(selector['expected_version'])
            else:
                assert current_rid == oid + '@' + str(selector['expected_version'])
                old = h.native(c, current_rid)
                assert old == literal['whole_old_native']
                old_api = h.api(old)
                old_api['expectedVersion'] = selector['expected_version']
                native[current_rid] = old
            api = copy.deepcopy(old_api)
            for edit in literal['field_edits']:
                keys, value = edit['field'].split('.'), api
                for key in keys[:-1]:
                    value = value[key]
                assert value[keys[-1]] == edit['old'], ('Zero/unexpected old field match', oid, edit['field'])
                value[keys[-1]] = copy.deepcopy(edit['new'])
            for amendment in literal.get('evidence_rebinds', []):
                positions = [i for i, edge in enumerate(api['evidence']) if edge == amendment['old']]
                assert len(positions) == 1
                api['evidence'][positions[0]] = copy.deepcopy(amendment['new'])
            for edge in literal.get('evidence_additions', []):
                assert edge not in api['evidence']
                api['evidence'].append(copy.deepcopy(edge))
            for edge in c.execute('select d.rowid as native_rowid,d.* from dependency d join revision r on r.id=d.basis_revision_id where r.object_id=? order by d.rowid', (oid,)):
                item = dict(edge)
                caller_oid = c.execute('select object_id from revision where id=?', (edge['revision_id'],)).fetchone()[0]
                caller_current = h.current(c, caller_oid)
                item.update({'changed_target_object_id': oid, 'target_current_revision_id': current_rid,
                             'caller_current_revision_id': caller_current, 'caller_is_current': caller_current == edge['revision_id'],
                             'basis_is_current': edge['basis_revision_id'] == current_rid, 'source_disposition': 'PENDING_ASTRA'})
                incoming[edge['native_rowid']] = item
                for rid in [edge['revision_id'], caller_current, edge['basis_revision_id']]:
                    native[rid] = h.native(c, rid)
        assert api['id'] == oid and api['expectedVersion'] == selector['expected_version']
        columns = [dict(v) for v in c.execute('pragma table_info("' + api['kind'] + '")') if v['name'] != 'revision_id']
        assert set(api['data']).issubset({v['name'] for v in columns})
        assert all(api['data'].get(v['name']) is not None for v in columns if v['notnull'])
        assert api['rationale'].strip()
        for edge in api['evidence']:
            got = sequence_heads.get(edge['object'])
            if got != edge['version']:
                issues.append({'consumer': oid, 'ordered_edge': edge, 'sequential_actual_or_explicit_planned_head': got,
                               'automatic_substitution': False})
            elif edge['object'] in heads and heads[edge['object']] == edge['version']:
                rid = edge['object'] + '@' + str(edge['version'])
                native[rid] = h.native(c, rid)
        sequence_heads[oid] = (api['expectedVersion'] or 0) + 1
        rows.append({'index': index, **selector, 'full_source_row': literal, 'actual449_current_revision_id': current_rid,
                     'full_actual_old_native': old, 'full_old_API_or_explicit_UNACCEPTED_T8_input_API': old_api,
                     'source_new_API_projection_NOT_OPERATION': api, 'expected_absence_proven': api['expectedVersion'] is None,
                     'whole_old_native_capture_pending_actual_T8_acceptance': future,
                     'planned_T8_producer_pin_if_needed': T8 if future else None})
    media = h.pointer(load(entry['media_source_pin']), entry['media_pointer'])
    assert len(media) == 2
    for item in media:
        assert item['literal_API'] == load(item['pin'])
        value = item['literal_API']
        blob = R / value['storagePath']
        assert h.sha(blob) == value['sha256'] and blob.stat().st_size == value['bytes']
        assert not c.execute('select id from native_asset where id=?', (value['id'],)).fetchone()
    terms = ['1945', '1946', 'Gondolen', '99/107', '99 och 107', 's. 99', 's. 107', 'uppslag 15',
             'A II c/33', 'A II c/34', 'AIIc/33', 'AIIc/34', '00023815', '00023816']
    routing, observed = [], set()
    for input_pin in INPUTS:
        source_objects = load(input_pin)['objects']
        for pointer_key, saved in source_objects.items():
            if saved['id'] in observed or h.current(c, saved['object_id']) != saved['id']:
                continue
            observed.add(saved['id'])
            actual = h.native(c, saved['id'])
            assert actual == saved, ('Finite saved input changed', input_pin, saved['id'])
            matches = []
            for field, value in leaves({'data': h.api(actual)['data'], 'caveat': actual['caveat']}):
                matched = [term for term in terms if term in value]
                if matched:
                    matches.append({'field_pointer': field, 'matched_literal_terms': matched, 'whole_actual_field': value})
            if matches:
                native[actual['id']] = actual
                routing.append({'revision_id': actual['id'], 'object_id': actual['object_id'],
                                'saved_input_pin': input_pin, 'saved_input_pointer': '/objects/' + pointer_key,
                                'matches': matches, 'full_current_native_pointer': '/full_native/' + actual['id'],
                                'source_relevance_or_grade': 'NOT_INFERRED'})
    protected_pin = h.pin(R / 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json')
    protected = load(protected_pin)['objects']
    assert len(protected) == 42 and not set(ids).intersection(v['object_id'] for v in protected.values())
    for rid, value in protected.items():
        assert h.current(c, value['object_id']) == rid and h.native(c, rid) == value
    for path, digest in cache:
        h.checked_pin_path({'path': path, 'sha256': digest})
    h.checked_pin_path(BASE)
    result = {'task': 'T-0789', 'source_entrypoint_pin': ENTRY, 'frozen449_baseline_pin': BASE,
              'actual_frozen_state': h.state(c), 'planned_T0788_exact_operation_pin': T8,
              'rows': rows, 'all_history_incoming': list(incoming.values()), 'full_native': native,
              'sequential_support_head_issues': issues, 'literal_media_input_APIs': media,
              'bounded_annual_literal_current_routing': routing, 'finite_routing_input_pins': INPUTS,
              'routing_is_not_source_grade_or_fullscope_reading': True,
              'source_incoming_dispositions': 'PENDING; actual accepted T8 successor edges require additive fresh reconciliation',
              'protected42_whole_native_exact': True, 'protected42_target_intersection': [],
              'counts': {'targets': 20, 'creates': 12, 'revisions': 8, 'actual449_whole_old_matches': 7,
                         'planned_T8_successor_whole_native_pending': 1, 'media': 2, 'incoming_unique': len(incoming),
                         'finite_current_routing': len(routing), 'support_head_issues': len(issues)},
              'build_ready': False, 'operations_constructed': False, 'stage_canonical_Wotan_mutation': False,
              'usage': 'UNKNOWN pending root collector'}
    pin = h.write(OUT, result)
    c.close()
    print(json.dumps({'guard_pin': pin, 'counts': result['counts'], 'support_head_issues': issues}))


if __name__ == '__main__':
    main()
