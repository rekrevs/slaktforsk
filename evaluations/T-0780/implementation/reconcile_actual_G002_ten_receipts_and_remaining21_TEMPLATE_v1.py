"""UNRUN readonly receipt union reconciler, only after actual canonical acceptance.
Does not create acceptance receipts, apply operations, update program/Wotan or grant credit.
"""
import argparse,datetime,hashlib,json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(Path(p).resolve().relative_to(ROOT)),'sha256':sha(p)}
def loadpin(x):
 p=ROOT/x['path'];assert p.is_file() and sha(p)==x['sha256'];return json.loads(p.read_text())
def main(receipt_manifest,new_output):
 mp=Path(receipt_manifest).resolve();out=Path(new_output).resolve()
 assert mp.is_relative_to(ROOT/'evaluations/T-0780') and out.is_relative_to(ROOT/'evaluations/T-0780')
 assert not out.exists(),'Preserve earlier reconciliation'
 manifest_sha=sha(mp);m=json.loads(mp.read_text())
 assert m['task']=='T-0780' and m['status']=='ROOT_APPROVED_ACTUAL_CANONICAL_TEN_ACCEPTANCE'
 a=loadpin(m['actual_root_acceptance_receipt_pin'])
 assert a['task']=='T-0780' and a['approved_for_program_acceptance'] is True
 assert a['actual_canonical_state']['pending']==0
 assert a['actual_stage_comparison_pass'] is True and a['independent_exact_hash_final_pass'] is True
 assert a['protected_knowledge_and_review_state_pass'] is True
 assert a['accepted_citation_scopes']==m['exact_ten_citations'] and len(m['exact_ten_citations'])==10
 for k in ['verify','verify-assets','verify-source','inventory','verified-pedigree']:
  assert a['actual_validator_results'][k]['pass'] is True
 c=sqlite3.connect('file:'+str(ROOT/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True)
 state={'journal_head':c.execute('select max(sequence) from operation_payload').fetchone()[0],'pending':c.execute('select count(*) from pending_review').fetchone()[0]};c.close()
 assert state==a['actual_canonical_state'] and state['pending']==0
 cohort=loadpin(m['fixed_cohort_pin'])['members']['citations'];assert len(cohort)==len(set(cohort))==31
 assert set(m['exact_ten_citations'])<=set(cohort)
 receipts=[];seen=set()
 assert len(m['ten_actual_receipt_pins'])==10
 for rp in m['ten_actual_receipt_pins']:
  r=loadpin(rp);citation=r['citation']
  assert citation in cohort and citation not in seen;seen.add(citation)
  assert r['task']=='T-0678' and r['execution_task']=='T-0780' and r['program']=='G002'
  assert r['decision']==m['approved_receipt_decision'] and r['accepted_at']
  assert {'journal_head':r['journal'],'pending':r['pending']}==state
  assert r['root_acceptance_receipt']==m['actual_root_acceptance_receipt_pin']
  assert r['primary_final_review']==a['primary_final_review'] and r['independent_final_review']==a['independent_final_review']
  receipts.append({'citation':citation,'receipt_pin':rp,'literal_decision':r['decision'],'journal':r['journal'],'pending':r['pending']})
 assert seen==set(m['exact_ten_citations'])
 # Existing extra same-program receipts are an unexpected scope/count issue, not silently ignored.
 folder=ROOT/'genealogy2/verification/T-0678'
 declared={(ROOT[x['path']).resolve() for x in m['ten_actual_receipt_pins']}
 for p in folder.glob('*.json'):
  r=json.loads(p.read_text())
  if r.get('program')=='G002' and r.get('decision') is not None:assert p.resolve() in declared,('unexpected additional G002 receipt',str(p))
 remaining=[x for x in cohort if x not in seen];assert len(remaining)==21
 assert sha(mp)==manifest_sha
 result={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'MECHANICAL_ACTUAL_RECEIPT_UNION_ONLY',
  'manifest_pin':pin(mp),'actual_root_acceptance_receipt_pin':m['actual_root_acceptance_receipt_pin'],'actual_canonical_state':state,
  'program':'G002','cohort_pin':m['fixed_cohort_pin'],'fixed_total_citation_scopes':31,'actual_individually_accepted_receipts':receipts,
  'actual_accepted_count':10,'remaining_count':21,'remaining_citations_in_fixed_cohort_order':remaining,
  'no_new_source_priority_or_scope_lock':True,'next_two_require_root_current_versions_and_reuse_lock':True,
  'full_group_or_person_completion_inferred':False,'new_acceptance_receipts_created':0,'runtime_or_Wotan_writes':0}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result_pin':pin(out),'accepted_count':10,'remaining_count':21,'runtime_writes':0},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('actual_receipt_manifest');p.add_argument('--new-output',required=True);a=p.parse_args();main(a.actual_receipt_manifest,a.new_output)
