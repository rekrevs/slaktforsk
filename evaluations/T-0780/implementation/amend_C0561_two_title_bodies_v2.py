import json,pathlib,hashlib,copy,sqlite3,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0561-two-title-body-amendments-v2';w.mkdir(exist_ok=True);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
priorp=b/'implementation/C0563-duplicated-caveat-amendment-v3/concrete-current113-C0563-caveat-amended-sequence-proposal-v3.json';prior=load(priorp);seq=copy.deepcopy(prior['sequence']);idx={x['id']:(x,p) for p in seq for x in load(p['path'])['changes']};specs=[('five-final-selected-research','e0aab92564a2884856394572f725c8bf36ee0bd05fe027c313b6b691e417d1b0'),('Jonas-research-assessment','d43284c2d2dbe9057ee888f132cf4a3714fe7f6b58e8587acd558fb6f19edf57')];mapping=[];proof=[];sourcepins=[];c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
for name,h in specs:
 p=b/'source-review'/('C-0561-'+name+'-decisions-v2.json');assert sha(p)==h;d=load(p);am=d['additive_amendment'];assert sha(am['prior'])==am['prior_sha256'];olds=load(am['prior']);oldch,oldpin=idx[am['target']];oldop=load(oldpin['path']);new=copy.deepcopy(oldop);ch=next(x for x in new['changes'] if x['id']==am['target']);assert ch['expectedVersion']==1 and am['field']=='data.body';assert ch['data']['body'].count(am['candidate_old_clause'])==1;newbody=ch['data']['body'].replace(am['candidate_old_clause'],am['candidate_new_clause']);item=next(i for i in d['objects'] if i['current']['object_id']==am['target']);edit=next(e for e in item['edits'] if e['field']=='data.body');assert newbody==edit['new'];ch['data']['body']=newbody
 for oldi,newi in zip(olds['objects'],d['objects']):
  r=copy.deepcopy(newi)
  if oldi['current']['object_id']==am['target']:
   for a,z in zip(oldi['edits'],r['edits']):
    if z['field']=='data.body':z['new']=a['new']
  assert r==oldi
 for a,z in zip(oldop['changes'],new['changes']):
  r=copy.deepcopy(z)
  if r['id']==am['target']:r['data']['body']=a['data']['body']
  assert r==a
 old=item['current'];rid=old['id'];header=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());assert all(old[k]==v for k,v in header.items());assert dict(c.execute('select * from '+header['kind']+' where revision_id=?',(rid,)).fetchone())==old['data'];orig=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];assert len(orig)==len(old['origins']) and all(all(z[k]==v for k,v in a.items()) for a,z in zip(orig,old['origins']));ev=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];assert sorted(ev,key=lambda x:json.dumps(x,sort_keys=True))==sorted(old['evidence'],key=lambda x:json.dumps(x,sort_keys=True));new['id']=oldop['id']+'-title-limits-amended-v2';new['reason']='T-0780 exact source title-boundary amendment '+h+'; only settled body clause, native@1→2 and all other full payloads preserved, final approval pending.';np=save(name+'-operation-amended-v2.json',new);mapping.append({'old':oldpin,'new':np,'old_operation_id':oldop['id'],'new_operation_id':new['id']});proof.append({'target':am['target'],'old_full_payload':oldch,'new_full_payload':ch,'old_full_native':old,'exact_old_clause_count':1,'native_expectedVersion':1,'native_nextVersion':2,'all_other_module_payloads_arrays_metadata_evidence_origins_exact_unchanged':True,'source_amendment':am});sourcepins.append({'path':str(p),'sha256':h})
for i,p in enumerate(seq):
 for m in mapping:
  if p['path']==m['old']['path']:seq[i]=m['new']
for i,p in enumerate(seq):
 op=load(p['path']);p['index']=i+1;p['operation_id']=op['id'];p['targets']=[{'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()} for x in op['changes']]
replaceids={m['old_operation_id']:m['new_operation_id'] for m in mapping}
def reid(x):
 if isinstance(x,dict):return {k:reid(v) for k,v in x.items()}
 if isinstance(x,list):return [reid(v) for v in x]
 return replaceids.get(x,x) if isinstance(x,str) else x
changed={x['target'] for x in proof};fan=[];native={};cross=[]
for oid in changed:
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  row=dict(row);fan.append({'changed_target':oid,'edge':row,'primary_individual_disposition':None});rid=row['revision_id'];o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];native[rid]=o
for p in seq:
 for x in load(p['path'])['changes']:
  for e in x['evidence']:
   if e['object'] in changed:cross.append({'dependent':x['id'],'basis':e,'full_candidate_payload':x,'member_pin':p,'primary_disposition':None})
ip=save('two-exact-title-body-amendment-fullproof-and-incoming-v2.json',{'source_pins':sourcepins,'proofs':proof,'native_all_history_fanouts':fan,'full_native_referencers':native,'candidate_incoming_full_payloads':cross,'no_extra_native_versions':True});m=save('current113-C0561-title-amended-membership-inventory-v2.json',{'candidate_members':seq,'member_count':113,'unique_targets':777,'explicit_member_supersession':mapping,'global_source_approval':False});q=save('concrete-current113-C0561-title-amended-sequence-proposal-v2.json',{'sequence':seq,'members':113,'unique_targets':777,'constraints':reid(prior['constraints']),'static_head_order_violations':prior['static_head_order_violations'],'membership_pin':m,'evidence_versions_arrayorder_nativeheads_unchanged':True,'fresh_source_independent_fullhash_approval_required':True,'no_stage_apply':True});f=save('bounded-two-title-amendment-production-v2.json',{'source_pins':sourcepins,'input_pin':ip,'membership_pin':m,'proposal_pin':q,'changed_candidate_bodies':2,'native_incoming_edges':len(fan),'candidate_incoming_edges':len(cross),'failed_attempts':[],'source_review_repairs_preserved':[x['source_amendment']['failure'] for x in proof],'elapsed_seconds':time.time()-start,'model_usage_root_collect_after_final':True,'no_stage_probe_apply_actual328_modification':True});print({'input':ip,'membership':m,'proposal':q,'receipt':f,'nativeincoming':len(fan),'candidateincoming':len(cross)})
