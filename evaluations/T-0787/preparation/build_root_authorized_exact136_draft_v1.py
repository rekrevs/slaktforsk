"""Exact settled source136 draft only. Readonly SQLite; no CLI, stage or Wotan writes."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
OUT = R / 'evaluations/T-0787/implementation/exact136-draft-v1'
SOURCE = {'path': 'evaluations/T-0787/source-review/complete-exact136-individual-source-input-and-order-build-release-v1.json', 'sha256': '78e6e5172535a69958b85ccb6fad25292bfcefaa00b7f8ce87d6fe8b7dec6c22'}
COMPOSITION = {'path': 'evaluations/T-0787/preparation/nominal136-individual-source-API-input-composition-and-exact-support-media-guards-NOT-OPERATION-v1.json', 'sha256': 'a01d2ea6d42c64f8e7d0565bb32ea35a8043c72375cc2f423ab2e33a71f48e8d'}
OPID = 'T-0787/exact136-source-consequences-and-bounded3011-adoption-v1'
cache = {}


def load(pin):
    key = (pin['path'], pin['sha256'])
    if key not in cache:
        cache[key] = h.readpin(pin)[1]
    return cache[key]


def diff(old, new, pointer=''):
    """Lists are ordered values: retain the entire old/new array, never sort."""
    if type(old) is type(new) and isinstance(old, dict):
        result = []
        for key in list(old) + [k for k in new if k not in old]:
            address = pointer + '/' + key.replace('~', '~0').replace('/', '~1')
            if key not in old or key not in new:
                result.append({'pointer': address, 'old_present': key in old, 'new_present': key in new,
                               'old': old.get(key), 'new': new.get(key)})
            else:
                result.extend(diff(old[key], new[key], address))
        return result
    if old == new:
        return []
    return [{'pointer': pointer, 'old_present': True, 'new_present': True, 'old': old, 'new': new}]


def main():
    assert not OUT.exists(), ('Preserve existing draft; no retry', str(OUT))
    source = load(SOURCE)
    composition = load(COMPOSITION)
    assert source['source_ready_for_exact_draft'] is True
    assert source['final_source_ready_for_canonical'] is False
    assert composition['sequential_head_issues'] == composition['native_API_default_representation_questions'] == []
    assert len(source['ordered_targets']) == len(composition['rows']) == 136
    for ordered, row in zip(source['ordered_targets'], composition['rows']):
        assert ordered == {k: row[k] for k in ['object_id', 'source_spec_pin', 'source_row_pointer']}
    for pin in source['source_modules'] + source['individual_incoming_and_amendment_pins']:
        load(pin)
    proof = load(composition['baseline_proof_pin'])
    h.checked_pin_path(proof['baseline_pin'])
    main_before = h.pin(R / proof['main_pin']['path'])
    assert main_before == proof['main_pin']
    live = h.conn(R / main_before['path'])
    baseline = h.conn(R / proof['baseline_pin']['path'])
    assert h.state(live) == h.state(baseline) == {'journal_head': 447, 'pending': 0}
    assert not live.execute('select id from operation where id=?', (OPID,)).fetchone()
    protected_path = R / 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json'
    protected = json.loads(protected_path.read_text())['objects']
    assert len(protected) == 42
    for rid, native in protected.items():
        assert h.current(live, native['object_id']) == rid
        assert h.native(live, rid) == h.native(baseline, rid) == native
    changes = [copy.deepcopy(r['proposed_full_API_NOT_OPERATION']) for r in composition['rows']]
    ids = [a['id'] for a in changes]
    assert len(set(ids)) == 136 and not set(ids).intersection(n['object_id'] for n in protected.values())
    assert sum(a['expectedVersion'] is None for a in changes) == 6
    kinds = {r['id']: r['kind'] for r in live.execute('select id,kind from object')}
    refs = {'record': {'source_id': 'source'}, 'transcription': {'record_id': 'record'}, 'mention': {'record_id': 'record'},
            'observation': {'record_id': 'record', 'mention_id': 'mention'}, 'identity': {'mention_id': 'mention', 'person_id': 'person'},
            'event': {'place_id': 'place'}, 'participation': {'event_id': 'event', 'person_id': 'person', 'mention_id': 'mention'},
            'fact': {'subject_id': '*'}, 'question': {'subject_id': '*'}, 'assessment': {'subject_id': '*'},
            'search': {'question_id': 'question', 'source_id': 'source'}, 'narrative': {'subject_id': '*'}}
    bound = {'record': ['source_id'], 'transcription': ['record_id'], 'mention': ['record_id'],
             'observation': ['record_id', 'mention_id'], 'identity': ['mention_id'], 'participation': ['event_id', 'mention_id']}
    heads = {}
    schema_checks = []
    consequences = []
    for index, (row, api) in enumerate(zip(composition['rows'], changes)):
        oid = row['object_id']
        assert api['id'] == oid
        literal = h.pointer(load(row['source_spec_pin']), row['source_row_pointer'])
        if row['full_old_native'] is None:
            assert api['expectedVersion'] is None
            assert not live.execute('select id from object where id=?', (oid,)).fetchone()
            assert literal['full_new_API'] == api
            old_api = None
        else:
            rid = oid + '@' + str(api['expectedVersion'])
            assert h.current(live, oid) == rid
            assert h.native(live, rid) == h.native(baseline, rid) == row['full_old_native']
            old_api = h.api(row['full_old_native'])
            old_api['expectedVersion'] = api['expectedVersion']
            assert old_api == row['full_old_API']
            assert literal['whole_old_native'] == row['full_old_native']
        columns = [dict(v) for v in live.execute('pragma table_info("' + api['kind'] + '")') if v['name'] != 'revision_id']
        assert set(api['data']).issubset({v['name'] for v in columns})
        assert all(api['data'].get(v['name']) is not None for v in columns if v['notnull'])
        assert api['rationale'].strip()
        for field, required_kind in refs.get(api['kind'], {}).items():
            target = api['data'].get(field)
            if target is not None:
                assert target in kinds and (required_kind == '*' or kinds[target] == required_kind)
        for edge in api['evidence']:
            version = heads.get(edge['object'])
            if version is None:
                version = int(h.current(live, edge['object']).rsplit('@', 1)[1])
            assert version == edge['version'], (oid, edge, version)
        for field in bound.get(api['kind'], []):
            target = api['data'].get(field)
            if target is None:
                continue
            version = heads.get(target)
            if version is None:
                version = int(h.current(live, target).rsplit('@', 1)[1])
            explicit = next((e for e in api['evidence'] if e['object'] == target), None)
            expected = explicit['version'] if explicit else api.get('bindings', {}).get(target, heads.get(target))
            assert expected == version, (oid, field, target, expected, version)
        if api['kind'] == 'search':
            scope = api['data']['scope_json']
            assert scope['description'] and scope['query']
            assert api['data']['outcome'] != 'negative' or isinstance(scope.get('bounds'), dict) and scope['bounds']
        kinds[oid] = api['kind']
        heads[oid] = (api['expectedVersion'] or 0) + 1
        edits = diff(old_api, api) if old_api is not None else [{'pointer': '', 'old_present': False, 'new_present': True, 'old': None, 'new': api}]
        consequences.append({'index': index, 'object_id': oid, 'old_revision_id': row['full_old_native']['id'] if row['full_old_native'] else None,
                             'new_revision_id': oid + '@' + str(heads[oid]), 'source_spec_pin': row['source_spec_pin'],
                             'source_row_pointer': row['source_row_pointer'], 'full_source_disposition_row': literal,
                             'full_old_native': row['full_old_native'], 'full_old_API': old_api, 'full_new_API': api,
                             'field_differences': edits, 'unchanged_top_level_fields': [k for k in old_api if old_api[k] == api.get(k)] if old_api else [],
                             'explicit65_edge_amendments': row.get('explicit65_edge_amendments', []),
                             'all_other_fields_and_ordered_arrays_retained': all(old_api[k] == api[k] for k in old_api if not any(d['pointer'] == '/' + k or d['pointer'].startswith('/' + k + '/') for d in edits)) if old_api else None})
        schema_checks.append({'index': index, 'object_id': oid, 'expectedVersion': api['expectedVersion'], 'new_version': heads[oid],
                              'whole_old_or_absence_match': True, 'ordered_support_current_head_and_schema_pass': True})
    for api in changes:
        for edge in api['evidence']:
            assert edge['object'] not in heads or edge['version'] == heads[edge['object']], ('Final operation stale basis', api['id'], edge)
    media = copy.deepcopy(composition['media_registration_API_NOT_OPERATION'])
    assert media == load(composition['media_staging_API_pin'])
    blob = R / media['storagePath']
    assert h.sha(blob) == media['sha256'] and blob.stat().st_size == media['bytes']
    assert not live.execute('select id from native_asset where id=?', (media['id'],)).fetchone()
    attached = [(a['id'], e) for a in changes for e in a.get('media', []) if e['id'] == media['id']]
    assert len(attached) == 1 and attached[0][0] == 'R-T0787-Sundsvall-AIIa15-f3011-tested-page'
    incoming = {}
    occurrences = []
    for pin in source['individual_incoming_and_amendment_pins'][:3]:
        module = load(pin)
        raw_pin = module['input_pin']
        raw = load(raw_pin)
        pool = raw.get('full_incoming_exact_and_current_caller_native', raw.get('full_exact_and_current_incoming_callers'))
        for index, judgment in enumerate(module['rows']):
            edge = judgment['exact_edge']
            rowid = edge['native_rowid']
            stored = dict(live.execute('select rowid as native_rowid,* from dependency where rowid=?', (rowid,)).fetchone())
            assert stored == {k: edge[k] for k in stored}
            assert edge in raw['all_history_incoming']
            current_rid = edge['caller_current_revision_id']
            assert h.native(live, current_rid) == pool[current_rid]
            exact_rid = edge['revision_id']
            assert h.native(live, exact_rid) == pool[exact_rid]
            identity = {k: edge[k] for k in ['native_rowid', 'revision_id', 'basis_revision_id', 'role', 'note']}
            locator = {'source_disposition_pin': pin, 'source_row_pointer': '/rows/' + str(index), 'raw_current_input_pin': raw_pin,
                       'full_literal_source_disposition': judgment}
            occurrences.append({'native_rowid': rowid, **locator})
            if rowid not in incoming:
                incoming[rowid] = {'exact_native_edge': identity, 'full_exact_caller_native': pool[exact_rid],
                                  'full_current_caller_native': pool[current_rid], 'source_disposition_occurrences': []}
            assert incoming[rowid]['exact_native_edge'] == identity
            incoming[rowid]['source_disposition_occurrences'].append(locator)
    assert len(occurrences) == 94
    assert h.pin(R / main_before['path']) == main_before
    assert h.state(live) == {'journal_head': 447, 'pending': 0}
    for path, digest in cache:
        h.checked_pin_path({'path': path, 'sha256': digest})
    own_edge = R / 'evaluations/T-0787/independent-review/P0258-event-one-old-version-participation-edge-retain-v1.json'
    own = json.loads(own_edge.read_text())
    assert own['independent_disposition'] == 'RETAIN_CURRENT_EXACT_OLD_BASIS'
    operation = {'id': OPID, 'actor': 'Sol; exact source-settled individual consequences under root draft-only authorization',
                 'reason': 'T-0787: exact full-source corrections and necessary current copies, four explicitly approved identity/tree reviews, and bounded physical3011 negative-page adoption; historical knowledge, OWNER and life scopes retained.',
                 'dependencyReviewVersion': 2, 'media': [media], 'changes': changes}
    OUT.mkdir(parents=True)
    op_pin = h.write(OUT / 'exact136-one-controlled-operation-v1.json', operation)
    table_pin = h.write(OUT / 'all136-individual-whole-API-consequence-and-retain-table-v1.json',
                        {'task': 'T-0787', 'source_bundle_pin': SOURCE, 'composition_pin': COMPOSITION, 'rows': consequences,
                         'media_registration_API': media, 'incoming_edge_occurrences': occurrences,
                         'unique_native_rowid_incoming_dispositions': list(incoming.values()),
                         'counts': {'targets': 136, 'revisions': 130, 'creates': 6, 'media': 1, 'incoming_occurrences': 94,
                                    'unique_native_rowids': len(incoming), 'duplicate_rowid_occurrences': 94 - len(incoming)},
                         'own_event_edge_pin': h.pin(own_edge), 'actual_runtime_requests_not_yet_generated_or_approved': True,
                         'built_byte_primary_approved': False, 'built_byte_independent_approved': False, 'stage_or_canonical_authorized': False})
    member = {'operation_id': OPID, 'operation_pin': op_pin, 'target_ids': ids}
    membership_pin = h.write(OUT / 'exact136-ordered-operation-membership-v1.json',
                             {'task': 'T-0787', 'operations': [member], 'operation_count': 1, 'target_count': 136,
                              'revision_count': 130, 'create_count': 6, 'media_count': 1, 'source_bundle_pin': SOURCE})
    proof_pin = h.write(OUT / 'fresh447-wholeold-ordered-support-schema-protected-media-and-incoming-guards-v1.json',
                       {'task': 'T-0787', 'helper_pin': h.pin(Path(__file__).resolve()), 'source_bundle_pin': SOURCE,
                        'composition_pin': COMPOSITION, 'baseline_proof_pin': composition['baseline_proof_pin'],
                        'main_before_pin': main_before, 'main_after_pin': h.pin(R / main_before['path']), 'state': h.state(live),
                        'checks': schema_checks, 'protected42_pin': h.pin(protected_path), 'protected42_current_whole_native_equal': True,
                        'protected42_target_intersection': [], 'media_staging_pin': composition['media_staging_API_pin'],
                        'media_blob_pin': h.pin(blob), 'one_media_only_attached_to_physical3011': True,
                        'source65_explicit22_application': composition['source65_explicit22_application'],
                        'source94_occurrences_native_rowid_exact': True, 'source_incoming_unique_rowids': len(incoming),
                        'ordered_producers_final_support_heads_schema_pass': True, 'oldnative_data_array_order_not_normalized': True,
                        'SQLite_mode': 'readonly', 'CLI_stage_canonical_Wotan_mutations': False, 'usage': 'UNKNOWN pending root collector'})
    package_pin = h.write(OUT / 'exact136-one-operation-package-proposal-v1.json',
                         {'task': 'T-0787', 'membership_pin': membership_pin, 'operations': [member], 'operation_count': 1,
                          'target_count': 136, 'existing_revisions': 130, 'new_objects': 6, 'media_count': 1,
                          'source_bundle_pin': SOURCE, 'composition_pin': COMPOSITION, 'source_module_pins': source['source_modules'],
                          'individual_incoming_and_amendment_pins': source['individual_incoming_and_amendment_pins'],
                          'consequence_table_pin': table_pin, 'mechanical_guard_pin': proof_pin,
                          'built_byte_primary_approved': False, 'built_byte_independent_approved': False,
                          'stage_authorized': False, 'canonical_authorized': False,
                          'next_step': 'Separate primary and independent whole built-package byte gates; root authorizes any stage later.',
                          'usage': 'UNKNOWN pending root collector'})
    live.close()
    baseline.close()
    print(json.dumps({'package_pin': package_pin, 'membership_pin': membership_pin, 'operation_pin': op_pin,
                      'consequence_table_pin': table_pin, 'guard_pin': proof_pin, 'counts': {'targets': 136, 'revisions': 130, 'creates': 6,
                      'media': 1, 'incoming_occurrences': 94, 'unique_rowids': len(incoming)}, 'stage_canonical_UNRUN': True}))


if __name__ == '__main__':
    main()
