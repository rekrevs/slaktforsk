import json,pathlib,hashlib,sqlite3,copy,time
b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0561-P0437-network-date-structured-copy-queue-v1';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;r=load(w/'settled-module-receipt-v1.json');pin=next(p for p in r['candidate_modules'] if 'operation-' in p['path']);priorp=b/'implementation/C0425-THEME99BO-body-amendment-v3/concrete-current123-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp);seq=copy.deepcopy(prior['sequence']);seq.append(pin);heads={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']};targets={};viol=[];constraints=[]
for i,p in enumerate(seq):
 op=load(p['path']);assert sha(p['path'])==p['sha256'];p['index']=i+1;p['operation_id']=op['id'];p['targets']=[]
 for x in op['changes']:
  assert x['id'] not in targets,('overlap',x['id']);assert heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=(x,p);p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in x['evidence']:
   assert set(e)=={'object','version','role','note'} and type(e['version']) is int and e['version']>0
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':op['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in op['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in op['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==124 and len(targets)==825;assert viol==prior['static_head_order_violations'];fan=[];native={}
for ch in load(pin['path'])['changes']:
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(ch['id'],)):
  row=dict(row);fan.append({'changed_target':ch['id'],'edge':row,'primary_individual_disposition':None,'current_candidate_if_revised':targets.get(row['object_id'])});rid=row['revision_id']
  if rid not in native:
   o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];native[rid]=o

bases={}
for ch in load(pin['path'])['changes']:
 for e in ch['evidence']:
  rid=e['object']+'@'+str(e['version']);row=c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone()
  if not row:assert e['object'] in targets;bases[rid]={'explicit_future_candidate':targets[e['object']]};continue
  o=dict(row);o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))];bases[rid]=o

for o in list(native.values())+list(bases.values()):
 if o.get('kind')=='record':
  o['assets']=[dict(t) for t in c.execute('select * from record_asset where revision_id=?',(o['id'],))];o['media']=[dict(t) for t in c.execute('select * from record_media where revision_id=?',(o['id'],))]
spec=load(b/'source-review/C-0561-P0437-network-date-structured-copy-decisions-v1.json');retains=[x['current'] for x in spec['objects'] if not x['edits']];assert len(retains)==0
old=spec['objects'][0]['current'];new=load(pin['path'])['changes'][0];oldjson=json.loads(old['data']['value_json']);newjson=new['data']['value_json'];restore=copy.deepcopy(newjson);restore['routes'][0]=oldjson['routes'][0];assert restore==oldjson and newjson['routes'][0][1]==json.loads(spec['objects'][0]['edits'][0]['new'])['routes'][0][1];
inp=save('full-source-history-incoming-assets-bases-input-v1.json',{'fanouts':fan,'whole_old_native':old,'whole_new_candidate':new,'only_routes0_date_json_value_changed':True,'full_native_objects':native,'full_declared_support_bases':bases,'whole_retains':retains,'source_decisions':spec['objects'],'individual_dispositions_pending':True,'candidate_overlap_zero':True})
m=save('current124-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(priorp),'sha256':sha(priorp)},'candidate_members':seq,'unique_targets':825,'member_count':124,'duplicate_targets':0,'global_source_approval':False})
q=save('concrete-current124-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':124,'unique_targets':825,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':m,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
f=save('bounded-P0437-structured-copy-production-receipt-v1.json',{'source_pins':r['source_pins'],'input_pin':inp,'membership_pin':m,'proposal_pin':q,'changes':1,'retains':0,'full_field_entries':r['full_field_count'],'history_incoming_edges':len(fan),'current_incoming_edges':sum(x['edge']['is_current'] for x in fan),'failed_attempts':[],'elapsed_since_candidate_seconds':time.time()-pathlib.Path(pin['path']).stat().st_mtime,'no_stage_apply_or_source_judgment':True});print(json.dumps({'receipt':f,'membership':m,'proposal':q,'input':inp,'incoming':len(fan)}))
