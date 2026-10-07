import json,pathlib,hashlib,sqlite3,copy,time,collections
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0069-wide1059-reference-expansion-v1';w.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();p=b/'source-review/consequences-two/C-0069-complete-native-routing-dedup-v1.jsonl';rows=[json.loads(s) for s in p.open()];by=collections.defaultdict(list)
for o in rows:by[o['object_id']].append(o)
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;memo={};fallback={};errors=[];proof=[]
def native(oid):
 r=c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.object_id=? order by r.version desc limit 1',(oid,)).fetchone()
 if not r:raise ValueError('Missing exact baseline object '+oid)
 o=dict(r);rid=o['id'];o['data']=dict(c.execute('select * from '+o['kind']+' where revision_id=?',(rid,)).fetchone());o['origins']=[dict(t) for t in c.execute('select * from origin where revision_id=?',(rid,))];o['evidence']=[dict(t) for t in c.execute('select * from dependency where revision_id=?',(rid,))]
 if o['kind']=='record':o['assets']=[dict(t) for t in c.execute('select * from record_asset where revision_id=?',(rid,))];o['media']=[dict(t) for t in c.execute('select * from record_media where revision_id=?',(rid,))]
 return o
def resolve(oid,field,stack=()):
 key=(oid,field)
 if key in stack:raise ValueError('Exact reference cycle '+str(stack+(key,)))
 if key in memo:return memo[key]
 if field!='caveat':raise ValueError('Unknown reference field '+field)
 candidates=by.get(oid,[])
 if len(candidates)>1:raise ValueError('Multiple exact wide object matches '+oid)
 if candidates:o=candidates[0];origin='same_frozen_wide1059'
 else:o=native(oid);fallback[oid]=o;origin='explicit_fallback_frozen_baseline281_current_native'
 if field not in o:raise ValueError('Missing exact field '+oid+'.'+field)
 v=o[field];chain=[{'object_id':oid,'revision_id':o['id'],'field':field,'origin':origin}]
 if isinstance(v,dict):
  if set(v)!={'exact_same_as'} or not isinstance(v['exact_same_as'],str) or '.' not in v['exact_same_as']:raise ValueError('Unknown reference notation '+repr(v))
  target,f=v['exact_same_as'].rsplit('.',1);v,tail=resolve(target,f,stack+(key,));chain+=tail
 if not isinstance(v,str):raise ValueError('Resolved caveat is not exact string '+oid)
 current=native(oid)
 if o['id']!=current['id']:raise ValueError('Wide/fallback revision is not frozen current '+o['id'])
 if current[field]!=v:raise ValueError('Resolved value differs from exact frozen native '+oid+'.'+field)
 memo[key]=(v,chain);return memo[key]
expanded=copy.deepcopy(rows)
for old,new in zip(rows,expanded):
 if not isinstance(old.get('caveat'),dict):continue
 try:
  value,chain=resolve(old['object_id'],'caveat');new['caveat']=value;proof.append({'target_revision':old['id'],'original_exact_reference':old['caveat'],'resolved_string':value,'reference_chain':chain,'exact_frozen_current_native_value_equal':True,'source_disposition_not_adjudicated':True})
 except ValueError as e:errors.append({'target_revision':old['id'],'reference':old['caveat'],'error':str(e),'unresolved_original_preserved_needs_primary':True})
for old,new in zip(rows,expanded):
 r=copy.deepcopy(new);r['caveat']=old['caveat'];assert r==old
out=w/'expanded-full1059-native-input-v1.jsonl';assert not out.exists();out.write_text(''.join(json.dumps(o,ensure_ascii=False,separators=(',',':'))+'\n' for o in expanded));pp=w/'exact-reference-chain-native-proof-v1.json';pp.write_text(json.dumps({'original_input_pin':{'path':str(p),'sha256':sha(p)},'expanded_input_pin':{'path':str(out),'sha256':sha(out)},'proofs':proof,'errors_needing_primary':errors,'explicit_fallback_full_native_objects':fallback,'fallback_basis':'Existing task-frozen baseline-j281.sqlite read-only SQL full current native extraction; exact object_id only, no alias/fuzzy matching. All fallback use separately identified.','all_non_caveat_data_and_array_orders_exact_unchanged':True,'source_read_credit_and_judgments_not_adjudicated':True},ensure_ascii=False,indent=2)+'\n');rp=w/'reference-expansion-input-output-production-receipt-v1.json';rp.write_text(json.dumps({'proof_pin':{'path':str(pp),'sha256':sha(pp)},'expanded_pin':{'path':str(out),'sha256':sha(out)},'references_seen':len(proof)+len(errors),'verified_resolved':len(proof),'unresolved_errors':len(errors),'fallback_objects':len(fallback),'elapsed_seconds':time.time()-start,'failed_attempts':[],'no_prior_raw_diff_candidate_diagnostic_or_actual328_mutations':True,'model_usage_root_collect_after_final':True,'no_stage_apply_rebind':True},ensure_ascii=False,indent=2)+'\n');print({'receipt':sha(rp),'expanded':sha(out),'proof':sha(pp),'resolved':len(proof),'errors':len(errors),'fallback':len(fallback)})
