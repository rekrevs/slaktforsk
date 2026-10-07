"""Readonly finite27 exact source field/API/head/incoming guard. No operation or grade."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
S = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(S)
S.loader.exec_module(h)
O = Path(__file__).resolve().parent
PIN = {'path': 'evaluations/T-0787/preparation/fresh447-physical-backup-full50-logical-equality-and-protected42-proof-v1.json', 'sha256': 'b26805071faa41f0d5abf982b87c80202831a058a378890c7425b540e095161c'}
SPEC = [
    {'path': 'evaluations/T-0788/source-review/exact744-core-three-and-six-small-source-field-spec-v1.json', 'sha256': '380c6b0bec3028f0dad203d874a0fe7e38428e26fd208f6fcf9a495d358cb4c4'},
    {'path': 'evaluations/T-0788/source-review/finite-eighteen-current744-semantic-copy-exact-field-spec-v3.json', 'sha256': 'dbcce57329f7d42f439e02254e7a96403db0213babd49b9ef4f055860dbdfd3a'}]


def main():
    proof = h.readpin(PIN)[1]
    bp = h.checked_pin_path(proof['baseline_pin'])
    c = h.conn(bp)
    assert h.state(c) == {'journal_head': 447, 'pending': 0}
    rows, byid, issues, full = [], {}, [], {}
    for pin in SPEC:
        module = h.readpin(pin)[1]
        if module.get('order'):
            assert module['order'] == [r['object_id'] for r in module['rows']]
        for index, literal in enumerate(module['rows']):
            oid, version = literal['object_id'], literal['expected_version']
            rid = oid + '@' + str(version)
            assert oid not in byid and h.current(c, oid) == rid
            n = h.native(c, rid)
            assert n == literal['whole_old_native'], ('Whole old mismatch', oid)
            full[rid] = n
            old = h.api(n)
            old['expectedVersion'] = version
            new = copy.deepcopy(old)
            field_guards = []
            for edit in literal['field_edits']:
                keys = edit['field'].split('.')
                value = new
                for key in keys[:-1]:
                    value = value[key]
                assert value[keys[-1]] == edit['old'], ('Exact field/projection mismatch', oid, edit['field'])
                field_guards.append({'field': edit['field'], 'old_API': value[keys[-1]], 'source_old': edit['old'], 'source_new': edit['new'], 'match': True})
                value[keys[-1]] = copy.deepcopy(edit['new'])
            for amendment in literal.get('evidence_rebinds', []):
                before, after = amendment['old'], amendment['new']
                assert before['object'] == after['object'] and before['role'] == after['role'] and before['note'] == after['note']
                positions = [i for i, edge in enumerate(new['evidence']) if edge == before]
                assert len(positions) == 1, ('No exact singleton rebind', oid, before)
                new['evidence'][positions[0]] = copy.deepcopy(after)
            for edge in literal.get('evidence_additions', []):
                assert edge not in new['evidence']
                new['evidence'].append(copy.deepcopy(edge))
            row = {'object_id': oid, 'source_spec_pin': pin, 'source_row_pointer': '/rows/' + str(index), 'whole_source_disposition_row': literal,
                   'full_old_native': n, 'full_old_API': old, 'source_new_API_projection_NOT_OPERATION': new, 'literal_field_guards': field_guards}
            rows.append(row)
            byid[oid] = row
    assert len(rows) == 27
    heads = {}
    for index, row in enumerate(rows):
        api = row['source_new_API_projection_NOT_OPERATION']
        for edge in api['evidence']:
            version = heads.get(edge['object'])
            if version is None:
                version = int(h.current(c, edge['object']).rsplit('@', 1)[1])
            if version != edge['version']:
                issues.append({'index': index, 'object_id': row['object_id'], 'edge': edge, 'actual_sequential_current_head': version, 'requires_source_disposition_no_substitution': True})
        heads[row['object_id']] = api['expectedVersion'] + 1
    incoming = []
    for row in rows:
        oid = row['object_id']
        for edge in c.execute('select d.rowid as native_rowid,d.* from dependency d join revision r on r.id=d.basis_revision_id where r.object_id=? order by d.rowid', (oid,)):
            item = dict(edge)
            caller_oid = c.execute('select object_id from revision where id=?', (edge['revision_id'],)).fetchone()[0]
            current = h.current(c, caller_oid)
            item.update({'changed_target_object_id': oid, 'target_current_revision_id': h.current(c, oid),
                         'basis_is_current': edge['basis_revision_id'] == h.current(c, oid), 'caller_current_revision_id': current,
                         'caller_is_current': current == edge['revision_id'], 'individual_source_disposition': 'PENDING_ASTRA'})
            incoming.append(item)
            for rid in [edge['revision_id'], current]:
                if rid not in full:
                    full[rid] = h.native(c, rid)
    protected_pin = h.pin(R / 'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json')
    protected = h.readpin(protected_pin)[1]['objects']
    assert len(protected) == 42 and not set(byid).intersection(n['object_id'] for n in protected.values())
    for rid, n in protected.items():
        assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n
    for pin in SPEC:
        h.checked_pin_path(pin)
    h.checked_pin_path(proof['baseline_pin'])
    result = {'task': 'T-0788', 'status': 'EXACT27_OLD_FIELDS_AND_INCOMING_READONLY_GUARD_COMPLETE_SOURCE_HEAD_ISSUES_RETURNED' if issues else 'EXACT27_OLD_FIELDS_AND_ORDERED_SUPPORT_GUARDS_PASS_INCOMING_PENDING_INDIVIDUAL_ASTRA',
              'source_spec_pins': SPEC, 'baseline_proof_pin': PIN, 'baseline_state': h.state(c), 'rows': rows,
              'all_history_incoming': incoming, 'full_exact_and_current_incoming_caller_native': full,
              'sequential_support_head_issues': issues, 'counts': {'targets': 27, 'core': 9, 'finite': 18, 'all_history_incoming': len(incoming),
              'unique_native_dependency_rowids': len({e['native_rowid'] for e in incoming}), 'support_head_issues': len(issues)},
              'protected42_pin': protected_pin, 'protected42_target_intersection': [], 'protected42_whole_current_exact': True,
              'source_grade_inferred': False, 'operations_constructed': False, 'stage_canonical_Wotan_mutation': False,
              'usage': 'UNKNOWN pending root collector'}
    pin = h.write(O / 'exact27-whole-old-source-field-API-order-and-all-history-incoming-readonly-guard-v1.json', result)
    c.close()
    print(json.dumps({'guard_pin': pin, 'counts': result['counts'], 'issues': issues}))


if __name__ == '__main__':
    main()
