"""Mechanical quote/window verification; does not judge meaning or relevance."""
from pathlib import Path
from urllib.parse import quote
import datetime,json,sys
h=Path(__file__).resolve().parent;roles=sys.argv[1:] or ['candidate','review'];results=[]
for role in roles:
 for p in sorted((h/role/'claims').glob('*-batches/*.json')):
  batch=json.loads(p.read_text());claims=batch.get('claims',[]);entry={'path':str(p.relative_to(h)),'claims':len(claims),'within_six':0<len(claims)<=6,'quotes':[]}
  for c in claims:
   q={'id':c.get('id'),'object':c.get('object'),'field':c.get('field')}
   try:
    key=c['object'];objpath=h/'baseline-input/objects'/(quote(key,safe='')+'.json')
    if not objpath.exists():objpath=h/'baseline-input/supplement/objects'/(quote(key,safe='')+'.json')
    obj=json.loads(objpath.read_text());field=c['field']
    v=obj['revision'][field.split('.',1)[1]] if field.startswith('revision.') else obj['data'][field]
    if isinstance(v,str) and c.get('quote_encoding')!='JSON field value':
     a,b=c['start'],c['end'];q['match']=isinstance(a,int) and isinstance(b,int) and 0<=a<=b<=len(v) and v[a:b]==c['quote'];q['kind']='exact_text_slice'
    else:
     rendered=json.dumps(v,ensure_ascii=False,sort_keys=True)
     a,b=c.get('start'),c.get('end')
     q['kind']='structured_value_or_sorted_unicode_json_slice'
     q['match']=('quote' in c and c['quote']==v) or ('quoted_value' in c and c['quoted_value']==v) or (isinstance(a,int) and isinstance(b,int) and 0<=a<=b<=len(rendered) and rendered[a:b]==c.get('quote'))
    q['required_decision_fields_present']=all(k in c for k in ('quote','old_support','source_observation','judgment','decision','grounds','affected_copies')) and bool(c.get('grounds'))
   except Exception as e:q['match']=False;q['error']=str(e)
   entry['quotes'].append(q)
  results.append(entry)
r={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Only exact quote locations, batch size and required fields. No substantive judgement, coverage or support validation.','batches':results,'state':'PASS' if results and all(b['within_six'] and all(q['match'] and q.get('required_decision_fields_present',False) for q in b['quotes']) for b in results) else 'REVIEW_REQUIRED'}
(h/'claim-quote-check.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'state':r['state'],'batches':len(results),'claims':sum(b['claims'] for b in results)}))
