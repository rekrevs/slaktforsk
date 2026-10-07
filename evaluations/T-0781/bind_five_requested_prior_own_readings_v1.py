"""Five bounded exact own-reading locators and current425 equality; no scope judgement."""
import json,hashlib,copy
from pathlib import Path
B=Path('evaluations/T-0781');T=Path('evaluations/T-0780');scope={};p=B/'prepare_bounded_consequence_inputs_v1.py';exec(compile(p.read_text().split('assert not W.exists();')[0],str(p),'exec'),scope);c=scope['conn'](scope['BASE']);old=scope['conn'](T/'preparation/baseline-j281.sqlite');native=scope['native'];pin=scope['pin'];defs=(B/'build_settled_core_and_PATH98_drafts_v2.py').read_text().split('assert W.exists();')[0];d={};exec(compile(defs,'draftAPIdefinitions','exec'),d);api=d['api']
def load(p):return json.loads(Path(p).read_text())
def diff(a,b,path=''):
 if type(a)!=type(b):return [{'pointer':path,'old':a,'new':b}]
 if isinstance(a,dict):return sum([diff(a[k],b[k],path+'/'+k) if k in a and k in b else [{'pointer':path+'/'+k,'old':a.get(k),'new':b.get(k),'key_missing_old':k not in a,'key_missing_new':k not in b}] for k in dict.fromkeys(list(a)+list(b))],[])
 if isinstance(a,list):
  if len(a)!=len(b):return [{'pointer':path,'old':a,'new':b}]
  return sum([diff(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))],[])
 return [] if a==b else [{'pointer':path,'old':a,'new':b}]
rows=[];natives={};rdir=T/'fresh-independent-review'
for rid in ['TR-T0780-C0069-fullpost@1','AUDIT-T0780-C0069-fullpost@1']:
 n=native(c,rid);natives[rid]=n
 if rid.startswith('TR'):
  rp=rdir/'C-0069-full13-actual-transcription-bounded-review-v1.json';r=load(rp);op=r['actual'];i=0;pred={'pointer':'/payload_check','literal':r['payload_check'],'coverage':r['coverage']};chain=[]
 else:
  rp=rdir/'resumed-nine-TR-audit-metadata-actual-independent-renewal-v1.json';r=load(rp);j=next(i for i,x in enumerate(r['objects']) if x['object_id']==n['object_id']);item=r['objects'][j];op=item['candidate'];i=4;pred={'pointer':'/objects/'+str(j),'literal':item};chain=item['whole_prior_API_reuse_receipts']
 assert pin(Path(op['path']))['sha256']==op['sha256'];payload=load(op['path'])['changes'][i];actual=api(n);actual.pop('expectedVersion');supplied=copy.deepcopy(payload);supplied.pop('expectedVersion');differences=diff(supplied,actual)
 rows.append({'revision_id':rid,'own_receipt_pin':pin(rp),'own_literal_reading_predicate':pred,'own_prior_reading_chain':chain,'exact_reviewed_API_input_pin':op,'exact_reviewed_API_input_pointer':'/changes/'+str(i),'current_full_native_pointer':'/objects/'+rid,'comparison_projection':'API expectedVersion control removed; native data JSON text parsed exactly, evidence/origin/assets/media native rowid order retained','actual425_API_field_differences':differences,'all_semantic_data_and_scalar_metadata_equal':not [x for x in differences if not x['pointer'].startswith('/evidence/')],'mechanical_equality_not_scope_grade':True})
rp=rdir/'C-0044-candidate-payload-reading-v1.json';r=load(rp);er=rdir/'C-0062-expanded-last21-reading-v1.json';e=load(er)
for rid,index in [('AUDIT-T0110-C-0048@1',0),('R-5bff8de790faa07588de3620@2',1),('TR-1b819812aa3415fd3cec9a5c@2',1)]:
 n=native(c,rid);prior=native(old,rid);natives[rid]=n;differences=diff(prior,n);assert not differences
 extra=[]
 if rid.startswith('AUDIT'):
  assert e['dispositions'][0]['object']['id']==rid;sn=e['dispositions'][0]['object'];extra=[{'receipt_pin':pin(er),'pointer':'/dispositions/0','individual_assertion':{k:v for k,v in e['dispositions'][0].items() if k!='object'},'exact_saved_data_caveat_equal':sn['data']==n['data'] and sn['caveat']==n['caveat']}]
 rows.append({'requested_id_spelling':'AUDIT-T0110-C0048@1' if rid.startswith('AUDIT') else rid,'exact_native_revision_id':rid,'exact_id_correction_not_alias_substitution':rid.startswith('AUDIT'),'own_receipt_pin':pin(rp),'own_literal_reading_predicate':{'pointer':'/stronger_support_read_receipt/'+str(index),'literal':r['stronger_support_read_receipt'][index]},'additional_own_snapshot_locator':extra,'prior_native_baseline_pin':pin(T/'preparation/baseline-j281.sqlite'),'current_full_native_pointer':'/objects/'+rid,'whole_native_current425_equals_prior281':True,'actual_field_differences':differences,'reading_scope_determined_by_Astra_only':True})
out=B/'bounded-consequence-inputs-v1/five-requested-stronger-C0069-C0048-exact-own-reading-current425-bindings-v1.json';assert not out.exists();out.write_text(json.dumps({'task':'T-0781','rows':rows,'objects':natives,'current425_baseline_pin':pin(scope['BASE']),'main425_pin':pin(scope['MAIN']),'no_new_original_or_scope_grade':True},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'output_pin':pin(out),'comparisons':[(x.get('revision_id',x.get('exact_native_revision_id')),x.get('actual425_API_field_differences',x.get('actual_field_differences'))) for x in rows]},ensure_ascii=False,indent=2));c.close();old.close()
