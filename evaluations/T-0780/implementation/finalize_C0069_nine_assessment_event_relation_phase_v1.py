import json,pathlib,hashlib,sqlite3,copy,time
b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0069-nine-assessment-event-relation-queue-v1';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;r=load(w/'settled-module-receipt-v1.json');pin=next(p for p in r['candidate_modules'] if 'operation-' in p['path']);priorp=b/'implementation/C0069-twentysix-theme-queue-v1/concrete-current105-partial-sequence-and-constraint-proposal-v1.json';prior=load(priorp);seq=copy.deepcopy(prior['sequence']);f98=next(ch for ch in load(pin['path'])['changes'] if ch['id']=='F-P-0098-birth_place-books');oldbases={e['object'] for e in f98['evidence'] if e['version']==1};positions=[i for i,p in enumerate(seq) if any(ch['id'] in oldbases for ch in load(p['path'])['changes'])];seq.insert(min(positions),pin);heads={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']};targets={};viol=[];constraints=[]
for i,p in enumerate(seq):
 op=load(p['path']);assert sha(p['path'])==p['sha256'];p['index']=i+1;p['operation_id']=op['id'];p['targets']=[]
 for x in op['changes']:
  assert x['id'] not in targets,('overlap',x['id']);assert heads.get(x['id'])==x['expectedVersion'];targets[x['id']]=(x,p);p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in x['evidence']:
   assert set(e)=={'object','version','role','note'} and type(e['version']) is int and e['version']>0
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':op['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in op['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in op['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==106 and len(targets)==761;assert viol==prior['static_head_order_violations'];fan=[];native={}
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
cores=[i['current'] for i in load(b/'source-review/C-0069-nine-assessment-event-relation-decisions-v1.json')['objects'] if not i['edits']];assert len(cores)==4

spec=load(b/'source-review/C-0069-nine-assessment-event-relation-decisions-v1.json');exception=[]
for item in spec['objects']:
 ch=targets.get(item['current']['object_id'])
 if not ch or not item['edits']:continue
 new=ch[0]['data'].get('outcome');old=item['current']['data'].get('outcome')
 if old!=new:exception.append({'target':item['current']['id'],'old':old,'new':new})
assert not exception

ordered=[]
for ch in load(pin['path'])['changes']:
 if ch['id'] in ['E-birth-P-0098','F-P-0098-birth_place-books']:
  assert ch['evidence'][-2]['object']=='R-c09147d982c0d73a26f87c03' and ch['evidence'][-1]['object']=='TR-T0780-C0069-fullpost';ordered.append({'target':ch['id'],'last_two_exact_ordered_edges':ch['evidence'][-2:]})
inp=save('stronger-C70-support-and-all-history-incoming-input-v1.json',{'fanouts':fan,'full_native_objects':native,'full_declared_support_bases':bases,'four_full_legacy_review_retains':cores,'target_overlap_zero':True,'explicit_outcome_exception_proof':exception,'C70_before_fullTR_proof':ordered,'source_stronger_old_support_full':spec['stronger_old_support_full'],'current_ready_target_overlap_count':0,'individual_dispositions_pending':True,'prior_seven_API_questions_unchanged':viol})
m=save('current106-candidate-membership-inventory-v1.json',{'prior_proposal_pin':{'path':str(priorp),'sha256':sha(priorp)},'candidate_members':seq,'unique_targets':761,'member_count':106,'new_targets':5,'duplicate_targets':0,'global_source_approval':False})
q=save('concrete-current106-partial-sequence-and-constraint-proposal-v1.json',{'sequence':seq,'members':106,'unique_targets':761,'constraints':constraints,'static_head_order_violations':viol,'membership_pin':m,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
f=save('bounded-nine-assessment-event-relation-handoff-production-v1.json',{'source_pins':r['source_pins'],'input_pin':inp,'membership_pin':m,'proposal_pin':q,'revisions':5,'legacy_review_retains':4,'full_field_entries':75,'incoming_edges':len(fan),'full_native_referencers':len(native),'failed_attempts':[],'elapsed_since_candidate_seconds':time.time()-pathlib.Path(pin['path']).stat().st_mtime,'initial_reads_excluded':True,'model_usage_root_collect_after_final':True,'all_outcomes_unchanged':True,'F98_before_O98_proposed_no_rebind':True,'no_stage_probe_apply_actual328_modification':True});print(json.dumps({'input':inp,'membership':m,'proposal':q,'handoff':f,'fanout':len(fan),'native':len(native),'current':sum(x['edge']['is_current'] for x in fan),'constraints':len(constraints)}))
