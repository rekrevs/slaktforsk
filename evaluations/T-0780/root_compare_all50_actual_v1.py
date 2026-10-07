"""Read-only all-table comparison; preserve bytes and JSON array strings exactly."""
import datetime, hashlib, json, pathlib, sqlite3

B = pathlib.Path(__file__).resolve().parent
R = B.parents[1]
gate = json.loads((B / 'root-controlled-canonical-exact144-authorization-v1.json').read_text())
new_ids = {x['operation_id'] for x in gate['operations']}

def connect(path):
    c = sqlite3.connect('file:' + str(path.resolve()) + '?mode=ro', uri=True)
    c.row_factory = sqlite3.Row
    return c

def encoded(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True,
                      default=lambda b: {'binary_hex': b.hex()})

def rows(c, t):
    return sorted([dict(r) for r in c.execute('select * from "' + t + '"')], key=encoded)

stage = connect(B / 'full10-stage-final143-v1/stage.sqlite')
live = connect(R / 'genealogy2/data/research.sqlite')
schema = "select name,sql from sqlite_master where type='table' and name not like 'sqlite_%' order by name"
assert [tuple(x) for x in stage.execute(schema)] == [tuple(x) for x in live.execute(schema)]
checks, clocks = [], []
for name, _ in stage.execute(schema):
    a, z = rows(stage, name), rows(live, name)
    if name == 'operation':
        am, zm = {x['id']: x for x in a}, {x['id']: x for x in z}
        assert set(am) == set(zm)
        for oid in am:
            s, l = am[oid].copy(), zm[oid].copy()
            st, lt = s.pop('recorded_at'), l.pop('recorded_at')
            assert s == l
            if st != lt:
                assert oid in new_ids, 'Older operation timestamp changed'
                clocks.append({'operation_id': oid, 'stage_recorded_at': st, 'actual_recorded_at': lt})
        equal = True
    else:
        equal = a == z  # Original SQLite values, including exact binary bytes.
    assert equal, name
    checks.append({'table': name, 'rows': len(a), 'pass': equal})
assert len(checks) == 50
ordered = []
for t in ['dependency', 'origin', 'record_asset', 'record_media', 'review_resolution']:
    sql = 'select rowid,* from ' + t + ' order by rowid'
    a = [dict(x) for x in stage.execute(sql)]
    z = [dict(x) for x in live.execute(sql)]
    assert a == z
    ordered.append({'table': t, 'rows': len(a), 'exact_insertion_order': True})
state = {'journal_head': live.execute('select max(sequence) from operation_payload').fetchone()[0],
         'pending': live.execute('select count(*) from pending_review').fetchone()[0]}
assert state == gate['final_state'] == {'journal_head': 425, 'pending': 0}
out = B / 'canonical-actual-full50-and-ordered-native-comparison-v1.json'
assert not out.exists()
result = {'task': 'T-0780', 'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'all50_schema_and_rows_compared': True, 'checks': checks,
          'recorded_at_clock_differences': clocks,
          'clock_scope': 'Only runtime recorded_at for exact144 new operations. All other operation fields and every older timestamp exact.',
          'ordered_native_tables': ordered, 'actual_canonical_state': state, 'pass': True,
          'binary_handling': 'Lossless hex only in SQL row sort key; original bytes compared directly. JSON column strings and arrays unchanged.',
          'initial_readonly_attempt_failure': 'JSON sort-key encoder lacked bytes handler; TypeError before proof output, no database mutation.'}
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
stage.close()
live.close()
print(json.dumps({'all50_PASS': True, 'runtime_clock_differences': len(clocks), 'actual_state': state}))
