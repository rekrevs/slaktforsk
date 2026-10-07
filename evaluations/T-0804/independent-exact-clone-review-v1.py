import json,copy,hashlib,sqlite3
from pathlib import Path
p=Path('evaluations/T-0804')
def read(s):return json.loads((p/s).read_text())
def sha(s):return hashlib.sha256((p/s).read_bytes()).hexdigest()
op=read('implementation/candidate-operation-v2.json');tab=read('implementation/individual-consequence-table-v2.json');core=read('primary/source-approved-core-design-v1.json');sem=read('primary/semantic-dispositions-v2.json');rb=read('primary/exact-projected-rebind-decisions-v1.json')
b=sqlite3.connect('file:'+str(p/'preparation/baseline464.sqlite')+'?mode=ro',uri=True);b.row_factory=sqlite3.Row
expected={x['id']:copy.deepcopy(x) for x in core['changes']}
for row in tab['changes']+tab['retains']:
 n=row['old_native']
 if not n:continue
 actual=dict(b.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(n['id'],)).fetchone());actual['data']=dict(b.execute('select * from '+actual['kind']+' where revision_id=?',(n['id'],)).fetchone())
 for k,t in [('origins','origin'),('evidence','dependency')]:actual[k]=[dict(z) for z in b.execute('select * from '+t+' where revision_id=? order by rowid',(n['id'],))]
 assert actual==n,n['id']
 assert b.execute('select version from current_revision where object_id=?',(n['object_id'],)).fetchone()[0]==n['version']
for s in sem['changes']:
 n=next(r['old_native'] for r in tab['changes'] if r['object']==s['object'])
 a={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':{k:json.loads(v) if k.endswith('_json') and isinstance(v,str) else v for k,v in n['data'].items() if k!='revision_id'},'origins':[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in n['origins']],'evidence':[{'object':x['basis_revision_id'].rsplit('@',1)[0],'version':int(x['basis_revision_id'].rsplit('@',1)[1]),'role':x['role'],'note':x['note']} for x in n['evidence']],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 for f in s['fields']:
  d=a if f['field'] in a else a['data'];assert d[f['field']].count(f['old'])==1;d[f['field']]=d[f['field']].replace(f['old'],f['new'],1)
 oid,v=s['support'].rsplit('@',1);a['evidence'].append({'object':oid,'version':int(v),'role':'supports','note':'T-0804: exakt ägarbekräftad familjekoppling enligt PCD-2026-10-07-001; kompletterar arkivstöd utan ny originalutvinning.'});expected[a['id']]=a
for r in rb['decisions']:
 assert expected[r['target']]['evidence'][r['edge_index']]==r['original_proposed_edge'];expected[r['target']]['evidence'][r['edge_index']]=r['new_edge']
assert len(expected)==87 and len(rb['decisions'])==57
seen=set()
for a in op['changes']:
 assert a==expected[a['id']],a['id']
 assert a==next(r['new_api'] for r in tab['changes'] if r['object']==a['id'])
 for e in a['evidence']:
  if e['object'] in expected:assert e['object'] in seen and e['version']==(expected[e['object']]['expectedVersion'] or 0)+1
  else:assert e['version']==b.execute('select version from current_revision where object_id=?',(e['object'],)).fetchone()[0]
 seen.add(a['id'])
assert len(tab['retains'])==6 and not tab['unapproved_rebinds']
assert op['changes']==read('implementation/candidate-operation-v1.json')['changes']
out={'role':'independent Astra source and exact consequence review','ready_for_clone_stage':True,'canonicalApproval':False,'operationSha256':sha('implementation/candidate-operation-v2.json'),'consequenceSha256':sha('implementation/individual-consequence-table-v2.json'),'coreSha256':sha('primary/source-approved-core-design-v1.json'),'semanticSha256':sha('primary/semantic-dispositions-v2.json'),'rebindSha256':sha('primary/exact-projected-rebind-decisions-v1.json'),'literalProof':'87 exact APIs independently reconstructed from approved 15 core plus72 semantic decisions; 57 individually assessed bindings; old native rows and complete ordered arrays equal baseline464; six historical retains exact; no unapproved bindings. Reason-only v2 amendment approved.','sourceJudgement':'Owner-confirmed exact grandparent chain supports individually passed identity/supporting tree, not full PK05 extraction or LIFE. Preserve two CORROBORATED edges with added separate OWNER fact; normalize Jan-Christer bridge transparently. Four older Maj competitors retired with full histories. Current860/720/744 reservations read and retained, not biological/legal expansion. Projected PK/theme/BIO bindings preserve underlying outcomes and named archival debts.','conditions':'Clone only. Actual dependent requests require individual source review; final full axes, pedigree, protected native arrays and historical rows require staged final hash approval before root canonical apply.'}
(p/'independent-candidate-clone-stage-gate-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
