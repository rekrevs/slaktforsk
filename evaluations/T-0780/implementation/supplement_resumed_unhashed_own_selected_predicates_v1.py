"""Own explicit read-ID predicates without a declared standalone input hash; locators only."""
import json,hashlib,datetime
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/resumed-final-selected-and-prior-own-predicate-join-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(s):return str(s).replace('~','~0').replace('/','~1')
P=W/'compact-strict-own-predicates-input-index-and-current-field-equality-v1.json';assert sha(P)=='fc234a10bbf8773930e0c65957bd4ec3806892fb845fea17d349efcd4dfaa08b';d=load(P)
F=B/'implementation/five-expanded-exactnative-pointer-join-v2/full-frozen-native-residual-dictionary-v1.json';native=load(F)['objects']
for name in ['current-full-native-objects-v1.json','additional-context-full-native-objects-v2.json']:
 for x in load(B/'implementation/dependency-preparation-v1'/name)['objects'].values():native.setdefault(x['id'],x)
selected={}
for cid in ['C-0044','C-0106','C-0561','C-0563','C-0060','C-0685','C-0069']:
 p=B/'preparation/selected'/f'{cid}-source-relevant-current-context-v1.json'
 if p.exists():selected[cid]=(pin(p),{x['revision_id']:(i,x) for i,x in enumerate(load(p)['objects'])})
readingindex=B/'fresh-independent-review/C-0561-all288-selected-reading-index-v1.json';idoc=load(readingindex);indexbindings={}
for i,x in enumerate(idoc['receipts']):
 assert sha(x['path'])==x['sha256']
 for rid in x['read_ids']:indexbindings[(x['path'],rid)]={'own_fullselected_scope_index_pin':pin(readingindex),'own_fullselected_scope_index_pointer':'/receipts/'+str(i),'literal_own_fullselected_scope':idoc['scope']}
locators={}
for p in sorted((B/'fresh-independent-review').glob('*.json')):
 doc=load(p);cid=doc.get('citation');ids=doc.get('read_ids')
 if cid not in selected or not isinstance(ids,list):continue
 inputpin,objects=selected[cid]
 if any(isinstance(doc.get(k),str) and doc[k]==inputpin['sha256'] for k in ['input_sha256','source_input_sha256','selected_input_sha256']):continue
 scope={k:v for k,v in doc.items() if k in ['status','scope','method','reading_note','read_scope']}
 for i,rid in enumerate(ids):
  if not isinstance(rid,str) or rid not in objects or rid not in native:continue
  ix,snap=objects[rid];base=native[rid];equal=snap['data']==base['data'] and snap['caveat']==base['caveat']
  locators.setdefault(rid,[]).append({'own_individual_receipt_pin':pin(p),'own_individual_full_read_ID_pointer':'/read_ids/'+str(i),'literal_own_explicit_ID_version':rid,'literal_own_reading_scope':scope,'source_specific_selected_input_locator_pin':inputpin,'source_specific_selected_input_pointer':'/objects/'+str(ix),'source_specific_input_index_exact_ID_version_equal':snap['revision_id']==rid,'selected_full_data_caveat_equal_frozen_native':equal,'native_input_locator_pin':pin(F) if rid in load(F)['objects'] else None,'native_input_pointer':'/objects/'+esc(rid),'input_hash_NOT_declared_in_this_individual_own_receipt':True,'input_locator_basis':'Exact own citation plus immutable native ID/version and unique preserved selected-context row; not an independently declared historical input-hash assertion','own_whole_selected_reading_index_binding':indexbindings.get((str(p),rid)),'metadata_field_names_absent_in_selected_snapshot':[k for k in base if k not in snap],'no_prior_input_hash_or_scope_grade_or_readcredit_inferred':True})
scopes={};counts={}
for scope,rows in d['scopes'].items():
 result=[]
 for row in rows:
  if not row['no_exact_saved_whole_data_caveat_match']:continue
  rid=row['revision_id'];ls=locators.get(rid,[])
  if ls:result.append({'revision_id':rid,'explicit_own_full_read_predicates_and_unhashed_selected_input_locators':ls,'strict_declared_input_snapshot_binding_still_unavailable_in_prior_index':True})
 scopes[scope]=result;counts[scope]={'previous_strict_missing_rows':sum(x['no_exact_saved_whole_data_caveat_match'] for x in rows),'explicit_own_read_ID_version_selected_context_locators':len(result),'still_no_supplemental_own_selected_read_ID_locator':sum(x['no_exact_saved_whole_data_caveat_match'] for x in rows)-len(result)}
p=W/'supplemental-explicit-own-selected-read-predicates-with-unhashed-input-locators-v1.json';assert not p.exists();p.write_text(json.dumps({'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'strict_input_index_pin':pin(P),'counts':counts,'scopes':scopes,'rules':'These are literal own per-ID/version full-reading predicates plus source-specific context locators. A standalone historical input hash was not declared by that individual receipt. Reviewer decides immutable-version sufficiency and source scope; no blanket input, metadata or sourcecredit inferred.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result_pin':pin(p),'counts':counts},indent=2))
