"""Five exact Astra new_entire_API audit payloads, no source judgments or canonical apply."""
import json,hashlib,copy,sqlite3,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-five-completed-full-source-audits-queue-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
S=B/'source-review/resumed-five-completed-full-source-audit-specifications-v1.json';assert sha(S)=='4530e394b3ecc8954d3e92ba958275f169850682e8dfd46c8365caa4059f0109';d=load(S);assert len(d['objects'])==5
P=B/'implementation/resumed-three-completed-audit-metadata-amendments-queue-v1/concrete-current136-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='68f6c0e36a3eeb7da7ec0e3d7742994c46d1fa32003c4355c72b56133cd581f8';prior=load(P);seq=copy.deepcopy(prior['sequence']);changes=[copy.deepcopy(x['new_entire_API']) for x in d['objects']]
c=sqlite3.connect('file:'+str((B/'preparation/baseline-j281.sqlite').resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;heads={r['object_id']:r['version'] for r in c.execute('select object_id,max(version) version from revision group by object_id')};oldtargets={x['id'] for p in seq for x in load(p['path'])['changes']}
for item,ch in zip(d['objects'],changes):
 assert item['object_id']==ch['id'] and ch['expectedVersion'] is None and ch['kind']=='assessment';assert ch['id'] not in heads and ch['id'] not in oldtargets;assert ch==item['new_entire_API'];assert set(ch)=={'id','kind','expectedVersion','data','origins','evidence','disposition','evidenceStatus','rationale','caveat'};assert not c.execute('select 1 from dependency where basis_revision_id like ?',(ch['id']+'@%',)).fetchone()
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
op={'id':'T-0780/resumed-five-completed-full-source-audits-v1','actor':'Codex Sol exact settled Astra implementation','reason':'T-0780 source scoped audits only; exact whole API source '+sha(S)+'; no global source approval inferred.','dependencyReviewVersion':2,'changes':changes};pin=save('five-completed-full-source-audits-operation-v1.json',op);seq.append(pin);targets={};constraints=[];viol=[];updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']}
for i,p in enumerate(seq):
 assert sha(p['path'])==p['sha256'];q=load(p['path']);p.update(index=i+1,operation_id=q['id'],targets=[],changes=len(q['changes']))
 for x in q['changes']:
  assert x['id'] not in targets and heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=x;p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(canon(x).encode()).hexdigest()})
  for e in x['evidence']:
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':q['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in q['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in q['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==137 and len(targets)==865 and not viol
proof=save('five-whole-new-API-source-exact-equality-and-no-overlap-proof-v1.json',{'source_pin':{'path':str(S),'sha256':sha(S)},'objects':[{'source_pointer':'/objects/'+str(i)+'/new_entire_API','actual_pointer':'/changes/'+str(i),'full_source_object':item,'whole_actual_API':ch,'whole_API_exact_equal':item['new_entire_API']==ch,'no_baseline_or_current_candidate_ID_overlap':True,'all_current_history_incoming_count':0} for i,(item,ch) in enumerate(zip(d['objects'],changes))],'ordered_all_metadata_evidence_origins_source_arrays_preserved':True})
mp=save('current137-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(P),'sha256':sha(P)},'candidate_members':seq,'unique_targets':865,'member_count':137,'new_audits':5,'duplicate_targets':0,'global_source_approval':False})
pp=save('concrete-current137-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':137,'unique_targets':865,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':mp,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
rp=save('bounded-five-new-full-source-audits-production-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pin':{'path':str(S),'sha256':sha(S)},'operation_pin':pin,'proof_pin':proof,'membership_pin':mp,'proposal_pin':pp,'new_native_objects':5,'candidate_and_baseline_overlap_zero':True,'history_current_incoming_zero':True,'all_entire_APIs_exact_source_equal':True,'stage_canonical_probe':'UNRUN','failed_attempts':[],'elapsed_seconds':time.time()-START,'actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'production':rp,'membership':mp,'proposal':pp,'operation':pin},indent=2))
