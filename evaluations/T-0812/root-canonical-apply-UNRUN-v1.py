import pathlib,hashlib,json,sqlite3,subprocess,time
R=pathlib.Path.cwd();D=R/'evaluations/T-0812';I=D/'implementation';db=R/'genealogy2/data/research.sqlite'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def state():
 with sqlite3.connect(db.resolve().as_uri()+'?mode=ro',uri=True) as c:
  return {'journal_head':c.execute('select max(sequence) from operation_payload').fetchone()[0],'pending':c.execute('select count(*) from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null').fetchone()[0]}
def save(p,v):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 authorization=json.load(open(D/'root-canonical-authorization-v1.json'));assert authorization['root_authorized'] is True
 for pin in authorization['pins']:
  assert sha(R/pin['path'])==pin['sha256'],pin
 assert sha(db)=='337a4a112456e5f1a745cd831c9431b97db044b88f658035a065f243bc40e98f'
 assert state()=={'journal_head':477,'pending':0}
 ops=[('operation-v1.json','f4c93141988777743cd4dfc56ce26acd84cb8c14c98a52ae944197f602972914',134),('repair-operation-v1.json','0821e87eb610b6e869b3cb820e1a9b9037fb6e57436f01e72c2cc72df0c2bd9f',2),('two-resolution-operation-v1.json','fe6ac43d9de5bf9d57ce104d81321ffe76f775b0129efd37c015f3e3f10bf8fd',0),('person-caveat-operation-v1.json','140a21618c672b5c8a0acc8c20de5b2f05ab085a085d966472bd6d0d13b09673',0)]
 for ix,(name,pin,remaining) in enumerate(ops,1):
  path=I/name;assert sha(path)==pin
  before=state();assert before['journal_head']==476+ix
  save(D/f'root-actual-before-{ix}-v1.json',before)
  args=['node','genealogy2/cli.mjs','apply',str(path)];start=time.monotonic();result=subprocess.run(args,cwd=R,capture_output=True,text=True)
  output=D/f'root-actual-apply-{ix}-v1.json';assert not output.exists();output.write_text(result.stdout)
  after=state();save(D/f'root-actual-apply-{ix}-v1.process.json',{'args':args,'exit':result.returncode,'stderr':result.stderr,'elapsed_seconds':time.monotonic()-start,'before':before,'after':after})
  assert result.returncode==0,result.stderr
  assert after=={'journal_head':477+ix,'pending':remaining},after
  print(json.dumps({'step':ix,'actual_state':after}),flush=True)
 save(D/'root-actual-stage-v1.json',{'state':state(),'supported_sequential_cli_only':True,'operation_count':4,'no_database_replacement':True})
if __name__=='__main__':main()
