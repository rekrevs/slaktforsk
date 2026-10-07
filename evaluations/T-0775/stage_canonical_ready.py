import pathlib,json,hashlib,sqlite3,subprocess,datetime
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1];freeze=json.loads((B/'final-review/candidate-freeze-v1.json').read_text());dest=R/'genealogy2/operations';stage=B/'canonical-ready';stage.mkdir(exist_ok=True);rows=[]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for entry in freeze['operations_in_exact_apply_order']:
 oldp=pathlib.Path(entry['path']);raw=oldp.read_text();obj=json.loads(raw);oldreason=obj['reason'];newreason=oldreason
 if 'isolerad' in oldreason or 'isolerat' in oldreason:
  newreason='T-0775 AC2–4: kontrollerat kanoniskt införande efter självständig slutgranskning. '+oldreason
  for term in ['; endast isolerat pilotklon.','; isolerad pilotklon.','; endast isolerad klon.']:
   newreason=newreason.replace(term,'.')
  oldliteral=json.dumps(oldreason,ensure_ascii=False);newliteral=json.dumps(newreason,ensure_ascii=False);assert raw.count(oldliteral)==1;raw=raw.replace(oldliteral,newliteral,1)
 newobj=json.loads(raw);assert {k:v for k,v in obj.items() if k!='reason'}=={k:v for k,v in newobj.items() if k!='reason'}
 filename='T-0775-'+oldp.name.replace('-candidate-operation','-candidate').replace('-resolution-operation','-resolution').replace('-text-amendment-operation','-text-amendment').replace('independent-copy-amendment-operation','independent-copy-amendment');newp=dest/filename;assert not newp.exists();newp.write_text(raw)
 rows.append({'id':obj['id'],'before_path':str(oldp),'before_sha256':h(oldp),'staged_path':str(newp),'staged_sha256':h(newp),'reason_before':oldreason,'reason_after':newreason,'only_outer_reason_changed':oldreason!=newreason,'all_other_values_identical':True})
manifest={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorizing_root_instruction':'Stage canonical-ready copies, change only exclusive clone outer reason, preserve all other values and original freeze.','source_freeze_sha256':h(B/'final-review/candidate-freeze-v1.json'),'operations':rows,'canonical_applied':False};(stage/'metadata-amendment-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
db=stage/'research.sqlite';assert not db.exists();a=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True);o=sqlite3.connect(db);a.backup(o);o.close();a.close()
receipts=[]
for x in rows:
 cmd=['node','genealogy2/cli.mjs','apply',x['staged_path'],'--db',str(db),'--journal',str(stage/'journal')];run=subprocess.run(cmd,cwd=R,capture_output=True,text=True);receipt={'id':x['id'],'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr};receipts.append(receipt)
 if run.returncode:break
(stage/'replay-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n');print('Staged',len(rows),'outer reasons amended',sum(x['only_outer_reason_changed'] for x in rows),'replayed',len(receipts),'failures',sum(r['exit_code']!=0 for r in receipts))
