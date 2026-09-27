"""Assemble approved C-0002 proposals for isolated review; never apply canonical."""
import copy
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / 'genealogy2/data/research.sqlite'
SOURCE = HERE / 'c0002-native-source-decisions-proposed-20260924.json'
COPY = HERE / 'c0002-copy-build-input-rootapproved-20260924.json'
WITNESS = HERE / 'c0002-witness-followup-decisions-proposed-20260924.json'
ROOT_ACCEPT = HERE / 'c0002-root-source-followup-acceptance-20260924.json'
COPY_ACCEPT = HERE / 'c0002-root-substantive-acceptance-20260924.json'
OUT = HERE / 'c0002-combined-preliminary-operation-20260924.json'
REPORT = HERE / 'c0002-combined-preliminary-buildcheck-20260924.json'
EXPECTED = {
    SOURCE: '77e74f7e57c39c85ffd82d57aa298f7d872798d2a06aa0347d040f5296f1fde9',
    COPY: 'f9479ca8092f0d1d79064ea808ee87186102e2ea8cd8a01d6c0ea5341f0e74b4',
    WITNESS: 'f0821677feea1665f960884bed8ef444e607200e4da084c930dfbb33284a1c12',
    ROOT_ACCEPT: '59113238ebd421da62add055589c6ce996a2cb9a4d95bd485c3df6a0d72fa965',
    COPY_ACCEPT: 'bc60e39a02557b547d6656d8dcbb5a2222b6d8c72e7d39f5ceacdbda1a17e2d7',
}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
for path, digest in EXPECTED.items(): assert sha(path) == digest, path
source = json.loads(SOURCE.read_text())
copy_input = json.loads(COPY.read_text())
witness = json.loads(WITNESS.read_text())
assert len(source['proposed_changes']) == 27 and len(source['fieldcoverage']) == 21
assert len(copy_input['changes']) == 19 and len({x['object_id'] for x in copy_input['changes']}) == 16
assert len(witness['changes']) == 50 and len({x['object_id'] for x in witness['changes']}) == 46
assert set(x['id'] for x in source['proposed_changes']).isdisjoint({x['object_id'] for x in copy_input['changes'] + witness['changes']})
assert {x['object_id'] for x in copy_input['changes']} & {x['object_id'] for x in witness['changes']} == {'BIO-P-0001','KEY-P-0001-ee8eaa9a6746','PATH-P-0001-KP-05'}
assert {(x['object_id'],x['field']) for x in copy_input['changes']} & {(x['object_id'],x['field']) for x in witness['changes']} == {('BIO-P-0001','caveat')}
conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
conn.row_factory = sqlite3.Row

def one(sql, params=()):
    row=conn.execute(sql,params).fetchone()
    assert row is not None, (sql,params)
    return dict(row)
def rows(sql,params=()): return [dict(x) for x in conn.execute(sql,params)]
def current(oid):
    kind=one('SELECT kind FROM object WHERE id=?',(oid,))['kind']
    rev=one('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
    data=one(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],));data.pop('revision_id')
    if 'value_json' in data and data['value_json'] is not None: data['value_json']=json.loads(data['value_json'])
    origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rev['id'],))]
    evidence=[]
    for x in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rev['id'],)):
        obj,version=x['basis_revision_id'].rsplit('@',1)
        evidence.append({'object':obj,'version':int(version),'role':x['role'],'note':x['note']})
    return kind,rev,data,origins,evidence

def add_evidence(items, extra):
    result=copy.deepcopy(items)
    seen={(x['object'],x['version'],x['role']) for x in result}
    for x in extra:
        key=(x['object'],x['version'],x['role'])
        if key not in seen: result.append(copy.deepcopy(x));seen.add(key)
    return result

# Bind every documentary reuse reference at the exact current version and column.
refs=defaultdict(list)
for field in source['fieldcoverage']:
    for ref in field['exact_reuse_refs']:
        refs[ref].append(field['column'])
assert len(refs)==16
tr_evidence=[]
for ref,cols in sorted(refs.items()):
    oid,version=ref.rsplit('@',1)
    kind,rev,_,_,_=current(oid)
    assert rev['id']==ref, (ref,rev['id'])
    if oid=='TR-d53dad7fd2161f53b6aab1c4':
        assert cols==[2,3,10,16]
        note='Dokumentärt återbruk kol. 2, 3 och 16 samt kol. 10 endast moderns råform 67 15/12. Ej stöd för faderns återtagna 25/5 eller hänvisningens återtagna 263.3.'
    elif oid=='R-510e9de3e16243afcce92e2e':
        assert cols==[1]
        note='Samma avgränsade källpost: ny rubrik-/postgränskontroll samt kol. 1, 10 fader, 11–15, 19, 21; övriga sakvärden återbrukas enligt separata versionsbindningar. Ingen extra oberoende källröst.'
    else:
        note='Dokumentärt återbruk i kol. '+', '.join(map(str,cols))+'. Exakt samma C-0002-källröst; ingen ny oberoende källa.'
    tr_evidence.append({'object':oid,'version':int(version),'role':'supports','note':note})
assert any(x['object']=='R-510e9de3e16243afcce92e2e' for x in tr_evidence)

source_changes=[]
source_checks=[]
for original in source['proposed_changes']:
    c=copy.deepcopy(original);oid=c['id'];after=c['after']
    if oid=='TR-T0677-C0002-consolidated-control': after['evidence']=tr_evidence
    if oid.startswith('M-P-0001-C0002-witness'):
        old='Fadderkolumnen är kontext, inte identitetsbelägg.'
        assert after['caveat'].count(old)==1
        after['caveat']=after['caveat'].replace(old,'Ingen ny personidentifikation görs från fadderkolumnen i denna granskning.')
    if oid=='AUDIT-T0677-C0002':
        old='Root v4-copyimpact hanteras separat.'
        assert after['data']['body'].count(old)==1
        after['data']['body']=after['data']['body'].replace(old,'Kopierättelserna ingår i samma versionsbundna operation enligt c0002-copy-build-input-rootapproved-20260924.json (SHA-256 f9479ca8092f0d1d79064ea808ee87186102e2ea8cd8a01d6c0ea5341f0e74b4) och c0002-root-substantive-acceptance-20260924.json (SHA-256 bc60e39a02557b547d6656d8dcbb5a2222b6d8c72e7d39f5ceacdbda1a17e2d7).')
    if oid=='ADOPT-T0677-C0002-P-0028':
        old='Aktuella kopior rättas enligt root v4.'
        assert after['data']['body'].count(old)==1
        after['data']['body']=after['data']['body'].replace(old,'Aktuella kopior rättas enligt rootgodkänt copy-v5 och dess två PATH-preciseringar, SHA-256 f9479ca8092f0d1d79064ea808ee87186102e2ea8cd8a01d6c0ea5341f0e74b4; rootacceptans SHA-256 bc60e39a02557b547d6656d8dcbb5a2222b6d8c72e7d39f5ceacdbda1a17e2d7.')
    if oid=='O-T0677-C0002-mother-marital-column':
        assert after['data']['mention_id']=='M-P-0001-C0002-mother'
        assert current('M-P-0001-C0002-mother')[1]['id']=='M-P-0001-C0002-mother@1'
        after['evidence'].append({'object':'M-P-0001-C0002-mother','version':1,'role':'derived_from','note':'Versionsbunden strukturreferens för moderns eget omnämnande i samma C-0002-post.'})
    if c['expectedVersion'] is None:
        assert conn.execute('SELECT 1 FROM object WHERE id=?',(oid,)).fetchone() is None,oid
        operation_change={'id':oid,'kind':c['kind'],'expectedVersion':None,**after}
        source_checks.append({'id':oid,'create_absent':True})
    else:
        kind,rev,data,origins,evidence=current(oid)
        assert kind==c['kind'] and rev['version']==c['expectedVersion'],oid
        assert set(data)==set(after['data']), (oid,set(data)^set(after['data']))
        operation_change={'id':oid,'kind':kind,'expectedVersion':rev['version'],'data':after['data'],'disposition':after['disposition'],'evidenceStatus':after['evidenceStatus'],'rationale':after['rationale'],'caveat':after['caveat'],'origins':origins,'evidence':copy.deepcopy(after.get('evidence',[]))}
        source_checks.append({'id':oid,'head':rev['id'],'kind':kind,'data_fields_preserved':sorted(data)})
    source_changes.append(operation_change)

patches=defaultdict(dict)
versions={}
for c in copy_input['changes']:
    oid,field=c['object_id'],c['field']
    assert field not in patches[oid],(oid,field)
    patches[oid][field]={'before':c['before'],'after':c['after'],'origin':'copy_v5','rationale':c['rationale']}
    assert oid not in versions or versions[oid]==c['current_revision']
    versions[oid]=c['current_revision']
for w in witness['changes']:
    oid,field=w['object_id'],w['field']
    assert oid not in versions or versions[oid]==w['current_revision']
    versions[oid]=w['current_revision']
    if field in patches[oid]:
        assert (oid,field)==('BIO-P-0001','caveat')
        assert patches[oid][field]['before']==w['current_before']
        assert patches[oid][field]['after']==w['copy_v5_after']
        patches[oid][field]['after']=w['after']
        patches[oid][field]['origin']='merged_copy_plus_witness'
        patches[oid][field]['rationale']+=' '+w['rationale']
    else:
        patches[oid][field]={'before':w['current_before'],'after':w['after'],'origin':'witness_followup','rationale':w['rationale']}
assert len(patches)==59 and sum(len(x) for x in patches.values())==68

witness_evidence=defaultdict(list)
for w in witness['changes']:
    witness_evidence[w['object_id']].extend(w.get('evidence_add',[]))
copy_evidence=[{'object':'R-510e9de3e16243afcce92e2e','version':1,'role':'supports','note':'C-0002:s egen avgränsade post; samma källröst, ingen ny originalkälla.'},{'object':'TR-T0677-C0002-consolidated-control','version':1,'role':'supports','note':'C-0002:s nya versionsbundna transkription och reservationer; ingen extra oberoende röst.'}]
followup_changes=[]
diff=[]
for oid,fields in sorted(patches.items()):
    kind,rev,data,origins,evidence=current(oid)
    assert rev['id']==versions[oid],(oid,rev['id'],versions[oid])
    newdata=copy.deepcopy(data)
    metadata={'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],'rationale':rev['rationale'],'caveat':rev['caveat']}
    for field,p in fields.items():
        original=data[field] if field in data else metadata[field]
        if field=='value_json':
            raw=one(f'SELECT value_json FROM {kind} WHERE revision_id=?',(rev['id'],))['value_json']
            assert raw==p['before'],(oid,field,'raw JSON before')
            proposed_before=json.loads(p['before']) if isinstance(p['before'],str) else p['before']
            proposed_after=json.loads(p['after']) if isinstance(p['after'],str) else p['after']
        else:
            proposed_before,proposed_after=p['before'],p['after']
        assert original==proposed_before,(oid,field)
        if field in data:newdata[field]=proposed_after
        else:metadata[field]=proposed_after
        diff.append({'object_id':oid,'current_revision':rev['id'],'field':field,'before':p['before'],'after':p['after'],'origin':p['origin']})
    rationales=list(dict.fromkeys(p['rationale'] for p in fields.values()))
    metadata['rationale']=(rev['rationale']+'\nT-0677: '+' '.join(rationales)).strip()
    extra=[]
    if oid in {x['object_id'] for x in copy_input['changes']}: extra.extend(copy_evidence)
    extra.extend(witness_evidence[oid])
    operation_change={'id':oid,'kind':kind,'expectedVersion':rev['version'],'data':newdata,'disposition':metadata['disposition'],'evidenceStatus':metadata['evidenceStatus'],'rationale':metadata['rationale'],'caveat':metadata['caveat'],'origins':origins,'evidence':add_evidence(evidence,extra)}
    followup_changes.append(operation_change)

changes=source_changes+followup_changes
# Existing residence-chain evidence points to historical versions of the same
# two household records; the new revision must use their current T-0675/0676 heads.
residence=next(c for c in changes if c['id']=='F-P-0028-residence-documented_chain')
rebase_notes={
    'R-67f44133b117de7897502fa2':'Samma källa i aktuell @2: Johans Rosinedahl fol. 1064, endast bokperioden 1910–1917; inte barns yrke/datum/klammer eller ny vigsel. Bokperiod är inte obruten faktisk bosättning. Ingen extra oberoende röst.',
    'R-ac9bd9bbd4cf62fd811703f3':'Samma källa i aktuell @2: Johans egen Ytterhiske fol. 1839 och territoriell kyrkobokföring från 1925 till dödshållpunkten 1935; inte Brage 2 på barnets rad 13 eller ägande. Bokperiod är inte obruten faktisk bosättning. Ingen extra oberoende röst.',
}
for basis,note in rebase_notes.items():
    assert current(basis)[1]['version']==2
    hits=[e for e in residence['evidence'] if e['object']==basis and e['version']==1 and e['role']=='supports']
    assert len(hits)==1
    hits[0]['version']=2
    hits[0]['note']=note
# EP witness links remain person_id NULL but must follow the new current M revisions.
for change in changes:
    if change['id'] in ('EP-E-baptism-P-0001-M-P-0001-C0002-witness2-witness','EP-E-baptism-P-0001-M-P-0001-C0002-witness4-witness'):
        assert change['data']['person_id'] is None
        target=change['data']['mention_id']
        assert target in ('M-P-0001-C0002-witness2','M-P-0001-C0002-witness4')
        old=[e for e in change['evidence'] if e['object']==target and e['version']==1 and e['role']=='derived_from']
        assert len(old)==1
        old[0]['version']=2
        old[0]['note']='Versionsbunden strukturreferens: samma dopvittnesomnämnande i ny råformsrevision; ingen personidentifikation.'
assert len(changes)==86 and len({x['id'] for x in changes})==86
assert sum(x['expectedVersion'] is None for x in changes)==7
assert sum(x['expectedVersion'] is not None for x in changes)==79
assert len(diff)==68
operation={'id':'T-0677/C0002-source-copy-witness-v1','actor':'Codex Sol; root/Astra decisions','reason':'T-0677 AK1: C-0002:s egen post med 21 kolumners fulla relevanta utvinning, exakt dokumentärt återbruk och riktad oberoende kontroll. AK3: sakrättelser och vittnesreservationer prövade individuellt i källa, tre personers avgränsade adoption och berörda kopior/forskningsobjekt. Historisk råavskrift och ägaruppgifter bevaras; samma original ger ingen extra oberoende röst.','dependencyReviewVersion':2,'changes':changes}
OUT.write_text(json.dumps(operation,ensure_ascii=False,indent=2)+'\n')
report={'task':'T-0677','state':'PRELIMINARY_FOR_ROOT_DIFF_REVIEW_NOT_CANONICAL_APPLY','operation_path':str(OUT.relative_to(ROOT)),'operation_sha256':sha(OUT),'inputs':{str(p.relative_to(ROOT)):sha(p) for p in EXPECTED},'counts':{'operation_changes':86,'creates':7,'revisions':79,'source_proposal_changes':27,'copy_objects':16,'copy_fields':19,'witness_objects':46,'witness_fields':50,'followup_union_objects':59,'followup_unique_changed_fields':68,'same_field_merge':[{'object_id':'BIO-P-0001','field':'caveat'}],'source_copy_witness_object_overlap':0},'source_amendments':{'witness_M_caveats':10,'TR_reuse_ref_evidence':len(tr_evidence),'historical_TR_reuse':'columns 2,3,16 and column 10 mother 67 15/12 only; no 25/5 or 263.3','audit_and_adoption_copy_reference':'root-approved copy-v5 build input and root acceptance','R_510e9d_revision':'retained @1'},'approved_evidence_rebases':[{'object_id':'F-P-0028-residence-documented_chain','before_basis':basis+'@1','after_basis':basis+'@2','role':'supports','after_note':note,'scope':'Root/Astra-approved exact same-record current revision; historical edge stays in @1 fact revision.'} for basis,note in rebase_notes.items()],'static_source_checks':source_checks,'static_followup_diff':diff,'no_temp_apply_yet':True,'no_canonical_apply':True}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'operation':str(OUT),'sha256':sha(OUT),'report':str(REPORT),'report_sha256':sha(REPORT),'counts':report['counts']},ensure_ascii=False))
