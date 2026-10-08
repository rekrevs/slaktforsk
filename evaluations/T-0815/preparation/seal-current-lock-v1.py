from pathlib import Path
import json,hashlib,sqlite3,datetime,importlib.util,time
R=Path.cwd();D=R/'evaluations/T-0815/preparation';started=time.monotonic()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def save(n,v):(D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
base=read(D/'baseline-v1.json');assert sha(base['main']['path'])==base['main']['sha256'];c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
old=sqlite3.connect('file:evaluations/T-0814/preparation/baseline481.sqlite?mode=ro',uri=True);old.row_factory=sqlite3.Row
state={'journal_head':c.execute('select max(sequence) from operation_payload').fetchone()[0],'pending':c.execute('select count(*) from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null').fetchone()[0]};assert state==base['state']
assert [dict(x)for x in old.execute('select * from operation_payload order by sequence')]==[dict(x)for x in c.execute('select * from operation_payload where sequence<=481 order by sequence')]
prior=read('evaluations/T-0814/preparation/unchanged481-receipt-reuse-proof-v1.json');assert all(sha(x['path'])==x['sha256']for x in prior['journal_file_pins']);recon=read('evaluations/T-0813/preparation/actual-accepted-reconciliation-v1.json');assert recon['all_exact']
delta=[]
for row in c.execute('select p.*,o.request_hash from operation_payload p join operation o on o.id=p.operation_id where p.sequence>481 order by p.sequence'):
 row=dict(row);p=next((R/'genealogy2/journal').glob(f"{row['sequence']:09d}-*.json"));j=read(p);request=json.loads(row['request_json']);assert j['request']==request and j['sequence']==row['sequence'] and j['policy']==row['policy'] and j['requestHash']==row['request_hash'] and request['id']==row['operation_id'];delta.append({'sequence':row['sequence'],'operation_id':row['operation_id'],'policy':row['policy'],'request_hash':row['request_hash'],'journal_path':str(p.relative_to(R)),'journal_sha256':sha(p),'all_exact':True,'accepted_envelope':j})
save('accepted-delta482-483-v1.json',{'all_exact':True,'entries':delta});save('actual-accepted-reconciliation-v1.json',{'all_exact':True,'journal_head':483,'count':483,'prefix481_payloads_exact_to_verified_baseline':True,'prefix481_journal_hashes_unchanged':True,'prefix_reconciliation':'evaluations/T-0813/preparation/actual-accepted-reconciliation-v1.json','prefix_journal_pins':'evaluations/T-0814/preparation/unchanged481-receipt-reuse-proof-v1.json','delta':'evaluations/T-0815/preparation/accepted-delta482-483-v1.json','no_history_reinterpretation':True})
sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);hc=h.conn(R/base['main']['path']);owner=read('evaluations/T-0813/preparation/all-current-OWNER-scope-v1.json')
for o in owner['OWNER_full_native']:
 assert h.current(hc,o['object_id'])==o['id']
 # Native extractor decodes stored json; compare exact raw rows against481, preserving all metadata/order.
 assert h.native(hc,o['id'])==h.native(h.conn(R/'evaluations/T-0814/preparation/baseline481.sqlite'),o['id'])
save('OWNER-scope-reuse-v1.json',{'full_current_OWNER45':'evaluations/T-0813/preparation/all-current-OWNER-scope-v1.json','current45_heads_and_fullnative_exact_to481':True,'full25bases_and_exact6PCDs_in_same_packet':True,'additional_PCD002':'evaluations/T-0814/preparation/PCD-2026-10-08-002-snapshot.md','qualification':'45 current scopes provided for Astra; absence of literal focal match is not proof of no relevant OWNER scope.'})
revs=read(D/'native-support-versions-v1.json')['revisions'];ops=[]
for oid in sorted({r['operation_id']for r in revs}):
 row=c.execute('select p.sequence,p.policy,o.request_hash from operation_payload p join operation o on o.id=p.operation_id where p.operation_id=?',(oid,)).fetchone()
 if row:ops.append({'operation_id':oid,**dict(row),'receipt':str(next((R/'genealogy2/journal').glob(f"{row['sequence']:09d}-*.json")).relative_to(R))})
 else:ops.append({'operation_id':oid,'qualification':'Accepted historical import predates journal; native metadata retained.'})
save('accepted-direct-support-operation-index-v1.json',{'operations':ops,'qualification':'Exact full canonical envelopes referenced, not duplicate aggregate history.'})
child=read(D/'native/P-0009.json');edges=[o for o in child['current']if o['kind']=='relation' and o['data']['relation_type']=='parent' and o['data']['to_person']=='P-0009' and o['data']['from_person']in['P-0042','P-0043']];save('exact-parent-to-Ada-links-v1.json',{'fullnative_edges':edges,'actual_edge_count':len(edges),'direction_type_only_routing':True,'all_child_current_native':str((D/'native/P-0009.json').relative_to(R))})
media=[]
for o in revs:
 if o['kind']=='record':media.extend(dict(x)for x in c.execute('select rm.*,m.* from record_media rm join native_asset m on m.id=rm.asset_id where rm.revision_id=? order by rm.rowid',(o['id'],)))
save('existing-record-media-metadata-v1.json',{'record_media':media,'qualification':'Metadata only; no original bytes opened; no source permission or own extraction inferred.'})
scopes=['T-0091','T-0227','T-0228','T-0260','T-0261','T-0410','T-0411','T-0412','T-0579']
norms=['AGENTS.md','wotan/README.md','wotan/dev-log/T-0815.md','genealogy2/AGENTS.md','genealogy2/docs/working.md','docs/research/person-contract.md','docs/research/source-strategy.md','NORTH-STAR.md']+[f'wotan/dev-log/{t}.md'for t in scopes]
for p in norms:
 q=D/'normative-and-owner-snapshots'/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
save('current-semantic-field-routing-v1.json',{'focal':[{'person':pid,'fullnative':str((D/f'native/{pid}.json').relative_to(R)),'fields':'All body/caveat/data/structured status/outcomes/rationale, exact ordered evidence/origins and direct bound/current stronger support'}for pid in ['P-0042','P-0043']],'child':'P-0009','interpretation':False,'old_owner_scopes':'Full exact snapshots; routing only, no promotion'})
backup=D/'baseline483.sqlite';out=sqlite3.connect(backup);c.backup(out);out.close();assert sha(base['main']['path'])==base['main']['sha256']
reuse=['evaluations/T-0813/preparation/actual-accepted-reconciliation-v1.json','evaluations/T-0814/preparation/unchanged481-receipt-reuse-proof-v1.json','evaluations/T-0813/preparation/all-current-OWNER-scope-v1.json','evaluations/T-0814/preparation/PCD-2026-10-08-002-snapshot.md','evaluations/T-0814/root-actual-final-verification-v1.json','evaluations/T-0814/actual-main-stage-comparison-v1.json','evaluations/T-0814/root-actual-inventory-full-v1.json','evaluations/T-0814/root-actual-pedigree-P0269-v1.json','evaluations/T-0814/root-actual-pedigree-P0270-v1.json','evaluations/T-0815/root-start-baseline-v1.json']
reuse.extend(x['receipt']for x in ops if 'receipt'in x);reuse=sorted(set(reuse))
result={'state':state,'main_unchanged':True,'current_persons':3,'focal_persons':2,'protected_child':'P-0009','actual_parent_links':len(edges),'OWNER_current':45,'backup_sha256':sha(backup),'reconciliation_all483_exact':True,'capture':read(D/'capture-result-v1.json'),'elapsed_sealing_seconds':time.monotonic()-started,'no_originals_opened':True,'no_native_or_queue_writes':True};save('preparation-result-v1.json',result)
files=[{'path':str(p.relative_to(R)),'sha256':sha(p)}for p in sorted(D.rglob('*'))if p.is_file()]+[{'path':p,'sha256':sha(p),'reuse':True}for p in reuse]
save('locked-input-manifest-v1.json',{'task':'T-0815','main':base['main'],'state':state,'focal':['P-0042','P-0043'],'protected_child':'P-0009','original_ceiling':0,'files':files,'fullperson_index':str((D/'current-person-index-v1.json').relative_to(R)),'native_support':str((D/'native-support-versions-v1.json').relative_to(R)),'scope':str((D/'fixed-scope-v1.json').relative_to(R)),'OWNER':'Reuse exact all45 native+25bases+sixPCD sections plusPCD002; Astra determines relevance','receipt_reconciliation':str((D/'actual-accepted-reconciliation-v1.json').relative_to(R)),'notes':['Full native/source textual input only. Metadata routing is not source judgment.','Source/path history and old negatives preserved; no reinterpretation or opening original images.']});print(json.dumps({'manifest_sha256':sha(D/'locked-input-manifest-v1.json'),'pins':len(files),'result':result},ensure_ascii=False))
