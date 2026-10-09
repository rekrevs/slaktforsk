import json,sqlite3,re,hashlib
from pathlib import Path
out=Path('evaluations/T-0830/independent')
c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
rows=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.version=(select max(x.version) from revision x where x.object_id=r.object_id)').fetchall()
rx=re.compile(r'P-?0134|P-?0316|C-?0436|C-?0437|C-?0512|C000563[34]_0001[34]|C003306[78]_002[12][24]|C0033073_00134|Anna\s+Christina.*Lars|Cajsa\s+Märta|Kajsa\s+Märta',re.I)
sel=[]
for r in rows:
 d=c.execute('select * from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone()
 if not d:continue
 native={'revision':dict(r),'data':dict(d)}
 if rx.search(json.dumps(native,ensure_ascii=False)):
  native['origins']=[dict(x) for x in c.execute('select * from origin where revision_id=?',(r['id'],))]
  native['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=?',(r['id'],))]
  sel.append(native)
(out/'independent-current-semantic-scan-v1.json').write_text(json.dumps({'baseline':505,'query':rx.pattern,'current_count':len(rows),'matches':sel},ensure_ascii=False,indent=2))
closure={}
for file in ['five-source-existing-record-closures-v1','hypothetical-source-head-closures-v1']:
 for root in json.load(open('evaluations/T-0830/preparation/'+file+'.json')):
  for a in root['current_affected']:closure[a['native']['revision']['id']]=a['native']
own=set()
for i in range(8):own.update(x['revision']['id'] for x in json.load(open(out/f'current-own-full-{i}.json')))
remaining={x['revision']['id']:x for x in sel if x['revision']['id'] not in own}
remaining.update({k:v for k,v in closure.items() if k not in own})
# Render all full data and unique caveats/rationale once with explicit lookup, no truncation.
caves={};rats={};render=[]
for k,x in sorted(remaining.items()):
 r=x['revision'];cv=r.get('caveat','');ra=r.get('rationale','')
 ci=caves.setdefault(cv,'C'+str(len(caves)+1));ri=rats.setdefault(ra,'R'+str(len(rats)+1))
 render.append({'id':k,'kind':r['kind'],'state':[r['disposition'],r.get('evidence_status')],'caveat_id':ci,'rationale_id':ri,'data':x['data'],'evidence':x['evidence']})
(out/'remaining-text-dictionary-v1.json').write_text(json.dumps({'caveats':{v:k for k,v in caves.items()},'rationales':{v:k for k,v in rats.items()}},ensure_ascii=False,indent=2))
for i in range(0,len(render),25):(out/f'remaining-current-{i//25}.json').write_text(json.dumps(render[i:i+25],ensure_ascii=False,indent=2))
print({'semantic':len(sel),'closure':len(closure),'own_read':len(own),'remaining':len(render),'batches':(len(render)+24)//25,'caveats':len(caves)})
