"""Exact three source-settled audit payload amendments, preserving complete superseded ops."""
import json,hashlib,copy,sqlite3,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-three-completed-audit-metadata-amendments-queue-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
S=B/'source-review/resumed-three-completed-primary-audit-metadata-amendments-v1.json';assert sha(S)=='bc0e4453d79eb7569d31eb36c931901a441721e3b5f659c3a843d90e2b1229dd';d=load(S);assert len(d['objects'])==3
P=B/'implementation/resumed-P0069-household-key-qualification-queue-v1/concrete-current136-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='05ce6992a1e9c2132b60d65c8ed79871a86cb6ffdb2695a4808082ef80cb8264';prior=load(P);seq=copy.deepcopy(prior['sequence']);assert len(seq)==136
amendments={};proofs=[]
for item in d['objects']:
 found=[]
 for i,p in enumerate(seq):
  assert sha(p['path'])==p['sha256']
  for j,ch in enumerate(load(p['path'])['changes']):
   if ch['id']==item['object_id']:found.append((i,j,p,ch))
 assert len(found)==1
 i,j,p,ch=found[0];assert ch==item['old_entire_API'];assert p['path']==item['actual_candidate_pin']['path'] and p['sha256']==item['actual_candidate_pin']['sha256'];assert '/changes/'+str(j)==item['actual_candidate_pointer'];assert item['candidate_revision_id']==ch['id']+'@'+str((ch['expectedVersion'] or 0)+1)
 updated=copy.deepcopy(ch)
 for e in item['edits']:
  obj=updated['data'] if e['field'].startswith('data.') else updated;key=e['field'].removeprefix('data.');assert obj[key]==e['old'];obj[key]=e['new']
 assert updated==item['new_entire_API'];assert updated['evidence']==ch['evidence'] and updated['origins']==ch['origins'];amendments.setdefault(i,{'prior_pin':p,'op':copy.deepcopy(load(p['path'])),'changed_indexes':[]});amendments[i]['op']['changes'][j]=updated;amendments[i]['changed_indexes'].append(j);proofs.append(item)
assert len(amendments)==3
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
memberproof=[]
for serial,(index,a) in enumerate(sorted(amendments.items()),1):
 a['op']['id']=a['op']['id']+'/completed-primary-audit-metadata-amendment-v1';a['op']['reason']+=' Exact bounded audit metadata amendment '+sha(S);pin=save(f'{serial:02}-audit-metadata-superseding-operation-v1.json',a['op']);seq[index]=pin
 oldop=load(a['prior_pin']['path']);unchanged=[]
 for j,(old,new) in enumerate(zip(oldop['changes'],a['op']['changes'])):
  if j not in a['changed_indexes']:assert old==new;unchanged.append(old['id'])
 memberproof.append({'prior_member_pin':a['prior_pin'],'new_member_pin':pin,'changed_indexes':a['changed_indexes'],'all_other_whole_API_payloads_exact_unchanged':unchanged})
c=sqlite3.connect('file:'+str((B/'preparation/baseline-j281.sqlite').resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;heads={r['object_id']:r['version'] for r in c.execute('select object_id,max(version) version from revision group by object_id')};targets={};constraints=[];viol=[];updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']}
for i,p in enumerate(seq):
 assert sha(p['path'])==p['sha256'];q=load(p['path']);p.update(index=i+1,operation_id=q['id'],targets=[],changes=len(q['changes']))
 for x in q['changes']:
  assert x['id'] not in targets and heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=x;p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(canon(x).encode()).hexdigest()})
  for e in x['evidence']:
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':q['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in q['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in q['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==136 and len(targets)==860 and not viol
proof=save('three-full-audit-API-edits-and-all-other-member-payload-retains-v1.json',{'source_pin':{'path':str(S),'sha256':sha(S)},'exact_source_objects_and_full_API_proofs':proofs,'superseding_member_proofs':memberproof,'all_ordered_origins_evidence_and_nonexplicit_fields_retained':True})
mp=save('current136-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(P),'sha256':sha(P)},'candidate_members':seq,'unique_targets':860,'member_count':136,'superseding_members':3,'same_candidate_version_audit_amendments':3,'duplicate_targets':0,'global_source_approval':False})
pp=save('concrete-current136-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':136,'unique_targets':860,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':mp,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
rp=save('bounded-three-audit-metadata-amendment-production-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pin':{'path':str(S),'sha256':sha(S)},'proof_pin':proof,'membership_pin':mp,'proposal_pin':pp,'changed_targets':3,'unchanged_whole_target_payloads_in_superseded_members':sum(len(x['all_other_whole_API_payloads_exact_unchanged']) for x in memberproof),'all_other_metadata_and_ordered_arrays_protected':True,'stage_canonical_probe':'UNRUN','failed_attempts':[],'elapsed_seconds':time.time()-START,'actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'production':rp,'membership':mp,'proposal':pp,'proof':proof},indent=2))
