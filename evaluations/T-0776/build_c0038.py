"""Exact field patches authorized by primary Astra; no interpretation."""
import pathlib,json,sqlite3,hashlib,datetime
B=pathlib.Path(__file__).resolve().parent
c=sqlite3.connect('file:'+str(B/'clone/research-candidate-v2.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
source=json.loads((B/'source-decisions/C-0038-source.json').read_text());decision=json.loads((B/'source-decisions/C-0038-decisions.json').read_text());rid=source['record_version'].rsplit('@',1)[0]
def rows(q,args=()):return [dict(r) for r in c.execute(q,args)]
def existing(oid,version):
 rev=rows('select * from current_revision where object_id=?',(oid,))[0];assert rev['version']==version
 kind=rev['kind'];data=rows('select * from '+kind+' where revision_id=?',(rev['id'],))[0];data.pop('revision_id')
 for k,v in data.items():
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 return {'id':oid,'kind':kind,'expectedVersion':version,'data':data,'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in rows('select * from origin where revision_id=?',(rev['id'],))],'evidence':[{'object':r['basis_revision_id'].rsplit('@',1)[0],'version':int(r['basis_revision_id'].rsplit('@',1)[1]),'role':r['role'],'note':r['note']} for r in rows('select * from dependency where revision_id=?',(rev['id'],))],'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],'rationale':rev['rationale'],'caveat':rev['caveat']}
changes={};table=[]
for edit in decision['native_changes']:
 obj=changes.setdefault(edit['id'],existing(edit['id'],edit['expectedVersion']));field=edit['field'];target=obj if field=='caveat' else obj['data'];actual=target[field]
 if field.endswith('_json'):
  # Compare exact stored JSON text before parsing; writer owns canonical serialization.
  original=rows('select '+field+' from '+obj['kind']+' where revision_id=?',(edit['id']+'@'+str(edit['expectedVersion']),))[0][field]
  assert original==edit['before'];target[field]=json.loads(edit['after']);count=1
 else:
  count=actual.count(edit['before']);assert count==edit['expected_match_count'],(edit['id'],field,count)
  target[field]=actual.replace(edit['before'],edit['after'],1)
 table.append({**edit,'actual_match_count':count,'disposition':'revise'})
for obj in changes.values():
 for e in obj['evidence']:
  if e['object']==rid:e['version']=2
 if obj['id']!=rid and not any(e['object']==rid for e in obj['evidence']):obj['evidence'].append({'object':rid,'version':2,'role':'supports','note':'T-0776: exakt källbunden C-0038-rättelse; samma registreringskedja.'})
 obj['rationale']+=' '+decision['operation_reason']
changes=list(changes.values())
def ev(oid,ver,note,role='supports'):return {'object':oid,'version':ver,'role':role,'note':note}
bases=[ev(rid,2,'Full egen originalpost138; samma registreringskedja.'),ev('S-0032',1,'Versionsbunden källmetadata.')]
def new(oid,kind,data,evidence,caveat):
 assert not rows('select id from object where id=?',(oid,));changes.append({'id':oid,'kind':kind,'expectedVersion':None,'data':data,'origins':[],'evidence':evidence,'disposition':'recorded','evidenceStatus':None,'rationale':decision['operation_reason'],'caveat':caveat})
aid='AUDIT-T0776-C0038';limits=decision['gates']+' '+source['dependence']
new(aid,'assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_reservations','body':json.dumps({'source':source,'decisions':decision},ensure_ascii=False,indent=2)},bases,limits)
mid='M-T0776-C0038-P0009';new(mid,'mention',{'record_id':rid,'name_literal':'Ada Wilhelmina Jansson','role_literal':'Jungf.'},bases+[ev(aid,1,'Egen namn-/yrkescell.')],limits)
new('O-T0776-C0038-P0009-fullfields','observation',{'record_id':rid,'mention_id':mid,'property':'full_source_fields','value_literal':'C-0038, inflyttningspost138: tio egna fält och avgränsad datumditto-kedja.','value_json':{'fields':source['fields'],'date_chain':source['date_chain'],'reading_decisions':source['reading_decisions'],'geometry_order':['x1','x2','y1','y2']}},bases+[ev(aid,1,'Fullfältstabell och uttryckliga råmärkes-/suffixbegränsningar.'),ev(mid,1,'Versionsbunden strukturreferens: mention_id','derived_from')],limits)
new('ADOPT-T0776-C0038-P-0009','assessment',{'subject_id':'P-0009','criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':json.dumps({'person':'P-0009','scope':source['scope'],'fields':source['fields'],'coverage':decision['coverage'],'adoption':decision['new_objects'][2]['instruction'],'reading_decisions':source['reading_decisions'],'dependence':source['dependence']},ensure_ascii=False,indent=2)},bases+[ev(aid,1,'Egen post138 och nödvändig datumditto-föregångare.')],limits)
op={'id':'T-0776/C0038-candidate-v1','actor':'Codex Sol mechanical implementation of settled Astra decisions','reason':'T-0776 AC2–4: källbundna titel-/civilstånds-/suffixrättelser, full tiofältsutvinning och Ada-adoption; kontrollerad kanonisk införsel efter självständig slutgranskning.','dependencyReviewVersion':2,'changes':changes}
def save(name,value):(B/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
save('C-0038-candidate-operation-v1.json',op);save('C-0038-consequence-table-v1.json',{'rows':table,'shared_copy_dispositions':'Awaiting explicit Astra artifact; no implicit retain.'})
files=['C-0038-candidate-operation-v1.json','C-0038-consequence-table-v1.json','source-decisions/C-0038-source.json','source-decisions/C-0038-decisions.json']
save('C-0038-first-candidate-freeze-v1.json',{'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'candidate_before_testing','baseline_head':249,'files':[{'path':str(B/f),'sha256':hashlib.sha256((B/f).read_bytes()).hexdigest()} for f in files]})
print(len(changes),'changes,',len(table),'exact field patches')
