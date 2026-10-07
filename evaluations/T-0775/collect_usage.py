"""Metadata-only usage snapshot. Never preserve messages or tool arguments."""
import pathlib,json,collections,datetime
B=pathlib.Path(__file__).resolve().parent;floor='2026-10-01T19:46:00';wanted={'/root/hybrid_sol_lead','/root/hybrid_astra_sources','/root/hybrid_astra_final'};cli_thread='01a0f91d-72c9-7741-a4df-3bf32dd26a0b';rows=[]
for p in pathlib.Path('/Users/sverker/.codex/sessions/2026/10/01').glob('*.jsonl'):
 with p.open() as f:
  meta=json.loads(next(f)).get('payload',{})
  if meta.get('agent_path') not in wanted and meta.get('id')!=cli_thread:continue
  thread=meta.get('id');records=[];contexts=[];seen=set()
  for line in f:
   d=json.loads(line);v=d.get('payload',{})
   if d.get('type')=='turn_context':contexts.append({'timestamp':d.get('timestamp'),'turn_id':v.get('turn_id'),'model':v.get('model'),'effort':v.get('effort')})
   if d.get('type')=='token_usage_record' and v.get('thread_id')==thread and d.get('timestamp','')>=floor:
    key=v.get('response_id')
    if key in seen:raise RuntimeError('duplicate response usage record')
    seen.add(key);records.append({'timestamp':d.get('timestamp'),'response_id':key,'turn_id':v.get('turn_id'),'usage':v.get('usage')})
  totals=collections.Counter()
  for rec in records:totals.update(rec['usage'])
  rows.append({'agent_path':meta.get('agent_path') or ('cli_final_review_failed_infrastructure' if thread==cli_thread else None),'thread_id':thread,'source_log':str(p),'start':meta.get('timestamp'),'contexts':contexts,'usage_records':records,'actual_usage_sum':dict(totals)})
phase_rows=[]
for agent in rows:
 byturn={}
 for rec in agent['usage_records']:
  tid=rec['turn_id'];byturn.setdefault(tid,collections.Counter()).update(rec['usage'])
 for tid,total in byturn.items():
  if agent['agent_path']=='/root/hybrid_sol_lead':phase='metadata preparation' if tid=='01a0f904-c9c3-7890-9950-891fc70ec197' else ('implementation, technical verification and correction follow-through (mixed phase)' if tid=='01a0f90b-8174-7ef1-8a1a-adfff0506879' else 'canonical promotion and actual post-apply verification')
  elif agent['agent_path']=='/root/hybrid_astra_sources':phase='primary Astra source and consequence assessment'
  elif agent['agent_path']=='/root/hybrid_astra_final':phase='required independent final Astra assessment and correction decisions'
  else:phase='required final review CLI attempt, incomplete infrastructure overhead'
  models=sorted({ctx['model'] for ctx in agent['contexts'] if ctx['turn_id']==tid and ctx['model']})
  phase_rows.append({'agent_path':agent['agent_path'],'turn_id':tid,'actual_models':models,'phase':phase,'actual_usage_sum':dict(total)})
out={'snapshot_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'floor':floor+'Z','agents':rows,'per_turn_phase_usage':phase_rows,'root':{'thread_id':'01a0f63b-96a6-7dd2-a745-deec73593f58','actual_model':None,'usage':None,'reason':'Local root artifact contains no turn_context/token_usage_record; absence is unknown, not zero.'},'production_final_astra':{'status':'independent-agent-active; initial CLI attempt incomplete/no PASS','counting':'Required final source assessment is production, not extra pilot validation.'},'limitations':['In-progress snapshots exclude not-yet-logged responses.','All agent preparation after pilot instruction is included, including pre37percent-meter metadata work.','No matched allAstra baseline for these sources; model costs cannot establish causal savings.','Owner budget37percent start includes unrelated subscription use; exact perphase fractions unavailable unless response timing is explicitly bound.']}
(B/'usage-snapshot.json').write_text(json.dumps(out,indent=2)+'\n');print([(r['agent_path'],len(r['usage_records']),r['actual_usage_sum']) for r in rows])
