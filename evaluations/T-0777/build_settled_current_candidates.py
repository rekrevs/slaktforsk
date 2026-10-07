import pathlib,json,sqlite3,hashlib
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
connection=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True);connection.row_factory=sqlite3.Row
exec((B/'native_payload.py').read_text())
for cid in ['C-0402','C-0573','C-0896']:
 path=B/'source-review'/f'{cid}-current-decisions-v1.json';dec=json.loads(path.read_text());changes=[];table=[]
 for d in dec['decisions']:
  oid=d['object'];obj=existing(oid,d['version']);cur=json.loads((B/'current'/('inspect-'+oid.replace('/','__')+'.json')).read_text())['current']
  fields=d['fields']
  if d.get('decision_ref'):
   ref=json.loads((B/'source-review'/d['decision_ref']).read_text());fields=[{'field':ref['field'],'old_full_field':ref['old_full_field'],'new_full_field':ref['new_full_field']}]
  for f in fields:
   key=f['field'].removeprefix('data.');assert cur[key]==f['old_full_field'],(cid,oid,key,'exact old field mismatch')
   new=f.get('new_full_field',f['old_full_field']);assert d['disposition']=='retain' or 'new_full_field' in f,(cid,oid,key,'no approved newfield')
   target=obj['data'] if key in obj['data'] else obj
   if d['disposition']=='revise':target[key]=json.loads(new) if key.endswith('_json') else new
   table.append({'source':cid,'object':oid,'version':d['version'],'kind':obj['kind'],'field':f['field'],'old_full_field':f['old_full_field'],'old_support':obj['evidence'],'full_current_context':cur,'approved_new_full_field':new,'disposition':d['disposition'],'reason':d['reason'],'exact_fullfield_match':True,'operation':f'T-0777/{cid.replace("-","")}-consequence-candidate-v1' if d['disposition']=='revise' else None})
  if d['disposition']=='revise':
   audit=('AUDIT-T0777-C0573-'+('P0430' if 'P-0430' in oid else 'P0433')) if cid=='C-0573' else 'AUDIT-T0777-C0896-SCB1930'
   newedges=[{'object':audit,'version':1,'role':'supports','note':f'T-0777 AC3: avgjord egen källräckvidd för {cid}; inga kontinuitets- eller identitetsinferenser.'}]
   if cid=='C-0896':
    newedges += [{'object':'R-T0777-C0896-Astrid-SCB1930','version':1,'role':'supports','note':'Egna SCB1930fält och lastarrival1926ankare.'},{'object':'AUDIT-T0777-C0896-parish','version':1,'role':'supports','note':'Egna parishfält; occupation-order reservation bevarad.'}]
   obj['evidence']+=newedges;changes.append(obj)
 (B/f'{cid}-consequence-table-v1.json').write_text(json.dumps({'task':'T-0777','scope':cid,'rows':table,'individually_disposed_objects':len(dec['decisions']),'revised_objects':len(changes),'retained_objects':len(dec['decisions'])-len(changes),'metadata_outcomes_preserved_unless_explicit_field_revision':True},ensure_ascii=False,indent=2)+'\n')
 if changes:
  out=B/f'{cid}-consequence-candidate-operation-v1.json';op={'id':f'T-0777/{cid.replace("-","")}-consequence-candidate-v1','actor':'Codex Sol exact settled individual dispositions','reason':f'T-0777 AC3–5: {cid} current source-specific copies corrected with exact field decisions and explicit versioned support; unrelated metadata/evidence/origins and review outcomes preserved; canonical-ready after independent final review.','dependencyReviewVersion':2,'changes':changes};out.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');(B/f'{cid}-first-consequence-freeze-v1.json').write_text(json.dumps({'task':'T-0777','files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [path,out,B/f'{cid}-consequence-table-v1.json']]},ensure_ascii=False,indent=2)+'\n')
 print(cid,len(changes),'revisions',len(dec['decisions'])-len(changes),'retains')
