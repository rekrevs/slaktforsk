import json,copy,hashlib
from pathlib import Path
B=Path('evaluations/T-0781');D=json.loads((B/'mechanical-current425-preparation-v1/full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json').read_text());d=B/'implementation/C0049-core-and-C0067-P0098-drafts-v1';tp=d/'six-exact-draft-operations-and-individual-consequence-preservation-table-v1.json';t=json.loads(tp.read_text());sp=Path(t['source_spec_pin']['path']);s=json.loads(sp.read_text());ps=Path(t['source_PATH98_spec_pin']['path']);ss=json.loads(ps.read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
rows=[]
for p in sorted(d.glob('[0-9]*operation*.json')):
 op=json.loads(p.read_text());assert len(op['changes'])==1;c=op['changes'][0]
 if c['expectedVersion'] is None:
  a=next(x for x in s['new_objects'] if x['object_id']==c['id']);assert a['new_entire_API']==c
 else:
  r=next(x for x in t['individual_revisions'] if x['object_id']==c['id']);e=copy.deepcopy(r['full_baseline_API']);old=D['objects'][c['id']+'@'+str(c['expectedVersion'])];assert e['data']=={k:v for k,v in old['data'].items() if k!='revision_id'};assert e['caveat']==old['caveat']
  for edit in r['source_edits']:
   keys=edit['field'].split('.');x=e
   for key in keys[:-1]:x=x[key]
   assert x[keys[-1]]==edit['old'];x[keys[-1]]=edit['new']
  # Compare the entire unchanged evidence prefix separately; source specs supply exact appended support.
  assert c['evidence'][:len(e['evidence'])]==e['evidence'];assert len(c['evidence'])-len(e['evidence']) in [0,1]
  if len(c['evidence'])>len(e['evidence']):
   a=next((x for x in s['revisions'] if x['object_id']==c['id']),None)
   if a is None:a=ss['objects'][0] if 'objects' in ss else ss
   add=a['evidence_addition'];b=add.get('basis',add.get('basis_revision_id'));oid,v=b.rsplit('@',1);e['evidence'].append({'object':oid,'version':int(v),'role':add['role'],'note':add['note']})
  assert e==c==r['full_candidate_API']
 status='PENDING_EXACT_RATIONALE_AMENDMENT' if c['id']=='TR-bf8e09efe7e3e3c20156c785' else 'BOUNDED_API_PASS'
 rows.append({'operation':pin(p),'object_id':c['id'],'pointer':'/changes/0','whole_actual_API_read':True,'entire_API_source_reconstruction':True,'status':status,'own_source_judgment':'Own frozen C49 top6 source/exposure/reservations and stronger C0184 retained; C67 PATH98 own1869 remains unread and no cost/field/independence guarantee. Source-level full extraction wrappers confer no identity/person review upgrade.','open_issue':'Current rationale still says old literal/no original reread despite corrected text; primary amendment a5f47aa… pending actual.' if status.startswith('PENDING') else None})
out={'task':'T-0781','status':'FIVE_BOUNDED_CORE_APIS_PASS_ONE_RATIONALE_PENDING','pins':[pin(tp),pin(sp),pin(ps),pin(B/'independent-review/C0049-original-first-whole-entry-reading-freeze-v1.json'),pin(B/'independent-review/nine-other-sibling-route-source-scope-dispositions-and-IF002-v1.json')],'rows':rows,'IF002':'CLOSED_FOR_EXACT_PATH98_DRAFT','incoming_scope':'12 exact primary record/event dispositions actually read, unchanged fathername/occupation accepted within exact own fields, dependent9 revisions inspected separately in small14; actual stage requests remain later gate.','global_PASS':False,'runtime_authority':False}
f=B/'independent-review/C0049-core-five-pass-one-metadata-pending-and-P0098-API-review-v1.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(f))
