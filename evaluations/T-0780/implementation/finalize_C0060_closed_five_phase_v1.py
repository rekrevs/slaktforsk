import pathlib,json,hashlib,sqlite3,copy,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0060-closed-five-consequence-queue-v1';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
priorp=b/'implementation/C0060-selected-eight-research-queue-v1/concrete-current90-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp)['sequence'];idx={ch['id']:(ch,pin) for pin in prior for ch in load(pin['path'])['changes']};receipt=load(w/'settled-module-receipt-v1.json');pins={load(p['path'])['id'].split('/C0060-')[1].removesuffix('-closed-five-v1'):p for p in receipt['candidate_modules'] if 'operation-' in p['path']};p30=pins['P0030-selected-six-research'];principal=pins['C0106-four-principal-biography'];op30=load(p30['path']);bio=load(principal['path']);r30='RESEARCH-P-0030-9d76f0343410';checks=[]
# Explicit source-spec supersession leaves former three P30 changes exactly identical.
for ch in op30['changes']:
 if ch['id']==r30:assert ch['expectedVersion']==4;continue
 assert ch==idx[ch['id']][0];checks.append({'target':ch['id'],'prior_payload_exact_equal':True})
assert len(checks)==3
spec=load(b/'source-review/C-0060-C0106-four-principal-biography-decisions-v2.json');am=spec['amendment'];assert sha(am['supersedes'])==am['sha256'];oldbio=idx['BIO-P-0066'][0];newbio=next(z for z in bio['changes'] if z['id']=='BIO-P-0066');assert oldbio['data']['markdown'].count(am['old_candidate_clause'])==1
assert newbio['data']['markdown']==oldbio['data']['markdown'].replace(am['old_candidate_clause'],am['new_candidate_clause']);rest=copy.deepcopy(newbio);rest['data']['markdown']=oldbio['data']['markdown'];newedge=rest['evidence'].pop();assert newedge['object']=='TR-T0780-C0106-fullpost' and newedge['version']==1;assert rest==oldbio;assert next(z for z in bio['changes'] if z['id']=='BIO-P-0065')==idx['BIO-P-0065'][0]
# Mechanical split proposal only: identical target payloads, no evidence rebind.
oldparts=copy.deepcopy(op30);oldparts['id']+='-prior-three-proposal';oldparts['reason']+='; mechanical unchanged-three/research-late split proposed for explicit primary binding.';oldparts['changes']=[ch for ch in op30['changes'] if ch['id']!=r30]
newpart=copy.deepcopy(oldparts);newpart['id']=op30['id']+'-research-last-proposal';newpart['changes']=[ch for ch in op30['changes'] if ch['id']==r30]
a=save('P0030-prior-three-split-proposal-v1.json',oldparts);z=save('P0030-RESEARCH30-late-split-proposal-v1.json',newpart)
repl={idx['CONTRACT-P-0030-PK-04'][1]['operation_id']:a,idx['BIO-P-0066'][1]['operation_id']:principal};sequence=[];mapping=[]
for pin in prior:
 if pin['operation_id'] in repl: np=repl[pin['operation_id']];sequence.append(np);mapping.append({'old':pin,'explicit_proposed_replacement':np})
 else:sequence.append(pin)
sequence=sequence[:-1]+[pins['eleven-structured-housing-minority'],pins['P0031-twelve-current-consequence'],pins['seven-probate-age'],z]+sequence[-1:]
heads={r['object_id']:r['version'] for r in c.execute('select object_id,max(version) version from revision group by object_id')};updates={ch['id']:{'index':i+1,'newVersion':(ch['expectedVersion'] or 0)+1,'expectedVersion':ch['expectedVersion']} for i,p in enumerate(sequence) for ch in load(p['path'])['changes']};targets={};constraints=[];viol=[];schema=[]
for i,p in enumerate(sequence):
 op=load(p['path']);assert sha(p['path'])==p['sha256'];p['operation_id']=op['id'];p['index']=i+1;p['targets']=[]
 for ch in op['changes']:
  assert ch['id'] not in targets,(ch['id'],'duplicate');assert heads.get(ch['id'])==ch['expectedVersion'];targets[ch['id']]=(ch,p);p['targets'].append({'id':ch['id'],'expectedVersion':ch['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in ch['evidence']:
   if set(e)!={'object','version','role','note'} or type(e['version']) is not int or e['version']<1:schema.append({'target':ch['id'],'edge':e})
   if e['object'] in updates:constraints.append({'target':ch['id'],'operation':op['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in op['changes']):viol.append({'target':ch['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for ch in op['changes']:heads[ch['id']]=(ch['expectedVersion'] or 0)+1
assert len(sequence)==94 and len(targets)==698 and not schema and not viol,(len(sequence),len(targets),viol)
selected={ch['id'] for pin in pins.values() for ch in load(pin['path'])['changes']};assert len(selected)==25;fan=[];native={}
for oid in sorted(selected):
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  row=dict(row);fan.append({'changed_target':oid,'edge':row,'primary_individual_disposition':None,'proposed_current_candidate':targets.get(row['object_id'])});rid=row['revision_id']
  if rid not in native:
   o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];native[rid]=o
bases={}
for pin in pins.values():
 for ch in load(pin['path'])['changes']:
  for e in ch['evidence']:
   rid=e['object']+'@'+str(e['version']);row=c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone()
   if not row:assert e['object'] in targets and (targets[e['object']][0]['expectedVersion'] or 0)+1==e['version'];bases[rid]={'explicit_future_candidate':targets[e['object']]};continue
   if rid in bases:continue
   o=dict(row);o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];bases[rid]=o
inp=save('all-history-incoming-full-native-and-basis-input-v1.json',{'fanouts':fan,'full_native_referencers':native,'full_support_bases':bases,'exact_PRIOR_three_P30_payload_checks':checks,'BIO65_whole_payload_identical':True,'BIO66_exact_clause_only_and_one_ordered_C0106_TR_addition':newedge,'individual_source_dispositions_pending':True,'split_payloads_exact_equal_to_grouped_candidate':True,'no_generic_rebind':True})
m=save('current94-explicit-replacement-membership-inventory-v1.json',{'prior_proposal':{'path':str(priorp),'sha256':sha(priorp)},'explicit_replacements':mapping,'candidate_members':sequence,'unique_targets':698,'member_count':94,'new_unique_targets':20,'amended_existing_native_payloads':1,'duplicates':0,'schema_errors':schema,'global_source_approval':False,'proposal_only_split_not_primary_bound':True})
q=save('concrete-current94-partial-sequence-and-constraint-proposal-v1.json',{'sequence':sequence,'unique_targets':698,'members':94,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':m,'primary_fresh_global_binding_and_individual_dependency_dispositions_required':True,'not_native_PASS_or_stage':True})
f=save('closed-five-module-handoff-and-production-v1.json',{'source_pins':receipt['source_pins'],'input_pin':inp,'membership_pin':m,'proposal_pin':q,'new_targets':20,'amended_prior_BIO66_target':1,'other_four_prior_payloads_identical':True,'full_field_entries':receipt['full_field_count'],'all_history_incoming_edges':len(fan),'full_incoming_objects':len(native),'current_incoming_edges':sum(t['edge']['is_current'] for t in fan),'no_stage_probe_apply_request_resolution':True,'failed_attempts':[],'observed_seconds_since_first_candidate':time.time()-min(pathlib.Path(p['path']).stat().st_mtime for p in pins.values()),'prebuild_reads_excluded':True,'model_usage_root_collect_after_final':True,'closed_five_module_cap_complete':True,'queued_next_unperformed':['KEY9 24c83...','six-military-question-source f4908abe...']});print(json.dumps({'input':inp,'membership':m,'proposal':q,'handoff':f,'incoming':len(fan),'native':len(native),'current_edges':sum(t['edge']['is_current'] for t in fan),'constraints':len(constraints)}))
