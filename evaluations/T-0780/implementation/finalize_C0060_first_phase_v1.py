import json,pathlib,sqlite3,hashlib,copy,time,collections
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0060-first-settled-queue-v1';a=b/'implementation/C0060-thirteen-adoption-queue-v1';c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;load=lambda p:json.load(open(p))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,x):p=w/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
r=load(w/'settled-module-receipt-v1.json');ar=load(a/'settled-module-receipt-v1.json');sourcepins=r['source_pins']+ar['source_pins'];original=[p for p in r['candidate_modules']+ar['candidate_modules'] if 'operation-' in p['path']];sources=[o for s in sourcepins for o in load(s['path'])['objects']];specids={o['current']['object_id'] for o in sources};split=[]
for stem,groups in [('six-current-wrapper',[('old-TR-READ-before-records',lambda x:x['kind']!='record'),('two-records-last',lambda x:x['kind']=='record')]),('selected12-structured-core',[('observations-and-fact-before-mention',lambda x:x['kind']!='mention'),('mention-after-old-M-basis-observation',lambda x:x['kind']=='mention')])]:
 p=w/(stem+'-operation-v1.json');op=load(p)
 for suffix,predicate in groups:
  z=copy.deepcopy(op);z['id']+='-explicit-'+suffix;z['reason']+=' Exact source implementation explicitly authorizes order split; all target payloads, arrays and evidence versions preserved.';z['changes']=[ch for ch in op['changes'] if predicate(ch)];pin=save(suffix+'-operation-v1.json',z);split.append(pin)
new=[next(p for p in original if 'two-full-transcription-' in p['path']),split[0],split[2],split[3],next(p for p in original if 'thirteen-person-adoption-' in p['path']),split[1]];newtarget={ch['id']:(ch,p) for p in new for ch in load(p['path'])['changes']};assert len(newtarget)==27
oldtarget={ch['id']:ch for p in original for ch in load(p['path'])['changes']};assert newtarget.keys()==oldtarget.keys() and all(newtarget[oid][0]==ch for oid,ch in oldtarget.items())
priorp=b/'implementation/C0425-expanded-source-path-queue-v1/concrete-current77-partial-sequence-and-constraint-return-v1.json';prior=load(priorp)['sequence'];priortarget={ch['id']:(ch,s) for s in prior for ch in load(s['path'])['changes']};overlap=set(priortarget)&set(newtarget);assert not overlap
heads={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};seq=prior+new;updates={ch['id']:{'operation_id':load(p['path'])['id'],'index':i+1,'expectedVersion':ch['expectedVersion'],'newVersion':(ch['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for ch in load(p['path'])['changes']};viol=[];constraints=[];schema=[];evidence_count=0
for i,p in enumerate(seq):
 op=load(p['path']);assert sha(p['path'])==p['sha256'];p['index']=i+1;p['operation_id']=op['id'];p['targets']=[]
 for ch in op['changes']:
  assert heads.get(ch['id'])==ch['expectedVersion'];p['targets'].append({'id':ch['id'],'expectedVersion':ch['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in ch['evidence']:
   evidence_count+=1
   if set(e)!={'object','version','role','note'} or type(e['version']) is not int or e['version']<1:schema.append({'target':ch['id'],'edge':e})
   if e['object'] in updates:constraints.append({'dependent':ch['id'],'dependent_operation':op['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']],'source_order_grade_required':True})
   if heads.get(e['object'])!=e['version'] and not any(z['id']==e['object'] and (z['expectedVersion'] or 0)+1==e['version'] for z in op['changes']):viol.append({'dependent':ch['id'],'basis':e,'proposed_head':heads.get(e['object'])})
 for ch in op['changes']:heads[ch['id']]=(ch['expectedVersion'] or 0)+1
fan=[];full={};preserve=[]
for item in sources:
 if not item['edits']:continue
 o=item['current'];ch=newtarget[o['object_id']][0];assert ch['disposition']==o['disposition'] and ch['evidenceStatus']==o['evidence_status'];checks={'object':o['id'],'status_unchanged':True}
 if o['kind']=='record':
  assets=[{'path':z['asset_path'],'region':z['region']} for z in c.execute('select * from record_asset where revision_id=?',(o['id'],))];media=[{'id':z['asset_id'],'region':z['region']} for z in c.execute('select * from record_media where revision_id=?',(o['id'],))];assert assets==ch['assets'] and media==ch['media'];checks['assets_media_exact_array_order']=True
 if o['kind']=='transcription':assert o['data']['text']==ch['data']['text'];checks['old_text_exact']=True
 if 'outcome' in o['data']:assert o['data']['outcome']==ch['data']['outcome'];checks['outcome_unchanged']=True
 preserve.append(checks)
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(o['object_id'],)):
  row=dict(row);rid=row['revision_id'];fan.append({'changed_target':o['object_id'],'edge':row,'exact_candidate_if_revised':newtarget.get(row['object_id'],priortarget.get(row['object_id'])),'Astra_disposition':None})
  if rid not in full:
   z=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());z['data']=dict(c.execute('select * from '+z['kind']+' where revision_id=?',(rid,)).fetchone());z['origins']=[dict(q) for q in c.execute('select * from origin where revision_id=?',(rid,))];z['evidence']=[dict(q) for q in c.execute('select * from dependency where revision_id=? order by basis_revision_id,role',(rid,))]
   if z['kind']=='record':z['assets']=[dict(q) for q in c.execute('select * from record_asset where revision_id=?',(rid,))];z['media']=[dict(q) for q in c.execute('select * from record_media where revision_id=?',(rid,))]
   full[rid]=z
# Exact ordered adoption support heads, including two not-yet-native TR1 candidates.
basis=[]
for ch in load(a/'thirteen-person-adoption-operation-v1.json')['changes']:
 assert not c.execute('select 1 from object where id=?',(ch['id'],)).fetchone()
 for e in ch['evidence']:
  rid=e['object']+'@'+str(e['version']);exists=c.execute('select 1 from revision where id=?',(rid,)).fetchone();future=newtarget.get(e['object']);assert exists or future and (future[0]['expectedVersion'] or 0)+1==e['version'];basis.append({'adoption':ch['id'],'edge':e,'exact_native_revision_exists':bool(exists),'explicit_TR_candidate_pin':future[1] if future else None,'no_future_core_version_inference':True})
assert not schema and not viol
p=save('all-history-incoming-full-native-crossbasis-and-protected-input-v1.json',{'incoming_edges':fan,'full_native_objects':full,'protected_oldTR_assets_media_outcome_checks':preserve,'ordered_adoption_basis_checks':basis,'exact_split_target_payloads_unchanged':True,'prior624_overlaps':[],'no_individual_disposition_inferred':True});m=save('current83-candidate-membership-inventory-v1.json',{'amends_membership_only':{'path':str(priorp),'sha256':sha(priorp)},'candidate_members':seq,'unique_targets':651,'member_count':83,'new_targets':27,'new_transcriptions':2,'new_adoptions':13,'existing_revisions':12,'duplicate_targets':0,'schema_errors':schema,'source_flags_preserved_as_data':True,'incomplete_scopes':['C0060remaining','C0069','whole10finalreview','actual328individualrequests'],'global_source_and_sequence_approval':False});q=save('concrete-current83-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'unique_targets':651,'members':83,'evidence_entries_checked':evidence_count,'exact_order_constraints':constraints,'static_head_order_violations':viol,'two_newTR_expectednull_at_version1':True,'oldREAD_TR_and_O_before_M_before_R2':True,'membership_pin':m,'full_individual_inputs_pin':p,'primary_fresh_global_hash_binding_required':True,'no_nativePASS_or_stage_authority':True,'stage_or_apply':0});save('bounded-C0060-first-plus-adoption-handoff-and-production-v1.json',{'source_pins':sourcepins,'individual_input_pin':p,'membership_pin':m,'sequence_pin':q,'incoming_edges':len(fan),'incoming_current':sum(z['edge']['is_current'] for z in fan),'full_incoming_objects':len(full),'revisions':12,'new_transcriptions':2,'new_adoptions':13,'structured_retains':6,'adoption_core_retains':13,'individual_full_field_rows':234,'original_grouped_candidates_preserved':True,'failed_attempts':0,'elapsed_finalize_seconds':time.time()-start,'elapsed_builder_seconds':r['elapsed_seconds']+ar['elapsed_seconds'],'full_phase_elapsed_unknown_not_zero':True,'model_usage_unknown_root_collect_after_final':True,'no_stage_probe_apply_actual328_modification':True});print({'input':p,'membership':m,'proposal':q,'incoming':len(fan),'full':len(full),'constraints':len(constraints)})
