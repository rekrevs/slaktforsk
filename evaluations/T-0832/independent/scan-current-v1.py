import sqlite3,json,re,pathlib,hashlib
out=pathlib.Path('evaluations/T-0832/independent')
c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
heads=[dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.version=(select max(r2.version) from revision r2 where r2.object_id=r.object_id)')]
pat=re.compile(r'P-0272|Anna\s*Stina\s*(?:Strand|Ström)|C-?0?(?:456|457|658)\b|C0033072_00137|C0033073_00133|A0036201_00112|R-b3e23944|R-cb27515d|R-237a94ab',re.I)
found=[]
for r in heads:
 data=[dict(x) for x in c.execute('select * from "'+r['kind']+'" where revision_id=?',(r['id'],))]
 s=json.dumps([r,data],ensure_ascii=False)
 if not pat.search(s):continue
 x={'revision':r,'data':data,'evidence':[dict(z) for z in c.execute('select * from dependency where revision_id=?',(r['id'],))],'origins':[dict(z) for z in c.execute('select * from origin where revision_id=?',(r['id'],))]}
 if r['kind']=='record':
  x['assets']=[dict(z) for z in c.execute('select * from record_asset where revision_id=?',(r['id'],))];x['media']=[dict(z) for z in c.execute('select * from record_media where revision_id=?',(r['id'],))]
 found.append(x)
(out/'independent-semantic-scan-full-v1.json').write_text(json.dumps({'query':pat.pattern,'current_count':len(heads),'matches':found},ensure_ascii=False,indent=2)+'\n')
# Same literal caveat repeated remains exact in full native export; present once for human review plus all ids.
caveats={}
for x in found:caveats.setdefault(x['revision']['caveat'],[]).append(x['revision']['id'])
(out/'independent-semantic-caveats-v1.json').write_text(json.dumps(caveats,ensure_ascii=False,indent=2)+'\n')
for n in range(0,len(found),25):
 a=[]
 for x in found[n:n+25]:
  a.append({'id':x['revision']['id'],'status':x['revision']['evidence_status'],'rationale':x['revision']['rationale'],'data':x['data']})
 (out/f'semantic-full-{n//25}.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
print({'heads':len(heads),'matches':len(found),'distinct_caveats':len(caveats),'blocks':(len(found)+24)//25})
