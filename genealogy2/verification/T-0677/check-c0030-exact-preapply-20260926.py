import json,hashlib,sqlite3,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[2]
load=lambda n:json.loads((H/n).read_text())
sha=lambda n:hashlib.sha256((H/n).read_bytes()).hexdigest()
expected={
'c0030-root-source-proposal-acceptance-20260925.json':'dcf1fb48b762ebf11772ff89db57737578e7e5c88e4844fe93f8be0bd260dfb8',
'c0030-root-substantive-build-acceptance-20260925.json':'563fc17fa377255a5e0357367e580339fee24673f9081692965bc91f5f4426bb',
'c0030-root-split-build-amendment-20260925.json':'944521e2978320b7d2955b8f49e9da46fc74ca270b754dc77dd4d6d858ea577c',
'c0030-source-split-proposed-operation-20260925.json':'5ba48d4a1ef09d2033966b9bb8102303164dfec5d9ca08a53c1c4a4a8b626027',
'c0030-person-split-proposed-operation-20260925.json':'eaf85a71bb256dd231f6c8692d801a5ac0d0a2afb63a06e6f8c0d9f2703fe7a3',
'c0030-split-temp-full-diffcheck-20260925.json':'3b2948df35f18cd05d1801e18494dc6d52bf9060670ff00345f9ac1de6dd3a2a',
'c0030-split-temp-after-pending-full-20260925.json':'9f98bd13d51972222a621b7eee4771a6e6f426a8e4b333d2454f436bce22b5dc',
'c0030-split-temp-preflight-summary-20260925.json':'6746d472e5ccabf841522d5378a863948fc6fab0a00a579fe8aeb181546c884a',
'c0030-split-temp-pending-individual-review-proposed-20260925.json':'57ab2379da78b08b7f9ec77db7ed177e57601c1158777d6caf3d76f0cd2f14ab'}
checks=[]
def ck(name,condition,detail=''):
 checks.append((name,bool(condition),detail))
for n,h in expected.items():ck('sha '+n,sha(n)==h,sha(n))
source=load('c0030-source-split-proposed-operation-20260925.json');person=load('c0030-person-split-proposed-operation-20260925.json');combined=load('c0030-combined-proposed-operation-20260925.json')
sc=source['changes'];pc=person['changes'];cc=combined['changes']
ck('operation split union equals combined changes by full change payload',len(sc)==4 and len(pc)==8 and len(cc)==12 and sorted(sc+pc,key=lambda x:x['id'])==sorted(cc,key=lambda x:x['id']))
ck('source then person staged partition',len({x['id'] for x in sc+pc})==12 and [x['id'] for x in sc]==['TR-T0677-C0030-consolidated-control','AUDIT-T0677-C0030','O-T0677-C0030-row9-control','O-T0677-C0030-row10-control'] and {x['id'] for x in sc}.isdisjoint({x['id'] for x in pc}))
ck('operation policy 2',all(x['dependencyReviewVersion']==2 for x in (source,person,combined)))
proposal=load('c0030-native-source-proposed-v2-20260925.json')
ck('approved source proposal hash',sha('c0030-native-source-proposed-v2-20260925.json')==load('c0030-root-substantive-build-acceptance-20260925.json')['source_sha256'])
ck('approved person proposal hash',sha('c0030-person-impact-proposed-20260925.json')==load('c0030-root-substantive-build-acceptance-20260925.json')['person_sha256'])
sp={x['id']:x for x in proposal['proposed_changes']}
ck('four source change payloads equal approved after',len(sp)==4 and all(x=={'id':x['id'],'kind':sp[x['id']]['kind'],'expectedVersion':sp[x['id']]['expectedVersion'],**{**sp[x['id']]['after'],'data':{**sp[x['id']]['after']['data'],**({'value_json':json.loads(sp[x['id']]['after']['data']['value_json'])} if sp[x['id']]['after']['data'].get('value_json') else {})},'origins':[{'unit':o['unit_id'],'coverage':o['coverage'],'note':o['note']} for o in sp[x['id']]['after']['origins']]}} for x in sc))
impact=load('c0030-person-impact-proposed-20260925.json')
ck('person ids/types/versions equal approved proposal',set((x['id'],x['kind'],x['expectedVersion']) for x in pc)==set((x['object_id'],x['kind'],x['expected_version']) for x in impact['changes']+impact['adoptions']))
byid={x['id']:x for x in pc};field_ok=[];before_ok=[];evidence_ok=[]
for p in impact['changes']:
 x=byid[p['object_id']];old=p['current_full'];before_ok.append(x['expectedVersion']==old['revision']['version'])
 for f in p['fields']:
  target=x['data'] if f['field'] in x['data'] else x
  field_ok.append(target[f['field']]==f['after'] and (old['data'].get(f['field']) if f['field'] in old['data'] else old['revision'].get(f['field']))==f['before'])
  for rep in f['exact_replacements']:field_ok.append(f['before'].count(rep['old'])==1 and f['after'].count(rep['new'])==1)
 old_ev=[{'object':e['basis_revision_id'].rsplit('@',1)[0],'version':int(e['basis_revision_id'].rsplit('@',1)[1]),'role':e['role'],'note':e['note']} for e in old['evidence']]
 add_ev=[{'object':e['basis_revision_id'].rsplit('@',1)[0],'version':int(e['basis_revision_id'].rsplit('@',1)[1]),'role':e['role'],'note':e['note']} for e in p['evidence_add']]
 evidence_ok.append(sorted(x['evidence'],key=str)==sorted(old_ev+add_ev,key=str))
ck('six approved person field replacements',len(field_ok)>=6 and all(field_ok),str(len(field_ok)))
ck('six approved person previous versions',all(before_ok))
ck('six approved person evidence additions only',all(evidence_ok))
for a in impact['adoptions']:
 x=byid[a['object_id']]
 ck('adoption '+a['object_id'],x['data']==a['data'] and x['expectedVersion']==a['expected_version'])
# canonical full payloads and temp diff
con=sqlite3.connect(f"file:{R/'genealogy2/data/research.sqlite'}?mode=ro",uri=True);con.row_factory=sqlite3.Row
def rows(q,args=()):return [dict(r) for r in con.execute(q,args)]
def full(rid):
 r=rows('select * from revision where id=?',(rid,))[0];kind=rows('select kind from object where id=?',(r['object_id'],))[0]['kind'];d=rows(f'select * from {kind} where revision_id=?',(rid,))[0];d.pop('revision_id')
 for k,v in list(d.items()):
  if k.endswith('_json') and v is not None:d[k]=json.loads(v)
 origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in rows('select unit_id,coverage,note from origin where revision_id=?',(rid,))]
 evidence=[]
 for x in rows('select basis_revision_id,role,note from dependency where revision_id=?',(rid,)):
  o,v=x['basis_revision_id'].rsplit('@',1);evidence.append({'object':o,'version':int(v),'role':x['role'],'note':x['note']})
 return {'kind':kind,'revision':r,'data':d,'origins':origins,'evidence':evidence}
ck('canonical journal 192',max(int(p.name[0:9]) for p in (R/'genealogy2/journal').glob('*.json'))==192)
ck('canonical pending zero',rows('select count(*) as n from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null')[0]['n']==0)
diff=load('c0030-split-temp-full-diffcheck-20260925.json');items=diff['items'];ck('temp diff 12 unique items',len(items)==12 and {x['id'] for x in items}=={x['id'] for x in sc+pc})
for item in items:
 x=next(x for x in sc+pc if x['id']==item['id']);v=x['expectedVersion'];old=full(f"{x['id']}@{v}") if v is not None else None
 ck('canonical before '+x['id'],item['before']==old and (not v or rows('select max(version) as v from revision where object_id=?',(x['id'],))[0]['v']==v))
 a=item['after'];operation=source if x in sc else person
 ck('temp after '+x['id'],a['kind']==x['kind'] and a['data']==x['data'] and a['revision']['operation_id']==operation['id'] and a['revision']['version']==(v+1 if v else 1) and all(a['revision'][k]==x[change] for k,change in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')]) and sorted(a['origins'],key=str)==sorted(x.get('origins',[]),key=str) and sorted(a['evidence'],key=str)==sorted(x['evidence'],key=str))
 ck('changed fields '+x['id'],item['changed_typed_fields']==([] if old is None else [k for k in sorted(set(old['data'])|set(a['data'])) if old['data'].get(k)!=a['data'].get(k)]))
summary=load('c0030-split-temp-preflight-summary-20260925.json');pending=load('c0030-split-temp-after-pending-full-20260925.json');review=load('c0030-split-temp-pending-individual-review-proposed-20260925.json')
ck('temp summary hashes',summary['operation_sha256']=={'source':sha('c0030-source-split-proposed-operation-20260925.json'),'person':sha('c0030-person-split-proposed-operation-20260925.json')} and summary['full_diff_sha256']==sha('c0030-split-temp-full-diffcheck-20260925.json'))
ck('temp stage counts and validators',summary['stage_pending']['source']['data']['count']==0 and pending['count']==4 and all(summary['results'][k]['result']['ok'] for k in ['verify','verify-assets','verify-source']))
ck('individual request IDs and full payloads',len(review['dispositions'])==4 and {x['request_id'] for x in review['dispositions']}=={x['id'] for x in pending['requests']} and all(x['affected_full']==next(i['after'] for i in items if i['after']['revision']['id']==x['affected_revision_id']) and x['changed_full']==next(i['after'] for i in items if i['after']['revision']['id']==x['changed_revision_id']) for x in pending['requests']) and all(next(d for d in review['dispositions'] if d['request_id']==x['id'])['affected_full']==x['affected_full'] and next(d for d in review['dispositions'] if d['request_id']==x['id'])['changed_full']==x['changed_full'] for x in pending['requests']))

for n,ok,d in checks:print(('PASS' if ok else 'FAIL'),n,d[:160])
print('TOTAL',sum(ok for _,ok,_ in checks),'/',len(checks))
raise SystemExit(0 if all(ok for _,ok,_ in checks) else 1)
