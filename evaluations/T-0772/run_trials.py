"""Kör T-0772:s försök exakt en gång var i schemaordning, högst tre samtidigt.

Ett försök räknas som startat när logs/<id>.start.json finns; det startas aldrig
om. Svaret ligger i runs/<id>/answer.json, råström och tider i logs/ utanför
försökets egen katalog.
"""
import concurrent.futures as cf, datetime, json, pathlib, subprocess, sys

b = pathlib.Path(__file__).resolve().parent
TIMEOUT = 900
ALLOWED = ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep']
DISALLOWED = ['WebFetch', 'WebSearch', 'Agent']
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()


def argv(t, prompt):
    return ['claude', '-p', prompt, '--model', t['model'], '--effort', t['reasoning_effort'],
            '--output-format', 'stream-json', '--verbose', '--no-session-persistence',
            '--permission-mode', 'acceptEdits', '--allowedTools', *ALLOWED,
            '--disallowedTools', *DISALLOWED, '--strict-mcp-config', '--no-chrome']


def run(t):
    rd = b / 'runs' / t['id']
    start_file = b / 'logs' / f"{t['id']}.start.json"
    prompt = (rd / 'RUN.md').read_text().rstrip('\n')
    cmd = argv(t, prompt)
    record = {**t, 'cwd': str(rd), 'argv': cmd, 'start': now()}
    with open(start_file, 'x') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    out = open(b / 'logs' / f"{t['id']}.stream.jsonl", 'w')
    err = open(b / 'logs' / f"{t['id']}.stderr.txt", 'w')
    p = subprocess.Popen(cmd, cwd=rd, stdout=out, stderr=err, stdin=subprocess.DEVNULL)
    try:
        code, timed_out = p.wait(timeout=TIMEOUT), False
    except subprocess.TimeoutExpired:
        p.kill(); code, timed_out = p.wait(), True
    out.close(); err.close()
    record.update(end=now(), returncode=code, timed_out=timed_out,
                  answer_exists=(rd / 'answer.json').exists())
    (b / 'logs' / f"{t['id']}.end.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(t['order'], t['id'], 'exit', code, 'timeout' if timed_out else '', flush=True)
    return record


if __name__ == '__main__':
    schedule = json.loads((b / 'schedule.json').read_text())
    todo = [t for t in schedule if not (b / 'logs' / f"{t['id']}.start.json").exists()]
    if len(sys.argv) > 1:
        todo = todo[:int(sys.argv[1])]
    print('not yet started', len(todo), flush=True)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(run, todo))
    print('batch finished', flush=True)
