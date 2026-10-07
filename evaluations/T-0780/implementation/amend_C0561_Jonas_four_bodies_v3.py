import json,pathlib,hashlib,copy,sqlite3,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0561-Jonas-four-body-amendment-v3';w.mkdir(exist_ok=True);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
sp=b/'source-review/C-0561-Jonas-research-assessment-decisions-v3.json';assert sha(sp)=='07b93871a3536c1fbe5d580b1ec74d5d0d36eedafe2c948a25794af5a2d5c86c';s=load(sp);am=s['additional_amendment_v3'];assert sha(am['prior'])==am['sha256'];oldspec=load(am['prior']);assert [i['current'] for i in oldspec['objects']]==[i['current'] for i in s['objects']];priorp=b/'implementation/C0561-two-title-body-amendments-v2/concrete-current113-C0561-title-amended-sequence-proposal-v2.json';prior=load(priorp);member=next(p for p in prior['sequence'] if any(x['id']=='CONTRACT-P-0432-PK-08' for x in load(p['path'])['changes']));old=load(member['path']);new=copy.deepcopy(old);idx={x['id']:x for x in new['changes']};proof=[];changed={e['object_id'] for e in am['changes']};assert len(changed)==4
for e in am['changes']:
 ch=idx[e['object_id']];assert ch['expectedVersion']==1 and e['field']=='data.body';body=ch['data']['body'];assert body.count(e['old_clause'])==1;ch['data']['body']=body.replace(e['old_clause'],e['new_clause']);item=next(i for i in s['objects'] if i['current']['object_id']==ch['id']);assert ch['data']['body']==next(a for a in item['edits'] if a['field']=='data.body')['new'];proof.append({'target':ch['id'],'old_full_payload':next(x for x in old['changes'] if x['id']==ch['id']),'new_full_payload':ch,'native_full_current':item['current'],'exact_old_clause_count':1,'native_expected1_next2':True})
for a,z in zip(old['changes'],new['changes']):
 restored=copy.deepcopy(z)
 if z['id'] in changed:restored['data']['body']=a['data']['body']
 assert restored==a
for a,z in zip(oldspec['objects'],s['objects']):
 assert {k:v for k,v in a.items() if k!='edits'}=={k:v for k,v in z.items() if k!='edits'}
 if a['current']['object_id'] not in changed:assert a==z;continue
 olded={e['field']:e for e in a['edits']};newed={e['field']:e for e in z['edits']};assert {k:v for k,v in olded.items() if k!='data.body'}=={k:v for k,v in newed.items() if k!='data.body'}
 if 'data.body' in olded:assert olded['data.body']['old']==newed['data.body']['old']
 else:assert a['current']['data']['body']==newed['data.body']['old']
new['id']=old['id']+'-four-body-amended-v3';new['reason']='T-0780 exact four body-field source amendment '+sha(sp)+'; same32native@1→2, v2title/allotherpayloads preserved, finalsource approval pending.';np=save('Jonas32-four-body-operation-amended-v3.json',new);seq=copy.deepcopy(prior['sequence'])
for i,p in enumerate(seq):
 if p['path']==member['path']:seq[i]=np
for i,p in enumerate(seq):
 op=load(p['path']);p['index']=i+1;p['operation_id']=op['id'];p['targets']=[{'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()} for x in op['changes']]
def reid(x):
 if isinstance(x,dict):return {k:reid(v) for k,v in x.items()}
 if isinstance(x,list):return [reid(v) for v in x]
 return new['id'] if x==old['id'] else x
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;fan=[];native={};cross=[]
for oid in changed:
 item=next(i['current'] for i in s['objects'] if i['current']['object_id']==oid);header=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(item['id'],)).fetchone());assert all(item[k]==v for k,v in header.items());assert dict(c.execute('select * from '+header['kind']+' where revision_id=?',(item['id'],)).fetchone())==item['data']
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  row=dict(row);fan.append({'target':oid,'edge':row,'primary_disposition':None});rid=row['revision_id'];o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];native[rid]=o
for p in seq:
 for x in load(p['path'])['changes']:
  for e in x['evidence']:
   if e['object'] in changed:cross.append({'dependent':x['id'],'basis':e,'full_candidate_payload':x,'member_pin':p,'primary_disposition':None})
ip=save('four-body-source-v2-v3-native-oldmatch-proof-and-incoming-v3.json',{'source_pin':{'path':str(sp),'sha256':sha(sp)},'prior_source_pin':{'path':am['prior'],'sha256':am['sha256']},'old_member_pin':member,'new_member_pin':np,'proofs':proof,'all_other28payloads_and_all_arrays_evidence_origins_metadata_exact_unchanged':True,'v2_title_body_unchanged':True,'native_all_history_incoming':fan,'full_native_referencers':native,'candidate_incoming':cross});m=save('current113-Jonas-v3-membership-inventory-v3.json',{'candidate_members':seq,'members':113,'unique_targets':777,'explicit_member_supersession':{'old':member,'new':np},'global_source_approval':False});q=save('concrete-current113-Jonas-v3-sequence-proposal-v3.json',{'sequence':seq,'members':113,'unique_targets':777,'constraints':reid(prior['constraints']),'static_head_order_violations':prior['static_head_order_violations'],'membership_pin':m,'basis_versions_arrays_nativeheads_unchanged':True,'fresh_source_independent_wholehash_binding_required':True,'no_stage_apply':True});f=save('bounded-one-module-Jonas-v3-production-v3.json',{'source_pin':{'path':str(sp),'sha256':sha(sp)},'input_pin':ip,'membership_pin':m,'proposal_pin':q,'four_body_fields_changed_same32native_targets':True,'native_incoming_edges':len(fan),'candidate_incoming_edges':len(cross),'failed_attempts':[],'elapsed_seconds':time.time()-start,'model_usage_root_collect_after_final':True,'no_stage_probe_apply_actual328_modification':True});print({'input':ip,'membership':m,'proposal':q,'receipt':f,'nativeincoming':len(fan),'candidateincoming':len(cross)})
