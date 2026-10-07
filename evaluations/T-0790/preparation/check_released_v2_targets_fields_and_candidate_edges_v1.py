"""Root-released READ ONLY v2 mechanical scan, no candidate construction."""
from pathlib import Path
import json,sqlite3,hashlib
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0790/preparation';p=R/'evaluations/T-0790/source-review/settled-90-dispositions-and-literal-field-decisions-v2.json';assert hashlib.sha256(p.read_bytes()).hexdigest()=='011e36d7fec196201345423f1277741be1b0879861693c7c7e359ecde795af90';v=json.loads(p.read_text());c=sqlite3.connect('file:'+str(O/'baseline-j454.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
heads=dict(c.execute('select object_id,max(version) from revision group by object_id'));final=heads.copy();issues=[];ordered=[]
for x in v['exact_changes']:
 oid=x['target_revision'].rsplit('@',1)[0];actual=heads.get(oid);expected=x['expectedVersion'];ordered.append((oid,x))
 if actual!=expected:issues.append({'type':'stale_target','object':oid,'source_target':x['target_revision'],'actual_current':f'{oid}@{actual}'})
 final[oid]=actual+1 if actual is not None else 1
for x in v['six_life_reviews']:
 oid=x['id'];ordered.append((oid,x))
 if heads.get(oid) is not None or x['expectedVersion'] is not None:issues.append({'type':'unexpected_creation_match_or_expectedVersion','object':oid,'actual':heads.get(oid),'expected':x['expectedVersion']})
 final[oid]=1
working=heads.copy();edgeissues=[];fields=[];supportissues=[]
for oid,x in ordered:
 if 'target_revision' in x:
  kind=x['kind'];cur=f'{oid}@{heads[oid]}';data=dict(c.execute('select * from '+kind+' where revision_id=?',(cur,)).fetchone());rev=dict(c.execute('select * from revision where id=?',(cur,)).fetchone())
  for f in x['field_changes']:
   name=f['field'];actual=data.get(name,rev.get(name));fields.append({'object':oid,'field':name,'matches_exact_current_old':actual==f['old']})
   if actual!=f['old']:issues.append({'type':'literal_old_field_mismatch','object':oid,'field':name,'supplied_old':f['old'],'actual_old':actual})
  edges=[{'object':r['basis_revision_id'].rsplit('@',1)[0],'version':int(r['basis_revision_id'].rsplit('@',1)[1]),'role':r['role'],'note':r['note']} for r in c.execute('select * from dependency where revision_id=? order by rowid',(cur,))]
 else:edges=x['evidence']
 for i,e in enumerate(edges):
  if working.get(e['object'])!=e['version']:edgeissues.append({'caller':oid,'caller_kind':x['kind'],'edge_index':i,'old_edge':e,'head_at_candidate_order':working.get(e['object']),'final_planned_head':final.get(e['object']),'basis_changed_in_package':e['object'] in [p[0] for p in ordered],'question':'Source select literal version/role/note/order or retain with separately approved versioned remedy; no mechanical inference'})
 for key in ['final_supporting_versions']:
  for rid in x.get(key,[]):
   b,ver=rid.rsplit('@',1)
   if final.get(b)!=int(ver):supportissues.append({'caller':oid,'field':key,'version':rid,'actual_final_planned_head':final.get(b)})
 working[oid]=final[oid]
for row in v['individual_table']:
 for rid in row.get('final_supporting_versions',[]):
  b,ver=rid.rsplit('@',1)
  if final.get(b)!=int(ver):supportissues.append({'caller':row['object_id'],'field':'individual_table.final_supporting_versions','version':rid,'actual_final_planned_head':final.get(b)})
report={'source_v2_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'target_or_literal_issues':issues,'candidate_order_noncurrent_edges':edgeissues,'noncurrent_final_support_metadata':supportissues,'field_checks':fields,'candidate_order':[a for a,b in ordered],'final_planned_heads_for_changed':{a:final[a] for a,b in ordered},'no_operation_constructed':True,'no_stage_runtime':True,'no_sourcejudgment':True}
(O/'released-v2-exact-target-field-and-all-edge-source-questionlist-v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'target_field_issues':issues,'noncurrent_edge_count':len(edgeissues),'noncurrent_edges':[{k:e[k] for k in ['caller','edge_index','old_edge','head_at_candidate_order','final_planned_head']} for e in edgeissues],'support_meta_count':len(supportissues)},ensure_ascii=False))
