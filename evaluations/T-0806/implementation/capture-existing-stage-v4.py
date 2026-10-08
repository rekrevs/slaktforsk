import json,hashlib,shutil,subprocess,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0806/implementation';MAIN=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def cli(args,p):
 t=time.monotonic();r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);p.write_text(r.stdout);save(p.with_suffix('.process.json'),{'args':args,'exit':r.returncode,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t});assert r.returncode==0,(args,r.stderr);return json.loads(r.stdout)
def main():
 stage=D/'stage468-v2';db=stage/'stage.sqlite';c=h.conn(db);assert h.state(c)=={'journal_head':468,'pending':0}
 for pid in ['P-0048','P-0287']:cli(['person',pid,'--format','json','--db',str(db)],stage/(pid+'-person-final.json'))
 for pid in ['P-0269','P-0270']:cli(['pedigree',pid,'--db',str(db)],stage/(pid+'-pedigree.json'))
 cli(['inventory','--db',str(db)],stage/'inventory.json');cli(['verify','--db',str(db)],stage/'verify.json');save(stage/'capture-complete.json',{'state':h.state(c),'apply_not_repeated':True,'json_formatter_correction_only':True})
if __name__=='__main__':main()
