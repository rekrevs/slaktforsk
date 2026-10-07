import pathlib,json,sqlite3,hashlib
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
connection=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True);connection.row_factory=sqlite3.Row
exec((B/'native_payload.py').read_text())
p=B/'source-review/C-0084-consequence-decisions-v1.json';dec=json.loads(p.read_text());changes=[];rowsout=[]
for d in dec['decisions']:
 oid=d['object'];obj=existing(oid,d['version']);capture=json.loads((B/'current'/('inspect-'+oid.replace('/','__')+'.json')).read_text());cur=capture['current']
 for f in d['fields']:
  field=f['field'];key=field.removeprefix('data.');assert cur[key]==f['old_full_field'],(oid,key,'old fullfield mismatch')
  if d['disposition']=='revise':
   target=obj['data'] if field.startswith('data.') else obj
   new=f['new_full_field'];target[key]=json.loads(new) if key.endswith('_json') else new
  rowsout.append({'source':'C0084 no34 count/status cells','object':oid,'version':d['version'],'field':field,'old_full_field':f['old_full_field'],'old_support':obj['evidence'],'new_full_field':f['new_full_field'],'disposition':d['disposition'],'reason':d['reason'],'full_current_context':cur,'exact_fullfield_match':True,'operation':'T-0777/C0084-consequence-candidate-v1' if d['disposition']=='revise' else None,'metadata_amendment':'P0118 sex caveat/source rationale precise; all unspecified metadata retained' if oid=='P-0118' else None})
 if d['disposition']=='revise':
  obj['evidence'].append({'object':'AUDIT-T0777-C0084','version':1,'role':'supports','note':'T-0777 AC3: avgjord fullfältsprövning, ersätter äldre räkne-/civilståndsattribution utan att skriva om historiken.'})
  for basis in d.get('append_evidence',[]):
   o,v=basis.rsplit('@',1);obj['evidence'].append({'object':o,'version':int(v),'role':'supports','note':'T-0777: äldre egen uttrycklig Ogift m-markering; könkunskap bevaras utan C0084-räkneinferens.'})
  changes.append(obj)
op={'id':'T-0777/C0084-consequence-candidate-v1','actor':'Codex Sol exact implementation of settled individual Astra dispositions','reason':'T-0777 AC3–5: correct five current source-attribution copies, preserve stronger1910sex support and all unrelated identity/review knowledge; canonical-ready after independent review.','dependencyReviewVersion':2,'changes':changes}
out=B/'C-0084-consequence-candidate-operation-v1.json';out.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
(B/'C-0084-consequence-table-v1.json').write_text(json.dumps({'task':'T-0777','scope':'C-0084','rows':rowsout,'individual_disposed_objects':14,'revised_objects':5,'retained_objects':9,'all_unspecified_fields_and_metadata_preserved':True},ensure_ascii=False,indent=2)+'\n')
(B/'C-0084-first-consequence-candidate-freeze-v1.json').write_text(json.dumps({'task':'T-0777','status':'first consequence candidate before clone testing','files':[{'path':str(x.relative_to(R)),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in [p,out,B/'C-0084-consequence-table-v1.json']]},ensure_ascii=False,indent=2)+'\n')
print('Five exact revisions;14 individually disposed objects; source audit and explicit1910support appended')
