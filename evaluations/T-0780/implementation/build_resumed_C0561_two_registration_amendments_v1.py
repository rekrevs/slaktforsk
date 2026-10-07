"""Exact Astra same-version PATH480 body amendment, with prior member preserved."""
import json,hashlib,copy,sqlite3,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-C0561-two-registration-wording-amendment-queue-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
S=B/'source-review/resumed-C0561-two-registration-wording-amendment-v1.json';assert sha(S)=='66629b17117c3a11d8b893f057422440cf476c531a4bf332160c8d39cd2f52e2';d=load(S)
P=B/'implementation/resumed-C0561-ten-bounded-context-queue-v1/concrete-current133-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='d6e39bf88e2a3ed8d07ab1dcfb8ba986afc8622386a5e6c2fe3435f74535c44d';prior=load(P)
seq=copy.deepcopy(prior['sequence']);assert len(d['objects'])==2;locations=[]
for item in d['objects']:
 found=[]
 for i,p in enumerate(seq):
  assert sha(p['path'])==p['sha256']
  for j,ch in enumerate(load(p['path'])['changes']):
   if ch['id']==item['object_id']:found.append((i,j,p,ch))
 assert len(found)==1
 i,j,p,ch=found[0];assert item['candidate_revision_id']==ch['id']+'@'+str(ch['expectedVersion']+1);assert item['field']=='data.body' and ch['data']['body']==item['old'];locations.append((i,j,p,ch,item))
assert len({x[0] for x in locations})==1
index=locations[0][0];oldpin=locations[0][2];oldop=load(oldpin['path']);op=copy.deepcopy(oldop);op['id']='T-0780/resumed-C0561-ten-bounded-context-registration-amendment-v1';op['reason']=oldop['reason']+' Same-version bounded registration clauses amendment '+sha(S)
for i,j,p,ch,item in locations:op['changes'][j]['data']['body']=item['new']
restored=copy.deepcopy(op['changes'])
for i,j,p,ch,item in locations:restored[j]['data']['body']=item['old']
assert restored==oldop['changes']
c=sqlite3.connect('file:'+str((B/'preparation/baseline-j281.sqlite').resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;heads={r['object_id']:r['version'] for r in c.execute('select object_id,max(version) version from revision group by object_id')}
fan=[]
for i,j,p,ch,item in locations:
 assert heads[ch['id']]==ch['expectedVersion']
 fan.extend(dict(r) for r in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(ch['id'],)))
assert not fan
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
pin=save('ten-C0561-bounded-context-registration-amended-operation-v1.json',op);seq[index]=pin;targets={};constraints=[];viol=[];updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']}
for i,p in enumerate(seq):
 assert sha(p['path'])==p['sha256'];q=load(p['path']);p.update(index=i+1,operation_id=q['id'],targets=[],changes=len(q['changes']))
 for x in q['changes']:
  assert x['id'] not in targets and heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=x;p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(canon(x).encode()).hexdigest()})
  for e in x['evidence']:
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':q['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in q['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in q['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==133 and len(targets)==853 and not viol
changedids={x[3]['id'] for x in locations}
proof=save('exact-two-registration-body-amendments-and-eight-target-retain-proof-v1.json',{'source_pin':{'path':str(S),'sha256':sha(S)},'prior_member_pin':oldpin,'actual_new_member_pin':pin,'proofs':[{'target':ch['id'],'old_entire_API':ch,'new_entire_API':op['changes'][j],'exact_field':item['field'],'old':item['old'],'new':item['new'],'rationale':item['rationale'],'candidate_version_preserved':ch['expectedVersion']+1} for i,j,p,ch,item in locations],'all_other_target_payloads_exact_unchanged':[x['id'] for x in op['changes'] if x['id'] not in changedids],'all_other_fields_and_ordered_arrays_exact':True,'all_history_incoming_edges':fan})
mp=save('current133-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(P),'sha256':sha(P)},'candidate_members':seq,'unique_targets':853,'member_count':133,'superseding_members':1,'same_candidate_version_body_amendments':2,'duplicate_targets':0,'global_source_approval':False})
pp=save('concrete-current133-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':133,'unique_targets':853,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':mp,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
rp=save('bounded-two-registration-amendments-production-receipt-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pin':{'path':str(S),'sha256':sha(S)},'operation_pin':pin,'proof_pin':proof,'membership_pin':mp,'proposal_pin':pp,'changed_native_targets':2,'unchanged_other_member_targets':8,'incoming_current_and_history':0,'stage_canonical_probe':'UNRUN','global_source_binding':'PENDING','failed_attempts':[],'elapsed_seconds':time.time()-START,'actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'receipt':rp,'proposal':pp,'membership':mp,'operation':pin},indent=2))
