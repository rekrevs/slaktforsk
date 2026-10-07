import pathlib,json,sqlite3,hashlib
B=pathlib.Path(__file__).resolve().parent;base=sqlite3.connect(B/'clone/research-pre.sqlite');base.row_factory=sqlite3.Row;stage=sqlite3.connect(B/'clone/final-candidate-v3.sqlite');stage.row_factory=sqlite3.Row
ops=json.loads((B/'final-full-stage-check-v2.json').read_text())['operations']
def payload(db,oid):
 r=db.execute('select * from current_revision where object_id=?',(oid,)).fetchone()
 if not r:return None
 r=dict(r);return {'revision':r,'data':dict(db.execute('select * from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone()),'evidence':[dict(z) for z in db.execute('select * from dependency where revision_id=?',(r['id'],))],'origins':[dict(z) for z in db.execute('select * from origin where revision_id=?',(r['id'],))]}
for scope in ['0084','0402','0573','0896','0911']:
 selected=[n for n in ops if n.startswith('C-'+scope)];mut=[]
 for n in selected:
  for ch in json.loads((B/n).read_text())['changes']:
   old=payload(base,ch['id']);new=payload(stage,ch['id']);diff=[]
   if old:
    for section in ['revision','data']:
     for field in new[section]:
      if field in ['id','revision_id','version']:continue
      if old[section].get(field)!=new[section][field]:diff.append({'field':section+'.'+field,'old':old[section].get(field),'new':new[section][field]})
   mut.append({'object':ch['id'],'old_version':None if old is None else old['revision']['version'],'new_version':new['revision']['version'],'operation':n,'old_full_fields':old,'new_full_fields':new,'exact_changed_fields':diff})
 dispositions=[]
 for p in sorted((B/'source-review').glob('C-'+scope+'*decisions*.json')):
  d=json.loads(p.read_text());dispositions.append({'path':str(p.relative_to(B)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'decisions':d})
 p=B/f'C-{scope}-final-consequence-table-v3.json';p.write_text(json.dumps({'task':'T-0777','scope':'C-'+scope,'mutations':mut,'primary_individual_dispositions':dispositions,'direct_source_dispositions':json.loads((B/f'source-review/C-{scope}-direct-source-dispositions-v1.json').read_text()),'historical_candidates_preserved':True,'full_structured_data_present':True},ensure_ascii=False,indent=2)+'\n')
print('five final complete tables created')
