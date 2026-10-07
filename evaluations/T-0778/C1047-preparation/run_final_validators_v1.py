import pathlib,subprocess,json,concurrent.futures
P=pathlib.Path(__file__).resolve().parent;R=P.parents[2];db=P/'clone/c1047-final-v3.sqlite'
def run(cmd):
 r=subprocess.run(['node','genealogy2/cli.mjs',cmd,'--db',str(db)],cwd=R,capture_output=True,text=True);v={'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'stage':str(db.relative_to(R))};(P/('C1047-final-v3-'+cmd+'-receipt-v1.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(cmd,r.returncode,flush=True);assert r.returncode==0
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,['verify','verify-assets','verify-source']))
