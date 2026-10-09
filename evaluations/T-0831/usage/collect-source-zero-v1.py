"""Exact completed source-zero turn boundaries; no content or credentials read."""
import json,pathlib,datetime
roles=[('primary','12-41-16-01a12040-bea3-73c1-958f-bd7b5a0436cb','2026-10-09T13:41:50.056Z','2026-10-09T13:46:47.102Z','evaluations/T-0830/usage/primary-cumulative-exclusion-through-source-final-v1.json'),('independent','12-44-57-01a12044-1e5b-77d2-8a9f-6dd6ffd54c32','2026-10-09T13:47:11.446Z','2026-10-09T13:48:45.745Z','evaluations/T-0828/usage/independent-cumulative-exclusion-through-partial-eight-v1.json')]
for role,suffix,start,end,previous_path in roles:
 session=pathlib.Path('/Users/sverker/.codex/sessions/2026/10/09/rollout-2026-10-09T'+suffix+'.jsonl');chosen={}
 for line in session.open():
  x=json.loads(line)
  if x.get('type')=='token_usage_record' and start<=x['timestamp']<=end:
   z=x['payload'];chosen[z['response_id']]={'timestamp':x['timestamp'],'usage':z['usage']}
 keys=['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens','total_tokens'];total={k:sum(v['usage'].get(k,0) for v in chosen.values()) for k in keys}
 out={'task':'T-0831','agent':'/root/five_ancestry_'+role,'model':'gpt-6-astra','collected_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'start_task_event':start,'completed_task_event':end,'distinct_responses':len(chosen),'response_ids':list(chosen),'usage':total,'uncached_input_tokens':total['input_tokens']-total['cached_input_tokens'],'root_usage':'UNKNOWN','collection_rule':'Completed source0 turn only; no original interpretation; actual planning production, disjoint from T0830 roles.'}
 pathlib.Path('evaluations/T-0831/usage/'+role+'-source-zero-after-final-v1.json').write_text(json.dumps(out,indent=2)+'\n')
 previous=json.load(open(previous_path))['response_ids'];excluded={'response_ids':list(dict.fromkeys(previous+list(chosen))),'purpose':'Exclude prior task production plus T0831 source0 from future T0830 collection. Independent retains T0830 source work for final cumulative count; primary separates already-measured T0830 source work.'}
 pathlib.Path('evaluations/T-0831/usage/'+role+'-exclusion-for-T0830-final-v1.json').write_text(json.dumps(excluded,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k!='response_ids'}))
