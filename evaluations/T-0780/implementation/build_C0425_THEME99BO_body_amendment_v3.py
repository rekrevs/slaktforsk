import json,pathlib,hashlib,copy,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0425-THEME99BO-body-amendment-v3';w.mkdir(exist_ok=False);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,x):
 p=w/n;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
sp=b/'source-review/C-0425-selected71-theme-decisions-v3.json';assert sha(sp)=='6b8e8f1c3ad33a3a16ad64d895c80d36d566b78c16adb07f4983bd3a4793b63d';z=load(sp);am=z['undated_reference_amendment'];ap=pathlib.Path(am['prior_path']);assert sha(ap)==am['prior_sha256'];a=load(ap);oid=am['object_id'];sourceproof=[]
for x,y in zip(a['objects'],z['objects']):
 assert x['current']==y['current']
 if x['current']['object_id']!=oid:assert x==y;continue
 restore=copy.deepcopy(y);e=next(e for e in restore['edits'] if e['field']=='data.body');assert e['new']==am['new'];e['new']=am['prior_candidate_new'];assert restore==x;sourceproof=[x,y]
assert len(sourceproof)==2
mp=b/'implementation/C0425-two-question-title-body-amendment-v2/current123-candidate-membership-inventory-v1.json';assert sha(mp)=='820ed5f39003850a9ae92f24d5a76daae88252f912557e8854e3df8988d31a71';m=load(mp);matches=[p for p in m['candidate_members'] if any(x['id']==oid for x in load(p['path'])['changes'])];assert len(matches)==1;oldmember=matches[0];assert sha(oldmember['path'])==oldmember['sha256'];oldop=load(oldmember['path']);new=copy.deepcopy(oldop);oldpayload=next(x for x in oldop['changes'] if x['id']==oid);payload=next(x for x in new['changes'] if x['id']==oid);assert payload['data']['body']==am['prior_candidate_new'];payload['data']['body']=am['new'];restore=copy.deepcopy(payload);restore['data']['body']=oldpayload['data']['body'];assert restore==oldpayload
for x,y in zip(oldop['changes'],new['changes']):
 if x['id']!=oid:assert x==y
new['id']=oldop['id']+'/THEME99BO-body-v3';new['reason']=oldop['reason']+'; exact THEME99BO body-only source amendment '+sha(sp);pin=save('shared-theme-operation-THEME99BO-v3.json',new);pp=save('full-source-latest-candidate-body-reconstruction-proof-v1.json',{'source_pins':[{'path':str(p),'sha256':sha(p)} for p in [sp,ap]],'source_v2_v3_full_decisions':sourceproof,'other70_source_decisions_exact':True,'whole_old_new_actuals':[oldpayload,payload],'only_one_data_body_changed':True,'all_other52_candidate_payloads_exact':len(oldop['changes'])==53,'all40_caveat_and_Q23_amendments_preserved':True,'explicit_old_member':oldmember});save('settled-module-receipt-v1.json',{'source_pins':[{'path':str(sp),'sha256':sha(sp)}],'candidate_modules':[pin],'reconstruction_pin':pp,'full_field_count':1,'failed_attempts':[],'elapsed_seconds':time.time()-start});print(pin)
