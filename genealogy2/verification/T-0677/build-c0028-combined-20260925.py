"""Build root-approved C-0028 proposal for isolated validation only."""
import copy
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
FILES={
 'source':HERE/'c0028-native-source-proposed-v2-20260925.json',
 'person':HERE/'c0028-person-impact-proposed-v2-20260925.json',
 'accept':HERE/'c0028-root-substantive-build-acceptance-20260925.json',
}
EXPECTED={
 'source':'7f5559cf440b44928bc70a037b3bcbc03620e79cb6d0cd70939d4ab8c14bf9b5',
 'person':'0db319b2fe062a74202a6a1699da30c26f6232b4e39dbbb52b36f589d45aefc0',
}
OUT=HERE/'c0028-combined-proposed-operation-20260925.json'
REPORT=HERE/'c0028-combined-buildcheck-20260925.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for k in ('source','person'):assert sha(FILES[k])==EXPECTED[k]
source,person,accept=[json.loads(FILES[k].read_text()) for k in FILES]
assert accept['state']=='ACCEPTED_FOR_ISOLATED_BUILD_AND_TEMP_ONLY'
assert [x['sha256'] for x in accept['inputs']]==[EXPECTED['source'],EXPECTED['person']]
head=sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1].name
assert head.startswith('000000188-')
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(x) for x in conn.execute(sql,args)]
assert not rows('SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id WHERE rs.request_id IS NULL')
def current(oid):
 obj=rows('SELECT kind FROM object WHERE id=?',(oid,));assert len(obj)==1,oid
 kind=obj[0]['kind'];rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
 assert len(rev)==1;rev=rev[0]
 data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],));assert len(data)==1
 data=data[0];data.pop('revision_id')
 for k,v in tuple(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origins=[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']}
          for r in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id',(rev['id'],))]
 evidence=[]
 for r in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role',(rev['id'],)):
  basis,version=r['basis_revision_id'].rsplit('@',1)
  evidence.append({'object':basis,'version':int(version),'role':r['role'],'note':r['note']})
 return kind,rev,data,origins,evidence
def edge(raw):
 if 'basis_revision_id' in raw:
  basis,version=raw['basis_revision_id'].rsplit('@',1)
  return {'object':basis,'version':int(version),'role':raw['role'],'note':raw['note']}
 return copy.deepcopy(raw)
def ref_edge(ref,role,note):
 basis,version=ref.rsplit('@',1)
 return {'object':basis,'version':int(version),'role':role,'note':note}
def ekey(e):return (e['object'],e['version'],e['role'])

assert current('R-C0028-15')[1]['id']=='R-C0028-15@1'
source_changes=[];source_checks=[]
for p in source['proposed_changes']:
 oid=p['id'];assert p['expectedVersion'] is None and not rows('SELECT id FROM object WHERE id=?',(oid,))
 after=copy.deepcopy(p['after'])
 for k,v in tuple(after['data'].items()):
  if k.endswith('_json') and isinstance(v,str):after['data'][k]=json.loads(v)
 after['origins']=[{'unit':o.get('unit',o.get('unit_id')),'coverage':o['coverage'],'note':o['note']}
                   for o in after['origins']]
 after['evidence']=[edge(e) for e in after['evidence']]
 source_changes.append({'id':oid,'kind':p['kind'],'expectedVersion':None,**after})
 source_checks.append({'object_id':oid,'absent':True,'typed_data':after['data'],
                       'origins':after['origins'],'evidence':after['evidence']})
assert len(source_changes)==4

byfields=defaultdict(dict);version={};supports={}
for p in person['changes']:
 oid=p['object_id'];field=p['field']
 assert oid not in version or version[oid]==p['expected_revision']
 assert field not in byfields[oid],(oid,field)
 version[oid]=p['expected_revision'];byfields[oid][field]=p
 if oid in supports:assert supports[oid]==p['evidence_supports']
 supports[oid]=p['evidence_supports']
assert len(byfields)==5 and sum(map(len,byfields.values()))==7
person_changes=[];person_checks=[]
for oid,fields in sorted(byfields.items()):
 kind,rev,data,origins,evidence=current(oid)
 assert rev['id']==version[oid],oid
 newdata=copy.deepcopy(data)
 metadata={'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],
           'rationale':rev['rationale'],'caveat':rev['caveat']}
 field_checks=[]
 for field,p in fields.items():
  before=data[field] if field in data else metadata[field]
  assert before==p['before'],(oid,field)
  after=p['after']
  if field in data:newdata[field]=after
  else:metadata[field]=after
  field_checks.append({'field':field,'before':before,'after':after})
 if oid=='P-0007':
  p=fields['sex'];metadata['rationale']=p['revision_rationale_after']
 else:
  assert all('revision_rationale_after' not in p for p in fields.values())
 added=[];oldkeys={ekey(e) for e in evidence}
 newrefs={
  'P-0007':['TR-T0677-C0028-consolidated-control@1','O-T0677-C0028-statistical-fields@1'],
 }.get(oid,['TR-T0677-C0028-consolidated-control@1'])
 assert all(ref in supports[oid] for ref in newrefs),oid
 for ref in newrefs:
  note=('Samma C-0028-post: konsoliderad kolumnkontroll med dokumentärt återbruk och kvarvarande reservationer; ingen extra oberoende källröst.'
    if ref.startswith('TR-') else
    'Egen källobservation binder återbrukad rå 1 till kolumn 5 Lefv. född. kv.; inget namn-/rollantagande.')
  e=ref_edge(ref,'supports',note)
  assert ekey(e) not in oldkeys,oid
  added.append(e)
 newevidence=evidence+added
 person_changes.append({'id':oid,'kind':kind,'expectedVersion':rev['version'],'data':newdata,
   'disposition':metadata['disposition'],'evidenceStatus':metadata['evidenceStatus'],
   'rationale':metadata['rationale'],'caveat':metadata['caveat'],
   'origins':origins,'evidence':newevidence})
 person_checks.append({'object_id':oid,'current_revision':rev['id'],'fields':field_checks,
  'before_evidence':evidence,'added_evidence':added,'after_evidence':newevidence,
  'origins_preserved':True,'metadata_rationale_changed':metadata['rationale']!=rev['rationale']})

adoptions=[]
for a in person['adoption_proposals']:
 oid=a['proposed_id'];assert not rows('SELECT id FROM object WHERE id=?',(oid,))
 body=a['body']
 old='12 dokumentärt återbrukade positiva enheter';new='12 dokumentärt återbrukade hela enheter'
 assert body.count(old)==1,oid
 body=body.replace(old,new)
 if oid=='ADOPT-T0677-C0028-P-0007':
  old='Fadderfältet är blankt;';new='Fadderfältets tidigare dokumenterade blankhet återbrukas;'
  assert body.count(old)==1
  body=body.replace(old,new)
 bases=list(a['basis'])
 if oid=='ADOPT-T0677-C0028-P-0015':
  bases.append('O-P-0015-father-occupation1920@2')
 assert len(bases)==len(set(bases))
 evidence=[]
 for ref in bases:
  if ref=='O-P-0015-father-occupation1920@2':
   note='Individuellt korrigerad egen yrkesobservation, järnvägsarb. skilt från stugnummer.'
  else:note='Samma avgränsade C-0028-post; källa, avskrift, audit och egen kontroll är ingen extra oberoende källröst.'
  evidence.append(ref_edge(ref,'supports',note))
 adoptions.append({'id':oid,'kind':'assessment','expectedVersion':None,
  'data':{'subject_id':a['subject_id'],'criteria':'bounded_source_adoption/1',
          'outcome':'adopted_with_limits','body':body},
  'disposition':'recorded','evidenceStatus':None,
  'rationale':'T-0677 C-0028: avgränsad källadoption utan person-, identitets- eller trädgrindshöjning.',
  'caveat':'','evidence':evidence})
assert len(adoptions)==3

changes=source_changes+person_changes+adoptions
assert len(changes)==12 and len({x['id'] for x in changes})==12
assert sum(x['expectedVersion'] is None for x in changes)==7
byid={x['id']:x for x in changes}
deps={x['id']:{e['object'] for e in x['evidence'] if e['object'] in byid and
      e['version']==(byid[e['object']]['expectedVersion'] or 0)+1} for x in changes}
ordered=[];done=set()
while len(done)<len(changes):
 ready=[oid for oid in byid if oid not in done and deps[oid]<=done]
 assert ready,{'cycle_or_bad_edges':{oid:sorted(v-done) for oid,v in deps.items() if oid not in done}}
 for oid in ready:ordered.append(oid);done.add(oid)
revised={x['id'] for x in changes if x['expectedVersion'] is not None}
stale=[]
for x in changes:
 for e in x['evidence']:
  if e['object'] in revised and e['version']==byid[e['object']]['expectedVersion']:
   stale.append({'target':x['id'],'basis':e['object'],'version':e['version'],'role':e['role']})
assert not stale,stale
ordered_changes=[byid[oid] for oid in ordered]
op={'id':'T-0677/C0028-source-person-adoption-v1',
 'actor':'Codex Sol; root/Astra approved bounded source and person decisions',
 'reason':'T-0677 C-0028: acceptanskriterium 1 och 3, full relevant avgränsad källkontroll med explicit dokumentärt återbruk och individuella person-/forskningsföljder. R@1 bevaras; inga automatiska rebaser eller grindhöjningar.',
 'dependencyReviewVersion':2,'changes':ordered_changes}
OUT.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
full_diff=[]
for x in ordered_changes:
 if x['expectedVersion'] is None:before=None
 else:
  kind,rev,data,origins,evidence=current(x['id'])
  before={'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}
 full_diff.append({'id':x['id'],'action':'create' if before is None else 'revise','before':before,'after':x})
report={'task':'T-0677','state':'COMBINED_PROPOSAL_FOR_ISOLATED_TEMP_NOT_CANONICAL_APPLY',
 'canonical_head':head,'pending':0,
 'inputs':{k:{'path':str(path.relative_to(ROOT)),'sha256':sha(path)} for k,path in FILES.items()},
 'operation_path':str(OUT.relative_to(ROOT)),'operation_sha256':sha(OUT),
 'counts':{'objects':12,'source_creates':4,'person_revisions':5,'person_fields':7,
           'adoption_creates':3,'total_revisions':5,'total_creates':7,
           'stale_old_basis_edges':0},
 'source_checks':source_checks,'person_checks':person_checks,'full_before_after':full_diff,
 'ordered_ids':ordered,'R_retained_current_revision':'R-C0028-15@1',
 'root_amendments_applied':['three adoption body whole-reuse phrases',
   'P0007 adoption witness-blank reuse wording','P0015 adoption O@2 support'],
 'no_canonical_apply':True,'no_review_resolution':True}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'operation_sha256':sha(OUT),'buildcheck_sha256':sha(REPORT),'counts':report['counts']}))
