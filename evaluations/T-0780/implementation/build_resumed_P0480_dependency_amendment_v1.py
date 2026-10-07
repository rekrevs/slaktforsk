"""Exact Astra same-version PATH480 body amendment, with prior member preserved."""
import json,hashlib,copy,sqlite3,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-P0480-path-dependency-amendment-queue-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
S=B/'source-review/resumed-P0480-path-dependency-amendment-v1.json';assert sha(S)=='6d070d021c5226191b1b0382f24e976a4ed8bf2c4efec9c00c81fa3f57524b26';d=load(S)
P=B/'implementation/resumed-C0563-partial-pointer-two-queue-v1/concrete-current131-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='ef7f27943ea5c8e55da528e5c5b236ccc77f727fbeef6a255bbee7e50057550b';prior=load(P)
seq=copy.deepcopy(prior['sequence']);found=[]
for i,p in enumerate(seq):
 assert sha(p['path'])==p['sha256']
 for j,ch in enumerate(load(p['path'])['changes']):
  if ch['id']==d['object_id']:found.append((i,j,p,ch))
assert len(found)==1
index,changeindex,oldpin,oldtarget=found[0];assert oldtarget['expectedVersion']+1==d['expected_candidate_version'];assert d['field']=='data.body' and oldtarget['data']['body']==d['old']
oldop=load(oldpin['path']);op=copy.deepcopy(oldop);op['id']='T-0780/resumed-C0561-two-marriage-path-date-copy-revisions-P0480-dependency-amendment-v1';op['reason']=oldop['reason']+' Same-version bounded PATH480 dependency clause amendment '+sha(S)
op['changes'][changeindex]['data']['body']=d['new'];restored=copy.deepcopy(op['changes']);restored[changeindex]['data']['body']=d['old'];assert restored==oldop['changes']
c=sqlite3.connect('file:'+str((B/'preparation/baseline-j281.sqlite').resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;heads={r['object_id']:r['version'] for r in c.execute('select object_id,max(version) version from revision group by object_id')};assert heads[d['object_id']]==oldtarget['expectedVersion']
fan=[dict(r) for r in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(d['object_id'],))];assert not fan
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
pin=save('two-C0561-marriage-path-date-copy-P0480-amended-operation-v1.json',op);seq[index]=pin;targets={};constraints=[];viol=[];updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']}
for i,p in enumerate(seq):
 assert sha(p['path'])==p['sha256'];q=load(p['path']);p.update(index=i+1,operation_id=q['id'],targets=[],changes=len(q['changes']))
 for x in q['changes']:
  assert x['id'] not in targets and heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=x;p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(canon(x).encode()).hexdigest()})
  for e in x['evidence']:
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':q['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in q['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in q['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==131 and len(targets)==842 and not viol
proof=save('exact-P0480-body-amendment-and-other-target-retain-proof-v1.json',{'source_pin':{'path':str(S),'sha256':sha(S)},'prior_member_pin':oldpin,'actual_new_member_pin':pin,'target':d['object_id'],'old_entire_API':oldtarget,'new_entire_API':op['changes'][changeindex],'exact_field':d['field'],'old':d['old'],'new':d['new'],'rationale':d['rationale'],'candidate_version_preserved':3,'all_other_target_payloads_exact_unchanged':[x['id'] for j,x in enumerate(op['changes']) if j!=changeindex],'all_other_fields_and_ordered_arrays_exact':True,'all_history_incoming_edges':fan})
mp=save('current131-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(P),'sha256':sha(P)},'candidate_members':seq,'unique_targets':842,'member_count':131,'superseding_members':1,'same_candidate_version_body_amendments':1,'duplicate_targets':0,'global_source_approval':False})
pp=save('concrete-current131-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':131,'unique_targets':842,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':mp,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
rp=save('bounded-P0480-dependency-amendment-production-receipt-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pin':{'path':str(S),'sha256':sha(S)},'operation_pin':pin,'proof_pin':proof,'membership_pin':mp,'proposal_pin':pp,'changed_native_targets':1,'unchanged_other_member_targets':1,'incoming_current_and_history':0,'stage_canonical_probe':'UNRUN','global_source_binding':'PENDING','failed_attempts':[],'elapsed_seconds':time.time()-START,'actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'receipt':rp,'proposal':pp,'membership':mp,'operation':pin},indent=2))
