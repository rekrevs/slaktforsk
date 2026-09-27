"""Slutverifiering av T-0772: frysta indata, fullständiga körningar, blindkopior, låsta betyg."""
import collections, hashlib, json, pathlib, sys

b = pathlib.Path(__file__).resolve().parent
root, old = b.parent.parent, b.parent / 'T-0769'
errors = []
need = lambda cond, msg: None if cond else errors.append(msg)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

s = json.loads((b / 'schedule.json').read_text())
need(len(s) == 30 and len({r['id'] for r in s}) == 30, 'Schedule not 30 unique')
need(all(v == 5 for v in collections.Counter((r['task'], r['arm']) for r in s).values()), 'Not 5 per cell')
for name, h in json.loads((old / 'frozen-manifest.json').read_text())['files'].items():
    need(sha(root / name) == h, 'T-0769 frozen changed: ' + name)
for name, h in json.loads((b / 'frozen-manifest.json').read_text())['files'].items():
    need(sha(root / name) == h, 'T-0772 frozen changed: ' + name)
wrapper = (b / 'WRAPPER.txt').read_text()
need(wrapper == (old / 'WRAPPER.txt').read_text(), 'Wrapper differs from T-0769')
for r in s:
    rd = b / 'runs' / r['id']
    for p in (old / r['task'] / 'public').iterdir():
        if p.is_file():
            need((rd / p.name).read_bytes() == p.read_bytes(), 'Input differs: ' + str(rd / p.name))
    need((rd / 'RUN.md').read_text() == wrapper + str(rd.resolve()) + '\n', 'RUN.md differs: ' + r['id'])
ms = json.loads((b / 'measurements.json').read_text())
need(len(ms) == 30, 'Not 30 measurements')
for r in ms:
    need(r['end'] and r['returncode'] == 0 and not r['timed_out'], 'Unfinished/failed: ' + r['id'])
    need(r['answer_exists'], 'No answer: ' + r['id'])
    need(r['argv_model'] == r['init_model'] == 'claude-opus-5-5' and r['models_used'] == ['claude-opus-5-5'], 'Model: ' + r['id'])
    need(r['argv_effort'] == r['reasoning_effort'], 'Effort: ' + r['id'])
old_map = json.loads((old / 'blind-map.private.json').read_text())
for cid, ref in json.loads((b / 'blind-map.private.json').read_text()).items():
    task = old_map[ref.split(':')[1]][0] if ref.startswith('T-0769:') else ref[0]
    src = (old / 'blind' / task / (ref.split(':')[1] + '.json')) if ref.startswith('T-0769:') else b / 'runs' / ref / 'answer.json'
    q = b / 'blind' / task / f'{cid}.json'
    need(q.exists() and q.read_bytes() == src.read_bytes(), 'Blind diff: ' + cid)
    need((b / 'scores' / f'{cid}.final.json').exists(), 'Missing grade: ' + cid)
for name, h in json.loads((b / 'grade-lock.json').read_text())['files'].items():
    need(sha(root / name) == h, 'Grade changed after lock: ' + name)
result = {'ok': not errors, 'errors': errors}
(b / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result)); sys.exit(bool(errors))
