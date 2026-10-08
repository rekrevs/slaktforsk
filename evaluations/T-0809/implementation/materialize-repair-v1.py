import json,copy,hashlib,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0809';I=D/'implementation';start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(I/'stage472-v2/stage.sqlite');assert h.state(c)=={'journal_head':472,'pending':96};sf=D/'primary-actual96-repair-and-resolve-spec-v2.json';assert sha(sf)=='fabaa4dc93cb4464532ad1ce7cc2d971f61cae3e96a627a27966bbb9264992df';spec=json.load(open(sf));pending=[dict(x)for x in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];assert [x['id']for x in pending]==[x['request']for x in spec['resolve']];apis={};olds={};fields={};rebinds=[]
for change in spec['changes']:
 oid=change['id'];assert oid not in apis;n=h.native(c,h.current(c,oid));assert n['version']==change['expectedVersion'];api=h.api(n);api['expectedVersion']=n['version'];olds[oid]=n;fields[oid]=change['fields']
 for f in change['fields']:
  parent=api if f['field']=='caveat' else api['data'];assert parent[f['field']]==f['old'],('oldfield mismatch',oid,f['field']);parent[f['field']]=f['new']
 for r in change['evidenceRebinds']:
  assert n['evidence'][r['index']]==r['oldEdge'];e=api['evidence'][r['index']];assert e['object']==r['object']and e['version']==r['oldVersion'];e['version']=r['newVersion'];rebinds.append({'target':oid,**r})
 for e in change['supportAppend']:
  assert e not in api['evidence'],('duplicate',oid,e);api['evidence'].append(copy.deepcopy(e))
 apis[oid]=api
heads=dict(c.execute('select object_id,max(version)from revision group by object_id'));projected={**heads,**{oid:a['expectedVersion']+1 for oid,a in apis.items()}};issues=[]
for oid,a in apis.items():
 for index,e in enumerate(a['evidence']):
  assert e['object']in projected
  if e['version']!=projected[e['object']]:issues.append({'target':oid,'index':index,'edge':e,'current':heads.get(e['object']),'projected':projected[e['object']]})
request_table=[];retains=[]
for req,decision in zip(pending,spec['resolve']):
 assert req['affected_revision_id']==decision['affected_revision_id']and req['changed_revision_id']==decision['changed_revision_id'];old=h.native(c,req['affected_revision_id']);current=h.native(c,h.current(c,old['object_id']));assert old==current;request_table.append({'actual_request':req,'source_disposition':decision,'full_old_and_current_native':current,'changed_basis_native':h.native(c,req['changed_revision_id'])})
 if decision['decision']=='RETAIN_EXACT':assert old['object_id']not in apis;retains.append({'revision_id':old['id'],'old_native':old,'source_disposition':'RETAIN_EXACT','rationale':decision['rationale'],'request_id':req['id']})
 else:assert decision['decision']=='REVISE'and old['object_id']in apis
op={'id':'T-0809/four-current-copy-repairs-and-96-individual-decisions-v1','actor':'Codex / settled Astra decisions','reason':'T-0809 AC1–4: four exact current-copy corrections and 96 individualized actual dependency dispositions after accepted source adoption. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':list(apis.values()),'resolve':[{'request':x['request'],'rationale':x['rationale']}for x in spec['resolve']]};p=I/'repair-operation-v1.json';assert not p.exists();p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');table={'operation_sha256':sha(p),'source_spec':{'path':str(sf.relative_to(R)),'sha256':sha(sf)},'changes':[{'object_id':oid,'old_native':olds[oid],'new_api':a,'literal_fields':fields[oid],'source_disposition':'REVISE','rationale':'Exact source-approved four-copy followup'}for oid,a in apis.items()],'individual_request_consequences':request_table,'retains':retains,'explicit_rebinds':rebinds};q=I/'repair-consequence-table-v1.json';q.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');pf=I/'repair-preflight-v1.json';pf.write_text(json.dumps({'changes':4,'individual_resolutions':96,'individual_retains':len(retains),'issues':issues,'literal_old_fields_exact':True,'old_native_order_preserved':True,'elapsed_seconds':time.monotonic()-start},indent=2)+'\n');print('op',sha(p));print('table',sha(q));print('issues',len(issues),'retains',len(retains))
