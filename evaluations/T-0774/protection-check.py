"""Check exact original protection scope; never alter protected files."""
from pathlib import Path
import datetime,hashlib,json,sys
h=Path(__file__).resolve().parent
entries=json.loads((h/'protected-before.json').read_text())
expected={e['path'] for e in entries}
actual=set()
for directory in ('evaluations/T-0773','genealogy2/journal','genealogy2/operations'):
    actual.update(str(p) for p in Path(directory).rglob('*') if p.is_file())
actual.update(str(p) for p in Path('genealogy2/verification/T-0677').glob('*') if p.is_file() and p.suffix in ('.json','.py','.sha256'))
actual.update(str(p) for p in Path('genealogy2/data').glob('research.sqlite*') if p.is_file())
def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
failed=[e['path'] for e in entries if not Path(e['path']).is_file() or digest(e['path'])!=e['sha256']]
locks=[]
for filename in ('first-source-locks.json',):
    for e in json.loads((h/filename).read_text())['files']:
        locks.append({'path':e['path'],'match':Path(e['path']).is_file() and digest(e['path'])==e['sha256']})
baseline=json.loads((h/'baseline-lock.json').read_text())
source_locks=[{'path':c['image'],'match':digest(c['image'])==c['sha256']}
              for c in json.loads((h/'source-input/cases.json').read_text())]
protocol_match=digest(h/'protocol-v1.md')==json.loads((h/'protocol-lock-v1.json').read_text())['protocol_sha256']
r={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'protected_count':len(entries),'hash_mismatches':failed,'added':sorted(actual-expected),'missing':sorted(expected-actual),'first_source_locks':locks,'baseline_match':digest(baseline['database'])==baseline['sha256'],'scope':'Exact original selection: T-0677 verification direct json/py/sha256 files; canonical DB/operations/journal; all T-0773 files.'}
r['source_locks']=source_locks
r['protocol_match']=protocol_match
r['state']='PASS' if not any(r[k] for k in ('hash_mismatches','added','missing')) and all(x['match'] for x in locks+source_locks) and r['baseline_match'] and protocol_match else 'FAILED'
p=h/(sys.argv[1] if len(sys.argv)>1 else 'protection-final.json');p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'state':r['state'],'protected':len(entries),'first_locks':len(locks),'receipt':str(p)}))
