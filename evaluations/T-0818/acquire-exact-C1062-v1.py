import datetime, hashlib, json, pathlib, subprocess, tempfile

D = pathlib.Path('evaluations/T-0818/originals')
D.mkdir(exist_ok=True)
IMAGE = 'C0006950_00205'
REF = 'https://sok.riksarkivet.se/bildvisning/' + IMAGE
LOG = []

def save(path, value):
    assert not path.exists()
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def fetch(url, name):
    target = D / name
    assert not target.exists()
    with tempfile.NamedTemporaryFile(prefix='T0818-http-', dir='/private/tmp') as headers:
        args = ['curl', '-sS', '-L', '--max-time', '45', '-e', REF, '-D', headers.name,
                '-o', str(target), '-w', '%{http_code}', url]
        r = subprocess.run(args, capture_output=True, text=True)
        raw = pathlib.Path(headers.name).read_text(errors='replace').splitlines()
        safe = [line for line in raw if line.startswith('HTTP/') or line.split(':', 1)[0].lower()
                in {'date', 'etag', 'last-modified', 'content-type', 'content-length'}]
    entry = {'url': url, 'referer': REF, 'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'exit': r.returncode, 'http': r.stdout, 'stderr': r.stderr, 'safe_response_headers': safe,
             'body_path': str(target), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None}
    LOG.append(entry)
    if r.returncode or r.stdout != '200':
        raise RuntimeError(json.dumps(entry))
    return target

try:
    manifest = fetch('https://lbiiif.riksarkivet.se/arkis!C0006950/manifest', 'C0006950-manifest-v1.json')
    m = json.loads(manifest.read_text())
    canvases = [c for c in m['items'] if c['id'].endswith(IMAGE + '/canvas')]
    assert len(canvases) == 1
    canvas = canvases[0]
    info = fetch('https://lbiiif.riksarkivet.se/v2/arkis!' + IMAGE + '/info.json', IMAGE + '-info-v1.json')
    ip = json.loads(info.read_text())
    body = canvas['items'][0]['items'][0]['body']
    original = fetch(body['id'], IMAGE + '.jpg')
    dims = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', str(original)], capture_output=True, text=True)
    assert dims.returncode == 0
    actual = {line.split(':')[0].strip(): int(line.split(':')[1].strip())
              for line in dims.stdout.splitlines() if 'pixelWidth:' in line or 'pixelHeight:' in line}
    assert actual['pixelWidth'] == ip['width'] and actual['pixelHeight'] == ip['height']
    save(D / 'exact-acquired-original-v1.json', {
        'task': 'T-0818', 'image_key': IMAGE, 'original_path': str(original),
        'sha256': hashlib.sha256(original.read_bytes()).hexdigest(), 'bytes': original.stat().st_size,
        'width': actual['pixelWidth'], 'height': actual['pixelHeight'], 'manifest_label': m.get('label'),
        'canvas': canvas, 'info': ip, 'provider_version': 'unknown',
        'version_note': 'Canonical S/record revisions and IIIF protocol version are not a provider revision. Response validators retained separately.',
        'original_units_acquired': 1, 'own_rows_read': 0, 'http_requests': LOG,
        'scope': 'Karl ownrow16 and Charlotta ownrow24 on one shared image; metadata acquisition only, no interpretation.'})
    print(json.dumps({'image': IMAGE, 'width': ip['width'], 'height': ip['height'], 'sha256': hashlib.sha256(original.read_bytes()).hexdigest()}))
finally:
    save(D / 'actual-http-log-v1.json', LOG)
