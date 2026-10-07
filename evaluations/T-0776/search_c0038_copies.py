import sqlite3,json,pathlib,datetime
B=pathlib.Path(__file__).resolve().parent;c=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
terms=['tjenstf','tjänstf','2:2','609','civilstatus'];hits=[]
for r in c.execute('select * from current_revision'):
 d=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone());rev=dict(r);f={k:v for k,v in {**d,**rev}.items() if isinstance(v,str) and any(t in v.lower() for t in terms)}
 if not f:continue
 if all(not any(t in v.lower() for t in terms[:-1]) for v in f.values()) and not ('C0038' in r['object_id'] or 'C-0038' in str(d)):continue
 ev=[dict(v) for v in c.execute('select * from dependency where revision_id=?',(r['id'],))];orig=[dict(v) for v in c.execute('select * from origin where revision_id=?',(r['id'],))]
 hits.append({'id':r['object_id'],'version':rev['version'],'kind':r['kind'],'full_matched_fields':f,'full_data':d,'full_revision':rev,'evidence':ev,'origins':orig,'disposition':None})
p=B/'C-0038-global-exact-copy-input-v1.json';p.write_text(json.dumps({'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_journal':248,'terms':terms,'rows':hits,'truncated':False,'scope':'Mechanical global current native search; substring hits do not establish relevance.'},ensure_ascii=False,indent=2)+'\n');print(len(hits),'full current hits')
