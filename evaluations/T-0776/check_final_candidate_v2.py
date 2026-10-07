import json,pathlib,sqlite3,subprocess,hashlib,concurrent.futures
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1];db=B/'clone/research-final-candidate-v2.sqlite';c=sqlite3.connect('file:'+str(db)+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
op_paths=['C-0037-candidate-operation-v2.json','C-0038-candidate-operation-v1.json','C-0083-initial-candidate-operation-v1.json','independent-IF2-IF3-operation-v1.json','C-0083-consequence-amendment-operation-v1.json','C-0083-final-participation-operation-v2.json'];latest={}
for path in op_paths:
 for change in json.loads((B/path).read_text())['changes']:latest[change['id']]=change
op={'changes':list(latest.values())};checks=[]
def norm(x):
 if isinstance(x,dict):return {k:norm(v) for k,v in x.items()}
 if isinstance(x,list):return sorted((norm(v) for v in x),key=lambda v:json.dumps(v,sort_keys=True))
 return x
for x in op['changes']:
 rev=dict(c.execute('select * from revision where object_id=? order by version desc limit 1',(x['id'],)).fetchone());data=dict(c.execute('select * from '+x['kind']+' where revision_id=?',(rev['id'],)).fetchone());data.pop('revision_id')
 for k,v in data.items():
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 ev=[{'object':r['basis_revision_id'].rsplit('@',1)[0],'version':int(r['basis_revision_id'].rsplit('@',1)[1]),'role':r['role'],'note':r['note']} for r in c.execute('select * from dependency where revision_id=?',(rev['id'],))]
 origins=[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in c.execute('select * from origin where revision_id=?',(rev['id'],))]
 expected={'data':x['data'],'evidence':x.get('evidence',[]),'origins':x.get('origins',[]),'disposition':x['disposition'],'evidenceStatus':x.get('evidenceStatus'),'rationale':x['rationale'],'caveat':x.get('caveat',''),'version':(x['expectedVersion'] or 0)+1}
 actual={'data':data,'evidence':ev,'origins':origins,'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],'rationale':rev['rationale'],'caveat':rev['caveat'],'version':rev['version']}
 matches={k:(norm(expected[k])==norm(actual[k]) if k in ('evidence','origins') else expected[k]==actual[k]) for k in expected};checks.append({'id':x['id'],'pass':all(matches.values()),'field_matches':matches,'expected':expected,'actual':actual})
pending=[dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on q.id=r.request_id where r.request_id is null')]
(B/'final-full-object-match-v2.json').write_text(json.dumps({'checks':checks,'all_pass':all(x['pass'] for x in checks),'pending':pending},ensure_ascii=False,indent=2)+'\n');print('Full objects matched',sum(x['pass'] for x in checks),'/',len(checks),'pending',len(pending))
def run(cmd):
 r=subprocess.run(['node','genealogy2/cli.mjs',cmd,'--db',str(db)],cwd=R,capture_output=True,text=True);p=B/('final-candidate-'+cmd+'-v2.json');p.write_text(json.dumps({'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr},ensure_ascii=False,indent=2)+'\n');return cmd,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:print('Checks',list(e.map(run,['verify','verify-assets','verify-source'])))
