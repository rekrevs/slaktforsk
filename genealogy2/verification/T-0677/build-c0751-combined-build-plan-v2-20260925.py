"""Read-only C-0751 schema and same-operation evidence audit; no operation."""
import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
SOURCE=HERE/'c0751-native-source-decisions-proposed-v3-20260925.json'
MARRIAGE=HERE/'c0751-marriage-copy-followup-proposed-v2-20260925.json'
OTHER=HERE/'c0751-other-current-impact-proposed-v4-20260925.json'
PREFLIGHT=HERE/'c0751-source-dependency-preflight-proposed-20260925.json'
OUT=HERE/'c0751-combined-build-plan-proposed-v2-20260925.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected={SOURCE:'a7d597bfa3a3c8d0c705dd29a4b27973e7b8233aea084242f64c7089399394f0',
          MARRIAGE:'6d44287d28660784505d2ba7e35537e763885fc30b0a86706d3835ca7dddafe9',
          OTHER:'223b8218373fa1b0ca96199a266b192f9d9d88aa68ffdaa86d50a9ae4fb875ce',
          PREFLIGHT:'5617465a20b03efab92107cc37df26140b238f2acf6c917c8939a57ba3ec14d7'}
for p,digest in expected.items():assert sha(p)==digest,p
source=json.loads(SOURCE.read_text());marriage=json.loads(MARRIAGE.read_text())
other=json.loads(OTHER.read_text());preflight=json.loads(PREFLIGHT.read_text())
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(r) for r in conn.execute(sql,args)]
def current(oid):
    obj=rows('SELECT kind FROM object WHERE id=?',(oid,))
    if not obj:return None
    assert len(obj)==1
    kind=obj[0]['kind'];rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
    assert len(rev)==1;rev=rev[0]
    data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],))
    assert len(data)==1;data=data[0];data.pop('revision_id')
    for key,value in list(data.items()):
        if key.endswith('_json') and value is not None:data[key]=json.loads(value)
    origins=[{'unit_id':r['unit_id'],'coverage':r['coverage'],'note':r['note']}
             for r in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rev['id'],))]
    evidence=rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rev['id'],))
    return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}

source_changes=source['proposed_changes']
source_revisions={x['id'] for x in source_changes if x['expectedVersion'] is not None}
source_creates={x['id'] for x in source_changes if x['expectedVersion'] is None}
marriage_fields={(x['object_id'],x['field']):x for x in marriage['changes']}
other_fields={(x['object_id'],x['field']):x for x in other['changes']}
assert len(source_changes)==10 and len(source_revisions)==6 and len(source_creates)==4
assert len(marriage_fields)==19 and len(other_fields)==101
overlap=sorted(set(marriage_fields)&set(other_fields))
assert len(overlap)==7
assert not (source_revisions|source_creates)&{x[0] for x in set(marriage_fields)|set(other_fields)}
overlap_rows=[]
for oid,field in overlap:
    m,o=marriage_fields[(oid,field)],other_fields[(oid,field)]
    overlap_rows.append({'object_id':oid,'field':field,'current_revision':m['current_revision'],
                         'marriage_v2_after_exactly_in_other_v4':o['marriage_v2_after']==m['after'],
                         'other_v4_after_is_composed_field':True})
assert all(r['marriage_v2_after_exactly_in_other_v4'] for r in overlap_rows)

heads={};before_mismatches=[]
for x in source_changes:
    oid=x['id'];cur=current(oid)
    if x['expectedVersion'] is None:assert cur is None,oid
    else:
        assert cur is not None and cur['revision']['version']==x['expectedVersion'],oid
        heads[oid]={'kind':cur['kind'],'revision_id':cur['revision']['id']}
for family,changes in [('marriage_v2',marriage['changes']),('other_v4',other['changes'])]:
    for x in changes:
        oid,field=x['object_id'],x['field'];cur=current(oid)
        assert cur is not None and cur['revision']['id']==x['current_revision'],oid
        heads[oid]={'kind':cur['kind'],'revision_id':cur['revision']['id']}
        raw=rows(f'SELECT {field} FROM {cur["kind"]} WHERE revision_id=?',(cur['revision']['id'],)) if field in cur['data'] else []
        actual=raw[0][field] if raw else cur['revision'][field]
        if actual!=x['before']:
            before_mismatches.append({'family':family,'object_id':oid,'field':field,
                                      'current':actual,'proposal_before':x['before']})
assert not before_mismatches

changed_revisions=source_revisions|{oid for oid,_ in set(marriage_fields)|set(other_fields)}
stale=[]
for target in sorted(changed_revisions):
    target_full=current(target)
    for edge in target_full['evidence']:
        basis_id,version=edge['basis_revision_id'].rsplit('@',1)
        if basis_id not in changed_revisions:continue
        basis_full=current(basis_id)
        assert basis_full is not None and basis_full['revision']['version']==int(version)
        stale.append({'target_id':target,'target_current_revision':target_full['revision']['id'],
                      'basis_id':basis_id,'basis_current_revision':basis_full['revision']['id'],
                      'current_edge':edge,'target_full_current_payload':target_full,
                      'basis_full_current_payload':basis_full,
                      'would_be_stale_if_unchanged':True})
assert len(stale)==2
assert {(x['target_id'],x['basis_id']) for x in stale}=={
    ('O-P-0422-C0751-own','R-4d7b64dfced04156063566c0'),
    ('O-P-0480-Sara-neighbour','R-d2d304a2b1e0b6c0fb88fdeb')}

future_ids=source_creates|{x['object_id'] for x in other['bounded_adoptions_proposed']}|{
    other['new_key_candidate']['object_id']}
assert len(future_ids)==16 and all(current(x) is None for x in future_ids)
proposed_edge_refs=[]
for family,changes in [('source_v3',source_changes),('marriage_v2',marriage['changes']),('other_v4',other['changes'])]:
    for x in changes:
        oid=x.get('id',x.get('object_id'))
        edges=x['after'].get('evidence',[]) if family=='source_v3' else x.get('evidence_add',[])
        for edge in edges:
            if 'basis_revision_id' in edge:basis_ref=edge['basis_revision_id']
            else:basis_ref=edge['object']+'@'+str(edge['version'])
            basis_id,_=basis_ref.rsplit('@',1)
            if basis_id in changed_revisions:
                proposed_edge_refs.append({'family':family,'target_id':oid,'basis_ref':basis_ref,
                                           'role':edge['role'],'note':edge['note']})
proposed_old=[x for x in proposed_edge_refs if x['basis_ref'].rsplit('@',1)[0] in changed_revisions
              and x['basis_ref']==current(x['basis_ref'].rsplit('@',1)[0])['revision']['id']]
assert len(proposed_old)==2
assert {(x['target_id'],x['basis_ref']) for x in proposed_old}=={
    ('BIO-P-0481','F-P-0481-source_interpretation-individual-limits@1'),
    ('RESEARCH-P-0481-9d76f0343410','F-P-0481-source_interpretation-individual-limits@1')}
def proposed_fields(oid):
    fields=[]
    for x in source_changes:
        if x['id']==oid and x['expectedVersion'] is not None:
            fields.append({'family':'source_v3','field':'full revision after',
                           'current_full':current(oid),'proposed_after':x['after']})
    for family,changes in [('marriage_v2',marriage['changes']),('other_v4',other['changes'])]:
        for x in changes:
            if x['object_id']==oid:
                fields.append({'family':family,'field':x['field'],'before':x['before'],
                               'marriage_v2_after':x.get('marriage_v2_after'),
                               'after':x['after']})
    return fields
proposed_stale=[]
for x in proposed_old:
    basis_id=x['basis_ref'].rsplit('@',1)[0]
    proposed_stale.append({**x,'target_full_current_payload':current(x['target_id']),
                           'basis_full_current_payload':current(basis_id),
                           'target_relevant_proposed_fields':proposed_fields(x['target_id']),
                           'basis_relevant_proposed_fields':proposed_fields(basis_id),
                           'would_be_stale_if_added_at_old_version':True})
for x in stale:
    x['target_relevant_proposed_fields']=proposed_fields(x['target_id'])
    x['basis_relevant_proposed_fields']=proposed_fields(x['basis_id'])

pending_preflight={'path':str(PREFLIGHT.relative_to(ROOT)),'sha256':sha(PREFLIGHT),
                   'direct_current_dependents_reviewed':len(preflight['reviews']),
                   'candidate_retains_not_resolved':preflight['counts']['retain_candidate'],
                   'revisions_already_in_source_proposal':preflight['counts']['revision_in_source_proposal']}
plan={'task':'T-0677','state':'READ_ONLY_BUILD_PLAN_V2_FOR_ASTRA_EVIDENCE_DECISION_NO_OPERATION',
      'canonical_journal_head':184,'canonical_pending_at_capture':0,
      'inputs':{str(p.relative_to(ROOT)):sha(p) for p in expected},
      'provisional_counts':{'source_objects':10,'source_revisions':6,'source_creates':4,
                            'marriage_v2_objects':19,'marriage_v2_fields':19,
                            'other_v4_objects':101,'other_v4_fields':101,
                            'other_v4_marriage_format_only_fields':len(other['marriage_only_format_delta']),
                            'same_field_overlaps':7,'combined_existing_revision_objects':len(changed_revisions),
                            'provisional_new_objects_including_11_adoptions_and_key':16,
                            'provisional_total_objects':len(changed_revisions|future_ids)},
      'same_field_merge_rows':overlap_rows,'current_heads_for_provisional_revisions':heads,
      'proposal_before_mismatches':before_mismatches,
      'same_operation_stale_current_edges_if_left_unchanged':stale,
      'stale_edge_count':len(stale),
      'source_v3_explicit_rebase_proposals':source['explicit_evidence_rebases'],
      'proposed_intra_operation_edges_to_changed_basis':proposed_edge_refs,
      'proposed_edges_still_using_changed_basis_old_head':proposed_stale,
      'total_same_operation_stale_edge_pairs_for_Astra':len(stale)+len(proposed_stale),
      'source_direct_dependent_preflight':pending_preflight,
      'schema_plan':{'operation_dependencyReviewVersion':2,
                     'revision_change_fields':['id','kind','expectedVersion','data','disposition','evidenceStatus','rationale','caveat','origins','evidence'],
                     'create_expectedVersion':None,
                     'same_field_merge':'other_v4.after is already composed with marriage_v2.after at seven overlaps; do not apply both sequentially',
                     'order':'three R revisions before two source O revisions and new TR/AUDIT/M/O; all same-operation edges must point to final versions; then merged person/research revisions and proposed adoptions/key',
                     'origins_and_media':'Preserve current origins/evidence on revisions and existing media bindings on R; no duplicate media',
                     'pending':'Only actual pending after isolated temp apply may be individually dispositioned; no prospective blanket retain'},
      'guards':['Other current-impact v4 is an input for this plan; no combined operation is approved or built.',
                'No evidence rebase is authorized by this mechanical plan. Source v3 proposes two exact R@2 edges, but Astra/root decides final combined evidence.',
                'No native operation, temp apply, canonical apply, or review resolution was produced.'],
      'no_operation_built':True,'no_temp_apply':True,'no_canonical_apply':True}
OUT.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(OUT),'sha256':sha(OUT),'counts':plan['provisional_counts'],
                  'stale_current_edges':len(stale),'stale_proposed_additions':len(proposed_stale),
                  'before_mismatches':len(before_mismatches)}))
