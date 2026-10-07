import pathlib,json,hashlib,copy,time,sqlite3
start=time.time();w=pathlib.Path('evaluations/T-0780/implementation');out=w/'C0685-C0563-split-proposal-v1';out.mkdir(exist_ok=True);sp=pathlib.Path('evaluations/T-0780/source-review/C0563-five-explicit-operation-split-decisions-v1.json');sha='3852af4610d512b657f56deac8246c22b78876a2a64a653c281f440806effd41';assert hashlib.sha256(sp.read_bytes()).hexdigest()==sha;sd=json.load(open(sp));assert hashlib.sha256(pathlib.Path(sd['constraint_input']['path']).read_bytes()).hexdigest()==sd['constraint_input']['sha256']
folders=['C0563-settled-queue-v1','C0563-additional-settled-queue-v1','C0563-semantic-settled-queue-v1'];modules={}
for folder in folders:
 for f in (w/folder).glob('*operation-v1.json'):modules[f.name.removesuffix('-operation-v1.json')]=(f,json.load(open(f)))
for f in (w/'C0685-v1').glob('*operation-v2.json'):modules['C0685-'+f.name.removesuffix('-operation-v2.json')]=(f,json.load(open(f)))
newgroups={};preservation=[]
def split(key,part,ids):
 f,op=modules[key];chs=[c for c in op['changes'] if c['id'] in ids];assert len(chs)==len(ids)
 n=copy.deepcopy(op);n['id']=op['id']+'-explicit-'+part+'-v1';n['reason']=op['reason']+' Source-approved payload-preserving operation split '+sha+'; proposed sequence awaits primary binding.';n['changes']=chs;newgroups[part]=(f,n)
 for ch in chs:preservation.append({'object_id':ch['id'],'original_module':str(f),'original_payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'split_group':part,'split_payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'entire_payload_and_order_preserved':True})
f,op=modules['father-wife-column'];audit={c['id'] for c in op['changes'] if c['expectedVersion'] is None};split('father-wife-column','C0563-father-audit',audit);split('father-wife-column','C0563-father-revisions',{c['id'] for c in op['changes']}-audit)
f,op=modules['selected22-mention-observation'];oids={i['dependent'] for i in sd['five_split_decisions'] if i['dependent'].startswith('O-')};split('selected22-mention-observation','C0563-observations-before-mentions',oids);split('selected22-mention-observation','C0563-mentions-after-old-basis-dependents',{c['id'] for c in op['changes']}-oids)
f,op=modules['selected44-path-theme'];trids={i['dependent'] for i in sd['five_split_decisions'] if i['dependent'].startswith('TR-')};rid={'R-521806d99b24fc04d967d271'};split('selected44-path-theme','C0563-historical-transcriptions-before-record',trids);split('selected44-path-theme','C0563-final-record-metadata',rid);split('selected44-path-theme','C0563-path-theme-revisions',{c['id'] for c in op['changes']}-trids-rid)
# Concrete deliberate proposal, not automatic operation sorting. All source-approved old bases remain exact.
order=['full-transcription','C0685-original-transcription','C0685-source-audit','C0563-father-audit','C0563-father-revisions','selected45-contract-identity','C0563-observations-before-mentions','C0563-historical-transcriptions-before-record','C0563-mentions-after-old-basis-dependents','selected30-key-question','C0563-path-theme-revisions','READ-boundary-three','sixteen-person-adoption','sixteen-question-path-research','P0471-consequence-adoption','seventeen-key','fifteen-theme','three-biography-semantic','Emanuel-health-semantic','C0561-C0685-Johan-biography-combined','C0685-source-metadata','C0685-records','C0685-mentions','C0685-observations','C0685-consequences','C0685-bounded-adoptions','C0563-final-record-metadata']
seq=[];allchanges=[]
for index,key in enumerate(order,1):
 f,op=newgroups.get(key,modules.get(key));target=out/(str(index).zfill(2)+'-'+key+'-operation-v1.json');assert not target.exists();target.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');seq.append({'index':index,'path':str(target),'operation_id':op['id'],'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_module':str(f),'targets':[{'id':ch['id'],'expectedVersion':ch['expectedVersion'],'nextVersion':(ch['expectedVersion'] or 0)+1,'entire_payload_sha256':hashlib.sha256(json.dumps(ch,ensure_ascii=False,sort_keys=True).encode()).hexdigest()} for ch in op['changes']]});allchanges.extend((index,ch) for ch in op['changes'])
assert len(allchanges)==151 and len({ch['id'] for _,ch in allchanges})==151
c=sqlite3.connect('file:evaluations/T-0780/preparation/baseline-j281.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row;heads={r['object_id']:r['version'] for r in c.execute('select object_id,max(version) version from revision group by object_id')};violations=[];supports=0
for pin in seq:
 op=json.load(open(pin['path']));produced={ch['id']:(ch['expectedVersion'] or 0)+1 for ch in op['changes']}
 for ch in op['changes']:
  assert heads.get(ch['id'])==ch['expectedVersion'];heads[ch['id']]=(ch['expectedVersion'] or 0)+1
  for e in ch['evidence']:
   assert set(e)=={'object','version','role','note'} and isinstance(e['version'],int);supports+=1
   if heads.get(e['object'])!=e['version']:violations.append({'operation':op['id'],'target':ch['id'],'edge':e,'head_at_write':heads.get(e['object'])})
 for ch in op['changes']:
  for e in ch['evidence']:
   if e['object'] in produced and produced[e['object']]!=e['version']:violations.append({'operation':op['id'],'target':ch['id'],'within_operation_stale':e})
# Exact approved payload inventory covers every module target once; splitting never changes target payloads.
sourcechanges=[ch for _,op in modules.values() for ch in op['changes']];assert len(sourcechanges)==len(allchanges);actual={ch['id']:ch for _,ch in allchanges};assert all(actual[ch['id']]==ch for ch in sourcechanges)
r={'task':'T-0780','scope':'C0685 and currently settled C0563 ONLY; concrete partial proposal, not full10 readiness','source_split_sha256':sha,'sequence':seq,'unique_native_changes':151,'support_api_entries_checked':supports,'sequence_violations':violations,'all_original_target_payloads_preserved_exactly':True,'individual_split_payload_hashes':preservation,'stage_or_canonical_applies':0,'failed_attempts':0,'elapsed_seconds':time.time()-start,'status':'RETURN_PRIMARY_EXACT_SEQUENCE_HASH_APPROVAL_REQUIRED','not_ready_scopes':['C0561 whole','C0425','C0060','C0069'],'no_automatic_rebind_or_source_adjudication':True};(out/'concrete-sequence-and-preservation-receipt-v1.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'targets':151,'operations':len(seq),'violations':violations,'manifest_sha':hashlib.sha256((out/'concrete-sequence-and-preservation-receipt-v1.json').read_bytes()).hexdigest()}))
