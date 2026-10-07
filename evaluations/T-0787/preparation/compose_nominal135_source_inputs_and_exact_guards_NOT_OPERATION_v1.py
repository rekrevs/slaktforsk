"""Readonly settled source135 input composition only; no CLI/operation/stage."""
from pathlib import Path
import json,copy,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
proofp=O/'fresh447-physical-backup-full50-logical-equality-and-protected42-proof-v1.json';assert h.sha(proofp)=='b26805071faa41f0d5abf982b87c80202831a058a378890c7425b540e095161c';proof=json.loads(proofp.read_text());bp=R/proof['baseline_pin']['path'];assert h.sha(bp)==proof['baseline_pin']['sha256'];c=h.conn(bp)
D=R/'evaluations/T-0787/source-review'
files=[('fifteen-core-source-and-current-identity-copy-exact-fields-spec-v5.json','928f6d760a530500661fb9125a32e69c8813e45489f6f3d8e12195ade1340b58'),('finite-necessary-current-copy-exact-fields-spec-v5.json','5f88a6ea51b3121d99871969939fa4f059d55c392b5e8cbaf72998d21f8db887'),('eight-direct-incoming-small-current-copy-exact-source-spec-v1.json','73d8dfc884f75a6c1bc591dd8eb322880f47fccc8c3f86b51f10f0ecd5ff7ee4')]
rows=[];pins=[];byid={};heads={};issues=[];already=[];applied=[];assetdefaults=[]
for fn,digest in files:
 p=D/fn;assert h.sha(p)==digest;j=json.loads(p.read_text());pins.append(h.pin(p))
 for i,v in enumerate(j['rows']):
  oid=v['object_id'];assert oid not in byid;rid=oid+'@'+str(v['expected_version']);assert h.current(c,oid)==rid;n=h.native(c,rid);assert n==v['whole_old_native'];a=h.api(n);a['expectedVersion']=v['expected_version'];old=copy.deepcopy(a)
  for f in v['field_edits']:
   target=a;keys=f['field'].split('.')
   for key in keys[:-1]:target=target[key]
   assert target[keys[-1]]==f['old'],(oid,f['field']);target[keys[-1]]=copy.deepcopy(f['new'])
  for rb in v.get('evidence_rebinds',[]):
   if 'old' in rb:
    before,after=rb['old'],rb['new'];idx=[ix for ix,e in enumerate(a['evidence']) if e==before];assert len(idx)==1;assert before['object']==after['object'] and before['role']==after['role'] and before['note']==after['note'];a['evidence'][idx[0]]=copy.deepcopy(after)
   else:
    idx=[ix for ix,e in enumerate(a['evidence']) if (e['object'],e['version'],e['role'])==(rb['basis_object_id'],rb['old_version'],rb['role'])];assert len(idx)==1;a['evidence'][idx[0]]['version']=rb['new_version']
  for e in v.get('evidence_additions',[]):
   assert not any((e['object'],e['version'],e['role'])==(z['object'],z['version'],z['role']) for z in a['evidence']);a['evidence'].append(copy.deepcopy(e))
  r={'object_id':oid,'source_spec_pin':h.pin(p),'source_row_pointer':'/rows/'+str(i),'full_old_native':n,'full_old_API':old,'proposed_full_API_NOT_OPERATION':a,'source_literal_row':v,'explicit65_edge_amendments':[]};rows.append(r);byid[oid]=r
assert len(rows)==129
p=D/'sixty-five-individual-incoming-source-consequence-and-explicit-rebind-dispositions-v1.json';assert h.sha(p)=='d2f9e9e5dbdd55dad7bbc573afb3bc078a61bfce21bb64c3a521a63b3dce2420';j=json.loads(p.read_text());pins.append(h.pin(p))
for i,v in enumerate(j['explicit_current_revised_caller_evidence_amendments']):
 oid=v['caller_object_id'];r=byid[oid];a=r['proposed_full_API_NOT_OPERATION'];assert a['expectedVersion']==v['caller_expected_version'];o=v['old_edge'];basis,ver=o['basis_revision_id'].rsplit('@',1);before={'object':basis,'version':int(ver),'role':o['role'],'note':o['note']};after=v['new_edge'];assert before['object']==after['object'] and before['role']==after['role'] and before['note']==after['note'];assert r['full_old_API']['evidence'].count(before)==1
 oldidx=[k for k,e in enumerate(a['evidence']) if e==before];newidx=[k for k,e in enumerate(a['evidence']) if e==after]
 if oldidx:assert len(oldidx)==1 and not newidx;a['evidence'][oldidx[0]]=copy.deepcopy(after);state='applied_exact_once';applied.append(i)
 else:assert len(newidx)==1;state='already_identical_explicit_rebind_no_duplicate';already.append(i)
 r['explicit65_edge_amendments'].append({'source_pin':h.pin(p),'pointer':'/explicit_current_revised_caller_evidence_amendments/'+str(i),'state':state,'full_old_API_edge':before,'full_new_API_edge':after})
for fn,digest in [('four-new-individual-identity-and-tree-full-API-source-spec-v1.json','9cd8bad6845045f8d328ee4b6a067ca1b589541fe26c54baa9a126992ff22be9'),('exact3011-physical-record-and-negative-search-full-API-source-spec-v1.json','4a13a8992af05a37f0977ab350e41292ae5882f6669461a29facfea2607816ed')]:
 p=D/fn;assert h.sha(p)==digest;j=json.loads(p.read_text());pins.append(h.pin(p))
 for i,v in enumerate(j['rows']):
  a=copy.deepcopy(v['full_new_API']);oid=a['id'];assert oid not in byid and a['expectedVersion'] is None;assert not c.execute('select id from object where id=?',(oid,)).fetchone();assert not c.execute('select id from revision where object_id=?',(oid,)).fetchone()
  if a['kind']=='assessment':assert set(a['data'])=={'subject_id','criteria','outcome','body'}
  if a['kind']=='search':assert a['data']['scope_json']['description'] and a['data']['scope_json']['query'] and isinstance(a['data']['scope_json']['bounds'],dict) and a['data']['scope_json']['bounds'] and a['data']['outcome']=='negative'
  if a['kind']=='record' and 'assets' not in a:assetdefaults.append({'object_id':oid,'explicit_source_API_assets':'omitted','native_full_API_assets_default':[],'source_or_root_explicit_normalization_disposition_required_before_actual_API_compare':True,'source_pin':h.pin(p),'source_pointer':'/rows/'+str(i)+'/full_new_API'})
  r={'object_id':oid,'source_spec_pin':h.pin(p),'source_row_pointer':'/rows/'+str(i),'full_old_native':None,'expected_absent_exact':True,'proposed_full_API_NOT_OPERATION':a,'source_literal_row':v};rows.append(r);byid[oid]=r
assert len(rows)==135
media=copy.deepcopy(j['media_registration_API']);mp=R/'evaluations/T-0786/resume-current446-v1/actual-3011-stage-media-root-authorized-output-v1.json';assert media==json.loads(mp.read_text());assert h.sha(R/media['storagePath'])==media['sha256'];assert (R/media['storagePath']).stat().st_size==media['bytes'];assert not c.execute('select id from native_asset where id=?',(media['id'],)).fetchone()
for index,r in enumerate(rows):
 a=r['proposed_full_API_NOT_OPERATION'];assert a['id']==r['object_id'];oid=a['id'];expected=a['expectedVersion'];assert expected==(heads.get(oid) if oid in heads else (int(h.current(c,oid).rsplit('@',1)[1]) if expected is not None else None))
 for e in a['evidence']:
  actual=heads.get(e['object']);actual=actual if actual is not None else int(h.current(c,e['object']).rsplit('@',1)[1])
  if actual!=e['version']:issues.append({'index':index,'target':oid,'edge':e,'actual_expected_current_basis_head':actual,'no_inferred_rebind':True})
 if a['kind']=='record':
  sid=a['data']['source_id'];assert any(e['object']==sid for e in a['evidence']) or a.get('bindings',{}).get(sid)==int(h.current(c,sid).rsplit('@',1)[1])
 if a['kind']=='record' and a.get('media'):
  for ref in a['media']:assert ref['id']==media['id'] or c.execute('select id from native_asset where id=?',(ref['id'],)).fetchone()
 heads[oid]=(expected or 0)+1
protected=json.loads((R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json').read_text())['objects'];assert not set(byid).intersection(n['object_id'] for n in protected.values())
stronger={rid:h.native(c,rid) for rid in ['TR-68c6e60879784dec2253a77a@2','R-f0daaefd9c25840abc871c44@1']}
assert h.current(c,'TR-68c6e60879784dec2253a77a')=='TR-68c6e60879784dec2253a77a@2' and h.current(c,'R-f0daaefd9c25840abc871c44')=='R-f0daaefd9c25840abc871c44@1';assert h.sha(bp)==proof['baseline_pin']['sha256']
out=h.write(O/'nominal135-individual-source-API-input-composition-and-exact-support-media-guards-NOT-OPERATION-v1.json',{'task':'T-0787','status':'MECHANICAL_INPUT_ONLY_PENDING_28_FANOUT_SOURCE_DISPOSITIONS_AND_POSSIBLE_BIRTH_TARGET','baseline_proof_pin':h.pin(proofp),'source_pins':pins,'rows':rows,'source135_nominal_order':list(byid),'media_registration_API_NOT_OPERATION':media,'media_staging_API_pin':h.pin(mp),'sequential_head_issues':issues,'source65_explicit22_application':{'applied_once_count':len(applied),'already_identical_count':len(already),'all22accounted':len(applied)+len(already)==22},'native_API_default_representation_questions':assetdefaults,'T0675_exact_current_stronger_support_native':stronger,'T0675_scope_reading_credit':'Exactcurrentnative/head binding only; earlier own accepted fullsource receipts remain reading authority','counts':{'nominal_targets':135,'existing_revisions':129,'new_review_objects':4,'new_record_and_search':2,'new_media':1,'head_issues':len(issues)},'no_operations_stage_canonical_or_Wotan_mutation':True,'final_source_or_independent_globalapproval_not_inferred':True,'usage':'UNKNOWN pending root collector'})
print(json.dumps({'input_pin':out,'targets':135,'head_issues':issues,'explicit22':{'applied':len(applied),'already':len(already)},'schema_questions':assetdefaults}));c.close()
