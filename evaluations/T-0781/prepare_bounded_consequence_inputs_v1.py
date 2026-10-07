"""Readonly exact selected current/history/incoming capture, no source judgments or builds."""
import hashlib,json,sqlite3,datetime
from pathlib import Path
B=Path('evaluations/T-0781');W=B/'bounded-consequence-inputs-v1';BASE=B/'mechanical-current425-preparation-v1/baseline-j425.sqlite';MAIN=Path('genealogy2/data/research.sqlite')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def conn(p):
 c=sqlite3.connect(p.resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
def native(c,rid):
 n=dict(c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone())
 n['data']=dict(c.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone())
 for key,t in [('origins','origin'),('evidence','dependency')]+([('assets','record_asset'),('media','record_media')] if n['kind']=='record' else []):n[key]=[dict(x) for x in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
def current(c,oid):return c.execute('select id from revision where object_id=? order by version desc limit 1',(oid,)).fetchone()[0]
def save(n,v):
 p=W/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');return pin(p)
assert not W.exists();W.mkdir(); c=conn(BASE);live=conn(MAIN)
expected_main={'path':str(MAIN),'sha256':'efea4dfa8feec3f2f5bff8167792b01513ebb5689d9d2ec5278983a23ca208b3'};assert pin(MAIN)==expected_main
assert live.execute('select max(sequence) from operation_payload').fetchone()[0]==425
assert live.execute('select count(*) from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null').fetchone()[0]==0
targets={'BIO-P-0049':4,'BIO-P-0105':1,'RESEARCH-P-0105-9d76f0343410':1,'BIO-P-0104':2}
pool={};rows=[]
def add(rid):
 if rid not in pool:
  pool[rid]=native(c,rid);assert pool[rid]==native(live,rid)
 return '/objects/'+rid.replace('~','~0').replace('/','~1')
for oid,version in targets.items():
 rid=current(c,oid);assert rid==oid+'@'+str(version) and current(live,oid)==rid
 histories=[r[0] for r in c.execute('select id from revision where object_id=? order by version',(oid,))]
 for h in histories:add(h)
 edges=[]
 for h in histories:
  for e in c.execute('select rowid as native_edge_rowid,* from dependency where basis_revision_id=? order by rowid',(h,)):
   e=dict(e);a=add(e['revision_id']);n=pool[e['revision_id']];cur=current(c,n['object_id']);cp=add(cur)
   edges.append({'exact_dependency_edge':e,'affected_native_pointer':a,'affected_is_current':cur==n['id'],'affected_latest_current_revision_id':cur,'affected_current_native_pointer':cp})
 outgoing=[]
 for e in pool[rid]['evidence']:
  outgoing.append({'edge':e,'exact_basis_native_pointer':add(e['basis_revision_id'])})
 rows.append({'object_id':oid,'expected_current_version':version,'exact_current_revision_id':rid,'complete_current_native_pointer':add(rid),'complete_current':pool[rid],'ordered_history_revision_ids':histories,'all_history_incoming_edges':edges,'incoming_current_edge_count':sum(x['affected_is_current'] for x in edges),'incoming_historical_edge_count':sum(not x['affected_is_current'] for x in edges),'ordered_current_support':outgoing,'source_disposition':'PENDING_EXACT_FIELD_SPEC','automatic_rebind':False})
native_pin=save('C0067-four-first-targets-full-current-history-support-incoming-native-v1.json',{'objects':pool,'order':'data JSON text unchanged; evidence/origin/assets/media ORDER BY rowid','entire_each_native_equals_fresh425_live':True})
result=save('C0067-four-first-targets-exact-guards-and-allhistory-incoming-v1.json',{'task':'T-0781','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current425_state':{'journal_head':425,'pending':0},'full_native_pin':native_pin,'targets':rows,'same_current_versions':True,'live_DB_unchanged_pin':pin(MAIN),'source_grade':False,'operations_constructed':0,'canonical_writes':0,'new_originals':0})
assert pin(MAIN)==expected_main;c.close();live.close();print(json.dumps({'guard_index':result,'native_pin':native_pin,'incoming_per_target':[(r['object_id'],r['incoming_current_edge_count'],r['incoming_historical_edge_count']) for r in rows]},ensure_ascii=False,indent=2))
