"""Uniform read-only export of native IDs in all fixed historical person views."""
from pathlib import Path
from urllib.parse import quote
import datetime,hashlib,json,sqlite3
h=Path(__file__).resolve().parent;old=h/'baseline-input';out=old/'supplement';out.mkdir(exist_ok=True);(out/'objects').mkdir(exist_ok=True);(out/'segments').mkdir(exist_ok=True)
b=json.loads((h/'baseline-lock.json').read_text());db=sqlite3.connect('file:'+b['database']+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
heads={r['object_id']:dict(r) for r in db.execute('select * from current_revision')};revs={r['id']:r['object_id'] for r in db.execute('select id,object_id from revision')};refs=set()
def collect(v):
 if isinstance(v,dict):
  for x in v.values():collect(x)
 elif isinstance(v,list):
  for x in v:collect(x)
 elif isinstance(v,str):
  if v in heads:refs.add(v)
  elif v in revs:refs.add(revs[v])
for p in sorted(old.glob('P-*-person.json')):collect(json.loads(p.read_text()))
baseids={i['id'] for i in json.loads((old/'object-index.json').read_text())};ids=refs-baseids;pending=[(i,heads[i]['version']) for i in ids];objects={}
while pending:
 oid,ver=pending.pop();key=f'{oid}@{ver}'
 if key in objects:continue
 rev=dict(db.execute('select * from revision where object_id=? and version=?',(oid,ver)).fetchone());kind=heads[oid]['kind'];data=dict(db.execute(f'select * from {kind} where revision_id=?',(key,)).fetchone());data.pop('revision_id')
 for k,v in data.items():
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 ev=[]
 for d in db.execute('select * from dependency where revision_id=?',(key,)):
  bo,bv=d['basis_revision_id'].rsplit('@',1);ev.append({'object':bo,'version':int(bv),'role':d['role'],'note':d['note']});pending.extend([(bo,int(bv)),(bo,heads[bo]['version'])])
 o={'kind':kind,'revision':rev,'data':data,'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in db.execute('select * from origin where revision_id=?',(key,))],'evidence':ev,'assets':[dict(r) for r in db.execute('select * from record_asset where revision_id=?',(key,))] if kind=='record' else []};objects[key]=o
 (out/'objects'/f'{quote(key,safe="")}.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
idx=[];si=[]
for oid in sorted(ids):
 ver=heads[oid]['version'];o=objects[f'{oid}@{ver}'];segments=[]
 for field,value in o['data'].items():
  if not isinstance(value,str) or field.endswith('_id') or len(value)<80:continue
  for start in range(0,len(value),3000):
   end=min(start+3000,len(value));sid=f'{oid}@{ver}-{field}-{start}-{end}';s={'segment_id':sid,'object_id':oid,'version':ver,'kind':o['kind'],'field':field,'start':start,'end':end,'text':value[start:end],'full_field_length':len(value),'evidence':o['evidence'],'subject':o['data'].get('subject_id')};(out/'segments'/f'{quote(sid,safe="")}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');si.append({k:s[k] for k in ('segment_id','object_id','version','field','start','end','full_field_length','subject')});segments.append(sid)
 idx.append({'id':oid,'version':ver,'kind':o['kind'],'subject':o['data'].get('subject_id'),'criteria':o['data'].get('criteria'),'segments':segments,'object_file':'supplement/objects/'+quote(f'{oid}@{ver}',safe='')+'.json','person_scoped':False,'routing':'referenced by fixed historical person view'})
(out/'object-index.json').write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n');(out/'segment-index.json').write_text(json.dumps(si,ensure_ascii=False,indent=2)+'\n')
assert refs <= baseids|ids
m={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':227,'method':'All exact native object/revision IDs appearing anywhere in all13 frozen person views, minus initially indexed IDs. Full exact/current dependency closure. No semantic or known-miss selection.','view_referenced_current_ids':sorted(refs),'additional_current_objects':len(ids),'closure_revisions':len(objects),'segments':len(si),'snapshot_files':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*.json')}};(out/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');db.close();print({k:m[k] for k in ('additional_current_objects','closure_revisions','segments')})
