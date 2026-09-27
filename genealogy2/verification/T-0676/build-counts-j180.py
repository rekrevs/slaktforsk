#!/usr/bin/env python3
"""Count actual T-0676 journals 157–180 and link saved apply/check outputs.

No CLI tests, original access, or native writes are performed.
"""
import collections
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'genealogy2/verification/T-0676'
OUT=BASE/'counts-j180-20260924.json'

def load(p): return json.loads(p.read_text())
def rel(p): return str(p.relative_to(ROOT))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

apply_candidates=[]
for p in BASE.glob('*apply-result*.json'):
    try:
        outer=load(p);result=outer.get('result',outer)
    except (json.JSONDecodeError, UnicodeDecodeError):continue
    if isinstance(result,dict) and result.get('journal',{}).get('written')==1:
        apply_candidates.append((p,outer,result))

rows=[]
for n in range(157,181):
    matches=list((ROOT/'genealogy2/journal').glob(f'{n:09d}-*.json'))
    assert len(matches)==1,(n,matches)
    p=matches[0];d=load(p);q=d['request'];op=q['id']
    assert d['sequence']==n and d['requestHash'] in p.name
    changes=q.get('changes',[]);resolves=q.get('resolve',[])
    creates=[x for x in changes if x.get('expectedVersion') is None]
    revisions=[x for x in changes if x.get('expectedVersion') is not None]
    apps=[(ap,outer,result) for ap,outer,result in apply_candidates if result.get('operation')==op]
    assert len(apps)==1,(n,op,[x[0].name for x in apps])
    ap,outer,result=apps[0]
    assert result['changes']==len(changes),(n,'apply change mismatch')
    prefix=ap.name.split('-apply-result')[0]
    suffix='-20260924' if ap.name.endswith('-20260924.json') else ''
    checks={}
    for typ in ['verify','verify-assets','verify-source']:
        cp=BASE/f'{prefix}-{typ}-result{suffix}.json'
        if not cp.exists() and suffix:
            cp=BASE/f'{prefix}-{typ}-result.json'
        if n in (179,180):
            cp=BASE/f'{prefix}-{typ}-20260924.json'
        if cp.exists():
            value=load(cp)
            actual=value.get('result',value)
            checks[typ]={'path':rel(cp),'sha256':digest(cp),'ok':actual.get('ok') if isinstance(actual,dict) else None,
                         'exit_code':value.get('exitCode') if isinstance(value,dict) else None}
        else: checks[typ]={'path':None,'status':'saved_result_not_found_by_exact_apply_prefix'}
    rows.append({
      'sequence':n,'operation_id':op,'journal_file':rel(p),'journal_sha256':digest(p),
      'request_hash':d['requestHash'],'changes':len(changes),'creates':len(creates),'revisions':len(revisions),
      'change_kinds':dict(sorted(collections.Counter(x['kind'] for x in changes).items())),
      'native_resolve':len(resolves),
      'native_resolve_decision_field':dict(sorted(collections.Counter(x.get('decision','not_specified') for x in resolves).items())),
      'apply_result':{'path':rel(ap),'sha256':digest(ap),'operation_id':result['operation'],
                      'changes':result['changes'],'pending_reviews_after_apply':result.get('pendingReviews'),
                      'journal_written':result['journal']['written'],
                      'exit_code':outer.get('exitCode') if isinstance(outer,dict) else None},
      'saved_checks':checks,
      'saved_three_check_set_found':all(checks[k].get('ok') is True for k in ['verify','verify-assets','verify-source'])
    })

summary={
 'journal_count':len(rows),
 'changes':sum(x['changes'] for x in rows),
 'creates':sum(x['creates'] for x in rows),
 'revisions':sum(x['revisions'] for x in rows),
 'native_resolve':sum(x['native_resolve'] for x in rows),
 'native_resolve_decision_field':dict(sorted(collections.Counter(k for x in rows for k,v in x['native_resolve_decision_field'].items() for _ in range(v)).items())),
 'apply_results_found':sum(bool(x['apply_result']) for x in rows),
 'complete_saved_three_check_sets':sum(x['saved_three_check_set_found'] for x in rows),
 'missing_saved_three_check_sets':[x['sequence'] for x in rows if not x['saved_three_check_set_found']]
}
assert summary['changes']==783 and summary['creates']==146 and summary['revisions']==637 and summary['native_resolve']==229
assert summary['missing_saved_three_check_sets']==[157]
result={
 'schema':'T0676-journal-counts/1','task':'T-0676','date':'2026-09-24',
 'scope':'actual canonical journal entries 157–180 inclusive; no future proposal counted',
 'method':'Counts derive solely from each journal JSON request.changes and request.resolve. Missing expectedVersion means create; an explicit version means revision. Apply/check files are linked by exact operation id and apply-result filename stem. No SQLite rowid or prospective pending used for totals.',
 'summary':summary,'per_journal':rows,
 'separation_note':'Documentary substantive reviews, comparison approvals, and content-retain decisions are not counted as native resolve. Only request.resolve entries actually present in journal JSON count as native resolution; 228 omit a decision field, one explicitly says revised. No resolution count implies an independent source or a substantive approval.',
 'journal_157_check_evidence':{
   'dev_log':'wotan/dev-log/T-0676.md:204',
   'log_statement':'The first native-batch checkpoint identifies operation T-0676/reuse-3-44-v1, journal 157, then reports verify, verify-assets and verify-source PASS with pending 0 at lines 204–210.',
   'saved_individual_results':'not_found',
   'temporal_boundary':'The next checkpoint at lines 236–245 identifies journal 158 apply before reporting its own PASS checks. The saved umea-bi11 verify files therefore support the later j158 state, not a separate j157 result.',
   'later_current_head':'Journal 180 has its own saved apply and three ok=true checks; those are later-head validation and do not backfill individual j157 artifacts.'
 },
 'check_caveat':'Journal 157 has a dev-log PASS statement but no individually saved verify, verify-assets, or verify-source result located for that post-apply state. This is a saved-artifact gap, not a claim that checks failed or never ran. All other 23 journal entries have saved three-check results reporting ok=true. No later result is attributed to j157. No new checks were run for this report.',
 'canonical_change':False,'wotan_change':False
}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(rel(OUT))
print(json.dumps(summary,ensure_ascii=False))
