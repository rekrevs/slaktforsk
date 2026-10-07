import json,pathlib,hashlib,copy,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0425-two-question-title-body-amendment-v2';w.mkdir(exist_ok=False);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,x):
 p=w/n;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
sp=b/'source-review/C-0425-selected23-question-path-decisions-v2.json';assert sha(sp)=='25ea48e9a624ffa9f0e4983908d495d417f520fd60b6d374cc84f3ad42e884f7';z=load(sp);ap=pathlib.Path(z['future_scope_amendment']['prior_pin']['path']);assert sha(ap)==z['future_scope_amendment']['prior_pin']['sha256'];a=load(ap);ids={'P-0096/Q-02','P-0101/Q-03'};proof=[]
for x,y in zip(a['objects'],z['objects']):
 assert x['current']==y['current'];oid=x['current']['object_id']
 if oid not in ids:assert x==y;continue
 restored=copy.deepcopy(y);changes={e['field']:e for e in x['edits']}
 for e in restored['edits']:
  if e['field'] in ['data.body','data.title']:
   if e['field'] in changes:e['new']=changes[e['field']]['new']
   else:assert e['old']==x['current']['data'][e['field'][5:]]
 restored['edits']=[e for e in restored['edits'] if e['field'] in changes];assert restored==x;proof.append({'old_full_decision':x,'new_full_decision':y})
mp=b/'implementation/C0425-forty-caveat-two-body-amendment-v1/current123-candidate-membership-inventory-v1.json';assert sha(mp)=='62d6f8d4bd00eaa7a2e8668c245cfdc83975e67639e691b0ea781a11ab8f21b7';m=load(mp);matches=[p for p in m['candidate_members'] if any(x['id'] in ids for x in load(p['path'])['changes'])];assert len(matches)==1;oldmember=matches[0];assert sha(oldmember['path'])==oldmember['sha256'];oldop=load(oldmember['path']);new=copy.deepcopy(oldop);fieldproof=[]
for x in new['changes']:
 if x['id'] not in ids:continue
 oid=x['id'];prior=next(t for t in a['objects'] if t['current']['object_id']==oid);current=next(t for t in z['objects'] if t['current']['object_id']==oid);oldpayload=copy.deepcopy(x)
 for field in ['data.body','data.title']:
  oldedit=next((e for e in prior['edits'] if e['field']==field),None);expected=oldedit['new'] if oldedit else prior['current']['data'][field[5:]];e=next(e for e in current['edits'] if e['field']==field);assert x['data'][field[5:]]==expected;x['data'][field[5:]]=e['new']
 restore=copy.deepcopy(x);restore['data']['body']=oldpayload['data']['body'];restore['data']['title']=oldpayload['data']['title'];assert restore==oldpayload;fieldproof.append({'id':oid,'whole_old_payload':oldpayload,'whole_new_payload':copy.deepcopy(x),'only_body_title_changed':True,'latest_40_caveats_exact_preserved':True})
assert len(fieldproof)==2;new['id']=oldop['id']+'/two-Q-title-body-v2';new['reason']=oldop['reason']+'; exact twoQtitle/body source amendment '+sha(sp);pin=save('shared-question-path-operation-twoQ-v2.json',new);pp=save('full-source-and-latest-candidate-reconstruction-proof-v1.json',{'source_pins':[{'path':str(p),'sha256':sha(p)} for p in [sp,ap]],'source_v1_v2_proof':proof,'whole_old_new_actuals':fieldproof,'all_other18_change_payloads_exact':True,'all21_other_source_decisions_exact':True,'explicit_old_member':oldmember});save('settled-module-receipt-v1.json',{'source_pins':[{'path':str(sp),'sha256':sha(sp)}],'candidate_modules':[pin],'reconstruction_pin':pp,'full_field_count':4,'failed_attempts':[],'elapsed_seconds':time.time()-start});print(pin)
