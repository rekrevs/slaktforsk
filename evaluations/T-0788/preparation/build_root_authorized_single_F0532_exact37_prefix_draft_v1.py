"""Root-released immutable single F532 draft plus unchanged exact36 prefix."""
import copy
import importlib.util
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
s = importlib.util.spec_from_file_location('h', R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py')
h = importlib.util.module_from_spec(s)
s.loader.exec_module(h)
d = importlib.util.spec_from_file_location('d', R / 'evaluations/T-0787/preparation/build_root_authorized_exact136_draft_v1.py')
diff = importlib.util.module_from_spec(d)
d.loader.exec_module(diff)
AUTH = {'path': 'evaluations/T-0788/root-authorized-single-F0532-exact37-draft-only-v1.json', 'sha256': '4e488273b819bf30bc6c541bea47f9a4387f27ea5f7e00aaf6a9b8e58e032000'}
OUT = R / 'evaluations/T-0788/implementation/exact37-prefix-plus-single-F0532-draft-v1'


def main():
    assert not OUT.exists(), 'Preserve existing candidate; no overwrite'
    auth = h.readpin(AUTH)[1]
    assert auth['root_authorized'] is True and auth['runtime_authorized'] is auth['canonical_authorized'] is auth['resolver_build_authorized'] is False
    source = h.readpin(auth['source_spec_pin'])[1]
    guard = h.readpin(auth['guard_pin'])[1]
    assert guard['guard_status'] == 'EXACT_F532_MAIN449_STAGE450_GUARDS_PASS' and guard['support_head_issues'] == []
    for key in ['primary_gate_pin', 'independent_gate_pin']:
        h.readpin(auth[key])
    literal = source['rows'][0]
    api = copy.deepcopy(h.pointer(source, auth['source_pointer']))
    assert api == guard['source_new_API_verified_NOT_OPERATION']
    initial_pin = source['package_amendment']['initial_proposal_pin']
    initial = h.readpin(initial_pin)[1]
    member36 = copy.deepcopy(initial['operations'][0])
    op36 = h.readpin(member36['operation_pin'])[1]
    prior_table = h.readpin(initial['consequence_table_pin'])[1]
    assert [r['full_new_API'] for r in prior_table['rows']] == op36['changes']
    assert len(prior_table['rows']) == 36 and api['id'] not in member36['target_ids']
    for label, key, state in [('MAIN449', 'main_pin', {'journal_head': 449, 'pending': 0}),
                              ('STAGE450', 'stage_pin', {'journal_head': 450, 'pending': 27})]:
        c = h.conn(h.checked_pin_path(auth[key]))
        assert h.state(c) == state
        assert h.current(c, api['id']) == literal['old_revision_id']
        assert h.native(c, literal['old_revision_id']) == literal['whole_old_native']
        assert guard['databases'][label]['database_pin'] == auth[key]
        assert guard['databases'][label]['all_history_incoming'] == []
        assert not c.execute('select id from operation where id=?', ('T-0788/exact-F0532-dated744-preservation-caveat-v1',)).fetchone()
        c.close()
    operation = {'id': 'T-0788/exact-F0532-dated744-preservation-caveat-v1',
                 'actor': 'Sol; exact separately source-approved F532 metadata scope under root draft-only authority',
                 'reason': 'T-0788: date the historical preservation snapshot for the already preserved folio744 only; retain all structured fields, old six bases and other source limits.',
                 'dependencyReviewVersion': 2, 'changes': [api]}
    OUT.mkdir(parents=True)
    op_pin = h.write(OUT / 'single-F0532-exact-caveat-correction-operation-v1.json', operation)
    memberF = {'operation_id': operation['id'], 'operation_pin': op_pin, 'target_ids': [api['id']]}
    rows = copy.deepcopy(prior_table['rows'])
    rows.append({'index': 36, 'object_id': api['id'], 'source_spec_pin': auth['source_spec_pin'], 'source_row_pointer': '/rows/0',
                 'full_source_disposition_row': literal, 'full_old_native': literal['whole_old_native'],
                 'full_old_API': literal['full_old_API'], 'full_new_API': api, 'old_revision_id': literal['old_revision_id'],
                 'new_revision_id': literal['new_revision_id'], 'field_differences': diff.diff(literal['full_old_API'], api),
                 'old6_evidence_dispositions': literal['old_evidence_dispositions'], 'all_history_incoming': [],
                 'raw_native_structured_text_retained': literal['whole_old_native']['data']['value_json'],
                 'source_grade_inferred': False})
    table_pin = h.write(OUT / 'all37-individual-whole-API-consequence-and-retain-table-v1.json', {
        'task': 'T-0788', 'rows': rows, 'initial36_consequence_table_pin': initial['consequence_table_pin'],
        'initial36_rows_whole_exact_unchanged': rows[:36] == prior_table['rows'],
        'prior28_individual_incoming': prior_table['all28_individual_incoming'],
        'F532_zero_incoming_guard_pin': auth['guard_pin'], 'primary_F532_disposition_pin': auth['primary_gate_pin'],
        'independent_F532_disposition_pin': auth['independent_gate_pin'], 'literal_media_registration_API': prior_table['media_registration_API'],
        'counts': {'targets': 37, 'revisions': 32, 'creates': 5, 'media': 1},
        'actual_request_instructions_not_renewed_or_built': True, 'stage_canonical_authorized': False})
    membership_pin = h.write(OUT / 'exact37-two-native-operation-membership-v1.json', {
        'task': 'T-0788', 'operations': [member36, memberF], 'operation_count': 2, 'target_count': 37,
        'revision_count': 32, 'create_count': 5, 'media_count': 1, 'initial36_membership_pin': initial['membership_pin'],
        'source_amendment_pin': auth['source_spec_pin']})
    format_pin = h.write(OUT / 'single-F0532-source-explicit-structured-value-projection-and-only-two-API-differences-v1.json', {
        'source_spec_pin': auth['source_spec_pin'], 'source_format_pointer': '/exact_format', 'literal_source_format': source['exact_format'],
        'native_old_structured_text': literal['whole_old_native']['data']['value_json'],
        'full_old_API': literal['full_old_API'], 'full_new_API': api,
        'only_caveat_and_ordered_one_context_append': True, 'old6_order_role_note_basis_retained': True})
    proof_pin = h.write(OUT / 'fresh-main449-stage450-and-exact36-prefix-single-F0532-byte-proof-v1.json', {
        'root_draft_authorization_pin': AUTH, 'helper_pin': h.pin(Path(__file__).resolve()), 'source_spec_pin': auth['source_spec_pin'],
        'mechanical_guard_pin': auth['guard_pin'], 'main_pin': auth['main_pin'], 'stage_pin': auth['stage_pin'],
        'initial36_package_pin': initial_pin, 'initial36_operation_pin': member36['operation_pin'],
        'initial36_ordered_member_whole_exact': member36 == initial['operations'][0],
        'single_F_API_exact_source_guard': True, 'protected42_disjoint_and_whole_current_exact': True,
        'MAIN_STAGE_CLI_Wotan_mutation': False, 'usage': 'UNKNOWN pending root collector'})
    proposal_pin = h.write(OUT / 'exact37-two-native-operation-package-proposal-v1.json', {
        'task': 'T-0788', 'membership_pin': membership_pin, 'operations': [member36, memberF], 'operation_count': 2,
        'target_count': 37, 'existing_revisions': 32, 'new_objects': 5, 'media_count': 1,
        'native_prefix_package_pin': initial_pin, 'correction_source_spec_pin': auth['source_spec_pin'],
        'correction_primary_readiness_pin': auth['primary_gate_pin'], 'correction_independent_readiness_pin': auth['independent_gate_pin'],
        'correction_mechanical_guard_pin': auth['guard_pin'], 'consequence_table_pin': table_pin,
        'source_format_pin': format_pin, 'mechanical_build_proof_pin': proof_pin,
        'built_byte_primary_approved': False, 'built_byte_independent_approved': False,
        'same_stage_correction_authorized': False, 'resolutions_constructed': False, 'canonical_authorized': False,
        'next_step': 'Both exact-built source/consequence byte gates, root separately authorizes at most one same-stage correction and renewed actual request capture.',
        'usage': 'UNKNOWN pending root collector'})
    for key in ['main_pin', 'stage_pin']:
        h.checked_pin_path(auth[key])
    h.checked_pin_path(member36['operation_pin'])
    print(json.dumps({'proposal_pin': proposal_pin, 'membership_pin': membership_pin, 'correction_operation_pin': op_pin,
                      'table_pin': table_pin, 'format_pin': format_pin, 'proof_pin': proof_pin, 'stage_canonical_UNRUN': True}))


if __name__ == '__main__':
    main()
