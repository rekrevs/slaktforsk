import pathlib,json,sqlite3,hashlib,datetime,native_payload
B=pathlib.Path(__file__).resolve().parent
native_payload.connection=sqlite3.connect('file:'+str(B/'clone/research-candidate-v4.sqlite')+'?mode=ro',uri=True);native_payload.connection.row_factory=sqlite3.Row
source=json.loads((B/'source-decisions/C-0083-initial-source-v1.json').read_text());decision=json.loads((B/'source-decisions/C-0083-initial-decisions-v1.json').read_text());rid=source['record_version'].rsplit('@',1)[0];changes=[];table=[]
grouped={}
for edit in decision['native_changes']:
 obj=grouped.setdefault(edit['id'],native_payload.existing(edit['id'],edit['expectedVersion']));field=edit['field']
 if field.endswith('_json'):
  raw=native_payload.rows('select '+field+' from '+obj['kind']+' where revision_id=?',(edit['id']+'@'+str(edit['expectedVersion']),))[0][field]
  assert raw==edit['before'];obj['data'][field]=json.loads(edit['after']);count=1
 else:
  count=obj['data'][field].count(edit['before']);assert count==edit['expected_match_count'],(edit['id'],field,count)
  obj['data'][field]=obj['data'][field].replace(edit['before'],edit['after'],1)
 for binding in edit.get('approved_support',[rid+'@1']):
  oid,ver=binding.rsplit('@',1)
  if not any(e['object']==oid and e['version']==int(ver) for e in obj['evidence']):obj['evidence'].append({'object':oid,'version':int(ver),'role':'supports','note':'T-0776: individuellt Astra-prövad dokumentär konsolidering; ingen ytterligare originalöppning.'})
 table.append({**edit,'actual_match_count':count,'disposition':'revise'})
for obj in grouped.values():obj['rationale']+=' '+decision['operation_reason'];changes.append(obj)
def ev(oid,version,note):return {'object':oid,'version':version,'role':'supports','note':note}
bases=[ev(rid,1,'Samma födelse-/doporiginal och tidigare fullutvinning, ingen extra historisk röst.'),ev('S-0008',1,'Versionsbunden källmetadata.')]
def new(oid,kind,data,evidence,caveat):
 assert not native_payload.rows('select id from object where id=?',(oid,));changes.append({'id':oid,'kind':kind,'expectedVersion':None,'data':data,'origins':[],'evidence':evidence,'disposition':'recorded','evidenceStatus':None,'rationale':decision['operation_reason'],'caveat':caveat})
aid='AUDIT-T0776-C0083';new(aid,'assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_limits','body':json.dumps({'source':source,'initial_decisions':decision},ensure_ascii=False,indent=2)},bases,decision['protected'])
for pid,role,cols in [('P-0015','father',[9,10]),('P-0117','mother',[9,10,11,12,13,14,20,21]),('P-0119','child',[1,2,3,4,5,6,7,8,15,16,17,18,19,21])]:
 new('ADOPT-T0776-C0083-'+pid,'assessment',{'subject_id':pid,'criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':json.dumps({'person':pid,'role':role,'scope':source['scope'],'own_source_fields':[f for f in source['fields'] if f['column'] in cols],'adoption':decision['new_objects'][1]['instruction'],'normalization':source['normalization'],'diplomatic_limits':source['diplomatic_limits'],'identity_limits':source['identity_limits'],'reuse_ground':source['reuse_ground']},ensure_ascii=False,indent=2)},bases+[ev(aid,1,'Personens egen roll i full födelse-/doppost; övriga personer har separata roller.')],decision['protected'])
op={'id':'T-0776/C0083-initial-candidate-v1','actor':'Codex Sol mechanical implementation of settled Astra decisions','reason':'T-0776 AC2–4: full födelse-/doppost med 21 tryckta fält, tre individuella adoptioner och precis föräldrabostadsrättelse; kontrollerad kanonisk införsel efter självständig slutgranskning.','dependencyReviewVersion':2,'changes':changes}
def save(name,x):(B/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
save('C-0083-initial-candidate-operation-v1.json',op);save('C-0083-initial-consequence-table-v1.json',{'rows':table,'remaining_consequences':'Awaiting exact primary Astra handoff; not implicitly retained.'})
files=['C-0083-initial-candidate-operation-v1.json','C-0083-initial-consequence-table-v1.json','source-decisions/C-0083-initial-decisions-v1.json','source-decisions/C-0083-initial-source-v1.json']
save('C-0083-first-candidate-freeze-v1.json',{'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_head':251,'status':'initial_candidate_before_testing_not_final','files':[{'path':str(B/f),'sha256':hashlib.sha256((B/f).read_bytes()).hexdigest()} for f in files]});print(len(changes),'initial changes')
