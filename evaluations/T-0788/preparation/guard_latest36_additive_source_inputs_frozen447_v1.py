"""Readonly final36 mechanical inputs. Reuse prior27; no operation or source grade."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
S = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(S)
S.loader.exec_module(h)
O = Path(__file__).resolve().parent
PRIOR = {'path': 'evaluations/T-0788/preparation/exact27-whole-old-source-field-API-order-and-all-history-incoming-readonly-guard-v1.json', 'sha256': '7c1e21db8c07f8c72bc4bef87a1b305676c497a6bb64e3fde6bed135bb38d579'}
SPECS = [
    {'path': 'evaluations/T-0788/source-review/exact744-core-three-and-six-small-source-field-spec-v1.json', 'sha256': '380c6b0bec3028f0dad203d874a0fe7e38428e26fd208f6fcf9a495d358cb4c4'},
    {'path': 'evaluations/T-0788/source-review/finite-nineteen-current744-semantic-copy-exact-field-spec-v5.json', 'sha256': 'bd0165352f9c4f4eaeb6454c6d35b762671bf6d39671fc2d71596e383dd0eb2e'},
    {'path': 'evaluations/T-0788/source-review/three-direct-current-parent-copy-and-transfer-reservation-source-spec-v1.json', 'sha256': 'ed956906c1c0e22c9d78fa907ec55456b3490ec57139618720ddcc75901ed675'},
    {'path': 'evaluations/T-0788/source-review/four-bounded-identity-tree-and-one-mother-adoption-full-API-source-spec-v3.json', 'sha256': '064eae70893a99cd8817d064043eea9e12bbdea1aebe2acf143a91db6815896e'}]


def main():
    previous = h.readpin(PRIOR)[1]
    prior = {v['object_id']: v for v in previous['rows']}
    proof = h.readpin(previous['baseline_proof_pin'])[1]
    c = h.conn(h.checked_pin_path(proof['baseline_pin']))
    assert h.state(c) == {'journal_head': 447, 'pending': 0}
    rows, ids, full, reused = [], set(), {}, []
    modules = []
    for pin in SPECS:
        module = h.readpin(pin)[1]
        modules.append(module)
        for index, literal in enumerate(module['rows']):
            if 'full_new_API' in literal:
                api = copy.deepcopy(literal['full_new_API'])
                oid = api['id']
                assert api['expectedVersion'] is None and oid not in ids
                assert not c.execute('select id from object where id=?', (oid,)).fetchone()
                rows.append({'object_id': oid, 'source_spec_pin': pin, 'source_row_pointer': '/rows/' + str(index),
                             'full_source_row': literal, 'full_old_native': None, 'expected_absent': True,
                             'source_new_API_projection_NOT_OPERATION': api})
            else:
                oid, version = literal['object_id'], literal['expected_version']
                rid = oid + '@' + str(version)
                assert oid not in ids and h.current(c, oid) == rid
                native = h.native(c, rid)
                assert native == literal['whole_old_native']
                old = h.api(native)
                old['expectedVersion'] = version
                if oid in prior:
                    assert native == prior[oid]['full_old_native'] and old == prior[oid]['full_old_API']
                    reused.append({'object_id': oid, 'prior_pin': PRIOR, 'prior_row_pointer': '/rows/' + str(previous['rows'].index(prior[oid])),
                                   'exact_full_old_native_and_API_reused': True,
                                   'new_source_edit_values_changed': literal['field_edits'] != prior[oid]['whole_source_disposition_row']['field_edits']})
                api = copy.deepcopy(old)
                guards = []
                for edit in literal['field_edits']:
                    keys, value = edit['field'].split('.'), api
                    for key in keys[:-1]:
                        value = value[key]
                    assert value[keys[-1]] == edit['old'], ('Source field/API projection mismatch', oid, edit['field'])
                    guards.append({'field': edit['field'], 'source_old': edit['old'], 'source_new': edit['new'], 'exact_old_match': True})
                    value[keys[-1]] = copy.deepcopy(edit['new'])
                for amendment in literal.get('evidence_rebinds', []):
                    before, after = amendment['old'], amendment['new']
                    assert before['object'] == after['object'] and before['role'] == after['role'] and before['note'] == after['note']
                    position = [i for i, edge in enumerate(api['evidence']) if edge == before]
                    assert len(position) == 1
                    api['evidence'][position[0]] = copy.deepcopy(after)
                for edge in literal.get('evidence_additions', []):
                    assert edge not in api['evidence']
                    api['evidence'].append(copy.deepcopy(edge))
                full[rid] = native
                rows.append({'object_id': oid, 'source_spec_pin': pin, 'source_row_pointer': '/rows/' + str(index),
                             'full_source_row': literal, 'full_old_native': native, 'full_old_API': old,
                             'source_new_API_projection_NOT_OPERATION': api, 'exact_field_guards': guards})
            ids.add(oid)
    assert len(rows) == 36 and len(reused) == 27
    assert sum(r['full_old_native'] is None for r in rows) == 5
    heads, issues, kinds = {}, [], dict(c.execute('select id,kind from object'))
    for index, row in enumerate(rows):
        api = row['source_new_API_projection_NOT_OPERATION']
        columns = [dict(v) for v in c.execute('pragma table_info("' + api['kind'] + '")') if v['name'] != 'revision_id']
        assert set(api['data']).issubset({v['name'] for v in columns})
        assert all(api['data'].get(v['name']) is not None for v in columns if v['notnull'])
        assert api['rationale'].strip()
        for edge in api['evidence']:
            version = heads.get(edge['object'])
            if version is None:
                current = c.execute('select max(version) from revision where object_id=?', (edge['object'],)).fetchone()[0]
                version = current
            if version != edge['version']:
                issues.append({'index': index, 'object_id': row['object_id'], 'edge': edge,
                               'actual_sequential_head': version, 'no_auto_rebind': True})
        heads[row['object_id']] = (api['expectedVersion'] or 0) + 1
        kinds[row['object_id']] = api['kind']
    incoming_by_rowid = {v['native_rowid']: copy.deepcopy(v) for v in previous['all_history_incoming']}
    full.update(previous['full_exact_and_current_incoming_caller_native'])
    added = []
    for row in rows:
        oid = row['object_id']
        if oid in prior:
            continue
        for edge in c.execute('select d.rowid as native_rowid,d.* from dependency d join revision r on r.id=d.basis_revision_id where r.object_id=? order by d.rowid', (oid,)):
            item = dict(edge)
            caller_oid = c.execute('select object_id from revision where id=?', (edge['revision_id'],)).fetchone()[0]
            current = h.current(c, caller_oid)
            item.update({'changed_target_object_id': oid, 'target_current_revision_id': h.current(c, oid),
                         'basis_is_current': edge['basis_revision_id'] == h.current(c, oid), 'caller_current_revision_id': current,
                         'caller_is_current': current == edge['revision_id'], 'individual_source_disposition': 'PENDING_ASTRA'})
            if edge['native_rowid'] in incoming_by_rowid:
                assert incoming_by_rowid[edge['native_rowid']] == item
            incoming_by_rowid[edge['native_rowid']] = item
            added.append(item)
            for rid in [edge['revision_id'], current]:
                full[rid] = h.native(c, rid)
    protected = h.readpin(previous['protected42_pin'])[1]['objects']
    assert len(protected) == 42 and not ids.intersection(n['object_id'] for n in protected.values())
    for rid, n in protected.items():
        assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
    media = modules[0]['media_registration_API']
    assert h.sha(R / media['storagePath']) == media['sha256'] and (R / media['storagePath']).stat().st_size == media['bytes']
    assert not c.execute('select id from native_asset where id=?', (media['id'],)).fetchone()
    for pin in SPECS:
        h.checked_pin_path(pin)
    h.checked_pin_path(proof['baseline_pin'])
    result = {'task': 'T-0788', 'status': 'FULL36_READONLY_GUARDS_PASS_INCOMING_SOURCE_DISPOSITION_PENDING' if not issues else 'FULL36_READONLY_CURRENT_GUARDS_COMPLETE_SUPPORT_HEAD_QUESTIONS_RETURNED',
              'source_spec_pins': SPECS, 'prior27_guard_pin': PRIOR, 'baseline_proof_pin': previous['baseline_proof_pin'],
              'actual_baseline_state': h.state(c), 'rows': rows, 'exact_prior27_full_old_reuse': reused,
              'additive_all_history_incoming': added, 'all_history_incoming': list(incoming_by_rowid.values()),
              'full_exact_and_current_incoming_caller_native': full, 'sequential_support_head_issues': issues,
              'literal744_media_registration_API_NOT_OPERATION': media,
              'protected42_whole_current_exact': True, 'protected42_target_intersection': [],
              'counts': {'targets': 36, 'existing_revisions': 31, 'new_objects': 5, 'reused_prior_targets': 27,
                         'additional_old_targets': 4, 'additional_incoming': len(added), 'all_incoming': len(incoming_by_rowid),
                         'head_issues': len(issues), 'media': 1}, 'source_grade_inferred': False,
              'operation_stage_canonical_Wotan_mutation': False, 'usage': 'UNKNOWN pending root collector'}
    pin = h.write(O / 'complete36-additive-whole-old-API-support-and-incoming-guard-NOT-OPERATION-v1.json', result)
    c.close()
    print(json.dumps({'guard_pin': pin, 'counts': result['counts'], 'support_head_issues': issues}))


if __name__ == '__main__':
    main()
