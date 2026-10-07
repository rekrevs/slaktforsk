"""One root-authorized fresh sequential clone stage. Never canonical or resolutions.

UNRUN preparation. Root supplies immutable authorization plus exact gate JSON pointers.
Every mutation is solely the whitelisted CLI apply to an absent task-local clone.
"""
import argparse
import copy
import datetime
import hashlib
import json
import shutil
import sqlite3
import subprocess
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / 'evaluations/T-0781'
MAIN = ROOT / 'genealogy2/data/research.sqlite'
ORDER_TABLES = ('origin', 'dependency', 'record_asset', 'record_media')
DERIVED = {'object_search', 'object_search_config', 'object_search_content',
           'object_search_data', 'object_search_docsize', 'object_search_idx'}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def readpin(pin):
    p = (ROOT / pin['path']).resolve()
    assert p.is_relative_to(ROOT) and sha(p) == pin['sha256'], pin
    return p, json.loads(p.read_text())


def pin(path):
    return {'path': str(Path(path).relative_to(ROOT)), 'sha256': sha(path)}


def pointer(value, path):
    for key in path.strip('/').split('/') if path else []:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def write(path, value):
    assert not path.exists(), ('Preserve existing artifact', path)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return pin(path)


def conn(path):
    c = sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)
    c.row_factory = sqlite3.Row
    return c


def state(c):
    return {'journal_head': c.execute('select max(sequence) from operation_payload').fetchone()[0],
            'pending': c.execute('select count(*) from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null').fetchone()[0]}


def encode(x):
    return {'bytes_hex': x.hex()} if isinstance(x, bytes) else x


def rows(c, table, rowid=False, maximum=None):
    sql = 'select ' + ('rowid as _native_rowid,*' if rowid else '*') + ' from "' + table + '"'
    params = ()
    if maximum is not None:
        sql += ' where rowid<=?'
        params = (maximum,)
    if rowid:
        sql += ' order by rowid'
    return [[encode(v) for v in r] for r in c.execute(sql, params)]


def row_digest(items, ordered):
    serialized = [json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in items]
    if not ordered:
        serialized.sort()
    return hashlib.sha256(('\n'.join(serialized) + '\n').encode()).hexdigest()


def all50(c):
    schema = [list(r) for r in c.execute("select type,name,tbl_name,sql from sqlite_master where sql is not null order by type,name")]
    names = [r[0] for r in c.execute("select name from sqlite_master where type='table' order by name")]
    assert len(names) == 50
    tables = {}
    for name in names:
        rs = rows(c, name)
        tables[name] = {'rows': len(rs), 'sha256': row_digest(rs, False)}
    return {'schema': schema, 'tables': tables,
            'ordered_native_arrays': {n: row_digest(rows(c, n, True), True) for n in ORDER_TABLES}}


def native(c, rid):
    r = c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?', (rid,)).fetchone()
    assert r is not None, rid
    n = dict(r)
    n['data'] = dict(c.execute('select * from ' + n['kind'] + ' where revision_id=?', (rid,)).fetchone())
    for key, table in [('origins', 'origin'), ('evidence', 'dependency')] + ([('assets', 'record_asset'), ('media', 'record_media')] if n['kind'] == 'record' else []):
        n[key] = [dict(x) for x in c.execute('select * from ' + table + ' where revision_id=? order by rowid', (rid,))]
    return n


def current(c, oid):
    r = c.execute('select id from revision where object_id=? order by version desc limit 1', (oid,)).fetchone()
    assert r is not None, oid
    return r[0]


def api(n):
    a = {'id': n['object_id'], 'kind': n['kind'], 'expectedVersion': n['version'] - 1 or None,
         'data': {k: json.loads(v) if k.endswith('_json') and isinstance(v, str) else v for k, v in n['data'].items() if k != 'revision_id'},
         'origins': [{'unit': x['unit_id'], 'coverage': x['coverage'], 'note': x['note']} for x in n['origins']],
         'evidence': [{'object': x['basis_revision_id'].rsplit('@', 1)[0], 'version': int(x['basis_revision_id'].rsplit('@', 1)[1]), 'role': x['role'], 'note': x['note']} for x in n['evidence']],
         'disposition': n['disposition'], 'evidenceStatus': n['evidence_status'], 'rationale': n['rationale'], 'caveat': n['caveat']}
    if n['kind'] == 'record':
        a['assets'] = [{'path': x['asset_path'], 'region': x['region']} for x in n['assets']]
        a['media'] = [{'id': x['asset_id'], 'region': x['region']} for x in n['media']]
    return a


def expected_defaults(x, actual):
    # Same explicitly recorded domain defaults as T0780, never sort an array.
    y = copy.deepcopy(x)
    for key, default in [('origins', []), ('evidence', []), ('evidenceStatus', None), ('caveat', '')]:
        y.setdefault(key, default)
    for key in actual['data']:
        y['data'].setdefault(key, None)
    for key in ['origins', 'evidence']:
        for edge in y[key]:
            edge.setdefault('note', '')
            if key == 'origins':
                edge.setdefault('coverage', 'partial')
    if x['kind'] == 'record':
        for key in ['assets', 'media']:
            y.setdefault(key, [])
            for edge in y[key]:
                edge.setdefault('region', 'helbild')
    return y


def gatecheck(spec, proposal_sha, membership_sha):
    _, g = readpin(spec['pin'])
    assert pointer(g, spec['ready_pointer']) is True
    assert pointer(g, spec['proposal_sha_pointer']) == proposal_sha
    assert pointer(g, spec['membership_sha_pointer']) == membership_sha


def run_cli(args, output):
    command = ['node', str(ROOT / 'genealogy2/cli.mjs'), *args]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    output.write_text(result.stdout)
    output.with_suffix('.stderr.txt').write_text(result.stderr)
    write(output.with_suffix('.process.json'), {'argv': command, 'returncode': result.returncode,
                                              'stdout_pin': pin(output), 'stderr_pin': pin(output.with_suffix('.stderr.txt'))})
    assert result.returncode == 0, ('CLI failed; stop, no retry', args, result.stderr)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--authorization', type=Path, required=True)
    parser.add_argument('--authorization-sha256', required=True)
    args = parser.parse_args()
    ap = args.authorization.resolve()
    assert sha(ap) == args.authorization_sha256
    authorization = json.loads(ap.read_text())
    assert authorization['authorization'] == 'ONE_FRESH_EXACT16_SEQUENTIAL_CLONE_STAGE_ONLY'
    assert authorization['root_authorized'] is True and authorization['canonical_apply_authorized'] is False
    assert authorization['resolution_apply_authorized'] is False
    assert authorization['helper_pin'] == pin(Path(__file__).resolve())
    pp, proposal = readpin(authorization['proposal_pin'])
    mp, membership = readpin(authorization['membership_pin'])
    assert proposal['membership_pin'] == authorization['membership_pin']
    assert proposal['operations'] == membership['operations']
    members = membership['operations']
    assert len(members) == 16 and sum(m['changes'] for m in members) == 174
    for role in ['primary_gate', 'independent_prestage_gate']:
        gatecheck(authorization[role], sha(pp), sha(mp))
    assert authorization['primary_gate']['pin']['path'] != authorization['independent_prestage_gate']['pin']['path']
    readpin(authorization['fresh_baseline_receipt_pin'])
    baseline_path = (ROOT / authorization['baseline_pin']['path']).resolve()
    assert baseline_path.is_relative_to(TASK) and sha(baseline_path) == authorization['baseline_pin']['sha256']
    assert authorization['main_pin']['path'] == 'genealogy2/data/research.sqlite'
    assert sha(MAIN) == authorization['main_pin']['sha256']
    for p in authorization['review_pins']:
        readpin(p)
    for p in authorization['media_pins']:
        assert sha(ROOT / p['path']) == p['sha256']
    ops = []
    ids = set()
    base = conn(baseline_path)
    live = conn(MAIN)
    assert state(base) == state(live) == {'journal_head': 425, 'pending': 0}
    before = all50(base)
    assert all50(live) == before
    heads = dict(base.execute('select object_id,max(version) from revision group by object_id'))
    # CLI requires CURRENT heads, not merely existence of an old revision.
    for m in members:
        path, op = readpin(m)
        assert op['id'] == m['operation_id'] and op['dependencyReviewVersion'] == 2
        assert len(op['changes']) == m['changes'] and not set(op).intersection({'resolve', 'media', 'spans', 'mappings', 'unitDecisions'})
        assert base.execute('select count(*) from operation where id=?', (op['id'],)).fetchone()[0] == 0
        for x in op['changes']:
            assert x['id'] not in ids and heads.get(x['id']) == x['expectedVersion']
            ids.add(x['id'])
            for e in x['evidence']:
                assert heads.get(e['object']) == e['version'], ('Source/version disposition required before stage', x['id'], e)
            heads[x['id']] = (x['expectedVersion'] or 0) + 1
        ops.append((path, op))
    assert len(ids) == 174
    _, protected_input = readpin(authorization['protected42_pin'])
    protected = protected_input['objects']
    assert len(protected) == 42
    for rid, n in protected.items():
        assert native(base, rid) == n == native(live, rid) and n['object_id'] not in ids
    stage = (ROOT / authorization['stage_path']).resolve()
    assert stage.is_relative_to(TASK) and not stage.exists() and stage != baseline_path and stage != MAIN
    stage.mkdir()
    db = stage / 'stage.sqlite'
    shutil.copyfile(baseline_path, db)
    assert sha(db) == authorization['baseline_pin']['sha256']
    journal = stage / 'journal'
    journal.mkdir()
    write(stage / 'authorization.json', authorization)
    write(stage / 'baseline-all50-state.json', before)
    write(stage / 'protected42-before.json', protected)
    steps = []
    try:
        for i, (path, op) in enumerate(ops, 1):
            assert sha(ap) == args.authorization_sha256 and sha(MAIN) == authorization['main_pin']['sha256']
            assert sha(pp) == authorization['proposal_pin']['sha256'] and sha(mp) == authorization['membership_pin']['sha256']
            for role in ['primary_gate', 'independent_prestage_gate']:
                gatecheck(authorization[role], sha(pp), sha(mp))
            assert sha(path) == members[i - 1]['sha256']
            c = conn(db)
            prior = state(c)
            assert prior['journal_head'] == 424 + i
            if steps:
                assert prior == steps[-1]['after']
            c.close()
            receipt = {'step': i, 'operation_pin': pin(path), 'operation_id': op['id'], 'before': prior}
            write(stage / f'step-{i:02}-actual-before.json', receipt)
            try:
                run_cli(['apply', str(path), '--db', str(db), '--journal', str(journal)], stage / f'step-{i:02}-apply.json')
            finally:
                c = conn(db)
                receipt['after'] = state(c)
                c.close()
                write(stage / f'step-{i:02}-actual-before-after.json', receipt)
            assert receipt['after']['journal_head'] == prior['journal_head'] + 1
            assert receipt['after']['pending'] >= prior['pending']
            c = conn(db)
            stored = c.execute('select * from operation_payload where operation_id=?', (op['id'],)).fetchone()
            assert json.loads(stored['request_json']) == op, ('Unexpected request normalization; stop', op['id'])
            for rid, n in protected.items():
                assert current(c, n['object_id']) == rid and native(c, rid) == n
            c.close()
            steps.append(receipt)
        c = conn(db)
        final_state = state(c)
        assert final_state['journal_head'] == 441
        after = all50(c)
        write(stage / 'stage-all50-state.json', after)
        assert after['schema'] == before['schema']
        preserved = {}
        for name in before['tables']:
            if name in DERIVED:
                continue
            # All existing physical knowledge/review rows remain exact; new rows append.
            limit = base.execute('select max(rowid) from "' + name + '"').fetchone()[0]
            oldrows = rows(base, name, True)
            got = rows(c, name, True, limit) if limit is not None else []
            assert got == oldrows, ('Existing native/history/review row modified', name)
            preserved[name] = {'existing_rows_exact': True, 'existing_order_digest': row_digest(oldrows, True)}
        assert rows(c, 'review_resolution', True) == rows(base, 'review_resolution', True)
        assert after['tables']['asset'] == before['tables']['asset'] and after['tables']['native_asset'] == before['tables']['native_asset']
        # Narrow derived-search exemption only: actual current rows must equal domain.indexObject.
        untouched_before = [list(r) for r in base.execute('select object_id,kind,text from object_search order by object_id') if r['object_id'] not in ids]
        untouched_after = [list(r) for r in c.execute('select object_id,kind,text from object_search order by object_id') if r['object_id'] not in ids]
        assert untouched_before == untouched_after
        search_rows = []
        for oid in ids:
            n = native(c, current(c, oid))
            expected = '\n'.join(str(x) for x in [oid, n['disposition'], n['evidence_status'], n['rationale'], n['caveat'], *n['data'].values()] if x is not None)
            got = [dict(r) for r in c.execute('select object_id,kind,text from object_search where object_id=?', (oid,))]
            assert got == [{'object_id': oid, 'kind': n['kind'], 'text': expected}]
            search_rows.append({'object_id': oid, 'exact_current_domain_index_text': True})
        write(stage / 'existing-native-history-order-and-narrow-derived-search-proof.json', {'tables': preserved, 'derived_only': sorted(DERIVED), 'untouched_search_rows_exact': True, 'touched_current_search_rows': search_rows})
        pool, origins = {}, {}
        def add(rid):
            if rid in pool:
                return rid
            n = native(c, rid)
            pool[rid] = n
            for edge in n['origins']:
                u = c.execute('select * from unit where id=?', (edge['unit_id'],)).fetchone()
                assert u is not None
                origins[edge['unit_id']] = dict(u)
            for edge in n['evidence']:
                add(edge['basis_revision_id'])
            return rid
        targets, targetproof = {}, []
        for path, op in ops:
            for i, x in enumerate(op['changes']):
                rid = x['id'] + '@' + str((x['expectedVersion'] or 0) + 1)
                add(rid)
                targets[rid] = pool[rid]
                actual = api(pool[rid])
                expected = expected_defaults(x, actual)
                write(stage / ('target-proof-' + str(len(targetproof) + 1).zfill(3) + '.json'), {'revision_id': rid, 'actual_full_API': actual, 'approved_input_API': x, 'explicit_domain_defaulted_expected_API': expected, 'arrays_not_sorted': True})
                assert actual == expected, ('Actual ordered API differs', rid)
                history = [r[0] for r in c.execute('select id from revision where object_id=? order by version', (x['id'],))]
                for oldrid in history:
                    add(oldrid)
                targetproof.append({'revision_id': rid, 'operation_pin': pin(path), 'input_pointer': '/changes/' + str(i), 'whole_API_exact': True, 'ordered_history': history})
        pending = [dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')]
        assert len(pending) == final_state['pending']
        requests = []
        for q in pending:
            ar, cr = add(q['affected_revision_id']), add(q['changed_revision_id'])
            ac, cc = add(current(c, pool[ar]['object_id'])), add(current(c, pool[cr]['object_id']))
            previous = pool[cr]['previous_id']
            if previous:
                add(previous)
            histories = {}
            for rid in [ar, cr]:
                hs = [r[0] for r in c.execute('select id from revision where object_id=? order by version', (pool[rid]['object_id'],))]
                histories[pool[rid]['object_id']] = hs
                for h in hs:
                    add(h)
            requests.append({'actual_request': q, 'affected_exact_revision_id': ar, 'affected_current_revision_id': ac, 'changed_exact_revision_id': cr, 'changed_current_revision_id': cc, 'changed_previous_revision_id': previous, 'full_histories': histories, 'primary_and_independent_individual_grade': 'PENDING', 'automatic_rebind_or_resolution': False})
        old_payloads = {}
        for rid, n in pool.items():
            if base.execute('select id from revision where id=?', (rid,)).fetchone():
                assert n == native(base, rid)
                old_payloads[rid] = n
        nativepin = write(stage / 'complete-actual-target-request-history-upstream-native-payloads.json', {'objects': pool, 'origin_units': origins, 'order': 'All native evidence/origins/assets/media ORDER BY rowid; JSON source arrays unchanged'})
        targetpin = write(stage / 'all174-actual-full-native-targets-and-exact-API-bindings.json', {'objects': targets, 'target_proofs': targetproof, 'all174_complete': len(targets) == 174})
        requestpin = write(stage / 'all-actual-individual-request-and-complete-dependency-context-routing.json', {'native_pin': nativepin, 'requests': requests, 'actual_pending_count': len(pending), 'full_dependency_subgraph': {rid: n['evidence'] for rid, n in pool.items()}, 'no_source_grade': True})
        baselinepin = write(stage / 'all-existing-actual-context-payloads-exact-baseline-equality.json', {'objects': old_payloads, 'all_full_native_fields_and_rowid_array_order_equal_baseline': True})
        write(stage / 'all-operation-payloads.json', [dict(r) for r in c.execute('select * from operation_payload order by sequence')])
        write(stage / 'protected42-after.json', {rid: native(c, rid) for rid in protected})
        c.close()
        validators = []
        for cmd in ['verify', 'verify-assets', 'verify-source', 'inventory']:
            output = stage / (cmd + '.json')
            run_cli([cmd, '--db', str(db), '--journal', str(journal)], output)
            validators.append(pin(output))
        output = stage / 'pedigree-verified-P0269.json'
        run_cli(['pedigree', 'P-0269', '--db', str(db)], output)
        validators.append(pin(output))
        assert all50(live) == before and sha(MAIN) == authorization['main_pin']['sha256']
        for p in authorization['media_pins']:
            assert sha(ROOT / p['path']) == p['sha256']
        for p in authorization['review_pins']:
            readpin(p)
        c = conn(db)
        assert state(c) == final_state
        c.close()
        write(stage / 'complete-stage-result-and-Astra-handoff.json', {'task': 'T-0781', 'authorization_pin': pin(ap), 'proposal_pin': pin(pp), 'membership_pin': pin(mp), 'actual_state': final_state, 'operation_count': 16, 'actual_target_count': 174, 'actual_request_context_native_pin': nativepin, 'all174_native_API_binding_pin': targetpin, 'actual_individual_request_pin': requestpin, 'old_context_baseline_equality_pin': baselinepin, 'stage_DB_pin': pin(db), 'validators': validators, 'protected42_exact': True, 'live_all50_exact_and_main_SHA_unchanged': True, 'individual_request_source_and_independent_grades_required': True, 'resolutions_applied': 0, 'canonical_apply': False, 'actual_program_acceptance': False})
    except BaseException as error:
        c = conn(db)
        actual = state(c)
        c.close()
        write(stage / 'failure-stop-preserved-actual-state.json', {'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(), 'actual_state': actual, 'stage_DB_pin': pin(db), 'completed_steps': steps, 'no_retry_no_newclone_no_resolutions': True})
        raise
    finally:
        base.close()
        live.close()


if __name__ == '__main__':
    main()
