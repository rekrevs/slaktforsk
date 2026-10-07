"""UNRUN draft. One literal root-authorized stage; no canonical or resolve path.
Root audits and pins this code BEFORE calling main. Source APIs/retains supplied.
"""
import argparse,datetime,hashlib,importlib.util,json,shutil,sqlite3,subprocess,time,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3];TASK=R/'evaluations/T-0792';MAIN=R/'genealogy2/data/research.sqlite'
LIB=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py'
LIB_SHA='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2'
PEOPLE={'P-0241','P-0246','P-0239','P-0240'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def loadpin(p):
 q=(R/p['path']).resolve();assert q.is_relative_to(R) and sha(q)==p['sha256'];return q,json.loads(q.read_text())
def save(p,v):
 assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def at(v,p):
 for k in p.strip('/').split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
def native(h,c,rid):
 n=h.native(c,rid)
 # Explicit fix: older helper conditional omits these arrays for nonrecords.
 for k,t in [('origins','origin'),('evidence','dependency')]:n[k]=[dict(x) for x in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
def cli(args,p):
 r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True)
 save(p.with_suffix('.process.json'),{'args':args,'returncode':r.returncode,'stderr':r.stderr});p.write_text(r.stdout)
 assert r.returncode==0,('Stop; preserve actual stage; no retry',args,r.stderr)
 return json.loads(r.stdout)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--authorization',required=True,type=Path);parser.add_argument('--authorization-sha256',required=True);args=parser.parse_args()
 started=time.monotonic();ap=args.authorization.resolve();assert ap.is_relative_to(TASK) and sha(ap)==args.authorization_sha256
 a=json.loads(ap.read_text());assert a['task']=='T-0792' and a['mode']=='one-stage-only-no-resolve-no-canonical';assert a['code_sha256']==sha(__file__)
 assert sha(LIB)==LIB_SHA
 spec=importlib.util.spec_from_file_location('bounded_native_helpers',LIB);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
 bp,_=loadpin(a['baseline_state_pin']);bs=json.loads(bp.read_text());basepath=R/bs['backup']['path'];assert sha(basepath)==bs['backup']['sha256'];assert sha(MAIN)==bs['main']['sha256']
 op_path,op=loadpin(a['operation_pin']);tablepath,table=loadpin(a['consequence_table_pin']);assert op['dependencyReviewVersion']==2
 assert set(op)=={'id','actor','reason','dependencyReviewVersion','changes'} and 'T-0792' in op['reason'];assert op['id']==a['operation_id']
 ids=[x['id'] for x in op['changes']];assert len(set(ids))==len(ids) and ids==a['authorized_change_ids']
 for role in ['source_gate','independent_gate']:
  _,g=loadpin(a[role]['pin']);assert at(g,a[role]['ready_pointer']) is True
  assert at(g,a[role]['operation_sha_pointer'])==a['operation_pin']['sha256'];assert at(g,a[role]['consequence_sha_pointer'])==a['consequence_table_pin']['sha256']
 base=h.conn(basepath);live=h.conn(MAIN);assert h.state(base)==h.state(live)=={'journal_head':462,'pending':0};before=h.all50(base);assert before==h.all50(live)
 heads=dict(base.execute('select object_id,max(version) from revision group by object_id'));old_heads=heads.copy()
 assert not base.execute('select 1 from operation where id=?',(op['id'],)).fetchone()
 life=[];protected={}
 for row in base.execute("select r.* from current_revision r left join assessment a on a.revision_id=r.id where r.evidence_status='OWNER_CONFIRMED' or (r.kind='assessment' and a.criteria in ('identity_review/1','tree_effect/1')) order by r.object_id"):
  n=native(h,base,row['id'])
  if n['evidence_status']=='OWNER_CONFIRMED' or (n['kind']=='assessment' and n['data']['criteria'] in ['identity_review/1','tree_effect/1']):protected[row['id']]=n
 for x in op['changes']:
  assert heads.get(x['id'])==x['expectedVersion'],('Return to Astra: 0/multiple/stale target',x['id'])
  assert not any(n['object_id']==x['id'] for n in protected.values()),('Protected OWNER/identity/tree target',x['id'])
  for edge in x['evidence']:assert heads.get(edge['object'])==edge['version'],('Return to Astra: stale evidence',x['id'],edge)
  if x['kind']=='assessment' and x['data']['criteria']=='life_picture_review/1':life.append(x['data']['subject_id']);assert x['data']['outcome'] in ['passed','failed']
  heads[x['id']]=(x['expectedVersion'] or 0)+1
 assert set(life)==PEOPLE and len(life)==4
 # Table APIs are literal, ordered, complete; retains are source dispositions.
 assert table['operation_sha256']==a['operation_pin']['sha256']
 assert [x['new_api']['id'] for x in table['changes']]==ids
 for x,t in zip(op['changes'],table['changes']):
  assert x==t['new_api'] and t['source_disposition'] and t['rationale']
  old=native(h,base,h.current(base,x['id'])) if x['expectedVersion'] is not None else None
  assert old==t['old_native'],('Return to Astra: exact old object differs',x['id'])
 for t in table['retains']:
  assert native(h,base,t['revision_id'])==t['old_native'] and t['source_disposition']=='retain' and t['rationale']
 stage=(R/a['stage_path']).resolve();assert stage.is_relative_to(TASK/'implementation') and not stage.exists();stage.mkdir();db=stage/'stage.sqlite';shutil.copyfile(basepath,db);journal=stage/'journal';journal.mkdir()
 save(stage/'authorization.json',a);save(stage/'before.json',{'all50':before,'protected':protected,'state':h.state(base)})
 try:
  assert sha(MAIN)==bs['main']['sha256'] and sha(ap)==args.authorization_sha256
  cli(['apply',str(op_path),'--db',str(db),'--journal',str(journal)],stage/'apply.json')
  c=h.conn(db);actualstate=h.state(c);assert actualstate['journal_head']==463
  req=dict(c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone());assert json.loads(req['request_json'])==op
  proofs=[]
  for x in op['changes']:
   n=native(h,c,h.current(c,x['id']));actual=h.api(n);assert actual==h.expected_defaults(x,actual);proofs.append({'approved_literal_api':x,'actual_native':n,'actual_api':actual})
  for rid,n in protected.items():assert h.current(c,n['object_id'])==rid and native(h,c,rid)==n
  after=h.all50(c);assert after['schema']==before['schema'];preserved={}
  for name in before['tables']:
   if name in h.DERIVED:continue
   sql=base.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
   if 'WITHOUT ROWID' in sql.upper():assert after['tables'][name]==before['tables'][name];preserved[name]='complete exact';continue
   limit=base.execute('select max(rowid) from "'+name+'"').fetchone()[0];assert h.rows(c,name,True,limit) == h.rows(base,name,True) if limit is not None else True;preserved[name]='old rowid/order exact'
  assert h.rows(c,'review_resolution',True)==h.rows(base,'review_resolution',True)
  for name in ['asset','native_asset']:assert after['tables'][name]==before['tables'][name]
  assert [list(r) for r in base.execute('select object_id,kind,text from object_search order by object_id') if r['object_id'] not in ids]==[list(r) for r in c.execute('select object_id,kind,text from object_search order by object_id') if r['object_id'] not in ids]
  for oid in ids:
   n=native(h,c,h.current(c,oid));expected='\n'.join(str(x) for x in [oid,n['disposition'],n['evidence_status'],n['rationale'],n['caveat'],*n['data'].values()] if x is not None)
   assert [dict(r) for r in c.execute('select object_id,kind,text from object_search where object_id=?',(oid,))]==[{'object_id':oid,'kind':n['kind'],'text':expected}]
  pending=[dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')]
  pool={}
  def add(rid):
   if rid in pool:return
   n=native(h,c,rid);pool[rid]=n
   for e in n['evidence']:add(e['basis_revision_id'])
  for q in pending:
   for rid in [q['affected_revision_id'],q['changed_revision_id']]:
    add(rid);oid=pool[rid]['object_id'];add(h.current(c,oid))
    for row in c.execute('select id from revision where object_id=? order by version',(oid,)):add(row[0])
  save(stage/'actual-requests-full-context.json',{'actual_state':actualstate,'requests':pending,'objects':pool,'no_auto_rebind_or_resolution':True,'Astra_individual_disposition_required':bool(pending)})
  save(stage/'actual-literal-target-proofs.json',proofs);save(stage/'old-row-order-protected-proof.json',{'tables':preserved,'protected_current_exact':True,'all50_after':after,'canonical_unchanged':sha(MAIN)==bs['main']['sha256']});c.close()
  validators=[]
  for label,command in [('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source']),('inventory',['inventory']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]:
   p=stage/(label+'.json');result=cli(command+['--db',str(db),'--journal',str(journal)],p)
   if label.startswith('verify'):assert result['ok'] is True
   validators.append({'path':str(p.relative_to(R)),'sha256':sha(p)})
  assert sha(MAIN)==bs['main']['sha256'] and h.all50(live)==before
  save(stage/'result.json',{'actual_state':actualstate,'stage_db':{'path':str(db.relative_to(R)),'sha256':sha(db)},'validators':validators,'literal_targets_equal':True,'old_rows_and_order_preserved':True,'protected_OWNER_identity_tree_exact':True,'canonical_unchanged':True,'source_final_approval':False,'resolutions_applied':0,'elapsed_seconds':time.monotonic()-started})
 except BaseException as e:
  c=h.conn(db);save(stage/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'actual_state':h.state(c),'elapsed_seconds':time.monotonic()-started,'no_retry':True});c.close();raise
 finally:base.close();live.close()
if __name__=='__main__':main()
