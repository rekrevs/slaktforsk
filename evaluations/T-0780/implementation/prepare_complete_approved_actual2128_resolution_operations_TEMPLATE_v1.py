"""UNRUN. Build reviewable resolution-only files after BOTH exact complete approvals.

Read-only DB; writes only a previously absent review artifact directory.
Never applies operations. No implicit retain, rebind, rationale synthesis or partial build.
See actual2128-resolution-builder-input-contract-v1.json for the required manifest.
"""
import argparse,datetime,hashlib,json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
EXPECTED_REQUESTS=2128

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def readpin(p):
 path=ROOT/p['path']
 assert path.is_file() and digest(path)==p['sha256'],('pin mismatch',p)
 return json.loads(path.read_text())
def pointer(x,p):
 assert p=='' or p.startswith('/'),p
 for raw in p.split('/')[1:]:
  k=raw.replace('~1','/').replace('~0','~')
  x=x[int(k)] if isinstance(x,list) else x[k]
 return x

def build(manifest_path,output_path):
 manifest_path=Path(manifest_path).resolve();output_path=Path(output_path).resolve()
 assert manifest_path.is_relative_to(ROOT/'evaluations/T-0780')
 assert output_path.is_relative_to(ROOT/'evaluations/T-0780/implementation')
 assert not output_path.exists(),'Preserve earlier drafts; choose a new review directory'
 m=json.loads(manifest_path.read_text())
 assert m['task']=='T-0780' and m['status']=='COMPLETE_APPROVED_ALL2128_INDIVIDUAL_RESOLUTIONS'
 assert m['no_canonical_apply_authorized'] is True
 requests=readpin(m['actual_request_index_pin'])['requests']
 actual={x['actual_request']['id']:x for x in requests}
 assert len(actual)==len(requests)==EXPECTED_REQUESTS
 approvals=m['individual_approvals']
 ids=[x['request_id'] for x in approvals]
 assert len(ids)==len(set(ids))==EXPECTED_REQUESTS,'Duplicate/missing individual approval'
 assert set(ids)==set(actual),'Unexpected/missing request IDs'
 assert m['operation_actor'].strip() and m['operation_reason'].strip()
 assert isinstance(m['max_resolutions_per_operation'],int) and 1<=m['max_resolutions_per_operation']<=EXPECTED_REQUESTS
 # Explicit final gates must bind each individual ID, not only an aggregate count.
 for role in ['primary','independent']:
  g=readpin(m[role+'_complete_resolution_gate_pin'])
  assert pointer(g,m[role+'_gate_ready_pointer']) is True
  assert pointer(g,m[role+'_gate_stage_pin_pointer'])==m['stage_DB_pin']
  gids=pointer(g,m[role+'_gate_approved_IDs_pointer'])
  assert isinstance(gids,list) and len(gids)==len(set(gids))==EXPECTED_REQUESTS and set(gids)==set(actual)
 stage_path=ROOT/m['stage_DB_pin']['path']
 assert stage_path.is_relative_to(ROOT/'evaluations/T-0780/full10-stage-final143-v1')
 assert digest(stage_path)==m['stage_DB_pin']['sha256']
 db=sqlite3.connect('file:'+str(stage_path)+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
 state={'journal_head':db.execute('select max(sequence) from operation_payload').fetchone()[0],
        'pending':db.execute('select count(*) from pending_review').fetchone()[0]}
 assert state==m['expected_actual_stage_state']=={'journal_head':424,'pending':EXPECTED_REQUESTS}
 pending={r['id']:dict(r) for r in db.execute('select * from pending_review')}
 assert set(pending)==set(actual),'Actual stage pending set changed'
 rows=[]
 for item in approvals:
  q=actual[item['request_id']];request=q['actual_request']
  assert pending[item['request_id']]==request,'Actual pending request identity/versions changed'
  pr=pointer(readpin(item['primary_decision_pin']),item['primary_row_pointer'])
  ir=pointer(readpin(item['independent_decision_pin']),item['independent_row_pointer'])
  assert pr['actual_request']==ir['actual_request']==request,'Source/independent exact request mismatch'
  instruction=pointer(pr,item['primary_resolution_instruction_pointer'])
  independent_instruction=pointer(ir,item['independent_approved_resolution_instruction_pointer'])
  assert instruction==independent_instruction,'Independent approval is not the exact primary instruction'
  assert set(instruction)=={'request','rationale'} and instruction['request']==item['request_id']
  assert isinstance(instruction['rationale'],str) and instruction['rationale'].strip()
  assert pointer(pr,item['primary_current_revision_pointer'])==q['affected_latest_current_revision_id']
  assert pointer(ir,item['independent_current_revision_pointer'])==q['affected_latest_current_revision_id']
  scope=pointer(pr,item['primary_individual_scope_pointer'])
  ownscope=pointer(ir,item['independent_individual_scope_pointer'])
  assert scope and ownscope,'Explicit per-ID source and independent scopes required'
  current=db.execute('select id from current_revision where object_id=?',(q['affected_latest_current_revision_id'].rsplit('@',1)[0],)).fetchone()
  assert current['id']==q['affected_latest_current_revision_id']
  rows.append({'actual_request':request,'current_revision_id':current['id'],'exact_resolution_instruction':instruction,
               'primary_decision_pin':item['primary_decision_pin'],'primary_row_pointer':item['primary_row_pointer'],
               'literal_primary_scope':scope,'independent_decision_pin':item['independent_decision_pin'],
               'independent_row_pointer':item['independent_row_pointer'],'literal_independent_scope':ownscope})
 db.close();assert digest(stage_path)==m['stage_DB_pin']['sha256']
 # Retain the manifest's explicitly approved request order; never deduplicate/sort to hide differences.
 operations=[];size=m['max_resolutions_per_operation']
 for start in range(0,len(rows),size):
  chunk=rows[start:start+size];n=len(operations)+1
  operations.append({'id':m['operation_id_prefix']+f'/{n:03d}','actor':m['operation_actor'],
     'reason':m['operation_reason'],'changes':[],
     'resolve':[x['exact_resolution_instruction'] for x in chunk]})
 existing=sqlite3.connect('file:'+str(stage_path)+'?mode=ro',uri=True)
 assert all(existing.execute('select 1 from operation where id=?',(op['id'],)).fetchone() is None for op in operations)
 existing.close();assert len({op['id'] for op in operations})==len(operations)
 output_path.mkdir()
 pins=[]
 for i,op in enumerate(operations,1):
  p=output_path/f'{i:03d}-individual-source-approved-resolution-operation-v1.json'
  p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');pins.append({'path':str(p.relative_to(ROOT)),'sha256':digest(p),'operation_id':op['id'],'changes':0,'resolve_count':len(op['resolve'])})
 proof={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'REVIEWABLE_ONLY_UNAPPLIED',
  'manifest_pin':{'path':str(manifest_path.relative_to(ROOT)),'sha256':digest(manifest_path)},'stage_DB_pin':m['stage_DB_pin'],
  'actual_stage_state':state,'exact_individual_approvals':rows,'operations':pins,'coverage':{'actual_pending':EXPECTED_REQUESTS,'unique_approved':len(ids),'operation_count':len(pins),'duplicate_IDs':0,'missing_IDs':0,'unexpected_IDs':0},
  'runtime_mutation_authorized':False,'program_acceptance':False,'no_automatic_retain_or_rebind':True}
 p=output_path/'complete-individual-resolution-review-package-index-v1.json';p.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'review_index':str(p.relative_to(ROOT)),'sha256':digest(p),'operations':len(pins),'individual_resolutions':len(rows),'applied':False},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('complete_approval_manifest');p.add_argument('--new-review-directory',required=True);a=p.parse_args();build(a.complete_approval_manifest,a.new_review_directory)
