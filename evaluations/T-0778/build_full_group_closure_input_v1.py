import pathlib,json,sqlite3,re,hashlib
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1];pre=json.loads((R/'genealogy2/verification/T-0677/pre-start-scope-review-proposed-20260924.json').read_text());sel=json.loads((B/'selection.json').read_text());c=sqlite3.connect('file:'+str(R/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
current={r['object_id']:dict(r) for r in c.execute('select * from current_revision')}
def full(oid):
 r=current[oid];d=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone());return {'revision':r,'full_data':d,'evidence':[dict(z) for z in c.execute('select * from dependency where revision_id=?',(r['id'],))],'origins':[dict(z) for z in c.execute('select * from origin where revision_id=?',(r['id'],))],'assets':[dict(z) for z in c.execute('select * from record_asset where revision_id=?',(r['id'],))] if r['kind']=='record' else [],'native_media':[dict(z) for z in c.execute('select * from record_media where revision_id=?',(r['id'],))] if r['kind']=='record' else []}
records=[r['manifest']['object_id'] for r in pre['current_records']];scope=[];allowners=set(['T-0227','T-0237','T-0410','T-0373','T-0631','T-0376','T-0732','T-0618','T-0619','T-0620'])
for item in pre['whole_citation_crosswalk']:
 m=item['manifest'];cid=m['id'];rids=set(m['native_record_ids']);objs=set(rids)
 # exact native direct support/current ownrecord membership, then review/adoption support closure forward.
 for oid,r in current.items():
  if r['kind'] not in ['transcript','assessment','research','observation','mention']:continue
  ds=c.execute('select basis_revision_id from dependency where revision_id=?',(r['id'],)).fetchall()
  if any(z[0].rsplit('@',1)[0] in rids for z in ds):objs.add(oid)
 for oid,r in current.items():
  if oid.startswith(('ADOPT-','AUDIT-','TR-')) and re.search(r'(?<![0-9])'+cid.replace('C-','C')+r'(?![0-9])',oid):objs.add(oid)
 receipt=sel['completion_receipts'].get(cid);rd=json.loads((R/receipt['path']).read_text()) if receipt else None
 if rd:
  allowners.update(re.findall(r'T-\d{4}',json.dumps(rd,ensure_ascii=False)))
 acceptedops=set()
 for oid in objs:acceptedops.add(current[oid]['operation_id'])
 payloads=[]
 for op in sorted(acceptedops):
  row=c.execute('select * from operation_payload where operation_id=?',(op,)).fetchone()
  if row:payloads.append({'sequence':row['sequence'],'operation_id':op,'request':json.loads(row['request_json'])})
 scope.append({'citation':cid,'accepted_receipt':receipt,'receipt_full_fields':rd,'scope_manifest':item,'full_current_primary_and_sourcebound_objects':[full(o) for o in sorted(objs)],'actual_current_operation_specs':payloads,'strength_reuse_disposition':'ASTRA_REQUIRED'})
backlog=json.loads((R/'wotan/backlog.json').read_text());tasks={t['id']:t for t in backlog['tasks']};owners=[]
for tid in sorted(allowners):
 if tid not in tasks:continue
 p=R/'wotan/dev-log'/(tid+'.md');owners.append({'task':tasks[tid],'devlog_path':str(p.relative_to(R)),'devlog_full_text':p.read_text() if p.is_file() else None,'owner_route_only':True})
assets=[]
for p in pre['fixed_manifest_members']['imported_assets']:
 row=c.execute('select * from asset where path=?',(p,)).fetchone();q=R/p;assets.append({'path':p,'registered':dict(row) if row else None,'actual_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'record_links':[dict(z) for z in c.execute('select * from record_asset where asset_path=?',(p,))]})
(B/'full-group-closure-input-v1.json').write_text(json.dumps({'task':'T-0778','baseline_journal':269,'40_scope_inputs':scope,'48_assigned_records_full_current':[full(o) for o in records],'33_primary_assets':assets,'11_extra_crossmedia_full_manifest':[{'citation':z['manifest']['id'],'extra_media':z['extra_media_outside_primary33']} for z in pre['whole_citation_crosswalk'] if z['extra_media_outside_primary33']],'union_checks':pre['union_checks'],'explicit_followup_task_routes_full':owners,'limitation':'Current mechanical full-field routing; no source approval or automatic taskDONE. Historical accepted operation payloads preserved in SQL, embedded change data arrays retain order.'},ensure_ascii=False,indent=2)+'\n');print('40scope/48R/33assets owners',len(owners))
