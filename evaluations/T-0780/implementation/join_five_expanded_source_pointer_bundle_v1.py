import pathlib,json,hashlib,sqlite3,collections,copy,re,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/five-expanded-exactnative-pointer-join-v1';w.mkdir(exist_ok=False);load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def save(n,x):
 p=w/n;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
fi=w/'frozen-inputs';fi.mkdir();frozen={}
def freeze(p):
 p=pathlib.Path(p);key=str(p)
 if key not in frozen:
  cp=fi/(str(len(frozen)).zfill(4)+'-'+p.name);cp.write_bytes(p.read_bytes());assert sha(cp)==sha(p);frozen[key]={'path':key,'sha256':sha(p),'frozen_path':str(cp)}
 return frozen[key]
scopes={};scopepins={};allids=set()
for cid,method in [('0044','all_lexical'),('0563','outside_direct_selected'),('0561','outside_direct_selected'),('0106','outside_direct_selected'),('0425','outside_direct_selected')]:
 lp=b/f'preparation/selected/C-{cid}-semantic-consequence-input-v1.json';dp=b/f'preparation/selected/C-{cid}-source-relevant-current-context-v1.json';lpins=freeze(lp);dpins=freeze(dp);lex=load(lp)['candidates'];direct=load(dp)['objects'];directids={x['revision_id'] for x in direct};scope=[{'original_lexical_index':i,'whole_routing_tuple':x} for i,x in enumerate(lex) if method=='all_lexical' or x['revision_id'] not in directids];assert len({x['whole_routing_tuple']['revision_id'] for x in scope})==len(scope);scopes[cid]=scope;scopepins[cid]=save('C-'+cid+'-exact-ordered-scope-tuples-v1.json',{'method':method,'lexical_pin':lpins,'direct_context_pin':dpins,'lexical_count':len(lex),'direct_context_count':len(direct),'scope_count':len(scope),'ordered_scope':scope,'dedup_aliases':[{'revision_id':rid,'lexical_indices':[i for i,x in enumerate(lex) if x['revision_id']==rid]} for rid in {x['revision_id'] for x in lex} if sum(x['revision_id']==rid for x in lex)>1]});allids.update(x['whole_routing_tuple']['revision_id'] for x in scope)
mp=b/'implementation/C0425-THEME99BO-body-amendment-v3/current123-candidate-membership-inventory-v1.json';assert sha(mp)=='7206aeccc003657304ab8f9fbd2ffc5a29753862bd0c842fa4cc675d2d126334';freeze(mp);membership=load(mp);actual=collections.defaultdict(list)
for pin in membership['candidate_members']:
 assert sha(pin['path'])==pin['sha256']
 for x in load(pin['path'])['changes']:
  if x['id']+'@'+str(x['expectedVersion']) in allids:actual[x['id']].append({'operation_pin':pin,'full_latest_actual_payload':x})
# Frozen canonical baseline provides full residual fields; no source judgment or reading inferred.
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;native={}
for rid in sorted(allids):
 row=c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone();assert row is not None,(rid,'missing frozen baseline');o=dict(row);o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(x) for x in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=?',(rid,))]
 if o['kind']=='record':o['assets']=[dict(x) for x in c.execute('select * from record_asset where revision_id=?',(rid,))];o['media']=[dict(x) for x in c.execute('select * from record_media where revision_id=?',(rid,))]
 native[rid]=o
nativepin=save('full-frozen-native-residual-dictionary-v1.json',{'objects':native,'dependency_SQL_row_presentation_order_not_evidence_order_approval':True,'all_embedded_arrays_and_origin_media_arrays_preserved':True})
index=collections.defaultdict(list);contexts={};conflicts=[]
def ptrparts(p):return [x.replace('~1','/').replace('~0','~') for x in p.split('/')[1:]]
def get(x,p):
 for k in ptrparts(p):x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def addcontext(pin,path,x):
 key=pin['path']+'#'+path
 if key not in contexts:contexts[key]={'source_pin':pin,'json_pointer':path,'full_context':x}
 return key
def walk(x,path,pin,decision=None):
 if isinstance(x,dict):
  # A native revision disposition is not a source consequence decision.
  if any(k in x for k in ['edits','decision','action','Astra_disposition','primary_decision','primary_disposition']) or ('disposition' in x and 'data' not in x):decision=addcontext(pin,path,x)
  if isinstance(x.get('data'),dict):
   identifiers=[x[k] for k in ['id','revision_id'] if isinstance(x.get(k),str) and re.fullmatch('.+@[1-9][0-9]*',x[k])]
   if isinstance(x['data'].get('revision_id'),str):identifiers.append(x['data']['revision_id'])
   vals=set(identifiers)
   if vals & allids:
    if len(vals)!=1:conflicts.append({'pin':pin,'pointer':path,'full_payload':x,'identifiers':identifiers})
    else:index[next(iter(vals))].append({'reading_pointer':{'source_pin':pin,'json_pointer':path},'full_snapshot':x,'individual_decision_context_key':decision})
  for k,v in x.items():walk(v,path+'/'+str(k).replace('~','~0').replace('/','~1'),pin,decision)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+'/'+str(i),pin,decision)
groups=collections.defaultdict(list)
for p in (b/'source-review').rglob('*.json'):
 m=re.match(r'(.*)-v(\d+)\.json$',p.name);groups[(str(p.parent),m[1] if m else p.name)].append((int(m[2]) if m else 0,p))
latest=[p for g in groups.values() for n,p in g if n==max(v for v,q in g)];sourcepins=[]
for p in sorted(latest):
 pin={'path':str(p),'sha256':sha(p)};sourcepins.append(pin);before=sum(map(len,index.values()));walk(load(p),'',pin)
 if sum(map(len,index.values()))!=before:freeze(p)
# Explicit C69 individual reading/decision reuse indexes, kept distinct from native equality.
reuse=collections.defaultdict(list)
for name,expected in [('C-0069-expanded527-individual-source-disposition-index-v2.json','9bf4c66551b61d30dc5d7c40b657ed3b0582baf8cb63d08103a14bf5501237cb'),('C-0069-remaining532-individual-reading-and-decision-reuse-v1.json','637caf701e6ab7b8cd874a80e0b5336088c61c0aaa1d517fe65ab4d9f35f5d7b')]:
 p=b/'source-review'/name;assert sha(p)==expected;pin=freeze(p);d=load(p)
 for i,o in enumerate(d['objects']):
  rid=o.get('revision_id') or (o['object_id']+'@'+str(o['version']) if 'object_id' in o and 'version' in o else None)
  if rid not in allids:continue
  ctx={'index_pin':pin,'json_pointer':'/objects/'+str(i),'whole_individual_disposition_index_entry':o,'reading_and_decision_pointers_not_interchangeable':True};reuse[rid].append(ctx)
  for k in ['primary_decision','individual_decision_pointer','reading_snapshot_pointer']:
   q=o.get(k)
   if isinstance(q,dict):
    path=q.get('path') or q.get('source_path');h=q.get('sha256') or q.get('source_sha256');pointer=q.get('pointer') or q.get('json_pointer')
    if path and h and pointer is not None:
     assert sha(path)==h;fp=freeze(path);ctx[k+'_full_named_context']=addcontext(fp,pointer,get(load(path),pointer))
originextras={'document_path','start_line','end_line','raw'}
def project(x,other):
 z=copy.deepcopy(x);removed=[]
 if 'current' in z:removed.append('/current');z.pop('current')
 for i,o in enumerate(z.get('origins',[])):
  for k in originextras:
   if k in o:removed.append('/origins/'+str(i)+'/'+k);o.pop(k)
 for i,o in enumerate(z.get('assets',[])):
  if i>=len(other.get('assets',[])):continue
  for k in ['sha256','bytes']:
   if k in o and k not in other['assets'][i]:removed.append('/assets/'+str(i)+'/'+k);o.pop(k)
 return z,removed
def diff(a,z,p=''):
 if type(a)!=type(z):return [{'json_path':p,'native_full_value':a,'source_full_value':z,'difference':'type'}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(z)):
   q=p+'/'+str(k)
   if k not in a:out.append({'json_path':q,'difference':'extra_source_field','source_full_value':z[k]})
   elif k not in z:out.append({'json_path':q,'difference':'missing_source_native_field','native_full_value':a[k]})
   else:out+=diff(a[k],z[k],q)
  return out
 if isinstance(a,list):return [] if a==z else [{'json_path':p,'difference':'ordered_array','native_full_value':a,'source_full_value':z}]
 return [] if a==z else [{'json_path':p,'difference':'value','native_full_value':a,'source_full_value':z}]
comparisons={}
for rid,obj in native.items():
 records=[]
 for p in index[rid]:
  source=p['full_snapshot'];projected,removed=project(source,obj);pn,rn=project(obj,source);equal=pn==projected;edgeequal=collections.Counter(map(canon,pn.get('evidence',[])))==collections.Counter(map(canon,projected.get('evidence',[])));an=copy.deepcopy(pn);an.pop('evidence',None);az=copy.deepcopy(projected);az.pop('evidence',None);edgeonly=not equal and edgeequal and an==az
  records.append({**p,'strict_full_native_equal':obj==source,'explicit_projected_ordered_native_equal':equal,'edge_multiset_only_NOT_ordered_equal':edgeonly,'removed_source_enrichment_fields':removed,'removed_native_enrichment_fields':rn,'all_remaining_full_residuals':diff(pn,projected),'available_top_native_field_equalities':{k:(type(obj[k])==type(source[k]) and obj[k]==source[k]) for k in obj if k in source}})
 comparisons[rid]=records
counts={};outputpins=[]
for cid,scope in scopes.items():
 rows=[]
 for t in scope:
  rid=t['whole_routing_tuple']['revision_id'];p=comparisons[rid];rows.append({'ordered_routing_tuple':t,'full_native_dictionary_key':rid,'source_snapshot_field_comparisons':p,'exact_C69_individual_reuse_bindings':reuse[rid],'latest_actual_candidates':actual[native[rid]['object_id']],'no_pointer_full_residual_object':native[rid] if not p else None,'source_decision_unset_or_pending_fields_copied_only':True,'no_grade_unreadness_retain_or_wholeapproval_inferred':True})
 ct={'scope_objects':len(rows),'objects_with_ordered_native_pointer':sum(any(x['explicit_projected_ordered_native_equal'] for x in row['source_snapshot_field_comparisons']) for row in rows),'objects_only_evidence_order_match':sum(not any(x['explicit_projected_ordered_native_equal'] for x in row['source_snapshot_field_comparisons']) and any(x['edge_multiset_only_NOT_ordered_equal'] for x in row['source_snapshot_field_comparisons']) for row in rows),'objects_without_snapshot_pointer':sum(not row['source_snapshot_field_comparisons'] for row in rows),'objects_with_explicit_C69_reuse':sum(bool(row['exact_C69_individual_reuse_bindings']) for row in rows)};counts[cid]=ct;outputpins.append(save('C-'+cid+'-full-individual-pointer-join-residuals-v1.json',{'scope_pin':scopepins[cid],'counts':ct,'objects':rows}))
contexts_pin=save('deduplicated-full-source-decision-contexts-v1.json',{'contexts':contexts,'identifier_conflicts':conflicts});idx=save('complete-input-index-and-rules-v1.json',{'frozen_inputs':list(frozen.values()),'latest_source_file_pins':sourcepins,'scope_pins':scopepins,'full_native_pin':nativepin,'mandatory_current_membership_pin':{'path':str(mp),'sha256':sha(mp)},'projection_rules':['ignore only current CLI flag','ignore only origins enrichment document_path/start_line/end_line/raw','ignore only asset sha256/bytes when native attachment lacks them','all native origins/media/data embedded arrays remain ordered','evidence edge multiset separate, never ordered equality'],'scope_freeze_method':'C0044 all ordered lexical265; others exact lexical ordered set difference from locked source-relevant current context IDs; no counts assumed.'});receipt=save('bounded-five-source-one-bundle-production-receipt-v1.json',{'counts':counts,'unique_native_objects':len(native),'scope_aliases_total_occurrences':sum(len(v) for v in scopes.values()),'cross_scope_same_revision_aliases':[{'revision_id':rid,'scopes':[cid for cid,s in scopes.items() if any(x['whole_routing_tuple']['revision_id']==rid for x in s)]} for rid in allids if sum(any(x['whole_routing_tuple']['revision_id']==rid for x in s) for s in scopes.values())>1],'output_pins':outputpins,'context_pin':contexts_pin,'input_index_pin':idx,'identifier_conflicts':len(conflicts),'failed_attempts':[],'elapsed_seconds':time.time()-start,'no_source_judgment_candidate_rebind_stage_apply_or_source11':True,'all_prior_artifacts_unchanged':True});print(json.dumps(receipt));print(json.dumps(counts))
