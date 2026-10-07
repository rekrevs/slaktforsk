"""Mechanical exact settled-spec to latest API binding; historical differences are explicit, no grades."""
import json,copy,hashlib,datetime,re
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/resumed-current140-settled-spec-API-binding-index-v2'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(s):return str(s).replace('~','~0').replace('/','~1')
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
P=B/'implementation/resumed-P0431-PER-source-route-qualification-queue-v1/concrete-current140-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='70f1a4704ee5427250e1a640c7b956a287908ccf44cfc55accb3de772a302994'
actual={}
for member in load(P)['sequence']:
 assert sha(member['path'])==member['sha256']
 for i,ch in enumerate(load(member['path'])['changes']):
  assert ch['id'] not in actual;actual[ch['id']]={'member_pin':member,'API_pointer':'/changes/'+str(i),'whole_API':ch}
sources=set()
for c in (B/'implementation').glob('resumed-*-build-config-v*.json'):
 d=load(c);assert sha(d['source_path'])==d['source_sha256'];sources.add(d['source_path'])
for name in ['resumed-eleven-reviewer-clause-decisions-v1.json','resumed-two-marriage-path-residual-amendment-v1.json','resumed-two-copy-decisions-v1.json','resumed-P0480-path-dependency-amendment-v1.json','resumed-C0561-two-registration-wording-amendment-v1.json','resumed-three-completed-primary-audit-metadata-amendments-v1.json','resumed-four-completed-transcription-metadata-amendments-v1.json','resumed-five-completed-full-source-audit-specifications-v2.json','resumed-five-completed-full-source-audit-specifications-v3.json','resumed-F437-candidate-envelope-format-amendment-v1.json']:
 sources.add(str(B/'source-review'/name))
sourcehashes={sha(p):str(p) for p in (B/'source-review').glob('resumed-*.json')}
for member in load(P)['sequence']:
 for h in re.findall(r'[0-9a-f]{64}',load(member['path']).get('reason','')):
  if h in sourcehashes:sources.add(sourcehashes[h])
retainformat=B/'source-review/resumed-F437-candidate-envelope-format-amendment-v1.json';retainoriginal=Path(load(retainformat)['amends']['path']);assert sha(retainoriginal)==load(retainformat)['amends']['sha256'];exactretains=load(retainformat)['entries'];assert len(exactretains)==16
def api(n):
 data={k:json.loads(v) if k.endswith('_json') and isinstance(v,str) else v for k,v in n['data'].items() if k!='revision_id'}
 return {'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':data,'origins':[{'unit':o['unit_id'],'coverage':o['coverage'],'note':o['note']} for o in n['origins']],'evidence':[{'object':e['basis_revision_id'].rsplit('@',1)[0],'version':int(e['basis_revision_id'].rsplit('@',1)[1]),'role':e['role'],'note':e['note']} for e in n['evidence']],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
def diff(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):return sum((diff(a.get(k),b.get(k),p+'/'+esc(k)) for k in sorted(set(a)|set(b))),[])
 return [] if a==b else [{'pointer':p,'exact_spec_value':a,'exact_latest_value':b,'ordered_array_difference':isinstance(a,list) or isinstance(b,list)}]
rows=[];skipped=[]
for source in sorted(sources):
 d=load(source);objects=d.get('objects',[])
 if not objects and all(k in d for k in ['object_id','field','old','new']):objects=[d]
 for i,item in enumerate(objects):
  expected=item.get('new_entire_API');basis=item.get('prior_candidate');cur=item.get('current',item.get('full_current'));edits=item.get('edits',[]) or ([{k:item[k] for k in ['field','old','new']}] if all(k in item for k in ['field','old','new']) else [])
  oid=item.get('object_id',cur.get('object_id') if isinstance(cur,dict) else None)
  if expected is not None:expected=copy.deepcopy(expected);oid=expected['id']
  elif isinstance(basis,dict) and all(k in basis for k in ['id','expectedVersion','data']):expected=copy.deepcopy(basis)
  elif isinstance(cur,dict) and all(k in cur for k in ['id','object_id','version','kind','data','origins','evidence']):expected=api(cur)
  elif isinstance(item.get('candidate_payload'),dict):expected=copy.deepcopy(item['candidate_payload']);oid=expected['id']
  if not isinstance(oid,str) or oid not in actual:
   skipped.append({'source_pin':pin(source),'source_object_pointer':'/objects/'+str(i),'object_id':oid,'reason':'No latest candidate target or no supported exact API identity'});continue
  fieldchecks=[];address_issue=[]
  for e in edits:
   f=e['field'];field=f.removeprefix('data.');root=expected.get('data') if f.startswith('data.') and isinstance(expected,dict) else expected
   value=e['new'];old=e['old']
   if field.endswith('_json'):
    if isinstance(value,str):value=json.loads(value)
    if isinstance(old,str):old=json.loads(old)
   if isinstance(root,dict) and field in root:
    if root[field]!=old:address_issue.append({'field':f,'reason':'Historical spec old value does not equal chosen full API basis','exact_basis_value':root[field],'exact_spec_old':old})
    root[field]=value
   elif expected is not None:address_issue.append({'field':f,'reason':'Source field address absent in API shape; historical attempt retained'})
   live=actual[oid]['whole_API']['data'] if f.startswith('data.') else actual[oid]['whole_API']
   fieldchecks.append({'field':f,'new_value_pointer':'/objects/'+str(i)+'/edits','exact_spec_new':value,'latest_actual_value':live.get(field),'exact_latest_field_equal':live.get(field)==value})
  additions=item.get('evidence_additions',[]) or ([item['evidence_addition']] if item.get('evidence_addition') else [])
  if isinstance(expected,dict) and not item.get('new_entire_API'):
   for e in additions:
    if 'basis_revision_id' in e:
     ob,v=e['basis_revision_id'].rsplit('@',1);e={'object':ob,'version':int(v),'role':e['role'],'note':e['note']}
    expected['evidence'].append(copy.deepcopy(e))
  x=actual[oid]
  rows.append({'source_pin':pin(source),'source_object_pointer':'/objects/'+str(i) if d.get('objects') else '', 'object_id':oid,'whole_expected_source_API':expected,'latest_actual_member_pin':x['member_pin'],'latest_actual_API_pointer':x['API_pointer'],'latest_whole_API_payload_sha256':hashlib.sha256(canon(x['whole_API']).encode()).hexdigest(),'exact_whole_source_API_equals_latest':expected==x['whole_API'] if expected is not None else None,'all_exact_spec_latest_API_differences':diff(expected,x['whole_API']) if expected is not None else [],'explicit_field_checks':fieldchecks,'historical_source_API_basis_or_address_issues':address_issue,'whole_API_basis_not_available_in_spec':expected is None,'no_sourcegrade_or_scope_credit_inferred':True})
assert not W.exists();W.mkdir();p=W/'per-resumed-spec-exact-latest-whole-API-and-field-bindings-v1.json';p.write_text(json.dumps({'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_proposal_pin':pin(P),'source_specification_pins':[pin(x) for x in sorted(sources)],'rows':rows,'skipped_explicit':skipped,'F437_exact16_retain_format_source_pin':pin(retainformat),'F437_original_source_decision_pin':pin(retainoriginal),'F437_exact16_retained_entries_no_automatic_rebind_or_new_revision':exactretains,'rules':'Exact mechanical equality only. Initial and superseded specs remain historical; every remaining value/address difference explicit. Latest governing source decisions and all grades remain Astra. Native JSONtext fields explicitly parsed to API structured values, arrays unchanged.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result_pin':pin(p),'specifications':len(sources),'rows':len(rows),'whole_API_equal_latest':sum(r['exact_whole_source_API_equals_latest'] is True for r in rows),'historical_or_field_only':sum(r['exact_whole_source_API_equals_latest'] is not True for r in rows),'skipped':len(skipped)},indent=2))
