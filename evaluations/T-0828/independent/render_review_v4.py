from pathlib import Path
import json,difflib
p=Path('evaluations/T-0828'); d=json.loads((p/'implementation/individual-consequence-table-final-v4.json').read_text()); seen={};out=[]
def diff(o,n):
 if o==n:return None
 if isinstance(o,dict) and isinstance(n,dict):return {k:diff(o.get(k),n.get(k)) for k in o.keys()|n.keys() if o.get(k)!=n.get(k)}
 if isinstance(o,str) and isinstance(n,str):
  try:a=json.loads(o);b=json.loads(n);return diff(a,b)
  except:pass
  # line-based exact removed/added content, suppress long unchanged body
  delta=[]
  a=o.splitlines(keepends=True);b=n.splitlines(keepends=True)
  for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
   if tag!='equal':delta.append({'removed':''.join(a[i:j]),'added':''.join(b[k:l])})
  return delta
 return {'old':o,'new':n}
for r in d['fields']:
 v=diff(r['old_value'],r['new_value']);s=json.dumps(v,ensure_ascii=False,indent=1)
 if s in seen:s='[SAME DELTA AS '+seen[s]+']'
 else:seen[s]=r['object_id']+'/'+r['field']
 out.append(r['object_id']+' '+r['field']+'\n'+s)
s='\n\n'.join(out)
for i in range(0,len(s),23000):(p/'independent'/f'candidate-v4-semantic-delta{i//23000}.txt').write_text(s[i:i+23000])
print(len(s),(len(s)+22999)//23000)
