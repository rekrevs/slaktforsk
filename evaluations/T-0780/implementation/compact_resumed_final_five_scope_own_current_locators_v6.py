"""Compact reviewer locators; primary spec assertions never renamed as own judgments."""
import json,hashlib,datetime
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/resumed-final-five-scope-own-current-field-join-v6'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(k):return str(k).replace('~','~0').replace('/','~1')
P=B/'implementation/resumed-final-five-scope-own-current-field-join-v6/five-scope-exact-own-current-field-reading-locators-v6.json';d=load(P)
ids={r['revision_id'] for rows in d['scopes'].values() for r in rows};ownrows={};receipts=[]
for p in sorted((B/'fresh-independent-review').glob('*.json')):
 if any(t in p.name for t in ['semantic-scan','expanded-military-scan','search-input','routing-for-own','exact-routing']):continue
 doc=load(p);pp=pin(p);receipts.append(pp)
 def walk(x,ptr):
  if isinstance(x,dict):
   oid=x.get('object_id',x.get('id',x.get('object',x.get('revision_id'))));version=x.get('expectedVersion',x.get('expected_version',x.get('version')))
   cur=x.get('full_current',x.get('current_full_object',x.get('current')))
   if isinstance(cur,dict):oid=cur.get('revision_id',cur.get('id',cur.get('object_id',oid)));version=cur.get('version',version)
   assertions={k:v for k,v in x.items() if k not in ['data','body','caveat','text','markdown','description','origins','evidence','rationale'] and (k in ['decision','reason','judgment','source_disposition','own_disposition','review','all_actual_fields_exact','disposition'] or any(t in k for t in ['whole_current_data_and_caveat_read','full_data_and_caveat_read','full_current_data_and_caveat_read','exact_full_current_data_caveat_reuse','full_native_read','full_current','whole_native_fields_read','full_api_equal','actual_full_api_equal','API_exact_equals','full_data_metadata_evidence_origins_read'])) and isinstance(v,(str,bool,int,type(None)))}
   # A native snapshot's recorded/accepted disposition is metadata, not a review assertion.
   if isinstance(x.get('data'),dict) and 'kind' in x:assertions={}
   if isinstance(oid,str) and assertions:
    if '@' in oid:rid=oid
    elif isinstance(version,int):rid=oid+'@'+str(version)
    else:rid=None
    matching=[rid] if rid in ids else [z for z in ids if z.rsplit('@',1)[0]==oid] if rid is None else []
    for target in matching:
     ownrows.setdefault(target,[]).append({'own_receipt_pin':pp,'own_individual_assertion_pointer':ptr,'native_ID_version_exact':rid==target,'version_unspecified_ID_only_requires_review':rid is None,'literal_assertions':{k:(v if not isinstance(v,str) or len(v)<=500 else {'bounded_excerpt':v[:500],'complete_value_pointer':ptr+'/'+esc(k)}) for k,v in assertions.items()}})
   for k,v in x.items():
    if isinstance(v,(dict,list)):walk(v,ptr+'/'+esc(k))
  elif isinstance(x,list):
   for i,v in enumerate(x):
    if isinstance(v,(dict,list)):walk(v,ptr+'/'+str(i))
 walk(doc,'')
scopes={}
for scope,rows in d['scopes'].items():
 out=[]
 for r in rows:
  matched=[]
  for z in r['own_reading_comparisons']:
   if not z['whole_data_and_caveat_exact_equal']:continue
   matched.append({'own_receipt_pin':z['own_receipt_pin'],'saved_snapshot_input_pin':z['snapshot_input_pin'],'saved_snapshot_pointer':z['snapshot_pointer'],'exact_data_and_caveat_equal':True,'other_field_equality_bools':z['all_present_native_field_equalities'],'missing_metadata_field_names':list(z['missing_native_fields_exact_values']),'differing_field_names':[x['field'] for x in z['all_remaining_field_differences']],'snapshot_parent_context_pointer':z['individual_assertion_pointer'],'snapshot_parent_is_primary_spec_context_only':z['snapshot_input_pin']['path'].startswith(str(B/'source-review')),'own_scope_source_pointer':'Original v1 row literal_own_reading_scope','actual_own_target_assertions':[x for x in ownrows.get(r['revision_id'],[]) if x['own_receipt_pin']==z['own_receipt_pin']], 'direct_exact_individual_reading_predicate':z.get('direct_exact_individual_reading_predicate',False),'direct_own_individual_reading_assertion':z['literal_individual_assertion'] if z.get('direct_exact_individual_reading_predicate') else None,'no_blanket_input_scope_or_metadata_readcredit':True})
  out.append({'revision_id':r['revision_id'],'exact_whole_data_caveat_matches':matched,'all_saved_own_actual_target_assertion_locators':ownrows.get(r['revision_id'],[]),'no_exact_saved_whole_data_caveat_match':not matched})
 scopes[scope]=out
assert W.exists();p=W/'compact-five-scope-exact-reading-snapshot-and-own-target-assertion-locators-v6.json';assert not p.exists();p.write_text(json.dumps({'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prior_complete_comparison_pin':pin(P),'rules':'Primary spec row assertions are context only; actual own pertarget assertions separately pinned. Explicit ID/version or unspecified-version flag; no routing ID readcredit. Scope confirmation remains independent. No full current bodies/wrapper metadata duplicated.','scopes':scopes,'new_own_receipts_pinned':receipts,'no_sourceapproval_or_new_readcredit_inferred':True},ensure_ascii=False,indent=2)+'\n');print(str(p),sha(p))
