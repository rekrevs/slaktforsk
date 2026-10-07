from pathlib import Path
import json,sqlite3,importlib.util,datetime,hashlib
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0795/preparation'
spec=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
c=h.conn(O/'baseline-j457.sqlite');assert h.state(c)=={'journal_head':457,'pending':0}
cp='genealogy/citations/C-0906-yrkeskallor-for-gunnar-hook-katalogprov.md'
us=[dict(x) for x in c.execute('select * from unit where document_path=? order by start_line,end_line,id',(cp,))]
doc=dict(c.execute('select * from document where path=?',(cp,)).fetchone())
h.write(O/'C0906-complete-frozen-native-units.json',{'document':doc,'units':us,'full_document_units':[u['id'] for u in us if u['start_line']==1 and u['end_line']==38]})
full=next(u['raw'] for u in us if u['start_line']==1 and u['end_line']==38);(O/'C0906-frozen-full.md').write_text(full)
receipts=[]
for r in c.execute('select * from operation_payload where sequence>=455 order by sequence'):
 n=dict(r);matches=[]
 for p in (R/'genealogy2/journal').glob(str(r['sequence']).zfill(9)+'-*'):
  matches.append(h.pin(p))
 n['journal_files']=matches;n['request_sha256']=hashlib.sha256(r['request_json'].encode()).hexdigest();receipts.append(n)
# Find actual canonical journal path from repository rather than assume.
if not all(x['journal_files'] for x in receipts):
 for n in receipts:
  n['journal_files']=[h.pin(p) for p in (R/'genealogy2').rglob(str(n['sequence']).zfill(9)+'-*.json') if '/data/' in str(p)]
assert len(receipts)==3 and all(n['journal_files'] for n in receipts)
h.write(O/'T0790-actual-three-receipts-and-journal.json',receipts)
v=json.loads((O/'P-0212-person.json').read_text());research=v['research']
# Complete protected current person/gates/owner/relations carried in person view, plus native rows of related protected types.
pids={'P-0212'}; protected={}
for row in c.execute('select * from current_revision'):
 rid=row['id'];n=h.native(c,rid);ds=json.dumps(n['data'],ensure_ascii=False)
 if ('P-0212' in ds and (n['kind'] in ['person','relation','identity_decision'] or n['evidence_status']=='OWNER_CONFIRMED' or any(s in ds for s in ['identity_review/1','tree_effect/1']))) or n['object_id']=='P-0212':
  n['origins']=[dict(x) for x in c.execute('select * from origin where revision_id=? order by rowid',(rid,))];n['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=? order by rowid',(rid,))];protected[rid]=n
h.write(O/'protected-P0212-identity-tree-relation-OWNER.json',protected)
contexts=['README.md','NORTH-STAR.md','AGENTS.md','genealogy2/AGENTS.md','genealogy2/README.md','genealogy2/docs/working.md','docs/research/research-program.md','docs/research/person-contract.md','docs/research/source-strategy.md','docs/research/riksarkivet-access.md','PROJECT-CONTROL.md','wotan/README.md','wotan/backlog.json','wotan/dev-log/T-0795.md','wotan/dev-log/T-0790.md','wotan/dev-log/T-0359.md','wotan/dev-log/T-0362.md','wotan/dev-log/T-0767.md']
h.write(O/'context-pins.json',[h.pin(R/p) for p in contexts])
h.write(O/'preparation-pinmanifest-v1.json',{'scope':'T0795 P0212 six metadata units; no source interpretation','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[h.pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.suffix in ['.json','.md','.py']],'inspect_research_syntax':'research is person JSON subtree; CLI has no standalone research command','expected_baseline':h.state(c),'native_order':'rowid arrays preserved','source_judgment':'not performed'})
print(json.dumps({'C0906_units':len(us),'C0906_lines':38,'accepted_ops':len(receipts),'protected':len(protected)}))
