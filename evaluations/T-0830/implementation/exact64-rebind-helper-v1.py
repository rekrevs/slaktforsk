import json,copy,sys
from pathlib import Path
D=Path('evaluations/T-0830/implementation');op=json.load(open(sys.argv[1]));review=json.load(open('evaluations/T-0830/primary/preflight-rebind-review-v1.json'));m={a['id']:a for a in op['changes']};changes=[]
for r in review['individual_rebind_dispositions']:
 assert r['disposition']=='APPROVE_EXACT_REBIND'
 a=m[r['dependent']];hits=[i for i,e in enumerate(a['evidence'])if e==r['old_edge']];assert len(hits)==1,(r['dependent'],hits)
 i=hits[0];a['evidence'][i]=copy.deepcopy(r['new_edge']);changes.append({'dependent':r['dependent'],'array_index':i,'old':r['old_edge'],'new':r['new_edge'],'reason':r['reason']})
Path(sys.argv[2]).write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');Path(sys.argv[3]).write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
