import pathlib,json,sqlite3,hashlib,datetime
B=pathlib.Path(__file__).resolve().parent;R=B.parents[2];selection=json.loads((B/'selection.json').read_text());c=sqlite3.connect('file:'+str(R/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
journals=[]
for row in c.execute('select * from operation_payload order by sequence'):
 ps=list((R/'genealogy2/journal').glob(f'{row["sequence"]:09d}-*.json'));assert len(ps)==1;x=json.loads(ps[0].read_text());assert x['request']==json.loads(row['request_json']);journals.append({'sequence':row['sequence'],'operation_id':row['operation_id'],'path':str(ps[0].relative_to(R)),'sha256':hashlib.sha256(ps[0].read_bytes()).hexdigest(),'request_matches_sql':True})
assert len(journals)==277
manifest=json.loads((R/selection['basis']['path']).read_text());rows=[]
for item in manifest['whole_citation_crosswalk']:
 m=item['manifest'];cid=m['id'];receipt=selection['completion_receipts'].get(cid);checks=[];data=None
 if receipt:
  p=R/receipt['path'];data=json.loads(p.read_text());assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['sha256']
  def walk(x,route=''):
   if isinstance(x,dict):
    if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):
     q=R/x['path'];checks.append({'json_route':route,'path':x['path'],'expected_sha256':x['sha256'],'exists':q.is_file(),'hash_matches':q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==x['sha256']})
    for k,v in x.items():walk(v,route+'/'+k)
   elif isinstance(x,list):
    for i,v in enumerate(x):walk(v,route+'/'+str(i))
  walk(data)
 rows.append({'citation':cid,'manifest_full_metadata':item,'completion_receipt':receipt,'completion_full_fields':data,'direct_bound_artifact_checks':checks,'accepted_reading_repetition_forbidden':bool(receipt),'remaining_scope':cid in selection['selected']})
assert len(rows)==40 and sum(bool(r['completion_receipt']) for r in rows)==39
out={'task':'T-0778','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_journal':277,'pending':0,'journal_request_checks':journals,'manifest_count':40,'accepted_receipts':39,'remaining_scopes':selection['selected'],'complete_manifest_crosswalk':rows,'direct_binding_mismatches':[{'citation':r['citation'],**x} for r in rows for x in r['direct_bound_artifact_checks'] if not x['hash_matches']],'closure_semantic_assessment':'Independent Astra must assess all task acceptance criteria and explicit followupownership from preserved inputs; counts alone do not prove completion.'};(B/'program40-reconciliation-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('277journals/40manifest/39receipts; directbinding discrepancies',len(out['direct_binding_mismatches']))
