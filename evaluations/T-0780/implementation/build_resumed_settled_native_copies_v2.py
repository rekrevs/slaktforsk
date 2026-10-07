"""Mechanical implementation of exactly two Astra-settled copy corrections."""
import copy
import datetime
import hashlib
import json
import sqlite3
import time
from pathlib import Path

import argparse
parser=argparse.ArgumentParser()
parser.add_argument('configuration')
args=parser.parse_args()
CFG=json.loads(Path(args.configuration).read_text())
START=time.time()
B=Path('evaluations/T-0780')
W=Path(CFG['output_dir'])
SOURCE=Path(CFG['source_path'])
SOURCE_SHA=CFG['source_sha256']
PRIOR=Path(CFG['prior_proposal_path'])
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
assert sha(SOURCE)==SOURCE_SHA
assert sha(PRIOR)==CFG['prior_proposal_sha256']
d=load(SOURCE);prior=load(PRIOR);assert len(d['objects'])==CFG['new_targets']
c=sqlite3.connect('file:'+str((B/'preparation/baseline-j281.sqlite').resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
def native(rid):
 row=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone();assert row is not None,rid;n=dict(row)
 n['data']=dict(c.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone());n['origins']=[dict(z) for z in c.execute('select * from origin where revision_id=?',(rid,))];n['evidence']=[dict(z) for z in c.execute('select * from dependency where revision_id=?',(rid,))]
 if n['kind']=='record':
  n['assets']=[dict(z) for z in c.execute('select * from record_asset where revision_id=?',(rid,))];n['media']=[dict(z) for z in c.execute('select * from record_media where revision_id=?',(rid,))]
 return n
def api(n):
 data={k:v for k,v in n['data'].items() if k!='revision_id'}
 for k,v in data.items():
  if k.endswith('_json') and isinstance(v,str):data[k]=json.loads(v)
 return {'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':data,'origins':[{'unit':z['unit_id'],'coverage':z['coverage'],'note':z['note']} for z in n['origins']],'evidence':[{'object':z['basis_revision_id'].rsplit('@',1)[0],'version':int(z['basis_revision_id'].rsplit('@',1)[1]),'role':z['role'],'note':z['note']} for z in n['evidence']],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
changes=[];proofs=[];fields=[];oldtargets={x['id'] for p in prior['sequence'] for x in p['targets']}
for item in d['objects']:
 o=item['current'];oid=o['object_id'];assert oid not in oldtargets;actual=native(o['id'])
 for k,v in actual.items():
  if k in ['origins','evidence']:assert sorted(map(canon,v))==sorted(map(canon,o[k])),(oid,k)
  else:assert v==o[k],(oid,k)
 assert not c.execute('select 1 from revision where object_id=? and version>?',(oid,o['version'])).fetchone()
 old=api(o);ch=copy.deepcopy(old)
 for e in item['edits']:
  obj=ch['data'] if e['field'].startswith('data.') else ch;key=e['field'].removeprefix('data.');before=json.loads(e['old']) if key.endswith('_json') and isinstance(e['old'],str) else e['old'];after=json.loads(e['new']) if key.endswith('_json') and isinstance(e['new'],str) else e['new'];assert obj[key]==before,(oid,key);obj[key]=after
 if item.get('evidence_addition'):
  add=item['evidence_addition'];bid,ver=add['basis_revision_id'].rsplit('@',1);ch['evidence'].append({'object':bid,'version':int(ver),'role':add['role'],'note':add['note']})
 restored=copy.deepcopy(ch)
 for e in item['edits']:
  obj=restored['data'] if e['field'].startswith('data.') else restored;key=e['field'].removeprefix('data.');obj[key]=json.loads(e['old']) if key.endswith('_json') and isinstance(e['old'],str) else e['old']
 restored['evidence']=restored['evidence'][:len(old['evidence'])];assert restored==old
 changes.append(ch);proofs.append({'target':oid,'full_current':o,'old_API_payload':old,'new_API_payload':ch,'exact_edits':item['edits'],'evidence_addition':item.get('evidence_addition'),'all_other_fields_ordered_arrays_exact':True,'source_rationale':item['rationale']})
 editfields={e['field'] for e in item['edits']}
 for k,v in old.items():
  if k=='data':
   for f,val in v.items():fields.append({'object':oid,'version':o['version'],'field':'data.'+f,'old':val,'new':ch['data'][f],'disposition':'revise' if 'data.'+f in editfields else 'retain','rationale':item['rationale'],'support':ch['evidence'],'source_sha256':SOURCE_SHA})
  else:fields.append({'object':oid,'version':o['version'],'field':k,'old':v,'new':ch[k],'disposition':'revise' if k in editfields or v!=ch[k] else 'retain','rationale':item['rationale'],'source_sha256':SOURCE_SHA})
# Preflight all incoming edges before writing any candidate artifact.
preflight_fan=[]
for ch in changes:
 for z in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(ch['id'],)):
  preflight_fan.append({'changed_target':ch['id'],'edge':dict(z)})
grade_pin=CFG.get('incoming_grade_pin')
if grade_pin:
 assert sha(grade_pin['path'])==grade_pin['sha256'];grades=load(grade_pin['path']);assert sha(grades['input_pin']['path'])==grades['input_pin']['sha256']
 assert sorted(map(canon,[x['edge'] for x in preflight_fan]))==sorted(map(canon,[x['edge'] for x in grades['objects']]))
 assert all(x['whole_native_read'] and x['disposition']=='retain_exact_current_no_rebind' and x['dependent_revision_required'] is False for x in grades['objects'])
else:assert not preflight_fan,('Return unexpected incoming count to Astra before dependent build',preflight_fan)
assert not W.exists();W.mkdir()
op={'id':CFG['operation_id'],'actor':'Codex Sol bounded implementation of settled Astra inputs','reason':'T-0780 AC3 exact source/current copy corrections '+SOURCE_SHA+'; no new original or review-grade change.','dependencyReviewVersion':2,'changes':changes};pin=save(CFG['operation_filename'],op)
seq=copy.deepcopy(prior['sequence'])+[pin];targets={};constraints=[];viol=[];heads={z['object_id']:z['version'] for z in c.execute('select object_id,max(version) version from revision group by object_id')};updates={x['id']:{'index':i+1,'expectedVersion':x['expectedVersion'],'newVersion':(x['expectedVersion'] or 0)+1} for i,p in enumerate(seq) for x in load(p['path'])['changes']}
for i,p in enumerate(seq):
 assert sha(p['path'])==p['sha256'];q=load(p['path']);p.update(index=i+1,operation_id=q['id'],targets=[],changes=len(q['changes']))
 for x in q['changes']:
  assert x['id'] not in targets;assert heads.get(x['id'])==x['expectedVersion'];targets[x['id']]={'payload':x,'operation_pin':{'path':p['path'],'sha256':p['sha256']}};p['targets'].append({'id':x['id'],'expectedVersion':x['expectedVersion'],'payload_sha256':hashlib.sha256(canon(x).encode()).hexdigest()})
  for e in x['evidence']:
   assert set(e)=={'object','version','role','note'}
   if e['object'] in updates:constraints.append({'target':x['id'],'operation':q['id'],'index':i+1,'edge':e,'basis_update':updates[e['object']]})
   if heads.get(e['object'])!=e['version'] and not any(t['id']==e['object'] and (t['expectedVersion'] or 0)+1==e['version'] for t in q['changes']):viol.append({'target':x['id'],'edge':e,'proposed_current_head':heads.get(e['object'])})
 for x in q['changes']:heads[x['id']]=(x['expectedVersion'] or 0)+1
assert len(seq)==CFG['members'] and len(targets)==CFG['targets'] and not viol
fan=[];full={};bases={}
for ch in changes:
 for z in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(ch['id'],)):
  edge=dict(z);fan.append({'changed_target':ch['id'],'edge':edge,'Astra_individual_disposition':next((z for z in grades['objects'] if z['edge']==edge),None) if grade_pin else None,'current_candidate_consumer':targets.get(edge['object_id'])});full[edge['revision_id']]=native(edge['revision_id'])
 for e in ch['evidence']:
  rid=e['object']+'@'+str(e['version'])
  if c.execute('select 1 from revision where id=?',(rid,)).fetchone():bases[rid]=native(rid)
  else:assert e['object'] in targets;bases[rid]={'explicit_future_candidate':targets[e['object']]}
proofpin=save('two-full-payload-reconstruction-proof-v1.json',{'source_pin':{'path':str(SOURCE),'sha256':SOURCE_SHA},'proofs':proofs,'only_explicit_field_and_evidence_addition_changes':True})
fieldpin=save('individual-full-field-consequence-table-v1.json',{'entries':fields})
inputpin=save('full-current-history-incoming-and-support-input-v1.json',{'changed_fullcurrent':[x['current'] for x in d['objects']],'all_history_fanout':fan,'incoming_fullnative':full,'full_support_bases':bases,'candidate_overlap_zero':True,'individual_grading_pending':not bool(grade_pin),'incoming_source_grade_pin':grade_pin,'no_automatic_rebind_or_resolution':True})
mp=save(f"current{CFG['members']}-candidate-membership-inventory-v1.json",{'prior_proposal_pin':{'path':str(PRIOR),'sha256':sha(PRIOR)},'candidate_members':seq,'unique_targets':len(targets),'member_count':len(seq),'new_targets':CFG['new_targets'],'duplicate_targets':0,'global_source_approval':False})
pp=save(f"concrete-current{CFG['members']}-partial-sequence-and-constraint-proposal-v1.json",{'sequence':seq,'members':len(seq),'unique_targets':len(targets),'constraints':constraints,'static_head_order_violations':viol,'membership_pin':mp,'fresh_primary_hash_binding_required':True,'no_native_PASS_or_stage':True})
rp=save('bounded-two-copy-production-receipt-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pin':{'path':str(SOURCE),'sha256':SOURCE_SHA},'operation_pin':pin,'proof_pin':proofpin,'field_table_pin':fieldpin,'input_pin':inputpin,'membership_pin':mp,'proposal_pin':pp,'revisions':CFG['new_targets'],'all_field_entries':len(fields),'all_history_incoming_edges':len(fan),'current_incoming_edges':sum(z['edge']['is_current'] for z in fan),'incoming_distinct_fullobjects':len(full),'no_overlap':True,'outcomes_evidence_origins_arrays_protectedgrades_preserved':True,'canonical_apply_stage_probe':'UNRUN','independent_and_global_binding':'PENDING','failed_attempts':[],'elapsed_build_seconds':time.time()-START,'actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'receipt':rp,'members':len(seq),'targets':len(targets),'incoming_current':sum(z['edge']['is_current'] for z in fan),'incoming_allhistory':len(fan),'input':inputpin,'membership':mp,'proposal':pp},indent=2))
