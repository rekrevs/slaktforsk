import pathlib,json,hashlib,importlib.util,time
R=pathlib.Path.cwd();D=R/'evaluations/T-0810';I=D/'implementation';S=I/'stage476-v1';sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(S/'stage.sqlite');assert h.state(c)=={'journal_head':476,'pending':0};start=time.monotonic();ops=[json.load(open(I/p)) for p in ['operation-v3.json','repair-operation-v1.json','six-resolution-operation-v1.json']];table=[json.load(open(I/p)) for p in ['consequence-table-v3.json','repair-consequence-table-v1.json','six-resolution-consequence-table-v1.json']];expected={x['id']:x for op in ops for x in op['changes']};proof=[]
for oid,x in expected.items():
 n=h.native(c,h.current(c,oid));a=h.api(n);assert a==h.expected_defaults(x,a);proof.append({'object_id':oid,'actual_native':n,'final_literal_api_exact':True})
res=[]
for op in ops[1:]:
 actual=[dict(x)for x in c.execute('select *from review_resolution where operation_id=? order by rowid',(op['id'],))];assert [{'request':x['request_id'],'rationale':x['rationale']}for x in actual]==op['resolve'];res.extend(actual)
retains=[]
for t in table:
 for row in t['retains']:
  assert h.native(c,row['revision_id'])==row['old_native'];oid=row['old_native']['object_id'];now=h.current(c,oid);assert now==row['revision_id']or oid in expected;retains.append({'revision_id':row['revision_id'],'current_revision_id':now,'current_exact_retained':now==row['revision_id'],'source_approved_followup_revision':now!=row['revision_id']and oid in expected,'rationale':row.get('rationale',row.get('source_disposition',{})),'request_id':row.get('request_id')})
media=[]
for m in ops[0]['media']:
 rr=dict(c.execute('select *from native_asset where id=?',(m['id'],)).fetchone());assert rr['sha256']==m['sha256']and rr['storage_path']==m['storagePath'];p=R/m['storagePath'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'];media.append(rr)
out=S/'final-native-135-and-65-resolution-proof.json';out.write_text(json.dumps({'state':h.state(c),'full_final_native_changes':proof,'individual65_stored_resolutions':res,'all_old_retain_native_versions_preserved':retains,'two_native_media_exact':media,'elapsed_seconds':time.monotonic()-start},ensure_ascii=False,indent=2)+'\n');print('native',len(proof),'resolutions',len(res),'retains',len(retains),'followup_retains',sum(x['source_approved_followup_revision'] for x in retains));print(hashlib.sha256(out.read_bytes()).hexdigest())
