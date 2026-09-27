"""Frys färdiga svar och T-0769-ankare som byte-identiska blindkopior blind/<task>/Cnnn.json."""
import hashlib, json, pathlib, shutil

b = pathlib.Path(__file__).resolve().parent
old = b.parent / 'T-0769'
mapping = json.loads((b / 'blind-map.private.json').read_text())
old_map = json.loads((old / 'blind-map.private.json').read_text())
ended = {p.name.removesuffix('.end.json') for p in (b / 'logs').glob('*.end.json')}
manifest = {}
for cid, ref in mapping.items():
    if ref.startswith('T-0769:'):
        bid = ref.split(':')[1]; task = old_map[bid][0]; src = old / 'blind' / task / f'{bid}.json'
    else:
        if ref not in ended:
            continue
        task = ref[0]; src = b / 'runs' / ref / 'answer.json'
        if not src.exists():
            continue
    out = b / 'blind' / task / f'{cid}.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        assert out.read_bytes() == src.read_bytes(), 'Answer changed after freezing: ' + cid
    else:
        shutil.copy2(src, out)
    manifest[cid] = {'task': task, 'sha256': hashlib.sha256(out.read_bytes()).hexdigest()}
(b / 'blind-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Blind answers frozen', len(manifest))
