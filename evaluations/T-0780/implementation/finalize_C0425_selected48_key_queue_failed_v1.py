import json,pathlib,sqlite3,hashlib,time,collections
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0425-selected48-key-queue-v1';c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
load=lambda p:json.load(open(p))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
priorp=b/'implementation/C0425-C0069-relation-identity-queue-v1/current66-candidate-membership-inventory-v1.json';prior=load(priorp);r=load(w/'settled-module-receipt-v1.json');new=[p for p in r['candidate_modules'] if 'operation-' in p['path']];members=prior['candidate_members']+new;targets={};overlaps=[];edges=[];full={};evidence_table=[];sourced=load(r['source_pins'][0]['path'])
for s in members:
 assert sha(s['path'])==s['sha256'];op=load(s['path'])
 for ch in op['changes']:
  if ch['id'] in targets:overlaps.append({'id':ch['id'],'prior':targets[ch['id']],'new_path':s['path'],'primary_disposition':None})
  targets[ch['id']]={'path':s['path'],'sha256':s['sha256'],'change':ch,'operation_id':op['id']}
for obj in sourced['objects']:
 o=obj['current'];pro=targets.get(o['object_id']);old=o['evidence'];changes=obj.get('individual_evidence_replacements',[]);newedges=[dict(z) for z in old]
 for re in changes:
  j=[i for i,e in enumerate(newedges) if e==re['old']];assert len(j)==1;assert re['old']['basis_revision_id']==re['new']['basis_revision_id'];newedges[j[0]]=re['new']
 for i,e in enumerate(old):evidence_table.append({'object_version':o['id'],'index':i,'old':e,'new':newedges[i],'disposition':obj['disposition'],'source_pin':r['source_pins'][0]})
 if obj['edits']:
  ch=pro['change'];assert ch['disposition']==o['disposition'] and ch['evidenceStatus']==o['evidence_status']
  projected=[{'object':z['basis_revision_id'].rsplit('@',1)[0],'version':int(z['basis_revision_id'].rsplit('@',1)[1]),'role':z['role'],'note':z['note']} for z in newedges];assert ch['evidence'][:len(old)]==projected
  for e in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(o['object_id'],)):
   e=dict(e);edges.append({'target':o['object_id'],'edge':e,'primary_disposition':None});rid=e['revision_id']
   if rid not in full:
    z=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());z['data']=dict(c.execute('select * from '+z['kind']+' where revision_id=?',(rid,)).fetchone());z['origins']=[dict(q) for q in c.execute('select * from origin where revision_id=?',(rid,))];z['evidence']=[dict(q) for q in c.execute('select * from dependency where revision_id=? order by basis_revision_id,role',(rid,))];full[rid]=z
assert not overlaps
p=save('individual-evidence-order-replacement-and-all-history-fanout-input-v1.json',{'evidence_rows_including_retains':evidence_table,'incoming_edges':edges,'incoming_full_native_objects':full,'prior465_overlaps':overlaps,'retained_nine_identities_no_new_operations': [o['current']['id'] for o in sourced['objects'] if o['current']['kind']=='identity'],'no_ID_operation_or_M_version_rebind_inferred':True})
# Mechanical concrete global partial proposal preserves previous membership order; its constraints are returned, never auto-resolved.
versions={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};constraints=[];viol=[];schema=[];seq=[];newids={z['id'] for s in new for z in load(s['path'])['changes']};updates={}
for i,s in enumerate(members):
 for ch in load(s['path'])['changes']:updates[ch['id']]={'index':i+1,'operation_id':load(s['path'])['id'],'expectedVersion':ch['expectedVersion'],'newVersion':(ch['expectedVersion'] or 0)+1}
for i,s in enumerate(members):
 op=load(s['path']);seq.append({'index':i+1,'path':s['path'],'sha256':s['sha256'],'operation_id':op['id'],'targets':[{'id':z['id'],'expectedVersion':z['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(z,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()} for z in op['changes']]})
 for ch in op['changes']:
  assert versions.get(ch['id'])==ch['expectedVersion']
  for e in ch['evidence']:
   if set(e)!={'object','version','role','note'}:schema.append({'target':ch['id'],'edge':e})
   up=updates.get(e['object'])
   if up:
    relation='dependent_before_basis_update' if e['version']==up['expectedVersion'] else 'basis_creation_or_update_before_dependent' if e['version']==up['newVersion'] else 'version_requires_source_review'
    constraints.append({'dependent':ch['id'],'dependent_operation':op['id'],'dependent_index':i+1,'basis':e,'basis_update':up,'technical_relation':relation,'source_sequence_grade_required':True})
   valid=versions.get(e['object'])==e['version'] or any(z['id']==e['object'] and (z['expectedVersion'] or 0)+1==e['version'] for z in op['changes'])
   if not valid:viol.append({'dependent':ch['id'],'operation_id':op['id'],'basis':e,'current_proposed_head':versions.get(e['object'])})
 for ch in op['changes']:versions[ch['id']]=(ch['expectedVersion'] or 0)+1
q=save('concrete-current66-partial-sequence-and-constraint-return-v1.json',{'scope':'All current candidate members, incomplete selected10 and not globally approved','sequence':seq,'unique_targets':len(targets),'members':len(members),'schema_errors':schema,'static_head_order_violations':viol,'all_exact_evidence_order_constraints':constraints,'individual_input_pin':p,'prior465_unique_targets_preserved':True,'primary_global_hash_binding_required':True,'no_automatic_reordering_or_splitting':True,'applies':0});assert not schema
m=save('current66-candidate-membership-inventory-v1.json',{'amends_membership_only':{'path':str(priorp),'sha256':sha(priorp)},'candidate_members':members,'unique_targets':len(targets),'prior_targets':465,'new_targets':30,'duplicate_target_conflicts':overlaps,'schema_errors':schema,'global_sequence_and_source_approval':False,'incomplete_scopes':['C0425','C0060','C0069'],'source_flags_preserved_as_data':True})
save('bounded-selected48-key-handoff-and-production-v1.json',{'source_pin':r['source_pins'][0],'revisions':30,'retains':18,'field_rows':384,'individual_evidence_rows':len(evidence_table),'incoming_edges':len(edges),'current_incoming_edges':sum(z['edge']['is_current'] for z in edges),'full_incoming_objects':len(full),'fanout_pin':p,'sequence_pin':q,'membership_pin':m,'static_head_order_violations':len(viol),'failed_attempts':0,'elapsed_seconds':time.time()-start,'builder_elapsed_seconds':r['elapsed_seconds'],'full_phase_elapsed_unknown_not_zero':True,'model_usage_unknown_root_collect_after_final':True,'no_stage_probe_apply_or_actual328_modification':True});print({'fanout':p,'sequence':q,'membership':m,'incoming':len(edges),'violations':len(viol),'constraints':len(constraints)})
