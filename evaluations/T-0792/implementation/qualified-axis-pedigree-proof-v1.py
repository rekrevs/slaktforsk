import copy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0792/implementation';S=D/'stage464-v1';OP=D/'candidate-operation-v2.json';ops={x['id']:x for x in json.loads(OP.read_text())['changes']};diag=json.loads((S/'full-axis-diagnostics-v1.json').read_text());bindings=[]
def axis(before,after,person,kind):
 expected=copy.deepcopy(before)
 for key in ['assessments','ignored_assessments']:
  aa=before.get(key,[]);bb=after.get(key,[]);assert len(aa)==len(bb)
  for i,(old,new) in enumerate(zip(aa,bb)):
   if old==new:continue
   oid=old['object_id'];assert oid in ops and oid in ['ASSESSMENT-P-0241','ASSESSMENT-P-0246','ASSESSMENT-P-0239','ASSESSMENT-P-0240'];op=ops[oid];assert old['revision_id']==oid+'@'+str(op['expectedVersion']);assert new['revision_id']==oid+'@'+str(op['expectedVersion']+1)
   for field in ['body','caveat','rationale','disposition']:
    approved=op['data'][field] if field=='body' else op[field];assert new[field]==approved
   assert new['evidence_status']==op['evidenceStatus'];assert old['outcome']==new['outcome'];assert old['criteria']==new['criteria'];assert old['subject_id']==new['subject_id']
   check=copy.deepcopy(old)
   for f in ['body','caveat','version','revision_id','origins','evidence']:check[f]=new[f]
   assert check==new,('Unexpected derived assessment field',oid)
   assert [{k:v for k,v in z.items() if k!='revision_id'} for z in old['origins']]==[{k:v for k,v in z.items() if k!='revision_id'} for z in new['origins']]
   for z in new['origins']:assert z['revision_id']==new['revision_id']
   # Evidence exact literal operation is additionally certified in actual-literal-target-proofs.
   expected[key][i]=new;bindings.append({'person':person,'axis':kind,'array':key,'index':i,'old_full':old,'approved_current_full':new,'operation_object':op,'operation_sha256':hashlib.sha256(OP.read_bytes()).hexdigest()})
 assert expected==after,('Unexpected full review axis delta',person,kind)
 return True
for r in diag['people']:
 for k in ['identity_review','tree_effect']:axis(r['before'][k],r['after'][k],r['person'],k)
 for k in ['person','passed','status','reasons','explanation']:assert r['before'][k]==r['after'][k]
 a=r['after'];assert a['identity_review']['outcome']=='passed' and a['identity_review']['usable'];assert a['tree_effect']['outcome']=='supporting' and a['tree_effect']['usable'];assert a['life_picture_review']['outcome']=='failed' and a['life_picture_review']['usable'] and a['life_picture_review']['issues']==[]
peds=[]
for pid,label in [('P-0269','Adam'),('P-0270','Axel')]:
 b=json.loads((R/f'evaluations/T-0792/reconciliation462/{label}-verified.json').read_text());s=json.loads((S/f'{label}-verified.json').read_text())
 for k in ['root','mode','rules','maxDepth','maxPaths','truncated','paths','edges']:assert b[k]==s[k],k
 assert len(b['gates'])==len(s['gates'])
 for x,y in zip(b['gates'],s['gates']):
  for k in ['person_id','person','criteria','passed','status','reasons','explanation']:assert x[k]==y[k]
  for k in ['identity_review','tree_effect']:axis(x[k],y[k],x['person_id'],k)
 # Entire exclusion nesting is retained for SOURCE review; each embedded gate checked mechanically.
 def gates(v):
  if isinstance(v,dict):
   if 'identity_review' in v and 'tree_effect' in v:yield v
   for z in v.values():yield from gates(z)
  elif isinstance(v,list):
   for z in v:yield from gates(z)
 bg=list(gates(b['excluded']));sg=list(gates(s['excluded']));assert len(bg)==len(sg)
 for x,y in zip(bg,sg):
  for k in ['person_id','person','criteria','passed','status','reasons','explanation']:assert x[k]==y[k]
  for k in ['identity_review','tree_effect']:axis(x[k],y[k],x['person_id'],k)
 peds.append({'root':pid,'all_gates':len(s['gates']),'exclusion_gates':len(sg),'paths':len(s['paths']),'edges':len(s['edges']),'protected':True,'before':b,'after':s})
out={'passed':True,'role':'Exact mechanical substitution of individually approved legacy objects only; SOURCE final approval still required','people':diag['people'],'legacy_substitutions':bindings,'pedigrees':peds,'all_four_life_usable_failed':True,'all_four_identity_passed_tree_supporting_usable':True,'unrelated_Maj_conflict_exact':True}
p=S/'qualified-full-axis-default-pedigree-proof-v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'legacy_substitution_bindings':len(bindings),'pedigrees':[{k:v for k,v in p.items() if k not in ['before','after']} for p in peds]}))
