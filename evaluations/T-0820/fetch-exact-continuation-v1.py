import json, hashlib, datetime, urllib.request
from pathlib import Path
import subprocess, re
D=Path(__file__).resolve().parent
for role in ('primary','independent'):
 p=D/(role+'-pre-acquisition-source-scope-gate-v1.json')
 assert p.is_file(), str(p)
r=json.loads((D/'originals/exact-manifest-routing-receipt-v1.json').read_text())
assert hashlib.sha256((D/'originals/folk901017-manifest.json').read_bytes()).hexdigest()==r['sha256']
canvas=r['direct_next_canvas'];url=canvas['items'][0]['items'][0]['body']['id']
assert url=='https://lbiiif.riksarkivet.se/folk!901017-091/full/max/0/default.jpg'
p=D/'originals/Folk_901017-091.jpg'
assert not p.exists(), 'Already acquired: reuse and reconcile receipt'
req=urllib.request.Request(url,headers={'Referer':'https://sok.riksarkivet.se/bildvisning/Folk_901017-091','User-Agent':'Mozilla/5.0'})
with urllib.request.urlopen(req,timeout=60) as resp:
 data=resp.read();status=resp.status;headers={k:resp.headers[k] for k in ('Content-Type','Date','ETag','Last-Modified') if resp.headers.get(k)}
assert status==200
p.write_bytes(data)
dimensions_output=subprocess.check_output(['/usr/bin/sips','-g','pixelWidth','-g','pixelHeight',str(p)],text=True)
dimensions=[int(re.search(r'pixelWidth: (\d+)',dimensions_output)[1]),int(re.search(r'pixelHeight: (\d+)',dimensions_output)[1])];fmt='JPEG'
assert data[:2]==bytes([255,216]) and data[-2:]==bytes([255,217])
receipt={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'referrer':'https://sok.riksarkivet.se/bildvisning/Folk_901017-091','HTTP':status,'headers':headers,'provider_version':headers.get('ETag') or headers.get('Last-Modified') or 'UNKNOWN','path':str(p.relative_to(Path.cwd())),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'dimensions':dimensions,'format':fmt,'source_interpretation':False,'images_acquired_this_task':1,'manifest_sha256':r['sha256'],'scope':'One direct adjacent image only; source-reading release pending root verification'}
(D/'originals/exact-continuation-acquisition-receipt-v1.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False))
assert dimensions==[800,639]
