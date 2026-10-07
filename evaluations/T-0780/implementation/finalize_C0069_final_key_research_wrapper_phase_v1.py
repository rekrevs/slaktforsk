import json,pathlib,hashlib,sqlite3,copy,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0069-final-key-research-queue-v1';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;r=load(w/'settled-module-receipt-v1.json');pins=[p for p in r['candidate_modules'] if 'operation-' in p['path']];key=next(p for p in pins if 'twelve-key' in p['path']);research=next(p for p in pins if 'two-research' in p['path']);wr=load(b/'implementation/C0069-three-wrapper-queue-v1/settled-module-receipt-v1.json');wrapper=next(p for p in wr['candidate_modules'] if 'operation-' in p['path']);priorp=b/'implementation/C0069-nine-assessment-event-relation-queue-v1/concrete-current106-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp);seq=copy.deepcopy(prior['sequence']);idx={x['id']:(x,p) for p in seq for x in load(p['path'])['changes']};oldkey=idx['KEY-P-0102-4e44704aaa76'][1];proof=[]
for x in load(key['path'])['changes']:
 old=idx[x['id']][0];assert x['expectedVersion']==old['expectedVersion']
 if x['id']!='KEY-P-0102-4e44704aaa76':assert x==old;proof.append({'target':x['id'],'whole_payload_exact_unchanged':True});continue
 restore=copy.deepcopy(x);restore['data']['body']=old['data']['body'];add=restore['evidence'].pop();sp=next(i for i in load(b/'source-review/C-0069-twelve-key-decisions-v2.json')['objects'] if i['current']['object_id']==x['id'])['additional_required_support'];assert add=={'object':sp['basis_revision_id'].rsplit('@',1)[0],'version':int(sp['basis_revision_id'].rsplit('@',1)[1]),'role':sp['role'],'note':sp['note']};assert restore==old;proof.append({'target':x['id'],'body_and_one_exact_ordered_stronger_support_only':add})
for i,p in enumerate(seq):
 if p['path']==oldkey['path']:seq[i]=key
op=load(wrapper['path']);record=copy.deepcopy(op);record['id']+='-record-last-proposal';record['reason']+='; payload-identical record-last split proposed for primary approval.';record['changes']=[x for x in op['changes'] if x['kind']=='record'];oldread=copy.deepcopy(record);oldread['id']=op['id']+'-oldTR-READ-before-record-proposal';oldread['changes']=[x for x in op['changes'] if x['kind']!='record'];rp=save('record-last-split-proposal-v1.json',record);tp=save('oldTR-READ-before-record-split-proposal-v1.json',oldread);assert len(record['changes'])==1 and len(oldread['changes'])==2
sourcep=next(p for p in seq if any(x['id']=='S-0037' for x in load(p['path'])['changes']));seq.remove(sourcep);seq=seq[:-1]+[research,tp,rp,sourcep]+seq[-1:]
heads={t['object_id']:t['version'] for t in c.execute('select object_id,max(version) version from revision group by object_id')};updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']};targets={};constraints=[];viol=[]
for i,p in enumerate(seq):
 o=load(p['path']);assert sha(p['path'])==p['sha256'];p['index']=i+1;p['operation_id']=o['id'];p['targets']=[]
 for x in o['changes']:
  assert x['id'] not in targets,('overlap',x['id']);assert heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=(x,p);p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in x['evidence']:
   assert set(e)=={'object','version','role','note'} and type(e['version']) is int and e['version']>0
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':o['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in o['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in o['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==109 and len(targets)==766 and not viol,(len(seq),len(targets),viol)
def full(rid):
 o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))]
 if o['kind']=='record':o['assets']=[dict(t) for t in c.execute('select * from record_asset where revision_id=?',(rid,))];o['media']=[dict(t) for t in c.execute('select * from record_media where revision_id=?',(rid,))]
 return o
selected={x['id'] for p in [key,research,wrapper] for x in load(p['path'])['changes']};fan=[];native={};bases={}
for oid in selected:
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  row=dict(row);fan.append({'changed_target':oid,'edge':row,'individual_primary_disposition':None,'current_candidate_if_revised':targets.get(row['object_id'])});native[row['revision_id']]=full(row['revision_id'])
for p in [key,research,wrapper]:
 for x in load(p['path'])['changes']:
  for e in x['evidence']:
   rid=e['object']+'@'+str(e['version']);row=c.execute('select 1 from revision where id=?',(rid,)).fetchone();bases[rid]=full(rid) if row else {'explicit_future_candidate':targets[e['object']]}
for x in op['changes']:
 old=full(x['id']+'@'+str(x['expectedVersion']))
 if x['kind']=='record':assert x['data']=={k:v for k,v in old['data'].items() if k!='revision_id'};assert x['assets']==[{'path':t['asset_path'],'region':t['region']} for t in old['assets']];assert x['media']==[{'id':t['asset_id'],'region':t['region']} for t in old['media']]
 if x['kind']=='transcription':assert x['data']['text']==old['data']['text']
ip=save('key-amendment-wrapper-full-native-and-all-history-fanout-input-v1.json',{'key_exact_amendment_proof':proof,'fanouts':fan,'full_native_objects':native,'full_support_bases':bases,'oldTR_text_record_data_asset_media_arrays_exact_preserved':True,'proposed_oldTR_READ_before_R2_and_all_R1_consumers_before_R2':True,'S0037_group_payload_unchanged_moved_after_R69_R2_proposal':sourcep,'primary_individual_dispositions_pending':True})
m=save('current109-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(priorp),'sha256':sha(priorp)},'explicit_superseded_key_member':oldkey,'new_key_member':key,'candidate_members':seq,'unique_targets':766,'member_count':109,'new_targets':5,'duplicate_targets':0,'global_source_approval':False})
q=save('concrete-current109-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':109,'unique_targets':766,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':m,'fresh_primary_global_hash_binding_required':True,'split_and_source_group_reordering_proposal_not_approval':True,'no_native_PASS_stage_or_request_resolution':True})
f=save('closed-three-module-final-selected-wrapper-handoff-production-v1.json',{'source_pins':r['source_pins']+wr['source_pins'],'input_pin':ip,'membership_pin':m,'proposal_pin':q,'existing_key_targets_amended':1,'other_two_key_payloads_identical':True,'new_research_revisions':2,'new_wrapper_revisions':3,'full_field_entries':r['full_field_count']+wr['full_field_count'],'incoming_edges':len(fan),'current_edges':sum(x['edge']['is_current'] for x in fan),'full_native_referencers':len(native),'failed_attempts':[],'elapsed_since_first_candidate_seconds':time.time()-min(pathlib.Path(p['path']).stat().st_mtime for p in [key,research,wrapper]),'prebuild_reads_excluded':True,'model_usage_root_collect_after_final':True,'closed_three_module_cap_complete':True,'Q102_primary_question_not_modified':True,'no_stage_probe_apply_actual328_modification':True});print(json.dumps({'input':ip,'membership':m,'proposal':q,'handoff':f,'fanout':len(fan),'native':len(native),'current':sum(x['edge']['is_current'] for x in fan),'constraints':len(constraints)}))
