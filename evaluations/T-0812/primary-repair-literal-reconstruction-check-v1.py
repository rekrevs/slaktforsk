import json,pathlib,hashlib,copy,datetime
b=pathlib.Path('evaluations/T-0812');des=json.loads((b/'primary-actual134-repair-and-resolution-spec-v1.json').read_text());op=json.loads((b/'implementation/repair-operation-v1.json').read_text());tab=json.loads((b/'implementation/repair-consequence-table-v1.json').read_text())
rows={x['object_id']:x for x in tab['changes']};actual={x['id']:x for x in op['changes']};specs={x['id']:[x] for x in des['changes']};new={}
assert op['resolve']==[{'request':r['request'],'rationale':r['rationale']} for r in des['resolve']]
assert set(actual)==set(specs)|set(new)
fields=0
for oid,cs in specs.items():
 r=rows[oid]; old=r['old_native']; a=actual[oid]; assert a==r['new_api']; data={k:v for k,v in old['data'].items() if k!='revision_id'}
 for k in data:
  if k.endswith('_json') and isinstance(data[k],str):
   try:data[k]=json.loads(data[k])
   except ValueError:pass
 exp={'id':oid,'kind':old['kind'],'expectedVersion':old['version'],'data':data,'disposition':old['disposition'],'evidenceStatus':old['evidence_status'],'rationale':old['rationale'],'caveat':old['caveat'],'origins':[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in old['origins']],'evidence':[]}
 for e in old['evidence']:
  i,v=e['basis_revision_id'].rsplit('@',1);exp['evidence'].append({'object':i,'version':int(v),'role':e['role'],'note':e['note']})
 for key,sourcekey,outkey in [('assets','asset_path','path'),('media','asset_id','id')]:
  if old.get(key):exp[key]=[{outkey:x[sourcekey],'region':x['region']} for x in old[key]]
 for k in ['assets','media']:
  if k in a and k not in exp: exp[k]=[]
 for c in cs:
  assert c['expectedVersion']==old['version']
  for f in c['fields']:
   path=f['field'].split('.');p=exp
   for k in path[:-1]:p=p[k]
   ov=f['old']
   if path[-1].endswith('_json') and isinstance(ov,str):ov=json.loads(ov)
   assert p[path[-1]]==ov,(oid,f['field'],'old')
   p[path[-1]]=f['new'];fields+=1
  for rb in c.get('support_rebinds',[]):
   matches=[e for e in exp['evidence'] if e['object']+'@'+str(e['version'])==rb['old']];assert len(matches)==1
   i,v=rb['new'].rsplit('@',1);matches[0]['object']=i;matches[0]['version']=int(v)
  exp['evidence']+=c.get('appendEvidence',[])
 assert exp==a,(oid,'payload',set(exp)^set(a),[(k,exp.get(k),a.get(k)) for k in set(exp)|set(a) if exp.get(k)!=a.get(k)])
for oid,c in new.items():
 exp=copy.deepcopy(c)
 if 'data' not in exp:
  keys=['record_id','text','reading_note'] if exp['kind']=='transcription' else ['subject_id','criteria','outcome','body']
  exp['data']={k:exp.pop(k) for k in keys}
 exp.setdefault('expectedVersion',None)
 assert exp==actual[oid],(oid,'new',set(exp)^set(actual[oid]))
assert len(tab['retains'])==89
assert not op.get('media')
proof={'task':'T-0812','result':'PASS','method':'Primary independent literal reconstruction from approved component fields and full old native table, including exact ordered metadata/evidence/origins/assets and explicit rebinds; all new payloads compared exactly.','changes':len(actual),'existing':len(specs),'new':len(new),'literal_fields':fields,'full_retains':len(tab['retains']),'operationSha256':hashlib.sha256((b/'implementation/repair-operation-v1.json').read_bytes()).hexdigest(),'consequenceSha256':hashlib.sha256((b/'implementation/repair-consequence-table-v1.json').read_bytes()).hexdigest()}
p=b/'primary-repair-literal-reconstruction-proof-v1.json';p.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(proof);print(hashlib.sha256(p.read_bytes()).hexdigest())
