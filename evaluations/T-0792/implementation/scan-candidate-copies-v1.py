import json,sqlite3,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[3];p=R/'evaluations/T-0792/primary/primary-decisions-v1.json';s=json.loads(p.read_text());db=sqlite3.connect((R/'genealogy2/data/research.sqlite').resolve().as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
changes={c['object']:c for c in s['changes']};needles=[]
for c in s['changes']:
 for f,op in c['fields'].items():
  if isinstance(op['old'],str) and len(op['old'])>30:needles.append((c['object'],f,op['old']))
results=[]
for kind, in db.execute('select distinct kind from object order by kind'):
 for row in db.execute(f'select r.object_id,r.version,r.rationale,r.caveat,x.* from current_revision r join {kind} x on x.revision_id=r.id order by r.object_id'):
  for f,v in dict(row).items():
   if not isinstance(v,str):continue
   for seed,sf,old in needles:
    if old in v:results.append({'seed':seed,'seed_field':sf,'target':row['object_id'],'version':row['version'],'field':f,'target_in_changes':row['object_id'] in changes,'occurrences':v.count(old),'full_current_field':v})
out={'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'Mechanical literal full-old-field matching only, not semantic judgement. Repeated shared caveats are reference candidates not automatic corrections; independent reviewer semantic scan complementary. No writes.','matches':results,'unexpected_candidates':[x for x in results if not x['target_in_changes']]};q=R/'evaluations/T-0792/implementation/old-field-copy-scan-v1.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'matches':len(results),'outside_changes':len(out['unexpected_candidates']),'outside_unique':len({x['target'] for x in out['unexpected_candidates']})}));db.close()
