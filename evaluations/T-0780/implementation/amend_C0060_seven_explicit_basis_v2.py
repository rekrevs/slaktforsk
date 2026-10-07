import pathlib,json,hashlib,copy,sqlite3,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0060-seven-explicit-basis-amendment-v2';w.mkdir(exist_ok=True);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;p=b/'source-review/C-0060-eleven-structured-housing-minority-decisions-v2.json';assert sha(p)=='ad6592b3f94d3e612a743b358460096883acf64ebe51b658edf237d4e684bd46';d=load(p);oldspec=load(b/'source-review/C-0060-eleven-structured-housing-minority-decisions-v1.json');oldpath=b/'implementation/C0060-closed-five-consequence-queue-v1/eleven-structured-housing-minority-operation-v1.json';old=load(oldpath);new=copy.deepcopy(old);new['id']='T-0780/C0060-eleven-structured-seven-explicit-bases-v2';new['reason']='T-0780 exact source-approved seven evidence basis substitutions '+sha(p)+'; all native targets/versions/body/status/other evidence unchanged; final source and stage gates pending.';idx={x['id']:x for x in new['changes']};tables=[];bases={};fan=[];native={}
def full(rid):
 o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))]
 if o['kind']=='record':o['assets']=[dict(t) for t in c.execute('select * from record_asset where revision_id=?',(rid,))];o['media']=[dict(t) for t in c.execute('select * from record_media where revision_id=?',(rid,))]
 return o
for a,z in zip(oldspec['objects'],d['objects']):
 restored=copy.deepcopy(z);rep=restored.pop('explicit_evidence_basis_replacement',None);assert restored==a
 if rep:
  ch=idx[rep['target']];assert ch['expectedVersion']==rep['expected_current_version'];assert ch['evidence'][rep['array_index']]==rep['old'];ch['evidence'][rep['array_index']]=rep['new'];assert {k:v for k,v in rep['old'].items() if k!='version'}=={k:v for k,v in rep['new'].items() if k!='version'}
  for typ in ['old','new']:
   e=rep[typ];rid=e['object']+'@'+str(e['version']);o=full(rid);given=rep['full_old_basis' if typ=='old' else 'full_current_basis']
   assert all(given[k]==v for k,v in o.items() if k not in ['assets','media']),rid;bases[rid]=o
  assert c.execute('select max(version) from revision where object_id=?',(rep['new']['object'],)).fetchone()[0]==2
  tables.append({'target':ch['id'],'expectedVersion':ch['expectedVersion'],'field':'evidence['+str(rep['array_index'])+']','old':rep['old'],'new':rep['new'],'source_rationale':rep['rationale'],'native_version_growth':0})
  for e in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(ch['id'],)):
   e=dict(e);fan.append({'target':ch['id'],'edge':e,'individual_primary_disposition':None});native[e['revision_id']]=full(e['revision_id'])
 else:tables.append({'target':z['current']['object_id'],'disposition':'retain_whole_object','source_rationale':z['rationale']})
assert len([t for t in tables if 'field' in t])==7
for before,after in zip(old['changes'],new['changes']):
 restore=copy.deepcopy(after);rep=next(i['explicit_evidence_basis_replacement'] for i in d['objects'] if i['current']['object_id']==after['id']);restore['evidence'][rep['array_index']]=rep['old'];assert restore==before
newpin=save('eleven-structured-seven-explicit-bases-operation-v2.json',new);priorp=b/'implementation/C0069-eight-observation-queue-v1/concrete-current99-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp);seq=copy.deepcopy(prior['sequence']);mapping=[]
for i,pin in enumerate(seq):
 if pin['path']==str(oldpath):mapping.append({'old':pin,'new':newpin});seq[i]=newpin
assert len(mapping)==1;heads={r['object_id']:r['version'] for r in c.execute('select object_id,max(version) version from revision group by object_id')};updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,pin in enumerate(seq) for x in load(pin['path'])['changes']};targets={};viol=[];constraints=[]
for i,pin in enumerate(seq):
 op=load(pin['path']);assert sha(pin['path'])==pin['sha256'];pin['index']=i+1;pin['operation_id']=op['id'];pin['targets']=[]
 for x in op['changes']:
  assert x['id'] not in targets;assert heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=x;pin['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in x['evidence']:
   assert set(e)=={'object','version','role','note'} and type(e['version']) is int and e['version']>0
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':op['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in op['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in op['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert not viol and len(seq)==99 and len(targets)==721
inp=save('individual-seven-basis-amendment-and-full-input-v2.json',{'source_pin':{'path':str(p),'sha256':sha(p)},'old_candidate_pin':{'path':str(oldpath),'sha256':sha(oldpath)},'new_candidate_pin':newpin,'individual_table':tables,'full_old_current_record_bases':bases,'all_history_incoming_changed_targets':fan,'full_native_referencers':native,'all_non_evidence_fields_and_other_array_slots_exact_unchanged':True,'no_generic_rebind':True})
m=save('current99-explicit-seven-basis-amended-membership-inventory-v2.json',{'prior_proposal_pin':{'path':str(priorp),'sha256':sha(priorp)},'explicit_member_replacement':mapping,'candidate_members':seq,'member_count':99,'unique_targets':721,'additional_native_revisions':0,'global_source_approval':False})
q=save('concrete-current99-seven-basis-amended-sequence-proposal-v2.json',{'sequence':seq,'members':99,'unique_targets':721,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':m,'primary_fresh_global_hash_binding_required':True,'source_fixed_seven_bases_only_not_global_source_approval':True,'no_nativePASS_stage_or_request_resolution':True})
f=save('bounded-seven-basis-amendment-handoff-production-v2.json',{'input_pin':inp,'membership_pin':m,'proposal_pin':q,'exact_basis_substitutions':7,'same_native_targets_expectedVersions':True,'four_whole_retains':4,'all_history_changed_target_incoming':len(fan),'full_referencers':len(native),'failed_attempts':[],'elapsed_seconds':time.time()-start,'model_usage_root_collect_after_final':True,'prior_failed_candidates_preserved':True,'no_stage_probe_apply_actual328_modification':True});print(json.dumps({'input':inp,'membership':m,'proposal':q,'handoff':f,'incoming':len(fan),'constraints':len(constraints)}))
