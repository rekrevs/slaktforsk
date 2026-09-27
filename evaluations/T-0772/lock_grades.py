"""Lås slutbetygen med kontrollsummor innan blindnyckeln används."""
import datetime, hashlib, json, pathlib

b = pathlib.Path(__file__).resolve().parent
root = b.parent.parent
mapping = json.loads((b / 'blind-map.private.json').read_text())
files = {}
for cid in mapping:
    p = b / 'scores' / f'{cid}.final.json'
    d = json.loads(p.read_text())
    assert isinstance(d.get('passed'), bool) and 0 <= d['score'] <= d['maxScore'], cid
    files[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
lock = b / 'grade-lock.json'
assert not lock.exists(), 'Already locked'
lock.write_text(json.dumps({'locked_before_unblinding': True,
                            'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            'files': files}, indent=2) + '\n')
print('Locked', len(files))
