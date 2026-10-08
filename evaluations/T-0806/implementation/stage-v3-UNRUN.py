import json,hashlib,shutil,subprocess,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0806/implementation';MAIN=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def cli(args,p):
 t=time.monotonic();r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);p.write_text(r.stdout);save(p.with_suffix('.process.json'),{'args':args,'exit':r.returncode,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t});assert r.returncode==0,(args,r.stderr);return json.loads(r.stdout)
def main():
 start=time.monotonic();b=json.load(open(D/'baseline-state-v1.json'));assert sha(MAIN)==b['main']['sha256'];assert sha(D/'baseline467.sqlite')==b['backup']['sha256'];op=json.load(open(D/'operation-v3.json'));table=json.load(open(D/'consequence-table-v3.json'));assert sha(D/'operation-v3.json')==table['operation_sha256'];base=h.conn(D/'baseline467.sqlite');assert h.state(base)=={'journal_head':467,'pending':0};stage=D/'stage468-v1';assert not stage.exists();stage.mkdir();db=stage/'stage.sqlite';shutil.copyfile(D/'baseline467.sqlite',db);journal=stage/'journal';journal.mkdir();save(stage/'baseline-all50.json',h.all50(base))
 try:
  cli(['apply',str(D/'operation-v3.json'),'--db',str(db),'--journal',str(journal)],stage/'apply.json');c=h.conn(db);state=h.state(c);assert state['journal_head']==468
  proof=[]
  for x in op['changes']:
   n=h.native(c,h.current(c,x['id']));actual=h.api(n);assert actual==h.expected_defaults(x,actual),x['id'];proof.append({'object_id':x['id'],'actual_native':n,'literal_api_exact':True})
  for x in table['retains']:assert h.native(c,x['revision_id'])==x['old_native'];assert h.current(c,x['old_native']['object_id'])==x['revision_id']
  save(stage/'literal-native-and-retains-proof.json',{'changes':proof,'retains_exact':len(table['retains'])});save(stage/'actual-all50.json',h.all50(c));save(stage/'actual-pending-full.json',[dict(x)for x in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')])
  for pid in ['P-0048','P-0287']:cli(['person',pid,'--db',str(db)],stage/(pid+'-person.json'))
  for pid in ['P-0269','P-0270']:cli(['pedigree',pid,'--db',str(db)],stage/(pid+'-pedigree.json'))
  cli(['inventory','--db',str(db)],stage/'inventory.json');cli(['verify','--db',str(db)],stage/'verify.json');assert sha(MAIN)==b['main']['sha256'];save(stage/'result.json',{'state':state,'main_unchanged':True,'literal81_exact':True,'retains236_exact':True,'elapsed_seconds':time.monotonic()-start})
 except Exception as e:save(stage/'failure-preserved.json',{'error':str(e),'elapsed_seconds':time.monotonic()-start});raise
if __name__=='__main__':main()
