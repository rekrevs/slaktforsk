import json,pathlib,shutil,hashlib
b=pathlib.Path(__file__).resolve().parent;m=json.loads((b/'blind-map.private.json').read_text());ms={x['id']:x for x in json.loads((b/'measurements.json').read_text())}
manifest={}
for bid,rid in m.items():
 if not ms.get(rid,{}).get('end'):continue
 p=b/'runs'/rid/'answer.json'
 if not p.exists():continue
 out=b/'blind'/rid[0]/f'{bid}.json';out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert out.read_bytes()==p.read_bytes(),'Answer changed after completion'
 else:shutil.copy2(p,out)
 manifest[bid]={'task':rid[0],'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(b/'blind-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Blind answers frozen',len(manifest))
