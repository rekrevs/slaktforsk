"""Exact nine source-settled TR and audit payload amendments, preserving complete superseded ops."""
import json,hashlib,copy,sqlite3,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-nine-completed-TR-audit-metadata-amendments-queue-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
S=B/'source-review/resumed-four-completed-transcription-metadata-amendments-v1.json';assert sha(S)=='254b2be205be8af9550232b91cf011f71f79938627c37b59fea35f7f9ac5f03d'
A=B/'source-review/resumed-five-completed-full-source-audit-specifications-v3.json';assert sha(A)=='72850f7043a9a268cfdf915e7ca7ee6fc1f86119e00a188fda2d07b27170f47e'
O=B/'source-review/resumed-five-completed-full-source-audit-specifications-v2.json';assert sha(O)=='f276a55cc517001bede2ae0b6ed73aa5dd07774ee19f018ce5ffee82f957da03'
d={'objects':[]}
for item in load(S)['objects']:d['objects'].append(dict(item,exact_source_pin={'path':str(S),'sha256':sha(S)}))
old={x['object_id']:x['new_entire_API'] for x in load(O)['objects']}
for item in load(A)['objects']:d['objects'].append(dict(item,old_entire_API=old[item['object_id']],exact_source_pin={'path':str(A),'sha256':sha(A)},old_entire_API_source_pin={'path':str(O),'sha256':sha(O)}))
assert len(d['objects'])==9
P=B/'implementation/resumed-C0685-twelve-residual-field-queue-v1/concrete-current139-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='927555add1c56c7ed5e7c1b92642c871ea601b1e55863b508646de6c4a6e4c42';prior=load(P);seq=copy.deepcopy(prior['sequence']);assert len(seq)==139
sources=[{'path':str(q),'sha256':sha(q)} for q in [S,A,O]]
def diff(a,b,p=''):
 if type(a)!=type(b):return [{'pointer':p,'old':a,'new':b}]
 if isinstance(a,dict):
  return sum((diff(a.get(k),b.get(k),p+'/'+k.replace('~','~0').replace('/','~1')) for k in sorted(set(a)|set(b))),[])
 if isinstance(a,list):return [] if a==b else [{'pointer':p,'old':a,'new':b,'ordered_array':True}]
 return [] if a==b else [{'pointer':p,'old':a,'new':b}]
amendments={};proofs=[]
for item in d['objects']:
 found=[]
 for i,p in enumerate(seq):
  assert sha(p['path'])==p['sha256']
  for j,ch in enumerate(load(p['path'])['changes']):
   if ch['id']==item['object_id']:found.append((i,j,p,ch))
 assert len(found)==1
 i,j,p,ch=found[0];assert ch==item['old_entire_API']
 updated=copy.deepcopy(item['new_entire_API']);assert updated['id']==ch['id'] and updated['expectedVersion']==ch['expectedVersion'];assert updated['evidence']==ch['evidence'] and updated['origins']==ch['origins'];changes=diff(ch,updated);assert changes
 amendments.setdefault(i,{'prior_pin':p,'op':copy.deepcopy(load(p['path'])),'changed_indexes':[]});amendments[i]['op']['changes'][j]=updated;amendments[i]['changed_indexes'].append(j);proofs.append(dict(item,actual_prior_member_pin=copy.deepcopy(p),actual_API_pointer='/changes/'+str(j),exact_recursive_changed_fields=changes))
assert len(amendments)==4
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
memberproof=[]
for serial,(index,a) in enumerate(sorted(amendments.items()),1):
 a['op']['id']=a['op']['id']+'/completed-TR-audit-metadata-amendment-v1';a['op']['reason']+=' Exact bounded TR/audit metadata amendments '+sha(S)+' '+sha(A);pin=save(f'{serial:02}-TR-audit-metadata-superseding-operation-v1.json',a['op']);seq[index]=pin
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
assert len(seq)==139 and len(targets)==882 and not viol
proof=save('nine-full-TR-audit-API-edits-and-all-other-member-payload-retains-v1.json',{'source_pins':sources,'exact_source_objects_and_full_API_proofs':proofs,'superseding_member_proofs':memberproof,'all_ordered_origins_evidence_and_nonexplicit_fields_retained':True})
mp=save('current139-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(P),'sha256':sha(P)},'candidate_members':seq,'unique_targets':882,'member_count':139,'superseding_members':4,'same_candidate_version_TR_audit_amendments':9,'duplicate_targets':0,'global_source_approval':False})
pp=save('concrete-current139-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':139,'unique_targets':882,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':mp,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
rp=save('bounded-nine-TR-audit-metadata-amendment-production-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pins':sources,'proof_pin':proof,'membership_pin':mp,'proposal_pin':pp,'changed_targets':9,'unchanged_whole_target_payloads_in_superseded_members':sum(len(x['all_other_whole_API_payloads_exact_unchanged']) for x in memberproof),'all_other_metadata_and_ordered_arrays_protected':True,'stage_canonical_probe':'UNRUN','failed_attempts':[],'elapsed_seconds':time.time()-START,'actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'production':rp,'membership':mp,'proposal':pp,'proof':proof},indent=2))
