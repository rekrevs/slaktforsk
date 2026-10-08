"""Task-local candidate staging scaffold. NEVER writes live Wotan.
Run only after source-settled literal proposal arrives; root authorizes live edits
separately after independent hash approval. No task/priority/source inference.
"""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
BASE=R/'evaluations/T-0793/wotan-before-front-tasks-v1.json'
EXPECTED=[f'T-{n:04d}' for n in range(806,814)]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def verify_current_baseline():
 b=json.loads(BASE.read_text());live=json.loads((R/'wotan/backlog.json').read_text())
 assert live==b['backlog'],'Live backlog changed since source baseline'
 for tid,digest in b['devlog_sha256'].items():
  assert sha(R/f'wotan/dev-log/{tid}.md')==digest,tid
 assert live['next_id']==806
 return b,live
def stage(proposal,out):
 b,old=verify_current_baseline();new=proposal['new_tasks']
 assert [x['entry']['id'] for x in new]==EXPECTED
 assert all(isinstance(x['devlog_text'],str) and x['devlog_text'].strip() for x in new)
 assert all(x['entry']['id'] not in {t['id'] for t in old['tasks']} for x in new)
 assert proposal['next_id']==814
 # Source supplies the exact anchor. Neither titles nor priorities choose it.
 anchor=proposal['insert_before_id'];assert anchor in {t['id'] for t in old['tasks']}
 tasks=list(old['tasks']);at=next(i for i,t in enumerate(tasks) if t['id']==anchor)
 tasks[at:at]=[x['entry'] for x in new]
 move=proposal.get('move_existing_task')
 if move:
  assert move['id']=='T-0793';item=next(t for t in tasks if t['id']=='T-0793')
  tasks=[t for t in tasks if t['id']!='T-0793'];at=next(i for i,t in enumerate(tasks) if t['id']==move['before_id']);tasks.insert(at,item)
 oldids={t['id'] for t in old['tasks']};assert [t for t in tasks if t['id']in oldids and t['id']!='T-0793']==[t for t in old['tasks'] if t['id']!='T-0793']
 assert all(next(t for t in tasks if t['id']==x['id'])==x for x in old['tasks'])
 assert len(tasks)==len(old['tasks'])+8 and len({t['id']for t in tasks})==len(tasks)
 candidate={**old,'next_id':814,'tasks':tasks};assert not out.exists();out.mkdir(parents=True)
 (out/'backlog.json').write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+'\n')
 files=[]
 for x in new:
  p=out/'dev-log'/f"{x['entry']['id']}.md";p.parent.mkdir(exist_ok=True);p.write_text(x['devlog_text']);files.append(p)
 seen=set()
 for a in proposal.get('existing_log_appends',[]):
  tid=a['task_id'];assert tid not in seen and tid in b['devlog_sha256'];seen.add(tid)
  original=(R/f'wotan/dev-log/{tid}.md').read_bytes();append=a['append_text'].encode();assert append.strip()
  p=out/'dev-log'/f'{tid}.md';assert not p.exists();p.write_bytes(original+append);assert p.read_bytes().startswith(original);files.append(p)
 # Complete source map/partitions are copied literally, never generated here.
 for name in ['fixed160_ownership','scope_partitions']:
  (out/(name+'.json')).write_text(json.dumps(proposal[name],ensure_ascii=False,indent=2)+'\n');files.append(out/(name+'.json'))
 proof={'live_wotan_unchanged':True,'reserved_ids':EXPECTED,'all_old_entries_status_after_priority_exact':True,'old_relative_order_exact_except_explicit_T0793_move':True,'old_log_full_prefixes_exact':True,'next_id':814,'files':[{'path':str(p.relative_to(R)),'sha256':sha(p)}for p in [out/'backlog.json',*files]],'source_scope_validation':'Requires independent Astra exact proposal and union review; no semantic certification by this scaffold.'}
 (out/'mechanical-candidate-proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
 verify_current_baseline();return proof
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--proposal',required=True);a.add_argument('--proposal-sha256',required=True);a.add_argument('--output',required=True);v=a.parse_args();p=Path(v.proposal).resolve();assert p.is_relative_to(R/'evaluations/T-0793') and sha(p)==v.proposal_sha256;o=Path(v.output).resolve();assert o.is_relative_to(R/'evaluations/T-0793');print(json.dumps(stage(json.loads(p.read_text()),o)))
