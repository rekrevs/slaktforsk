import pathlib,json,hashlib,copy,time
b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0043-literal-scope-amendment-v3';w.mkdir(exist_ok=True);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
specp=b/'source-review/C-0043-literal-and-initial-scope-amendment-v3.json';assert sha(specp)=='2ff2e3b5bafded654f580f1813c7f57389b65ef3fbdb815b0a366c1ccc680402';s=load(specp);assert sha(s['candidate_input']['path'])==s['candidate_input']['sha256'];approvedold=load(s['candidate_input']['path']);priorp=b/'implementation/all10-final-comparator-movement-queue-v1/concrete-current113-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp);member=next(p for p in prior['sequence'] if any(x['id']=='TR-T0780-C0043-fullpost' for x in load(p['path'])['changes']));old=load(member['path']);new=copy.deepcopy(old);idx={x['id']:x for x in new['changes']};sourceidx={x['id']:x for x in approvedold['changes']};tables=[]
for oid,x in idx.items():
 src=copy.deepcopy(sourceidx[oid]);ev=[]
 for e in src['evidence']:
  if 'object' in e:ev.append(e);continue
  basis=e['basis'] if 'basis' in e else e['basis_revision_id'];obj,v=basis.rsplit('@',1);ev.append({'object':obj,'version':int(v),'role':e['role'],'note':e['note']})
 src['evidence']=ev;assert src==x,oid
for a in s['amendments']:
 x=idx[a['object_id']];assert x['expectedVersion'] is None and a['expectedVersion'] is None and a['native_version']==1
 for e in a['edits']:
  obj=x['data'] if e['field'].startswith('data.') else x;k=e['field'].removeprefix('data.');assert obj[k]==e['old'];obj[k]=e['new'];tables.append({'object':x['id'],'field':e['field'],'old':e['old'],'new':e['new'],'expectedVersion':None,'native_version':1})
for before,after in zip(old['changes'],new['changes']):
 restore=copy.deepcopy(after)
 for a in s['amendments']:
  if a['object_id']!=after['id']:continue
  for e in a['edits']:(restore['data'] if e['field'].startswith('data.') else restore).__setitem__(e['field'].removeprefix('data.'),e['old'])
 assert restore==before
assert len(s['amendments'])==2 and len(new['changes'])==5;new['id']='T-0780/C0043-literal-initial-scope-amendment-v3';new['reason']='T-0780 exact primary amendment '+sha(specp)+'; source literals and initial-subset audit scope only, nativeNEW five preserved, final independent approval pending.';newpin=save('C0043-five-new-literal-scope-operation-v3.json',new);seq=copy.deepcopy(prior['sequence']);matches=0
for i,p in enumerate(seq):
 if p['path']==member['path']:seq[i]=newpin;matches+=1
assert matches==1
for i,p in enumerate(seq):
 o=load(p['path']);p['index']=i+1;p['operation_id']=o['id'];p['targets']=[{'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()} for x in o['changes']]
inp=save('strict-five-payload-reconstruction-and-field-amendment-proof-v3.json',{'source_pin':{'path':str(specp),'sha256':sha(specp)},'approved_original_candidate':s['candidate_input'],'latest_schema_fixed_old_member':member,'new_member':newpin,'fields':tables,'two_new_payloads_changed_other_three_exact_unchanged':True,'all_evidence_array_slots_origins_metadata_unchanged':True,'original_to_canonical_support_schema_reconstruction_exact':True,'same_five_NEW_expectednull_version1':True})
m=save('current113-C0043-amended-membership-inventory-v3.json',{'candidate_members':seq,'member_count':113,'unique_targets':777,'explicit_member_supersession':{'old':member,'new':newpin},'duplicate_targets':0,'global_source_approval':False});q=save('concrete-current113-C0043-amended-sequence-proposal-v3.json',{'sequence':seq,'members':113,'unique_targets':777,'constraints':prior['constraints'],'static_head_order_violations':prior['static_head_order_violations'],'membership_pin':m,'support_edges_and_native_heads_unchanged_exact':True,'fresh_primary_global_hash_binding_required':True,'no_native_PASS_stage_or_request_resolution':True});f=save('bounded-C0043-literal-scope-amendment-production-v3.json',{'proof_pin':inp,'membership_pin':m,'proposal_pin':q,'changed_NEW_payloads':2,'same_native_targets_versions':True,'failed_attempts':[],'no_stage_probe_apply_actual328_modification':True,'model_usage_root_collect_after_final':True});print({'proof':inp,'membership':m,'proposal':q,'receipt':f})
