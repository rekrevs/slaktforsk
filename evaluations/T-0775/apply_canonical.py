import pathlib,json,sqlite3,subprocess,hashlib,datetime
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1];C=B/'canonical-apply';C.mkdir(exist_ok=True)
freeze_path=B/'canonical-ready/stage-freeze-v1.json';freeze=json.loads(freeze_path.read_text());assert hashlib.sha256(freeze_path.read_bytes()).hexdigest()=='1fd013eb97e24f4f289c53f365ee748ccfb6a90f777f2939ebd6511d46729d52'
def status():
 c=sqlite3.connect('file:'+str(R/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True);j=c.execute('select max(sequence) from operation_payload').fetchone()[0];pending=c.execute('select count(*) from review_request q left join review_resolution r on q.id=r.request_id where r.request_id is null').fetchone()[0];c.close();return {'journal':j,'pending':pending}
assert status()=={'journal':237,'pending':0},status()
receipts=[]
for i,entry in enumerate(freeze['operations']):
 p=pathlib.Path(entry['staged_path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['staged_sha256'];before=status();assert before['journal']==237+i,before
 run=subprocess.run(['node','genealogy2/cli.mjs','apply',str(p)],cwd=R,capture_output=True,text=True);after=status();receipt={'operation':entry['id'],'path':str(p),'sha256':entry['staged_sha256'],'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before':before,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'after':after};(C/(str(i+1).zfill(2)+'-receipt.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');receipts.append(receipt)
 assert run.returncode==0 and after['journal']==238+i,receipt
(C/'receipts.json').write_text(json.dumps({'stage_freeze_sha256':hashlib.sha256(freeze_path.read_bytes()).hexdigest(),'receipts':receipts,'final':status()},ensure_ascii=False,indent=2)+'\n');assert status()=={'journal':248,'pending':0};print('Canonical11operationsAPPLIED,j248,pending0')
