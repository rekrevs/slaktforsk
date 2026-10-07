"""Root-gated one-life amendment to existing459 clone only; no reapply/new clone/main."""
from pathlib import Path
import json,argparse,importlib.util,time,traceback,sqlite3,datetime,shutil
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0795/preparation';S=O/'reviewed-stage-v1';D=O/'life-amendment-v1'
sp=importlib.util.spec_from_file_location('m',O/'stage_literal_UNRUN_v2.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);h=m.h
PROPOSAL=R/'evaluations/T-0795/source-review/primary-life-impact-amendment-proposal-v1.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--authorization',type=Path,required=True);ap.add_argument('--sha256',required=True);a=ap.parse_args();assert h.sha(a.authorization)==a.sha256;auth=json.loads(a.authorization.read_text());assert auth['same459_amendment_authorized'] is True and auth['helper_sha256']==h.sha(__file__)
 assert h.sha(PROPOSAL)==auth['proposal_sha256']=='11c02bb23942bc6824e761bc5e0532daf7f29a241aa5d05106871986a5cb861f'
 operation=D/'operation-life-literal.json';assert h.sha(operation)==auth['operation_sha256']=='7d616d4d8508ec638ec2ceaef10373b37a25a0cdd57024f7a9509cee712b13f3'
 for role in ['primary_gate','independent_gate']:
  g=auth[role];p=R/g['path'];assert h.sha(p)==g['sha256'];value=json.loads(p.read_text());assert h.pointer(value,g['ready_pointer']) is True and h.pointer(value,g['proposal_sha_pointer'])==auth['proposal_sha256']
 db=S/'stage.sqlite';assert h.sha(db)==auth['stage459_sha256']=='bc95d4c79d62348417a89c20182983f16da3d030b6670053202c14f4bd595ff8';c=h.conn(db);live=h.conn(m.MAIN);bs=json.loads((O/'baseline-state.json').read_text());assert h.sha(m.MAIN)==bs['main']['sha256'] and h.state(live)=={'journal_head':457,'pending':0} and h.state(c)=={'journal_head':459,'pending':0}
 capture=D/'immutable-before459.sqlite';assert not capture.exists();shutil.copy2(db,capture);assert h.sha(capture)==auth['stage459_sha256'];before=h.conn(capture);assert h.all50(before)==h.all50(c);h.write(D/'before459-backup-pin.json',{'backup':h.pin(capture),'original_hash':auth['stage459_sha256'],'readonly_preservation_not_apply_clone':True,'old_manifest_and_proposal_base_hash_alias':'All prior stage459 DB pins bc95d4c... now preserved byte-exact at this backup; existing execution DB alone proceeds460.'})
 old=m.native(c,'ASSESSMENT-T0790-P0212-life@1');source=json.loads(PROPOSAL.read_text());api=h.api(old);api['expectedVersion']=1;assert api==source['old_full_API'];op=json.loads(operation.read_text());assert len(op['changes'])==1 and op['changes'][0]==source['new_full_API']
 out=D/'actual460';assert not out.exists();out.mkdir();m.run(['apply',str(operation),'--db',str(db),'--journal',str(S/'journal')],out/'apply-life.json');assert h.state(c)['journal_head']==460
 actual=m.native(c,'ASSESSMENT-T0790-P0212-life@2');assert h.api(actual)==h.expected_defaults(op['changes'][0],h.api(actual));assert m.native(c,old['id'])==old
 for t in ['origin','dependency','record_asset','record_media','review_resolution']:
  maximum=before.execute('select max(rowid) from '+t).fetchone()[0] or 0;assert h.rows(before,t,True)==h.rows(c,t,True,maximum)
 # All raw historical rows remain; changed derived FTS excepted.
 b=h.all50(before);aft=h.all50(c)
 for t in b['tables']:
  if t in h.DERIVED:continue
  sql=before.execute('select sql from sqlite_master where name=?',(t,)).fetchone()[0]
  if 'WITHOUT ROWID' in sql.upper():assert b['tables'][t]==aft['tables'][t];continue
  limit=before.execute('select max(rowid) from "'+t+'"').fetchone()[0] or 0;assert h.rows(before,t)==h.rows(c,t,maximum=limit),t
 prior=json.loads((O/'continuation-v1/actual459/final459-all35-full-native-proof.json').read_text())
 for x in prior:assert m.native(c,x['actual_native']['id'])==x['actual_native'] and h.current(c,x['actual_native']['object_id'])==x['actual_native']['id']
 protected=json.loads((O/'protected-P0212-identity-tree-relation-OWNER.json').read_text())
 for rid,n in protected.items():assert h.current(c,n['object_id'])==rid and m.native(c,rid)==n
 for row in before.execute("select id from current_revision where id like 'ASSESSMENT%' or id like 'CONTRACT%' or id like 'THEME%'"):
  n=m.native(before,row[0]);assert m.native(c,h.current(c,n['object_id']))['data'].get('outcome')==n['data'].get('outcome')
 pending=[dict(x) for x in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];h.write(out/'actual-pending-full.json',pending);h.write(out/'all50-and36-full-native-proof.json',{'all50':aft,'original35':prior,'life_v1':old,'life_v2':actual,'seven_old_retains_preserved':True,'axes_grades_preserved':True})
 if pending:print({'STOP':'individual source review required','pending':len(pending)});return
 assert h.state(c)=={'journal_head':460,'pending':0}
 for name,args in [('P0212-person',['person','P-0212','--format','json']),('P0212-inspect',['inspect','P-0212']),('inventory',['inventory','--full']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270']),('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source'])]:
  got=m.run(args+['--db',str(db)],out/(name+'.json'))
  if name.startswith('verify'):assert got['ok'] is True
 for label in ['Adam-verified','Axel-verified']:
  base=json.loads((O/(label+'.json')).read_text());now=json.loads((out/(label+'.json')).read_text())
  for key in ['root','mode','rules','maxDepth','maxPaths','truncated','paths','edges','excluded','root_gate']:assert now[key]==base[key],key
  assert [g['person_id'] for g in now['gates']]==[g['person_id'] for g in base['gates']]
  for oldg,newg in zip(base['gates'],now['gates']):
   for key in ['criteria','passed','status','reasons','explanation','person','identity_review','tree_effect']:assert oldg[key]==newg[key],(oldg['person_id'],key)
   for key in ['source','criteria','outcome','usable']:assert oldg['life_picture_review'].get(key)==newg['life_picture_review'].get(key),(oldg['person_id'],'life',key)
  target=next(g for g in now['gates'] if g['person_id']=='P-0212');assert target['life_picture_review']['usable'] is True and target['life_picture_review']['outcome']=='failed'
 h.write(out/'verified-pedigree-axis-preservation.json',{'both_paths_edges_roots_identity_tree_axes_exact_baseline':True,'all_life_axes_source_criteria_outcome_usable_exact_baseline':True,'P0212_usable_restored':True,'failed_unchanged':True,'allowed_current_metadata_assessment_growth':6})
 first=S/'operation-media-bound.json';second=O/'continuation-v1/resolution-operation.json';table=S/'final-media-bound-consequence-table.json';manifest={'reviewed_stage_DB_pin':h.pin(db),'ordered_operations':[h.pin(first),h.pin(second),h.pin(operation)],'consequence_table_pin':h.pin(table),'life_consequence_table_pin':h.pin(D/'single-life-seven-edges-consequence-table.json'),'person_views':{'P-0212':{'baseline':h.pin(O/'P-0212-person.json'),'stage':h.pin(out/'P0212-person.json')}},'final_derived_pins':{k:h.pin(out/(k+'.json')) for k in ['inventory','Adam-verified','Axel-verified','verify','verify-assets','verify-source']},'final_state':h.state(c),'main_unchanged':h.sha(m.MAIN)==bs['main']['sha256'],'source_final_gates':'pending dual SOURCE exact460 approval','production_elapsed_monotonic_seconds':time.monotonic()-started,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};h.write(out/'final-stage-manifest.json',manifest);assert h.sha(m.MAIN)==bs['main']['sha256'];print(manifest['final_state'])
if __name__=='__main__':
 started=time.monotonic()
 try:main()
 except BaseException as e:
  p=D/'life-amendment-failure-preserved.json'
  if not p.exists():h.write(p,{'error':str(e),'traceback':traceback.format_exc(),'elapsed_monotonic_seconds':time.monotonic()-started,'retry_authorized':False})
  raise
