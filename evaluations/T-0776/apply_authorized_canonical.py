import pathlib,json,sqlite3,hashlib,subprocess,datetime
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1];out=B/'canonical-apply';out.mkdir(exist_ok=True)
gate=json.loads((B/'root-controlled-apply-gate-v1.json').read_text());assert gate['approved']=='CONTROLLED_APPLY_EXACT_SEVEN_OPERATIONS';assert hashlib.sha256((B/'final-review/candidate-freeze-v1.json').read_bytes()).hexdigest()==gate['candidate_freeze_sha256']
def head():return max(int(p.name.split('-')[0]) for p in (R/'genealogy2/journal').glob('*.json'))
def pending():
 c=sqlite3.connect('file:'+str(R/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True)
 return c.execute('select count(*) from review_request q left join review_resolution r on q.id=r.request_id where r.request_id is null').fetchone()[0]
assert head()==248 and pending()==0
for i,row in enumerate(gate['operations']):
 assert head()==248+i;path=R/row['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256']
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(['node','genealogy2/cli.mjs','apply',str(path)],cwd=R,capture_output=True,text=True)
 receipt={'started_at_utc':started,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operation_path':row['path'],'operation_sha256':row['sha256'],'expected_head_before':248+i,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'head_after':head(),'pending_after':pending()}
 (out/f'{i+1:02d}-apply-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');assert p.returncode==0,receipt;assert head()==249+i;print('Applied',i+1,'head',head(),'pending',receipt['pending_after'],flush=True)
assert head()==255 and pending()==0
