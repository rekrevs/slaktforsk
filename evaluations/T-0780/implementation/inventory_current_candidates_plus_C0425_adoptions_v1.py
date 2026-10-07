import json,pathlib,hashlib,sqlite3,collections,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0425-nine-adoption-queue-v1';c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
load=lambda p:json.load(open(p))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
priorp=b/'implementation/C0685-C0563-split-proposal-v2/current-partial-member-schema-and-repair-coverage-v3.json';c561p=b/'implementation/C0561-final-expanded-queue-v1/all-history-fanout-and-concrete-sequence-proposal-v2.json';c425p=b/'implementation/C0425-first-settled-queue-v1/concrete-first-queue-sequence-proposal-v1.json';r=load(w/'settled-module-receipt-v1.json');ap=[p for p in r['candidate_modules'] if 'operation-' in p['path']];members=load(priorp)['candidate_members']+load(c561p)['sequence']+load(c425p)['sequence']+ap;assert len({p['path'] for p in members})==len(members)
byid=collections.defaultdict(list);schema=[];protected=[];events=[];support_count=0;basis_inputs=[];basis_missing=[];native_current={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};statusflags=[]
for s in members:
 assert sha(s['path'])==s['sha256'];o=load(s['path']);assert o['id'];
 for i,ch in enumerate(o['changes']):
  rid=ch['id']+'@'+str((ch['expectedVersion'] or 0)+1);byid[ch['id']].append({'member_path':s['path'],'member_sha256':s['sha256'],'operation_id':o['id'],'expectedVersion':ch['expectedVersion'],'next_revision':rid,'payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'kind':ch['kind']});
  for k in ['disposition','evidenceStatus','rationale','caveat']:assert k in ch
  for e in ch['evidence']:
   support_count+=1
   if set(e)!={'object','version','role','note'} or type(e['version']) is not int or e['version']<1:schema.append({'target':ch['id'],'edge':e,'path':s['path']})
  if ch['kind']=='event':events.append({'target':rid,'candidate_path':s['path'],'data':ch['data'],'disposition':ch['disposition'],'evidenceStatus':ch['evidenceStatus']})
  if ch['kind']=='person' or (ch['kind']=='assessment' and any(t in str(ch['data'].get('criteria','')) for t in ['identity_review','tree_effect','life_picture_review'])):
   baseline=c.execute('select r.* from revision r where object_id=? and version=?',(ch['id'],ch['expectedVersion'])).fetchone() if ch['expectedVersion'] else None;protected.append({'target':rid,'candidate_path':s['path'],'baseline_status':dict(baseline) if baseline else None,'candidate_data':ch['data'],'candidate_disposition':ch['disposition'],'candidate_evidenceStatus':ch['evidenceStatus'],'source_judgment_not_inferred':True})
  if any(t in str(ch['data'])+str(ch['caveat']) for t in ['pending','Pending','väntar','återstår','oberoende']):statusflags.append({'target':rid,'candidate_path':s['path'],'data_and_caveat_preserved_as_data_not_global_approval':True})
duplicates={k:v for k,v in byid.items() if len(v)>1};assert not schema
# Exact declared adoption basis checks. Do not infer a later core version from another scope.
for s in ap:
 for ch in load(s['path'])['changes']:
  assert ch['id'] not in native_current and len(byid[ch['id']])==1
  for e in ch['evidence']:
   rid=e['object']+'@'+str(e['version']);exists=c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone();future=[q for q in byid.get(e['object'],[]) if q['next_revision']==rid];entry={'adoption':ch['id'],'ordered_edge':e,'native_current_version':native_current.get(e['object']),'baseline_exists':bool(exists),'exact_candidate_matches':future,'primary_version_or_order_disposition':None}
   if exists:
    z=dict(exists);z['data']=dict(c.execute('select * from '+z['kind']+' where revision_id=?',(rid,)).fetchone());z['evidence']=[dict(q) for q in c.execute('select * from dependency where revision_id=?',(rid,))];z['origins']=[dict(q) for q in c.execute('select * from origin where revision_id=?',(rid,))];entry['full_native']=z
   if not exists and len(future)!=1:basis_missing.append(entry)
   basis_inputs.append(entry)
p=save('adoption-basis-full-native-and-candidate-binding-v1.json',{'ordered_basis_checks':basis_inputs,'unresolved_matches':basis_missing,'no_future_core_inference':True,'new_adoptions':9,'core_changes':0});assert not basis_missing and not duplicates
q=save('current-source-bound-candidate-membership-inventory-v1.json',{'scope':'Membership only; incomplete C0425/C0060/C0069; no global order/approval','inventory_inputs':[{'path':str(z),'sha256':sha(z)} for z in [priorp,c561p,c425p]],'candidate_members':members,'candidate_targets':dict(byid),'member_count':len(members),'unique_targets':len(byid),'schema_errors':schema,'evidence_entries_checked':support_count,'duplicate_target_conflicts':duplicates,'protected_state_inputs':protected,'event_revision_inputs':events,'pending_source_flags_as_data':statusflags,'known_explicit_source_sequence_bindings':[{'path':str(z),'sha256':sha(z)} for z in [b/'source-review/C0685-C0563-exact-sequence-v2-primary-binding-v2.json',b/'source-review/C0561-fourteen-operation-partial-sequence-primary-binding-v1.json',b/'source-review/C0685-six-explicit-evidence-representation-order-amendment-v1.json']],'C0425_sequence_and_incoming_dispositions_pending':True,'stage_gate':False,'canonical_authorized':False})
s=ap[0];proposal=save('nine-adoption-concrete-sequence-proposal-v1.json',{'source_pin':r['source_pins'][0],'operation':s,'must_follow_five_C0425_TR_creation':True,'exact_basis_input_pin':p,'person_core_or_identity_changes':0,'new_objects':9,'primary_exact_hash_binding_required':True,'stage_or_apply':0});save('bounded-adoption-inventory-handoff-and-production-v1.json',{'basis_pin':p,'membership_pin':q,'proposal_pin':proposal,'core_retains':9,'new_adoptions':9,'individual_retained_core_field_table_count':63,'failed_attempts':0,'elapsed_seconds':time.time()-start,'elapsed_builder_seconds':r['elapsed_seconds'],'total_full_phase_elapsed_unknown_not_zero':True,'model_usage_unknown_root_collect_after_final':True,'actual328_and_probe_artifacts_modified':0,'stage_or_apply':0});print({'membership':q,'proposal':proposal,'targets':len(byid),'members':len(members),'supports':support_count})
