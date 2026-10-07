import json,sqlite3,hashlib,datetime
from pathlib import Path
b=Path('evaluations/T-0780');dp=b/'source-review/C-0044-primary-decisions-v1.json';assert hashlib.sha256(dp.read_bytes()).hexdigest()=='041ca6fb7f96661e37cac4ae5af29ccce2fb1dd25171257a0c16cecc7cf5398d';d=json.load(open(dp));impact=json.load(open(b/'implementation/C0044-original-record-impact-v1.json'));c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
cur={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on r.object_id=o.id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')}
def full(oid):
 r=cur[oid].copy();rid=r['id'];r['data']=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(rid,)).fetchone());r['origins']=[dict(x) for x in c.execute('select * from origin where revision_id=?',(rid,))];r['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=?',(rid,))]
 if r['kind']=='record':
  r['assets']=[dict(x) for x in c.execute('select * from record_asset where revision_id=?',(rid,))];r['media']=[dict(x) for x in c.execute('select * from record_media where revision_id=?',(rid,))]
 return r
entries=[];mismatches=[]
for o in d['objects']:
 old=o['current'];r=full(old['object_id']);assert r['id']==old['revision_id']
 for field,v in old['data'].items():assert r['data'][field]==v
 for field in ['caveat','rationale','disposition','evidence_status']:assert r[field]==old[field]
 edits={e['field']:e for e in o['edits']}
 for field,v in [('data.'+k,v) for k,v in old['data'].items() if k!='revision_id']+[(k,old[k]) for k in ['caveat','rationale','disposition','evidence_status']]:
  e=edits.get(field)
  if e and e['old']!=v:mismatches.append({'object':old['object_id'],'field':field,'expected_old':e['old'],'actual_old':v})
  entries.append({'object_id':old['object_id'],'revision_id':r['id'],'field':field,'old_wording':v,'new_wording':e['new'] if e else v,'Astra_disposition':o['disposition'],'Astra_rationale':e['reason'] if e else o['rationale'],'support':r['evidence'],'field_edit':bool(e)})
assert not mismatches
fan=[];settled={x['current']['object_id']:x for x in d['objects']}
for item in impact['dependencies']['current']:
 r=full(item['object_id']);sd=settled.get(item['object_id']);fan.append({'impact_path':item,'current_full_native':r,'primary_93_context_disposition':sd['disposition'] if sd else None,'primary_93_edit_fields':[x['field'] for x in sd['edits']] if sd else [],'requested_rebind_or_retain_current_basis':None,'requested_individual_rationale':None,'warning':'Changing R@1→R@2 requires explicit individual basis disposition. Exact current old evidence preserved until Astra settles.'})
(b/'implementation/C-0044-R1-dependency-fanout-input-v1.json').write_text(json.dumps({'task':'T-0780','source_record':'R-f81045d395fcb687a2417ed6@1','proposed_record_version':2,'current_fanout':fan,'historical_fanout':impact['dependencies']['historical'],'current_count':len(fan),'semantic_screening_pending':True,'no_dependent_operation_generated_or_apply':True},ensure_ascii=False,indent=2)+'\n')
(b/'implementation/C-0044-exact-context-consequence-plan-v1.json').write_text(json.dumps({'task':'T-0780','objects':93,'changed_objects':sum(bool(x['edits']) for x in d['objects']),'retained_objects':sum(not x['edits'] for x in d['objects']),'individual_fields':len(entries),'entries':entries,'exact_oldfield_matches_PASS':True,'dependencyfanout_pending_before_dependent_operations':True},ensure_ascii=False,indent=2)+'\n');print({'objects':93,'fields':len(entries),'edited_objects':14,'fanout':len(fan),'oldfield_matches':'PASS'})
