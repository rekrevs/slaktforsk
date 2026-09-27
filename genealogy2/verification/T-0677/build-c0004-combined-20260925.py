"""Build root-approved C-0004 operation for isolated validation only."""
import copy
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
SOURCE=HERE/'c0004-native-source-decisions-proposed-v2-20260924.json'
IMPACT=HERE/'c0004-current-impact-proposed-v4-20260925.json'
ACCEPT=HERE/'c0004-root-substantive-acceptance-20260925.json'
EVIDENCE_DECISION=HERE/'c0004-root-evidence-amendment-20260925.json'
CAPTURE=HERE/'c0004-package-currentheads-pre-v4-20260925.json'
OUT=HERE/'c0004-combined-proposed-operation-20260925.json'
REPORT=HERE/'c0004-combined-buildcheck-20260925.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE)=='6f1331f9a22198857eae7fb5400a6275b8b39c2c28742ec2fa87d0705ac4361f'
assert sha(IMPACT)=='0ab717e42105dd10a8baa98f4577b4be42aee4b229ad64d09e810a2cc44ee33e'
assert sha(ACCEPT)=='a26989689f1ca99423a65472a63473878b3d5edfc0c6862a7f955bff839a3e51'
assert sha(EVIDENCE_DECISION)=='f4728ae6427f2657ea0cb519359d6e7e0554b92c5c10d9b3e3c923193dcfa21e'
source=json.loads(SOURCE.read_text());impact=json.loads(IMPACT.read_text());accept=json.loads(ACCEPT.read_text())
assert len(source['proposed_changes'])==3 and len(impact['bounded_adoptions'])==8
assert len(impact['changes'])==14 and len({x['object_id'] for x in impact['changes']})==11
assert accept['state']=='APPROVED_TO_BUILD_AND_TEMP_VALIDATE_NOT_CANONICAL_APPLY'
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(x) for x in conn.execute(sql,args)]
def current(oid):
    obj=rows('SELECT kind FROM object WHERE id=?',(oid,));assert len(obj)==1,oid
    kind=obj[0]['kind'];rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
    assert len(rev)==1;rev=rev[0]
    data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],));assert len(data)==1
    data=data[0];data.pop('revision_id')
    for key,value in list(data.items()):
        if key.endswith('_json') and value is not None:
            data[key]=json.loads(value)
    origins=[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']}
             for r in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rev['id'],))]
    evidence=[]
    for r in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rev['id'],)):
        basis,version=r['basis_revision_id'].rsplit('@',1)
        evidence.append({'object':basis,'version':int(version),'role':r['role'],'note':r['note']})
    return kind,rev,data,origins,evidence
def edge(raw):
    if 'basis_revision_id' in raw:
        basis,version=raw['basis_revision_id'].rsplit('@',1)
        return {'object':basis,'version':int(version),'role':raw['role'],'note':raw['note']}
    return raw
def add_edges(existing,extra):
    result=copy.deepcopy(existing)
    seen={(e['object'],e['version'],e['role']) for e in result}
    for raw in extra:
        e=edge(raw);key=(e['object'],e['version'],e['role'])
        if key not in seen:result.append(e);seen.add(key)
    return result
changes=[];source_checks=[];field_diff=[]
for proposed in source['proposed_changes']:
    oid=proposed['id'];after=copy.deepcopy(proposed['after']);version=proposed['expectedVersion']
    if oid=='O-P-0001-C0004-household':
        old='dess sakliga bärare granskas separat'
        new='sakuppgiften kvarstår i BIO-P-0001, BIO-P-0028 och de åtta föräldrarelationerna till P-0035–P-0038'
        assert after['caveat'].count(old)==1
        after['caveat']=after['caveat'].replace(old,new)
        assert 'laterFourChildren' not in after['data']['value_json']
    if 'value_json' in after['data'] and isinstance(after['data']['value_json'],str):
        after['data']['value_json']=json.loads(after['data']['value_json'])
    if version is None:
        assert not rows('SELECT id FROM object WHERE id=?',(oid,))
        changes.append({'id':oid,'kind':proposed['kind'],'expectedVersion':None,**after})
        source_checks.append({'id':oid,'absent':True})
    else:
        kind,rev,data,origins,evidence=current(oid)
        assert kind==proposed['kind'] and rev['version']==version
        assert set(data)==set(after['data'])
        assert {(x['unit'],x['coverage'],x['note']) for x in origins}=={
            (x['unit_id'],x['coverage'],x['note']) for x in after['origins']}
        assert {(e['object'],e['version'],e['role']) for e in evidence}.issubset(
            {(e['object'],e['version'],e['role']) for e in after['evidence']})
        changes.append({'id':oid,'kind':kind,'expectedVersion':version,'data':after['data'],
                        'disposition':after['disposition'],'evidenceStatus':after['evidenceStatus'],
                        'rationale':after['rationale'],'caveat':after['caveat'],
                        'origins':origins,'evidence':after['evidence']})
        source_checks.append({'id':oid,'head':rev['id'],'current_data':data,
                              'approved_after_data':after['data'],'current_caveat':rev['caveat'],
                              'approved_after_caveat':after['caveat']})
patches=defaultdict(dict);versions={};extras=defaultdict(list)
for p in impact['changes']:
    oid,field=p['object_id'],p['field']
    assert field not in patches[oid],(oid,field)
    patches[oid][field]=p
    assert oid not in versions or versions[oid]==p['current_revision']
    versions[oid]=p['current_revision']
    extras[oid].extend(p['evidence_add'])
assert len(patches)==11 and sum(map(len,patches.values()))==14
for oid,fields in sorted(patches.items()):
    kind,rev,data,origins,evidence=current(oid)
    assert rev['id']==versions[oid]
    newdata=copy.deepcopy(data);caveat=rev['caveat']
    for field,p in fields.items():
        before=data[field] if field in data else rev[field]
        approved_before=json.loads(p['before']) if field=='value_json' else p['before']
        approved_after=json.loads(p['after']) if field=='value_json' else p['after']
        assert before==approved_before,(oid,field)
        if field in data:newdata[field]=approved_after
        else:
            assert field=='caveat'
            caveat=approved_after
        field_diff.append({'id':oid,'current_revision':rev['id'],'field':field,
                           'before':p['before'],'after':p['after']})
    rationale=rev['rationale']+'\nT-0677: '+' '.join(dict.fromkeys(p['rationale'] for p in fields.values()))
    changes.append({'id':oid,'kind':kind,'expectedVersion':rev['version'],'data':newdata,
                    'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],
                    'rationale':rationale,'caveat':caveat,'origins':origins,
                    'evidence':add_edges(evidence,extras[oid])})
for a in impact['bounded_adoptions']:
    oid=a['object_id'];assert not rows('SELECT id FROM object WHERE id=?',(oid,))
    changes.append({'id':oid,'kind':'assessment','expectedVersion':None,
                    'data':{'subject_id':a['subject_id'],'criteria':'bounded_source_adoption/1',
                            'outcome':'adopted_with_limits','body':a['body']},
                    'disposition':'recorded','evidenceStatus':None,
                    'rationale':'T-0677: C-0004:s avgränsade källadoption, ingen identitets-, trädverkans- eller livsbildsgrind.',
                    'caveat':'','evidence':[edge(e) for e in a['evidence']]})
# Astra-approved same-object rebase: only the unchanged husband-surname
# reservation, now in the revised research object. No other auto-rebase.
rebase_targets={'CONTRACT-P-0030-PK-05','KEY-P-0030-74f8d1ba6394',
                'P-0030/Q-01','P-0030/Q-02'}
rebase_note='Endast oförändrad reservation för makens efternamn i RESEARCH-P-0030@4; ingen ny namnidentifiering eller oberoende källröst.'
for change in changes:
    if change['id'] in rebase_targets:
        hits=[e for e in change['evidence'] if e['object']=='RESEARCH-P-0030-9d76f0343410'
              and e['version']==3 and e['role']=='supports']
        assert len(hits)==1,change['id']
        hits[0]['version']=4;hits[0]['note']=rebase_note
    if change['id']=='O-P-0001-C0574-sibling-birthfields':
        hits=[e for e in change['evidence'] if e['object']=='TR-T0677-C0004-consolidated-control'
              and e['version']==1]
        assert len(hits)==1
        hits[0]['role']='context'
        hits[0]['note']='Separat C0004-årreservation kvalificerar korshänvisningen; C0574:s egna råfält oförändrade, inget C0004-fält införs som observation ur C0574.'
# The same-operation research revision must precede its four dependents.
research=[c for c in changes if c['id']=='RESEARCH-P-0030-9d76f0343410']
assert len(research)==1
changes=[c for c in changes if c not in research]
changes.insert(3,research[0])
assert len(changes)==22 and len({c['id'] for c in changes})==22
assert sum(c['expectedVersion'] is None for c in changes)==10
assert sum(c['expectedVersion'] is not None for c in changes)==12
op={'id':'T-0677/C0004-source-impact-adoptions-v1','actor':'Codex Sol; root/Astra approved source and impact',
    'reason':'T-0677 C-0004: källpostens 104 fysiska celler med exakt återbruk/kontroll, godkänd hushållsgräns och källberoende; 11 individuella följdobjekt och åtta avgränsade källadoptioner. Inga identitets-, trädverkans- eller livsbildsgrindar uppgraderas.',
    'dependencyReviewVersion':2,'changes':changes}
OUT.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
report={'task':'T-0677','state':'PROPOSED_FOR_TEMP_VALIDATION_NOT_CANONICAL_APPLY',
        'operation_path':str(OUT.relative_to(ROOT)),'operation_sha256':sha(OUT),
        'inputs':{str(p.relative_to(ROOT)):sha(p) for p in (SOURCE,IMPACT,ACCEPT,EVIDENCE_DECISION,CAPTURE)},
        'counts':{'objects':22,'creates':10,'revisions':12,'source_changes':3,
                  'impact_objects':11,'impact_fields':14,'bounded_adoptions':8},
        'source_checks':source_checks,'impact_field_diff':field_diff,
        'approved_evidence_amendments':{'research_rebase_targets':sorted(rebase_targets),
            'research_rebase_from':'RESEARCH-P-0030-9d76f0343410@3',
            'research_rebase_to':'RESEARCH-P-0030-9d76f0343410@4',
            'research_rebase_note':rebase_note,
            'C0574_TR_edge_role':'context','other_rebases':0},
        'no_canonical_apply':True,'no_pending_resolution':True}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'operation_sha256':sha(OUT),'buildcheck_sha256':sha(REPORT),
                  'counts':report['counts']}))
