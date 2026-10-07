import json,pathlib,hashlib,copy,re,collections,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0069-remaining532-disposition-candidate-pointer-handoff-v1';w.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();load=lambda p:json.load(open(p))
def save(n,x):
 p=w/n;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
rp=b/'implementation/C0069-wide1059-reference-expansion-v1/bounded-one-module-reference-resolution-final-receipt-v2.json';sp=b/'implementation/C0069-wide1059-expanded-source-match-v2/individual-wide1059-exact-source-match-and-differences-v1.json';pp=b/'implementation/C0069-wide1059-expanded-projection-match-v2/individual459-persisted-projection-and-all-remaining-differences-v2.json';mp=b/'implementation/C0425-ADOPT0099-glyph-amendment-v2/current123-candidate-membership-inventory-v1.json';assert sha(mp)=='315bd2e67310c2206182567b8fb0d48854d0a88822a9608842c8788868d41c34';r=load(rp);strict={x['revision_id']:x for x in load(sp)['rows']};project={x['revision_id']:x for x in load(pp)['objects']};ordered=set(r['ordered_union_revision_ids']);orderonly=set(r['evidence_order_only_revision_ids']);ids=ordered|orderonly;assert len(ordered)==473 and len(orderonly)==59 and len(ids)==532
membership=load(mp);targets=collections.defaultdict(list)
for pin in membership['candidate_members']:
 assert sha(pin['path'])==pin['sha256']
 for x in load(pin['path'])['changes']:targets[x['id']].append({'operation_pin':pin,'full_candidate':x})
cache={};used={}
def document(p,h=None):
 p=pathlib.Path(p)
 if str(p) not in cache:cache[str(p)]=load(p);used[str(p)]=sha(p)
 if h:assert used[str(p)]==h
 return cache[str(p)]
def parts(ptr):return [x.replace('~1','/').replace('~0','~') for x in ptr.split('/')[1:]]
def at(d,ps):
 for k in ps:d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def fieldpaths(x,p=''):
 if isinstance(x,dict):return [q for k,v in x.items() for q in fieldpaths(v,p+'/'+str(k).replace('~','~0').replace('/','~1'))] if x else [p]
 if isinstance(x,list):return [q for i,v in enumerate(x) for q in fieldpaths(v,p+'/'+str(i))] if x else [p]
 return [p]
def context(pointer):
 d=document(pointer['source_path'],pointer['source_sha256']);ps=parts(pointer['json_pointer']);snapshot=at(d,ps);parent=at(d,ps[:-1]) if ps else d
 # Parent is preserved even when it is stronger_full_support with no disposition; never infer retain/read absence.
 dp=None
 for n in range(len(ps)-1,-1,-1):
  o=at(d,ps[:n])
  if isinstance(o,dict) and any(k in o for k in ['disposition','decision','Astra_disposition','action','edits']):dp={'json_pointer':'/'+('/'.join(ps[:n])) if n else '', 'whole_context':o,'explicit_decision_keys':{k:o[k] for k in ['disposition','decision','Astra_disposition','action','edits','rationale','Astra_rationale'] if k in o}};break
 return {'reading_snapshot_pointer':pointer,'full_snapshot':snapshot,'snapshot_field_jsonpaths':fieldpaths(snapshot),'immediate_enclosing_context_pointer':'/'+('/'.join(ps[:-1])) if ps[:-1] else '', 'whole_immediate_enclosing_context':parent,'individual_decision_pointer_and_whole_context':dp,'no_read_credit_or_disposition_inferred':True}
# Latest source snapshots selected by explicit filename version metadata only.
groups=collections.defaultdict(list)
for p in (b/'source-review').rglob('*.json'):
 m=re.match(r'(.*)-v(\d+)\.json$',p.name);groups[(str(p.parent),m[1] if m else p.name)].append((int(m[2]) if m else 0,p))
latest=[]
for g in groups.values():latest.extend(p for n,p in g if n==max(v for v,q in g))
latestindex=collections.defaultdict(list)
def walk(x,path,pin):
 if isinstance(x,dict):
  identifier=x.get('id') or x.get('revision_id') or (x.get('data',{}).get('revision_id') if isinstance(x.get('data'),dict) else None)
  if identifier in ids and isinstance(x.get('data'),dict):latestindex[identifier].append({'source_path':pin['path'],'source_sha256':pin['sha256'],'json_pointer':path})
  for k,v in x.items():walk(v,path+'/'+str(k).replace('~','~0').replace('/','~1'),pin)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+'/'+str(i),pin)
for p in sorted(latest):
 d=load(p);walk(d,'',{'path':str(p),'sha256':sha(p)})
rows=[]
for rid in sorted(ids):
 pointers=[{'match_kind':'strict_ordered','pointer':p} for p in strict[rid]['exact_full_native_equal_source_pointers']]
 if rid in project:
  pointers += [{'match_kind':p['classification'],'pointer':p['source_pointer'],'full_prior_comparison':p} for p in project[rid]['per_pointer_comparisons'] if p['persisted_projection_ordered_full_equal'] or p['evidence_order_only_difference_after_projection']]
 old=[{'match_kind':p['match_kind'],'full_prior_comparison':p.get('full_prior_comparison'),'context':context(p['pointer'])} for p in pointers];new=[context(p) for p in latestindex[rid]];oid=rid.rsplit('@',1)[0];candidates=targets.get(oid,[])
 rows.append({'revision_id':rid,'frozen_category':'ordered473' if rid in ordered else 'evidence_order_only59_NOT_ordered_equal','prior_pointer_contexts':old,'latest_exact_revision_source_snapshot_contexts':new,'latest_actual_candidates':candidates,'candidate_target_overlap_count':len(candidates),'prior_or_latest_no_individual_decision_context_pointers':[x['context']['reading_snapshot_pointer'] for x in old if x['context']['individual_decision_pointer_and_whole_context'] is None],'actual_explicit_decision_fields_without_adjudication':[x['individual_decision_pointer_and_whole_context']['explicit_decision_keys'] for x in new if x['individual_decision_pointer_and_whole_context']],'multiple_or_conflicting_decision_contexts_not_selected':len(new)>1,'evidence_array_order_never_normalized':True,'no_implicit_retain_grade_source_judgment':True})
result=save('individual532-full-prior-latest-disposition-and-actual-candidate-handoff-v1.json',{'objects':rows,'rules':'Frozen473 ordered union and59 evidence-order-only classifications preserved. Full snapshot reading pointer distinct from enclosing actual explicit decision pointer/context. No decision/retain inferred from current equality. Latest filename-version source metadata not approval. Whole contexts and ordered payloads untruncated. Multiple context decisions reproduced, no source adjudication.'})
frozen=w/'frozen-pointer-inputs';frozen.mkdir();pins=[]
for i,(p,h) in enumerate(sorted(used.items())):
 cp=frozen/(str(i).zfill(3)+'-'+pathlib.Path(p).name);cp.write_bytes(pathlib.Path(p).read_bytes());assert sha(cp)==h;pins.append({'path':p,'sha256':h,'frozen_path':str(cp)})
idx=save('frozen-full-pointer-inputs-and-membership-index-v1.json',{'prior_input_pins':[{'path':str(p),'sha256':sha(p)} for p in [rp,sp,pp,mp]],'whole_membership':membership,'full_source_pointer_input_copies':pins,'latest_source_file_pins':[{'path':str(p),'sha256':sha(p)} for p in latest]})
receipt=save('bounded-one-module532-production-receipt-v1.json',{'result_pin':result,'input_index_pin':idx,'ordered_objects':473,'order_only_objects':59,'objects':532,'objects_with_actual_candidate':sum(bool(x['latest_actual_candidates']) for x in rows),'prior_pointers_without_individual_decision_context':sum(len(x['prior_or_latest_no_individual_decision_context_pointers']) for x in rows),'full_source_inputs_frozen':len(pins),'failed_attempts':[],'elapsed_seconds':time.time()-start,'no_grade_retain_read_credit_rebind_or_stage_apply':True,'all_previous473_59_527_and_candidates_unchanged':True});print(json.dumps(receipt))
