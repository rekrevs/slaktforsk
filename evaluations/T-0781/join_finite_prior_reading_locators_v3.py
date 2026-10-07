"""Finite exact saved reading/source locator join; never grants scope or reading credit."""
import json,hashlib,copy,sqlite3
from pathlib import Path
B=Path('evaluations/T-0781');OLD=Path('evaluations/T-0780');D=B/'mechanical-current425-preparation-v1';W=B/'finite-prior-reading-locator-join-v3'
def load(p):return json.loads(Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
cache={};pins={}
def checked(p):
 path=p['path']
 if path not in cache:
  assert pin(path)==p,p;cache[path]=load(path);pins[path]=p
 return cache[path]
def esc(s):return str(s).replace('~','~0').replace('/','~1')
def ptr(doc,p):
 for k in p.lstrip('/').split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');doc=doc[int(k)] if isinstance(doc,list) else doc[k]
 return doc
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+esc(k))
 elif isinstance(x,list):
  for i,v in enumerate(x):
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+str(i))
def identity(x):
 if not isinstance(x,dict):return None
 for key in ['revision_id','revision','id','object_id','object']:
  v=x.get(key)
  if isinstance(v,str):
   if '@' in v:return v
   ver=x.get('version',x.get('expectedVersion'))
   if isinstance(ver,int):return v+'@'+str(ver)
 for k in ['current','full_current','full_native','current_full_object']:
  if isinstance(x.get(k),dict):
   v=identity(x[k])
   if v:return v
 return None
def semantic(x):
 if not isinstance(x,dict) or not isinstance(x.get('data'),dict) or 'caveat' not in x:return None
 data={}
 for k,v in x['data'].items():
  if k=='revision_id':continue
  if k.endswith('_json') and isinstance(v,str):
   if 'revision_id' in x['data']:
    v=json.loads(v)  # Native SQL JSON text must be valid.
   else:
    try:v=json.loads(v)  # Legacy semantic snapshot can retain native JSON text.
    except json.JSONDecodeError:pass  # Already structured API string remains exact string.
  data[k]=v
 return {'data':data,'caveat':x['caveat']}
def diff(a,b):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):return [{'field':k,'prior':a.get(k),'actual':b.get(k)} for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)]
 return [{'prior':a,'actual':b}]
assert not W.exists();W.mkdir()
np=pin(D/'full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json');native=checked(np)
rp=pin(D/'finite-current-semantic-copy-field-routing-and-prior250-equality-v1.json');routing=checked(rp)
literal=[x['revision_id'] for x in routing['current_field_routes'] if any(any(t in ['C-0067','C0067'] for t in m['matched_literal_terms']) for m in x['matches'])];assert len(literal)==169
views=checked(pin(D/'full13-person-research-inspect-pre-source-release-input-index-v1.json'))
people=[x['person_id'] for x in views['persons']]
profile=[rid for oid,rid in native['current_object_revisions'].items() if oid in ['BIO-'+p for p in people] or (oid.startswith('RESEARCH-') and any(oid.startswith('RESEARCH-'+p+'-') for p in people))]
c=sqlite3.connect((D/'baseline-j425.sqlite').resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
seeds=['R-d9840df54c7f19f2454c4d2d@1','R-59279649d0a5ccf6537e098c@1'];direct=[]
for seed in seeds:
 direct.extend(x[0] for x in c.execute('select d.revision_id from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id=? and not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) order by d.rowid',(seed,)))
groups={'C0067-literal169':literal,'13-current-BIO-and-RESEARCH':profile,'C0049-C0067-direct-current-record-consumers':sorted(set(direct))};targets=set().union(*map(set,groups.values()));assert targets<=set(native['objects'])
ownpath=OLD/'fresh-independent-review/resumed-finite-own-reading-reuse-bindings-recomputed-v1.json';own=checked(pin(ownpath));ownrows={}
for scope,arr in own['scopes'].items():
 for i,x in enumerate(arr):
  rid=x['revision_id']
  if rid not in targets:continue
  actual=native['objects'][rid];snapshot=ptr(checked(x['snapshot_pin']),x['snapshot_pointer']);proof=semantic(snapshot)
  checked(x['own_receipt_pin'])
  ownrows.setdefault(rid,[]).append({'own_binding_index_pin':pin(ownpath),'own_binding_pointer':'/scopes/'+esc(scope)+'/'+str(i),'own_receipt_pin':x['own_receipt_pin'],'literal_own_reading_predicate':x['own_literal_reading_predicate'],'snapshot_input_pin':x['snapshot_pin'],'snapshot_input_pointer':x['snapshot_pointer'],'exact_ID_version':rid,'whole_data_and_caveat_equal_to_current425':proof==semantic(actual),'present_semantic_field_differences':diff(proof,semantic(actual)),'scope_or_metadata_credit_not_enlarged':True})
# Exact actual member scopes preserve individual review rows, full-operation reading assertions and scoped renewal chains.
memberpath=OLD/'implementation/resumed-current140-independent-receipt-join-v2/per-current140-operation-and-target-receipt-join-v1.json';members=checked(pin(memberpath));actualrows={}
for mi,m in enumerate(members['members']):
 mp=m['current_member'];matching=[(ti,x) for ti,x in enumerate(m['per_target']) if x['target_id']+'@'+str((x['native_expected_version'] or 0)+1) in targets]
 if not matching:continue
 op=checked({'path':mp['path'],'sha256':mp['sha256']})
 for ti,t in matching:
  rid=t['target_id']+'@'+str((t['native_expected_version'] or 0)+1);change=op['changes'][t['actual_change_index']];assert change['id']==t['target_id']
  actual=native['objects'][rid];expected={'data':change['data'],'caveat':change.get('caveat','')};present=semantic(actual)
  for key in present['data']:expected['data'].setdefault(key,None)
  same=expected==present
  actualrows.setdefault(rid,[]).append({'saved_individual_member_join_pin':pin(memberpath),'exact_member_target_pointer':'/members/'+str(mi)+'/per_target/'+str(ti),'actual_operation_pin':{'path':mp['path'],'sha256':mp['sha256']},'actual_API_pointer':'/changes/'+str(t['actual_change_index']),'actual_API_generated_revision_ID_exact':rid,'complete_current_data_and_caveat_equals_reviewed_actual_API':same,'semantic_differences':diff(expected,present),'own_individual_actual_review_row_pointers':t.get('actual_target_review_row_pointers',[]),'literal_whole_operation_reading_attestations':t.get('exact_operation_literal_reading_attestations',[]),'actual_prior_current_payload_renewal_chains':t.get('actual_prior_current_payload_renewal_chains',[]),'no_whole_input_pin_only_credit':True,'independent_must_confirm_each_literal_scope':True})
# Only the preserved individual primary source context dictionary; native disposition alone is not a source grade.
primarypath=OLD/'implementation/five-expanded-exactnative-pointer-join-v2/deduplicated-full-source-decision-contexts-v1.json';primary=checked(pin(primarypath));primaryrows={}
oids={rid.rsplit('@',1)[0] for rid in targets}
for contextkey,z in primary['contexts'].items():
 x=z['full_context']
 if not isinstance(x,dict):continue
 declares={k:x[k] for k in ['decision','Astra_disposition','source_disposition','primary_disposition','rationale','reason','scope','limitation','basis_retained'] if k in x}
 if not any(k in declares for k in ['decision','Astra_disposition','source_disposition','primary_disposition']):
  disp=x.get('disposition')
  if not isinstance(disp,str) or disp in ['recorded','accepted','rejected','pending']:continue
  declares['disposition']=disp
 rid=identity(x)
 if not rid or rid.rsplit('@',1)[0] not in oids:continue
 checked(z['source_pin']);snapshots=[]
 for sp,s in walk(x):
  srid=identity(s)
  if srid!=rid or semantic(s) is None:continue
  if rid in targets:snapshots.append({'snapshot_pointer':z['json_pointer']+sp,'exact_ID_version':rid,'whole_data_and_caveat_equal_to_current425':semantic(s)==semantic(native['objects'][rid]),'semantic_differences':diff(semantic(s),semantic(native['objects'][rid]))})
 primaryrows.setdefault(rid.rsplit('@',1)[0],[]).append({'individual_primary_context_index_pin':pin(primarypath),'individual_context_index_pointer':'/contexts/'+esc(contextkey),'primary_source_pin':z['source_pin'],'primary_individual_disposition_pointer':z['json_pointer'],'declared_revision_ID':rid,'same_revision_as_selected_current':rid in targets,'literal_primary_individual_disposition':declares,'exact_current_snapshot_equality_locators':snapshots,'no_unversioned_or_metadata_only_source_approval':True,'source_grade_in_new_scope_requires_primary_confirmation':True})
rows=[]
for rid in sorted(targets):
 rows.append({'revision_id':rid,'subject_id':native['objects'][rid]['data'].get('subject_id'),'groups':[k for k,v in groups.items() if rid in v],'full_current_native_pin':np,'full_current_native_pointer':'/objects/'+esc(rid),'own_same_revision_saved_reading_bindings':ownrows.get(rid,[]),'own_current_actual_API_review_bindings':actualrows.get(rid,[]),'primary_individual_prior_disposition_bindings':primaryrows.get(rid.rsplit('@',1)[0],[]),'no_exact_own_saved_reading_locator_in_these_finite_inputs':not ownrows.get(rid) and not actualrows.get(rid),'new_source_grade':None})
p=W/'finite169-plus13profiles-and-direct-consumer-exact-prior-reading-disposition-locators-v1.json';p.write_text(json.dumps({'task':'T-0781','groups':groups,'rows':rows,'rules':'Exact physical same revision/ordered semantic equality is mechanical only. Prior individual scope not enlarged. Missing locator is not unread; present pin alone is not reading credit. No semantic/source grades inferred.','counts':{'unique_current_revisions':len(rows),'literal_C0067':169,'13_BIO_RESEARCH':len(profile),'direct_current_record_consumers':len(set(direct)),'with_exact_same_revision_own_recomputed_locator':len(ownrows),'with_exact_current_actual_API_join':len(actualrows),'with_individual_primary_object_context':sum(bool(x['primary_individual_prior_disposition_bindings']) for x in rows)},'input_pins':list(pins.values())},ensure_ascii=False,indent=2)+'\n');c.close();print(json.dumps({'result_pin':pin(p),'counts':load(p)['counts']},indent=2))
