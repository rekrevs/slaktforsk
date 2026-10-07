import sqlite3,json,pathlib,re,hashlib
b=pathlib.Path('evaluations/T-0790');p=b/'preparation/reviewed-stage-v1/stage.sqlite';c=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
people=['P-0004','P-0210','P-0005','P-0006','P-0211','P-0212'];patterns={'birthplace_inference':r'Stockholmstrakten|Stockholmstrakts|förlossnings|hemresa','baptism_exclusion':r'aldrig.*döpt|ingen dopnotis|dopnotis.*kan skilja|livslång.*dop','catalogue_exhaustion':r'utanför NAD|samtliga utanför|samtliga serier kräver|ingen lärarmatrikel efter|är analoga|enda nätåtkomliga|främst i icke-digitala','readingstatus':r'column9|kolumn.?9|personaktsnum','maternal_sibling':r'A-0238|moderskap|äldre systr|tre syskon','privacy_paths':r'T-?0034|birthday|obligatoriska.*passage'}
heads=[dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.version=(select max(x.version) from revision x where x.object_id=r.object_id)')];hits=[];scoped=0
for r in heads:
 data=c.execute('select * from "'+r['kind']+'" where revision_id=?',(r['id'],)).fetchone()
 if data is None:continue
 data=dict(data);txt=json.dumps(data,ensure_ascii=False)+' '+r['caveat'];
 if not any(p in txt or p in r['object_id'] for p in people):continue
 scoped+=1;which=[k for k,v in patterns.items() if re.search(v,txt,re.I)]
 if not which:continue
 hits.append({'revision':r['id'],'kind':r['kind'],'matches':which,'data':data,'caveat':r['caveat'],'rationale':r['rationale']})
 print(r['id'],which, ' | '.join(m.group(0) for m in re.finditer(r'.{0,35}(?:Stockholmstrakten|aldrig.*?döpt|ingen dopnotis|utanför NAD|samtliga utanför|samtliga serier kräver|ingen lärarmatrikel efter|är analoga|enda nätåtkomliga|främst i icke-digitala|äldre systr|A-0238).{0,100}',txt))[:500])
out={'stage_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'independent_search_scope':'All current native head data+caveats mentioning six Pids or their objectids; includes semantic copies beyond operation list. Pattern hits are candidates, not current errors. Earlier full readings reused for unchanged objects.','scoped_current_objects':scoped,'patterns':patterns,'candidates':hits};(b/'independent-review/final-stage-semantic-candidates-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('SCOPED',scoped,'HITS',len(hits))
