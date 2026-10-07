"""Literal source plan materialization only. No stage-media/apply."""
from pathlib import Path
import json,copy,importlib.util,datetime,time
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0795/preparation';start=time.monotonic()
s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
planp=R/'evaluations/T-0795/source-review/primary-literal-field-plan-v2.json';specp=R/'evaluations/T-0795/source-review/native-six-spec-v2.json'
assert h.sha(planp)=='2ebdb4da8121fd5cba6ede63c8e5de61555e1f3e70927d6eefa2ba3cdb4c7905';assert h.sha(specp)=='3845e5daaa1dd64f18a7904ec8e5504bd0c0e5d21b2144106ce58bce66aaa48f'
plan=json.loads(planp.read_text());spec=json.loads(specp.read_text());c=h.conn(O/'baseline-j457.sqlite');main=h.conn(R/'genealogy2/data/research.sqlite');assert h.state(main)==h.state(c)=={'journal_head':457,'pending':0};assert h.all50(main)==h.all50(c)
out=O/'literal-package-v1';assert not out.exists();out.mkdir();targets={};table=[];anomalies=[]
new=copy.deepcopy(spec['changes']);newids={x['id'] for x in new}
for x in new:
 assert c.execute('select count(*) from object where id=?',(x['id'],)).fetchone()[0]==0
 for e in x.get('evidence',[]):
  if e['object'] not in newids:
   actual=h.current(c,e['object']);assert actual==e['object']+'@'+str(e['version']),(x['id'],e,actual)
for row in plan['rows']:
 n=h.native(c,row['revision']);assert n==h.native(main,row['revision']);assert h.current(c,row['object_id'])==row['revision'] and n['version']==row['version']
 field=row['field'];full='data + disposition + evidence_status + rationale + caveat + evidence + origins'
 if field==full:actual=n
 elif field.startswith('data.'):actual=n['data'][field[5:]]
 else:actual=n[field]
 # Full retains express their complete native source payload.
 if actual!=row['old']:
  anomalies.append({'object':row['object_id'],'field':field,'actual':actual,'specified_old':row['old']});continue
 if row['disposition']=='revise':
  if row['object_id'] not in targets:
   a=h.api(n);a['expectedVersion']=n['version'];targets[row['object_id']]={'old_native':n,'old_api':copy.deepcopy(a),'new_api':a,'rows':[]}
  t=targets[row['object_id']];a=t['new_api']
  if field.startswith('data.'):a['data'][field[5:]]=row['new']
  else:a[field]=row['new']
  t['rows'].append(row)
  for rid in row['evidence']:
   oid,ver=rid.rsplit('@',1);edge={'object':oid,'version':int(ver),'role':'supports','note':row['rationale']}
   if not any(e['object']==oid and e['version']==int(ver) and e['role']=='supports' for e in a['evidence']):a['evidence'].append(edge)
 table.append({'source_row':row,'actual_native':n,'literal_match':True})
if anomalies:
 h.write(out/'STOP-old-field-discrepancies.json',anomalies);raise AssertionError(('Return to Astra',len(anomalies)))
changes=new+[t['new_api'] for t in targets.values()]
rebind=[]
for a in changes:
 for e in a.get('evidence',[]):
  if e['object'] in targets:rebind.append({'dependent':a['id'],'basis':e,'new_version':targets[e['object']]['new_api']['expectedVersion']+1})
h.write(out/'evidence-version-return-to-Astra.json',rebind)
# No operation staged until every evidence rebind is decided explicitly.
op={'id':'T0795-six-metadata-and-literal-consequences-v1','actor':'Codex/Sol-literal-Astra-source-plan','reason':'T-0795 AC2–4: sex avgränsade metadatautfall och exakta följdrättelser; inga personoriginal eller nya personfakta.','dependencyReviewVersion':2,'changes':changes}
h.write(out/'operation-DRAFT-no-media.json',op);h.write(out/'individual-consequence-table.json',{'source_plan':h.pin(planp),'rows':table,'targets':list(targets.values()),'retains':sum(r['disposition']=='retain' for r in plan['rows']),'version_rebinds_pending':rebind})
for m in spec['media_to_stage']:assert h.sha(R/m['path'])==m['sha256']
h.write(out/'six-media-stage-plan.json',spec['media_to_stage'])
h.write(out/'preparation-explicit-scope-amendment.json',{'original_manifest':h.pin(O/'current-input-manifest-v1.json'),'amendment':'Generic preparation PK_scope describes requested initial life-picture availability only. Actual T0795 semantic consequence plan includes PK06,PK08,PK12 revisions and PK03,PK04,PK10 retains; all12 current PK and full research were captured. This changes no review grade or canonical state.','effective_P_ids':['P-0212'],'actual_plan':h.pin(planp)})
h.write(out/'result.json',{'changes':len(changes),'new':len(new),'revisions':len(targets),'source_rows':len(table),'rebinds':rebind,'stage_media':False,'apply':False,'elapsed_seconds':time.monotonic()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[h.pin(p) for p in sorted(out.iterdir())]});print({'changes':len(changes),'revisions':len(targets),'rebinds':len(rebind)})
