import json,pathlib,hashlib,re,time,collections
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0069-wide1059-source-input-match-v1';w.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();widep=b/'source-review/consequences-two/C-0069-complete-native-routing-dedup-v1.jsonl';lexp=b/'preparation/selected/C-0069-semantic-consequence-input-v1.json';wide=[json.loads(s) for s in widep.open()];lex=json.load(open(lexp));assert len(wide)==1059 and len(lex['candidates'])==669;assert len({x['id'] for x in wide})==1059
required={'id','object_id','version','operation_id','disposition','evidence_status','rationale','caveat','previous_id','kind','data','evidence','origins'};groups=collections.defaultdict(list)
for p in (b/'source-review').rglob('*.json'):
 if not any(t in p.name for t in ['decision','disposition','handoff','retain']):continue
 m=re.match(r'(.*)-v(\d+)\.json$',p.name)
 if m:groups[(str(p.parent),m[1])].append((int(m[2]),p))
latest=[];excluded=[]
for items in groups.values():
 v=max(i[0] for i in items)
 latest.extend(p for n,p in items if n==v);excluded.extend({'path':str(p),'sha256':sha(p),'filename_version':n} for n,p in items if n<v)
index=collections.defaultdict(list);pins=[];opaque=[]
def walk(x,path,parent,pin):
 if isinstance(x,dict):
  if required<=set(x) and isinstance(x['data'],dict):
   ctx={k:parent[k] for k in ['disposition','rationale','Astra_disposition','Astra_rationale','action','decision'] if isinstance(parent,dict) and k in parent}
   index[x['id']].append({'payload':x,'pointer':{'source_path':pin['path'],'source_sha256':pin['sha256'],'json_pointer':path,'disposition_pointer_only':ctx}});return
  for k,v in x.items():walk(v,path+'/'+str(k).replace('~','~0').replace('/','~1'),x,pin)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+'/'+str(i),parent,pin)
for p in sorted(latest):
 pin={'path':str(p),'sha256':sha(p)};d=json.load(open(p));before=sum(len(v) for v in index.values());walk(d,'',{},pin);count=sum(len(v) for v in index.values())-before;pin['full_native_payload_pointers']=count;pins.append(pin)
 if not count:opaque.append(pin)
def differences(a,z,path=''):
 if type(a)!=type(z):return [{'path':path,'difference':'type','wide_type':type(a).__name__,'spec_type':type(z).__name__}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(z)):
   p=path+'/'+k
   if k not in a:out.append({'path':p,'difference':'source_extra_key'})
   elif k not in z:out.append({'path':p,'difference':'source_missing_key'})
   else:out.extend(differences(a[k],z[k],p))
  return out
 if isinstance(a,list):
  out=[]
  if len(a)!=len(z):out.append({'path':path,'difference':'array_length','wide_length':len(a),'spec_length':len(z)})
  for i,(x,y) in enumerate(zip(a,z)):out.extend(differences(x,y,path+'/'+str(i)))
  return out
 return [] if a==z else [{'path':path,'difference':'value','wide':a,'source':z}]
rows=[];unmatched=[];nonmatches=[];exact=0;multiple=0;lexids={x['revision_id'] for x in lex['candidates']};wideids={x['id'] for x in wide}
for obj in wide:
 candidates=index.get(obj['id'],[]);matches=[];diffs=[]
 for cand in candidates:
  if obj==cand['payload']:matches.append(cand['pointer'])
  else:diffs.append({'pointer':cand['pointer'],'differences':differences(obj,cand['payload'])})
 if matches:exact+=1;multiple+=len(matches)>1
 else:unmatched.append(obj)
 row={'revision_id':obj['id'],'object_id':obj['object_id'],'kind':obj['kind'],'wide_payload_sha256':hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'lexical669_candidate':obj['id'] in lexids,'exact_full_native_equal_source_pointers':matches,'same_revision_non_equal_source_pointers':diffs,'needs_primary_input_reading':not bool(matches),'source_disposition_not_adjudicated':True};rows.append(row)
 if diffs:nonmatches.append(row)
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
mp=save('individual-wide1059-exact-source-match-and-differences-v1.json',{'matching_criteria':'Whole JSON dictionaries equal ignoring object-key serialization order only. Every header,data,value,type,metadata,evidence/origin array order and duplicates must match. Extra or missing keys are non-equal; no projection/SQL-row sorting/enriched-origin normalization. Disposition is copied only as source JSON-pointer metadata, never adjudicated. Filename-max-version selects current mechanical candidates; it is not source approval or reading certification.','rows':rows});up=w/'unmatched-full-native-inputs-v1.jsonl';assert not up.exists();up.write_text(''.join(json.dumps(o,ensure_ascii=False,separators=(',',':'))+'\n' for o in unmatched));lp=save('lexical669-to-wide1059-routing-index-v1.json',{'rows':[{'revision_id':x['revision_id'],'wide1059_present':x['revision_id'] in wideids,'lexical_partial_input_pointer':'/candidates/'+str(i),'lexical_disposition_pointer_only':{'Astra_disposition':x.get('Astra_disposition'),'Astra_rationale':x.get('Astra_rationale')},'partial_lexical_fields_not_full_native_match_or_source_reading':True} for i,x in enumerate(lex['candidates'])],'lexical_outside_wide':[x for x in lex['candidates'] if x['revision_id'] not in wideids]});sp=save('latest-source-spec-full-native-pointer-index-v1.json',{'selected_source_files':pins,'excluded_lower_filename_versions':excluded,'opaque_no_fullnative_payload_files':opaque,'not_a_source_approval_manifest':True});receipt=save('bounded-wide1059-match-input-output-receipt-v1.json',{'input_pins':[{'path':str(p),'sha256':sha(p)} for p in [widep,lexp]],'match_table_pin':mp,'unmatched_full_native_pin':{'path':str(up),'sha256':sha(up)},'lexical_routing_pin':lp,'source_index_pin':sp,'wide_native_objects':1059,'lexical_candidates':669,'exact_full_native_matches':exact,'unmatched_full_native_objects':len(unmatched),'multiple_exact_pointer_objects':multiple,'objects_with_non_equal_same_revision_pointers':len(nonmatches),'selected_source_files':len(pins),'full_native_pointer_count':sum(len(x) for x in index.values()),'failed_attempts':[],'elapsed_seconds':time.time()-start,'model_usage_root_collect_after_final':True,'no_source_dispositions_claimed_or_routing_read_certification':True,'prior113_members_777_targets_and_all_diagnostic_files_untouched':True,'no_stage_apply_or_rebind':True});print({'receipt':receipt,'matches':exact,'unmatched':len(unmatched),'multiple_exact':multiple,'sameid_non_equal':len(nonmatches),'sourcefiles':len(pins),'fullpointers':sum(len(x) for x in index.values())})
