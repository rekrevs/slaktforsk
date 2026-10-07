import pathlib,json,sqlite3,hashlib
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
connection=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True);connection.row_factory=sqlite3.Row
exec((B/'native_payload.py').read_text())
def save_op(name,oid,changes,reason):
 op={'id':oid,'actor':'Codex Sol exact approved source metadata amendment','reason':reason,'dependencyReviewVersion':2,'changes':changes};p=B/name;p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');return p
path=B/'source-review/C-0402-metadata-amendment-v3.json';d=json.loads(path.read_text());changes=[]
for dec in d['decisions']:
 obj=existing(dec['object'],dec['version']);cur=json.loads((B/'current'/('inspect-'+dec['object']+'.json')).read_text())['current']
 for f in dec['fields']:
  k=f['field'].removeprefix('data.');assert cur[k]==f['old_full_field'];target=obj['data'] if k in obj['data'] else obj;target[k]=f['new_full_field']
 obj['evidence'].append({'object':'AUDIT-T0777-C0402','version':1,'role':'supports','note':'T-0777: explicit own d./s. cells clear old unextracted-template flags; no identity change.'});changes.append(obj)
p=save_op('C-0402-role-metadata-candidate-operation-v1.json','T-0777/C0402-role-metadata-candidate-v1',changes,'T-0777 AC2–5: two settled own raw-role extractions and explicit stale-template metadata amendments; dependent requests individually reviewed later.')
(B/'C-0402-first-role-metadata-freeze-v1.json').write_text(json.dumps({'task':'T-0777','files':[{'path':str(q.relative_to(R)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in [path,p]]},ensure_ascii=False,indent=2)+'\n')
path=B/'source-review/C-0911-current-amendment-v2.json';d=json.loads(path.read_text());dec=next(x for x in d['decisions'] if x['object']=='R-5fcb723c98597da6131ddbea');obj=existing(dec['object'],dec['version']);cur=json.loads((B/'current'/('inspect-'+dec['object']+'.json')).read_text())['current']
for f in dec['fields']:
 k=f['field'].removeprefix('data.');assert cur[k]==f['old_full_field'];obj[k]=f['new_full_field']
obj['assets']=[{'path':x['path'],'region':x['region']} for x in cur['media'] if x['origin']=='legacy']
if any(x['origin']!='legacy' for x in cur['media']):raise RuntimeError('Native media must preserve explicitly before record revision')
p=save_op('C-0911-record-metadata-candidate-operation-v1.json','T-0777/C0911-record-metadata-candidate-v1',[obj],'T-0777 AC3–5: exact own Emma name/death metadata correction, all record data/assets/origins/evidence preserved; source/current same-row binding changes explicitly approved separately; dependent requests reviewed individually.')
(B/'C-0911-first-record-metadata-freeze-v1.json').write_text(json.dumps({'task':'T-0777','files':[{'path':str(q.relative_to(R)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in [path,p]],'assets_preserved':obj['assets']},ensure_ascii=False,indent=2)+'\n')
print('C0402 twoM metadata candidates; C0911 oneR metadata candidate frozen')
