from pathlib import Path
import json,sqlite3,hashlib
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0790/preparation'
m=json.loads((O/'current-input-manifest-v1.json').read_text());n=json.loads((O/'complete-current-history-support-native.json').read_text());c=sqlite3.connect('file:'+str(O/'baseline-j454.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
heads=set(m['current_heads']);incoming=[]
for rid in heads:
 for x in c.execute('select d.*,r.object_id,r.version,r.disposition,r.caveat from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id=? order by d.rowid',(rid,)):
  v=dict(x);v['caller_current']=c.execute('select max(version) from revision where object_id=?',(v['object_id'],)).fetchone()[0]==v['version'];incoming.append(v)
receipts=[]
for x in json.loads((O/'accepted-operation-receipts.json').read_text()):
 files=list((R/'genealogy2/journal').glob(f"{x['sequence']:09d}-*.json"));assert len(files)==1;assert json.loads(files[0].read_text())['request']==json.loads(x['request_json']);receipts.append({'sequence':x['sequence'],'operation_id':x['operation_id'],'database_request_sha256':hashlib.sha256(x['request_json'].encode()).hexdigest(),'journal_files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]})
# Database is authoritative accepted receipt; journal filename routes metadata only.
p={'incoming_dependencies':incoming,'receipt_database_and_file_routing':receipts,'context_pins_file':'evaluations/T-0790/preparation/context-pins.json','bounded_entrypoints':{p:info['view'] for p,info in m['people'].items()},'background_allOWNER_not_read_credit':True,'availability_counts':m['counts'],'theme_missing':60-m['counts']['themes_available'],'PK_missing':30-m['counts']['PK_available'],'assessment_reading':'Full person assessments and research reviews must be read individually; no inferred gate from historical outcomes','independent_review_inputs':'original images excluded by scope; accepted native/document support only'}
(O/'supplement-current-incoming-receipts-and-context-v2.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'incoming':len(incoming),'receipts':len(receipts),'journal_mapped':sum(bool(x['journal_files']) for x in receipts)}))
