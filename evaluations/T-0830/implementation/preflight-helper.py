"""Read-only mechanical preflight. Does not amend evidence or authorize source claims."""
import json,sqlite3,sys
from pathlib import Path
op=json.load(open(sys.argv[1]));c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row;m={a['id']:a for a in op['changes']};assert len(m)==len(op['changes']);issues=[];refs={'record':['source_id'],'transcription':['record_id'],'mention':['record_id'],'observation':['record_id','mention_id'],'identity':['mention_id'],'participation':['event_id','mention_id']};graph={k:set()for k in m}
for oid,a in m.items():
 current=c.execute('select *from current_revision where object_id=?',(oid,)).fetchone();actual=current['version']if current else None
 if actual!=a['expectedVersion']:issues.append({'object':oid,'issue':'expectedVersion mismatch','actual':actual,'requested':a['expectedVersion']})
 seen=set()
 for e in a['evidence']:
  key=(e['object'],e['version'],e['role'])
  if key in seen:issues.append({'object':oid,'issue':'duplicate exact evidence key; preserve notes and return reviewer','edge':e})
  seen.add(key);bid=e['object'];r=c.execute('select version from current_revision where object_id=?',(bid,)).fetchone();expected=(m[bid]['expectedVersion']or 0)+1 if bid in m else(r['version']if r else None)
  if e['version']!=expected:issues.append({'object':oid,'issue':'stale/missing explicit basis; no automatic latest rebind','edge':e,'required_current_version':expected})
  if bid in m:graph[oid].add(bid)
 for f in refs.get(a['kind'],[]):
  bid=a['data'].get(f)
  if bid in m:graph[oid].add(bid)
remaining=set(m);layers=[]
while remaining:
 layer=[k for k in m if k in remaining and not graph[k]&remaining]
 if not layer:issues.append({'issue':'actual explicit+boundReference cycle','remaining':sorted(remaining)});break
 layers.append(layer);remaining-=set(layer)
print(json.dumps({'issues':issues,'actual_bound_fields':refs,'assessment_subject_id':'existence-only; no implicit version edge','layers':layers,'proposed_order':[k for layer in layers for k in layer],'source_claims_approved':False},ensure_ascii=False,indent=2));sys.exit(bool(issues))
