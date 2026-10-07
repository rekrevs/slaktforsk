"""Append verified implementation/completion evidence to a bounded-pass measurement."""
import json,hashlib,sys,datetime
from pathlib import Path
p=Path(__file__).resolve().parent
measurement,post,category=sys.argv[1:]
f=p/measurement;d=json.loads(f.read_text());citation=post.upper().replace('C','C-',1)
assert not any(e.get('post')==citation and e['category']==category for e in d['events'])
if category=='canonical_application':
 q=p/f'{post}-canonical-implementation-receipt-20260930.json';r=json.loads(q.read_text());assert r['actual_full_match'] and r['pending']==0 and all(v['ok'] for v in r['validators'].values())
 ids=[c['id'] for label in ['source','person'] for c in json.loads((p/f'{post}-{label}-proposed-operation-20260930.json').read_text())['changes']]
 e={'at_utc':r['verified_at_utc'],'category':category,'post':citation,'journal_end':r['journal'],'object_ids':ids,'new_objects':r['new_objects'],'revisions':r['revised_objects'],'pending':0,'validators':'verify/verify-assets/verify-source PASS'}
elif category=='post_completion':
 q=p/f'{post}-astra-completion-20260930.json';r=json.loads(q.read_text());at=r['accepted_at'];elapsed=int((datetime.datetime.fromisoformat(at.replace('Z','+00:00'))-datetime.datetime.fromisoformat(d['started_at_utc'].replace('Z','+00:00'))).total_seconds());e={'at_utc':at,'category':category,'post':citation,'elapsed_from_pass_start_seconds':elapsed,'result':'Bounded source scope accepted after canonical verification.'}
else:raise ValueError(category)
e['evidence']=[{'path':str(q.relative_to(p.parents[2])),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}];d['events'].append(e);applied=[x for x in d['events'] if x['category']=='canonical_application'];d['latest_totals'].update(canonical_objects_created_or_revised=len(set(i for x in applied for i in x['object_ids'])),canonical_change_entries=sum(len(x['object_ids']) for x in applied),completed_post_scopes=sum(x['category']=='post_completion' for x in d['events']));d['latest_checkpoint_utc']=e['at_utc'];f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(d['latest_totals'])
