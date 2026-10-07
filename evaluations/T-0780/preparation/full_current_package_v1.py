import json,sqlite3
from pathlib import Path
b=Path('evaluations/T-0780/preparation');s=b/'selected';c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row;current={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')};allrev={r['id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id')};ids=set()
for p in s.glob('C-*-impact-v1.json'):
 x=json.load(open(p));ids.update(q['object_id'] for q in x['review']['items'] if q.get('current'))
persons=set()
for p in s.glob('C-*-impact-v1.json'):
 card=json.load(open(b/(p.name[:6]+'-routing-v1.json')));persons.update(card['metadata_person_routing'])
 for cl in card['actual_j281_accepted_graph_claims']:persons.update(v for k,v in cl['data'].items() if k in ['person_id','from_person','to_person'])
for pid in sorted(persons):
 ids.add(pid)
 for k in ['fact','assessment','question','narrative']:
  ids.update(r[0] for r in c.execute('select r.object_id from '+k+' d join revision r on r.id=d.revision_id where d.subject_id=?',(pid,)) if r[0] in current)
rids={current[x]['id'] for x in ids if x in current};todo=list(rids)
while todo:
 rid=todo.pop()
 for r in c.execute('select basis_revision_id from dependency where revision_id=?',(rid,)):
  if r[0] not in rids:rids.add(r[0]);todo.append(r[0])
objects=[]
for rid in sorted(rids):
 r=allrev[rid].copy();r['data']=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(rid,)).fetchone());r['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=?',(rid,))];r['origins']=[dict(x) for x in c.execute('select a.*,u.document_path,u.start_line,u.end_line,u.raw from origin a join unit u on u.id=a.unit_id where a.revision_id=?',(rid,))];r['current']=current[r['object_id']]['id']==rid
 if r['kind']=='record':
  r['assets']=[dict(x) for x in c.execute('select ra.*,a.sha256,a.bytes from record_asset ra join asset a on a.path=ra.asset_path where ra.revision_id=?',(rid,))];r['media']=[dict(x) for x in c.execute('select rm.*,n.* from record_media rm join native_asset n on n.id=rm.asset_id where rm.revision_id=?',(rid,))]
 objects.append(r)
(s/'complete-current-impact-and-support-package-v1.json').write_text(json.dumps({'metadata_only_no_adjudication':True,'objects':objects,'count':len(objects),'current_count':sum(x['current'] for x in objects)},ensure_ascii=False,indent=2)+'\n');print(len(objects))
