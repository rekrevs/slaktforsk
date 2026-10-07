"""UNRUN. Exact root-authorized MAIN apply or separate readonly postverification.

One CLI call only, no retries, database replacement, resolutions or administration.
"""
from pathlib import Path
import argparse, importlib.util, json, hashlib, subprocess, traceback

R = Path(__file__).resolve().parents[3]
T = R / 'evaluations/T-0786'
M = R / 'genealogy2/data/research.sqlite'
J = R / 'genealogy2/journal'
HELPER = R / 'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
EXPECTED = {
    'main_before': 'bef3080f01c220630ae8567618599195de52b82ddc1a8ef9199f4c57cc5fb8e1',
    'handoff': '5e4eecfe397bf37eb3fb7ee927a094b3c6939bc370320ed23c9754026715cb8b',
    'primary': '614cc301f4d60bb0a272ad0f79b8cee3c3a1454acef0572714ac0af30f073f95',
    'independent': '6a6091c12849b3b7bd77097e88963776e56dc2625f5014643a431dcbd8900873',
    'operation': 'a527c23ab1ce3bd0bb7844a44dc3fe4b60f71de859286e0ef22720bc00221e5c',
    'package': 'ee182ba52f68c41a8b073e93263713331d4c5abfc42beefb2929bfb64607445a',
    'stage': 'bf560a98675d357debe577fb1e3db4747cff79c5e59c78d1b1a1203e06b3a356',
    'baseline': '1e8e6b4079df557d9dd904578178321381b6c2ef5d54ac15ff74eacdac942541',
}

def main():
    assert __debug__, 'Assertions required'
    p = argparse.ArgumentParser()
    p.add_argument('--authorization', type=Path, required=True)
    p.add_argument('--authorization-sha256', required=True)
    p.add_argument('--phase', choices=['apply-and-verify', 'verify-only'], required=True)
    args = p.parse_args()
    ap = args.authorization.resolve()
    assert ap.is_relative_to(T) and sha(ap) == args.authorization_sha256
    auth = json.loads(ap.read_text())
    assert auth['task'] == 'T-0786' and auth['root_authorized'] is True
    assert auth['phase'] == args.phase
    assert auth['canonical_apply_authorized'] is (args.phase == 'apply-and-verify')
    assert auth['authorization'] == ('CONTROLLED_MAIN_POSTLOGIN_ONE_SEARCH_APPLY_ONCE' if args.phase == 'apply-and-verify' else 'READONLY_POSTLOGIN_MAIN447_VERIFICATION')
    assert auth['retry_authorized'] is False and auth['database_replacement_authorized'] is False
    assert auth['helper_pin']['sha256'] == sha(Path(__file__).resolve())
    assert (R / auth['helper_pin']['path']).resolve() == Path(__file__).resolve()
    assert auth['readonly_helper_pin']['sha256'] == sha(HELPER)
    assert (R / auth['readonly_helper_pin']['path']).resolve() == HELPER
    sp = importlib.util.spec_from_file_location('proven_readonly_functions', HELPER)
    h = importlib.util.module_from_spec(sp); sp.loader.exec_module(h)
    out = (R / auth['output_path']).resolve()
    assert out.is_relative_to(T) and not out.exists()
    out.mkdir()
    attempted = 0

    def checked(pin):
        path = (R / pin['path']).resolve()
        assert path.is_relative_to(R) and sha(path) == pin['sha256'], pin
        return path
    def load(pin): return json.loads(checked(pin).read_text())
    def save(name, value): return h.write(out / name, value)
    pins = [auth[k] for k in ['helper_pin', 'readonly_helper_pin', 'handoff_pin', 'primary_gate_pin', 'independent_gate_pin', 'operation_pin', 'package_pin', 'stage_DB_pin', 'baseline_DB_pin', 'protected42_pin', 'comparator_pin', 'fresh_root_baseline_receipt_pin']]
    pins += auth['additional_immutable_pins']
    def recheck():
        assert sha(ap) == args.authorization_sha256
        seen = {}
        for pin in pins:
            assert seen.setdefault(pin['path'], pin['sha256']) == pin['sha256']
            checked(pin)
    def protect(c, objects):
        for rid, n in objects.items():
            assert h.current(c, n['object_id']) == rid and h.native(c, rid) == n

    try:
        recheck()
        for key, name in [('handoff_pin','handoff'), ('primary_gate_pin','primary'), ('independent_gate_pin','independent'), ('operation_pin','operation'), ('package_pin','package'), ('stage_DB_pin','stage'), ('baseline_DB_pin','baseline')]:
            assert auth[key]['sha256'] == EXPECTED[name]
        assert auth['baseline_state'] == {'journal_head':446, 'pending':0}
        assert auth['final_state'] == {'journal_head':447, 'pending':0}
        assert load(auth['fresh_root_baseline_receipt_pin'])['fresh_baseline_verified'] is True
        hand = load(auth['handoff_pin']); pri = load(auth['primary_gate_pin']); own = load(auth['independent_gate_pin'])
        assert pri['ready_for_canonical'] is True and own['final_ready_for_canonical'] is True
        assert pri['operation_pin'] == own['operation'] == hand['operation_pin'] == auth['operation_pin']
        assert pri['package_pin'] == own['package'] == hand['package_pin'] == auth['package_pin']
        assert pri['stage_DB_pin'] == own['stage_DB'] == hand['stage_DB_pin'] == auth['stage_DB_pin']
        assert pri['actual_state'] == own['actual_state'] == hand['actual_state'] == auth['final_state']
        assert load(hand['actual_request_pin'])['requests'] == []
        pins += [hand['source_spec_pin'], hand['native_target_and_support_pin'], hand['actual_request_pin'], hand['full_all50_diff_pin'], *hand['validators']]
        code_paths = {v['path'] for v in auth['additional_immutable_pins']}
        assert {'genealogy2/cli.mjs','genealogy2/lib/domain.mjs','genealogy2/lib/store.mjs','genealogy2/lib/recovery.mjs'} <= code_paths
        recheck()
        op = load(auth['operation_pin']); x = op['changes'][0]
        assert op['id'] == 'T-0786/shared-Sodertalje-uppslag15-postlogin-access-note-v1'
        assert op['dependencyReviewVersion'] == 2 and len(op['changes']) == 1
        assert not set(op).intersection({'resolve','media','spans','mappings','unitDecisions'})
        assert x == load(hand['source_spec_pin'])['full_new_API']
        assert x['id'] == 'SEARCH-T0786-Sodertalje-uppslag15-postlogin-access' and x['kind'] == 'search' and x['expectedVersion'] is None
        assert auth['operations'] == [{'operation_id':op['id']}]  # Comparator permits only this new clock.
        basepath = checked(auth['baseline_DB_pin']); stagepath = checked(auth['stage_DB_pin'])
        assert basepath != M and stagepath != M
        base, live, stage = h.conn(basepath), h.conn(M), h.conn(stagepath)
        protected = load(auth['protected42_pin'])['objects']; assert len(protected) == 42
        try:
            before = h.all50(base)
            assert h.state(base) == auth['baseline_state'] and h.state(stage) == auth['final_state']
            protect(base, protected); protect(live, protected); protect(stage, protected)
            if args.phase == 'apply-and-verify':
                assert sha(M) == EXPECTED['main_before'] and h.all50(live) == before and h.state(live) == auth['baseline_state']
                assert not live.execute('select id from object where id=?',(x['id'],)).fetchone()
                assert not live.execute('select id from operation where id=?',(op['id'],)).fetchone()
                for e in x['evidence']: assert h.current(live, e['object']) == e['object']+'@'+str(e['version'])
                assert [dict(r) for r in live.execute('select * from pending_review')] == []
            prefix = [h.pin(f) for f in sorted(J.glob('*.json')) if int(f.name.split('-')[0]) <= 446]
            assert len(prefix) == 446
            save('fresh-before-and-journal-prefix.json', {'actual_state':h.state(live),'main_pin':h.pin(M),'baseline_all50':before,'journal_prefix':prefix,'protected42_exact':True,'authorization_pin':h.pin(ap)})
        finally: base.close(); live.close(); stage.close()
        if args.phase == 'apply-and-verify':
            recheck()
            for v in prefix: checked(v)
            attempted += 1
            h.run_cli(['apply',str(checked(auth['operation_pin'])),'--db',str(M),'--journal',str(J)],out/'apply.stdout.json')
        c = h.conn(M)
        try:
            assert h.state(c) == auth['final_state']
            stored = dict(c.execute('select p.*,o.request_hash,o.recorded_at from operation_payload p join operation o on o.id=p.operation_id where p.operation_id=?',(op['id'],)).fetchone())
            assert stored['sequence'] == 447 and json.loads(stored['request_json']) == op
            f = J / ('000000447-'+stored['request_hash']+'.json'); env = json.loads(f.read_text())
            assert env['request'] == op and env['sequence'] == 447 and env['requestHash'] == stored['request_hash'] and env['recordedAt'] == stored['recorded_at'] and env['policy'] == stored['policy']
            assert len(list(J.glob('*.json'))) == 447
            for v in prefix: checked(v)
            full = load(hand['native_target_and_support_pin'])
            for n in [full['target'],*full['source_support_objects'].values()]: assert h.native(c,n['id']) == n
            protect(c, protected)
            after = h.all50(c)
            save('actual447-entire-stored-request-and-native.json', {'actual_state':h.state(c),'stored':stored,'journal_pin':h.pin(f),'envelope':env,'new_API_and_ordered_supports_equal_reviewed_stage':True,'protected42_exact':True})
        finally: c.close()
        comparator = checked(auth['comparator_pin'])
        assert comparator == (T/'implementation/compare_root_applied_one_search_to_reviewed_stage_v1.py').resolve()
        cmd = ['python',str(comparator),'--stage',str(stagepath),'--gate',str(ap),'--output',str(out/'all50-reviewed-stage-versus-actual.json')]
        result = subprocess.run(cmd,cwd=R,text=True,capture_output=True)
        (out/'comparison.stdout.txt').write_text(result.stdout); (out/'comparison.stderr.txt').write_text(result.stderr)
        save('comparison.process.json', {'argv':cmd,'exit_code':result.returncode}); assert result.returncode == 0
        assert json.loads((out/'all50-reviewed-stage-versus-actual.json').read_text())['pass'] is True
        validators = []
        for name,cmd in [('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source']),('inventory',['inventory']),('P-0269-verified-pedigree',['pedigree','P-0269']),('P-0270-verified-pedigree',['pedigree','P-0270'])]:
            got = h.run_cli(cmd,out/(name+'.json'))
            if name.startswith('verify'): assert got['ok'] is True
            else:
                ref = next(pin for pin in hand['validators'] if Path(pin['path']).name == name+'.json' or (name=='inventory' and Path(pin['path']).name=='inventory.json'))
                assert got == load(ref)
            validators.append(h.pin(out/(name+'.json')))
        recheck()
        c = h.conn(M)
        try: assert h.state(c) == auth['final_state'] and h.all50(c) == after
        finally: c.close()
        final = save('complete-postlogin-one-search-actual447-handoff.json', {'task':'T-0786','authorization_pin':h.pin(ap),'actual_state':auth['final_state'],'main_pin':h.pin(M),'operation_pin':auth['operation_pin'],'package_pin':auth['package_pin'],'stage_DB_pin':auth['stage_DB_pin'],'all50_comparison_pin':h.pin(out/'all50-reviewed-stage-versus-actual.json'),'validators':validators,'actual_CLI_calls':attempted,'no_Wotan_administration_or_task_DONE':True,'usage':'UNKNOWN pending root collector'})
        print(json.dumps({'handoff_pin':final,'actual_state':auth['final_state']}))
    except BaseException as e:
        c = h.conn(M)
        try: state = h.state(c)
        finally: c.close()
        save('STOP-no-retry-actual-state.json', {'error':repr(e),'traceback':traceback.format_exc(),'actual_state':state,'main_pin':h.pin(M),'actual_CLI_calls':attempted,'no_retry_no_DB_replace':True})
        raise

if __name__ == '__main__': main()
