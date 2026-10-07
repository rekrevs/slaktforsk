"""Root-only controlled apply: exact reviewed package with explicit expected state per step.

This helper is never invoked by the preparation/implementation agent.
"""
import argparse, datetime, hashlib, json, pathlib, sqlite3, subprocess
B=pathlib.Path(__file__).resolve().parent; R=B.parents[1]
a=argparse.ArgumentParser();a.add_argument("gate");args=a.parse_args()
gate_path=pathlib.Path(args.gate);gate=json.loads(gate_path.read_text())
assert gate["approved"]=="CONTROLLED_APPLY_EXACT_PACKAGE"
assert gate["task"]=="T-0778"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for row in gate["pinned_artifacts"]:assert sha(R/row["path"])==row["sha256"]
def state():
 c=sqlite3.connect("file:"+str(R/"genealogy2/data/research.sqlite")+"?mode=ro",uri=True)
 head=c.execute("select max(sequence) from operation_payload").fetchone()[0]
 pending=c.execute("select count(*) from review_request q left join review_resolution r on q.id=r.request_id where r.request_id is null").fetchone()[0];c.close();return {"journal_head":head,"pending":pending}
assert state()==gate["baseline_state"]
out=B/"canonical-apply-C1047";out.mkdir(exist_ok=True)
for i,row in enumerate(gate["operations"],1):
 assert state()==row["expected_before"]
 path=R/row["path"];assert sha(path)==row["sha256"]
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=subprocess.run(["node","genealogy2/cli.mjs","apply",str(path)],cwd=R,capture_output=True,text=True)
 receipt={"started_at_utc":started,"finished_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"gate_path":str(gate_path),"gate_sha256":sha(gate_path),"operation_path":row["path"],"operation_sha256":row["sha256"],"expected_before":row["expected_before"],"expected_after":row["expected_after"],"exit_code":result.returncode,"stdout":result.stdout,"stderr":result.stderr,"actual_after":state()}
 (out/f"{i:02d}-apply-receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
 assert result.returncode==0,receipt
 assert receipt["actual_after"]==row["expected_after"],receipt
 print("Applied",i,"of",len(gate["operations"]),receipt["actual_after"],flush=True)
assert state()==gate["final_state"]
