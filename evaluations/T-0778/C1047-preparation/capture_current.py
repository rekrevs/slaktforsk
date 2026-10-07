import json,pathlib,re,subprocess,concurrent.futures,hashlib,sqlite3
B=pathlib.Path(__file__).resolve().parent;R=B.parents[2]
selection=json.loads((B/'selection.json').read_text()); ids=set(); people=set(); case={}
for card in selection['cards']:
 impact=json.loads((B/(card['citation']+'-impact.json')).read_text()); ci={x['object_id'] for x in impact['review']['items']}; ids.update(ci)
 ps=set()
 for oid in ci:ps.update(re.findall(r'P-\d{4}',oid))
 ps.update(card['person_ids_from_current_identity_links'])
 case[card['citation']]={'impact_objects':sorted(ci),'person_routes':sorted(ps),'person_route_basis':'identifier text in impact metadata; candidate route only, not source judgement'};people.update(ps)
(B/'current').mkdir(exist_ok=True)
def run(item):
 typ,oid,args=item
 p=B/'current'/(typ+'-'+oid.replace('/','__')+'.json');r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,text=True,capture_output=True)
 if r.returncode:raise RuntimeError((oid,r.stderr))
 d=json.loads(r.stdout);p.write_text(r.stdout);return {'id':oid,'view':typ,'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'version':d.get('currentVersion'),'truncated':False}
items=[('inspect',oid,['inspect',oid]) for oid in sorted(ids|people)]+[('person-full',p,['person',p,'--full','--format','json']) for p in sorted(people)]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:captures=list(e.map(run,items))
c=sqlite3.connect('file:'+str(R/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
# Full current searchable text for affected person contexts and impact objects. No global corpus dump.
rows=[]
for row in c.execute('select object_id,kind,text from object_search'):
 if row['object_id'] in ids or any(p in row['object_id'] for p in people):rows.append(dict(row))
(B/'semantic-copy-search-input.json').write_text(json.dumps({'scope':'current object_search complete texts for candidate person routes and impact objects','rows':rows,'truncated':False,'limitation':'Independent Astra search must additionally query outside this routed input; no claim of semantic exhaustiveness.'},ensure_ascii=False,indent=2)+'\n')
(B/'current-manifest.json').write_text(json.dumps({'cases':case,'captures':captures,'count':len(captures),'journal':c.execute('select max(sequence) from operation_payload').fetchone()[0],'pending':c.execute('select count(*) from review_request q left join review_resolution r on q.id=r.request_id where r.request_id is null').fetchone()[0],'field_truncation':False,'source_images_opened':False},ensure_ascii=False,indent=2)+'\n')
print('Captured',len(captures),'views for',len(people),'routed persons;',len(rows),'complete search rows')
