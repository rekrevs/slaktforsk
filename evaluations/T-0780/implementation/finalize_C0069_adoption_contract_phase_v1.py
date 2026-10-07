import json,pathlib,hashlib,sqlite3,copy,time
b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0069-thirtyfour-contract-queue-v1';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;r=load(w/'settled-module-receipt-v1.json');pin=next(p for p in r['candidate_modules'] if 'operation-' in p['path']);priorp=b/'implementation/C0069-eight-adoption-retain-queue-v1/concrete-current102-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp);seq=copy.deepcopy(prior['sequence']);seq.insert(len(seq)-1,pin);heads={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']};targets={};viol=[];constraints=[]
for i,p in enumerate(seq):
 op=load(p['path']);assert sha(p['path'])==p['sha256'];p['index']=i+1;p['operation_id']=op['id'];p['targets']=[]
 for x in op['changes']:
  assert x['id'] not in targets,('overlap',x['id']);assert heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=(x,p);p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in x['evidence']:
   assert set(e)=={'object','version','role','note'} and type(e['version']) is int and e['version']>0
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':op['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in op['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in op['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==102 and len(targets)==736;assert viol==prior['static_head_order_violations'];fan=[];native={}
for ch in load(pin['path'])['changes']:
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(ch['id'],)):
  row=dict(row);fan.append({'changed_target':ch['id'],'edge':row,'primary_individual_disposition':None,'current_candidate_if_revised':targets.get(row['object_id'])});rid=row['revision_id']
  if rid not in native:
   o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];native[rid]=o

bases={}
for ch in load(pin['path'])['changes']:
 for e in ch['evidence']:
  rid=e['object']+'@'+str(e['version']);row=c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone()
  if not row:assert e['object'] in targets;bases[rid]={'explicit_future_candidate':targets[e['object']]};continue
  o=dict(row);o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];bases[rid]=o
cores=[i['current'] for i in load(b/'source-review/C-0069-thirtyfour-contract-decisions-v1.json')['objects'] if not i['edits']];assert len(cores)==28
inp=save('contract-full-supports-and-all-history-incoming-input-v1.json',{'fanouts':fan,'full_native_objects':native,'full_declared_support_bases':bases,'twentyeight_full_contract_retains':cores,'contract_target_overlap_zero':True,'current_ready_target_overlap_count':0,'individual_dispositions_pending':True,'prior_seven_API_questions_unchanged':viol})
m=save('current102-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(priorp),'sha256':sha(priorp)},'candidate_members':seq,'unique_targets':736,'member_count':102,'new_targets':6,'duplicate_targets':0,'global_source_approval':False})
q=save('concrete-current102-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':102,'unique_targets':736,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':m,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
f=save('bounded-adoption-plus-contract-handoff-production-v1.json',{'prior_adoption_phase_pin':{'path':str(b/'implementation/C0069-eight-adoption-retain-queue-v1/bounded-eight-adoption-fourteen-retains-handoff-production-v1.json'),'sha256':sha(b/'implementation/C0069-eight-adoption-retain-queue-v1/bounded-eight-adoption-fourteen-retains-handoff-production-v1.json')},'source_pins':r['source_pins'],'input_pin':inp,'membership_pin':m,'proposal_pin':q,'new_adoptions_this_phase':8,'contract_revisions':6,'contract_retains':28,'core_revisions':0,'full_contract_field_entries':272,'incoming_edges':len(fan),'failed_attempts':[{'script':'build_C0069_thirtyfour_contract_queue_v1.py','reason':'Root message appended six-revision count to SHA. Initial 65-character guard stopped before writes; exact actual 64-character prefix independently verified and bound, parent notified.'}],'observed_since_contract_candidate_seconds':time.time()-pathlib.Path(pin['path']).stat().st_mtime,'initial_reads_excluded':True,'model_usage_root_collect_after_final':True,'no_stage_probe_apply_actual328_modification':True});print(json.dumps({'input':inp,'membership':m,'proposal':q,'handoff':f,'fanout':len(fan),'native':len(native),'current':sum(x['edge']['is_current'] for x in fan),'constraints':len(constraints)}))
