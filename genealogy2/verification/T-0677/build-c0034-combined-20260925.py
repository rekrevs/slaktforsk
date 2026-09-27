"""Build root-approved C0034 source/person/adoption proposal; no canonical apply."""
import copy,hashlib,json,sqlite3
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
paths={'source':H/'c0034-native-source-proposed-v2-20260925.json','person':H/'c0034-person-impact-proposed-20260925.json','accept':H/'c0034-root-substantive-build-acceptance-20260925.json'}
expected={'source':'b7a3eff7c540362347b444809f2568be7c1f0bc99d7886ab91e45b69bc8ea6f5','person':'cd9fc9ef7052d76541eba25da4fb1349de3f6571a6ba1f2800d020ee69efbbb4','accept':'0cad86ea444deb787015db0684c3f9ba9ae0df65757c3a92dc1b5fb0f1c2df7e'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for k,p in paths.items():assert sha(p)==expected[k],k
source,person,accept=(json.loads(paths[k].read_text()) for k in paths)
head=sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1].name;assert head.startswith('000000190-'),head
con=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);con.row_factory=sqlite3.Row
rows=lambda q,a=():[dict(x) for x in con.execute(q,a)]
assert not rows('SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id WHERE rs.request_id IS NULL')
def edge(x):
 if 'basis_revision_id' in x:
  o,v=x['basis_revision_id'].rsplit('@',1);return {'object':o,'version':int(v),'role':x['role'],'note':x['note']}
 return copy.deepcopy(x)
def ek(e):return(e['object'],e['version'],e['role'],e['note'])
def current(oid):
 ob=rows('SELECT kind FROM object WHERE id=?',(oid,));assert len(ob)==1,oid
 kind=ob[0]['kind'];rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))[0]
 data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],))[0];data.pop('revision_id')
 for k,v in tuple(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origin=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rev['id'],))]
 evidence=[]
 for x in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rev['id'],)):
  evidence.append(edge(x))
 return {'kind':kind,'revision':rev,'data':data,'origins':origin,'evidence':evidence}
def normalize(x):return {'kind':x['kind'],'revision':x['revision'],'data':x['data'],'origins':sorted(x['origins'],key=lambda e:e['unit']),'evidence':sorted(x['evidence'],key=ek)}
def snapshot_to_current(s):
 return {'kind':s['kind'],'revision':s['revision'],'data':s['data'],'origins':[{'unit':e.get('unit',e.get('unit_id')),'coverage':e['coverage'],'note':e['note']} for e in s['origins']],'evidence':[edge(e) for e in s['evidence']]}
sout=[]
for p in source['proposed_changes']:
 oid=p['id'];version=p['expectedVersion'];a=copy.deepcopy(p['after'])
 for k,v in tuple(a['data'].items()):
  if k.endswith('_json') and isinstance(v,str):a['data'][k]=json.loads(v)
 a['origins']=[{'unit':e.get('unit',e.get('unit_id')),'coverage':e['coverage'],'note':e['note']} for e in a['origins']]
 a['evidence']=[edge(e) for e in a['evidence']]
 if version is None:assert not rows('SELECT id FROM object WHERE id=?',(oid,))
 else:
  before=current(oid);assert before['revision']['version']==version and before['kind']==p['kind']
  assert before['data']==a['data'] and sorted(before['origins'],key=lambda e:e['unit'])==sorted(a['origins'],key=lambda e:e['unit'])
  assert sorted(before['evidence'],key=ek)==sorted(a['evidence'],key=ek)
  assert a['disposition']==before['revision']['disposition'] and a['evidenceStatus']==before['revision']['evidence_status']
 sout.append({'id':oid,'kind':p['kind'],'expectedVersion':version,**a})
assert len(sout)==6
pout=[];approved_replaces=[]
for p in person['changes']:
 oid=p['object_id'];before=current(oid);snapshot=snapshot_to_current(p['current_full'])
 assert normalize(before)==normalize(snapshot),oid
 assert before['revision']['version']==p['expected_version']
 d=copy.deepcopy(before['data']);m={'disposition':before['revision']['disposition'],'evidenceStatus':before['revision']['evidence_status'],'rationale':before['revision']['rationale'],'caveat':before['revision']['caveat']}
 for f in p['fields']:
  name=f['field'];val=d[name] if name in d else m[name];assert val==f['before'],(oid,name)
  if f['exact_replacements']:
   assert isinstance(val,str);text=val
   for pair in f['exact_replacements']:
    old,new=pair['old'],pair['new'];assert text.count(old)==1,(oid,name,old[:50]);text=text.replace(old,new,1)
   assert text==f['after'],(oid,name)
  if name in d:d[name]=f['after']
  else:m[name]=f['after']
 m['rationale']=before['revision']['rationale']+' T-0677 C-0034, acceptanskriterium 1 och 3: '+' '.join(dict.fromkeys(f['rationale'] for f in p['fields']))
 ev=copy.deepcopy(before['evidence'])
 for replacement in p['evidence_replace']:
  old,new=edge(replacement['before']),edge(replacement['after']);assert ev.count(old)==1,(oid,old)
  ev[ev.index(old)]=new;approved_replaces.append({'target':oid,'before':old,'after':new})
 for raw in p['evidence_add']:
  e=edge(raw);assert e not in ev,(oid,e);ev.append(e)
 pout.append({'id':oid,'kind':before['kind'],'expectedVersion':before['revision']['version'],'data':d,**m,'origins':before['origins'],'evidence':ev})
assert len(pout)==7 and sum(len(x['fields']) for x in person['changes'])==9
assert len(approved_replaces)==4
ad=[]
for a in person['adoptions']:
 oid=a['object_id'];assert not rows('SELECT id FROM object WHERE id=?',(oid,))
 assert a['data']['criteria']=='bounded_source_adoption/1' and a['data']['outcome']=='adopted_with_limits'
 ad.append({'id':oid,'kind':a['kind'],'expectedVersion':None,'data':a['data'],'disposition':'recorded','evidenceStatus':None,'rationale':'T-0677 C-0034: avgränsad källadoption enligt acceptanskriterium 1 och 3; inga PK-, identitets- eller trädgrindar höjs.','caveat':'','evidence':[edge(e) for e in a['evidence_add']]})
assert len(ad)==2
changes=sout+pout+ad;assert len(changes)==15 and len({x['id'] for x in changes})==15
by={x['id']:x for x in changes}
deps={x['id']:{e['object'] for e in x['evidence'] if e['object'] in by and e['version']==(by[e['object']]['expectedVersion'] or 0)+1} for x in changes}
order=[];done=set()
while len(done)<len(changes):
 ready=[o for o in by if o not in done and deps[o]<=done];assert ready,deps
 order+=ready;done.update(ready)
stale=[(x['id'],e) for x in changes for e in x['evidence'] if e['object'] in by and by[e['object']]['expectedVersion'] is not None and e['version']==by[e['object']]['expectedVersion']]
assert not stale,stale
op={'id':'T-0677/C0034-source-person-adoption-v1','actor':'Codex Sol; root/Astra approved bounded source and person decisions','reason':'T-0677 C-0034: acceptanskriterium 1 och 3, full relevant vigselpostkontroll med dokumentärt återbruk, reserverade råfält och individuellt sakgranskade följder. Endast fyra explicit godkända evidensversionsbyten; inga grindhöjningar.','dependencyReviewVersion':2,'changes':[by[o] for o in order]}
out=H/'c0034-combined-proposed-operation-20260925.json';out.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
report={'task':'T-0677','state':'PROPOSAL_ISOLATED_TEMP_ONLY','canonical_head':head,'pending':0,'inputs':{k:{'path':str(paths[k].relative_to(ROOT)),'sha256':sha(paths[k])} for k in paths},'operation_sha256':sha(out),'counts':{'objects':15,'source_revision':1,'source_creates':5,'person_revisions':7,'person_fields':9,'adoption_creates':2,'revisions':8,'creates':7,'approved_evidence_replacements':4,'stale_same_operation_edges':0},'approved_evidence_replacements':approved_replaces,'ordered_ids':order,'full_before_after':[{'id':x['id'],'before':None if x['expectedVersion'] is None else current(x['id']),'after':x} for x in op['changes']],'no_canonical_apply':True,'no_review_resolution':True}
rp=H/'c0034-combined-buildcheck-20260925.json';rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'operation_sha256':sha(out),'buildcheck_sha256':sha(rp),'counts':report['counts']}))
