"""Literal mechanical candidate materialization only; no apply/canonical path."""
import copy,hashlib,importlib.util,json,sqlite3
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0791/implementation';P=R/'evaluations/T-0791/primary/primary-decisions-v4.json';EXPECTED='c9ec931753552d23473bba8baa7cd3b1194eb1bac1bbf075e977c50f76d66035';assert hashlib.sha256(P.read_bytes()).hexdigest()==EXPECTED
L=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';s=importlib.util.spec_from_file_location('h',L);h=importlib.util.module_from_spec(s);s.loader.exec_module(h);b=h.conn(D/'baseline460.sqlite');spec=json.loads(P.read_text());assert h.state(b)=={'journal_head':460,'pending':0}
def native(rid):
 n=h.native(b,rid)
 for k,t in [('origins','origin'),('evidence','dependency')]:n[k]=[dict(x) for x in b.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
note='Versionsbundet befintligt underlag för just denna livsbildsbedömning; administrativa kopior räknas inte som oberoende röster.'
heads=dict(b.execute('select object_id,max(version) from revision group by object_id'));changes=[];con=[];errors=[];authorized={x['object']:x['version']+1 for x in spec['changes']}
for x in spec['changes']:
 oid=x['object'];assert heads.get(oid)==x['version'];old=native(h.current(b,oid));api=h.api(old);api['expectedVersion']=x['version'];checks=[]
 for f,edit in x['fields'].items():
  target=api if f in ['caveat','rationale','disposition','evidenceStatus'] else api['data'];assert target[f]==edit['old'],('Unexpected field match',oid,f);target[f]=edit['new'];checks.append({'field':f,'old':edit['old'],'new':edit['new']})
 for ref in x['support']:
  o,v=ref.rsplit('@',1);v=int(v);assert heads.get(o)==v,('Return Astra stale/unapplied support',oid,ref,heads.get(o));e={'object':o,'version':v,'role':'supports','note':note}
  if not any(a['object']==o and a['version']==v and a['role']=='supports' for a in api['evidence']):api['evidence'].append(e)
 changes.append(api);heads[oid]=x['version']+1;con.append({'object':oid,'version':x['version'],'old_native':old,'new_api':api,'fields':checks,'source_disposition':'revise','rationale':x['reason'],'support':x['support']})
for x in spec['newReviews']:
 assert x['id'] not in heads
 refs=[]
 for ref in x['evidenceRefsBaseline']:
  o,v=ref.rsplit('@',1);v=int(v);assert heads.get(o)==v or (o in authorized and v==authorized[o]-1),('Unexpected review rebind',o,v,heads.get(o));current=heads[o];refs.append({'object':o,'version':current,'role':'supports','note':note})
 api={'id':x['id'],'kind':'assessment','expectedVersion':None,'data':{'subject_id':x['subject'],'criteria':x['criteria'],'outcome':x['outcome'],'body':x['body']},'origins':[],'evidence':refs,'disposition':'recorded','evidenceStatus':None,'rationale':'T-0791 AC1–4: individuell livsbildsbedömning av befintligt accepterat underlag; ingen ny originalforskning.','caveat':'Avgränsad befintligmaterialgranskning. failed är livsbildens kunskapsutfall; identitet, Trädverkan och OWNER_CONFIRMED ändras inte. Ingen allmän källuttömning.'}
 changes.append(api);con.append({'object':x['id'],'version':None,'old_native':None,'new_api':api,'fields':[{'field':'new_object','old':None,'new':api}],'source_disposition':'create_life_review','rationale':api['rationale'],'support':refs})
operation={'id':'T-0791/current-four-life-and-exact-semantic-corrections-v1','actor':'Codex/Sol-literal-Astra-T0791','reason':'T-0791 AC1–4: fyra individuella befintligmaterialbedömningar och exakta aktuella följdrättelser; inga nya original/katalogsökningar.','dependencyReviewVersion':2,'changes':changes}
raw=json.dumps(operation,ensure_ascii=False,indent=2)+'\n';opPath=D/'candidate-operation-v2.json';assert not opPath.exists();opPath.write_text(raw);retains=[]
for x in spec['individualDispositions']:
 if x['object'] in authorized:continue
 rid=f"{x['object']}@{x['version']}";assert h.current(b,x['object'])==rid;retains.append({'revision_id':rid,'old_native':native(rid),'source_disposition':'retain','rationale':x['reason'],'exact_field':x['field'],'individual_decision':x['decision']})
table={'task':'T-0791','candidate_source_pin':{'path':str(P.relative_to(R)),'sha256':EXPECTED},'operation_sha256':hashlib.sha256(opPath.read_bytes()).hexdigest(),'changes':con,'retains':retains,'individual_dispositions':spec['individualDispositions'],'protected':spec['protected'],'evidence_order':'Existing complete native origins/evidence retained in rowid order; only explicitly approved source edges appended; matching existing edge retained with original note.'};tablePath=D/'individual-consequence-table-v2.json';assert not tablePath.exists();tablePath.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');b.close();print(json.dumps({'changes':len(changes),'retains':len(retains),'operation_sha256':table['operation_sha256'],'table_sha256':hashlib.sha256(tablePath.read_bytes()).hexdigest()}))
