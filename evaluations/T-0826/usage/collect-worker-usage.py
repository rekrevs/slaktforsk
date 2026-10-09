import argparse, json, datetime
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("session");p.add_argument("agent");p.add_argument("model");p.add_argument("output");p.add_argument("--previous");a=p.parse_args()
records={}
for line in Path(a.session).open():
 x=json.loads(line)
 if x.get("type")=="token_usage_record":
  z=x["payload"];records[z["response_id"]]={"timestamp":x["timestamp"],"usage":z["usage"]}
previous=set(json.loads(Path(a.previous).read_text())["response_ids"]) if a.previous else set()
chosen={k:v for k,v in records.items() if k not in previous}
keys=["input_tokens","cached_input_tokens","cache_write_input_tokens","output_tokens","reasoning_output_tokens","total_tokens"]
total={k:sum(v["usage"].get(k,0) for v in chosen.values()) for k in keys}
out={"agent":a.agent,"model":a.model,"collected_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"distinct_responses":len(chosen),"response_ids":list(chosen),"usage":total,"uncached_input_tokens":total["input_tokens"]-total["cached_input_tokens"],"first_record":min((v["timestamp"] for v in chosen.values()),default=None),"last_record":max((v["timestamp"] for v in chosen.values()),default=None),"previous_ids_excluded":len(previous),"root_usage":"UNKNOWN","collection_rule":"Run after worker FINAL; includes preparation, interpretations, failed attempts, repairs and finalization. Reused role next task requires previous response-id exclusion."}
Path(a.output).write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="response_ids"}))
