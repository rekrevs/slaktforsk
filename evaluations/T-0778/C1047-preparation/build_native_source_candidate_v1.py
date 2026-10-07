import pathlib,json,sqlite3
P=pathlib.Path(__file__).resolve().parent;B=P.parent;s=json.loads((B/'source-review/C-1047-native-source-spec-v1.json').read_text());c=sqlite3.connect(P/'clone/research-pre.sqlite');c.row_factory=sqlite3.Row;changes=[]
def ev(ref):
 oid,v=ref.rsplit('@',1);return {'object':oid,'version':int(v),'role':'supports','note':'T-0778 AC2–4: exact individually approved source-bound basis.'}
def add(oid,kind,data,caveat,supports,**extra):
 changes.append({'id':oid,'kind':kind,'expectedVersion':None,'data':data,'origins':[],'evidence':[ev(r) for r in supports],'disposition':'recorded','evidenceStatus':None,'rationale':'T-0778 AC2–4: mechanical implementation of settled native source specification; bounded adoption and unlinked source mentions.','caveat':caveat,**extra})
r=s['new_record'];mid='M-'+r['asset_sha256'];add(r['id'],'record',{k:r[k] for k in ['source_id','record_type','locator','dependence_note']},r['caveat'],r['supports'],assets=[],media=[{'id':mid,'region':'C-1047 own rows18–20; all18columns/headers/blanks/margins; other groups separately represented.'}])
for g in s['groups']:
 t=g['TR'];add(t['id'],'transcription',{k:t[k] for k in ['record_id','text','reading_note']},t['caveat'],g['supports'])
 a=g['audit'];add(a['id'],'assessment',{k:a[k] for k in ['subject_id','criteria','outcome','body']},a['caveat'],g['supports']+[t['id']+'@1'])
for a in s['adoptions']:
 supports=a['supports']+s['additional_adoption_supports'].get(a['id'],[])
 for ref in supports:
  oid,v=ref.rsplit('@',1)
  if not any(z['id']==oid for z in changes) and oid not in [g['record_id'] for g in s['groups']]:
   row=c.execute('select version from current_revision where object_id=?',(oid,)).fetchone();assert row and row[0]==int(v),(ref,'unexpected current basis')
 add(a['id'],'assessment',{k:a[k] for k in ['subject_id','criteria','outcome','body']},a['caveat'],supports)
for m in s['new_mentions']:
 assert m['person_id'] is None;add(m['id'],'mention',{'record_id':m['record_id'],'name_literal':m['name_literal'],'role_literal':m['role']},m['caveat'],m['supports'])
req={'id':'T-0778/C1047-native-source-v1','actor':'Codex Sol exact settled implementation','reason':'T-0778 AC2–4: three bounded source groups,126 enumerated cells, four person adoptions and three unlinked source mentions.','dependencyReviewVersion':2,'changes':changes}
(P/'C1047-native-source-operation-v1.json').write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n');print(len(changes),'new objects assembled; source versions checked')
