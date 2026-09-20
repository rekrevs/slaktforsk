import json,sys,pathlib
base=pathlib.Path(__file__).resolve().parent
rub=json.loads((base/'y/rubric.private.json').read_text())
try:
 a=json.loads(pathlib.Path(sys.argv[1]).read_text());ds=a['decisions'];d={x['id']:x for x in ds}
 checks=[]
 def check(n,p):checks.append({'name':n,'pass':bool(p)})
 check('exact_16_objects',len(ds)==16 and set(d)==set(rub['expected']))
 for k,v in rub['expected'].items():
  x=d.get(k,{})
  check(k+'.action',x.get('action')==v)
  check(k+'.resolve',x.get('resolve')==rub['requests'][k])
  check(k+'.rationale',isinstance(x.get('rationale'),str) and len(x['rationale'])>=15)
  if v=='revise':check(k+'.replacement',bool(x.get('replacement')))
 check('canonical_protected',a.get('canonical_changes')=={'persons':[],'relations':[],'owner_confirmed':[]})
 check('bounded_followup_present',isinstance(a.get('followups'),list) and len(a['followups'])>0)
 print(json.dumps({'automatic_pass':all(x['pass'] for x in checks),'score':sum(x['pass'] for x in checks),'maxScore':len(checks),'checks':checks,'manual_required':rub['manual_checks']},ensure_ascii=False,indent=2))
except Exception as e:print(json.dumps({'automatic_pass':False,'error':str(e),'score':0}))
