"""Read-only correction to expected protection check; no data or status mutation."""
import copy,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0791/implementation';S=D/'stage462-v1';rows=json.loads((S/'review-axis-full-diagnostics-v1.json').read_text());AM=R/'evaluations/T-0791/independent-protected-axis-amendment-v1.json';assert hashlib.sha256(AM.read_bytes()).hexdigest()=='45417621cefeee1b17247b1dbff31afe5a166ccf443461daf19f9af4a2463cd4'
def axis(a):return {k:v for k,v in a.items() if k!='ignored_assessments'}
proof=[]
for r in rows:
 for a in ['identity_review','tree_effect']:
  assert axis(r['before'][a])==axis(r['after'][a]),(r['person'],a)
  if r['person']!='P-0007':assert r['before'][a]==r['after'][a]
 assert r['before']['person']==r['after']['person'];assert r['before']['passed']==r['after']['passed'];life=r['after']['life_picture_review'];assert life['usable'] is True and life['outcome']=='failed' and life['issues']==[]
 proof.append({'person':r['person'],'identity_axis_complete_decision_equal':True,'tree_axis_complete_decision_equal':True,'protected_outcome_usable_issues_assessment_source_exact':True,'life_usable':True,'life_outcome':'failed','life_issues':[],'before':r['before'],'after':r['after']})
pedigrees=[]
for pid,label in [('P-0269','Adam'),('P-0270','Axel')]:
 b=json.loads((R/f'evaluations/T-0791/preparation/pedigree-{pid}.json').read_text());s=json.loads((S/f'{label}-verified.json').read_text());keys=['root','mode','rules','maxDepth','maxPaths','truncated','paths','edges'];assert all(b[k]==s[k]for k in keys)
 assert len(b['gates'])==len(s['gates']);gs=[]
 for x,y in zip(b['gates'],s['gates']):
  assert x['person_id']==y['person_id'];assert all(x[k]==y[k]for k in ['person','criteria','passed','status','reasons','explanation'])
  for a in ['identity_review','tree_effect']:assert axis(x[a])==axis(y[a]),(pid,x['person_id'],a)
  gs.append({'person':x['person_id'],'protected_complete_decision_axes_equal':True,'status':y['status'],'identity_outcome':y['identity_review']['outcome'],'identity_usable':y['identity_review']['usable'],'identity_issues':y['identity_review']['issues'],'tree_outcome':y['tree_effect']['outcome'],'tree_usable':y['tree_effect']['usable'],'tree_issues':y['tree_effect']['issues']})
 pedigrees.append({'root':pid,'paths_edges_rules_limits_exact':True,'all_identity_tree_gates':gs,'excluded_before':b['excluded'],'excluded_after':s['excluded'],'note':'Full raw defaults retained separately. Excluded structure may embed reviewed life/ignored legacy content; protected current decisions and path/edges exactly equal.'})
for name,v in [('qualified-full-individual-review-axis-proof-v2.json',{'passed':True,'amendment_sha256':hashlib.sha256(AM.read_bytes()).hexdigest(),'people':proof,'Maj_baseline_conflict_preserved':True,'qualification':'Maj aggregate axis remains unusable assessment_conflict already present on baseline460; native0789 failed/waiting unchanged. Only explicitly reviewed ignored legacy header@2→3 differs. No fabricated usablefailed/waiting.'}),('qualified-default-pedigree-protection-v2.json',{'passed':True,'pedigrees':pedigrees})]:
 p=S/name;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':True,'four_life_usable_failed':True,'both_pedigree_paths_edges_exact':True,'Maj_baseline_conflict_preserved':True}))
