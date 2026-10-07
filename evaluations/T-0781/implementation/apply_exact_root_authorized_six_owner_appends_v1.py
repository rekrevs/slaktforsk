"""One authorized six-log byte append; no backlog/native/task-state writes."""
from pathlib import Path
import datetime
import hashlib
import json
import sqlite3
import traceback

ROOT = Path(__file__).resolve().parents[3]
B = ROOT / 'evaluations/T-0781'
AUTH = B / 'root-six-exact-approved-owner-appends-authorization-v1.json'
OUT = B / 'six-owner-append-only-administration-actual-v1'
AUTH_SHA = '048076302076481614def11e5736e5dcaef2f75b9eeef4c09efc16ba732c77b8'
PLAN_PATH = 'evaluations/T-0781/implementation/six-future-owner-append-only-administration-plan-v1/six-individual-reviewable-append-only-owner-plan-v1.json'
PLAN_SHA = 'ef580868758bbd2a6ed524802310e70d247e12a8c701e947bd58ed5b933b9f9a'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def pin(path):
    return {'path': str(path.relative_to(ROOT)), 'sha256': sha(path)}


def state():
    c = sqlite3.connect((ROOT / 'genealogy2/data/research.sqlite').as_uri() + '?mode=ro', uri=True)
    try:
        return {'journal_head': c.execute('select max(sequence) from operation_payload').fetchone()[0],
                'pending': c.execute('select count(*) from pending_review').fetchone()[0]}
    finally:
        c.close()


def save(name, value):
    path = OUT / name
    assert not path.exists()
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return pin(path)


if not __debug__:
    raise RuntimeError('Assertions must be enabled')
assert sha(AUTH) == AUTH_SHA
auth = json.loads(AUTH.read_text())
assert auth['authorized'] is True and auth['task'] == 'T-0781' and auth['stop_after_two'] is True
assert auth['pins'][PLAN_PATH] == PLAN_SHA
for name, expected in auth['pins'].items():
    assert sha(ROOT / name) == expected, name
plan = json.loads((ROOT / PLAN_PATH).read_text())
assert plan['count'] == len(plan['rows']) == 6
assert [r['owner_task_id'] for r in plan['rows']] == auth['owners']
assert plan['new_tasks'] == plan['status_changes'] == plan['task_AC_changes'] == 0
assert not OUT.exists()
OUT.mkdir()
actual = []
try:
    acceptance = json.loads((B / 'root-actual-canonical-two-program-acceptance-v1.json').read_text())
    reconciliation = json.loads((B / 'actual-twelve-accepted-remaining19-reconciliation-v1.json').read_text())
    assert acceptance['approved_for_program_acceptance'] is True
    assert acceptance['actual_canonical_state'] == reconciliation['actual_canonical_state'] == {'journal_head': 442, 'pending': 0}
    assert reconciliation['actual_accepted_count'] == 12 and reconciliation['remaining_count'] == 19
    assert reconciliation['fixed_total_citation_scopes'] == 31
    assert state() == {'journal_head': 442, 'pending': 0}
    main_before = pin(ROOT / 'genealogy2/data/research.sqlite')
    backlog_path = ROOT / 'wotan/backlog.json'
    backlog_bytes = backlog_path.read_bytes()
    backlog = json.loads(backlog_bytes)
    entries = {r['id']: r for r in backlog['tasks']}
    prepared = []
    for row in plan['rows']:
        owner = row['owner_task_id']
        assert entries[owner] == row['current_backlog_entry']
        assert entries[owner]['status'] == row['current_status'] and entries[owner]['after'] == row['current_after']
        log = ROOT / row['existing_log_pin']['path']
        assert log == ROOT / ('wotan/dev-log/' + owner + '.md')
        before = log.read_bytes()
        assert digest(before) == row['existing_log_pin']['sha256'] and len(before) == row['existing_prefix_bytes']
        append = (ROOT / row['append_pin']['path']).read_bytes()
        assert digest(append) == row['append_pin']['sha256']
        assert append == row['append_text'].encode('utf-8')
        assert digest(before + append) == row['expected_after_full_log_sha256']
        prepared.append((row, log, before, append))
    freshpin = {'path': 'wotan/backlog.json', 'sha256': digest(backlog_bytes)}
    save('fresh-six-prefix-and-entry-guards-before-any-write-v1.json',
         {'authorization_pin': pin(AUTH), 'plan_pin': pin(ROOT / PLAN_PATH),
          'historical_plan_whole_backlog_pin': plan['current_backlog_pin'],
          'actual_fresh_backlog_pin': freshpin,
          'whole_backlog_pin_note': 'Earlier full-backlog pin remains historical. Each exact six owner entry and every original log byte freshly verified unchanged.',
          'fresh_exact_six_entries': [entries[r['owner_task_id']] for r in plan['rows']],
          'main_pin': main_before, 'actual_state': state(), 'all_six_preflight_guards_passed': True})
    for row, log, before, append in prepared:
        assert sha(AUTH) == AUTH_SHA and sha(ROOT / PLAN_PATH) == PLAN_SHA
        assert backlog_path.read_bytes() == backlog_bytes and log.read_bytes() == before
        assert (ROOT / row['append_pin']['path']).read_bytes() == append
        with log.open('ab') as f:
            f.write(append)
        after = log.read_bytes()
        assert after == before + append and after[:len(before)] == before
        assert digest(after) == row['expected_after_full_log_sha256']
        receipt = {'owner_task_id': row['owner_task_id'], 'log_path': row['existing_log_pin']['path'],
                   'original_prefix_sha256': digest(before), 'original_prefix_bytes': len(before),
                   'appended_sha256': digest(append), 'appended_bytes': len(append), 'append_pin': row['append_pin'],
                   'actual_full_after_sha256': digest(after), 'actual_full_after_bytes': len(after),
                   'historical_prefix_exact': True, 'unchanged_full_backlog_entry': entries[row['owner_task_id']],
                   'all_AC_status_after_preserved': True, 'append_count': 1}
        actual.append(receipt)
        save(row['owner_task_id'] + '-actual-exact-byte-append-receipt-v1.json', receipt)
    assert backlog_path.read_bytes() == backlog_bytes
    assert pin(ROOT / 'genealogy2/data/research.sqlite') == main_before and state() == {'journal_head': 442, 'pending': 0}
    for name, expected in auth['pins'].items():
        assert sha(ROOT / name) == expected, name
    final = save('complete-six-exact-owner-appends-actual-administrative-receipt-v1.json',
                 {'task': 'T-0781', 'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'authorization_pin': pin(AUTH), 'plan_pin': pin(ROOT / PLAN_PATH),
                  'actual_two_acceptance_pin': pin(B / 'root-actual-canonical-two-program-acceptance-v1.json'),
                  'actual12_remaining19_reconciliation_pin': pin(B / 'actual-twelve-accepted-remaining19-reconciliation-v1.json'),
                  'rows': actual, 'actual_append_count': 6, 'all_six_original_prefixes_exact': True,
                  'backlog_before_after_pin': freshpin, 'entire_backlog_bytes_unchanged': True,
                  'next_id_unchanged': backlog['next_id'], 'new_task_ids': 0, 'status_after_AC_changes': 0,
                  'native_writes': 0, 'MAIN_before_after_pin': main_before, 'actual_state': state(),
                  'root_T0781_report_log_status_or_structure_not_touched': True,
                  'model_usage': 'Root collects actual new-turn usage after final; unknown here, not zero.',
                  'next_unperformed_step': 'Root final task report, structure check, usage collection and DONE; stop after exact two.'})
    print(json.dumps({'final_administrative_receipt_pin': final, 'actual_appends': 6, 'MAIN_state': state()}, indent=2))
except BaseException as error:
    save('failure-stop-actual-administration-no-retry-v1.json',
         {'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(),
          'already_appended': actual, 'no_retry_no_native_no_status_or_backlog_writes': True})
    raise
