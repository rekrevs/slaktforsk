"""Full native current/candidate/current+history incoming preparation; no source interpretation."""
import json,hashlib,sqlite3,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-five-TR-caveat-full-inputs-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
P=B/'implementation/resumed-three-completed-audit-metadata-amendments-queue-v1/concrete-current136-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='68f6c0e36a3eeb7da7ec0e3d7742994c46d1fa32003c4355c72b56133cd581f8';seq=load(P)['sequence'];candidates={}
for p in seq:
 assert sha(p['path'])==p['sha256'];op=load(p['path'])
 for i,ch in enumerate(op['changes']):assert ch['id'] not in candidates;candidates[ch['id']]={'whole_candidate_API':ch,'actual_operation_pin':p,'actual_pointer':'/changes/'+str(i)}
c=sqlite3.connect('file:'+str((B/'preparation/baseline-j281.sqlite').resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
cache={}
def native(rid):
 if rid in cache:return cache[rid]
 row=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone();assert row;n=dict(row);n['data']=dict(c.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone());n['origins']=[dict(z) for z in c.execute('select * from origin where revision_id=?',(rid,))];n['evidence']=[dict(z) for z in c.execute('select * from dependency where revision_id=?',(rid,))]
 if n['kind']=='record':
  n['assets']=[dict(z) for z in c.execute('select * from record_asset where revision_id=?',(rid,))];n['media']=[dict(z) for z in c.execute('select * from record_media where revision_id=?',(rid,))]
 cache[rid]=n;return n
ids=['TR-baaa8600f886cf76403ac679','TR-ae613125a724f4492e857e93','TR-8cbd9fa358ce39a51da2d217','TR-bf959f7acb45424339703d06','TR-0814fb9576e735ecb8218e7a'];rows=[];incomingfull={};supports={}
for oid in ids:
 row=c.execute('select id,version from revision where object_id=? order by version desc limit 1',(oid,)).fetchone();assert row and row['version']==2,(oid,dict(row) if row else None);cur=native(row['id']);fan=[]
 for z in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  edge=dict(z);fan.append({'edge':edge,'whole_current_candidate_consumer_if_any':candidates.get(edge['object_id']),'Astra_individual_disposition':None});incomingfull[edge['revision_id']]=native(edge['revision_id'])
 for e in cur['evidence']:supports[e['basis_revision_id']]=native(e['basis_revision_id'])
 rows.append({'object_id':oid,'whole_current_native':cur,'latest_candidate_if_any':candidates.get(oid),'current_incoming_count':sum(x['edge']['is_current'] for x in fan),'all_history_incoming_count':len(fan),'all_incoming_edges':fan,'no_implicit_body_field_or_version_changes':True})
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
ip=save('five-entire-current-TR-caveat-and-candidate-and-all-incoming-native-inputs-v1.json',{'task':'T-0780','current_proposal_pin':pin(P),'objects':rows,'full_incoming_native_dictionary':incomingfull,'whole_current_support_bases':supports,'source_specification_pending':True,'no_source_interpretation_or_grading':True})
rp=save('bounded-five-TR-caveat-preparation-production-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_pin':ip,'targets':5,'candidate_overlap_targets':sum(x['latest_candidate_if_any'] is not None for x in rows),'current_incoming':sum(x['current_incoming_count'] for x in rows),'all_history_incoming':sum(x['all_history_incoming_count'] for x in rows),'distinct_incoming_versions':len(incomingfull),'elapsed_seconds':time.time()-START,'failed_attempts':[],'build_stage_canonical_probe':'UNRUN','actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'input':ip,'production':rp,'counts':[(x['object_id'],x['current_incoming_count'],x['all_history_incoming_count'],x['latest_candidate_if_any'] is not None) for x in rows]},indent=2))
