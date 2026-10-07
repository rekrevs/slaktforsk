import json,hashlib,copy
from pathlib import Path
B=Path('evaluations/T-0781');p=B/'implementation/C0049-small14-copy104-C0067-clause22-drafts-v1/C0067-current-witness-clause22-full-individual-consequence-and-preservation-table-v1.json';t=json.loads(p.read_text());sp=Path(t['source_spec_pin']['path']);s=json.loads(sp.read_text());op=Path(t['operation_pin']['path']);o=json.loads(op.read_text());dp=B/'mechanical-current425-preparation-v1/full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json';D=json.loads(dp.read_text());gp=Path(t['guard_pin']['path']);g=json.loads(gp.read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def api(n):
 e={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':{k:v for k,v in n['data'].items() if k!='revision_id'},'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']}for r in n['origins']],'evidence':[],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 for r in n['evidence']:
  oid,v=r['basis_revision_id'].rsplit('@',1);e['evidence'].append({'object':oid,'version':int(v),'role':r['role'],'note':r['note']})
 for key in ['assets','media']:
  if key in n:e[key]=copy.deepcopy(n[key])
 return e
rows=[]
for i,(r,a,c) in enumerate(zip(t['rows'],s['objects'],o['changes'])):
 old=D['objects'][r['baseline_revision_ID']];e=api(old);assert e==r['old_API'];assert a['current']['data']==old['data'] and a['current']['caveat']==old['caveat'];assert a['edits']==r['source_exact_edits']
 for edit in a['edits']:
  parts=edit['field'].split('.');dest=e
  for k in parts[:-1]:dest=dest[k]
  assert dest[parts[-1]]==edit['old'];dest[parts[-1]]=edit['new']
 add=a['evidence_addition'];key='basis_revision_id' if 'basis_revision_id'in add else 'basis';oid,v=add[key].rsplit('@',1);e['evidence'].append({'object':oid,'version':int(v),'role':add['role'],'note':add['note']})
 assert e==c==r['new_API'];assert r['source_explicit_rebinds']==[]
 rows.append({'object_id':c['id'],'current_revision':old['id'],'actual_pointer':'/changes/'+str(i),'own_whole_prior_current_body_caveat_scope':'C0067-131-current-semantic-dispositions-and-22-exact-copy-findings-v1.json','actual_entire_new_body_read':True,'own_judgment':'ACCEPT exact corrected clause; original-name/role/place only, no guaranteed access/exclusive route/age/employer/kinship or identity claim. Existing historically qualified outcomes retain.','entire_API_independently_reconstructed':True,'all_nonexplicit_current_fields_and_ordered_arrays_exact':True,'source_pointer':'/objects/'+str(i)})
assert len(rows)==22==len(o['changes'])
out={'task':'T-0781','status':'BOUNDED_ACTUAL22_SOURCE_CONSEQUENCE_PASS','pins':[pin(z)for z in [op,sp,p,gp,dp,B/'independent-review/C0067-131-current-semantic-dispositions-and-22-exact-copy-findings-v1.json',B/'independent-review/C0067-three-producer-wrapper-whole-API-independent-review-v1.json']],'rows':rows,'metadata_reading_limit':'Ordered old metadata/evidence/origins mechanically compared to complete frozen current payload; equality is not a new source/full-person reading claim. Entire current semantic fields/caveats previously actually read, all22newbodytexts now read.','exact_producer_prerequisite':'TR-T0781-C0067-fullpost@1 must precede consumers','global_PASS':False,'runtime_authority':False}
f=B/'independent-review/C0067-twentytwo-actual-clause-entire-API-consequence-review-v1.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(f))
