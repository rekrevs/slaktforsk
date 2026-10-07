import json,hashlib,copy
from pathlib import Path
B=Path('evaluations/T-0781');p=B/'implementation/final-five-and-thirteen-adoption-drafts-v1/five-full-individual-clause-consequence-and-preservation-table-v1.json';t=json.loads(p.read_text());sp=Path(t['source_spec_pin']['path']);s=json.loads(sp.read_text());op=Path(t['operation_pin']['path']);o=json.loads(op.read_text());dp=B/'mechanical-current425-preparation-v1/full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json';D=json.loads(dp.read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def api(n):
 e={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':{k:v for k,v in n['data'].items() if k!='revision_id'},'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']}for r in n['origins']],'evidence':[],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 for k in list(e['data']):
  if k.endswith('_json') and e['data'][k] is not None:e['data'][k]=json.loads(e['data'][k])
 for r in n['evidence']:
  oid,v=r['basis_revision_id'].rsplit('@',1);e['evidence'].append({'object':oid,'version':int(v),'role':r['role'],'note':r['note']})
 for key in ['assets','media']:
  if key in n:e[key]=copy.deepcopy(n[key])
 return e
rows=[]
for i,(r,a,c) in enumerate(zip(t['rows'],s['objects'],o['changes'])):
 old=D['objects'][c['id']+'@'+str(c['expectedVersion'])];n=copy.deepcopy(old);assert api(old)==r['old_API'];assert a['current']['data']==old['data'] and a['current']['caveat']==old['caveat'];assert a['edits']==r['source_exact_edits']
 for edit in a['edits']:
  parts=edit['field'].split('.');dest=n
  for k in parts[:-1]:dest=dest[k]
  assert dest[parts[-1]]==edit['old'];dest[parts[-1]]=edit['new']
 for rebind in a.get('evidence_rebinds',[]):
  hits=[j for j,e in enumerate(n['evidence']) if e==rebind['old']];assert len(hits)==1;n['evidence'][hits[0]]['basis_revision_id']=rebind['new_basis_revision_id']
 e=api(n);add=a['evidence_addition'];oid,v=add['basis_revision_id'].rsplit('@',1);e['evidence'].append({'object':oid,'version':int(v),'role':add['role'],'note':add['note']});assert e==c==r['new_API']
 assert c['disposition']==old['disposition'] and c['evidenceStatus']==old['evidence_status']
 rows.append({'object_id':c['id'],'current_revision':old['id'],'actual_pointer':'/changes/'+str(i),'source_pointer':'/objects/'+str(i),'whole_actual_API_read':True,'entire_API_independently_reconstructed':True,'own_judgment':a['reason'],'no_identity_grade_outcome_upgrade':True,'explicit_rebinds_reviewed':a.get('evidence_rebinds',[]),'all_other_metadata_and_ordered_arrays_exact':True})
assert len(rows)==5
adp=B/'source-review/two-source-thirteen-individual-bounded-adoption-specifications-v1.json';ad=json.loads(adp.read_text());aop=B/'implementation/final-five-and-thirteen-adoption-drafts-v1/02-two-source-thirteen-bounded-adoptions-draft-operation-v1.json';actual=json.loads(aop.read_text());adrows=[]
for i,(a,c) in enumerate(zip(ad['new_objects'],actual['changes'])):
 assert c==a['new_entire_API'];assert c['data']['criteria']=='bounded_source_adoption/1' and c['disposition']=='recorded' and c['evidenceStatus'] is None
 assert c['evidence'][0]['object'] in ['TR-T0781-C0049-fullpost','TR-T0781-C0067-fullpost'];assert c['evidence'][0]['version']==1
 adrows.append({'object_id':c['id'],'subject_id':c['data']['subject_id'],'actual_pointer':'/changes/'+str(i),'source_pointer':'/new_objects/'+str(i),'source_entire_API_actually_read_then_actual_full_API_exact_compared':True,'own_judgment':'Accept own-source-row adoption only, including individual stronger-older limits as stated. No new historical identity, full-person/contract/tree/life approval or independent evidence voice.'})
assert len(adrows)==13==len(actual['changes'])
out={'task':'T-0781','status':'BOUNDED_ACTUAL_FIVE_CLAUSES_AND_THIRTEEN_ADOPTIONS_PASS','pins':[pin(z)for z in[op,sp,p,dp,adp,aop,B/'independent-review/C0049-121-current-semantic-scope-and-legacy-outcome-dispositions-v1.json',B/'independent-review/C0067-131-current-semantic-dispositions-and-22-exact-copy-findings-v1.json']],'five_clause_rows':rows,'thirteen_adoption_rows':adrows,'reading_scope':'Five current/new bodies+caveats whole read with exact source edits and full API reconstruction. Each entire13 adoption API actually source-read and exact actual API equality; no duplicate original/image read. Source-bound P0048 own strongerbirth, P0050/51 strongermarriage/birthconflicts, P52latercensus/P53folio852/P57singleownrow, C67rawages41/31/(4), sourcewitness role/age/identity limits retained individually.','required_order':'Exact corresponding TR49/67@1 producers before18consumers','global_PASS':False,'runtime_authority':False}
f=B/'independent-review/two-source-five-clause-and-thirteen-adoption-exact-API-review-v1.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(f))
