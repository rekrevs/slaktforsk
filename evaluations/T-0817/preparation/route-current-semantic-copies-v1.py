from pathlib import Path
import json,re,hashlib,importlib.util,time
R=Path.cwd();D=R/'evaluations/T-0817';P=D/'preparation';start=time.monotonic();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);main=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(main)=='f73c9599c70b2938b581593c1250995122d79bfa4451e72be1e040cc6c339d0e';c=h.conn(main);assert h.state(c)=={'journal_head':484,'pending':0}
def save(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def fields(v,path=''):
 if isinstance(v,dict):
  for k,x in v.items():yield from fields(x,path+'.'+k if path else k)
 elif isinstance(v,list):
  for j,x in enumerate(v):yield from fields(x,path+f'[{j}]')
 else:yield path,v
patterns={'exact_shared_review_phrase':re.compile(re.escape('Både identitets- och livsbildsnivå förblir UNDERKÄND')),'shared_review_phrase_variant':re.compile(r'identitets.{0,35}livsbild.{0,40}UNDERKÄND',re.I),'exact_C0446':re.compile(r'C-?0446|C0043834_00110|R-508b3628d54f6430658fa240',re.I),'own_material_page_bound':re.compile(r'Hemsj[oö].{0,70}(?:s\.?\s*98|sida\s*98)|(?:s\.?\s*98|sida\s*98).{0,70}Hemsj[oö]',re.I)}
records=[]
for kindrow in c.execute('select distinct kind from object'):
 kind=kindrow['kind'];rows=c.execute('select r.*,d.* from current_revision r join "'+kind+'" d on d.revision_id=r.id').fetchall()
 for row in rows:
  raw=dict(row);matched=[]
  for path,val in fields(raw):
   if not isinstance(val,str):continue
   hits=[key for key,rx in patterns.items()if rx.search(val)]
   if hits:matched.append({'field':path,'full_old_value':val,'literal_locator_hits':hits})
   if path.endswith('_json'):
    try:decoded=json.loads(val)
    except ValueError:continue
    for nested,nv in fields(decoded,path+'(decoded)'):
     if isinstance(nv,str):
      hits=[key for key,rx in patterns.items()if rx.search(nv)]
      if hits:matched.append({'field':nested,'full_old_value':nv,'literal_locator_hits':hits,'serialized_parent_field_preserved':path})
  if matched:
   n=h.native(c,row['id']);basis=[]
   for e in n['evidence']:
    old=h.native(c,e['basis_revision_id']);now=h.native(c,h.current(c,old['object_id']));basis.append({'old_edge':e,'bound_revision':old['id'],'current_stronger_revision':now['id'],'current_stronger_native':now})
   records.append({'object_id':n['object_id'],'current_revision':n['id'],'full_current_native':n,'matching_fields':matched,'exact_basis_and_current_stronger':basis,'routing_only_no_source_disposition':True})
locked=json.load(open(P/'native-support-versions-v1.json'));baseline=[]
for old in locked['revisions']:
 n=h.native(c,old['id']);assert n['id']==old['id'];baseline.append({'revision_id':n['id'],'current_head_revision':h.current(c,n['object_id']),'is_current_head':h.current(c,n['object_id'])==n['id'],'full_native':n,'full_field_inventory':[{'field':path,'old_value':v}for path,v in fields(n) if path.startswith('data.')or path in['caveat','rationale','disposition','evidence_status']]})
assert len(baseline)==385
save('full385-bound-current-native-field-inventory-v1.json',{'revisions':baseline,'qualification':'385 exact locked bound/current revisions, not 385 certified current people/heads. Full fields are inputs; no interpretation or correction.'})
save('current-global-semantic-copy-routing-v1.json',{'candidates':records,'patterns':{k:v.pattern for k,v in patterns.items()},'current_head_only':True,'source_scope':'Exact C0446/own-row wording and requested shared identity/LIFE phrase; no source audit or evidence judgment','unmatched_patterns':[k for k in patterns if not any(k in f['literal_locator_hits']for r in records for f in r['matching_fields'])],'zero_hits_are_locator_results_not_source_absence':True,'array_order_preserved':True})
focal=json.load(open(P/'native/P-0337.json'));child=json.load(open(P/'native/P-0287.json'));ownerpath=R/'evaluations/T-0813/preparation/all-current-OWNER-scope-v1.json';owner=json.load(open(ownerpath));owners=[]
for x in owner['OWNER_full_native']:
 assert h.current(c,x['object_id'])==x['id'];owners.append(h.native(c,x['id']))
inv=json.load(open(R/'evaluations/T-0815/root-actual-inventory-full-v2.json'));axes=[{'person':x['id'],**{k:x.get(k)for k in ['identityGate','identityReview','treeEffect','lifePictureReview','stopReasons']}}for x in inv['people']]
rels={x['object_id']:h.native(c,x['id'])for x in focal['current']+child['current']if x['kind']=='relation'}
save('protected-native-review-snapshot-v1.json',{'current_OWNER45_fullnative':owners,'protected_child_fullnative':child,'focal_fullnative':focal,'all536_review_axes':axes,'relations_fullnative':list(rels.values()),'baseline_all50':'evaluations/T-0817/preparation/baseline-all50-v1.json','historical_scope_qualification':'Legacy fullcontract remains distinct from native LIFE; snapshot only, no upgrade or downshift'})
assert sha(main)=='f73c9599c70b2938b581593c1250995122d79bfa4451e72be1e040cc6c339d0e';save('semantic-routing-result-v1.json',{'candidate_objects':len(records),'matched_fields':sum(len(x['matching_fields'])for x in records),'locked_bound_current_revisions':385,'OWNER45':len(owners),'protected_child_current_objects':len(child['current']),'relations':len(rels),'all_review_axes':len(axes),'main_unchanged':True,'native_or_queue_changes':0,'source_openings':0,'source_decisions':0,'elapsed_seconds':time.monotonic()-start});print(json.dumps({'candidates':len(records),'fields':sum(len(x['matching_fields'])for x in records),'elapsed_seconds':time.monotonic()-start}))
