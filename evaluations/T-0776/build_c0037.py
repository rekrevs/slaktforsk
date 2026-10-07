"""Mechanical implementation of Astra's settled C0037 decisions."""
import json,pathlib,sqlite3,hashlib
B=pathlib.Path(__file__).resolve().parent
source=json.loads((B/'source-decisions/C-0037-source.json').read_text())
decisions=json.loads((B/'source-decisions/C-0037-decisions.json').read_text())
db=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True)
changes=[]
rid=source['record_version'].rsplit('@',1)[0]
def evidence(oid,version,note):return {'object':oid,'version':version,'role':'supports','note':note}
ev=[evidence(rid,1,'T-0776: samma originalpost och registreringskedja, ingen ny oberoende historisk röst.'),evidence('S-0031',1,'Versionsbunden källmetadata.')]
def add(oid,kind,data,bases,caveat):
 assert not db.execute('select 1 from object where id=?',(oid,)).fetchone()
 changes.append({'id':oid,'kind':kind,'expectedVersion':None,'data':data,'origins':[],'evidence':bases,'disposition':'recorded','evidenceStatus':None,'rationale':decisions['operation_reason'],'caveat':caveat})
limits='Samma flyttnings-/attestkedja; inget nytt oberoende vittne eller säkert fysiskt flyttdatum. Befintlig starkare födelse- och identitetskunskap, OWNER_CONFIRMED och alla granskningsgrindar bevaras.'
aid='AUDIT-T0776-C0037'
add(aid,'assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_limits','body':json.dumps({'source':source,'decisions':decisions},ensure_ascii=False,indent=2)},ev,limits)
mid='M-T0776-C0037-P0009'
add(mid,'mention',{'record_id':rid,'name_literal':'Ada Wilhelmina Jansson','role_literal':'dotter'},ev+[evidence(aid,1,'Egen namncells fullpostprövning.')],limits)
add('O-T0776-C0037-P0009-fullfields','observation',{'record_id':rid,'mention_id':mid,'property':'full_source_fields','value_literal':'C-0037, utflyttningspost 118: tio egna fält enligt fullfältstabellen.','value_json':{'fields':source['fields'],'normalization':source['normalization'],'geometry_order':['x1','x2','y1','y2']}},ev+[evidence(aid,1,'Samtliga tio egna fält, inklusive lokalt tomma celler.')],limits+' Tom födelsecell är endast denna källas blankhet; kvinnkönsantal 1 ändrar inte personmodellen.')
add('ADOPT-T0776-C0037-P-0009','assessment',{'subject_id':'P-0009','criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':json.dumps({'person':'P-0009','scope':source['scope'],'fields':source['fields'],'coverage':decisions['coverage'],'adoption':decisions['new_objects'][2]['instruction'],'limitations':source['limitations'],'dependence':source['dependence']},ensure_ascii=False,indent=2)},ev+[evidence(aid,1,'Egen post 118, full tiofältsutvinning.')],limits)
op={'id':'T-0776/C0037-candidate-v1','actor':'Codex Sol mechanical implementation of settled Astra decisions','reason':'T-0776 AC2–4: full originalpost 118, tio fält och avgränsad Ada-adoption; kontrollerad kanonisk införsel efter självständig slutgranskning.','dependencyReviewVersion':2,'changes':changes}
p=B/'C-0037-candidate-operation-v1.json';p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
files=['source-decisions/C-0037-source.json','source-decisions/C-0037-decisions.json','source-decisions/C-0037-handoff.md',p.name]
freeze={'citation':'C-0037','status':'first_candidate_before_testing','baseline_head':248,'files':[{'path':str(B/f),'sha256':hashlib.sha256((B/f).read_bytes()).hexdigest()} for f in files]}
(B/'C-0037-first-candidate-freeze-v1.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
(B/'C-0037-consequence-table-v1.json').write_text(json.dumps({'citation':'C-0037','rows':decisions['dispositions'],'shared_Ada_copies':'Deferred to Astra combined C0037/C0038 dispositions; no implicit retain.'},ensure_ascii=False,indent=2)+'\n')
print('4 new objects, 0 revisions; initial candidate frozen')
