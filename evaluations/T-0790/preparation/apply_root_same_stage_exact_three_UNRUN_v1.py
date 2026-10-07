"""UNRUN ROOT-ONLY one same-stage3 CLI apply; no clone/retry/canonical/resolve."""
import argparse,importlib.util,json,time,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0790/preparation'
IDS=['RESEARCH-P-0304-9d76f0343410','RESEARCH-P-0303-9d76f0343410','CONTRACT-P-0006-PK-05']
def main():
 assert __debug__
 p=argparse.ArgumentParser();p.add_argument('--authorization',required=True,type=Path);p.add_argument('--sha256',required=True);args=p.parse_args();start=time.monotonic()
 s=importlib.util.spec_from_file_location('m',O/'stage_literal_authorized_v1.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 assert args.authorization.resolve().is_relative_to(O) and m.sha(args.authorization)==args.sha256
 a=json.loads(args.authorization.read_text());assert a['task']=='T-0790' and a['mode']=='ROOT_SAME_STAGE_EXACT3_ONCE' and a['root_authorized'] is True and a['code_sha256']==m.sha(__file__)
 assert m.sha(m.LIB)==m.LIB_SHA and m.sha(O/'stage_literal_authorized_v1.py')==a['stage_helper_sha256']
 hs=importlib.util.spec_from_file_location('h',m.LIB);h=importlib.util.module_from_spec(hs);hs.loader.exec_module(h)
 db=(R/a['stage_DB_pin']['path']).resolve();assert db.is_relative_to(O/'reviewed-stage-v1') and m.sha(db)==a['stage_DB_pin']['sha256']
 opath,op=m.loadpin(a['operation_pin']);_,table=m.loadpin(a['consequence_table_pin']);assert [x['id'] for x in op['changes']]==IDS and op['dependencyReviewVersion']==2 and not any(k in op for k in ['resolve','media','spans','mappings','unitDecisions']);assert table['operation_sha256']==a['operation_pin']['sha256']
 for role in ['source_gate','independent_gate']:
  spec=a[role];_,g=m.loadpin(spec['pin']);assert m.at(g,spec['ready_pointer']) is True
  assert m.at(g,spec['operation_sha_pointer'])==a['operation_pin']['sha256'] and m.at(g,spec['consequence_sha_pointer'])==a['consequence_table_pin']['sha256'];assert g['pre_stage_db_sha256']==a['stage_DB_pin']['sha256'] and g['source_spec_sha256']==table['source_spec_pin']['sha256']
 c=h.conn(db);bs=json.loads((O/'baseline-state.json').read_text());assert m.sha(m.MAIN)==bs['main']['sha256'] and h.state(c)=={'journal_head':456,'pending':0};before=h.all50(c)
 assert not c.execute('select 1 from operation where id=?',(op['id'],)).fetchone();protected={};guards={}
 for row in c.execute("select r.* from current_revision r left join assessment a on a.revision_id=r.id where r.evidence_status='OWNER_CONFIRMED' or a.criteria in ('identity_review/1','tree_effect/1','legacy_review_header') order by r.object_id"):
  n=m.native(h,c,row['id'])
  if n['evidence_status']=='OWNER_CONFIRMED' or (n['kind']=='assessment' and n['data']['criteria'] in ['identity_review/1','tree_effect/1','legacy_review_header']):protected[row['id']]=n
 for x,t in zip(op['changes'],table['changes']):
  assert x==t['new_api'] and h.current(c,x['id'])==x['id']+'@'+str(x['expectedVersion']) and m.native(h,c,h.current(c,x['id']))==t['old_native']
  for edge in x['evidence']:assert h.current(c,edge['object'])==edge['object']+'@'+str(edge['version'])
 for name in before['tables']:
  if name in h.DERIVED:continue
  sql=c.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
  if 'WITHOUT ROWID' in sql.upper():guards[name]={'without_rowid':True,'complete_digest':before['tables'][name]}
  else:
   rs=h.rows(c,name,True);guards[name]={'without_rowid':False,'old_max_rowid':c.execute('select max(rowid) from "'+name+'"').fetchone()[0],'old_ordered_digest':h.row_digest(rs,True),'old_count':len(rs)}
 untouched=[list(row) for row in c.execute('select object_id,kind,text from object_search order by object_id') if row['object_id'] not in IDS]
 out=(R/a['output_path']).resolve();assert out.is_relative_to(O) and not out.exists();out.mkdir();m.save(out/'authorization.json',a);m.save(out/'pre456-full50-native-oldrow-order-guards.json',{'all50':before,'guards':guards,'protected':protected,'stage_DB_pin':a['stage_DB_pin']})
 try:
  assert m.sha(db)==a['stage_DB_pin']['sha256'] and m.sha(m.MAIN)==bs['main']['sha256'];m.cli(['apply',str(opath),'--db',str(db),'--journal',str(db.parent/'journal')],out/'apply.json')
  after=h.all50(c);actual=h.state(c);assert actual['journal_head']==457 and after['schema']==before['schema'];assert json.loads(c.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone()[0])==op
  for name,g in guards.items():
   if g['without_rowid']:assert after['tables'][name]==g['complete_digest'],name
   else:
    rs=h.rows(c,name,True,g['old_max_rowid']) if g['old_max_rowid'] is not None else [];assert len(rs)==g['old_count'] and h.row_digest(rs,True)==g['old_ordered_digest'],name
  assert after['tables']['asset']==before['tables']['asset'] and after['tables']['native_asset']==before['tables']['native_asset'] and after['tables']['review_resolution']==before['tables']['review_resolution']
  assert [list(row) for row in c.execute('select object_id,kind,text from object_search order by object_id') if row['object_id'] not in IDS]==untouched
  targets=[]
  for x in op['changes']:
   n=m.native(h,c,h.current(c,x['id']));api=h.api(n);assert api==h.expected_defaults(x,api)
   expected='\n'.join(str(z) for z in [x['id'],n['disposition'],n['evidence_status'],n['rationale'],n['caveat'],*n['data'].values()] if z is not None);assert [dict(r) for r in c.execute('select object_id,kind,text from object_search where object_id=?',(x['id'],))]==[{'object_id':x['id'],'kind':n['kind'],'text':expected}]
   targets.append({'source_literal_api':x,'actual_full_native':n,'actual_api':api})
  for rid,n in protected.items():assert h.current(c,n['object_id'])==rid and m.native(h,c,rid)==n
  pending=[dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')];assert len(pending)==actual['pending'];pool={}
  def add(rid):
   if rid in pool:return
   n=m.native(h,c,rid);pool[rid]=n
   for edge in n['evidence']:add(edge['basis_revision_id'])
  for q in pending:
   for rid in [q['affected_revision_id'],q['changed_revision_id']]:
    add(rid);oid=pool[rid]['object_id'];add(h.current(c,oid))
    for row in c.execute('select id from revision where object_id=? order by version',(oid,)):add(row[0])
  m.save(out/'actual457-individual-pending-full-context.json',{'actual_state':actual,'requests':pending,'objects':pool,'source_disposition':'REQUIRED_IF_PENDING','no_auto_rebind_or_resolve':True});m.save(out/'three-actual-full-native-api-proofs.json',targets)
  assert m.sha(m.MAIN)==bs['main']['sha256'];m.save(out/'result.json',{'actual_state':actual,'stage_DB_pin':h.pin(db),'all50_after':after,'oldrow_order_schema_WITHOUTROWID_exact':True,'native_OWNER_identity_tree_legacy_reviews_exact':True,'three_fullAPI_exact':True,'media_assets_old_resolution_rows_exact':True,'canonical_unchanged':True,'source_final_approval':False,'elapsed_monotonic_seconds':time.monotonic()-start})
 except BaseException as e:
  m.save(out/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'actual_state':h.state(c),'stage_DB_pin':h.pin(db),'no_retry_no_clone_no_resolve':True,'elapsed_monotonic_seconds':time.monotonic()-start});raise
 finally:c.close()
if __name__=='__main__':main()
