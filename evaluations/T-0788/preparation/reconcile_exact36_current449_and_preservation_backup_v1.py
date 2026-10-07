"""Readonly accepted449 reconciliation and one preservation backup. No operations."""
import copy
import importlib.util
import json
import sqlite3
from pathlib import Path

R = Path(__file__).resolve().parents[3]
S = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(S)
S.loader.exec_module(h)
O = Path(__file__).resolve().parent
SOURCE = {'path': 'evaluations/T-0788/source-review/complete-exact36-source-union-order-media-and-individual-incoming-draft-release-v1.json', 'sha256': '53216911b56a4a7bf7ed3a37a2db5033d9c3da05fc3e9380e16d6ec13302c2b8'}
OWN = {'path': 'evaluations/T-0788/independent-review/complete36-source-union-and-individual-retains-independent-draft-readiness-gate-v1.json', 'sha256': 'c4c92ef34605b278a75da0e8e86e161dd7cb38d9f47cf7af791dfb5b789cb455'}
PRIOR = {'path': 'evaluations/T-0788/preparation/complete36-additive-whole-old-API-support-and-incoming-guard-NOT-OPERATION-v1.json', 'sha256': '42246f70c2b390fde2e803b17c02212afe64219ae7c3820806dd34c9e38affbc'}
ACCEPTANCE = {'path': 'evaluations/T-0787/root-actual-canonical449-source-package-acceptance-v1.json', 'sha256': 'db87b9727c810ef2dbf8c5babbdc4fc046fc6a666fc32359e7e5faeb7f709385'}


def main():
    source, own, prior, acceptance = [h.readpin(pin)[1] for pin in [SOURCE, OWN, PRIOR, ACCEPTANCE]]
    assert source['ready_for_draft'] is True and own['ready_for_exact_draft'] is True
    assert own['source_union_pin'] == SOURCE
    M = R / acceptance['main_pin']['path']
    assert h.pin(M) == acceptance['main_pin']
    live = h.conn(M)
    assert h.state(live) == {'journal_head': 449, 'pending': 0}
    bp = O / 'baseline-j449.sqlite'
    assert not bp.exists(), 'Preserve existing backup; no replacement'
    destination = sqlite3.connect(bp)
    live.backup(destination)
    destination.close()
    base = h.conn(bp)
    before = h.all50(live)
    assert h.all50(base) == before and h.state(base) == h.state(live)
    protected_pin = {'path': 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json', 'sha256': prior.get('protected42_pin', {}).get('sha256') or h.sha(R / 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json')}
    protected = h.readpin(protected_pin)[1]['objects']
    assert len(protected) == 42
    for rid, n in protected.items():
        assert h.current(live, n['object_id']) == rid and h.native(live, rid) == h.native(base, rid) == n
    baseline_proof = h.write(O / 'fresh449-physical-backup-full50-and-protected42-proof-v1.json',
                             {'task': 'T-0788', 'accepted_T7_root_receipt_pin': ACCEPTANCE, 'main_pin': h.pin(M),
                              'baseline_pin': h.pin(bp), 'actual_state': h.state(live), 'all50': before,
                              'all50_logical_schema_rows_BLOB_native_array_order_equal': True,
                              'protected42_pin': protected_pin, 'protected42_exact': True,
                              'backup_is_preservation_not_stage_or_DB_replace': True, 'native_operation_or_Wotan_write': False})
    old_by_id = {r['object_id']: r for r in prior['rows']}
    modules, rows, body_delta, schema_issues, pool = {}, [], [], [], {}
    def module(pin):
        key = (pin['path'], pin['sha256'])
        if key not in modules:
            modules[key] = h.readpin(pin)[1]
        return modules[key]
    for selected in source['rows']:
        oid = selected['object_id']
        literal = h.pointer(module(selected['source_spec_pin']), selected['source_row_pointer'])
        previous = old_by_id[oid]
        if selected['action'] == 'create':
            api = copy.deepcopy(literal['full_new_API'])
            assert api['id'] == oid and api['expectedVersion'] is None
            assert not live.execute('select id from object where id=?', (oid,)).fetchone()
            expected = copy.deepcopy(previous['source_new_API_projection_NOT_OPERATION'])
            if api != expected:
                assert oid == 'IDENTITY-REVIEW-T0788-P0017'
                old_body, new_body = expected['data']['body'], api['data']['body']
                expected['data']['body'] = new_body
                assert api == expected
                body_delta.append({'object_id': oid, 'field': 'data.body', 'old': old_body, 'new': new_body,
                                   'source_spec_pin': selected['source_spec_pin'], 'source_row_pointer': selected['source_row_pointer'],
                                   'all_other_API_values_and_ordered_arrays_exact': True})
            n, old_api = None, None
        else:
            version = selected['expected_version']
            rid = oid + '@' + str(version)
            assert h.current(live, oid) == rid
            n = h.native(live, rid)
            assert n == h.native(base, rid) == literal['whole_old_native'] == previous['full_old_native']
            old_api = h.api(n)
            old_api['expectedVersion'] = version
            assert old_api == previous['full_old_API']
            api = copy.deepcopy(previous['source_new_API_projection_NOT_OPERATION'])
            assert literal == previous['full_source_row']
        columns = [dict(r) for r in live.execute('pragma table_info("' + api['kind'] + '")') if r['name'] != 'revision_id']
        assert set(api['data']).issubset({c['name'] for c in columns})
        assert all(api['data'].get(c['name']) is not None for c in columns if c['notnull'])
        rows.append({'index': selected['index'], 'object_id': oid, 'source_spec_pin': selected['source_spec_pin'],
                     'source_row_pointer': selected['source_row_pointer'], 'full_source_disposition_row': literal,
                     'full_old_native': n, 'full_old_API': old_api, 'exact_full_new_API_NOT_OPERATION': api,
                     'same_old_head_and_native_as_prior447': n is not None, 'exact_absent_on_actual449': n is None})
    assert len(rows) == 36 and len(body_delta) == 1
    assert not {r['object_id'] for r in rows}.intersection(n['object_id'] for n in protected.values())
    heads, issues, support_heads = {}, [], []
    for row in rows:
        api = row['exact_full_new_API_NOT_OPERATION']
        for edge in api['evidence']:
            actual = heads.get(edge['object'])
            if actual is None:
                actual = live.execute('select max(version) from revision where object_id=?', (edge['object'],)).fetchone()[0]
            support_heads.append({'consumer': api['id'], 'ordered_edge': edge, 'actual_sequential_current_version': actual})
            if actual != edge['version']:
                issues.append({'consumer': api['id'], 'edge': edge, 'actual_current_version': actual, 'no_auto_rebind': True})
        heads[api['id']] = (api['expectedVersion'] or 0) + 1
    def add(rid):
        if rid in pool:
            return
        n = h.native(live, rid)
        assert n == h.native(base, rid)
        pool[rid] = n
        for edge in n['evidence']:
            add(edge['basis_revision_id'])
            add(h.current(live, edge['basis_revision_id'].rsplit('@', 1)[0]))
    for row in rows:
        if row['full_old_native']:
            add(row['full_old_native']['id'])
        for edge in row['exact_full_new_API_NOT_OPERATION']['evidence']:
            rid = edge['object'] + '@' + str(edge['version'])
            if live.execute('select id from revision where id=?', (rid,)).fetchone():
                add(rid)
    incoming = []
    for locator in source['individual_incoming_dispositions']:
        judgment = h.pointer(module(locator['pin']), locator['pointer'])
        edge = judgment['exact_edge']
        assert edge['native_rowid'] == locator['native_rowid']
        stored = dict(live.execute('select rowid as native_rowid,* from dependency where rowid=?', (edge['native_rowid'],)).fetchone())
        assert stored == {k: edge[k] for k in stored}
        oid = live.execute('select object_id from revision where id=?', (edge['revision_id'],)).fetchone()[0]
        current = h.current(live, oid)
        add(edge['revision_id'])
        add(current)
        assert current == edge['caller_current_revision_id']
        assert pool[current] == prior['full_exact_and_current_incoming_caller_native'][current]
        incoming.append({'native_rowid': edge['native_rowid'], 'exact_edge': edge,
                         'individual_source_disposition_pin': locator['pin'], 'source_row_pointer': locator['pointer'],
                         'whole_individual_source_disposition': judgment, 'exact_caller_native_pointer': '/full_current_history_upstream_native/' + edge['revision_id'],
                         'current_caller_native_pointer': '/full_current_history_upstream_native/' + current,
                         'all_prior447_caller_fields_arrays_equal_accepted449': True})
    assert len(incoming) == len({e['native_rowid'] for e in incoming}) == 28
    actual_incoming = {r[0] for row in rows if row['full_old_native'] for r in live.execute('select d.rowid from dependency d join revision b on b.id=d.basis_revision_id where b.object_id=?', (row['object_id'],))}
    assert actual_incoming == {e['native_rowid'] for e in incoming}
    media = source['media_registration_API']
    assert media == prior['literal744_media_registration_API_NOT_OPERATION']
    assert h.sha(R / media['storagePath']) == media['sha256'] and (R / media['storagePath']).stat().st_size == media['bytes']
    assert not live.execute('select id from native_asset where id=?', (media['id'],)).fetchone()
    T7 = h.readpin(acceptance['handoff_pin'])[1]
    target136 = h.readpin(h.readpin(T7['reviewed_final_stage_handoff_pin'])[1]['native_prefix_stage_handoff_pin'])[1]['all136_API_pin']
    old_targets = h.readpin(target136)[1]['objects']
    for rid, n in old_targets.items():
        assert h.current(live, n['object_id']) == rid and h.native(live, rid) == n
    assert h.pin(M) == acceptance['main_pin'] and h.all50(live) == before
    for path, digest in modules:
        h.checked_pin_path({'path': path, 'sha256': digest})
    result = {'task': 'T-0788', 'status': 'EXACT36_ACTUAL449_RECONCILIATION_PASS' if not issues else 'STOP_RETURN_CURRENT_SUPPORT_HEAD_QUESTIONS_TO_ASTRA',
              'source_union_pin': SOURCE, 'independent_whole36_readiness_pin': OWN, 'prior447_guard_pin': PRIOR,
              'accepted_T7_root_receipt_pin': ACCEPTANCE, 'fresh449_baseline_proof_pin': baseline_proof,
              'main_before_and_after_pin': acceptance['main_pin'], 'baseline_pin': h.pin(bp), 'actual_state': h.state(live),
              'rows': rows, 'exact_five_v4_vs_v3_single_body_delta': body_delta, 'all28_individual_incoming': incoming,
              'full_current_history_upstream_native': pool, 'ordered_sequential_support_heads': support_heads,
              'current_support_head_issues': issues, 'schema_issues': schema_issues, 'protected42_whole_exact': True,
              'accepted136_native_current_and_all137_resolutions_preserved_by_all50_equal': True,
              'literal_media_registration_API_NOT_OPERATION': media, 'counts': {'targets': 36, 'revisions': 31, 'creates': 5,
              'media': 1, 'incoming_unique': 28, 'upstream_exact_and_current_native_revisions': len(pool), 'head_issues': len(issues)},
              'source_grade_inferred': False, 'operations_constructed': False, 'stage_canonical_Wotan_mutation': False,
              'usage': 'UNKNOWN pending root collector'}
    out = h.write(O / 'complete36-accepted449-reconciliation-full-old-new-supports-and-individual-incoming-v1.json', result)
    base.close()
    live.close()
    print(json.dumps({'reconciliation_pin': out, 'baseline_proof_pin': baseline_proof, 'counts': result['counts'], 'issues': issues}))


if __name__ == '__main__':
    main()
