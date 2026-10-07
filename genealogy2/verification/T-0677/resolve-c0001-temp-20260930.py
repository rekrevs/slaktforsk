import json,hashlib,sqlite3,subprocess,datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
p=Path(__file__).resolve().parent
spec=json.loads((p/'c0001-settled-request-decisions-20260930.json').read_text())
assert hashlib.sha256((p/'c0001-temp-pending-full-20260930.json').read_bytes()).hexdigest()==spec['pending_input_sha256']
summary=json.loads((p/'c0001-temp-preflight-summary-20260930.json').read_text());dbpath=Path(summary['temp_database'])
op={'id':spec['operation_id'],'actor':'Codex Sol implementation of individual Astra retain decisions','reason':'T-0677 AC3: åtta faktiska beroendeomprövningar avgjorda individuellt.','dependencyReviewVersion':2,'changes':[],'resolve':[{'request':d['request'],'rationale':d['rationale']} for d in spec['decisions']]}
f=p/'c0001-resolutions-proposed-operation-20260930.json';assert not f.exists();f.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
def run(args):
 cmd=['node','genealogy2/cli.mjs']+args+['--db',str(dbpath),'--journal',str(dbpath.parent/'journal')];r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,(cmd,r.stderr,r.stdout);return {'command':cmd,'exit':r.returncode,'payload':json.loads(r.stdout)}
apply=run(['apply',str(f)])
db=sqlite3.connect(f'file:{dbpath}?mode=ro',uri=True);db.row_factory=sqlite3.Row
actual=[dict(r) for r in db.execute('select * from review_resolution where operation_id=? order by request_id',(op['id'],))]
expected=sorted([{'request_id':r['request'],'operation_id':op['id'],'rationale':r['rationale']} for r in op['resolve']],key=lambda r:r['request_id']);assert actual==expected
pending=[dict(r) for r in db.execute('select * from pending_review')];assert not pending
with ThreadPoolExecutor(max_workers=3) as pool: checks=dict(zip(['verify','verify-assets','verify-source'],pool.map(lambda c:run([c]),['verify','verify-assets','verify-source'])))
result={'task':'T-0677','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'TEMP_RESOLUTIONS_ONLY_AWAITING_ASTRA_APPROVAL','operation_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'apply':apply,'actual_resolutions':actual,'all_exact':True,'pending':pending,'checks':checks}
(p/'c0001-temp-resolutions-receipt-20260930.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print({'resolutions':len(actual),'pending':len(pending),'sha256':result['operation_sha256'],'validators':'PASS'})
