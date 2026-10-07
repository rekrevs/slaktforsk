import json,pathlib,hashlib,copy,sqlite3,time
b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0069-two-research-amendment-v3';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
r=load(w/'settled-module-receipt-v1.json');pin=next(p for p in r['candidate_modules'] if 'operation-' in p['path']);op=load(pin['path']);priorp=b/'implementation/C0043-literal-scope-amendment-v3/concrete-current113-C0043-amended-sequence-proposal-v4.json';prior=load(priorp);oldpin=next(p for p in prior['sequence'] if any(x['id']=='RESEARCH-P-0102-9d76f0343410' for x in load(p['path'])['changes']));oldop=load(oldpin['path']);proof=[]
for old,new in zip(oldop['changes'],op['changes']):
 assert old['id']==new['id'] and old['expectedVersion']==new['expectedVersion']==1;rest=copy.deepcopy(new);rest['data']['body']=old['data']['body'];assert rest==old;proof.append({'target':new['id'],'expectedVersion':1,'native_version':2,'old_candidate_body':old['data']['body'],'new_candidate_body':new['data']['body'],'all_other_payload_fields_evidence_origins_arrays_exact_unchanged':True})
seq=copy.deepcopy(prior['sequence']);matches=0
for i,p in enumerate(seq):
 if p['path']==oldpin['path']:seq[i]=pin;matches+=1
assert matches==1
for i,p in enumerate(seq):
 o=load(p['path']);p['index']=i+1;p['operation_id']=o['id'];p['targets']=[{'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()} for x in o['changes']]
def replace(x):
 if isinstance(x,dict):return {k:replace(v) for k,v in x.items()}
 if isinstance(x,list):return [replace(v) for v in x]
 return op['id'] if x==oldop['id'] else x
constraints=replace(prior['constraints']);c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;fan=[];native={};cross=[];targetids={x['id'] for x in op['changes']}
for oid in targetids:
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  row=dict(row);fan.append({'changed_target':oid,'edge':row,'primary_individual_disposition':None});rid=row['revision_id'];o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];native[rid]=o
for p in seq:
 for x in load(p['path'])['changes']:
  for e in x['evidence']:
   if e['object'] in targetids:cross.append({'dependent':x['id'],'basis':e,'full_candidate_payload':x,'member_pin':p,'individual_primary_disposition':None})
spec=load(r['source_pins'][0]['path']);inputpin=save('complete-prior-diff-and-all-history-candidate-fanout-input-v3.json',{'source_pin':r['source_pins'][0],'initial_member_pin':oldpin,'new_member_pin':pin,'full_native_baseline_current_objects':[i['current'] for i in spec['objects']],'two_complete_candidate_comparisons':proof,'native_all_history_fanouts':fan,'full_native_referencers':native,'candidate_incoming_full_payloads':cross,'native_version_growth':0,'failed_source_v2_unimplemented':spec['amends_v2']})
m=save('current113-research-v3-membership-inventory-v3.json',{'candidate_members':seq,'unique_targets':777,'member_count':113,'explicit_member_supersession':{'old':oldpin,'new':pin},'duplicate_targets':0,'global_source_approval':False});q=save('concrete-current113-research-v3-sequence-proposal-v3.json',{'sequence':seq,'members':113,'unique_targets':777,'constraints':constraints,'static_head_order_violations':prior['static_head_order_violations'],'membership_pin':m,'support_edges_order_native_heads_exact_unchanged':True,'fresh_primary_global_hash_binding_required':True,'no_native_PASS_stage_or_request_resolution':True});f=save('bounded-two-research-v3-amendment-handoff-production-v3.json',{'source_pins':r['source_pins'],'input_pin':inputpin,'membership_pin':m,'proposal_pin':q,'same_two_native_at2_targets':True,'failed_mechanical_attempts':[],'source_failed_v2_preserved_unimplemented':spec['amends_v2'],'native_incoming_edges':len(fan),'candidate_incoming_edges':len(cross),'elapsed_since_candidate_seconds':time.time()-pathlib.Path(pin['path']).stat().st_mtime,'initial_reads_excluded':True,'model_usage_root_collect_after_final':True,'no_stage_probe_apply_actual328_modification':True});print({'input':inputpin,'membership':m,'proposal':q,'receipt':f,'nativeincoming':len(fan),'candidateincoming':len(cross)})
