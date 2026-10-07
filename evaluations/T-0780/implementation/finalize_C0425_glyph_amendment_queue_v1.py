import json,pathlib,copy,hashlib,sqlite3,collections,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0425-glyph-amendment-queue-v1';load=lambda p:json.load(open(p))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=w/n
 encoded=json.dumps(d,ensure_ascii=False,indent=2)+'\n'
 if p.exists():assert p.read_text()==encoded
 else:p.write_text(encoded)
 return {'path':str(p),'sha256':sha(p)}
def diffs(a,z,path=''):
 if type(a)!=type(z):return [{'field':path,'old':a,'new':z}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(a.keys()|z.keys()):out+=diffs(a.get(k),z.get(k),path+'.'+k if path else k)
  return out
 if isinstance(a,list):return [] if a==z else [{'field':path,'old':a,'new':z}]
 return [] if a==z else [{'field':path,'old':a,'new':z}]
r=load(w/'settled-module-receipt-v1.json');priorseqp=b/'implementation/C0425-expanded-research-structured-queue-v1/concrete-current76-partial-sequence-reposition-proposal-v2.json';prior=load(priorseqp)['sequence'];oldtarget={ch['id']:(ch,s) for s in prior for ch in load(s['path'])['changes']};oldmemberids={s['operation_id']:s for s in prior};source_by_target={};specdiff=[];formerly=[]
for pin in r['source_pins']:
 p=pathlib.Path(pin['path']);oldp=p.with_name(p.name.replace('-v3.json','-v2.json') if 'biography' in p.name else p.name.replace('-v2.json','-v1.json'));new=load(p);old=load(oldp);a={o['current']['id']:o for o in old['objects']};z={o['current']['id']:o for o in new['objects']};assert a.keys()==z.keys()
 for rid,o in z.items():
  assert a[rid]['current']==o['current'];source_by_target[o['current']['object_id']]=(o,pin,a[rid]);changes=diffs(a[rid],o)
  if changes:specdiff.append({'object':rid,'old_spec':{'path':str(oldp),'sha256':sha(oldp)},'new_spec':pin,'exact_spec_differences':changes})
  if not a[rid]['edits'] and o['edits']:formerly.append(o['current']['object_id'])
 if new['new_objects']:
  assert [n['id'] for n in old['new_objects']]==[n['id'] for n in new['new_objects']];specdiff.append({'new_transcription_specs':diffs(old['new_objects'],new['new_objects']),'old_spec':{'path':str(oldp),'sha256':sha(oldp)},'new_spec':pin})
# Preserve the original amended 11-wrapper grouped draft; derive two approved order groups without altering targets.
raw=w/'selected13-wrapper-operation-v1.json';op=load(raw);split=[]
for suffix,kind in [('historical-READ-TR-before-records',False),('five-records-last',True)]:
 x=copy.deepcopy(op);x['id']+='-explicit-'+suffix;x['reason']+=' Source explicit_sequence: old READ/TR consumers before R@2, no evidence-version substitution.';x['changes']=[z for z in op['changes'] if (z['kind']=='record')==kind];split.append(save(suffix+'-operation-v1.json',x))
newpins=[p for p in r['candidate_modules'] if 'operation-' in p['path'] and 'selected13-wrapper' not in p['path']]+split;newtargets={ch['id']:(ch,p) for p in newpins for ch in load(p['path'])['changes']};assert len(newtargets)==143
comparisons=[]
for oid,(ch,pin) in newtargets.items():
 if oid not in oldtarget:assert oid in formerly;comparisons.append({'target':oid,'former_retain_to_revision':True,'source_pin':source_by_target[oid][1],'new_candidate_pin':pin});continue
 oldch,oldpin=oldtarget[oid];assert ch['expectedVersion']==oldch['expectedVersion'];delta=diffs(oldch,ch);allowed={e['field'] for e in source_by_target[oid][0]['edits']} if oid in source_by_target else {'data.text','data.reading_note','caveat'}
 assert all(any(d['field']==a or d['field'].startswith(a+'.') for a in allowed) for d in delta),(oid,delta,allowed)
 comparisons.append({'target':oid,'old_candidate_pin':oldpin,'new_candidate_pin':pin,'payload_differences':delta,'target_version_meta_evidence_origins_and_all_unedited_fields_preserved':True})
assert sorted(formerly)==sorted(['O-P-0099-child-Nils-William','O-P-0099-own-r17','F-P-0099-religious_practice-household-examinations'])
# Strict clause matches bind four BIO amendments to previous exact candidate wording.
biospec=load(b/'source-review/C-0425-C0069-ten-expanded-biography-decisions-v3.json');reconstructed={oid:oldtarget[oid][0]['data']['markdown'] for oid in {z['object'] for z in biospec['additive_candidate_amendment']['changes']}}
for amendment in biospec['additive_candidate_amendment']['changes']:
 oid=amendment['object'];assert reconstructed[oid].count(amendment['previous_candidate_clause'])==1;reconstructed[oid]=reconstructed[oid].replace(amendment['previous_candidate_clause'],amendment['replacement_clause'])
assert all(text==newtargets[oid][0]['data']['markdown'] for oid,text in reconstructed.items())
# Explicit member replacement map; one old member can split into two, all originals remain immutable.
replacement=collections.defaultdict(list)
for pin in newpins:
 ids={ch['id'] for ch in load(pin['path'])['changes']};oldids={oldtarget[oid][1]['operation_id'] for oid in ids if oid in oldtarget};assert len(oldids)==1,(pin,oldids);replacement[next(iter(oldids))].append(pin)
sequence=[];mapping=[]
for s in prior:
 reps=replacement.get(s['operation_id'])
 if reps:
  mapping.append({'superseded_member':s,'additive_replacements':reps});sequence+=reps
 else:sequence.append(s)
assert len(sequence)==76
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;heads={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};targets=set();viol=[];schema=[];support=0
for i,s in enumerate(sequence):
 op=load(s['path']);assert sha(s['path'])==s['sha256'];s['index']=i+1;s['operation_id']=op['id'];s['targets']=[]
 for ch in op['changes']:
  assert ch['id'] not in targets;targets.add(ch['id']);assert heads.get(ch['id'])==ch['expectedVersion'];s['targets'].append({'id':ch['id'],'expectedVersion':ch['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
  for e in ch['evidence']:
   support+=1
   if set(e)!={'object','version','role','note'} or type(e['version']) is not int or e['version']<1:schema.append({'target':ch['id'],'edge':e})
   if heads.get(e['object'])!=e['version'] and not any(z['id']==e['object'] and (z['expectedVersion'] or 0)+1==e['version'] for z in op['changes']):viol.append({'target':ch['id'],'basis':e,'proposed_head':heads.get(e['object'])})
 for ch in op['changes']:heads[ch['id']]=(ch['expectedVersion'] or 0)+1
assert len(targets)==622 and not schema
# New incoming inputs include all exact history, not current-head-only filtering.
fan=[];full={}
for oid in formerly:
 for e in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(oid,)):
  e=dict(e);fan.append({'changed_target':oid,'edge':e,'primary_individual_disposition':None});rid=e['revision_id']
  if rid not in full:
   z=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());z['data']=dict(c.execute('select * from '+z['kind']+' where revision_id=?',(rid,)).fetchone());z['origins']=[dict(q) for q in c.execute('select * from origin where revision_id=?',(rid,))];z['evidence']=[dict(q) for q in c.execute('select * from dependency where revision_id=? order by basis_revision_id,role',(rid,))];full[rid]=z
p=save('exact-eight-spec-and-candidate-amendment-comparison-v1.json',{'spec_differences':specdiff,'candidate_comparisons':comparisons,'strict_BIO_previous_clause_matches':True,'formerly_retained_new_revision_targets':formerly,'new_native_growth':3,'newTR_expectedVersion_null_same_version1':True,'all_previous_files_preserved':True});q=save('three-new-target-all-history-fanout-input-v1.json',{'edges':fan,'full_native_objects':full,'primary_individual_decisions_required':True});m=save('explicit-member-supersession-and-current76-amended-membership-v1.json',{'prior_proposal':{'path':str(priorseqp),'sha256':sha(priorseqp)},'member_supersession_map':mapping,'candidate_members':sequence,'unique_targets':622,'member_count':76,'source_bindings_pending':True,'duplicate_native_targets':0,'schema_errors':schema,'evidence_entries_checked':support,'incomplete_scopes':['C0425-final','C0060','C0069'],'not_global_approved_sequence':True});v=save('concrete-current76-amended-partial-sequence-proposal-v1.json',{'sequence':sequence,'member_map_pin':m,'unique_targets':622,'members':76,'static_head_order_violations':viol,'source_explicit_F99_before_O99r17':True,'requires_primary_fresh_global_hash_binding':True,'source_representation_cases_separately_pending_or_bound':True,'no_global_source_or_native_PASS':True,'stage_probe_apply':0});save('bounded-glyph-amendment-handoff-and-production-v1.json',{'source_manifest':{'path':str(b/'source-review/C-0425-three-glyph-exact-consequence-amendment-manifest-v1.json'),'sha256':sha(b/'source-review/C-0425-three-glyph-exact-consequence-amendment-manifest-v1.json')},'source_pins':r['source_pins'],'comparison_pin':p,'new_incoming_pin':q,'membership_pin':m,'sequence_pin':v,'newly_revised_incoming_edges':len(fan),'newly_revised_full_incoming_objects':len(full),'failed_attempts':2,'elapsed_finalize_seconds':time.time()-start,'elapsed_builder_seconds':r['elapsed_seconds'],'full_phase_elapsed_unknown_not_zero':True,'model_usage_unknown_root_collect_after_final':True,'actual328_probe_stage_mutations':0});print({'comparison':p,'fanout':q,'membership':m,'sequence':v,'incoming':len(fan),'objects':len(full),'violations':len(viol)})
