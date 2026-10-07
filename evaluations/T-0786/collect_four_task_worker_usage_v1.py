"""Collect actual task worker response usage at explicit per-worker phase floors."""
import argparse, datetime, json
from pathlib import Path
a = argparse.ArgumentParser()
a.add_argument('--output', required=True, type=Path)
a.add_argument('--workers-final', action='store_true')
args = a.parse_args()
assert not args.output.exists()
phase = json.loads(Path('evaluations/T-0786/worker-four-task-run-phase-floors-v1.json').read_text())
fields = ['input_tokens', 'cached_input_tokens', 'cache_write_input_tokens', 'output_tokens', 'reasoning_output_tokens', 'total_tokens']
result = {'task':'T-0786–T-0789', 'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'workers_final':args.workers_final, 'workers':[], 'root_usage':'UNKNOWN_NOT_ZERO', 'shared_meter':'NOT_INFERRED', 'limitations':['Only actual per-response exact-thread records at explicit worker phase floors.', 'Reasoning is a subset of output, not added twice.', 'Preparation, both Astra roles, failed attempts, repairs and finalization all count.', 'A nonfinal snapshot omits later responses; no cost or savings claim.']}
for worker in phase['worker_logs']:
 records=[]; contexts=[]; seen=set()
 for line in Path(worker['source_log']).open():
  row=json.loads(line); payload=row.get('payload',{}); at=row.get('timestamp','')
  if at < phase['worker_phase_start_utc'][worker['agent']]: continue
  if row['type']=='turn_context': contexts.append({'at':at,'turn_id':payload.get('turn_id'),'model':payload.get('model'),'effort':payload.get('effort')})
  if row['type']!='token_usage_record' or payload.get('thread_id')!=worker['thread_id']: continue
  assert payload['response_id'] not in seen
  seen.add(payload['response_id']); records.append({'at':at,'response_id':payload['response_id'],'turn_id':payload['turn_id'],'usage':payload['usage']})
 turns={r['turn_id'] for r in records}; contexts=[c for c in contexts if c['turn_id'] in turns]
 sums={k:sum(r['usage'].get(k,0) for r in records) for k in fields}
 sums['uncached_input_tokens']=sums['input_tokens']-sums['cached_input_tokens']
 result['workers'].append({**worker,'phase_floor':phase['worker_phase_start_utc'][worker['agent']],'contexts':contexts,'response_records':records,'usage_sum':sums})
result['observed_worker_sum']={k:sum(w['usage_sum'][k] for w in result['workers']) for k in fields+['uncached_input_tokens']}
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':str(args.output),'workers_final':args.workers_final,'observed_worker_sum':result['observed_worker_sum']}))
