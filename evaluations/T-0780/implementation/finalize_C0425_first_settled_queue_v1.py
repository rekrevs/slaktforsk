import json,pathlib,sqlite3,hashlib,time,collections
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0425-first-settled-queue-v1';c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
load=lambda p:json.load(open(p))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
r=load(w/'settled-module-receipt-v1.json');seq=[p for p in r['candidate_modules'] if 'operation-' in p['path']];old=load(b/'implementation/C0685-C0563-split-proposal-v2/current-partial-member-schema-and-repair-coverage-v3.json');priorpaths=[]
def paths(x):
 if isinstance(x,dict):
  if 'path' in x and str(x['path']).endswith('.json'):
   p=pathlib.Path(x['path'])
   if p.exists():
    z=load(p)
    if isinstance(z,dict) and 'changes' in z:priorpaths.append(str(p))
  for v in x.values():paths(v)
 elif isinstance(x,list):
  for v in x:paths(v)
paths(old);paths(load(b/'implementation/C0561-final-expanded-queue-v1/all-history-fanout-and-concrete-sequence-proposal-v2.json'));prior={}
for p in set(priorpaths):
 for ch in load(p)['changes']:prior.setdefault(ch['id'],[]).append({'path':p,'sha256':sha(p),'expectedVersion':ch['expectedVersion'],'full_payload':ch})
overlaps=[];targets={};edges=[];full={};versions={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};viol=[];supportcount=0;extras=[]
for s in seq:
 assert sha(s['path'])==s['sha256'];op=load(s['path']);s['operation_id']=op['id'];s['targets']=[]
 for ch in op['changes']:
  assert ch['id'] not in targets;targets[ch['id']]=ch
  if ch['id'] in prior:overlaps.append({'id':ch['id'],'new':ch,'prior':prior[ch['id']],'Astra_disposition':None})
  assert versions.get(ch['id'])==ch['expectedVersion']
  for e in ch['evidence']:
   assert set(e)=={'object','version','role','note'} and isinstance(e['version'],int) and e['version']>0;supportcount+=1
   if versions.get(e['object'])!=e['version']:viol.append({'target':ch['id'],'basis':e,'current_sequential_version':versions.get(e['object'])})
  versions[ch['id']]=(ch['expectedVersion'] or 0)+1;s['targets'].append({'id':ch['id'],'expectedVersion':ch['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  if ch['expectedVersion'] is not None:
   for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(ch['id'],)):
    e=dict(row);edges.append({'changed_target':ch['id'],'edge':e,'Astra_disposition':None});rid=e['revision_id']
    if rid not in full:
     z=dict(c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone());z['data']=dict(c.execute('select * from '+z['kind']+' where revision_id=?',(rid,)).fetchone());z['origins']=[dict(q) for q in c.execute('select * from origin where revision_id=?',(rid,))];z['evidence']=[dict(q) for q in c.execute('select * from dependency where revision_id=? order by basis_revision_id,role',(rid,))];full[rid]=z
# Individual support-amendment declarations are separately bound and remain at end of each approved evidence array.
for source in r['source_pins']:
 for obj in load(source['path'])['objects']:
  if obj.get('additional_required_support'):
   ch=targets[obj['current']['object_id']];e=obj['additional_required_support'];expect={'object':e['basis_revision_id'].rsplit('@',1)[0],'version':int(e['basis_revision_id'].rsplit('@',1)[1]),'role':e['role'],'note':e['note']};assert ch['evidence'][-1]==expect;extras.append({'target':ch['id'],'exact_last_support':expect,'source_pin':source})
p=save('full-all-history-fanout-overlap-and-extra-support-input-v1.json',{'all_incoming_edges':edges,'full_native_objects':full,'prior_ready_unique_targets':len(prior),'prior_candidate_overlaps':overlaps,'exact_additional_required_support':extras,'source_decisions_required_before_dependent_changes':True});q=save('concrete-first-queue-sequence-proposal-v1.json',{'scope':'C0425 five settled modules only; not whole scope or whole10 gate','sequence':seq,'unique_targets':len(targets),'revisions':86,'new_transcriptions':5,'static_evidence_entries':supportcount,'static_violations':viol,'overlap_count':len(overlaps),'all_history_incoming_edges':len(edges),'current_incoming_edges':sum(z['edge']['is_current'] for z in edges),'full_incoming_objects':len(full),'individual_fanout_input_pin':p,'primary_exact_sequence_hash_binding_required':True,'primary_incoming_dispositions_pending':True,'no_generic_rebind_or_resolution':True,'applies':0});assert not viol and not overlaps
save('bounded-first-queue-handoff-and-production-v1.json',{'source_pins':r['source_pins'],'module_receipt':{'path':str(w/'settled-module-receipt-v1.json'),'sha256':sha(w/'settled-module-receipt-v1.json')},'fanout_pin':p,'sequence_pin':q,'source_v1_v2_failed_contract_specs_preserved':True,'source_additional_TR_support_count':len(extras),'failed_attempts':[{'type':'read_only_schema_inventory','reason':'IndexError on intentionally empty objects list in full-transcription spec; retry used empty-list-safe inventory; no candidates or source inputs changed.'}],'elapsed_measured_finalization_seconds':time.time()-start,'full_phase_elapsed_unobserved_not_zero':True,'model_usage_unknown_root_collect_after_final':True,'immutable_actual328_v3_or_probe_changes':0,'stage_probe_apply_count':0});print({'sequence':q,'fanout':p,'incoming':len(edges),'full_objects':len(full),'extras':len(extras),'prior_targets':len(prior)})
