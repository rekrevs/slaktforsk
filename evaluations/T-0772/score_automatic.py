"""Kör T-0769:s oförändrade automatiska kontroller på blindkopiorna."""
import json, pathlib, subprocess

b = pathlib.Path(__file__).resolve().parent
old = b.parent / 'T-0769'
for task in 'xyz':
    for p in sorted((b / 'blind' / task).glob('*.json')):
        dest = b / 'scores' / f'{p.stem}.auto.json'
        if dest.exists():
            continue
        cmd = (['python3', str(old / f'score_{task}.py'), str(p)] if task in 'xy'
               else ['node', str(old / 'z/private/evaluate.mjs'), str(p)])
        r = subprocess.run(cmd, capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except Exception:
            d = {'error': r.stderr or r.stdout, 'process_exit': r.returncode}
        dest.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('Automatic scored', len(list((b / 'scores').glob('*.auto.json'))))
