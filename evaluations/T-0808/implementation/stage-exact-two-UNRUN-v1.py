import json,hashlib,shutil,subprocess,importlib.util,time,traceback
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0808';I=D/'implementation';MAIN=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def cli(args,p):
 t=time.monotonic();r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);p.write_text(r.stdout);save(p.with_suffix('.process.json'),{'args':args,'exit':r.returncode,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t});assert r.returncode==0,r.stderr;return json.loads(r.stdout)
def main():
 start=time.monotonic();b=json.load(open(D/'preparation/baseline-state-v1.json'));assert sha(MAIN)==b['main']['sha256'];basepath=R/b['backup']['path'];assert sha(basepath)==b['backup']['sha256'];base=h.conn(basepath);assert h.state(base)=={'journal_head':469,'pending':0};S=I/'stage471-sequence-v1';assert not S.exists();S.mkdir();db=S/'stage.sqlite';shutil.copyfile(basepath,db);journal=S/'journal';journal.mkdir();save(S/'baseline-all50.json',h.all50(base));proof=[]
 try:
  for index,(name,tablefile,opsha,ctsha)in enumerate([('operation-v2.json','consequence-table-v2.json','d717b88acc0db1d98ef6b0efab8a19ad0ee14027bedf9ffcb338c80959512bad','4b7eb0a74818154273dfabf04990b4ee05064a9400ce3a59630699770773ac44'),('repair-operation-v2.json','repair-consequence-table-v2.json','90de4d5eef42ba1b1a08a1235841d3e0af8b84678878c1effabc5edf0ca12189','8a3cc51159e316555068aa8891ea81034312b708dab85b883ced582f0b3b319e')],1):
   opath=I/name;assert sha(opath)==opsha and sha(I/tablefile)==ctsha;op=json.load(open(opath));table=json.load(open(I/tablefile));assert table['operation_sha256']==opsha;c=h.conn(db)
   for t in table['changes']:
    if t['old_native']is not None:assert h.native(c,h.current(c,t['object_id']))==t['old_native'],t['object_id']
   c.close();cli(['apply',str(opath),'--db',str(db),'--journal',str(journal)],S/f'apply-{index}.json');c=h.conn(db);state=h.state(c);assert state['journal_head']==469+index
   accepted=dict(c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone());assert json.loads(accepted['request_json'])==op
   literal=[]
   for x in op['changes']:
    n=h.native(c,h.current(c,x['id']));actual=h.api(n);assert actual==h.expected_defaults(x,actual),x['id'];literal.append({'object_id':x['id'],'actual_native':n,'literal_api_exact':True})
   for t in table['retains']:assert h.native(c,t['revision_id'])==t['old_native'];assert h.current(c,t['old_native']['object_id'])==t['revision_id']
   pending=[dict(x)for x in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];save(S/f'after-{index}-native-proof.json',{'state':state,'literal':literal,'retains_exact':len(table['retains']),'accepted':accepted});save(S/f'after-{index}-pending-full.json',pending);proof.append({'step':index,'state':state,'changes':len(literal),'retains':len(table['retains'])});c.close()
  for pid in ['P-0242','P-0243','P-0312','P-0313']:cli(['person',pid,'--full','--format','json','--db',str(db)],S/(pid+'-person.json'))
  for pid in ['P-0269','P-0270']:cli(['pedigree',pid,'--db',str(db)],S/(pid+'-pedigree.json'))
  cli(['inventory','--db',str(db)],S/'inventory.json');cli(['verify','--db',str(db)],S/'verify.json');c=h.conn(db);save(S/'actual-all50.json',h.all50(c));assert sha(MAIN)==b['main']['sha256'];save(S/'result.json',{'steps':proof,'state':h.state(c),'main_unchanged':True,'exact_sequence_tested':True,'elapsed_seconds':time.monotonic()-start})
 except Exception as e:save(S/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.monotonic()-start});raise
if __name__=='__main__':main()
