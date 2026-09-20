import json,pathlib,datetime,hashlib,collections
base=pathlib.Path(__file__).resolve().parent
schedule=json.loads((base/'schedule.json').read_text()); byid={r['id']:r for r in schedule}
results=[]
for p in pathlib.Path('/Users/sverker/.codex/sessions/2026/09/19').glob('*.jsonl'):
 with p.open() as f:
  first=json.loads(next(f));meta=first.get('payload',{});ap=meta.get('agent_path','')
  if not ap.startswith('/root/trial_'):continue
  rid=ap.removeprefix('/root/trial_')
  if rid not in byid:continue
  ds=[first]+[json.loads(l) for l in f]
 thread=meta['id'];usage=collections.Counter();calls=[];models=[];final=None;records=[]
 for d in ds:
  v=d.get('payload',{})
  if d['type']=='token_usage_record' and v.get('thread_id')==thread:
   usage.update(v['usage']);records.append({'timestamp':d['timestamp'],'response_id':v.get('response_id'),'usage':v['usage']})
  if d['type']=='turn_context':models.append({'model':v.get('model'),'effort':v.get('effort')})
  if d['type']=='response_item':
   if v.get('type') in ['function_call','custom_tool_call']:calls.append({'timestamp':d['timestamp'],'name':v.get('name'),'arguments':v.get('arguments',v.get('input'))})
   if v.get('type')=='message' and v.get('role')=='assistant' and (v.get('channel')=='final' or v.get('phase')=='final_answer'):final=d
 start=meta['timestamp'];end=final['timestamp'] if final else None
 elapsed=(datetime.datetime.fromisoformat(end.replace('Z','+00:00'))-datetime.datetime.fromisoformat(start.replace('Z','+00:00'))).total_seconds() if end else None
 answer=base/'runs'/rid/'answer.json'
 r={**byid[rid],'thread_id':thread,'start':start,'end':end,'seconds':elapsed,'actual_models':models,'usage':dict(usage),'tool_calls':len(calls),'answer_exists':answer.exists(),'answer_sha256':hashlib.sha256(answer.read_bytes()).hexdigest() if answer.exists() else None}
 telemetry=base/'runs'/rid/'telemetry.json';telemetry.write_text(json.dumps({**r,'source_log':str(p),'calls':calls,'usage_records':records},ensure_ascii=False,indent=2)+'\n')
 results.append(r)
results.sort(key=lambda r:r['order']);(base/'measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print('started',len(results),'finished',sum(r['end'] is not None for r in results),'answers',sum(r['answer_exists'] for r in results))
for r in results:
 if r['end'] is None:print('running',r['id'],r['start'])
