import json,hashlib,copy
from pathlib import Path
B=Path('evaluations/T-0781');p=B/'implementation/C0049-small14-copy104-C0067-clause22-drafts-v1/C0049-small14-full-individual-consequence-and-preservation-table-v1.json';t=json.loads(p.read_text());sp=Path(t['source_spec_pin']['path']);s=json.loads(sp.read_text());op=Path(t['operation_pin']['path']);o=json.loads(op.read_text());dp=B/'mechanical-current425-preparation-v1/full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json';D=json.loads(dp.read_text())
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
 old=D['objects'][r['baseline_revision_ID']];n=copy.deepcopy(old);assert api(old)==r['old_API'];assert a['current']['data']==old['data'] and a['current']['caveat']==old['caveat'];assert a['edits']==r['source_exact_edits']
 for edit in a['edits']:
  parts=edit['field'].split('.');dest=n
  for k in parts[:-1]:dest=dest[k]
  assert dest[parts[-1]]==edit['old'];dest[parts[-1]]=edit['new']
 for rebind in a.get('evidence_rebinds',[]):
  hits=[j for j,e in enumerate(n['evidence']) if e==rebind['old']];assert len(hits)==1;n['evidence'][hits[0]]['basis_revision_id']=rebind['new_basis_revision_id']
 e=api(n);add=a['evidence_addition'];oid,v=add['basis_revision_id'].rsplit('@',1);e['evidence'].append({'object':oid,'version':int(v),'role':add['role'],'note':add['note']});assert e==c==r['new_API']
 assert c['disposition']==old['disposition'] and c['evidenceStatus']==old['evidence_status']
 rows.append({'object_id':c['id'],'current_revision':old['id'],'actual_pointer':'/changes/'+str(i),'source_pointer':'/objects/'+str(i),'whole_actual_API_read':True,'entire_API_independently_reconstructed':True,'own_judgment':a['reason'],'no_identity_grade_outcome_upgrade':True,'explicit_rebinds_reviewed':a.get('evidence_rebinds',[]),'all_other_metadata_and_ordered_arrays_exact':True})
assert len(rows)==14
out={'task':'T-0781','status':'BOUNDED_ACTUAL_SMALL14_SOURCE_CONSEQUENCE_PASS','pins':[pin(z)for z in[op,sp,p,dp,B/'source-review/C0049-seven-mention-and-one-event-incoming-exact-source-dispositions-v1.json',B/'source-review/C0049-eleven-record-and-one-birth-event-incoming-source-dispositions-v1.json',B/'independent-review/sixtytwo-current-consumer-whole-reading-and-source-scope-dispositions-v1.json']],'rows':rows,'source_meaning':'Own D:r/name/date/place corrected, own blank younger places not inherited ditto; stronger own C48 birth untouched. Same P57 person and accepted/TRANSCRIBED link retained with corrected name. No new original birth record or independent identity voice. Full prior current body/caveat own reading reused; all14actualwholeAPIs now actually read.','incoming_semantic_dispositions':'Eight exact mention/event incoming source decisions read: same-name P52/P53 identities retain M@1, historical ID57@1 stays historical; three O and current ID57 plus EP57 use only explicit ordered rebinds. R49 eleven direct consumer decisions read; unchanged fathername and occupation with separate later support retain old basis. Actual requests/resolutions remain later stage gate.','global_PASS':False,'runtime_authority':False}
f=B/'independent-review/C0049-fourteen-actual-entire-API-and-direct-dependency-review-v1.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(f))
