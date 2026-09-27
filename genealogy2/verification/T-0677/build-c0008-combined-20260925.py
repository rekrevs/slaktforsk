"""Build root-approved C-0008 operation for isolated validation only."""
import copy
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / 'genealogy2/data/research.sqlite'
FILES = {
    'source': HERE / 'c0008-native-source-proposed-v2-20260925.json',
    'person': HERE / 'c0008-person-copy-impact-proposed-20260925.json',
    'addendum': HERE / 'c0008-person-E-EP-evidence-addendum-proposed-20260925.json',
    'source_acceptance': HERE / 'c0008-root-source-proposal-acceptance-20260925.json',
    'final_acceptance': HERE / 'c0008-root-substantive-build-acceptance-20260925.json',
}
EXPECTED = {
    'source': '914f51cde112763290b0d7136bbd0eb7dca24457da3b75f4a63b033a80979fe5',
    'person': '53059b2b911461f412578d534172be9a6a571fea04ef77ec3c0db1ebf0774188',
    'addendum': 'a8b7125fd9695117a1889302b3796c30dbb3a9f5b3ebc49cef65d18a9cc79f5c',
    'source_acceptance': 'da882bba04e379aa8a0f6ebf6fa59d9a56d4b230ec041bb28ad096d28a0427ff',
    'final_acceptance': '0e19ea8b14212e3082f7deebc13d019b343e149e4bab162e965321d50f0e9d37',
}
OUT = HERE / 'c0008-combined-proposed-operation-20260925.json'
REPORT = HERE / 'c0008-combined-buildcheck-20260925.json'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for name,path in FILES.items():
    assert sha(path) == EXPECTED[name], name
source,person,addendum,accept,final_accept = (json.loads(FILES[k].read_text()) for k in FILES)
assert accept['source_proposal_sha256'] == EXPECTED['source']
assert final_accept['state']=='ACCEPTED_FOR_BUILD_AND_ISOLATED_TEMP_ONLY'
assert [x['sha256'] for x in final_accept['inputs']]==[EXPECTED[x] for x in ('source','person','addendum')]
conn = sqlite3.connect(f'file:{DB}?mode=ro',uri=True)
conn.row_factory = sqlite3.Row
def rows(sql,args=()): return [dict(r) for r in conn.execute(sql,args)]
def current(oid):
    ob=rows('SELECT kind FROM object WHERE id=?',(oid,));assert len(ob)==1,oid
    kind=ob[0]['kind']
    rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
    assert len(rev)==1
    rev=rev[0]
    data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],));assert len(data)==1
    data=data[0];data.pop('revision_id')
    for key,val in tuple(data.items()):
        if key.endswith('_json') and val is not None:data[key]=json.loads(val)
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
def edge_key(e): return (e['object'],e['version'],e['role'])
def merge(existing,extra):
    out=copy.deepcopy(existing);seen={edge_key(e) for e in out}
    for raw in extra:
        e=edge(raw)
        if edge_key(e) not in seen:out.append(e);seen.add(edge_key(e))
    return out

head=sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1].name
pending=rows('''SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id
                WHERE rs.request_id IS NULL''')
assert head.startswith('000000186-') and not pending

source_checks=[];prepared_source=[]
for proposed in source['proposed_changes']:
    oid=proposed['id'];kind=proposed['kind'];version=proposed['expectedVersion']
    after=copy.deepcopy(proposed['after'])
    for key,value in tuple(after['data'].items()):
        if key.endswith('_json') and isinstance(value,str):after['data'][key]=json.loads(value)
    after['origins']=[{'unit':x.get('unit',x.get('unit_id')),'coverage':x['coverage'],'note':x['note']}
                      for x in after['origins']]
    after['evidence']=[edge(x) for x in after['evidence']]
    if version is None:
        assert not rows('SELECT id FROM object WHERE id=?',(oid,))
        source_checks.append({'object_id':oid,'action':'create','absent':True,
                              'typed_data_keys':sorted(after['data']),'origin_count':len(after['origins']),
                              'evidence':after['evidence']})
    else:
        oldkind,rev,data,origins,evidence=current(oid)
        assert oldkind==kind and rev['version']==version and set(data)==set(after['data']),oid
        assert sorted(after['origins'],key=lambda x:x['unit'])==origins,oid
        changed=[key for key in data if data[key]!=after['data'][key]]
        source_checks.append({'object_id':oid,'action':'revise','current_revision':rev['id'],
          'changed_typed_fields':changed,'before_evidence':evidence,'proposed_evidence':after['evidence'],
          'origins_preserved':True,'before_caveat':rev['caveat'],'proposed_caveat':after['caveat']})
    prepared_source.append({'id':oid,'kind':kind,'expectedVersion':version,**after})
assert len(prepared_source)==5

patches=defaultdict(dict);versions={};extra=defaultdict(list)
for p in person['changes']:
    oid,field=p['object_id'],p['field']
    assert oid not in versions or versions[oid]==p['current_revision']
    versions[oid]=p['current_revision']
    assert field not in patches[oid],(oid,field)
    p=copy.deepcopy(p)
    if oid=='CONTRACT-P-0003-PK-05' and field=='body':
        old='T-0675 aktuell precisering:'
        new='Aktuell precisering, T-0675 och T-0677:'
        assert p['after'].startswith(old)
        p['after']=new+p['after'][len(old):]
    patches[oid][field]=p
    extra[oid].extend(p['evidence_add'])
assert len(patches)==8 and sum(map(len,patches.values()))==10
add={x['object_id']:x for x in addendum['objects']}
assert set(add)=={'E-baptism-P-0003','EP-E-baptism-P-0003-P-0003-baptized',
                 'EP-E-baptism-P-0003-M-P-0003-C0008-witness1-witness',
                 'EP-E-baptism-P-0003-M-P-0003-C0008-witness2-witness'}
assert set(add)<=set(patches)

person_checks=[];prepared_person=[]
for oid,fields in sorted(patches.items()):
    kind,rev,data,origins,evidence=current(oid)
    assert rev['id']==versions[oid],oid
    newdata=copy.deepcopy(data)
    metadata={'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],
              'rationale':rev['rationale'],'caveat':rev['caveat']}
    for field,p in fields.items():
        before=data[field] if field in data else metadata[field]
        assert before==p['before'],(oid,field)
        if field in data:newdata[field]=p['after']
        else:metadata[field]=p['after']
    proposed_evidence=merge(evidence,extra[oid])
    if oid in add:
        a=add[oid]
        assert a['from_revision']==rev['id'] and a['field']=='caveat'
        assert a['before']==fields['caveat']['before'] and a['after']==fields['caveat']['after']
        assert [edge(x) for x in a['evidence_before']]==evidence,oid
        proposed_evidence=[edge(x) for x in a['evidence_after_proposed']]
        if oid in ('EP-E-baptism-P-0003-M-P-0003-C0008-witness1-witness',
                   'EP-E-baptism-P-0003-M-P-0003-C0008-witness2-witness'):
            mention='M-P-0003-C0008-witness1' if 'witness1' in oid else 'M-P-0003-C0008-witness2'
            removed=[e for e in proposed_evidence if e['object']==mention and e['role']=='supports']
            assert len(removed)==1,oid
            proposed_evidence=[e for e in proposed_evidence if e not in removed]
            assert len([e for e in proposed_evidence if e['object']==mention and e['role']=='derived_from'])==1
        oldkeys={edge_key(x) for x in evidence}
        assert sum(edge_key(e) not in oldkeys for e in proposed_evidence)>=2,oid
    prepared_person.append({'id':oid,'kind':kind,'expectedVersion':rev['version'],
      'data':newdata,'disposition':metadata['disposition'],'evidenceStatus':metadata['evidenceStatus'],
      'rationale':metadata['rationale'],'caveat':metadata['caveat'],
      'origins':origins,'evidence':proposed_evidence})
    person_checks.append({'object_id':oid,'current_revision':rev['id'],'fields':sorted(fields),
      'origins_preserved':True,'before_evidence':evidence,'proposed_evidence':proposed_evidence,
      'explicit_addendum':oid in add})

adoptions=[]
for a in person['bounded_adoptions_proposed']:
    assert not rows('SELECT id FROM object WHERE id=?',(a['object_id'],))
    adoptions.append({'id':a['object_id'],'kind':'assessment','expectedVersion':None,
      'data':{'subject_id':a['subject_id'],'criteria':a['criteria'],
              'outcome':'adopted_with_limits','body':a['body']},
      'disposition':'recorded','evidenceStatus':None,
      'rationale':'T-0677 C-0008: avgränsad källadoption; inga person-, identitets- eller trädgrindar uppgraderas.',
      'caveat':'','evidence':[edge(x) for x in a['evidence']]})
assert len(adoptions)==2

changes=prepared_source+prepared_person+adoptions
assert len(changes)==15 and len({x['id'] for x in changes})==15
assert sum(x['expectedVersion'] is None for x in changes)==5
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
assert ordered.index('R-70eeff109bc651dce649a0ee')<ordered.index('TR-T0677-C0008-consolidated-control')
assert ordered.index('TR-T0677-C0008-consolidated-control')<ordered.index('M-P-0003-C0008-witness1')
assert ordered.index('TR-T0677-C0008-consolidated-control')<ordered.index('AUDIT-T0677-C0008')

ordered_changes=[byid[oid] for oid in ordered]
op={'id':'T-0677/C0008-source-person-adoption-v1',
  'actor':'Codex Sol; root/Astra approved bounded source and person decisions',
  'reason':'T-0677 C-0008: acceptanskriterium 1 och 3, avgränsad full relevant källutvinning med redovisat återbruk och individuella person-/forskningsföljder samt begränsad adoption utan identitets- eller trädgrindshöjning.',
  'dependencyReviewVersion':2,'changes':ordered_changes}
OUT.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
full_diff=[]
for change in ordered_changes:
    oid=change['id']
    if change['expectedVersion'] is None:before=None
    else:
        kind,rev,data,origins,evidence=current(oid)
        before={'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}
    full_diff.append({'id':oid,'action':'create' if before is None else 'revise','before':before,'after':change})
report={'task':'T-0677','state':'COMBINED_PROPOSAL_FOR_ISOLATED_TEMP_NOT_CANONICAL_APPLY',
  'canonical_head':head,'pending':0,'inputs':{key:{'path':str(path.relative_to(ROOT)),'sha256':sha(path)} for key,path in FILES.items()},
  'counts':{'objects':15,'source':5,'person_revision_objects':8,'person_fields':10,'adoptions':2,
            'revisions':10,'creates':5,'explicit_person_evidence_addenda':4,'stale_old_basis_edges':len(stale)},
  'source_checks':source_checks,'person_checks':person_checks,'full_before_after':full_diff,
  'prepared_change_order':ordered,'approved_rebase_targets':['M-P-0003-C0008-witness1',*sorted(add)],
  'adoption_outcome':'adopted_with_limits',
  'root_amendments_applied':['both adoption outcomes','PK05 body prefix','remove two redundant EP-to-own-M supports edges'],
  'operation_path':str(OUT.relative_to(ROOT)),'operation_sha256':sha(OUT),
  'no_canonical_apply':True,'no_review_resolution':True}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'operation_sha256':sha(OUT),'buildcheck_sha256':sha(REPORT),'counts':report['counts']}))
