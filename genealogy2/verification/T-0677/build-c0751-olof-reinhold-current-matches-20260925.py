"""Bounded read-only current-head search; no identity decision or native write."""
import hashlib
import json
import re
import sqlite3
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
OUT=HERE/'c0751-olof-reinhold-current-matches-20260925.json'
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True)
conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(r) for r in conn.execute(sql,args)]
def full(oid):
    objects=rows('SELECT kind FROM object WHERE id=?',(oid,))
    assert len(objects)==1,oid
    kind=objects[0]['kind']
    rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
    assert len(rev)==1
    rev=rev[0]
    data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],))
    assert len(data)==1
    data=data[0];data.pop('revision_id')
    for key,value in list(data.items()):
        if key.endswith('_json') and value is not None:data[key]=json.loads(value)
    origins=[{'unit_id':x['unit_id'],'coverage':x['coverage'],'note':x['note']}
             for x in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rev['id'],))]
    evidence=rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rev['id'],))
    return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}

kinds=('person','mention','record','observation','fact','assessment','narrative','transcription')
exact=[];near=[];counts={}
for kind in kinds:
    current=rows(f'''SELECT o.id,r.id revision_id,t.* FROM object o
                    JOIN revision r ON r.object_id=o.id
                    JOIN {kind} t ON t.revision_id=r.id
                    WHERE o.kind=? AND r.version=(SELECT MAX(version) FROM revision WHERE object_id=o.id)''',(kind,))
    counts[kind]=len(current)
    for row in current:
        text=' '.join(str(v) for k,v in row.items()
                      if k not in ('id','revision_id') and v is not None)
        exact_hit=re.search(r'\bOlof Reinhold(?: Lindberg)?\b',text,re.I)
        near_hit=re.search(r'\b(?:Olof|Olov|Olaf)\s+Rein\w+\b',text,re.I)
        if exact_hit:
            exact.append({'object_id':row['id'],'revision_id':row['revision_id'],
                          'kind':kind,'matched_text':exact_hit.group(0)})
        elif near_hit and ('lindberg' in text.casefold() or 'ekträsk' in text.casefold()):
            near.append({'object_id':row['id'],'revision_id':row['revision_id'],
                         'kind':kind,'matched_text':near_hit.group(0)})
assert {r['object_id'] for r in exact}=={
    'F-P-0422-household_context-Olof-Reinhold','CONTRACT-P-0422-PK-04','BIO-P-0422'}

context_ids={
    # The fact's subject is a separate person; the old fact caveat explicitly
    # says row 25 is outside the captured row-24 record.
    'P-0422':'subject of exact-name fact, not an Olof person identity',
    'R-59d82d4780e5951f47a4fc15':'folio 601 row 24 record, explicitly not row 25',
    # Existing C-0751 Lindberg/Ekträsk household uses Johan Reinhold, not Olof.
    'R-a562da850d1352c7634aa1ca':'C-0751 Lindberg/Ekträsk household record',
    'TR-0ba53795cef5612374e768d3':'C-0751 household historical transcription',
    'M-P-0481-C0751-own':'Johan Reinhold child-row mention, different first name',
    'O-P-0481-C0751-own':'Johan Reinhold child-row observation, different first name',
    'P-0481':'Johan Reinhold person, different first name',
    'RESEARCH-P-0481-9d76f0343410':'Johan Reinhold research carrier, different first name',
}
selected={oid:full(oid) for oid in sorted({r['object_id'] for r in exact+near}|set(context_ids))}
assert all(selected[r['object_id']]['revision']['id']==r['revision_id'] for r in exact+near)
assert selected['F-P-0422-household_context-Olof-Reinhold']['data']['value_json']['name']=='Olof Reinhold Lindberg'
assert selected['M-P-0481-C0751-own']['data']['name_literal']=='Johan Reinhold'
row7_locators=[]
for r in rows('''SELECT o.id,r.id revision_id,t.locator FROM object o
                 JOIN revision r ON r.object_id=o.id JOIN record t ON t.revision_id=r.id
                 WHERE o.kind='record' AND r.version=(SELECT MAX(version) FROM revision WHERE object_id=o.id)'''):
    if re.search(r'(?:s\.?\s*78|sida\s*78).{0,20}rad\s*7\b',r['locator'],re.I):
        row7_locators.append(r)
out={'task':'T-0677','state':'READ_ONLY_CURRENT_HEAD_SEARCH_NO_IDENTITY_DECISION',
     'canonical_journal_head':184,'canonical_pending_at_capture':0,
     'search_scope':{'kinds':list(kinds),'current_heads_scanned_by_kind':counts,
                     'exact_pattern':'\\bOlof Reinhold(?: Lindberg)?\\b (case-insensitive)',
                     'near_pattern':'\\b(?:Olof|Olov|Olaf)\\s+Rein\\w+\\b with Lindberg or Ekträsk in same current payload',
                     'context_rule':'only direct subject/row context and the existing C-0751 Johan Reinhold Lindberg/Ekträsk household; no global Reinhold dump'},
     'exact_current_matches':exact,'near_variant_current_matches':near,
     'current_record_locator_s78_row7_matches':row7_locators,
     'selected_context_ids_and_limits':context_ids,
     'selected_full_current_payloads':selected,
     'negative_findings':{'current_person_named_Olof_Reinhold_Lindberg':False,
                          'current_mention_named_Olof_Reinhold_Lindberg':False,
                          'current_record_or_observation_with_exact_name':False,
                          'current_record_locator_s78_row7':len(row7_locators)==0,
                          'near_Olov_Olaf_Reinhold_variant_in_Lindberg_Ektrask_context':len(near)==0},
     'limits':['F-P-0422:s folio 601 rad25 är personanknuten kontext med eget A-origin; R för rad24 är uttryckligen inte stöd för rad25.',
               'C-0751:s befintliga Lindberg/Ekträsk-objekt gäller Johan Reinhold. Ingen koppling till nygranskad sida 78 rad 7 fastställs här.',
               'Inga historiska revisioner eller originalbilder omprövades. Ingen identitets- eller släktskapsbedömning.'],
     'no_native_write':True}
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':str(OUT),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
                  'exact_matches':len(exact),'near_variants':len(near),
                  'selected_payloads':len(selected),'scanned':sum(counts.values())}))
