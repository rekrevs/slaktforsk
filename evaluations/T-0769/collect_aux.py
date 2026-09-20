import pathlib,json,collections,datetime
b=pathlib.Path(__file__).resolve().parent;rows=[]
for p in pathlib.Path('/Users/sverker/.codex/sessions/2026/09/19').glob('*.jsonl'):
 ds=[json.loads(l) for l in p.open()];meta=ds[0].get('payload',{});name=meta.get('agent_path','')
 if not name.startswith('/root/benchmark_'):continue
 thread=meta['id'];usage=collections.Counter();end=None;model=None;records=[]
 for d in ds:
  v=d.get('payload',{})
  if d['type']=='token_usage_record' and v.get('thread_id')==thread:
   usage.update(v['usage']);records.append({'timestamp':d['timestamp'],'usage':v['usage']})
  if d['type']=='turn_context':model=v.get('model')
  if d['type']=='event_msg' and v.get('type')=='task_complete':end=d['timestamp']
 rows.append({'agent':name,'model':model,'start':meta['timestamp'],'end':end,'usage':dict(usage),'usage_records':records})
rates=json.loads((b/'prices.json').read_text())['rates']
for r in rows:
 u=r['usage'];ip,cp,op=rates[r['model']];r['standard_api_proxy_usd']=((u['input_tokens']-u['cached_input_tokens'])*ip+u['cached_input_tokens']*cp+u['output_tokens']*op)/1e6
(b/'auxiliary-measurements.json').write_text(json.dumps(rows,indent=2)+'\n');print('Auxiliary agents',len(rows))
