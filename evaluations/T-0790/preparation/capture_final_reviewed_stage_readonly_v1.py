"""Only after root supplies exact final456/pending0 hash. Read-only CLI/SQL.
No clone/apply/resolve/source interpretation; full person JSON subsumes research.
"""
import argparse,concurrent.futures,importlib.util,json,sqlite3,time
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0790/preparation';S=O/'reviewed-stage-v1'
def main():
 assert __debug__
 a=argparse.ArgumentParser();a.add_argument('--root-final-stage-sha256',required=True);args=a.parse_args();start=time.monotonic()
 sp=importlib.util.spec_from_file_location('stage_ro',O/'stage_literal_authorized_v1.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
 spec=importlib.util.spec_from_file_location('h',m.LIB);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
 db=S/'stage.sqlite';assert m.sha(db)==args.root_final_stage_sha256;c=h.conn(db);assert h.state(c)=={'journal_head':456,'pending':0}
 bs=json.loads((O/'baseline-state.json').read_text());assert m.sha(m.MAIN)==bs['main']['sha256']
 out=O/'final-stage456-readonly-capture-v1';assert not out.exists();out.mkdir()
 op1=O/'materialized-source-v3-literal-v1/operation-literal.json';op2=O/'exact-nine-request-only-resolution-draft-v1/resolve-literal.json'
 ops=[json.loads(p.read_text()) for p in [op1,op2]];assert [op['id'] for op in ops]==['T0790-existing-material-life-six-v1','T0790-nine-individual-dependency-resolutions-v1']
 for op in ops:assert json.loads(c.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone()[0])==op
 firstproof=json.loads((S/'old-row-order-protected-proof.json').read_text());all50=h.all50(c);assert all50['schema']==firstproof['all50_after']['schema']
 allowed={'operation','operation_payload','review_resolution'};diff={name for name,proof in all50['tables'].items() if proof!=firstproof['all50_after']['tables'][name]};assert diff==allowed
 # Targets/current APIs and every context object stay exact across request-only resolve.
 targets=json.loads((S/'actual-literal-target-proofs.json').read_text());ctx=json.loads((S/'actual-requests-full-context.json').read_text())
 for proof in targets:
  n=proof['actual_native'];assert m.native(h,c,n['id'])==n and h.current(c,n['object_id'])==n['id']
 for rid,n in ctx['objects'].items():assert m.native(h,c,rid)==n
 native=h.write(out/'final-stage-full40-current-targets-and-nine-context-native.json',{'actual_target_proofs':targets,'full_request_context_objects':ctx['objects'],'resolved_actual_requests':ctx['requests'],'all_full_native_unchanged_since455':True})
 preservation=h.write(out/'final456-only-three-appendtables-and-full-native-preservation.json',{'only_changed_table_names':sorted(diff),'all50_final':all50,'initial455_fullproof_pin':h.pin(S/'old-row-order-protected-proof.json'),'full40current_and9context_exact':True,'media_arrays_assets_source_and_all_other_tables_exact455':True,'root_initial_same-stage_old-row_order_proof_required_in_manifest':True})
 commands=[]
 for person in ['P-0004','P-0210','P-0005','P-0006','P-0211','P-0212']:commands.append((person+'-person',['person',person,'--format','json']))
 commands += [('verify',['verify']),('inventory',['inventory']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]
 def run(item):
  label,cmd=item;p=out/(label+'.json');value=m.cli(cmd+['--db',str(db)],p)
  if label=='verify':assert value['ok'] is True
  return label,h.pin(p)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:results=dict(executor.map(run,commands))
 reused={}
 for label in ['verify-assets','verify-source']:
  p=S/(label+'.json');v=json.loads(p.read_text());assert v['ok'] is True;reused[label]={'pin':h.pin(p),'reuse_basis':preservation,'reason':'Request-only resolution appended operation/payload/resolution; every native/source/media/assets/ordered array unchanged relative successful455 check.'}
 six={p:results[p+'-person'] for p in ['P-0004','P-0210','P-0005','P-0006','P-0211','P-0212']}
 validators={label:results[label] if label in results else reused[label]['pin'] for label in ['verify','verify-assets','verify-source','inventory','Adam-verified','Axel-verified']}
 manifest={'task':'T-0790','actual_final_state':h.state(c),'reviewed_stage_DB_pin':h.pin(db),'ordered_operations':[h.pin(op1),h.pin(op2)],'consequence_table_pin':h.pin(O/'materialized-source-v3-literal-v1/individual-consequence-table.json'),'resolution_table_pin':h.pin(O/'exact-nine-request-only-resolution-draft-v1/nine-individual-resolution-table.json'),'source_spec_pin':h.pin(R/'evaluations/T-0790/source-review/settled-90-dispositions-and-literal-field-decisions-v3.json'),'preservation_proof_pin':preservation,'full_native_current_context_pin':native,'six_final_person_views':six,'six_final_validator_pins':validators,'reused_checks':reused,'first455_result_pin':h.pin(S/'result.json'),'root_same_stage_resolution_result_pin':h.pin(O/'nine-resolution-actual-v2/result.json'),'source_final_approval':False,'canonical_apply':False,'elapsed_monotonic_seconds':time.monotonic()-start}
 assert m.sha(db)==args.root_final_stage_sha256 and m.sha(m.MAIN)==bs['main']['sha256'];h.write(out/'final-stage-package-manifest-v1.json',manifest);c.close();print(json.dumps({'manifest':h.pin(out/'final-stage-package-manifest-v1.json'),'elapsed':time.monotonic()-start}))
if __name__=='__main__':main()
