"""Exact complete payload index for primary final assessment; no grades or writes to canonical."""
import json,hashlib,re,datetime,time,collections
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-current136-all10-audit-adoption-TR-index-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(k):return str(k).replace('~','~0').replace('/','~1')
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
M=B/'implementation/resumed-P0069-household-key-qualification-queue-v1/current136-candidate-membership-inventory-v1.json';assert sha(M)=='aab091f01b01b66b5d18972bde8672a9d023a6c9bd56dc84ef1a456c874b848b'
P=B/'implementation/resumed-P0069-household-key-qualification-queue-v1/concrete-current136-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='05ce6992a1e9c2132b60d65c8ed79871a86cb6ffdb2695a4808082ef80cb8264';members=load(M)['candidate_members'];assert members==load(P)['sequence'];assert len(members)==136
L=B/'root-pre-source-lock-v1.json';lock=load(L);OM=Path(lock['original_only_manifest']['path']);assert sha(OM)==lock['original_only_manifest']['sha256'];original=load(OM);assert set(x['citation'] for x in original['entries'])==set(lock['exact10'])
sourcefiles={sha(p):pin(p) for p in (B/'source-review').glob('*.json')};readindex=B/'implementation/resumed-current132-independent-receipt-join-v4/exact-review-receipt-input-index-v1.json';refs=load(readindex)['explicit_structured_path_hash_pairs'];reviewpins=load(readindex)['review_receipt_pins']
newconfig=[]
for p in (B/'implementation').glob('resumed-*-build-config-v*.json'):
 d=load(p);q=Path(d['source_path']);assert sha(q)==d['source_sha256'];newconfig.append({'configuration_pin':pin(p),'source_pin':pin(q),'output_dir':d['output_dir']})
rows=[];scope_counts=collections.Counter();type_counts=collections.Counter();flagcounts=collections.Counter()
flag=re.compile(r'pending|template|TODO|UNRUN|preliminary|incomplete|NOT_CHECKED|not yet|EJ UNDERSÖKT|inte läst|opróvad',re.I)
def flags(x,ptr=''):
 out=[]
 if isinstance(x,dict):
  for k,v in x.items():
   p=ptr+'/'+esc(k)
   if flag.search(k):out.append({'pointer':p,'key':k,'literal_value':v,'kind':'syntactic_key_flag'})
   out.extend(flags(v,p))
 elif isinstance(x,list):
  for i,v in enumerate(x):out.extend(flags(v,ptr+'/'+str(i)))
 elif isinstance(x,str):
  for match in flag.finditer(x):
   lo=max(0,match.start()-90);hi=min(len(x),match.end()+140);out.append({'pointer':ptr,'match':match.group(),'exact_character_span':[match.start(),match.end()],'bounded_exact_context':x[lo:hi],'kind':'lexical_string_flag_not_grade'})
 return out
for member in members:
 assert sha(member['path'])==member['sha256'];op=load(member['path'])
 for i,x in enumerate(op['changes']):
  oid=x['id']
  if not any(k in oid for k in ['AUDIT-T0780','ADOPT-T0780','TR-T0780']):continue
  digest=hashlib.sha256(canon(x).encode()).hexdigest();assert digest==member['targets'][i]['payload_sha256']
  category='audit' if oid.startswith('AUDIT-') else 'adoption' if oid.startswith('ADOPT-') else 'transcription'
  matches=re.findall(r'C0[0-9]{3}',oid);scope='C-'+matches[0][1:] if matches else 'UNRESOLVED_ID_ROUTING';scope_counts[scope]+=1;type_counts[category]+=1
  ownrefs=[r for r in refs if r['resolved_path']==member['path'] and r['declared_sha256']==member['sha256'] and r['declared_hash_matches_file']]
  source_refs=[r for r in refs if r['receipt_pin'] in [z['receipt_pin'] for z in ownrefs] and r['declared_hash_matches_file'] and r['resolved_path'].startswith(str(B/'source-review'))]
  reasonpins=[sourcefiles[h] for h in re.findall(r'[0-9a-f]{64}',op.get('reason','')) if h in sourcefiles]
  body=x['data'].get('body');parsed=None;parse_status=None
  if isinstance(body,str):
   try:parsed=json.loads(body);parse_status='valid_JSON_entire_body'
   except json.JSONDecodeError:parse_status='body_is_complete_non_JSON_text'
  f=flags(x);parsedflags=flags(parsed,'/parsed_entire_body') if parsed is not None else [];flagcounts[scope]+=len(f)+len(parsedflags)
  rows.append({'index':len(rows),'routing_citation_from_native_ID':scope,'kind':category,'object_id':oid,'expected_native_version':x['expectedVersion'],'proposed_native_version':(x['expectedVersion'] or 0)+1,'actual_operation_pin':{'path':member['path'],'sha256':member['sha256'],'operation_id':member['operation_id'],'sequence_index':member['index']},'actual_API_pointer':'/changes/'+str(i),'actual_payload_sha256':digest,'whole_actual_API_payload':x,'whole_ordered_evidence':x['evidence'],'whole_ordered_origins':x['origins'],'audit_entire_body_JSON_parse_status':parse_status,'audit_entire_body_parsed_JSON':parsed if category=='audit' else None,'syntactic_pending_template_flags':f+parsedflags,'original_scope_inputs':[a for a in original['entries'] if a['citation']==scope],'explicit_source_decision_SHA_pins_in_operation_reason':reasonpins,'exact_source_decision_inputs_related_by_own_review_document':source_refs,'exact_prior_own_receipt_operation_bindings':ownrefs,'no_grade_template_amendment_or_new_readcredit':True})
assert len(rows)==110
assert set(scope_counts)==set(lock['exact10'])
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
rp=save('complete-current136-all10-audit-adoption-TR-payload-and-flag-index-v1.json',{'task':'T-0780','membership_pin':pin(M),'proposal_pin':pin(P),'locked_exact10':lock['exact10'],'original_lock_pin':pin(L),'original_manifest_pin':pin(OM),'scope_counts':dict(scope_counts),'native_kind_counts':dict(type_counts),'flag_occurrence_counts':dict(flagcounts),'rows':rows,'resumed_settled_source_configuration_pins':newconfig,'no_primary_or_independent_assessment_inferred':True,'prior_receipt_index_historical_current132_pin':pin(readindex)})
pp=save('bounded-current136-all10-audit-adoption-TR-index-production-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result_pin':rp,'membership_pin':pin(M),'proposal_pin':pin(P),'actual_payloads':len(rows),'audit_adoption_transcription_counts':dict(type_counts),'scopes':len(scope_counts),'all_full_payloads_ordered_arrays_and_original_pins_preserved':True,'source_grade':'UNPERFORMED_BY_SOL','stage_canonical_probe':'UNRUN','elapsed_seconds':time.time()-START,'failed_attempts':[{'error':'Initial manifest entry-count assertion wrongly expected10; original units span12entries in10citations. Repaired by exact citation-set guard retaining all original entries; no writes in failed preparation.'},{'error':'Ad hoc FileNotFoundError for source checkpoint path; corrected source-review path, no writes or readcredit from failure'}],'actual_model_usage':'Root collects after worker final; unknown here'})
print(json.dumps({'result':rp,'production':pp,'counts':dict(type_counts),'scopes':dict(scope_counts)},indent=2))
