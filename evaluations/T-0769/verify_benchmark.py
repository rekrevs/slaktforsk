from pathlib import Path
import json,hashlib,collections,sys
b=Path(__file__).resolve().parent;errors=[]
def need(cond,message):
 if not cond:errors.append(message)
s=json.loads((b/'schedule.json').read_text());need(len(s)==60,'Schedule not60');need(len({r['id'] for r in s})==60,'Duplicate runID');need(all(v==5 for v in collections.Counter((r['task'],r['model']) for r in s).values()),'Not5percell')
f=json.loads((b/'frozen-manifest.json').read_text())
for name,h in f['files'].items():need(hashlib.sha256(Path(name).read_bytes()).hexdigest()==h,'Frozen changed:'+name)
for r in s:
 rd=b/'runs'/r['id']
 for p in (b/r['task']/'public').iterdir():
  if p.is_file():need((rd/p.name).read_bytes()==p.read_bytes(),'Input differs:'+str(rd/p.name))
 need((rd/'RUN.md').read_text()==(b/'WRAPPER.txt').read_text()+str(rd.resolve())+'\n','Wrapper differs:'+r['id'])
if '--complete' in sys.argv:
 ms=json.loads((b/'measurements.json').read_text());need(len(ms)==60,'Not60measurements')
 for r in ms:
  need(bool(r['end']),'Unfinished:'+r['id']);need(r['answer_exists'],'Noanswer:'+r['id']);need(all(m=={'model':r['model'],'effort':'medium'} for m in r['actual_models']),'Wrongmodel:'+r['id'])
  need(bool(r['usage'].get('total_tokens')),'Nousage:'+r['id'])
 for bid,rid in json.loads((b/'blind-map.private.json').read_text()).items():
  q=b/'blind'/rid[0]/(bid+'.json');need(q.exists(),'Missingblind:'+bid)
  if q.exists():need(q.read_bytes()==(b/'runs'/rid/'answer.json').read_bytes(),'Blinddiff:'+bid)
  g=b/'scores'/(bid+'.final.json');need(g.exists(),'Missinggrade:'+bid)
  if g.exists():
   d=json.loads(g.read_text());need(isinstance(d.get('passed'),bool),'No verdict:'+bid);need(isinstance(d.get('score'),(int,float)) and 0<=d['score']<=d.get('maxScore',-1),'Invalidscore:'+bid)
protected=json.loads((b/'protected-before.json').read_text())
for name,v in protected.items():need(Path(name).exists() and hashlib.sha256(Path(name).read_bytes()).hexdigest()==v['sha256'],'Research changed:'+name)
after={str(f) for root in ['genealogy2/journal','genealogy2/media/objects','genealogy2/data'] for f in Path(root).glob('*') if f.is_file()}
need(after==set(protected),'Protected file set changed')
result={'ok':not errors,'complete_mode':'--complete' in sys.argv,'errors':errors,'protected_files':len(protected)}
(b/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));sys.exit(bool(errors))
