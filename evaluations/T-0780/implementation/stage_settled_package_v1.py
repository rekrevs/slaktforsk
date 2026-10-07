"""Sequential CLI stage of an explicitly settled, hash-bound package. Never canonical apply."""
import argparse,base64,datetime,hashlib,json,sqlite3,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];MAIN=ROOT/'genealogy2/data/research.sqlite'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def connection(p):
 c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
def canon(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True)
def scalar(x):return {'bytes_hex':x.hex()} if isinstance(x,bytes) else x
def table_state(c):
 out={}
 for r in c.execute("select name from sqlite_master where type='table' order by name"):
  n=r[0];rows=[{k:scalar(v) for k,v in dict(z).items()} for z in c.execute('select * from "'+n+'"')];rows.sort(key=canon);out[n]={'rows':len(rows),'sha256':hashlib.sha256(canon(rows).encode()).hexdigest()}
 return out
def protection(c):
 return [dict(r) for r in c.execute("select r.*,a.criteria,a.outcome,a.body from revision r left join assessment a on a.revision_id=r.id where not exists(select1 from revision n where n.object_id=r.object_id and n.version>r.version) and (r.evidence_status='OWNER_CONFIRMED' or a.criteria in ('identity_review/1','tree_effect/1','life_picture_review/1')) order by r.object_id".replace('select1','select 1'))]
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def run(args,p):
 proc=subprocess.run(['node',str(ROOT/'genealogy2/cli.mjs'),*args],cwd=ROOT,capture_output=True,text=True);p.write_text(proc.stdout);p.with_suffix('.stderr.txt').write_text(proc.stderr);assert proc.returncode==0,f'{args}: {proc.stderr}';return json.loads(proc.stdout)
def main():
 p=argparse.ArgumentParser();p.add_argument('--gate',type=Path,required=True);p.add_argument('--new-stage',type=Path,required=True);a=p.parse_args();gate=json.load(open(a.gate));assert gate['status']=='settled_primary_package_ready_for_stage';assert gate['canonical_apply_authorized'] is False
 stage=a.new_stage.resolve();assert not stage.exists(),'Fresh stage required; prior attempts must be preserved';assert stage!=MAIN and MAIN not in stage.parents
 assert (ROOT/'evaluations/T-0780') in stage.parents,'Stage must remain inside this task evaluation directory'
 pins=gate['operations'];assert pins,'No implicit or empty package';ops=[]
 for pin in pins:
  path=(ROOT/pin['path']).resolve();assert digest(path)==pin['sha256'];op=json.load(open(path));assert op['dependencyReviewVersion']==2;ops.append((path,op))
 live=connection(MAIN);baseline=table_state(live);assert live.execute('select max(sequence) from operation_payload').fetchone()[0]==gate['baseline_journal'];assert live.execute('select count(*) from review_request r left join review_resolution s on r.id=s.request_id where s.request_id is null').fetchone()[0]==gate['baseline_pending'];protected=protection(live)
 stage.mkdir(parents=True);dbp=stage/'stage.sqlite';dest=sqlite3.connect(dbp);live.backup(dest);dest.close();check=connection(dbp);assert table_state(check)==baseline;check.close();write(stage/'baseline-all-table-state.json',baseline);write(stage/'protected-before.json',protected);write(stage/'package-gate.json',gate)
 journal=stage/'journal';journal.mkdir()
 for i,(path,op) in enumerate(ops,1):
  # Execute immutable exact file; no changes, sorting, generic resolutions or substituted versions.
  run(['apply',str(path),'--db',str(dbp),'--journal',str(journal)],stage/f'step-{i:03}-apply.json')
 staged=connection(dbp);assert staged.execute('select count(*) from review_request r left join review_resolution s on r.id=s.request_id where s.request_id is null').fetchone()[0]==gate['expected_pending_after'];assert protection(staged)==protected,'Protected knowledge/review state changed';write(stage/'protected-after.json',protection(staged));write(stage/'all-operation-payloads.json',[dict(r) for r in staged.execute('select * from operation_payload order by sequence')]);write(stage/'pending-after.json',[dict(r) for r in staged.execute('select r.* from review_request r left join review_resolution s on r.id=s.request_id where s.request_id is null')]);staged.close()
 for cmd in ['verify','verify-assets','verify-source','inventory']:
  run([cmd,'--db',str(dbp),'--journal',str(journal)],stage/(cmd+'.json'))
 run(['pedigree','P-0269','--db',str(dbp)],stage/'pedigree-verified-P0269.json');assert table_state(live)==baseline,'Live baseline changed during stage';write(stage/'stage-result.json',{'stage_only':True,'canonical_untouched':True,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operations':pins,'gate_sha256':digest(a.gate),'protected_unchanged':True,'no_silent_rebinding_or_resolutions':True});live.close()
if __name__=='__main__':main()
