"""Collect only exact resumed worker usage records; no inherited root totals."""
import argparse,datetime,json
from pathlib import Path
WORKERS={
 "/root/source_resume":("01a1059d-97bc-7243-959e-fe0ecb2842d4","rollout-2026-10-04T08-32-56-01a1059d-97bc-7243-959e-fe0ecb2842d4.jsonl"),
 "/root/independent_resume":("01a1059d-cc36-7511-8636-c8595af9bf3d","rollout-2026-10-04T08-33-09-01a1059d-cc36-7511-8636-c8595af9bf3d.jsonl"),
 "/root/implementation_resume":("01a1059e-012f-75a1-9ed8-6cb0cf5ca572","rollout-2026-10-04T08-33-23-01a1059e-012f-75a1-9ed8-6cb0cf5ca572.jsonl")}
a=argparse.ArgumentParser();a.add_argument("--output",required=True,type=Path);a.add_argument("--before");a.add_argument("--after");a.add_argument("--workers-final",action="store_true");args=a.parse_args();assert not args.output.exists()
fields=["input_tokens","cached_input_tokens","cache_write_input_tokens","output_tokens","reasoning_output_tokens","total_tokens"]
result={"task":"T-0780","at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"workers_final":args.workers_final,"workers":[],"root_usage":"UNKNOWN_NOT_INCLUDED","meter_readings":"NOT_INFERRED_FROM_TOKENS","limitations":["Actual per-response worker records only, no inherited root cumulative usage.","Reasoning is included in output, never add twice.","Shared meter use cannot identify causal cost or savings.","Preparation, failed attempts, repairs, both Astra roles and finalization are production.","Without workers-final, later and unlogged usage is not included."]}
for name,(tid,filename) in WORKERS.items():
 path=Path("/Users/sverker/.codex/sessions/2026/10/04")/filename;records=[];seen=set();contexts=[]
 for line in path.open():
  row=json.loads(line);p=row.get("payload",{});at=row.get("timestamp","")
  if args.before and at>=args.before:continue
  if args.after and at<args.after:continue
  if row["type"]=="turn_context":contexts.append({"at":at,"turn_id":p.get("turn_id"),"model":p.get("model"),"effort":p.get("effort")})
  if row["type"]!="token_usage_record" or p.get("thread_id")!=tid:continue
  key=p["response_id"];assert key not in seen;seen.add(key);records.append({"at":at,"response_id":key,"turn_id":p["turn_id"],"usage":p["usage"]})
 turns={x["turn_id"] for x in records};contexts=[x for x in contexts if x["turn_id"] in turns]
 total={k:sum(x["usage"].get(k,0) for x in records) for k in fields};total["uncached_input_tokens"]=total["input_tokens"]-total["cached_input_tokens"]
 result["workers"].append({"agent":name,"thread_id":tid,"source_log":str(path),"contexts":contexts,"response_records":records,"usage_sum":total})
result["observed_worker_sum"]={k:sum(x["usage_sum"].get(k,0) for x in result["workers"]) for k in fields+["uncached_input_tokens"]}
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n");print(json.dumps({"output":str(args.output),"workers_final":args.workers_final,"observed_worker_sum":result["observed_worker_sum"]}))
