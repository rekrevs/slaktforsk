"""Starta tre separata blinda Astra-granskare (codex exec), en per uppgift, parallellt.

Varje granskare körs en gång; judge/<task>/start.json markerar start och
förhindrar omstart. Utfiler kopieras till scores/ först efter kontroll.
"""
import concurrent.futures as cf, datetime, json, pathlib, subprocess, sys

b = pathlib.Path(__file__).resolve().parent
OLD, NEW = str(b.parent / 'T-0769'), str(b)
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()


def judge(task):
    wd = b / 'judge' / task
    (wd / 'out').mkdir(parents=True, exist_ok=True)
    prompt = ((b / 'judge' / 'PROMPT-COMMON.md').read_text() + '\n'
              + (b / 'judge' / f'PROMPT-{task.upper()}.md').read_text()).replace('{OLD}', OLD).replace('{NEW}', NEW)
    cmd = ['codex', 'exec', '-m', 'gpt-6-astra', '-c', 'model_reasoning_effort="medium"', '-s', 'workspace-write',
           '-C', str(wd), '--json', '-o', str(wd / 'last-message.txt'), prompt]
    rec = {'task': task, 'argv': cmd, 'start': now()}
    with open(wd / 'start.json', 'x') as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    with open(wd / 'events.jsonl', 'w') as out, open(wd / 'stderr.txt', 'w') as err:
        code = subprocess.run(cmd, cwd=wd, stdout=out, stderr=err, stdin=subprocess.DEVNULL).returncode
    rec.update(end=now(), returncode=code)
    (wd / 'end.json').write_text(json.dumps(rec, ensure_ascii=False, indent=2) + '\n')
    print(task, 'exit', code, flush=True)


if __name__ == '__main__':
    tasks = sys.argv[1:] or ['x', 'y', 'z']
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(judge, tasks))
