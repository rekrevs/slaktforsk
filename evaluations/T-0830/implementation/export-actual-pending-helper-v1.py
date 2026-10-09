"""Bounded complete native payload export for actual staged pending requests only."""
import json,sqlite3,sys,hashlib
from pathlib import Path
c=sqlite3.connect('file:'+str(Path(sys.argv[1]).resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row

def native(rid):
 r=c.execute('select * from revision join object on object.id=revision.object_id where revision.id=?',(rid,)).fetchone()
 if not r:raise ValueError(rid)
 r=dict(r);kind=r['kind'];x={'revision':r,'data':dict(c.execute('select * from '+kind+' where revision_id=?',(rid,)).fetchone()),'origins':[dict(z)for z in c.execute('select * from origin where revision_id=? order by rowid',(rid,))],'evidence':[dict(z)for z in c.execute('select * from dependency where revision_id=? order by rowid',(rid,))]}
 if kind=='record':
  x['assets']=[dict(z)for z in c.execute('select * from record_asset where revision_id=? order by rowid',(rid,))];x['media']=[dict(z)for z in c.execute('select * from record_media where revision_id=? order by rowid',(rid,))]
 return x
rows=[]
for q in c.execute('select * from pending_review order by id'):
 q=dict(q);oid=q['affected_revision_id'].rsplit('@',1)[0];head=c.execute('select id from current_revision where object_id=?',(oid,)).fetchone()[0];rows.append({'request':q,'affected_native':native(q['affected_revision_id']),'current_head_native':native(head),'changed_basis_native':native(q['changed_revision_id'])})
p=Path(sys.argv[2]);p.write_text(json.dumps({'actual_requests':rows,'request_count':len(rows),'distinct_current_objects':len(set(x['current_head_native']['revision']['object_id']for x in rows))},ensure_ascii=False,indent=2)+'\n');print({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'requests':len(rows)})
