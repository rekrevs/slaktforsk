import json,pathlib,hashlib,sqlite3,copy,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0060-final-two-key-source-queue-v1';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
priorp=b/'implementation/C0060-closed-five-consequence-queue-v1/concrete-current94-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp);sequence=copy.deepcopy(prior['sequence']);receipt=load(w/'settled-module-receipt-v1.json');pins=[p for p in receipt['candidate_modules'] if 'operation-' in p['path']];key=next(p for p in pins if 'nine-key' in p['path']);mil=next(p for p in pins if 'six-military' in p['path']);op=load(mil['path']);onlyS=copy.deepcopy(op);onlyS['id']+='-source-last-proposal';onlyS['reason']+='; mechanical source-last split proposed for explicit primary binding.';onlyS['changes']=[ch for ch in op['changes'] if ch['id']=='S-0049'];qs=copy.deepcopy(onlyS);qs['id']=op['id']+'-questions-before-records-proposal';qs['changes']=[ch for ch in op['changes'] if ch['id']!='S-0049'];sp=save('S0049-source-last-split-proposal-v1.json',onlyS);qp=save('five-military-questions-split-proposal-v1.json',qs)
sequence=sequence[:-1]+[key,qp]+sequence[-1:]+[sp];heads={r['object_id']:r['version'] for r in c.execute('select object_id,max(version) version from revision group by object_id')};targets={};updates={ch['id']:{'index':i+1,'newVersion':(ch['expectedVersion'] or 0)+1,'expectedVersion':ch['expectedVersion']} for i,p in enumerate(sequence) for ch in load(p['path'])['changes']};constraints=[];viol=[];schema=[]
for i,p in enumerate(sequence):
 op=load(p['path']);assert sha(p['path'])==p['sha256'];p['index']=i+1;p['operation_id']=op['id'];p['targets']=[]
 for ch in op['changes']:
  assert ch['id'] not in targets,(ch['id'],'unexpected overlap');assert heads.get(ch['id'])==ch['expectedVersion'];targets[ch['id']]=(ch,p);p['targets'].append({'id':ch['id'],'expectedVersion':ch['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in ch['evidence']:
   if set(e)!={'object','version','role','note'} or type(e['version']) is not int or e['version']<1:schema.append({'target':ch['id'],'edge':e})
   if e['object'] in updates:constraints.append({'target':ch['id'],'operation':op['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in op['changes']):viol.append({'target':ch['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for ch in op['changes']:heads[ch['id']]=(ch['expectedVersion'] or 0)+1
assert len(sequence)==97 and len(targets)==713 and not schema;assert viol==prior['static_head_order_violations'],('new conflicts',viol)
selected={ch['id'] for p in pins for ch in load(p['path'])['changes']};fan=[];native={};bases={}
def full(rid):
 o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))]
 if o['kind']=='record':o['assets']=[dict(t) for t in c.execute('select * from record_asset where revision_id=?',(rid,))];o['media']=[dict(t) for t in c.execute('select * from record_media where revision_id=?',(rid,))]
 return o
for oid in sorted(selected):
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  row=dict(row);fan.append({'changed_target':oid,'edge':row,'primary_individual_disposition':None,'current_candidate_if_revised':targets.get(row['object_id'])});native[row['revision_id']]=full(row['revision_id'])
for p in pins:
 for ch in load(p['path'])['changes']:
  for e in ch['evidence']:
   rid=e['object']+'@'+str(e['version'])
   if c.execute('select 1 from revision where id=?',(rid,)).fetchone():bases[rid]=full(rid)
   else:assert e['object'] in targets;bases[rid]={'explicit_future_candidate':targets[e['object']]}
oldS=next(i['current'] for i in load(b/'source-review/C-0060-six-military-question-source-decisions-v1.json')['objects'] if i['current']['object_id']=='S-0049');assert onlyS['changes'][0]['data']=={k:v for k,v in oldS['data'].items() if k!='revision_id'};assert [ch for ch in onlyS['changes']+qs['changes']]==[opch for opch in load(mil['path'])['changes'] if opch['id']=='S-0049']+[opch for opch in load(mil['path'])['changes'] if opch['id']!='S-0049']
inputpin=save('all-history-incoming-and-full-basis-source-input-v1.json',{'fanouts':fan,'full_native_objects':native,'full_support_bases':bases,'S0049_entire_data_description_unchanged':True,'both_TR_supports_preserved_in_approved_array_order':True,'source_split_payload_exact_preservation':True,'individual_source_dispositions_pending':True,'prior_seven_record_basis_questions_unchanged':viol})
m=save('current97-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(priorp),'sha256':sha(priorp)},'candidate_members':sequence,'unique_targets':713,'member_count':97,'new_targets':15,'duplicate_targets':0,'schema_errors':schema,'source_split_proposal_requires_primary_binding':True,'global_source_approval':False})
q=save('concrete-current97-partial-sequence-and-constraint-proposal-v1.json',{'sequence':sequence,'unique_targets':713,'members':97,'constraints':constraints,'static_head_order_violations':viol,'prior_seven_conflicts_unchanged':True,'membership_pin':m,'primary_fresh_global_hash_binding_required':True,'no_native_PASS_stage_or_request_resolution':True})
f=save('bounded-two-module-handoff-and-production-v1.json',{'source_pins':receipt['source_pins'],'input_pin':inputpin,'membership_pin':m,'proposal_pin':q,'new_revision_targets':15,'full_field_entries':receipt['full_field_count'],'all_history_incoming_edges':len(fan),'current_edges':sum(x['edge']['is_current'] for x in fan),'native_objects':len(native),'prior_seven_unsettled_API_questions_preserved':True,'failed_attempts':[],'observed_seconds_since_first_candidate':time.time()-min(pathlib.Path(p['path']).stat().st_mtime for p in pins),'prebuild_reads_excluded':True,'model_usage_root_collect_after_final':True,'closed_two_module_cap_complete':True,'no_stage_probe_apply_actual328_modification':True});print(json.dumps({'input':inputpin,'membership':m,'proposal':q,'handoff':f,'fanout':len(fan),'current':sum(x['edge']['is_current'] for x in fan),'native':len(native),'constraints':len(constraints)}))
