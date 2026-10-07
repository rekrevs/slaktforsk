"""Only exact121 current/history/incoming and four suggested absent review schemas."""
from pathlib import Path
import importlib.util,json
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('proven',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
M=R/'genealogy2/data/research.sqlite';assert h.sha(M)=='1b551564c2067226be4083b52ee471c57268d719ad4aaa53b9d2dc2d43275e21';c=h.conn(M);assert h.state(c)=={'journal_head':447,'pending':0}
bp=R/'evaluations/T-0786/resume-current446-v1/baseline-j446.sqlite';b=h.conn(bp);assert h.sha(bp)=='1e8e6b4079df557d9dd904578178321381b6c2ef5d54ac15ff74eacdac942541'
files=[('fifteen-core-source-and-current-identity-copy-exact-fields-spec-v3.json','9b632920f0aaa6baf45981e1c0de7f0aed9b7d86a71e69e85e42effda7ca0b79'),('finite-necessary-current-copy-exact-fields-spec-v3.json','b8de718f1d474d486124897cb2483cefc977a5b6e5aed9be238af899b26ffe53')]
rows=[];incoming=[];callers={};pins=[];ids=set();formats=[];examples={}
for fn,digest in files:
 p=R/'evaluations/T-0787/source-review'/fn;assert h.sha(p)==digest;j=json.loads(p.read_text());pins.append(h.pin(p))
 for i,v in enumerate(j['rows']):
  oid=v['object_id'];assert oid not in ids;ids.add(oid);rid=oid+'@'+str(v['expected_version']);assert h.current(c,oid)==h.current(b,oid)==rid;n=h.native(c,rid);assert n==h.native(b,rid)==v['whole_old_native'];a=h.api(n);a['expectedVersion']=v['expected_version'];literal=[]
  for f in v['field_edits']:
   nn=n;aa=a;keys=f['field'].split('.')
   for key in keys:nn=nn[key];aa=aa[key]
   same_native=nn==f['old'];same_api=aa==f['old'];decoded=(json.loads(nn)==aa) if keys[-1].endswith('_json') and isinstance(nn,str) else None
   assert same_native or same_api,(oid,f['field'])
   item={'field':f['field'],'source_full_old':f['old'],'source_full_new':f['new'],'current_native_old':nn,'current_API_old':aa,'literal_native_old_equal':same_native,'literal_API_old_equal':same_api,'native_JSON_decoded_equals_API':decoded,'API_conversion_authorized':False if same_native and not same_api else None};literal.append(item)
   if same_native and not same_api:formats.append({'object_id':oid,**item,'source_spec_pin':h.pin(p),'source_row_pointer':'/rows/'+str(i)})
  hist=[dict(z) for z in c.execute('select id,version,previous_id,operation_id from revision where object_id=? order by version',(oid,))];edges=[]
  for history in hist:
   for r in c.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(history['id'],)):
    e=dict(r);caller=h.native(c,e['revision_id']);current=h.current(c,caller['object_id']);e.update({'changed_target_object_id':oid,'target_current_revision_id':rid,'basis_is_current':history['id']==rid,'caller_current_revision_id':current,'caller_is_current':e['revision_id']==current});edges.append(e);incoming.append(e);callers[caller['id']]=caller;callers[current]=h.native(c,current)
  rows.append({'source_spec_pin':h.pin(p),'source_row_pointer':'/rows/'+str(i),'object_id':oid,'current_revision_id':rid,'current_head_whole_old_equal_source_and_frozen446':True,'full_old_native':n,'full_current_API':a,'individual_literal_fields_and_API_representation':literal,'source_disposition':v.get('source_disposition',v.get('individual_source_disposition')),'source_3011_addendum':v.get('source_disposition_3011_addendum',v.get('individual_source_disposition_3011_addendum')),'proposed_evidence_rebinds':v.get('evidence_rebinds',[]),'proposed_evidence_additions':v.get('evidence_additions',[]),'history':hist,'all_history_incoming':edges,'incoming_source_disposition':v['incoming_disposition']})
assert len(ids)==121
absent={};axes={}
for person in ['P0241','P0246']:
 for axis in ['IDENTITY-REVIEW','TREE-EFFECT']:
  oid=axis+'-T0787-'+person;assert not c.execute('select id from object where id=?',(oid,)).fetchone();absent[oid]={'object_absent':True,'revision_history_absent':not c.execute('select id from revision where object_id=?',(oid,)).fetchone()}
for person in ['P-0241','P-0246','P-0003']:
 rr=[dict(z) for z in c.execute("select r.id,r.object_id,a.criteria from current_revision r join assessment a on a.revision_id=r.id where a.subject_id=? and a.criteria in ('identity_review/1','tree_effect/1') order by a.criteria",(person,))];axes[person]=rr
 for z in rr:examples[z['id']]={'full_current_native':h.native(c,z['id']),'schema_example_API':h.api(h.native(c,z['id']))}
protected=json.loads((R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json').read_text())['objects'];assert not ids.intersection(n['object_id'] for n in protected.values());assert len(protected)==42
for rid,n in protected.items():assert h.current(c,n['object_id'])==rid and h.native(c,rid)==n
assert h.sha(M)=='1b551564c2067226be4083b52ee471c57268d719ad4aaa53b9d2dc2d43275e21'
result=h.write(O/'exact121-current447-wholeold-native-API-field-sides-and-all-history-incoming-v1.json',{'task':'T-0787','main_pin':h.pin(M),'actual_state':h.state(c),'root_actual447_handoff_pin':h.pin(R/'evaluations/T-0786/root-controlled-postlogin-one-search-v1/complete-postlogin-one-search-actual447-handoff.json'),'prior446_baseline_pin':h.pin(bp),'source_spec_pins':pins,'rows':rows,'all_history_incoming':incoming,'full_incoming_exact_and_current_caller_native':callers,'four_suggested_review_ID_absence':absent,'existing_current_native_axes':axes,'whole_native_review_schema_examples':examples,'assessment_schema':'data: subject_id,criteria,outcome,body; creates expectedVersion null; orderedorigins/evidence, numericdependencyReviewVersion2. identity_review/1 passed|failed and tree_effect/1 supporting|waiting|non_supporting onlysource decides','structured_API_format_questions':formats,'media3011_API_pin':h.pin(R/'evaluations/T-0786/resume-current446-v1/actual-3011-stage-media-root-authorized-output-v1.json'),'counts':{'targets':121,'field_edits':sum(len(x['individual_literal_fields_and_API_representation']) for x in rows),'all_history_incoming':len(incoming),'current_basis_incoming':sum(e['basis_is_current'] for e in incoming),'current_basis_current_callers':sum(e['basis_is_current'] and e['caller_is_current'] for e in incoming),'caller_payloads':len(callers),'API_format_questions':len(formats)},'protected42_wholecurrent_exact':True,'fresh447_wholeold_heads_equal_frozen446':True,'source_grades_or_individual_incoming_retains_inferred':False,'operations_constructed':False,'stage_canonical_or_Wotan_mutation':False,'usage':'UNKNOWN pending root collector'})
print(json.dumps({'input_pin':result,'targets':121,'incoming':len(incoming),'caller_native':len(callers),'API_format_questions':len(formats),'four_new_IDs_absent':True}));c.close();b.close()
