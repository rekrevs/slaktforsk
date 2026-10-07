"""Root releases exact final DB hash after same-stage3 actual proof. Read-only.
Reuses validated media/source tables only; fresh6fullperson and other4checks.
"""
import argparse,concurrent.futures,importlib.util,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0790/preparation';S=O/'reviewed-stage-v1'
def main():
 assert __debug__
 a=argparse.ArgumentParser();a.add_argument('--root-final-stage-sha256',required=True);a.add_argument('--root-actual-stage-result',required=True,type=Path);args=a.parse_args();start=time.monotonic()
 sp=importlib.util.spec_from_file_location('m',O/'stage_literal_authorized_v1.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);assert m.sha(m.LIB)==m.LIB_SHA
 hs=importlib.util.spec_from_file_location('h',m.LIB);h=importlib.util.module_from_spec(hs);hs.loader.exec_module(h)
 rp=args.root_actual_stage_result.resolve();assert rp.is_relative_to(S);root=json.loads(rp.read_text());db=S/'stage.sqlite';assert m.sha(db)==args.root_final_stage_sha256==root['stage_DB_pin']['sha256'];c=h.conn(db);assert h.state(c)==root['actual_state'] and root['actual_state']=={'journal_head':457,'pending':0}
 for key in ['oldrow_order_schema_WITHOUTROWID_exact','native_OWNER_identity_tree_legacy_reviews_exact','three_fullAPI_exact','media_assets_old_resolution_rows_exact','canonical_unchanged']:assert root[key] is True
 bs=json.loads((O/'baseline-state.json').read_text());assert m.sha(m.MAIN)==bs['main']['sha256'];before=json.loads((O/'final-stage456-readonly-capture-v1/final456-only-three-appendtables-and-full-native-preservation.json').read_text())['all50_final'];after=h.all50(c);assert after==root['all50_after'];source_media_tables=['asset','native_asset','record_asset','record_media','source','record','transcription','observation','mention','unit','document','interpretation_decision','interpretation_target']
 for name in source_media_tables:
  if name in before['tables']:assert after['tables'][name]==before['tables'][name],name
 opaths=[O/'materialized-source-v3-literal-v1/operation-literal.json',O/'exact-nine-request-only-resolution-draft-v1/resolve-literal.json',O/'final-three-literal-draft-v1/operation-final-three-literal.json'];ops=[json.loads(p.read_text()) for p in opaths]
 for op in ops:assert json.loads(c.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone()[0])==op
 proof=[]
 for op in [ops[0],ops[2]]:
  for x in op['changes']:
   n=m.native(h,c,h.current(c,x['id']));actual=h.api(n);assert actual==h.expected_defaults(x,actual);proof.append({'approved_literal_api':x,'actual_full_native':n,'actual_api':actual})
 ctx=json.loads((S/'actual-requests-full-context.json').read_text());assert len(ctx['requests'])==9
 for rid,n in ctx['objects'].items():assert m.native(h,c,rid)==n
 out=O/'final-stage457-readonly-capture-v1';assert not out.exists();out.mkdir();full=h.write(out/'full43current-targets-and-original-nine-context-native.json',{'targets':proof,'original9context_objects':ctx['objects'],'original9requests':ctx['requests'],'all43fullAPIs_exact':True,'no_pending':True})
 preserve=h.write(out/'root-full50-source-media-unchanged-reuse-proof.json',{'actual_all50':after,'root_same_stage3_actual_result_pin':h.pin(rp),'held456source_preservation_pin':h.pin(O/'final-stage456-readonly-capture-v1/final456-only-three-appendtables-and-full-native-preservation.json'),'source_media_tables_exact456':source_media_tables,'old_native_history_and_order_exact':True})
 labels=[(p+'-person',['person',p,'--format','json']) for p in ['P-0004','P-0210','P-0005','P-0006','P-0211','P-0212']]+[('verify',['verify']),('inventory',['inventory']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]
 def run(item):
  label,args=item;p=out/(label+'.json');v=m.cli(args+['--db',str(db)],p)
  if label=='verify':assert v['ok'] is True
  return label,h.pin(p)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:results=dict(e.map(run,labels))
 reused={}
 for label in ['verify-assets','verify-source']:
  p=S/(label+'.json');assert json.loads(p.read_text())['ok'] is True;reused[label]={'pin':h.pin(p),'basis_pin':preserve,'reason':'Exact456/source and media tables plus native records/transcriptions/observations/mentions unchanged; three assessed research revisions preserve source origins and only approved literal evidence additions. No new media/source record. Root full50 oldrows/order and fresh verify support this reuse.'}
 manifest={'task':'T-0790','actual_final_state':h.state(c),'reviewed_stage_DB_pin':h.pin(db),'ordered_operations':[h.pin(p) for p in opaths],'consequence_table_pin':h.pin(O/'materialized-source-v3-literal-v1/individual-consequence-table.json'),'resolution_table_pin':h.pin(O/'exact-nine-request-only-resolution-draft-v1/nine-individual-resolution-table.json'),'final_three_consequence_table_pin':h.pin(O/'final-three-literal-draft-v1/final-three-and-two-retains-consequence-table.json'),'source_spec_pin':h.pin(R/'evaluations/T-0790/source-review/settled-90-dispositions-and-literal-field-decisions-v3.json'),'final_three_source_spec_pin':h.pin(R/'evaluations/T-0790/source-review/final-semantic-three-amendments-and-two-retains-v1.json'),'preservation_proof_pin':preserve,'full_current_native_context_pin':full,'six_final_person_views':{p:results[p+'-person'] for p in ['P-0004','P-0210','P-0005','P-0006','P-0211','P-0212']},'six_final_validator_pins':{label:results[label] if label in results else reused[label]['pin'] for label in ['verify','verify-assets','verify-source','inventory','Adam-verified','Axel-verified']},'reused_checks':reused,'source_final_approval':False,'canonical_apply':False,'elapsed_monotonic_seconds':time.monotonic()-start}
 assert m.sha(db)==args.root_final_stage_sha256 and m.sha(m.MAIN)==bs['main']['sha256'];h.write(out/'final457-package-manifest-v1.json',manifest);c.close();print(json.dumps({'manifest':h.pin(out/'final457-package-manifest-v1.json'),'elapsed':time.monotonic()-start}))
if __name__=='__main__':main()
