"""Prepared template only. Run after exact candidate/source approval and clean preflight. No live writes."""
import json,sqlite3,hashlib,subprocess,os,time
from pathlib import Path
import sys
R=Path.cwd();D=R/'evaluations/T-0830/implementation';operation=Path(sys.argv[1]).resolve();media_plan=Path(sys.argv[2]).resolve();S=D/sys.argv[3];assert not S.exists();S.mkdir();src=S/'source';(src/'genealogy2/media/objects').mkdir(parents=True);(src/'genealogy').mkdir()
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();main=R/'genealogy2/data/research.sqlite';before=H(main);assert before=='64a1f5ef205c7b6588abce7a0adfb9ec7a65a25963524fde38928b3abbe66e93';base=sqlite3.connect('file:'+str(main)+'?mode=ro',uri=True);base.row_factory=sqlite3.Row;assert base.execute('select max(sequence)from operation_payload').fetchone()[0]==505;assert base.execute('select count(*)from pending_review').fetchone()[0]==0
clone=S/'stage.sqlite';cc=sqlite3.connect(clone);base.backup(cc);cc.close()
for a in base.execute('SELECT storage_path FROM native_asset UNION SELECT path FROM asset'):
 dest=src/a[0];dest.parent.mkdir(parents=True,exist_ok=True);os.link(R/a[0],dest)
def run(args,name):
 p=subprocess.run(args,capture_output=True,text=True);(S/(name+'.stdout')).write_text(p.stdout);(S/(name+'.stderr')).write_text(p.stderr);assert p.returncode==0,(name,p.stderr);return json.loads(p.stdout)
receipts=[]
for i,u in enumerate(json.load(open(media_plan))):
 m=u['planned'];got=run(['node','genealogy2/cli.mjs','stage-media',u['input'],'--source',str(src),'--provenance',m['provenance']],'media-'+str(i+1));assert got==m;receipts.append(got)
(S/'media-stage-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
result=run(['node','genealogy2/cli.mjs','apply',str(operation),'--db',str(clone),'--source',str(src),'--journal',str(S/'journal')],'apply')
c=sqlite3.connect(clone);c.row_factory=sqlite3.Row;pending=[dict(e)for e in c.execute('SELECT *FROM pending_review ORDER BY id')];(S/'pending-requests.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2)+'\n');assert H(main)==before
proof={'operation_sha256':H(operation),'main_sha256_before':before,'main_unchanged':True,'journal_after':c.execute('select max(sequence)from operation_payload').fetchone()[0],'pending_after':len(pending),'media_exact':len(receipts),'apply':result};(S/'initial-stage-proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps(proof))
