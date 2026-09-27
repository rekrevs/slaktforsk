"""Read-only current registration and evidence closure for two C-0028 seeds."""
import collections
import hashlib
import json
import sqlite3
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
OUT=HERE/'c0028-dependency-inventory-proposed-j188-20260925.json'
SEEDS=('O-P-0015-father-occupation1920','P-0007')
def sha_bytes(data):return hashlib.sha256(data).hexdigest()
def canonical_hash(value):return sha_bytes(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(x) for x in conn.execute(sql,args)]
def full(rid):
    revs=rows('SELECT * FROM revision WHERE id=?',(rid,));assert len(revs)==1,rid
    rev=revs[0];obj=rows('SELECT kind FROM object WHERE id=?',(rev['object_id'],));assert len(obj)==1
    kind=obj[0]['kind'];data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rid,));assert len(data)==1
    data=data[0];data.pop('revision_id')
    for key,value in tuple(data.items()):
        if key.endswith('_json') and value is not None:data[key]=json.loads(value)
    origins=rows('''SELECT o.revision_id,o.unit_id,o.coverage,o.note,u.document_path,u.start_line,u.end_line,
      d.sha256 document_sha256 FROM origin o JOIN unit u ON u.id=o.unit_id
      JOIN document d ON d.path=u.document_path WHERE o.revision_id=? ORDER BY o.unit_id''',(rid,))
    evidence=rows('SELECT revision_id,basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role',(rid,))
    payload={'object_id':rev['object_id'],'kind':kind,'revision':rev,'typed_data':data,
             'origins':origins,'evidence':evidence}
    payload['current_head_sha256']=canonical_hash(payload)
    return payload

head_file=sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1]
assert head_file.name.startswith('000000188-')
pending=rows('''SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id
  WHERE rs.request_id IS NULL''')
assert not pending
heads={r['id']:r for r in rows('''SELECT r.* FROM revision r JOIN
  (SELECT object_id,max(version) version FROM revision GROUP BY object_id) h
  ON h.object_id=r.object_id AND h.version=r.version''')}
by_object={r['object_id']:r['id'] for r in heads.values()}
assert by_object['O-P-0015-father-occupation1920']=='O-P-0015-father-occupation1920@1'
assert by_object['P-0007']=='P-0007@1'
assert by_object['R-C0028-15']=='R-C0028-15@1'

impact={}
for seed in SEEDS:
    raw=subprocess.check_output(['node','genealogy2/cli.mjs','impact',seed],cwd=ROOT)
    impact[seed]=json.loads(raw)
    assert impact[seed]['database_state']['last_operation']['sequence']==188
    assert len(impact[seed]['seeds'])==1 and impact[seed]['seeds'][0]['revision_id']==by_object[seed]

# CLI impact's import targets are registered routes, but they are not source
# evidence. Text candidates remain separate and are never promoted to a route.
routes=collections.defaultdict(list)
base_revisions=set()
for seed,x in impact.items():
    rid=by_object[seed]
    base_revisions.add(rid)
    routes[rid].append({'from_seed':rid,'route':'explicit_seed','distance':0})
    for target in x['provenance']['targets']:
        if not target['current']:continue
        target_rid=target['revision_id']
        assert target_rid in heads
        base_revisions.add(target_rid)
        routes[target_rid].append({'from_seed':rid,'route':'registered_import_target_not_evidence',
            'distance':0 if target_rid==rid else 1,'unit_id':target['unit_id'],
            'decision_id':target['decision_id'],'decision_state':target['state'],
            'document_path':target['document_path'],'start_line':target['start_line'],
            'end_line':target['end_line']})
    for dep in x['dependencies']['current']:
        target_rid=dep.get('revision_id')
        if target_rid and target_rid in heads:
            base_revisions.add(target_rid)
            routes[target_rid].append({'from_seed':rid,'route':'direct_current_dependency',
                'distance':1,'edge':dep})

reverse=collections.defaultdict(list)
for dep in rows('SELECT revision_id,basis_revision_id,role,note FROM dependency ORDER BY basis_revision_id,revision_id,role'):
    if dep['revision_id'] in heads:
        reverse[dep['basis_revision_id']].append(dep)
visited=set(base_revisions);front=set(base_revisions);transitive=[];distance=1
while front:
    nxt=set()
    for basis in sorted(front):
        for dep in reverse[basis]:
            target=dep['revision_id']
            if target in base_revisions:continue
            if target not in visited:nxt.add(target)
            transitive.append({'basis_revision_id':basis,'affected_revision_id':target,
                               'role':dep['role'],'note':dep['note'],
                               'distance_from_registered_frontier':distance})
    visited|=nxt;front=nxt;distance+=1
assert all(rid in heads for rid in visited)
items=[]
for rid in sorted(visited):
    item=full(rid)
    item['registration_routes']=routes[rid]
    item['transitive_incoming_current_edges']=[x for x in transitive if x['affected_revision_id']==rid]
    items.append(item)

text_candidates={}
for seed,x in impact.items():
    text_candidates[seed]={
      'current':[{'object_id':z['object_id'],'revision_id':z['revision_id'],'kind':z['kind'],
                  'matched_terms':z.get('matched_terms'),'routes':z.get('routes')} for z in x['text_candidates']['current']],
      'historical':[{'object_id':z['object_id'],'revision_id':z['revision_id'],'kind':z['kind'],
                     'matched_terms':z.get('matched_terms'),'routes':z.get('routes')} for z in x['text_candidates']['historical']]}

out={'task':'T-0677','state':'PROPOSED_READ_ONLY_CURRENT_DEPENDENCY_INVENTORY_NO_ASSESSMENT',
     'canonical_head_file':head_file.name,'canonical_head_sha256':sha_bytes(head_file.read_bytes()),
     'canonical_pending':0,'seed_revisions':[by_object[x] for x in SEEDS],
     'R_C0028_current_head_retained':'R-C0028-15@1',
     'P_0007_sex_revision_status':'UNDER_ASTRA_REVIEW_NO_DECISION_IN_THIS_FILE',
     'selection_rule':{
       'registered_frontier':'explicit seeds, current import-provenance targets and direct current dependency routes from CLI impact',
       'transitive_expansion':'reverse dependency edges from registered frontier, current heads only, until fixed point',
       'text_candidates':'reported separately as search matches, never source-support or registration edges',
       'head_hash':'SHA-256 of sorted-key compact JSON of object_id/kind/revision/typed_data/origins/evidence before adding routes',
       'no_automatic_R_revision_or_rebase':True},
     'impact_route_summary':{seed:{'current_dependencies':len(x['dependencies']['current']),
       'historical_dependencies':len(x['dependencies']['historical']),
       'import_origins':len(x['provenance']['origins']),
       'registered_import_target_rows':len(x['provenance']['targets']),
       'current_text_candidate_rows':len(x['text_candidates']['current']),
       'historical_text_candidate_rows':len(x['text_candidates']['historical'])}
       for seed,x in impact.items()},
     'current_registered_target_rows':{seed:[x for x in impact[seed]['provenance']['targets'] if x['current']] for seed in SEEDS},
     'current_dependency_routes':{seed:impact[seed]['dependencies']['current'] for seed in SEEDS},
     'transitive_current_dependency_edges':transitive,
     'items':items,'text_candidates_metadata_only':text_candidates,
     'counts':{'registered_frontier_revisions':len(base_revisions),
       'transitive_additional_revisions':len(visited-base_revisions),
       'current_full_payload_items':len(items),
       'transitive_current_edges':len(transitive),
       'current_text_candidate_rows':sum(len(x['text_candidates']['current']) for x in impact.values())},
     'limits':['No source interpretation, person or sex decision, review disposition, status change or native apply.',
       'Imported unit targets are provenance, not independent evidence.',
       'Text matches are metadata-only candidates and do not enter the registered dependency closure.',
       'R-C0028-15@1 remains the observed current head; no automatic revision or evidence rebase.']}
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(OUT.relative_to(ROOT)),'sha256':sha_bytes(OUT.read_bytes()),'counts':out['counts']},ensure_ascii=False))
