import json,pathlib,hashlib,re,collections,time
start=time.time();base=pathlib.Path('evaluations/T-0780');out=base/'implementation/C0069-left417-snapshot-pointer-coverage-v1';out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,x):
 p=out/n;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
src=pathlib.Path('/tmp/t0780-c69-left417.json');frozen=out/'frozen-primary-left417-input.json';frozen.write_bytes(src.read_bytes());assert sha(src)==sha(frozen);objects=json.loads(frozen.read_text());assert len(objects)==417 and len({x['id'] for x in objects})==417
ids={x['id'] for x in objects};groups=collections.defaultdict(list)
for p in (base/'source-review').rglob('*.json'):
 m=re.match(r'(.*)-v(\d+)\.json$',p.name);key=(str(p.parent),m[1] if m else p.name);groups[key].append((int(m[2]) if m else 0,p))
latest=[];excluded=[]
for g in groups.values():
 v=max(x[0] for x in g)
 for n,p in g:
  (latest if n==v else excluded).append(p)
index=collections.defaultdict(list);conflicts=[];pins=[]
def esc(k):return str(k).replace('~','~0').replace('/','~1')
def walk(x,path,pin,decision):
 if isinstance(x,dict):
  if any(k in x for k in ['edits','Astra_disposition','decision','action']) or ('disposition' in x and 'current' in x):decision={'json_pointer':path,'metadata_pointer_only':{k:x[k] for k in ['disposition','Astra_disposition','Astra_rationale','decision','action','rationale'] if k in x}}
  if isinstance(x.get('data'),dict):
   identifiers={k:x[k] for k in ['id','revision_id'] if isinstance(x.get(k),str) and re.fullmatch(r'.+@[1-9][0-9]*',x[k])}
   if isinstance(x['data'].get('revision_id'),str):identifiers['data.revision_id']=x['data']['revision_id']
   vals=set(identifiers.values())
   if vals & ids:
    if len(vals)!=1 or (x.get('object_id') is not None and x['object_id']!=next(iter(vals)).rsplit('@',1)[0]):conflicts.append({'source_pin':pin,'json_pointer':path,'identifiers':identifiers,'payload':x,'reason':'conflicting exact identifiers; no match selected'})
    else:index[next(iter(vals))].append({'source_pin':pin,'json_pointer':path,'exact_identifier_fields':identifiers,'individual_decision_pointer':decision,'snapshot':x})
  for k,v in x.items():walk(v,path+'/'+esc(k),pin,decision)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+'/'+str(i),pin,decision)
for p in sorted(latest):
 pin={'path':str(p),'sha256':sha(p)};pins.append(pin);walk(json.loads(p.read_text()),'',pin,None)
# No projection: dictionaries are key maps; arrays remain complete ordered native fields.
def compare(native,snapshot,path=''):
 available=[];residual=[];extra=[]
 for k,v in native.items():
  q=path+'/'+esc(k)
  if k not in snapshot:residual.append({'path':q,'reason':'missing_source_native_field','full_native_value':v})
  elif isinstance(v,dict) and isinstance(snapshot[k],dict):
   a,r,e=compare(v,snapshot[k],q);available+=a;residual+=r;extra+=e
  else:
   equal=type(v)==type(snapshot[k]) and v==snapshot[k];available.append({'path':q,'exact_equal':equal,'native_value':v,'source_value':snapshot[k]})
   if not equal:residual.append({'path':q,'reason':'available_field_not_equal','full_native_value':v,'full_source_value':snapshot[k]})
 for k,v in snapshot.items():
  if k not in native:extra.append({'path':path+'/'+esc(k),'source_value':v,'not_inferred_as_native_metadata':True})
 return available,residual,extra
rows=[];zero=0;multi=0;equal=0
for obj in objects:
 candidates=index[obj['id']];zero+=not candidates;multi+=len(candidates)>1;comparisons=[]
 for c in candidates:
  a,r,e=compare(obj,c['snapshot']);whole=not r and not e;equal+=whole;comparisons.append({**c,'available_native_fields':a,'missing_or_unequal_full_native_residuals':r,'extra_source_fields':e,'strict_whole_native_equal':whole,'missing_id_not_filled_from_revision_id':True})
 rows.append({'revision_id':obj['id'],'full_native':obj,'exact_snapshot_pointer_count':len(candidates),'multiple_pointers_not_automatically_selected':len(candidates)>1,'comparisons':comparisons,'no_pointer_full_residual':obj if not candidates else None,'source_reading_disposition_or_relevance_not_inferred':True})
result=save('individual417-snapshots-available-field-comparisons-full-residuals-v1.json',{'rules':'Exact revision identifiers only; no inferred id/version/operation/origin fields, no projection, fallback, fuzzy matching or array normalization. Dictionary key serialization order ignored; all arrays ordered and duplicate-sensitive. Multiple snapshots all retained, no preferred pointer. Enclosing individual disposition is pointer metadata only, never reading credit or judgment.','rows':rows,'identifier_conflicts':conflicts})
# Freeze complete source bytes supplying matches/conflicts, not merely their current path hashes.
used={c['source_pin']['path'] for cs in index.values() for c in cs}|{c['source_pin']['path'] for c in conflicts};snapshotdir=out/'source-inputs';snapshotdir.mkdir();copies=[]
for i,p in enumerate(sorted(used)):
 original=pathlib.Path(p);copy=snapshotdir/(str(i).zfill(3)+'-'+original.name);copy.write_bytes(original.read_bytes());assert sha(original)==sha(copy);copies.append({'original':p,'frozen_path':str(copy),'sha256':sha(copy)})
sourceindex=save('complete-source-snapshot-input-index-v1.json',{'latest_filename_version_selection_not_source_approval':pins,'excluded_older_filename_paths':[str(p) for p in excluded],'frozen_matched_source_inputs':copies})
receipt=save('bounded-one-module-pointer-coverage-receipt-v1.json',{'input_pin':{'original':str(src),'frozen':str(frozen),'sha256':sha(frozen)},'result_pin':result,'source_index_pin':sourceindex,'objects':417,'objects_with_exact_snapshot_identifiers':417-zero,'zero_pointer_objects':zero,'multiple_pointer_objects':multi,'identifier_conflicts':len(conflicts),'strict_whole_equal_snapshot_comparisons':equal,'source_files_scanned':len(pins),'matched_source_files_frozen':len(copies),'elapsed_seconds':time.time()-start,'failed_attempts':[],'prior473_59_527_and_all_candidates_diagnostics_unchanged':True,'no_source_read_credit_metadata_inference_candidate_write_stage_apply_or_rebind':True,'model_usage_parent_collect_after_final':True})
print(json.dumps(receipt));print(json.dumps({'with_snapshot':417-zero,'zero':zero,'multiple':multi,'conflicts':len(conflicts),'strict':equal}))
