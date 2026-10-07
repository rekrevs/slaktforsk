import json,hashlib,importlib.util,copy
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0804/implementation';P=R/'evaluations/T-0804/primary';sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);b=h.conn(R/'evaluations/T-0804/preparation/baseline464.sqlite');core=json.loads((P/'source-approved-core-design-v1.json').read_text());sem=json.loads((P/'semantic-dispositions-v2.json').read_text());heads=dict(b.execute('select object_id,version from current_revision'))
def native(oid):
 rid=h.current(b,oid);n=h.native(b,rid)
 for key,t in [('origins','origin'),('evidence','dependency')]:n[key]=[dict(z)for z in b.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
changes=copy.deepcopy(core['changes']);con=[];errors=[]
for x in sem['changes']:
 old=native(x['object']);a=h.api(old);assert old['version']==x['expectedVersion'];a['expectedVersion']=old['version'];checks=[]
 for edit in x['fields']:
  f=edit['field'];target=a if f in ['caveat','rationale','disposition','evidenceStatus']else a['data'];oldfield=target[f];count=oldfield.count(edit['old']);assert count==1,('Literal zero/multi',x['object'],f,count);target[f]=oldfield.replace(edit['old'],edit['new'],1);checks.append({'field':f,'old_full':oldfield,'new_full':target[f],'source_literal':edit})
 oid,vs=x['support'].rsplit('@',1);e={'object':oid,'version':int(vs),'role':'supports','note':'T-0804: exakt ägarbekräftad familjekoppling enligt PCD-2026-10-07-001; kompletterar arkivstöd utan ny originalutvinning.'}
 if not any(z['object']==oid and z['version']==int(vs) and z['role']=='supports'for z in a['evidence']):a['evidence'].append(e)
 changes.append(a);con.append({'object':x['object'],'old_native':old,'new_api':a,'source_fields':checks,'rationale':[z['reason']for z in x['fields']]})
assert len({x['id']for x in changes})==len(changes);projected={x['id']:(x['expectedVersion'] or 0)+1 for x in changes};proposals=[]
rebindSource=json.loads((P/'exact-projected-rebind-decisions-v1.json').read_text());assert rebindSource['inputSha256']=='4756e32956158e5f4b0efbbabc9ea4d6e5d5b6883db21f18a328e735bc05e058';appliedRebinds=[]
for rd in rebindSource['decisions']:
 target=next(x for x in changes if x['id']==rd['target']);assert target['evidence'][rd['edge_index']]==rd['original_proposed_edge'];target['evidence'][rd['edge_index']]=rd['new_edge'];appliedRebinds.append(rd)
for x in changes:
 for i,e in enumerate(x['evidence']):
  actual=projected.get(e['object'],heads.get(e['object']))
  if e['version']!=actual:proposals.append({'target':x['id'],'edge_index':i,'original_proposed_edge':copy.deepcopy(e),'proposed_resulting_version':actual,'old_current_version':heads.get(e['object']),'requiresIndividualExactSourceApproval':True})
assert not proposals,('Unapproved version amendments return Astra',proposals)
# Sort the exact approved resulting-dependency graph, without silently changing edge versions.
byid={x['id']:x for x in changes};pending=list(byid);ordered=[]
while pending:
 ready=[oid for oid in pending if all(e['object'] not in byid or e['object'] in ordered for e in byid[oid]['evidence'])]
 assert ready,('Resulting-version dependency cycle requires source decision',pending)
 for oid in ready:ordered.append(oid);pending.remove(oid)
op={k:v for k,v in core.items()if k!='changes'};op['changes']=[byid[oid]for oid in ordered];p=D/'candidate-operation-v1.json';p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
for x in core['changes']:con.append({'object':x['id'],'old_native':native(x['id']) if x['expectedVersion']is not None else None,'new_api':x,'source_core_design':True})
retains=[{'revision_id':z['object']+'@'+str(z['version']),'old_native':native(z['object']),'source_disposition':'retain','rationale':z['reason']}for z in sem['explicitHistoricalRetains']]
byid={a['id']:a for a in op['changes']}
for row in con:
 row['new_api']=byid[row['object']];row['source_disposition']='create' if row['old_native'] is None else 'revise';row['rationale']=row.get('rationale',row['new_api']['rationale'])
con.sort(key=lambda row:ordered.index(row['object']))
q=D/'individual-consequence-table-v1.json';q.write_text(json.dumps({'task':'T-0804','role':'Literal settled core/semantic and individually approved projected bindings; no apply, dual clone gates required.','source_core_pin':{'path':str((P/'source-approved-core-design-v1.json').relative_to(R)),'sha256':hashlib.sha256((P/'source-approved-core-design-v1.json').read_bytes()).hexdigest()},'semantic_pin':{'path':str((P/'semantic-dispositions-v2.json').relative_to(R)),'sha256':hashlib.sha256((P/'semantic-dispositions-v2.json').read_bytes()).hexdigest()},'candidate_pin':{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},'resulting_versions':projected,'ordered_change_ids':ordered,'operation_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'approved_projected_rebinds':appliedRebinds,'rebind_source_pin':{'path':str((P/'exact-projected-rebind-decisions-v1.json').relative_to(R)),'sha256':hashlib.sha256((P/'exact-projected-rebind-decisions-v1.json').read_bytes()).hexdigest()},'unapproved_rebinds':proposals,'changes':con,'retains':retains},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'changes':len(changes),'rebindsRequiringExactApproval':len(proposals),'retains':len(retains),'candidateSha':hashlib.sha256(p.read_bytes()).hexdigest(),'listSha':hashlib.sha256(q.read_bytes()).hexdigest()}))
