import json,pathlib,hashlib,copy
p=pathlib.Path('evaluations/T-0808');l=lambda s:json.loads((p/s).read_text());h=lambda s:hashlib.sha256((p/s).read_bytes()).hexdigest()
s=l('primary-actual83-and-six-copy-amendment-v1.json');seven=l('primary-seventh-title-copy-amendment-v1.json');op=l('implementation/repair-operation-v2.json');t=l('implementation/repair-consequence-table-v2.json');ctx=l('implementation/stage470-v1/actual-dependency-contexts-full-v1.json');bases={r['affected_full_native']['object_id']:r['affected_full_native'] for r in ctx['requests']};bases[seven['object_id']]=seven['full_old_native']
def norm(z):
 z=copy.deepcopy(z)
 for k,v in z.get('data',{}).items():
  if k.endswith('_json') and isinstance(v,str):z['data'][k]=json.loads(v)
 return z
for row in t['changes']:
 old=row['old_native'];a=row['new_api'];assert norm(old)==norm(bases[a['id']]);assert a==next(v for v in op['changes'] if v['id']==a['id'])
 d=norm(old)['data'];d.pop('revision_id');ev=[]
 for e in old['evidence']:
  id,v=e['basis_revision_id'].rsplit('@',1);ev.append(dict(object=id,version=int(v),role=e['role'],note=e['note']))
 exp=dict(id=old['object_id'],kind=old['kind'],expectedVersion=old['version'],data=d,origins=[dict(unit=z['unit_id'],coverage=z['coverage'],note=z['note']) for z in old['origins']],evidence=ev,disposition=old['disposition'],evidenceStatus=old['evidence_status'],rationale=old['rationale'],caveat=old['caveat']);app=[]
 if a['id']==seven['object_id']:
  assert d['value_json']['reports'][1]['title']=='Arbet.';d['value_json']['reports'][1]['title']='hemmansägare';app=seven['evidence_append']
 else:
  for f in s['field_changes']:
   if f['id']!=a['id']:continue
   ptr=exp
   for k in f['field'][:-1]:ptr=ptr[k]
   prior=f['old'];prior=json.loads(prior) if f['field'][-1].endswith('_json') and isinstance(prior,str) else prior
   assert ptr[f['field'][-1]]==prior
   ptr[f['field'][-1]]=f['new']
   for e in f.get('append_supports',[]):
    if e not in app:app.append(e)
  for r in s['explicit_rebinds']:
   if r['id']!=a['id']:continue
   e=ev[r['index']];assert e['object']==r['basis'] and e['version']==r['old_version'];e['version']=r['new_version']
 ev.extend(app);assert exp==a,(a['id'],[(k,exp[k],a.get(k)) for k in exp if exp[k]!=a.get(k)])
assert len(op['changes'])==7 and len(op['resolve'])==83
for got,r in zip(op['resolve'],s['individual_dependency_decisions']):
 assert got['request']==r['request_id']; assert r['reason'] in got['rationale'];print(r['request_id'][:7],got['rationale'])
assert set(v['request'] for v in op['resolve'])==set(r['request']['id'] for r in ctx['requests'])
out={'repairOperationSha256':h('implementation/repair-operation-v2.json'),'consequenceSha256':h('implementation/repair-consequence-table-v2.json'),'seven_full_api_exact':True,'all83_requests_exact_order_source_rationales':True,'independent83SourceSha256':h('independent-actual83-source-dispositions-v1.json'),'canonicalApproval':False};f=p/'independent-seven-repair-literal-check-v2.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS',hashlib.sha256(f.read_bytes()).hexdigest())
