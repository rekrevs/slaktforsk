"""ROOT ONLY. Invoke after actual canonical comparison and independent PASS.
Does not apply canonical or write Wotan. Requires concrete signed root receipt.
"""
import pathlib,json,hashlib,datetime,argparse,sqlite3
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1];p=argparse.ArgumentParser();p.add_argument('root_acceptance_receipt');a=p.parse_args();rp=pathlib.Path(a.root_acceptance_receipt).resolve();actual=json.loads(rp.read_text())
assert actual['task']=='T-0777' and actual['approved_for_program_acceptance'] is True
assert actual['actual_canonical_state']=={'journal_head':269,'pending':0}
assert actual['actual_full_object_matches']==128 and actual['actual_stage_comparison_pass'] is True and actual['independent_exact_hash_pass'] is True
c=sqlite3.connect('file:'+str(R/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True);assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==269;assert c.execute('select count(*) from review_request q left join review_resolution r on q.id=r.request_id where r.request_id is null').fetchone()[0]==0
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def bind(p):return {'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
measure=json.loads((B/'final-native-measurements-v1.json').read_text());receipts=[]
for scope in ['C-0084','C-0402','C-0573','C-0896','C-0911']:
 out=R/'genealogy2/verification/T-0677'/('c'+scope[2:]+'-astra-completion-20261002.json');assert not out.exists()
 rows=[o for o in measure['operations'] if pathlib.Path(o['path']).name.startswith(scope)];x={'task':'T-0677','execution_task':'T-0777','citation':scope,'accepted_at':now,'decision':'COMPLETE_WITH_RESERVATIONS_AFTER_INDEPENDENT_FINAL_PASS','journal':269,'pending':0,'new_objects':sum(o['new'] for o in rows),'revisions':sum(o['revised'] for o in rows),'bounded_adoptions':sum(o['adoptions'] for o in rows),'G001_complete':38,'G001_total':40,'root_acceptance_receipt':bind(rp),'stage_freeze':bind(B/'final-package-freeze-v1.json'),'full_consequence_table':bind(B/(scope+'-final-consequence-table-v3.json')),'limits':['Exact five scopes; no C1047/C1060.','No new identity/person/relation/gate conclusion.','Administrative anchors do not prove continuous residence.','28 heterogeneous scoped rows,81 prior C0021 cells and five gaplabel controls are separate coverage quantities.']};out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');receipts.append(bind(out))
(B/'program-acceptance-v1.json').write_text(json.dumps({'task':'T-0777','recorded_at_utc':now,'program':'G001','before':33,'after':38,'total':40,'receipts':receipts,'root_wotan_checkpoint_required':True},ensure_ascii=False,indent=2)+'\n');print('Five program receipts created; Wotan unchanged')
