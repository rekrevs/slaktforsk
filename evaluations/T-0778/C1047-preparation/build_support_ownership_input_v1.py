import pathlib,json,hashlib,sqlite3
B=pathlib.Path(__file__).resolve().parent;R=B.parents[2];mp=R/'genealogy2/verification/T-0673/manifest.json';cp=mp.parent/'cohorts-draft.json';m=json.loads(mp.read_text());co=json.loads(cp.read_text());group=json.loads((B/'full-group-closure-input-v1.json').read_text());cidroute={}
for z in group['40_scope_inputs']:
 for o in z['full_current_primary_and_sourcebound_objects']:cidroute.setdefault(o['revision']['object_id'],[]).append(z['citation'])
c=sqlite3.connect('file:'+str(R/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;out=[]
for kind,rows in co['support_association_owners'].items():
 for own in rows:
  if own['owner_cohort']!='G001':continue
  row=m[kind][own['manifest_index']];digest=hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();assert digest==own['row_sha256'];oid=row.get('object_id');r=c.execute('select * from current_revision where object_id=?',(oid,)).fetchone() if oid else None;cur=None
  if r:
   r=dict(r);cur={'revision':r,'full_data':dict(c.execute('select * from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone()),'evidence':[dict(z) for z in c.execute('select * from dependency where revision_id=?',(r['id'],))]}
  routes=cidroute.get(oid,[]);out.append({'support_kind':kind,'allocated_ownership':own,'exact_manifest_row':row,'hash_matches':True,'current_object':cur,'mechanical_related_scope_routes':routes,'accepted_outcome_refs':[z['accepted_receipt'] for z in group['40_scope_inputs'] if z['citation'] in routes and z['accepted_receipt']],'primary_or_independent_disposition':'ASTRA_REQUIRED'})
read=[z for z in co['content_reading_owners'] if z['owner_cohort']=='G001'];checks=[]
for z in read:
 checks.append({'allocated_owner':z,'actual_content_checks':[{'path':ref['id'],'exists':(R/ref['id']).is_file(),'actual_sha256':hashlib.sha256((R/ref['id']).read_bytes()).hexdigest() if (R/ref['id']).is_file() else None} for ref in z['asset_refs'] if ref['kind']=='imported_assets'],'meaning':'Primary ownership identifies original hash reading responsibility; exact accepted regions/fields still judged from source outcomes.'})
(B/'support-association-ownership-input-v1.json').write_text(json.dumps({'task':'T-0778','manifest_binding':{'path':str(mp.relative_to(R)),'sha256':hashlib.sha256(mp.read_bytes()).hexdigest()},'ownership_index_binding':{'path':str(cp.relative_to(R)),'sha256':hashlib.sha256(cp.read_bytes()).hexdigest()},'allocated_G001_support_rows':out,'content_reading_owners_G001':checks,'counts':{k:sum(z['support_kind']==k for z in out) for k in co['support_association_owners']},'disposition_limits':'Mechanical hash/current association evidence only; no source outcome assigned and no old original reopened.'},ensure_ascii=False,indent=2)+'\n');print('allocated supportrows',len(out),'contentowners',len(checks))
