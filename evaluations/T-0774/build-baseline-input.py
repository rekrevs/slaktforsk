"""Read-only, source-agnostic packaging of the fixed historical baseline."""
from pathlib import Path
import sqlite3,json,hashlib,shutil,datetime
from urllib.parse import quote
H=Path(__file__).resolve().parent; R=H.parents[1]; B=json.loads((H/'baseline-lock.json').read_text());D=sqlite3.connect('file:'+B['database']+'?mode=ro',uri=True);D.row_factory=sqlite3.Row
P=['P-0003','P-0007','P-0015','P-0016','P-0042','P-0043','P-0010','P-0020','P-0021','P-0022','P-0023','P-0024','P-0025'];marks=','.join('?' for _ in P);out=H/'baseline-input';out.mkdir(exist_ok=True);(out/'objects').mkdir(exist_ok=True);(out/'segments').mkdir(exist_ok=True)
ids=set(P);subjectids=set()
for kind in ['assessment','narrative','fact','question']:
 subjectids.update(r['object_id'] for r in D.execute(f'select r.object_id from current_revision r join {kind} d on d.revision_id=r.id where d.subject_id in ({marks})',P))
ids.update(subjectids);cases=[]
for c in ['C-0020','C-0021','C-0023','C-0024','C-0025']:
 src=R/'evaluations/T-0773/baseline-context'/f'{c}-impact.json';im=json.loads(src.read_text());assert im['database_state']['last_operation']['sequence']==227; (out/f'{c}-impact.json').write_bytes(src.read_bytes());ci={x['object_id'] for x in im['review']['items']+im['seeds']};ids.update(ci);cases.append({'citation':c,'impact_object_ids':sorted(ci),'seeds':im['seeds']})
heads={r['object_id']:dict(r) for r in D.execute('select * from current_revision')};pending=[(i,heads[i]['version']) for i in ids];objs={}
while pending:
 oid,ver=pending.pop();key=oid+'@'+str(ver)
 if key in objs:continue
 rev=dict(D.execute('select * from revision where object_id=? and version=?',(oid,ver)).fetchone());kind=heads[oid]['kind'];data=dict(D.execute(f'select * from {kind} where revision_id=?',(key,)).fetchone());data.pop('revision_id')
 for k,v in data.items():
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 evidence=[]
 for d in D.execute('select * from dependency where revision_id=?',(key,)):
  bo,bv=d['basis_revision_id'].rsplit('@',1);evidence.append({'object':bo,'version':int(bv),'role':d['role'],'note':d['note']});pending.extend([(bo,int(bv)),(bo,heads[bo]['version'])])
 obj={'kind':kind,'revision':rev,'data':data,'origins':[{'unit':d['unit_id'],'coverage':d['coverage'],'note':d['note']} for d in D.execute('select * from origin where revision_id=?',(key,))],'evidence':evidence,'assets':([dict(d) for d in D.execute('select * from record_asset where revision_id=?',(key,))] if kind=='record' else [])};objs[key]=obj
 (out/'objects'/f'{quote(key,safe="")}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
# Uniform complete textual segmentation: no semantic selection or expected answers.
index=[];segindex=[]
for oid in sorted(ids):
 obj=objs[oid+'@'+str(heads[oid]['version'])];data=obj['data'];segmentids=[]
 for field,value in data.items():
  if not isinstance(value,str) or field.endswith('_id') or len(value)<80:continue
  for start in range(0,len(value),3000):
   end=min(start+3000,len(value));sid=f'{oid}@{heads[oid]["version"]}-{field}-{start}-{end}';seg={'segment_id':sid,'object_id':oid,'version':heads[oid]['version'],'kind':obj['kind'],'field':field,'start':start,'end':end,'text':value[start:end],'full_field_length':len(value),'evidence':obj['evidence'],'subject':data.get('subject_id')};(out/'segments'/f'{quote(sid,safe="")}.json').write_text(json.dumps(seg,ensure_ascii=False,indent=2)+'\n');segindex.append({k:seg[k] for k in ['segment_id','object_id','version','field','start','end','full_field_length','subject']});segmentids.append(sid)
 index.append({'id':oid,'version':heads[oid]['version'],'kind':obj['kind'],'subject':data.get('subject_id'),'criteria':data.get('criteria'),'segments':segmentids,'object_file':'objects/'+quote(oid+'@'+str(heads[oid]['version']),safe='')+'.json','person_scoped':oid in subjectids})
(out/'object-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n');(out/'segment-index.json').write_text(json.dumps(segindex,ensure_ascii=False,indent=2)+'\n');(out/'case-routing.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
for pid in P:
 shutil.copyfile(R/'evaluations/T-0773/baseline-context'/f'{pid}-person.json',out/f'{pid}-person.json')
manifest={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':227,'method':'All currentperson-subject assessment/narrative/fact/question objects forfixed13personcohort, plusinitialsourceimpacts andfull exact/currentbasisclosure. Uniform3000charactersegments, no facit-driven selection.','persons':P,'current_objects':len(ids),'person_subject_objects':len(subjectids),'basis_revisions':len(objs),'text_segments':len(segindex),'snapshot_files':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*.json')}};(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print({k:manifest[k] for k in ['current_objects','person_subject_objects','basis_revisions','text_segments']})
