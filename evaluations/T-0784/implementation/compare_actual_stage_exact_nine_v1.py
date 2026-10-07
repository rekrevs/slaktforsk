"""Compare approved stage with MAIN without normalizing native values or order."""
import argparse
import datetime
import json
from pathlib import Path
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('--stage', type=Path, required=True)
parser.add_argument('--gate', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
assert not args.output.exists()
gate = json.loads(args.gate.read_text())
new_ids = {item['operation_id'] for item in gate['operations']}

def connect(path):
    connection = sqlite3.connect('file:' + str(path.resolve()) + '?mode=ro', uri=True)
    connection.row_factory = sqlite3.Row
    return connection

def sort_key(row):
    return json.dumps(row, ensure_ascii=False, sort_keys=True,
                      default=lambda value: {'binary_hex': value.hex()})

def rows(connection, table):
    return sorted((dict(row) for row in connection.execute('SELECT * FROM "' + table + '"')),
                  key=sort_key)

stage = connect(args.stage)
live = connect(Path('genealogy2/data/research.sqlite'))
schema_sql = "SELECT name,sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
schema = [tuple(row) for row in stage.execute(schema_sql)]
assert schema == [tuple(row) for row in live.execute(schema_sql)]
assert len(schema) == 50
checks, clocks = [], []
for table, _ in schema:
    expected, actual = rows(stage, table), rows(live, table)
    if table == 'operation':
        expected_by_id = {row['id']: row for row in expected}
        actual_by_id = {row['id']: row for row in actual}
        assert expected_by_id.keys() == actual_by_id.keys()
        for operation_id, expected_row in expected_by_id.items():
            left, right = expected_row.copy(), actual_by_id[operation_id].copy()
            stage_clock, actual_clock = left.pop('recorded_at'), right.pop('recorded_at')
            assert left == right, operation_id
            if stage_clock != actual_clock:
                assert operation_id in new_ids, 'Older runtime timestamp changed'
                clocks.append({'operation_id': operation_id, 'stage': stage_clock, 'actual': actual_clock})
    else:
        assert expected == actual, table
    checks.append({'table': table, 'rows': len(actual), 'pass': True})
ordered = []
for table in ['dependency', 'origin', 'record_asset', 'record_media', 'review_resolution']:
    sql = 'SELECT rowid,* FROM ' + table + ' ORDER BY rowid'
    expected = [dict(row) for row in stage.execute(sql)]
    actual = [dict(row) for row in live.execute(sql)]
    assert expected == actual, table
    ordered.append({'table': table, 'rows': len(actual), 'exact_insertion_order': True})
state = {'journal_head': live.execute('SELECT max(sequence) FROM operation_payload').fetchone()[0],
         'pending': live.execute('SELECT count(*) FROM pending_review').fetchone()[0]}
assert state == gate['final_state']
assert state['pending'] == 0
result = {'task': 'T-0784', 'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'all50_schema_and_rows_compared': True, 'checks': checks,
          'recorded_at_clock_differences': clocks, 'ordered_native_tables': ordered,
          'actual_canonical_state': state, 'pass': True,
          'comparison_scope': 'Raw SQLite values including BLOB bytes, exact JSON strings/arrays, full history and ordered native rows. Only new authorized operation runtime clocks may differ.'}
args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
stage.close()
live.close()
print(json.dumps({'all50_PASS': True, 'runtime_clock_differences': len(clocks), 'actual_state': state}))
