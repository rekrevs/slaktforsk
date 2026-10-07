import datetime,hashlib,importlib.util,json,sqlite3,time
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0804/preparation';M=R/'genealogy2/data/research.sqlite';B=D/'baseline464.sqlite';start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();assert not B.exists()
lib=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';s=importlib.util.spec_from_file_location('h',lib);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
c=h.conn(M);assert h.state(c)=={'journal_head':464,'pending':0};b=sqlite3.connect(B);c.backup(b);b.close();cb=h.conn(B);assert h.all50(c)==h.all50(cb)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out={'task':'T-0804','started':start,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'main':{'path':str(M.relative_to(R)),'sha256':sha(M)},'backup':{'path':str(B.relative_to(R)),'sha256':sha(B)},'state':h.state(c),'all50':h.all50(c),'no_canonical_change':True,'helper_pin':{'path':str(lib.relative_to(R)),'sha256':sha(lib)}}
(D/'baseline-state-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'state':out['state'],'elapsed':out['elapsed_seconds']}));c.close();cb.close()
