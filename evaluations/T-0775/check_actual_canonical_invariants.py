import sqlite3,pathlib,json
B=pathlib.Path(__file__).resolve().parent
pre=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True);post=sqlite3.connect('file:'+str(B.parents[1]/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True)
for d in [pre,post]:d.row_factory=sqlite3.Row

def state(d,kind):
 return {r['object_id']:dict(r) for r in d.execute('select r.*,x.* from revision r join '+kind+' x on x.revision_id=r.id where r.version=(select max(version) from revision where object_id=r.object_id)')}
checks=[]
for kind in ['person','relation','identity','identity_resolution']:
 a=state(pre,kind);b=state(post,kind);diff=[oid for oid in a if a[oid]!=b.get(oid)];checks.append({'kind':kind,'preexisting_count':len(a),'changed':diff,'pass':not diff})
for label,filter_sql,args in [('native_gates',"x.criteria in ('identity_review/1','tree_effect/1','life_picture_review/1')",()),('legacy_reviews',"x.criteria='legacy_review_header'",())]:
 a={k:v for k,v in state(pre,'assessment').items() if pre.execute('select 1 from assessment x where x.revision_id=? and '+filter_sql,(v['id'],*args)).fetchone()};b=state(post,'assessment');diff=[oid for oid in a if a[oid]!=b.get(oid)];checks.append({'kind':label,'preexisting_count':len(a),'changed':diff,'pass':not diff})
a={r['object_id']:dict(r) for r in pre.execute("select * from revision r where evidence_status='OWNER_CONFIRMED' and version=(select max(version) from revision where object_id=r.object_id)")};diff=[]
for oid,v in a.items():
 now=post.execute('select * from revision where object_id=? order by version desc limit 1',(oid,)).fetchone()
 if dict(now)!=v:diff.append(oid)
checks.append({'kind':'OWNER_CONFIRMED_current_revisions','preexisting_count':len(a),'changed':diff,'pass':not diff})
out={'checks':checks,'all_pass':all(r['pass'] for r in checks),'post_journal':post.execute('select max(sequence) from operation_payload').fetchone()[0],'scope':'Exact preexisting person/relationship/identity/current native gates/owner-confirmed revision invariants; source and approved copy revisions intentionally excluded.'};(B/'canonical-apply/protected-invariants.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
