import json,pathlib,hashlib,copy,sqlite3,time,collections
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0425-forty-caveat-two-body-amendment-v1';w.mkdir(exist_ok=False);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,x):
 p=w/n;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
cp=b/'source-review/C-0425-forty-first-year-candidate-caveat-amendment-v1.json';sp=b/'source-review/C-0425-selected77-contract-decisions-v4.json';assert sha(cp)=='f9d106d21294669176a5afbedaf717c8195aab3574a88687bce12774521dbc1c';assert sha(sp)=='7d9dcaec18e0e23524730723d6a1e5b96919edba0ac308e63c217522941724f7';cs=load(cp);ss=load(sp);ap=pathlib.Path(ss['continuation_scope_amendment']['prior_path']);assert sha(ap)==ss['continuation_scope_amendment']['prior_sha256'];oldss=load(ap);am=ss['continuation_scope_amendment']['changes']
mp=b/'implementation/C0425-ADOPT0099-glyph-amendment-v2/current123-candidate-membership-inventory-v1.json';assert sha(mp)=='315bd2e67310c2206182567b8fb0d48854d0a88822a9608842c8788868d41c34';membership=load(mp);seq=copy.deepcopy(membership['candidate_members']);ops={p['path']:load(p['path']) for p in seq};assert all(sha(p['path'])==p['sha256'] for p in seq);targets=collections.defaultdict(list)
for p in seq:
 for i,x in enumerate(ops[p['path']]['changes']):targets[x['id']].append((p,i,x))
assert len(cs['objects'])==40 and len({x['object_id'] for x in cs['objects']})==40 and len(am)==2
updates={};table=[];proof=[]
for x in cs['objects']:
 matches=targets[x['object_id']];assert len(matches)==1;p,i,current=matches[0];assert p['path']==x['operation_pin']['path'] and p['sha256']==x['operation_pin']['sha256'];assert x['candidate_pointer']=='/changes/'+str(i) and current==x['candidate_full'];assert x['field']=='caveat' and current['caveat']==x['old'];new=updates.setdefault(p['path'],copy.deepcopy(ops[p['path']]));new['changes'][i]['caveat']=x['new'];table.append({'object_id':x['object_id'],'field':'caveat','old':x['old'],'new':x['new'],'individual_source_decision':x,'prior_operation_pin':p})
for x in am:
 matches=targets[x['object_id']];assert len(matches)==1;p,i,current=matches[0];assert x['field']=='data.body' and current['data']['body']==x['prior_candidate_new'];new=updates.setdefault(p['path'],copy.deepcopy(ops[p['path']]));new['changes'][i]['data']['body']=x['new'];table.append({'object_id':x['object_id'],'field':'data.body','old':x['prior_candidate_new'],'new':x['new'],'individual_source_decision':x,'prior_operation_pin':p})
assert len(table)==42;changedids={x['object_id'] for x in table};allowed=collections.defaultdict(set)
for x in table:allowed[x['object_id']].add(x['field'])
sourceproof=[]
for a,z in zip(oldss['objects'],ss['objects']):
 assert a['current']==z['current'];oid=z['current']['object_id']
 if oid not in {x['object_id'] for x in am}:assert a==z
 else:
  changes=next(x for x in am if x['object_id']==oid);assert len(a['edits'])==len(z['edits']);ae=next(e for e in a['edits'] if e['field']=='data.body');ze=next(e for e in z['edits'] if e['field']=='data.body');assert ae['new']==changes['prior_candidate_new'] and ze['new']==changes['new'];restore=copy.deepcopy(z);next(e for e in restore['edits'] if e['field']=='data.body')['new']=ae['new'];assert restore==a;sourceproof.append({'old_full_decision':a,'new_full_decision':z})
assert len(sourceproof)==2
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
# All77 native headers/data/origins and exact dependency row multisets checked; arrays in source remain untouched.
for item in ss['objects']:
 o=item['current'];h=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(o['id'],)).fetchone());assert all(o[k]==h[k] for k in h);assert dict(c.execute('select * from '+h['kind']+' where revision_id=?',(o['id'],)).fetchone())==o['data'];orig=[dict(z) for z in c.execute('select * from origin where revision_id=?',(o['id'],))];assert len(orig)==len(o['origins']) and all(all(t[k]==s[k] for k in t) for t,s in zip(orig,o['origins']));ev=[dict(z) for z in c.execute('select * from dependency where revision_id=?',(o['id'],))];assert sorted(ev,key=lambda z:json.dumps(z,sort_keys=True))==sorted(o['evidence'],key=lambda z:json.dumps(z,sort_keys=True))
replacementpins=[]
for n,(path,new) in enumerate(updates.items()):
 old=ops[path];assert len(old['changes'])==len(new['changes'])
 for a,z in zip(old['changes'],new['changes']):
  restore=copy.deepcopy(z)
  for field in allowed[a['id']]:
   if field=='caveat':restore['caveat']=a['caveat']
   elif field=='data.body':restore['data']['body']=a['data']['body']
  assert restore==a
  if a!=z:proof.append({'object_id':a['id'],'full_old_payload':a,'full_new_payload':z,'exact_changed_fields':sorted(allowed[a['id']])})
 new['id']=old['id']+'/C0425-exact42-amendment-v1';new['reason']=old['reason']+'; exact joint source42-field amendment '+sha(cp)+' '+sha(sp);pin=save(str(n+1).zfill(2)+'-'+pathlib.Path(path).name.replace('.json','-exact42-v1.json'),new);oldpin=next(p for p in seq if p['path']==path);replacementpins.append({'old_member':oldpin,'new_member':pin});seq[seq.index(oldpin)]=pin
assert sum(len(x['exact_changed_fields']) for x in proof)==42
heads={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};viol=[];seen=set()
for n,p in enumerate(seq):
 op=load(p['path']);p['index']=n+1;p['operation_id']=op['id'];p['targets']=[]
 for x in op['changes']:
  assert x['id'] not in seen and heads.get(x['id'])==x['expectedVersion'];seen.add(x['id']);p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in x['evidence']:
   assert set(e)=={'object','version','role','note'}
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in op['changes']):viol.append({'target':x['id'],'edge':e,'head':heads.get(e['object'])})
 for x in op['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==123 and len(seen)==824 and not viol
native={};fan=[];candidatefan=[]
def nativeobj(rid):
 if rid in native:return
 o=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))]
 if o['kind']=='record':o['assets']=[dict(t) for t in c.execute('select * from record_asset where revision_id=?',(rid,))];o['media']=[dict(t) for t in c.execute('select * from record_media where revision_id=?',(rid,))]
 native[rid]=o
for oid in changedids:
 for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  row=dict(row);fan.append({'changed_target':oid,'edge':row,'individual_source_disposition':None});nativeobj(row['revision_id'])
 for p in seq:
  for x in load(p['path'])['changes']:
   for e in x['evidence']:
    if e['object']==oid:candidatefan.append({'changed_target':oid,'operation_pin':p,'full_referencer_candidate':x,'edge':e})
for obj in proof:
 for e in obj['full_new_payload']['evidence']:
  rid=e['object']+'@'+str(e['version'])
  if c.execute('select 1 from revision where id=?',(rid,)).fetchone():nativeobj(rid)
proofpin=save('whole42-field-source-and-actual-reconstruction-proof-v1.json',{'source_v3_v4_body_proof':sourceproof,'forty_caveat_individual_source_decisions':cs['objects'],'consequence_fields':table,'whole_changed_candidate_payloads':proof,'explicit_member_supersessions':replacementpins,'same_native_versions_no_duplicates':True,'unlisted_fields_and_all_arrays_exact':True})
inp=save('full-current-history-and-candidate-incoming-support-input-v1.json',{'native_fanouts':fan,'full_native_objects':native,'actual_candidate_fanouts':candidatefan,'individual_dispositions_not_inferred':True})
m=save('current123-candidate-membership-inventory-v1.json',{'candidate_members':seq,'member_count':123,'unique_targets':824,'supersessions':replacementpins,'prior_membership_pin':{'path':str(mp),'sha256':sha(mp)},'global_source_approval':False});q=save('concrete-current123-exact42-sequence-proposal-v1.json',{'sequence':seq,'members':123,'unique_targets':824,'static_head_order_violations':viol,'membership_pin':m,'fresh_primary_hash_binding_required':True,'no_stage_or_PASS':True})
r=save('closed-two-module-exact42-production-receipt-v1.json',{'source_pins':[{'path':str(p),'sha256':sha(p)} for p in [cp,sp,ap]],'membership_pin':m,'proposal_pin':q,'reconstruction_pin':proofpin,'full_incoming_pin':inp,'caveat_fields':40,'body_fields':2,'affected_members':len(updates),'changed_targets':len(proof),'all77_full_native_baseline_checks':True,'history_incoming_edges':len(fan),'candidate_incoming_edges':len(candidatefan),'failed_attempts':[],'elapsed_seconds':time.time()-start,'all_first_files_unchanged':True,'no_stage_apply_rebind_or_source11':True});print(json.dumps(r))
