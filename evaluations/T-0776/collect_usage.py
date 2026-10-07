"""Metadata only: exact T-0776 turns; no prompts/tool payloads preserved."""
import pathlib,json,collections,datetime
B=pathlib.Path(__file__).resolve().parent;floor='2026-10-02T06:41:10.017070';wanted={'/root/hybrid_sol_lead','/root/hybrid_astra_sources','/root/hybrid_astra_final'};rows=[]
for p in pathlib.Path('/Users/sverker/.codex/sessions').glob('2026/10/0[12]/*.jsonl'):
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
   phases.append({'turn_id':tid,'actual_models':sorted({x['model'] for x in contexts if x['turn_id']==tid}),'phase':'T-0776 Sol production preparation/settled implementation; exact within-turn phase not separately classified' if meta.get('agent_path')=='/root/hybrid_sol_lead' else 'T-0776 required Astra production assessment','actual_usage_sum':dict(t)})
  rows.append({'agent_path':meta.get('agent_path'),'thread_id':thread,'source_log':str(p),'contexts':contexts,'usage_records':records,'actual_usage_sum':dict(totals),'per_turn_phases':phases})
out={'task':'T-0776','snapshot_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'floor':floor+'Z','agents':rows,'root':{'thread_id':'01a0f63b-96a6-7dd2-a745-deec73593f58','actual_model':None,'usage':None,'reason':'No verified local turn_context/usage for root; UNKNOWN, not zero.'},'budget':{'baseline_percent':39,'status':'provisional latest owner reading before continuation chat','end_percent':None},'limitations':['Only exact T-0776 post-start turns, no T-0775 session cumulative total.','In-progress response and later finalization not yet logged.','Required primary/final Astra plus repairs count production.','Root is unknown and logged sums cannot represent whole-pilot totals.','No matched all-Astra comparator; no causal halving claim.','Reasoning tokens are subset of output and not added twice.']}
(B/'usage-snapshot.json').write_text(json.dumps(out,indent=2)+'\n');print([(a['agent_path'],a['thread_id'],len(a['usage_records']),a['actual_usage_sum']) for a in rows])
