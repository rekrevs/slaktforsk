import json,pathlib,hashlib
b=pathlib.Path('evaluations/T-0810');load=lambda p:json.loads((b/p).read_text());ops=[load('implementation/'+p) for p in ['operation-v3.json','repair-operation-v1.json','six-resolution-operation-v1.json']];proof=load('implementation/stage476-v1/final-native-135-and-65-resolution-proof.json');actual={r['object_id']:r['actual_native'] for r in proof['full_final_native_changes']};errors=[]
for op in ops:
 for c in op['changes']:
  n=actual[c['id']]
  for k,ak in [('disposition','disposition'),('evidenceStatus','evidence_status'),('rationale','rationale'),('caveat','caveat')]:
   if c.get(k)!=n.get(ak):errors.append([c['id'],k])
  dat={k:v for k,v in n['data'].items() if k!='revision_id'}
  for k,v in list(dat.items()):
   if k.endswith('_json') and isinstance(v,str):
    try:dat[k]=json.loads(v)
    except:pass
  exp=c['data'].copy()
  for k,v in list(exp.items()):
   if k.endswith('_json') and isinstance(v,str):
    try:exp[k]=json.loads(v)
    except:pass
  if dat!=exp:errors.append([c['id'],'data',dat,exp])
  origins=[{'unit':q['unit_id'],'coverage':q['coverage'],'note':q['note']} for q in n['origins']]
  ev=[]
  for e in n['evidence']:
   ob,ver=e['basis_revision_id'].rsplit('@',1);ev.append({'object':ob,'version':int(ver),'role':e['role'],'note':e['note']})
  if origins!=c.get('origins',[]):errors.append([c['id'],'origins'])
  if ev!=c.get('evidence',[]):errors.append([c['id'],'evidence'])
res=[{'request_id':r['request'],'operation_id':op['id'],'rationale':r['rationale']} for op in ops for r in op.get('resolve',[])]
assert res==proof['individual65_stored_resolutions'];print('errors',json.dumps(errors,ensure_ascii=False)[:6000]);print('actual',len(actual),'resolutions',len(res))
f=b/'independent-final-native-check-result-v1.json';f.write_text(json.dumps({'actual135':len(actual),'ordered65':len(res),'errors':errors},ensure_ascii=False,indent=2)+'\n')
