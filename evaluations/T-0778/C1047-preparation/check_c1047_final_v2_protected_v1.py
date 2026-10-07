import pathlib,json,sqlite3
B=pathlib.Path(__file__).resolve().parent
base=sqlite3.connect(B/'clone/research-pre.sqlite');stage=sqlite3.connect(B/'clone/c1047-final-v2.sqlite')
checks={}
for table in ['person','identity','relation','participation']:
 # existing append-only domain rows must persist byte for byte; person correction adds one new revision.
 old=base.execute('select * from '+table).fetchall();new=set(stage.execute('select * from '+table).fetchall());checks[table+'_all_historical_rows_preserved']=all(r in new for r in old)
checks['person_revision_count_delta']=stage.execute('select count(*) from person').fetchone()[0]-base.execute('select count(*) from person').fetchone()[0]
checks['identity_revision_count_equal']=stage.execute('select count(*) from identity').fetchone()[0]==base.execute('select count(*) from identity').fetchone()[0]
checks['relation_revision_count_equal']=stage.execute('select count(*) from relation').fetchone()[0]==base.execute('select count(*) from relation').fetchone()[0]
for dbname,db in [('baseline',base),('stage',stage)]:
 checks[dbname+'_owner_confirmed_count']=db.execute("select count(*) from current_revision where evidence_status='OWNER_CONFIRMED'").fetchone()[0]
checks['owner_confirmed_count_equal']=checks['baseline_owner_confirmed_count']==checks['stage_owner_confirmed_count']
checks['pass']=all(v for k,v in checks.items() if k.endswith('preserved') or k.endswith('equal')) and checks['person_revision_count_delta']==0
(B/'C1047-final-v2-protected-invariants-v1.json').write_text(json.dumps(checks,indent=2)+'\n');print(checks);assert checks['pass']
