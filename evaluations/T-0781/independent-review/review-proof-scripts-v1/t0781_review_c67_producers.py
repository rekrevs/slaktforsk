import json,hashlib,copy
from pathlib import Path
base=Path('evaluations/T-0781'); sp=base/'source-review/two-settled-fullsource-TR-audit-and-four-wrapper-specifications-v1.json'; d=base/'implementation/C0067-fullTR-audit-READ-draft-v1'; s=json.loads(sp.read_text()); idxp=d/'C0067-three-draft-producer-audit-wrapper-exact-consequence-and-order-index-v1.json';idx=json.loads(idxp.read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
rows=[]
for p in sorted(d.glob('*operation*.json')):
 o=json.loads(p.read_text());assert len(o['changes'])==1;c=o['changes'][0]
 if c['expectedVersion'] is None:
  a=next(a for a in s['new_objects'] if a['object_id']==c['id']);assert c==a['new_entire_API'];reason='Complete prior T0131 full own post, raw ages/E/(4), three Ultervattnet witnesses and reserved fourth, no new original/identity/grade credit. Entire embedded extraction read and checked against own sufficient prior reuse receipt.'
 else:
  a=next(a for a in s['revisions'] if a['object_id']==c['id']);old=a['current'];e=copy.deepcopy(idx['READ_baseline_API'])
  assert old=={k:v for k,v in idx['READ_current'].items()}
  for edit in a['edits']:
   parts=edit['field'].split('.');dest=e
   for key in parts[:-1]:dest=dest[key]
   assert dest[parts[-1]]==edit['old'];dest[parts[-1]]=edit['new']
  add=a['evidence_addition'];oid,v=add['basis'].rsplit('@',1);e['evidence'].append({'object':oid,'version':int(v),'role':add['role'],'note':add['note']});assert c==e
  reason='Recognizes sufficient complete prior source reading through bounded source boundary outcome only. Keeps R67@1 and all old ordered supports/origins, adds same-source TR. No person contract, witness identification or independent evidence upgrade.'
 rows.append({'operation':pin(p),'actual_pointer':'/changes/0','object_id':c['id'],'whole_operation_and_entire_API_read':True,'exact_source_reconstruction':True,'own_source_consequence':reason})
assert idx['incoming_zero'] is True
out={'task':'T-0781','status':'BOUNDED_C0067_THREE_PRODUCER_WRAPPER_API_PASS','source_spec':pin(sp),'mechanical_input':pin(idxp),'individual_rows':rows,'prerequisite_own_reading':pin(base/'independent-review/first-bounded-source-comparison-and-C0067-reuse-findings-v1.json'),'required_order':'TR before audit/READ and all support consumers','source_bound_outcome_not_person_review_upgrade':True,'global_approval':False,'runtime_authority':False}
p=base/'independent-review/C0067-three-producer-wrapper-whole-API-independent-review-v1.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(p))
