import pathlib,json,hashlib,copy,sqlite3,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0563-fullTR-compilation-amendment-v2';w.mkdir(exist_ok=True);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
specp=b/'source-review/C-0563-full-transcription-decisions-v2.json';assert sha(specp)=='90ae1325cd606d5080e69018d9cfe9784a1d72965d65eb56d9500b5642d4f6db';spec=load(specp);am=spec['additive_amendment'];assert sha(am['prior_spec'])==am['prior_sha256'];oldspec=load(am['prior_spec']);oldn=oldspec['new_objects'][0];newn=spec['new_objects'][0];assert {k:v for k,v in oldn.items() if k!='content'}=={k:v for k,v in newn.items() if k!='content'};a=json.loads(oldn['content']);z=json.loads(newn['content']);rest=copy.deepcopy(z)
for e in am['edits']:assert a[e['embedded_field']]==e['old'] and z[e['embedded_field']]==e['new'];rest[e['embedded_field']]=e['old']
assert rest==a and len(am['edits'])==2
priorp=b/'implementation/C0069-two-research-amendment-v3/concrete-current113-research-v3-sequence-proposal-v3.json';prior=load(priorp);member=next(p for p in prior['sequence'] if any(x['id']=='TR-T0780-C0563-fullpost' for x in load(p['path'])['changes']));old=load(member['path']);new=copy.deepcopy(old);target=next(x for x in new['changes'] if x['id']==newn['id']);assert target['expectedVersion'] is None and target['data']['text']==oldn['content'];target['data']['text']=newn['content'];new['id']=old['id']+'-compilation-amended-v2';new['reason']='T-0780 exact source-approved two embedded compilation fields '+sha(specp)+'; NEW expectednull1 preserved, diagnostic priorpayload immutable and cannot certify amended fullhash, new independent/global source binding required.'
for oldch,newch in zip(old['changes'],new['changes']):
 r=copy.deepcopy(newch)
 if r['id']==newn['id']:r['data']['text']=oldch['data']['text']
 assert r==oldch
newpin=save('C0563-fullTR-compilation-operation-v2.json',new);seq=copy.deepcopy(prior['sequence']);count=0
for i,p in enumerate(seq):
 if p['path']==member['path']:seq[i]=newpin;count+=1
assert count==1
for i,p in enumerate(seq):
 o=load(p['path']);p['index']=i+1;p['operation_id']=o['id'];p['targets']=[{'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()} for x in o['changes']]
def reid(x):
 if isinstance(x,dict):return {k:reid(v) for k,v in x.items()}
 if isinstance(x,list):return [reid(v) for v in x]
 return new['id'] if x==old['id'] else x
cross=[]
for p in seq:
 for x in load(p['path'])['changes']:
  for e in x['evidence']:
   if e['object']==newn['id']:cross.append({'dependent':x['id'],'basis':e,'full_candidate_payload':x,'member_pin':p,'primary_individual_disposition':None})
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;fan=[dict(t) for t in c.execute('select * from dependency where basis_revision_id in(select id from revision where object_id=?)',(newn['id'],))];assert not fan
inp=save('exact-source-and-native-candidate-reconstruction-with-incoming-v2.json',{'new_source_pin':{'path':str(specp),'sha256':sha(specp)},'old_source_pin':{'path':am['prior_spec'],'sha256':am['prior_sha256']},'old_member_pin':member,'new_member_pin':newpin,'two_exact_embedded_edits':am['edits'],'all_other17rows_data_header_annual_arrays_fullpayload_evidence_origins_metadata_exact_unchanged':True,'native_NEW_expectedVersion_null_nativeVersion1':True,'actual_native_incoming_edges':fan,'full_candidate_incoming_edges':cross,'diagnostic_old_payload_hash_must_not_equal_amended_TR_hash':{'old_text_sha256':hashlib.sha256(oldn['content'].encode()).hexdigest(),'new_text_sha256':hashlib.sha256(newn['content'].encode()).hexdigest()},'diagnostic97_and_actual328_files_immutable_untouched':True,'old_diagnostic343_match_does_not_certify_new_stage_wholepayload':True})
m=save('current113-C0563-fullTR-amended-membership-inventory-v2.json',{'candidate_members':seq,'members':113,'unique_targets':777,'explicit_member_supersession':{'old':member,'new':newpin},'duplicate_targets':0,'global_source_approval':False});q=save('concrete-current113-C0563-fullTR-amended-sequence-proposal-v2.json',{'sequence':seq,'members':113,'unique_targets':777,'constraints':reid(prior['constraints']),'static_head_order_violations':prior['static_head_order_violations'],'membership_pin':m,'basis_IDS_versions_arrayorder_unchanged':True,'fresh_source_and_independent_hash_binding_and_fresh_full10_stage_required':True,'no_native_PASS_or_stage':True});f=save('bounded-C0563-compilation-amendment-handoff-production-v2.json',{'source_pin':{'path':str(specp),'sha256':sha(specp)},'input_pin':inp,'membership_pin':m,'proposal_pin':q,'changed_native_NEW_payloads':1,'embedded_fields':2,'failed_mechanical_attempts':[],'primary_compilation_propagation_failure_preserved':am['failure'],'elapsed_seconds':time.time()-start,'model_usage_root_collect_after_final':True,'no_stage_probe_apply_actual328_modification':True});print({'input':inp,'membership':m,'proposal':q,'receipt':f,'candidateincoming':len(cross)})
