import json,pathlib,hashlib,copy,sys
B=pathlib.Path('evaluations/T-0781');O=B/'independent-review'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
p=pathlib.Path(sys.argv[1]);new=rd(p);oldp=B/'implementation/complete-two-source-settled-draft-package-v2/complete-two-source-draft-package-proposal-v1.json';old=rd(oldp);sp=B/'source-review/ten-exact-current-record-support-version-amendments-v1.json';s=rd(sp);by={r['consumer_object_id']:r for r in s['rows']};rows=[];ops=[]
for a,b in zip(old['operations'],new['operations']):
 aa=rd(a['path']);bb=rd(b['path']);assert pin(a['path'])['sha256']==a['sha256'];assert pin(b['path'])['sha256']==b['sha256'];expected=copy.deepcopy(aa)
 for i,c in enumerate(aa['changes']):
  if c['id'] not in by:continue
  r=by[c['id']];ei=r['edge_index'];assert c==r['entire_before_candidate_API'];assert c['evidence'][ei]==r['old_exact_API_edge'];expected['changes'][i]['evidence'][ei]=r['new_exact_API_edge'];assert expected['changes'][i]==r['entire_after_candidate_API'];assert bb['changes'][i]==expected['changes'][i]
  oldedge=r['old_exact_API_edge'];newedge=r['new_exact_API_edge'];assert oldedge['version']==1 and newedge['version']==2;assert {k:v for k,v in oldedge.items() if k!='version'}=={k:v for k,v in newedge.items() if k!='version'}
  rows.append({'object_id':c['id'],'prior_operation':pin(a['path']),'actual_operation':pin(b['path']),'actual_pointer':'/changes/'+str(i),'exact_old_edge':oldedge,'exact_new_edge':newedge,'edge_index':ei,'source_disposition_pointer':'/rows/'+str(s['rows'].index(r)),'own_judgment':'APPROVE_EXACT_INDIVIDUAL_SAME_CANDIDATE_SUPPORT_VERSION_REBIND','own_source_consequence':r['source_reason'],'only_exact_version_field_changed':True,'entire_current_and_prior_candidate_reading_reused':True,'all_other_entire_API_data_caveat_metadata_origins_ordered_supports_unchanged':True})
 assert bb==expected,(a['path'],b['path']);ops.append({'old':pin(a['path']),'new':pin(b['path']),'whole_operation_equal_except_explicit_source_version_fields':True})
assert len(rows)==10
out={'task':'T-0781','status':'EXACT_TEN_INDIVIDUAL_SUPPORT_VERSION_AMENDMENTS_PASS','source_spec':pin(sp),'prior_package':pin(oldp),'actual_package':pin(p),'rows':rows,'whole16_operation_equality_proofs':ops,'stronger_C69_own_prior_reuse':pin(O/'five-stronger-prior-own-reading-current425-reuse-dispositions-v1.json'),'own_R49_full_current_candidate_review':pin(O/'C0049-core-five-pass-one-metadata-pending-and-P0098-API-review-v1.json'),'limits':'Ten NEW candidate version edges only; old immutable native versions and unrelated current O50name/F50occupation/ID52/53 retain old exact bases. Same source image/registration chain, no new independent voice or original rereading. Prior blanket old-basis instructions for these ten new candidates superseded explicitly, not silently.','runtime_authority':False,'global_PASS':False}
q=O/'ten-exact-support-version-actual-API-independent-review-v1.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(q))
