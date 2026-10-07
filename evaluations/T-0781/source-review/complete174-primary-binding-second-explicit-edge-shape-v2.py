import json,hashlib,copy,sys
from pathlib import Path
B=Path('evaluations/T-0781');pp=Path(sys.argv[1]);proposal=json.loads(pp.read_text());tp=Path(proposal['full_individual_consequence_table_pin']['path']);table=json.loads(tp.read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def edge(e):
 oid,v=e['basis_revision_id'].rsplit('@',1);return {'object':oid,'version':int(v),'role':e['role'],'note':e['note']}
def api(n):
 a={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':{k:v for k,v in n['data'].items()if k!='revision_id'},'origins':[{'unit':o['unit_id'],'coverage':o['coverage'],'note':o['note']}for o in n['origins']],'evidence':[edge(e)for e in n['evidence']],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 if 'assets'in n:a['assets']=[{'path':x['asset_path'],'region':x['region']}for x in n['assets']]
 if 'media'in n:a['media']=n['media']
 return a
proof=[]
for i,r in enumerate(table['rows']):
 sp=Path(r['source_spec_pin']['path']);assert pin(sp)==r['source_spec_pin'];s=json.loads(sp.read_text())
 for part in r['source_decision_pointer'].strip('/').split('/'):s=s[int(part)]if isinstance(s,list)else s[part]
 assert s==r['exact_source_decision']
 if 'new_entire_API'in s:a=copy.deepcopy(s['new_entire_API']);oldok=None
 else:
  n=r['full_before_native'];a=api(n);assert a==r['full_before_API'],r['object_id'];oldok=True
  for k,v in s['current'].items():assert n[k]==v,(r['object_id'],'sourcecurrent',k)
  for e in s['edits']:
   parts=e['field'].split('.');v=a
   for part in parts[:-1]:v=v[part]
   assert v[parts[-1]]==e['old'],(r['object_id'],e['field']);v[parts[-1]]=e['new']
  for e in s.get('evidence_rebinds',[]):
   old=e.get('old',{'basis_revision_id':e.get('old_basis_revision_id'),'role':e.get('role'),'note':e.get('note')});want=edge(old);positions=[j for j,v in enumerate(a['evidence'])if v==want];assert len(positions)==1;pos=positions[0]
   if 'ordered_index'in e:assert pos==e['ordered_index']
   oid,version=e['new_basis_revision_id'].rsplit('@',1);a['evidence'][pos]['object']=oid;a['evidence'][pos]['version']=int(version)
  for e in ([s['evidence_addition']]if'evidence_addition'in s else s.get('evidence_additions',[])):a['evidence'].append(edge(e))
 amend=r.get('source_metadata_amendment')
 if r['object_id'].startswith('AUDIT-T0781'):
  ap=B/'source-review/two-full-audit-final-status-rationale-metadata-amendments-v1.json'
  amendments=json.loads(ap.read_text())['objects']; matches=[x for x in amendments if x['object_id']==r['object_id']];assert len(matches)==1
  amend=matches[0]
 if amend:
  # Exact source metadata amendment may be full source wrapper or one target entry.
  if 'field'in amend:
   assert a[amend['field']]==amend['old'];a[amend['field']]=amend['new']
  else:raise Exception(('unknown amendment shape',r['object_id'],list(amend)))
 assert a==r['entire_exact_after_API'],('WHOLE_API_MISMATCH',r['object_id'])
 op=json.loads(Path(r['operation_pin']['path']).read_text());assert pin(Path(r['operation_pin']['path']))==r['operation_pin'];assert op['changes'][r['change_index']]==a
 proof.append({'object_id':r['object_id'],'resulting_revision_id':r['resulting_revision_id'],'source_pin':r['source_spec_pin'],'source_pointer':r['source_decision_pointer'],'operation_pin':r['operation_pin'],'old_whole_API_from_native_exact':oldok,'independently_reconstructed_whole_new_API_exact':True,'all_unlisted_fields_and_order_retained':True})
out={'task':'T-0781','proposal_pin':pin(pp),'table_pin':pin(tp),'rows':proof,'count':len(proof),'scope':'Primary exact binding of already individually source-settled full fields/APIs, including ordered support and metadata; no new source reading','runtime_authorized':False,'explicit_audit_metadata_amendment_pin':pin(B/'source-review/two-full-audit-final-status-rationale-metadata-amendments-v1.json'),'preserved_initial_locator_failure_pin':pin(B/'source-review/complete174-primary-binding-initial-locator-assumption-failure-v1.json')};q=B/'source-review/complete174-primary-independent-API-reconstruction-and-source-binding-v1.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(q,hashlib.sha256(q.read_bytes()).hexdigest())
