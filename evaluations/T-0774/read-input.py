"""Small, exact read windows into frozen historical objects. Never reads main DB."""
from pathlib import Path
from urllib.parse import quote
import json,sys
H=Path(__file__).resolve().parent/'baseline-input'
def locate(section,key):
 p=H/section/(quote(key,safe='')+'.json')
 return p if p.exists() else H/'supplement'/section/(quote(key,safe='')+'.json')
mode=sys.argv[1]
if mode=='object':
 key=sys.argv[2];obj=json.loads(locate('objects',key).read_text())
 if len(sys.argv)>3:
  field=sys.argv[3];value=obj['data'][field];start=int(sys.argv[4]) if len(sys.argv)>4 else 0
  if isinstance(value,str):out={'object':key,'field':field,'start':start,'end':min(start+3000,len(value)),'length':len(value),'text':value[start:start+3000],'has_more':start+3000<len(value)}
  else:out={'object':key,'field':field,'value':value}
 else:
  out={k:obj[k] for k in ['kind','revision','origins','evidence','assets']};out['data_field_sizes']={k:len(v) if isinstance(v,str) else None for k,v in obj['data'].items()};out['short_data']={k:v for k,v in obj['data'].items() if not isinstance(v,str) or len(v)<=300}
 print(json.dumps(out,ensure_ascii=False,indent=2))
elif mode=='segment':
 print(locate('segments',sys.argv[2]).read_text())
elif mode=='index':
 idx=json.loads((H/'object-index.json').read_text());supp=H/'supplement/object-index.json'
 if supp.exists():idx+=json.loads(supp.read_text())
 start=int(sys.argv[2]);count=min(int(sys.argv[3]),6);print(json.dumps({'start':start,'end':min(start+count,len(idx)),'total':len(idx),'objects':idx[start:start+count]},ensure_ascii=False,indent=2))
else:raise SystemExit('object <id@version> [field [start]] | segment <segment-id> | index <start> <count<=6>')
