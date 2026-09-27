#!/usr/bin/env python3
"""Regenerate a read-only T-0676 crosscheck from the fixed scope and current native DB.

This does not decide citation adequacy or edit canonical state/Wotan.
"""
import copy
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'genealogy2/verification/T-0676'
SCOPE = BASE / 'scope.json'
parser = argparse.ArgumentParser()
parser.add_argument('--output', default=str(BASE / 'manifest-crosscheck-final-proposed-20260924.json'),
                    help='Choose a new output path for a later journal; do not overwrite reviewed snapshots.')
OUT = Path(parser.parse_args().output)
if not OUT.is_absolute():
    OUT = ROOT / OUT
EXPECTED_SCOPE_SHA = 'bb2a5858ee4b7fd79f3c361a7749f9522554a4cb6fa36124160595f3707f3214'

def read_json(path):
    return json.loads(path.read_text())

def one(conn, sql, args=()):
    return conn.execute(sql, args).fetchone()

def current(conn, oid):
    return one(conn, 'SELECT id,version,operation_id FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1', (oid,))

assert hashlib.sha256(SCOPE.read_bytes()).hexdigest() == EXPECTED_SCOPE_SHA
scope = read_json(SCOPE)
assert len(scope['records']) == 50 and len(scope['members']['citations']) == 13 and len(scope['members']['imported_assets']) == 11 and len(scope['cross_references']) == 24
baseline = read_json(BASE / 'manifest-crosscheck-preparation-20260924.json')
crosswalk = read_json(BASE / 'citation-scope-crosswalk-20260924.json')
routing = read_json(BASE / 'three-citation-outside-record-routing-20260924.json')
assessment_path = BASE / 'final-assessment-proposed-20260924.json'
assessment_sha = '685d4e7279356cfe2457d4ac19bad6d975556f33337f137e5d1e292f4405780d'
assert hashlib.sha256(assessment_path.read_bytes()).hexdigest() == assessment_sha
assessment = read_json(assessment_path)
backlog = read_json(ROOT / 'wotan/backlog.json')
ownership = read_json(ROOT / 'genealogy2/verification/T-0673/ownership.json')['cohort_tasks']
tasks = {t['id']:t for t in backlog['tasks']}
conn = sqlite3.connect(ROOT / 'genealogy2/data/research.sqlite')
conn.row_factory = sqlite3.Row
journal = {}
for p in sorted((ROOT / 'genealogy2/journal').glob('*.json')):
    name = p.name
    try: n = int(name.split('-',1)[0])
    except ValueError: continue
    if n >= 157:
        d = read_json(p)
        assert d['sequence'] == n
        journal[d['request']['id']] = {'sequence':n,'path':str(p.relative_to(ROOT)),
                                     'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                                     'request_hash':d['requestHash']}
latest = max(v['sequence'] for v in journal.values())

def revref(row):
    op = row['operation_id']
    return {'revision':row['id'],'operation':op,'journal_sequence':journal.get(op,{}).get('sequence')}

records=[]
for base in baseline['records']:
    x=copy.deepcopy(base)
    rid=x['record_id']
    r=current(conn,rid)
    assert r, rid
    x['record_head']=r['id']; x['record_operation']=r['operation_id']
    x['record_journal_sequence']=journal.get(r['operation_id'],{}).get('sequence',x['record_journal_sequence'])
    tr=conn.execute('''SELECT v.id,v.operation_id FROM transcription t JOIN revision v ON v.id=t.revision_id
      WHERE t.record_id=? AND v.version=(SELECT MAX(version) FROM revision WHERE object_id=v.object_id)
      ORDER BY v.id''',(rid,)).fetchall()
    aud=conn.execute('''SELECT v.id,v.operation_id,a.outcome FROM assessment a JOIN revision v ON v.id=a.revision_id
      WHERE a.subject_id=? AND a.criteria='source_record_review/1'
      AND v.version=(SELECT MAX(version) FROM revision WHERE object_id=v.object_id) ORDER BY v.id''',(rid,)).fetchall()
    x['transcriptions']=[revref(y) for y in tr]
    x['source_reviews']=[dict(revref(y),outcome=y['outcome']) for y in aud]
    x['evidence_state']='evidence_found' if aud else 'support_remains'
    x['canonical_review_status']='review_present' if aud else 'pending_native_review'
    x['citation_scope_warning']='record_review_does_not_complete_whole_citation'
    records.append(x)
assert [x['record_id'] for x in records]==[x['record'] for x in scope['records']]
reviewed=[x['ordinal'] for x in records if x['source_reviews']]
pending=[x['ordinal'] for x in records if not x['source_reviews']]
if latest == 178:
    assert len(reviewed)==43 and pending==[5,6,21,30,33,41,46],(len(reviewed),pending)
if latest >= 180:
    assert len(reviewed)==50 and not pending,(len(reviewed),pending)
assert all(records[i-1]['source_reviews'] for i in [4,12,28,47,15,17])

citations=[]
assessment_citations={x['citation']:x for x in assessment['citation_dispositions']}
for c in crosswalk['citations']:
    x=copy.deepcopy(c)
    cid=x['citation']
    x['T0676_record_reviews_present']=[i for i in x['G024RecordNumbers'] if i in reviewed]
    x['T0676_record_reviews_pending']=[i for i in x['G024RecordNumbers'] if i in pending]
    x['Astra_j178_conditional_disposition_historical']=assessment_citations[cid]
    x['whole_citation_status']='Astra_proposed_conditional_not_final'
    if latest >= 180:
        x['actual_journal_scope_state']='own_G024_records_reviewed' if not x['T0676_record_reviews_pending'] else 'own_G024_records_pending'
        x['actual_citation_disposition']=assessment_citations[cid]['disposition']
        if cid=='C-0916':
            x['actual_citation_disposition']='OWN_BOUNDED_RECORDS_REVIEWED'
        if cid=='C-0981':
            x['actual_citation_disposition']='PARTIAL_SPLIT_WITH_OWN_FOL1839_CELL_REVIEWED'
        x['whole_citation_status']='actual_own_scope_reviewed_with_exact_external_partials_retained'
    if cid=='C-0907': x['other_scope_owner']='T-0770 BLOCKED after T-0676: 49 historic zero-folio units'
    if cid=='C-0923': x['other_scope_owner']='T-0724 READY/G051: SEARCH-P-0009-SvenskaGravar-names@1 and SEARCH-P-0010-graves@1'
    if cid=='C-0981': x['other_scope_owner']='T-0701 READY/G026: two A II b/14 property-register R; C-0971/C-0980 historical coverage claims also there'
    citations.append(x)
assert len(citations)==13

assets=[]
for x0 in baseline['asset_units']:
    x=copy.deepcopy(x0)
    a=one(conn,'SELECT path,sha256,bytes FROM asset WHERE path=?',(x['path'],))
    assert a and a['sha256']==x['sha256'] and x['hash_matches_scope'],x['path']
    x['current_database_sha256']=a['sha256']; x['current_database_bytes']=a['bytes']
    x['status']='original_scope_asset_exact_hash_match'
    assets.append(x)
assert len(assets)==11
new_media=[dict(r) for r in conn.execute("SELECT id,storage_path,sha256,bytes,operation_id FROM native_asset WHERE operation_id IN ('T-0676/graves-own-thirteen-v2','T-0676/graves-six-approved-v2-proposed') ORDER BY operation_id,id")]
assert len(new_media)==19
for m in new_media:
    m['journal_sequence']=journal[m['operation_id']]['sequence']
    m['status']='bound_after_scope_freeze_separate_from_11_original_assets'

crossrefs=[]
assessment_crossrefs={(x['cohort'],x['entity'],x['reason']):x for x in assessment['cross_references']}
for x0 in scope['cross_references']:
    x=copy.deepcopy(x0);tid=ownership[x['cohort']]
    x['owner_task']=tid;x['owner_status']=tasks[tid]['status']
    x['T0676_status']='routed_cross_reference_not_disposed_by_record_count'
    x['Astra_conditional_disposition']=assessment_crossrefs[(x['cohort'],x['entity'],x['reason'])]
    if x['entity'] in ['R-e445f96b83125c478c8b1af8','R-fa685dc0f1a3a1defbd354ae']:
        h=current(conn,x['entity']);assert h;x['current_revision']=h['id']
    crossrefs.append(x)
assert len(crossrefs)==24

journal_items=[]
for op,j in sorted(journal.items(),key=lambda z:z[1]['sequence']):
    journal_items.append(dict(j,operation_id=op))
assert [x['sequence'] for x in journal_items]==list(range(157,latest+1))

priority=[]
assessment_priority={x['object_id']:x for x in assessment['priority_decisions']}
for x0 in baseline['priority_claims_for_final_crosscheck']:
    x=copy.deepcopy(x0)
    h=current(conn,x['object_id'])
    if h:x['current_revision_at_j178']=h['id']
    x['assessment']='pending_Astra_final_crosscheck_no_projected_approval'
    x['Astra_conditional_decision']=assessment_priority[x['object_id']]
    if latest >= 180:
        assert h and h['id']==assessment_priority[x['object_id']]['current_revision']
        x['j178_assessment_historical']=x['assessment']
        x['assessment']='ROOT_ASTRA_FINAL_RETAIN_AT_J180'
        x['final_check_required']=False
        x['actual_revision_unchanged_at_journal_head']=True
        x['actual_decision']='RETAIN_NO_CANONICAL_CHANGE'
    priority.append(x)

result={
 'format':'T-0676-manifest-crosscheck-final-proposed/1',
 'date':'2026-09-24',
 'state':f'FINAL_MANIFEST_PROPOSED_AT_J{latest}_NOT_TASK_DONE' if latest >= 180 else f'PROPOSED_READ_ONLY_AT_J{latest}_NOT_FINAL_DISPOSITION',
 'inputs':{'scope':str(SCOPE.relative_to(ROOT)),'scope_sha256':EXPECTED_SCOPE_SHA,
           'baseline_preparation':'genealogy2/verification/T-0676/manifest-crosscheck-preparation-20260924.json',
           'crosswalk':'genealogy2/verification/T-0676/citation-scope-crosswalk-20260924.json',
           'routing':'genealogy2/verification/T-0676/three-citation-outside-record-routing-20260924.json',
           'Astra_assessment':'genealogy2/verification/T-0676/final-assessment-proposed-20260924.json',
           'Astra_assessment_sha256':assessment_sha,
           'canonical_journal_sequence':latest,'journal_window':[157,latest]},
 'counts':{'fixed_records':50,'records_with_native_source_review':len(reviewed),'records_pending_native_review':len(pending),
           'current_transcription_records':sum(bool(x['transcriptions']) for x in records),'citations':len(citations),
           'original_scope_assets':len(assets),'new_grave_native_assets':len(new_media),'cross_references':len(crossrefs)},
 'reviewed_ordinals':reviewed,'pending_ordinals':pending,
 'newly_canonical_since_baseline':{'journal_176_floda592':[4,12,28,47],
                                   'journal_177_178_floda608':[15,17],
                                   'journal_179_180_umea1839':[5,6,21,30,33,41,46] if latest >= 180 else [],
                                   'umea1839_still_pending':[i for i in [5,6,21,30,33,41,46] if i in pending]},
 'journal_crosscheck':journal_items,
 'records':records,'citation_units':citations,'original_asset_units':assets,'new_grave_native_assets':new_media,
 'cross_references':crossrefs,'priority_claims_for_final_crosscheck':priority,
 'routing_report_items':routing['items'],
 'Astra_j178_conditional_DONE_gate_historical':assessment['proposed_DONE_gate'],
 'Astra_remaining_unowned_gaps_review':assessment['remaining_unowned_substantive_gaps_in_50R'],
 'limitations':['Read-only manifest; record audits do not by themselves dispose of entire frozen citations.',
                'At journal 180 Umeå fol. 1839 seven R were applied in journal 179 and their actual pending dependencies resolved in journal 180; none remain pending.' if latest >= 180 else f'Umeå fol. 1839 pending native review ordinals at journal {latest}: {[i for i in [5,6,21,30,33,41,46] if i in pending]}; no prepared operation is counted as applied.',
                'C-0907 historical zero-folio scope, C-0923 searches, and C-0971/C-0980 coverage conclusions retain their separate owners and exact bounds.',
                'Nineteen newer grave assets are separate from the eleven original scope assets.',
                'At j180 the source-audit gate is current, but DONE still requires the in-progress full suite and root final assessment. This builder makes no task completion decision.' if latest >= 180 else 'Astra must decide substantive citation and priority-claim dispositions after remaining native apply; this builder makes no approvals.']
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(str(OUT.relative_to(ROOT)))
print(json.dumps(result['counts'],ensure_ascii=False))
