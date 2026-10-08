"""Metadata only: exact T-0813 turns; no prompts/tool payloads preserved."""
import pathlib,json,collections,datetime
B=pathlib.Path(__file__).resolve().parent;floor=json.loads((B/'root-start-baseline-v1.json').read_text())['observed_utc'];wanted={'/root/t0791_0792_prepare','/root/t0791_primary','/root/t0791_independent'};rows=[]
for p in pathlib.Path('/Users/sverker/.codex/sessions').glob('2026/10/*/*.jsonl'):
 with p.open() as f:
  meta=json.loads(next(f)).get('payload',{});thread=meta.get('id')
  if meta.get('agent_path') not in wanted:continue
  contexts=[];records=[];seen=set()
  for line in f:
   x=json.loads(line);v=x.get('payload',{})
   if x.get('timestamp','')<floor:continue
   if x.get('type')=='turn_context':contexts.append({'timestamp':x.get('timestamp'),'turn_id':v.get('turn_id'),'model':v.get('model'),'effort':v.get('effort')})
   if x.get('type')=='token_usage_record' and v.get('thread_id')==thread:
    key=v.get('response_id');assert key not in seen;seen.add(key);records.append({'timestamp':x.get('timestamp'),'response_id':key,'turn_id':v.get('turn_id'),'usage':v.get('usage')})
  if not contexts and not records:continue
  allowed={x['turn_id'] for x in contexts};assert all(r['turn_id'] in allowed for r in records),'Unbound usage turn requires explicit metadata routing'
  totals=collections.Counter()
  for r in records:totals.update(r['usage'])
  phases=[]
  for tid in sorted(allowed):
   t=collections.Counter()
   for r in records:
    if r['turn_id']==tid:t.update(r['usage'])
   phases.append({'turn_id':tid,'actual_models':sorted({x['model'] for x in contexts if x['turn_id']==tid}),'phase':'T-0813 Sol production preparation/settled implementation; exact within-turn phase not separately classified' if meta.get('agent_path')=='/root/t0791_0792_prepare' else 'T-0813 required Astra production assessment','actual_usage_sum':dict(t)})
  rows.append({'agent_path':meta.get('agent_path'),'thread_id':thread,'source_log':str(p),'contexts':contexts,'usage_records':records,'actual_usage_sum':dict(totals),'per_turn_phases':phases})
out={'task':'T-0813','snapshot_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'floor':floor,'agents':rows,'root':{'thread_id':None,'actual_model':None,'usage':None,'reason':'No verified local turn_context/usage for root; UNKNOWN, not zero.'},'budget':{'baseline_percent':None,'status':'No current budget meter reading observed','end_percent':None},'limitations':['Only exact T-0813 post-start turns, no earlier-task cumulative total.','Capture after worker final responses and before next task turns; root finalization remains unobservable.','Required primary/final Astra plus repairs count production.','Root is unknown and logged sums cannot represent whole-pilot totals.','No matched all-Astra comparator; no causal halving claim.','Reasoning tokens are subset of output and not added twice.']}
(B/'usage-snapshot.json').write_text(json.dumps(out,indent=2)+'\n');print([(a['agent_path'],a['thread_id'],len(a['usage_records']),a['actual_usage_sum']) for a in rows])
