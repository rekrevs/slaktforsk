"""UNRUN exact21 draft builder. Copies guarded APIs; no CLI/SQLite/Wotan write.

Requires separate immutable root draft authorization and both final input gates.
It does not derive source grades, resolve requests, or repair source payloads.
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
S = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(S)
S.loader.exec_module(h)
D = importlib.util.spec_from_file_location('d', R / 'evaluations/T-0787/preparation/build_root_authorized_exact136_draft_v1.py')
d = importlib.util.module_from_spec(D)
D.loader.exec_module(d)
GUARD = {'path': 'evaluations/T-0789/preparation/exact21-actual-accepted452-input-guard-v1/exact21-actual-accepted452-whole-old-schema-support-head-and-full-incoming-guard-v1.json', 'sha256': '8def7d7ac334f5b8c63711b3f90800bb1de28947926faf26134fec05fffdad26'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--authorization', required=True)
    p.add_argument('--authorization-sha256', required=True)
    args = p.parse_args()
    cache = {}
    hashes = {}

    def read(pin):
        path = str(h.checked_pin_path(pin).resolve())
        assert hashes.setdefault(path, pin['sha256']) == pin['sha256'], 'Conflicting immutable pin'
        key = (path, pin['sha256'])
        if key not in cache:
            cache[key] = h.readpin(pin)[1]
        return cache[key]

    ap = Path(args.authorization).resolve()
    auth_pin = h.pin(ap)
    assert auth_pin['sha256'] == args.authorization_sha256
    auth = read(auth_pin)
    assert auth['action'] == 'BUILD_EXACT21_GUARDED_DRAFT_ONLY'
    assert auth['helper_pin'] == h.pin(Path(__file__).resolve())
    assert auth['guard_pin'] == GUARD
    assert auth['runtime_authorized'] is False
    out = (R / auth['output_directory']).resolve()
    assert out.is_relative_to(R / 'evaluations/T-0789/implementation') and not out.exists()
    g = read(GUARD)
    proof = read(auth['baseline_proof_pin'])
    assert proof['actual_current_guard_pin'] == GUARD
    assert proof['all50_schema_raw_rows_BLOB_and_native_array_order_equal'] is True
    assert proof['protected42_whole_native_current_exact'] is True
    assert g['sequential_support_head_issues'] == []
    assert g['counts'] == {'targets': 21, 'revisions': 9, 'creates': 12, 'media': 2, 'incoming_unique': 5, 'additional_post_T8_incoming': 1, 'head_issues': 0}
    ids = [r['object_id'] for r in g['rows']]
    assert len(ids) == len(set(ids)) == 21
    source = read(auth['final_source_union_pin'])
    selectors = h.pointer(source, auth['source_order_pointer'])
    assert [s['object_id'] for s in selectors] == ids
    for key in ['primary_final_input_gate', 'independent_final_input_gate']:
        binding = auth[key]
        gate = read(binding['pin'])
        assert h.pointer(gate, binding['ready_pointer']) is True
        assert h.pointer(gate, binding['source_union_pin_pointer']) == auth['final_source_union_pin']
        assert h.pointer(gate, binding['guard_pin_pointer']) == GUARD
    # Root supplies reviewed source locators; all changed current clauses remain
    # literal guarded projections. Renewed source placeholder metadata is not API.
    bindings = auth['individual_source_bindings']
    assert [b['object_id'] for b in bindings] == ids
    for binding, row in zip(bindings, g['rows']):
        assert h.pointer(read(binding['pin']), binding['pointer']) == binding['literal_source_disposition']
        if 'full_API_pointer' in binding:
            assert h.pointer(read(binding['pin']), binding['full_API_pointer']) == row['source_new_API_projection_NOT_OPERATION']
    # Exact five native edge identities plus primary/own dispositions are mandatory.
    incoming = auth['individual_incoming_bindings']
    assert [b['native_rowid'] for b in incoming] == [e['native_rowid'] for e in g['all_history_incoming']]
    for b, edge in zip(incoming, g['all_history_incoming']):
        assert b['actual_native_edge'] == edge
        for key in ['primary', 'independent']:
            v = b[key]
            assert h.pointer(read(v['pin']), v['pointer']) == v['literal_disposition']
    for b in auth['finite58_readiness_bindings']:
        assert h.pointer(read(b['pin']), b['ready_pointer']) is True
    assert len(auth['finite58_readiness_bindings']) == 2
    baseline = h.checked_pin_path(proof['baseline_pin'])
    mainpath = h.checked_pin_path(proof['main_after_pin'])
    c, base = h.conn(mainpath), h.conn(baseline)
    try:
        assert h.state(c) == h.state(base) == {'journal_head': 452, 'pending': 0}
        assert h.all50(c) == h.all50(base) == proof['all50']
        assert not c.execute('select id from operation where id=?', (auth['operation_id'],)).fetchone()
        protected = read(proof['protected42_pin'])['objects']
        assert len(protected) == 42 and not set(ids).intersection(n['object_id'] for n in protected.values())
        for rid, n in protected.items():
            assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
        changes, rows = [], []
        heads = dict(c.execute('select object_id,max(version) from revision group by object_id'))
        for index, row in enumerate(g['rows']):
            assert row['index'] == index
            api = copy.deepcopy(row['source_new_API_projection_NOT_OPERATION'])
            old = row['full_actual_old_native']
            assert api['id'] == row['object_id'] and api['expectedVersion'] == row['expected_version']
            if old is None:
                assert api['expectedVersion'] is None and not c.execute('select id from object where id=?', (api['id'],)).fetchone()
            else:
                assert h.current(c, api['id']) == old['id'] and h.native(c, old['id']) == old
                oldapi = h.api(old)
                oldapi['expectedVersion'] = old['version']
                assert oldapi == row['full_actual_old_API'] and api['expectedVersion'] == old['version']
            columns = [dict(v) for v in c.execute('pragma table_info("' + api['kind'] + '")') if v['name'] != 'revision_id']
            assert set(api['data']).issubset(v['name'] for v in columns)
            assert all(api['data'].get(v['name']) is not None for v in columns if v['notnull'])
            for origin in api['origins']:
                assert c.execute('select id from unit where id=?', (origin['unit'],)).fetchone()
            for edge in api['evidence']:
                assert heads.get(edge['object']) == edge['version'], ('Source head question; no substitution', api['id'], edge)
            heads[api['id']] = (api['expectedVersion'] or 0) + 1
            changes.append(api)
            rows.append({**copy.deepcopy(row), 'full_new_API': api, 'field_differences': d.diff(row['full_actual_old_API'], api),
                         'source_binding': bindings[index], 'new_revision_id': api['id'] + '@' + str(heads[api['id']]),
                         'ordered_arrays_preserved': True, 'source_grade_inferred': False})
        assert sum(v['expectedVersion'] is None for v in changes) == 12
        media = [copy.deepcopy(item['literal_API']) for item in g['literal_media_input_APIs']]
        for item in g['literal_media_input_APIs']:
            assert read(item['pin']) == item['literal_API']
            v = item['literal_API']
            blob = R / v['storagePath']
            assert h.sha(blob) == v['sha256'] and blob.stat().st_size == v['bytes']
            assert not c.execute('select id from native_asset where id=?', (v['id'],)).fetchone()
            attachments = [(a['id'], e) for a in changes for e in a.get('media', []) if e['id'] == v['id']]
            assert len(attachments) == 1 and attachments[0][0].startswith('R-T0789-P0007-own-annual-')
        operation = {'id': auth['operation_id'], 'actor': auth['actor'], 'reason': auth['reason'],
                     'dependencyReviewVersion': 2, 'media': media, 'changes': changes}
        # All authority input hashes rechecked before any draft output.
        for path, digest in hashes.items():
            assert h.sha(Path(path)) == digest
        assert h.pin(mainpath) == proof['main_after_pin'] and h.all50(c) == proof['all50']
        out.mkdir(parents=True)
        op = h.write(out / 'exact21-one-controlled-operation-v1.json', operation)
        table = h.write(out / 'exact21-full-individual-consequence-and-retain-table-v1.json', {
            'task': 'T-0789', 'rows': rows, 'guard_pin': GUARD, 'source_union_pin': auth['final_source_union_pin'],
            'individual_incoming_bindings': incoming, 'finite58_readiness_bindings': auth['finite58_readiness_bindings'],
            'full_native_input_pin': g['full_native_input_pin'], 'source_grade_inferred': False})
        member = {'operation_id': auth['operation_id'], 'operation_pin': op, 'target_ids': ids}
        membership = h.write(out / 'exact21-ordered-operation-membership-v1.json', {
            'task': 'T-0789', 'operations': [member], 'operation_count': 1, 'target_count': 21,
            'revision_count': 9, 'create_count': 12, 'media_count': 2})
        package = h.write(out / 'exact21-one-operation-package-proposal-v1.json', {
            'task': 'T-0789', 'operations': [member], 'membership_pin': membership, 'consequence_table_pin': table,
            'guard_pin': GUARD, 'baseline_proof_pin': auth['baseline_proof_pin'], 'baseline_pin': proof['baseline_pin'],
            'root_draft_authorization_pin': auth_pin, 'source_union_pin': auth['final_source_union_pin'],
            'primary_input_gate': auth['primary_final_input_gate'], 'independent_input_gate': auth['independent_final_input_gate'],
            'operation_count': 1, 'target_count': 21, 'existing_revisions': 9, 'new_objects': 12, 'media_count': 2,
            'built_byte_primary_approved': False, 'built_byte_independent_approved': False,
            'stage_authorized': False, 'canonical_authorized': False, 'actual_requests_not_inferred': True,
            'main_unchanged_pin': h.pin(mainpath), 'usage': 'UNKNOWN pending root collector'})
        print(json.dumps({'package_pin': package, 'membership_pin': membership, 'operation_pin': op, 'table_pin': table}))
    finally:
        c.close()
        base.close()


if __name__ == '__main__':
    main()
