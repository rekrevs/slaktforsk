import sqlite3,json,time
from pathlib import Path
b=Path('evaluations/T-0780/preparation');c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
cur={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on r.object_id=o.id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')}; revs={r['id']:dict(r) for r in c.execute('select * from revision')};dep={}
for r in c.execute('select * from dependency'):dep.setdefault(r['revision_id'],[]).append(dict(r))
records={r['revision_id']:dict(r) for r in c.execute('select * from record')};claims=[]
for oid,r in cur.items():
 k=r['kind']
 if k not in ['relation','identity'] or r['disposition']!='accepted':continue
 d=dict(c.execute('select * from '+k+' where revision_id=?',(r['id'],)).fetchone())
 if k=='relation' and d['relation_type']!='parent':continue
 todo=[(r['id'],[])];seen=set();paths=[]
 while todo:
  rid,path=todo.pop()
  if rid in seen:continue
  seen.add(rid)
  if rid in records:paths.append({'record':records[rid],'path':path,'current_record':cur[revs[rid]['object_id']]['id']==rid});continue
  for e in dep.get(rid,[]):
   if e['role'] in ['supports','derived_from']:todo.append((e['basis_revision_id'],path+[e]))
 if paths:claims.append({'claim_revision':r,'data':d,'record_paths':paths})
(b/'current-accepted-graph-v1.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
print({'current_accepted_claims_reaching_records':len(claims)})
