"""Bounded readonly two birth-event/origin/support input, no source grades."""
import json,sqlite3,hashlib
from pathlib import Path
B=Path('evaluations/T-0781');W=B/'bounded-consequence-inputs-v1';scope={};p=B/'prepare_bounded_consequence_inputs_v1.py';exec(compile(p.read_text().split('assert not W.exists();')[0],str(p),'exec'),scope)
c=scope['conn'](scope['BASE']);live=scope['conn'](scope['MAIN']);native=scope['native'];current=scope['current'];pin=scope['pin'];pool={};units={};rows=[]
def add(rid):
 if rid in pool:return '/objects/'+rid
 n=native(c,rid);assert n==native(live,rid);pool[rid]=n
 for o in n['origins']:
  uid=o['unit_id'];u=dict(c.execute('select * from unit where id=?',(uid,)).fetchone());assert u==dict(live.execute('select * from unit where id=?',(uid,)).fetchone());units[uid]=u
 for e in n['evidence']:add(e['basis_revision_id'])
 return '/objects/'+rid
for person in ['P-0052','P-0053']:
 oid='E-birth-'+person;rid=current(c,oid);hs=[x[0] for x in c.execute('select id from revision where object_id=? order by version',(oid,))];incoming=[]
 for h in hs:
  add(h)
  for e in c.execute('select rowid as native_edge_rowid,* from dependency where basis_revision_id=? order by rowid',(h,)):
   e=dict(e);add(e['revision_id']);cur=current(c,pool[e['revision_id']]['object_id']);add(cur);incoming.append({'edge':e,'affected_current_revision_id':cur,'affected_is_current':cur==e['revision_id']})
 ep=[]
 for r in c.execute('select revision_id from participation where event_id=? order by rowid',(oid,)):
  add(r[0]);ep.append(r[0])
 for target in [person,'BIO-'+person,'RESEARCH-'+person+'-9d76f0343410']:
  add(current(c,target))
 rows.append({'person_id':person,'event_object_id':oid,'current_revision_id':rid,'ordered_history_revision_ids':hs,'all_history_incoming':incoming,'participations_full_native_revision_ids':ep,'event_current_native_pointer':add(rid),'source_grade':'PENDING_PRIMARY','automatic_place_change':False})
paths=['genealogy/citations/C-0046-anders-alfred-jomark-folkrakning-1900.md','genealogy/citations/C-0072-anna-fredrika-folkrakning-1910.md'];supportorigins=[]
for path in paths:
 for r in c.execute('select * from unit where document_path=? order by rowid',(path,)):
  u=dict(r);assert u==dict(live.execute('select * from unit where id=?',(u['id'],)).fetchone());units[u['id']]=u
  for o in c.execute('select * from origin where unit_id=? order by rowid',(u['id'],)):
   o=dict(o);add(o['revision_id']);supportorigins.append({'source_document_path':path,'unit_id':u['id'],'origin_edge':o,'native_revision_pointer':'/objects/'+o['revision_id']})
for row in rows:
 row['existing_C0046_C0072_support_native_routing']=[x for x in supportorigins if pool[x['origin_edge']['revision_id']]['data'].get('subject_id')==row['person_id'] or row['person_id'] in units[x['unit_id']]['raw']]
 row['support_routing_is_not_person_birthplace_grade']=True
payload={'task':'T-0781','rows':rows,'objects':pool,'origin_units_full_text':units,'C0046_C0072_exact_origin_links':supportorigins,'source_document_pins':[pin(p) for p in paths],'baseline_pin':pin(scope['BASE']),'main425_pin':pin(scope['MAIN']),'data_JSON_native_text_and_fullmetadata_preserved':True,'arrays':'native ORDER BY rowid; no evidence-order sorting','new_sources_opened':0,'operations_built':0,'semantic_grade':False}
assert payload['main425_pin']['sha256']=='efea4dfa8feec3f2f5bff8167792b01513ebb5689d9d2ec5278983a23ca208b3'
out=W/'P0052-P0053-birth-events-EP-origins-and-existing-C0046-C0072-whole-current-support-input-v1.json';assert not out.exists();out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'input_pin':pin(out),'native_revisions':len(pool),'origin_units':len(units),'rows':[{k:v for k,v in r.items() if k in ['person_id','event_object_id','current_revision_id','all_history_incoming','participations_full_native_revision_ids']} for r in rows]},ensure_ascii=False,indent=2));c.close();live.close()
