"""Capture C-0004 package inputs at journal 182; no operation is built."""
import hashlib
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / 'genealogy2/data/research.sqlite'
SOURCE = HERE / 'c0004-native-source-decisions-proposed-v2-20260924.json'
IMPACT = HERE / 'c0004-current-impact-proposed-v3-20260924.json'
OUT = HERE / 'c0004-package-currentheads-pre-v4-20260925.json'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE) == '6f1331f9a22198857eae7fb5400a6275b8b39c2c28742ec2fa87d0705ac4361f'
assert sha(IMPACT) == '7ac8d65d1d1b023cbe35f633ad9753620fea1cc3e9675f954ff686933414c39e'
source = json.loads(SOURCE.read_text())
impact = json.loads(IMPACT.read_text())
assert len(source['proposed_changes']) == 3
assert len(impact['changes']) == 11 and len({x['object_id'] for x in impact['changes']}) == 9
assert len(impact['bounded_adoptions']) == 8
assert len(impact['individual_dispositions']) == 34
conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
conn.row_factory = sqlite3.Row

def rows(sql,args=()): return [dict(r) for r in conn.execute(sql,args)]
def current(oid):
    objs = rows('SELECT kind FROM object WHERE id=?',(oid,))
    if not objs: return None
    assert len(objs)==1
    kind=objs[0]['kind']
    revs=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
    assert len(revs)==1
    rev=revs[0]
    data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],))
    assert len(data)==1
    data=data[0]; data.pop('revision_id')
    if 'value_json' in data and data['value_json'] is not None:
        data['value_json']=json.loads(data['value_json'])
    origins=[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']}
             for r in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rev['id'],))]
    evidence=[]
    for r in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rev['id'],)):
        basis,version=r['basis_revision_id'].rsplit('@',1)
        evidence.append({'object':basis,'version':int(version),'role':r['role'],'note':r['note']})
    return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}

source_ids={x['id'] for x in source['proposed_changes']}
impact_ids={x['object_id'] for x in impact['changes']}
disposition_ids={x['object_id'] for x in impact['individual_dispositions']}
adoption_ids={x['object_id'] for x in impact['bounded_adoptions']}
later_ids={x['object_id'] for x in impact['later_four_children_preservation']['full_current_carriers']}
later_relation_ids={x for x in later_ids if x.startswith('REL-parent-')}
known_ids=source_ids|impact_ids|disposition_ids|adoption_ids|later_ids|{
    'R-31970be0126dcd188cd61fd1','READ-T0677-C0004',
    'BIO-P-0001','BIO-P-0028','F-P-0030-reported_family_context-relations'}
captured={oid:current(oid) for oid in sorted(known_ids)}
assert len(later_relation_ids)==8 and len(later_ids)==11
assert all(captured[x] is None for x in adoption_ids|{'TR-T0677-C0004-consolidated-control','AUDIT-T0677-C0004'})
assert captured['R-31970be0126dcd188cd61fd1'] is not None
for change in source['proposed_changes']:
    cur=captured[change['id']]
    if change['expectedVersion'] is None: assert cur is None
    else: assert cur['revision']['version']==change['expectedVersion']
for change in impact['changes']:
    cur=captured[change['object_id']]
    assert cur['revision']['id']==change['current_revision']
    field=change['field']
    old=cur['data'][field] if field in cur['data'] else cur['revision'][field]
    if field=='value_json': old=json.dumps(old,ensure_ascii=False,separators=(',',':'))
    assert old==change['before'], (change['object_id'],field)
for disposition in impact['individual_dispositions']:
    cur=captured[disposition['object_id']]
    assert cur['revision']['id']==disposition['current_revision']
for relation in impact['later_four_children_preservation']['full_current_carriers']:
    assert captured[relation['object_id']]['revision']['id']==relation['id']

out={'task':'T-0677','state':'PRE_V4_CURRENTHEAD_CAPTURE_ONLY_NO_OPERATION',
     'canonical_journal_head':182,'canonical_pending_at_capture':0,
     'source_v2_sha256':sha(SOURCE),'impact_v3_sha256':sha(IMPACT),
     'sets':{'source_change_ids':sorted(source_ids),'impact_change_ids':sorted(impact_ids),
             'impact_disposition_ids':sorted(disposition_ids),'adoption_ids':sorted(adoption_ids),
             'later_four_parent_relation_ids':sorted(later_relation_ids),
             'later_four_other_carrier_ids':sorted(later_ids-later_relation_ids)},
     'counts':{'source_changes':3,'impact_objects':9,'impact_fields':11,'reviewed_objects':34,
               'bounded_adoptions':8,'later_four_parent_relations':8,
               'captured_distinct_ids':len(captured)},
     'captured_current':captured,
     'package_guards':{'no_operation_built':True,'no_temp_apply':True,'no_canonical_apply':True,
                       'await_impact_v4_root_acceptance':True,
                       'R_READ_historical_TR_retained':True,
                       'O_household_value_json_excludes_laterFourChildren_in_source_v2':
                       'laterFourChildren' not in source['proposed_changes'][2]['after']['data']['value_json'],
                       'foreign_source_not_independent_R_support':True}}
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(OUT),'sha256':sha(OUT),'counts':out['counts']}))
