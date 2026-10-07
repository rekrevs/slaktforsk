"""Source-settled exact draft construction only; no stage or canonical code paths."""
import json,copy,hashlib
from pathlib import Path
B=Path('evaluations/T-0781');W=B/'implementation/C0049-core-and-C0067-P0098-drafts-v1'
def load(p):return json.loads(Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def save(n,v):
 p=W/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');return pin(p)
def api(n):
 a={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':{k:json.loads(v) if k.endswith('_json') and isinstance(v,str) else v for k,v in n['data'].items() if k!='revision_id'},'origins':[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in n['origins']],'evidence':[{'object':x['basis_revision_id'].rsplit('@',1)[0],'version':int(x['basis_revision_id'].rsplit('@',1)[1]),'role':x['role'],'note':x['note']} for x in n['evidence']],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 if n['kind']=='record':
  a['assets']=[{'path':x['asset_path'],'region':x['region']} for x in n['assets']];a['media']=[{'id':x['asset_id'],'region':x['region']} for x in n['media']]
 return a
def revise(row,n):
 assert all(n[k]==v for k,v in row['current'].items())
 old=api(n);new=copy.deepcopy(old)
 for e in row['edits']:
  field=e['field'];key=field.split('.')[-1];raw=n['data'] if field.startswith('data.') else n;assert raw[key]==e['old'] and e['old']!=e['new'],(n['id'],field)
  target=new['data'] if field.startswith('data.') else new;target[key]=json.loads(e['new']) if field.startswith('data.') and key.endswith('_json') and isinstance(e['new'],str) else e['new']
 for binding in row.get('evidence_rebinds',[]):
  indices=[i for i,x in enumerate(n['evidence']) if x==binding['old']];assert len(indices)==1 and binding['preserve_role_note_and_position'] is True
  i=indices[0];obj,ver=binding['new_basis_revision_id'].rsplit('@',1);new['evidence'][i]['object']=obj;new['evidence'][i]['version']=int(ver)
 addition=row.get('evidence_addition')
 if addition:
  obj,ver=addition['basis'].rsplit('@',1);item={'object':obj,'version':int(ver),'role':addition['role'],'note':addition['note']};assert item not in new['evidence'];new['evidence'].append(item)
 assert new['origins']==old['origins']
 for k in ['assets','media']:
  if k in old:assert new[k]==old[k]
 allowed={e['field'] for e in row['edits']}
 for k,v in old.items():
  if k in ['data','evidence']:continue
  if k not in allowed:assert new[k]==v
 for k,v in old['data'].items():
  if 'data.'+k not in allowed:assert new['data'][k]==v
 return old,new
def operation(number,name,changes,sourcepin):
 assert len({x['id'] for x in changes})==len(changes)
 op={'id':'T-0781/'+name+'-v1','actor':'codex','reason':'T-0781 AC2/AC3 exact individual sourceapproved draft '+sourcepin['path']+' SHA'+sourcepin['sha256']+'; old/current guards and incoming source dispositions preserved in accompanying table; no global approval, no runtime authorization.','dependencyReviewVersion':2,'changes':changes}
 return save(str(number).zfill(2)+'-'+name+'-draft-operation-v1.json',op)
assert not W.exists();W.mkdir(parents=True)
corepath=B/'source-review/two-settled-fullsource-TR-audit-and-four-wrapper-specifications-v1.json';assert pin(corepath)['sha256']=='83361bcc55e4683a0824ad99fc4f99f7fabd9bd6c8c3f7d7cb970bbef052336b';core=load(corepath)
ip=B/'source-review/C0049-eleven-record-and-one-birth-event-incoming-source-dispositions-v1.json';assert pin(ip)['sha256']=='2c1ad7974b2806dbb1b8a993e1102380f0f49deb87ae87e1aa2da36936a946d8';incoming=load(ip);assert incoming['core_R49_wrapper_production_permitted'] is True
gp=B/'bounded-consequence-inputs-v1/four-source-wrappers-P0057-birth-EP-relation-exact-current-and-allhistory-incoming-v1.json';guards=load(gp);native=load(guards['full_native_pin']['path'])['objects'];rows=[];ops=[]
rev=[x for x in core['revisions'] if 'C0049' in x['object_id'] or x['object_id']=='R-d9840df54c7f19f2454c4d2d' or x['object_id']=='READ-afbfe3f933d234b8f0f60c3e' or x['object_id']=='TR-bf8e09efe7e3e3c20156c785'];assert len(rev)==3
for x in rev:
 n=native[x['current']['id']];old,new=revise(x,n);rows.append({'object_id':x['object_id'],'source_edits':x['edits'],'full_baseline_API':old,'full_candidate_API':new,'explicit_retains':x['retains'],'source_reason':x['reason'],'incoming_disposition_pin':pin(ip),'incoming_guard_pin':pin(gp)})
ops.append(operation(1,'C0049-record-own-full-source-scope',[rows[0]['full_candidate_API']],pin(corepath)))
new=[x for x in core['new_objects'] if 'C0049' in x['object_id']];assert len(new)==2
for i,x in enumerate(new,2):
 assert [g for g in guards['new_object_absence_guards'] if g['object_id']==x['object_id']][0]['actual_existing_native_count']==0
 ops.append(operation(i,'C0049-'+('fullTR' if x['new_entire_API']['kind']=='transcription' else 'full-audit'),[copy.deepcopy(x['new_entire_API'])],pin(corepath)))
for i,x in enumerate(rows[1:],4):ops.append(operation(i,'C0049-'+('READ' if x['object_id'].startswith('READ-') else 'old-TR')+'-source-scope',[x['full_candidate_API']],pin(corepath)))
pathspec=B/'source-review/C0067-P0098-unread-other-year-source-route-clause-decision-v1.json';assert pin(pathspec)['sha256']=='f2595ea7f0ec16518f937c979f3b0712861e0583c1d809c0410ec0e416809520';s=load(pathspec);assert len(s['objects'])==1
gpath=B/'bounded-consequence-inputs-v1/C0049-small14-and-C0067-P0098-exact-current-field-overlap-allhistory-incoming-guards-v1.json';g=load(gpath);x=s['objects'][0];gr=[r for r in g['rows'] if r['object_id']==x['object_id']];assert len(gr)==1 and gr[0]['allhistory_incoming']==[] and gr[0]['existing_draft_target_overlap']==0
old,new=revise(x,gr[0]['complete_current']);rows.append({'object_id':x['object_id'],'source_edits':x['edits'],'full_baseline_API':old,'full_candidate_API':new,'source_reason':x['reason'],'incoming_guard_pin':pin(gpath),'incoming_zero':True})
ops.append(operation(6,'C0067-P0098-other-year-source-route',[new],pin(pathspec)))
result=save('six-exact-draft-operations-and-individual-consequence-preservation-table-v1.json',{'task':'T-0781','operation_pins':ops,'individual_revisions':rows,'new_objects_full_source_API':core['new_objects'][:2],'source_spec_pin':pin(corepath),'source_record_incoming_disposition_pin':pin(ip),'source_PATH98_spec_pin':pin(pathspec),'required_final_order':'R49 then C49 fullTR then audit/READ/oldTR; separate C67 TR must precede C67 support additions. All11 incoming consumer required new revisions must be included in final package, never skipped.','pending_other_C0049_consumer_modules':'Await exact individual source APIs; final global gate not ready','full_ordered_metadata_evidence_origins_assets_media_preserved':True,'stage':'UNRUN','canonical_apply':'UNRUN'})
print(json.dumps({'result_pin':result,'operations':ops},indent=2))
