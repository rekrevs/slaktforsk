import json,pathlib,hashlib,copy,sqlite3,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0561-child-BIO435-438-amendment-v3';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
r=load(w/'settled-module-receipt-v1.json');group=next(p for p in r['candidate_modules'] if 'operation-' in p['path']);op=load(group['path']);priorp=b/'implementation/C0069-three-expanded-BIO-queue-v1/concrete-current115-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp);idx={x['id']:(x,p) for p in prior['sequence'] for x in load(p['path'])['changes']};assert 'BIO-P-0435' not in idx;oldpin=idx['BIO-P-0438'][1];oldop=load(oldpin['path']);spec=load(r['source_pins'][0]['path']);assert sha(spec['amendment']['supersedes'])==spec['amendment']['sha256'];olds=load(spec['amendment']['supersedes']);sourcechecks=[]
for a,z in zip(olds['objects'],spec['objects']):
 oid=a['current']['object_id'];assert a['current']==z['current']
 if oid not in ['BIO-P-0435','BIO-P-0438']:assert a==z;sourcechecks.append({'target':oid,'whole_source_decision_exact_unchanged':True})
 elif oid=='BIO-P-0438':assert {k:v for k,v in a.items() if k not in ['edits','rationale']}=={k:v for k,v in z.items() if k not in ['edits','rationale']};assert a['edits'][0]['old']==z['edits'][0]['old']
 else:assert not a['edits'] and len(z['edits'])==1 and z['edits'][0]['field']=='data.markdown'
oldnew=copy.deepcopy(op);oldnew['id']+='-prior-six-amended-proposal';oldnew['changes']=[x for x in op['changes'] if x['id']!='BIO-P-0435'];new435=copy.deepcopy(op);new435['id']+='-new-BIO435-proposal';new435['changes']=[x for x in op['changes'] if x['id']=='BIO-P-0435'];assert len(oldnew['changes'])==6 and len(new435['changes'])==1;proof=[]
for a,z in zip(oldop['changes'],oldnew['changes']):
 restore=copy.deepcopy(z)
 if z['id']=='BIO-P-0438':restore['data']['markdown']=a['data']['markdown'];proof.append({'target':z['id'],'old_full_payload':a,'new_full_payload':z,'only_markdown_changed_expected1_next2':True})
 assert restore==a
p6=save('prior-six-BIO438-amended-member-proposal-v3.json',oldnew);p435=save('new-BIO435-member-proposal-v3.json',new435);seq=[]
for p in prior['sequence']:
 if p['path']==oldpin['path']:seq.extend([p6,p435])
 else:seq.append(copy.deepcopy(p))
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;heads={x['object_id']:x['version'] for x in c.execute('select object_id,max(version) version from revision group by object_id')};updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']};targets={};constraints=[];viol=[]
for i,p in enumerate(seq):
 o=load(p['path']);assert sha(p['path'])==p['sha256'];p['index']=i+1;p['operation_id']=o['id'];p['targets']=[]
 for x in o['changes']:
  assert x['id'] not in targets;assert heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=(x,p);p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in x['evidence']:
   assert set(e)=={'object','version','role','note'} and type(e['version']) is int and e['version']>0
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':o['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in o['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in o['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==116 and len(targets)==782 and not viol,(len(seq),len(targets),viol);fan=[];native={};cross=[]
for oid in ['BIO-P-0435','BIO-P-0438']:
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  row=dict(row);fan.append({'target':oid,'edge':row,'primary_disposition':None});rid=row['revision_id'];o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];native[rid]=o
for p in seq:
 for x in load(p['path'])['changes']:
  for e in x['evidence']:
   if e['object'] in ['BIO-P-0435','BIO-P-0438']:cross.append({'dependent':x['id'],'basis':e,'full_candidate_payload':x,'member_pin':p,'primary_disposition':None})
ip=save('exact-source-v2-v3-candidate-and-all-history-input-v3.json',{'source_pins':r['source_pins'],'old_member_pin':oldpin,'new_prior_six_member':p6,'new_BIO435_member':p435,'BIO438_full_payload_proof':proof,'BIO435_full_baseline_current':next(i['current'] for i in spec['objects'] if i['current']['object_id']=='BIO-P-0435'),'BIO435_full_candidate_payload':new435['changes'][0],'six_source_decisions_unchanged':sourcechecks,'native_fanouts':fan,'full_native_referencers':native,'candidate_incoming':cross,'all_arrays_evidence_origins_meta_unchanged_except_explicit_new_BIO435_supports':True,'source_implementation_historical_counts_six_two_preserved_not_actual_current_seven_one':True})
m=save('current116-candidate-membership-inventory-v3.json',{'candidate_members':seq,'members':116,'unique_targets':782,'explicit_old_member_supersession':{'old':oldpin,'new_prior_six':p6,'new_BIO435':p435},'duplicate_targets':0,'global_source_approval':False});q=save('concrete-current116-partial-sequence-proposal-v3.json',{'sequence':seq,'members':116,'unique_targets':782,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':m,'split_payload_identical_proposal_requires_source_binding':True,'fresh_source_independent_hash_approval_required':True,'no_stage_apply':True});f=save('bounded-one-module-BIO435-438-production-v3.json',{'input_pin':ip,'membership_pin':m,'proposal_pin':q,'BIO438_same_native1to2_candidate_amended':True,'BIO435_new_target1to2':True,'other_five_existing_payloads_exact_unchanged':True,'BIO434_fullretain':True,'native_incoming_edges':len(fan),'candidate_incoming_edges':len(cross),'failed_attempts':[{'script':'finalize_C0561_child_BIO435_438_amendment_v3.py','reason':'Source decision rationale changed for explicitly amended BIO438; initial overbroad source-rationale equality guard failed before writes. Native rationale remains exact unchanged; proof now distinguishes source decision explanation from native payload.'}],'elapsed_seconds':time.time()-start,'model_usage_root_collect_after_final':True,'no_stage_probe_apply_actual328_modification':True});print({'input':ip,'membership':m,'proposal':q,'receipt':f,'incoming':len(fan),'candidateincoming':len(cross),'constraints':len(constraints)})
