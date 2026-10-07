import json,copy,hashlib
from pathlib import Path
B=Path('evaluations/T-0781');sp=B/'source-review/P0052-P0053-structured-birth-place-three-revision-and-one-retain-decisions-v1.json';s=json.loads(sp.read_text());ip=Path(s['input_pin']['path']);inp=json.loads(ip.read_text());op=B/'implementation/birth52-53-settled-three-drafts-v1/01-P0052-P0053-structured-birth-place-three-revisions-draft-operation-v1.json';o=json.loads(op.read_text());rows=[]
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for i,(a,c) in enumerate(zip(s['objects'],o['changes'])):
 n=copy.deepcopy(a['current']);assert n==inp['objects'][n['id']]
 for x in a['edits']:
  ks=x['field'].split('.');v=n
  for k in ks[:-1]:v=v[k]
  assert v[ks[-1]]==x['old'];v[ks[-1]]=x['new']
 for x in a['evidence_rebinds']:
  v=n['evidence'][x['ordered_index']];assert v['basis_revision_id']==x['old_basis_revision_id'] and v['role']==x['role'] and v['note']==x['note'];v['basis_revision_id']=x['new_basis_revision_id']
 e={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':{k:(json.loads(v) if k.endswith('_json') and v is not None else v) for k,v in n['data'].items() if k!='revision_id'},'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']}for r in n['origins']],'evidence':[],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 for x in n['evidence']+a['evidence_additions']:
  oid,v=x['basis_revision_id'].rsplit('@',1);e['evidence'].append({'object':oid,'version':int(v),'role':x['role'],'note':x['note']})
 assert e==c
 rows.append({'object_id':c['id'],'actual_pointer':'/changes/'+str(i),'entire_actual_API_read':True,'independent_entire_API_reconstruction':True,'source_decision_pointer':'/objects/'+str(i),'own_judgment':a['reason'],'all_nonexplicit_fields_status_date_and_ordered_arrays_exact':True})
out={'task':'T-0781','status':'BOUNDED_THREE_BIRTH_SOURCE_FIELD_AND_ONE_RETAIN_PASS','pins':[pin(z)for z in[sp,ip,op,B/'independent-review/four-structured-birth-event-whole-current-reading-and-place-source-questions-v1.json']],'rows':rows,'own_actual_read_scope':{'whole_prior_C0046_C0072_citations':inp['source_document_pins'],'whole_source_wrappers_and_EP':[rid for rid,v in inp['objects'].items()if v['kind']in ['source','record'] or rid.startswith('READ-')or rid.startswith('EP-')],'whole_event_origins':[r['unit_id']for rid in ['E-birth-P-0052@1','E-birth-P-0053@1']for r in inp['objects'][rid]['origins']],'other_26_origin_units':'No new own fullreading credit; only five actual event-origin units needed and read. Two full source summaries and eight whole natives read, prior events/person/current ownreading reused.','new_original_images':0},'retained_EP52':{'revision_id':'EP-E-birth-P-0052-P-0052-principal@1','basis':'E-birth-P-0052@1','whole_current_native_read':True,'own_judgment':'Retain exact prior principal link and date/place values; E52 changes attribution/caveat only, so historical support remains sufficient. No automatic basis update.'},'finding_closure':'Both structured birthplace questions closed for exact actual operation. C46 explicitly supports P52 reported parish only. P53 former origin admits ditto basis; two relation origins add no birthplace. Null leaves geography undecided, not disproved. No identity or grade conversion.','global_PASS':False,'runtime_authority':False}
f=B/'independent-review/P0052-P0053-three-actual-birth-API-and-one-retain-independent-review-v1.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(f))
