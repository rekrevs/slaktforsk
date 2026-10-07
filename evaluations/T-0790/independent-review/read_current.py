import json,sys
p=sys.argv[1];section=sys.argv[2]
d=json.load(open('evaluations/T-0790/preparation/'+p+'-person.json')); seen=set();texts={}
def scan(v):
 if isinstance(v,dict):
  if 'revision_id'in v and 'object_id'in v:
   if v['revision_id']in seen:return
   seen.add(v['revision_id']); x={k:x for k,x in v.items() if k not in ['origins','pending_reviews','revision_id','object_id','kind','version','participation','qualifications']}
   for k in ['caveat','rationale']:
    t=x.get(k)
    if t:
     if t in texts:x[k]='SAME '+texts[t]
     else:texts[t]=v['revision_id']+'.'+k
   print('\n'+v['revision_id']);print(json.dumps(x,ensure_ascii=False))
   for k in ['participation','qualifications']:
    if k in v:scan(v[k])
  else:
   for x in v.values():scan(x)
 elif isinstance(v,list):
  for x in v:scan(x)
if section not in ['research','facts']:
 for k in section.split(','):scan(d.get(k))
elif section=='research':scan(d['research']);scan(d['assessments'])
else:
 for k in ['person','facts','contextFacts','relations','events','observations','narratives','questions','interpretationQuestions']:scan(d.get(k))
