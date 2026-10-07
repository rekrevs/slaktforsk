import json,hashlib,copy
from pathlib import Path
D=Path(__file__).parent;P=D.parent/'preparation';A=P/'materialized-source-v3-literal-v1'
v=json.loads((D/'settled-90-dispositions-and-literal-field-decisions-v3.json').read_text());n=json.loads((P/'complete-current-history-support-native.json').read_text())['objects'];o=json.loads((A/'operation-literal.json').read_text());t=json.loads((A/'individual-consequence-table.json').read_text())
def api(x):
 data={k:json.loads(z) if k.endswith('_json') and isinstance(z,str) else z for k,z in x['data'].items() if k!='revision_id'}
 return dict(id=x['object_id'],kind=x['kind'],expectedVersion=x['version'],data=data,origins=[dict(unit=z['unit_id'],coverage=z['coverage'],note=z['note']) for z in x['origins']],evidence=[dict(object=z['basis_revision_id'].rsplit('@',1)[0],version=int(z['basis_revision_id'].rsplit('@',1)[1]),role=z['role'],note=z['note']) for z in x['evidence']],disposition=x['disposition'],evidenceStatus=x['evidence_status'],rationale=x['rationale'],caveat=x['caveat'])
expected=[]
for c in v['exact_changes']:
 old=n[c['target_revision']];x=api(old)
 for f in c['field_changes']:
  assert old['data'][f['field']]==f['old'];x['data'][f['field']]=json.loads(f['new']) if f['field'].endswith('_json') and isinstance(f['new'],str) else f['new']
 x['evidence']=c['literal_api_evidence'];x['caveat']=(old['caveat']+'\n\n' if old['caveat'] else '')+c['amendment_caveat'];expected.append(x)
expected+=v['six_life_reviews'];assert o['changes']==expected
assert len(o['changes'])==40
for i,r in enumerate(t['changes']):
 assert r['new_api']==expected[i]
 if i<34:
  c=v['exact_changes'][i];assert r['old_native']==n[c['target_revision']];assert r['old_full_api']==api(n[c['target_revision']]);assert r['individual_evidence_decisions']==c['individual_evidence_decisions']
for r in t['retains']:assert r['old_native']==n[r['revision_id']]
assert t['all90_individual_dispositions']==v['individual_table'];assert len(t['retains'])==72
assert {r['revision_id'] for r in t['retains']}=={r['object_id']+'@'+str(r['old_version']) for r in v['individual_table'] if r['disposition']=='retain'}
assert t['followup']==v['bounded_followup']
head={}
for x in n.values():head[x['object_id']]=max(head.get(x['object_id'],0),x['version'])
for x in expected:
 assert head.get(x['id'])==x['expectedVersion']
 for e in x['evidence']:assert head[e['object']]==e['version']
 head[x['id']]=(head.get(x['id']) or 0)+1
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert h(A/'operation-literal.json')=='211f0922680418c50f70f2443ef08d601ab06c0f242ffeb70ce4091538b019d5'
assert h(A/'individual-consequence-table.json')=='3ec724d31e694f454e4c7dbc2dd8792fe17dfade30a45db4c6720439f12336bb'
gate=dict(task='T-0790',role='primary source/evidence',ready_for_stage=True,operation_sha256=h(A/'operation-literal.json'),consequence_sha256=h(A/'individual-consequence-table.json'),source_spec_sha256=h(D/'settled-90-dispositions-and-literal-field-decisions-v3.json'),review='Full literal40 APIs independently reconstructed from approved fields/current native and compared for exact equality, including data JSON typing, existing rationale/disposition/evidenceStatus, ordered origins/evidence and exact caveat append. All72 retained full natives equal current pinned records, all90 dispositions equal settled source decisions. Every sequential basis current at its mutation.',substantive_basis=['The full operation preserves existing identity/tree and OWNER knowledge; no person/relation/fact/event identity mutations occur. The only source observation change is unresolved column9 tested-status, without resolving raw glyphs or creating an event.','Thirty-four narrow corrections consolidate stronger maternal/dop/1964 evidence, remove unsupported Stockholm/chronology/absolute-baptism/catalog conclusions, and distinguish historical full-contract outcomes from native life outcomes.','PK06 is individual thematic assessment, not exhaustion: Gunnar STYRKT PK06 remains failed life via03/04/08. Evy passes only her person-bound minimized scope; four named living-person K09 passages still keep their life outcomes failed.','Every new review has explicit full field scope/reasons and literal evidence versions; no available-but-stale support binds, no self evidence inferred from table receipt references.','T0795 is already registered metadata-only sixunits/twelve total, including two total forU6; T0359/T0362 scopes preserved. No future source execution is included.'],counts=dict(existing_changes=34,new_life_reviews=6,individual_retains=72,individual_dispositions=90),life_outcomes={x['data']['subject_id']:x['data']['outcome'] for x in v['six_life_reviews']},limits='Approves exactly this package for baseline-clone staging only. Not canonical apply approval, dependency outcome approval, completed source access, or task DONE. Actual staged dependency effects and full poststage context require separate source/independent final gates.',new_source_access=0,canonical_or_stage_actions_performed=False)
q=D/'materialized-v1-prestage-source-gate.json';q.write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n');print(h(q))
