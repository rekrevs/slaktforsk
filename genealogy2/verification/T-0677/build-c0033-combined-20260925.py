"""Build C0033 operation from root-approved locked proposals; never apply canonical."""
import copy,hashlib,json,sqlite3
from collections import defaultdict
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
files={'source':H/'c0033-native-source-proposed-v2-20260925.json','person':H/'c0033-person-impact-proposed-20260925.json','accept':H/'c0033-root-substantive-build-acceptance-20260925.json'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'source':'7eccb47b67978a569d87c75d57c2f1bb262b6d9fa56d021ce02c8da599ab074d','person':'38cf19e95d003b94d6fef571285dea141b211c761e0e02197c31f8c2b586a234','accept':'def15a26acfde3d6aeb71981eb635c0d6a356bb5ab269b2ea1eee289a255172e'}
for k in files:assert sha(files[k])==expected[k],k
source,person,accept=(json.loads(files[k].read_text()) for k in files)
head=sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1].name
assert head.startswith('000000189-'),head
con=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);con.row_factory=sqlite3.Row
def rows(q,a=()):return [dict(x) for x in con.execute(q,a)]
assert not rows('SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id WHERE rs.request_id IS NULL')
def cur(oid):
 ob=rows('SELECT kind FROM object WHERE id=?',(oid,));assert len(ob)==1,oid
 kind=ob[0]['kind'];rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))[0]
 data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],))[0];data.pop('revision_id')
 for k,v in tuple(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rev['id'],))]
 evidence=[]
 for x in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rev['id'],)):
  o,v=x['basis_revision_id'].rsplit('@',1);evidence.append({'object':o,'version':int(v),'role':x['role'],'note':x['note']})
 return kind,rev,data,origins,evidence
def edge(x):
 if 'basis_revision_id' in x:
  o,v=x['basis_revision_id'].rsplit('@',1);return {'object':o,'version':int(v),'role':x['role'],'note':x['note']}
 return copy.deepcopy(x)
def ref(r,note):
 o,v=r.rsplit('@',1);return {'object':o,'version':int(v),'role':'supports','note':note}
def ek(e):return (e['object'],e['version'],e['role'])
sourceout=[]
for p in source['proposed_changes']:
 oid=p['id'];assert p['expectedVersion'] is None and not rows('SELECT id FROM object WHERE id=?',(oid,))
 a=copy.deepcopy(p['after'])
 for k,v in tuple(a['data'].items()):
  if k.endswith('_json') and isinstance(v,str):a['data'][k]=json.loads(v)
 a['origins']=[{'unit':x.get('unit',x.get('unit_id')),'coverage':x['coverage'],'note':x['note']} for x in a['origins']]
 a['evidence']=[edge(x) for x in a['evidence']]
 sourceout.append({'id':oid,'kind':p['kind'],'expectedVersion':None,**a})
assert len(sourceout)==6
patch=defaultdict(dict);ver={};support=defaultdict(set)
for p in person['changes']:
 oid,f=p['object_id'],p['field'];assert f not in patch[oid],(oid,f)
 assert oid not in ver or ver[oid]==p['expected_revision'];ver[oid]=p['expected_revision'];patch[oid][f]=p
 support[oid].update(p['evidence_add_supports'])
assert len(patch)==13 and sum(map(len,patch.values()))==20
snap={x['object_id']:x for x in person['full_current_changed']};assert set(snap)==set(patch)
pout=[];checks=[]
for oid,fields in sorted(patch.items()):
 kind,rev,data,orig,ev=cur(oid);s=snap[oid]
 assert rev['id']==ver[oid]==s['revision']['id'] and kind==s['kind'] and data==s['data'],oid
 assert sorted(orig,key=lambda x:x['unit'])==sorted([{'unit':x.get('unit',x.get('unit_id')),'coverage':x['coverage'],'note':x['note']} for x in s['origins']],key=lambda x:x['unit']),oid
 assert sorted(ev,key=ek)==sorted([edge(x) for x in s['evidence']],key=ek),oid
 d=copy.deepcopy(data);m={'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],'rationale':rev['rationale'],'caveat':rev['caveat']}
 for f,p in fields.items():
  before=d[f] if f in d else m[f];assert before==p['before'],(oid,f)
  if p['exact_replacements']:
   assert isinstance(before,str) and isinstance(p['after'],str)
   t=before
   for old,new in p['exact_replacements']:
    assert t.count(old)==1,(oid,f,old[:70],t.count(old));t=t.replace(old,new,1)
   assert t==p['after'],(oid,f,'replacement mismatch')
  if f in d:d[f]=p['after']
  else:m[f]=p['after']
 m['rationale']=rev['rationale']+' T-0677 C-0033, acceptanskriterium 1 och 3: '+' '.join(fields[f]['rationale'] for f in sorted(fields))
 added=[];seen={ek(x) for x in ev}
 for r in sorted(support[oid]):
  x=ref(r,'Samma C-0033-post: eget avgränsat rad-2-underlag och dokumentärt återbruk enligt fältpreciseringen; ingen extra oberoende källröst.')
  if ek(x) not in seen:added.append(x);seen.add(ek(x))
 pout.append({'id':oid,'kind':kind,'expectedVersion':rev['version'],'data':d,**m,'origins':orig,'evidence':ev+added})
 checks.append({'id':oid,'fields':sorted(fields),'current_revision':rev['id'],'added_evidence':added,'origins_preserved':True})
ad=[]
for a in person['adoptions']:
 oid=a['proposed_id'];assert not rows('SELECT id FROM object WHERE id=?',(oid,))
 assert a['outcome']=='adopted_with_limits'
 ad.append({'id':oid,'kind':'assessment','expectedVersion':None,'data':{'subject_id':a['subject_id'],'criteria':'bounded_source_adoption/1','outcome':a['outcome'],'body':a['body']},'disposition':'recorded','evidenceStatus':None,'rationale':'T-0677 C-0033: avgränsad källadoption enligt acceptanskriterium 1 och 3; inga PK-, identitets- eller trädgrindar höjs.','caveat':'','evidence':[ref(r,'Samma avgränsade C-0033-post med versionsbundet återbruk; ingen extra oberoende källröst.') for r in a['basis']]})
assert len(ad)==2
changes=sourceout+pout+ad;assert len(changes)==21 and len({x['id'] for x in changes})==21
by={x['id']:x for x in changes};deps={x['id']:{e['object'] for e in x['evidence'] if e['object'] in by and e['version']==(by[e['object']]['expectedVersion'] or 0)+1} for x in changes}
order=[];done=set()
while len(done)<len(changes):
 ready=[o for o in by if o not in done and deps[o]<=done];assert ready,deps
 order+=ready;done.update(ready)
stale=[(x['id'],e) for x in changes for e in x['evidence'] if e['object'] in by and by[e['object']]['expectedVersion'] is not None and e['version']==by[e['object']]['expectedVersion']]
assert not stale,stale
op={'id':'T-0677/C0033-source-person-adoption-v1','actor':'Codex Sol; root/Astra approved bounded source and person decisions','reason':'T-0677 C-0033: acceptanskriterium 1 och 3, full relevant rad-2-källkontroll med explicit återbruk och individuellt sakgranskade person- och forskningsföljder. R@1 bevaras; inga automatiska rebaser eller grindhöjningar.','dependencyReviewVersion':2,'changes':[by[o] for o in order]}
out=H/'c0033-combined-proposed-operation-20260925.json';out.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
report={'task':'T-0677','state':'TEMP_PROPOSAL_ONLY_NOT_CANONICAL_APPLY','canonical_head':head,'pending':0,'inputs':{k:{'path':str(files[k].relative_to(ROOT)),'sha256':sha(files[k])} for k in files},'operation_sha256':sha(out),'counts':{'objects':21,'source_creates':6,'person_revisions':13,'person_fields':20,'adoption_creates':2,'creates':8,'revisions':13,'stale_old_basis_edges':0},'person_checks':checks,'full_before_after':[{'id':x['id'],'before':None if x['expectedVersion'] is None else {'kind':cur(x['id'])[0],'revision':cur(x['id'])[1],'data':cur(x['id'])[2],'origins':cur(x['id'])[3],'evidence':cur(x['id'])[4]},'after':x} for x in op['changes']],'ordered_ids':order,'R_retained':'R-86e25c6dd1c2141e8454c02e@1','no_canonical_apply':True}
rp=H/'c0033-combined-buildcheck-20260925.json';rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'operation_sha256':sha(out),'buildcheck_sha256':sha(rp),'counts':report['counts']}))
