"""Build approved C-0751 combined proposal for isolated validation only."""
import copy
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
FILES={
 'source':HERE/'c0751-native-source-decisions-proposed-v3-20260925.json',
 'marriage':HERE/'c0751-marriage-copy-followup-proposed-v2-20260925.json',
 'other':HERE/'c0751-other-current-impact-proposed-v4-20260925.json',
 'texts':HERE/'c0751-root-v4-final-text-amendments-20260925.json',
 'plan':HERE/'c0751-combined-build-plan-proposed-v2-20260925.json',
 'review':HERE/'c0751-other-impact-final-independent-review-20260925.json',
 'accept':HERE/'c0751-root-substantive-build-acceptance-20260925.json',
}
EXPECTED={
 'source':'a7d597bfa3a3c8d0c705dd29a4b27973e7b8233aea084242f64c7089399394f0',
 'marriage':'6d44287d28660784505d2ba7e35537e763885fc30b0a86706d3835ca7dddafe9',
 'other':'223b8218373fa1b0ca96199a266b192f9d9d88aa68ffdaa86d50a9ae4fb875ce',
 'texts':'f8f85e0271fea83eae144786a9c646a4f483280416153ff39650f3e04e601a00',
 'plan':'3a81067e468e4a6edee737b6eb1ae960707ef2f0ea6dd98d2a11bca47341345d',
 'review':'156a8fa45e8e4c5852c8c0cbf624866ade61b66dad77fb08058d666ee14f28e5',
 'accept':'5b32fa59b651d2b9951a3bb761acee147ab66aa92a53d3a0af28e46f7ec0dc6d',
}
OUT=HERE/'c0751-combined-proposed-operation-20260925.json'
REPORT=HERE/'c0751-combined-buildcheck-20260925.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for key,path in FILES.items():assert sha(path)==EXPECTED[key],key
source,marriage,other,texts,plan,review,accept=[json.loads(FILES[k].read_text()) for k in FILES]
assert accept['canonical_apply_authorized'] is False
assert plan['canonical_journal_head']==184 and plan['canonical_pending_at_capture']==0
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(x) for x in conn.execute(sql,args)]
def current(oid):
 obj=rows('SELECT kind FROM object WHERE id=?',(oid,));assert len(obj)==1,oid
 kind=obj[0]['kind'];rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
 assert len(rev)==1;rev=rev[0]
 data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],));assert len(data)==1
 data=data[0];data.pop('revision_id')
 for key,value in list(data.items()):
  if key.endswith('_json') and value is not None:data[key]=json.loads(value)
 origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']}
          for x in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rev['id'],))]
 evidence=[]
 for x in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rev['id'],)):
  basis,version=x['basis_revision_id'].rsplit('@',1)
  evidence.append({'object':basis,'version':int(version),'role':x['role'],'note':x['note']})
 return kind,rev,data,origins,evidence
def edge(raw):
 if 'basis_revision_id' in raw:
  basis,version=raw['basis_revision_id'].rsplit('@',1)
  return {'object':basis,'version':int(version),'role':raw['role'],'note':raw['note']}
 return copy.deepcopy(raw)
def merge_edges(existing,extra):
 result=copy.deepcopy(existing)
 keys={(e['object'],e['version'],e['role']) for e in result}
 for raw in extra:
  e=edge(raw);key=(e['object'],e['version'],e['role'])
  if key not in keys:result.append(e);keys.add(key)
 return result

changes=[];source_checks=[]
for p in source['proposed_changes']:
 oid=p['id'];after=copy.deepcopy(p['after']);version=p['expectedVersion']
 for key,value in list(after['data'].items()):
  if key.endswith('_json') and isinstance(value,str):after['data'][key]=json.loads(value)
 if version is None:
  assert not rows('SELECT id FROM object WHERE id=?',(oid,))
  changes.append({'id':oid,'kind':p['kind'],'expectedVersion':None,**after})
  source_checks.append({'id':oid,'absent':True})
 else:
  kind,rev,data,origins,evidence=current(oid)
  assert kind==p['kind'] and rev['version']==version,oid
  assert set(data)==set(after['data']),oid
  proposed_origins={(x.get('unit',x.get('unit_id')),x['coverage'],x['note']) for x in after.get('origins',[])}
  assert proposed_origins=={(x['unit'],x['coverage'],x['note']) for x in origins},oid
  proposed_edges=[edge(e) for e in after['evidence']]
  changes.append({'id':oid,'kind':kind,'expectedVersion':version,'data':after['data'],
                  'disposition':after['disposition'],'evidenceStatus':after['evidenceStatus'],
                  'rationale':after['rationale'],'caveat':after['caveat'],
                  'origins':origins,'evidence':proposed_edges})
  source_checks.append({'id':oid,'head':rev['id'],'before_data':data,
                        'after_data':after['data'],'before_caveat':rev['caveat'],
                        'after_caveat':after['caveat'],
                        'before_evidence':evidence,'after_evidence':proposed_edges})

patches=defaultdict(dict);versions={};extras=defaultdict(list);field_checks=[]
for family,p_list in [('marriage_v2',marriage['changes']),('other_v4',other['changes'])]:
 for p in p_list:
  oid,field=p['object_id'],p['field']
  assert oid not in versions or versions[oid]==p['current_revision']
  versions[oid]=p['current_revision']
  if field in patches[oid]:
   assert family=='other_v4' and patches[oid][field]['family']=='marriage_v2'
   assert p['marriage_v2_after']==patches[oid][field]['after']
   patches[oid][field]={'family':family,'before':p['before'],'after':p['after']}
  else:patches[oid][field]={'family':family,'before':p['before'],'after':p['after']}
  extras[oid].extend(p['evidence_add'])
format_applied=[];format_superseded=[]
for p in other['marriage_only_format_delta']:
 oid,field=p['object_id'],p['field']
 if patches[oid][field]['family']=='other_v4':
  format_superseded.append((oid,field));continue
 assert patches[oid][field]['family']=='marriage_v2'
 assert patches[oid][field]['after']==p['marriage_v2_after']
 patches[oid][field]['after']=p['after']
 format_applied.append((oid,field))
assert len(format_applied)==3 and len(format_superseded)==5
amended=[]
for p in texts['amendments']:
 oid,field=p['object_id'],p['field']
 assert patches[oid][field]['family']=='other_v4'
 assert patches[oid][field]['after'].count(p['old'])==1
 patches[oid][field]['after']=patches[oid][field]['after'].replace(p['old'],p['new'])
 amended.append((oid,field))
assert len(amended)==2
assert len(patches)==113 and sum(map(len,patches.values()))==113
for oid,fields in sorted(patches.items()):
 kind,rev,data,origins,evidence=current(oid)
 assert rev['id']==versions[oid],oid
 newdata=copy.deepcopy(data);metadata={'disposition':rev['disposition'],
   'evidenceStatus':rev['evidence_status'],'rationale':rev['rationale'],'caveat':rev['caveat']}
 for field,p in fields.items():
  raw=rows(f'SELECT {field} FROM {kind} WHERE revision_id=?',(rev['id'],)) if field in data else []
  before=raw[0][field] if raw else rev[field]
  assert before==p['before'],(oid,field)
  after=json.loads(p['after']) if field.endswith('_json') and isinstance(p['after'],str) else p['after']
  if field in data:newdata[field]=after
  else:
   assert field in metadata,(oid,field)
   metadata[field]=after
  field_checks.append({'id':oid,'current_revision':rev['id'],'field':field,
                       'before':p['before'],'after':p['after'],'source_family':p['family']})
 rationales=[x['rationale'] for x in marriage['changes']+other['changes'] if x['object_id']==oid]
 metadata['rationale']=(rev['rationale']+'\nT-0677 C-0751: '+' '.join(dict.fromkeys(rationales))).strip()
 newevidence=merge_edges(evidence,extras[oid])
 if oid in ('BIO-P-0481','RESEARCH-P-0481-9d76f0343410'):
  hits=[e for e in newevidence if e['object']=='F-P-0481-source_interpretation-individual-limits'
        and e['version']==1 and e['role']=='supports']
  assert len(hits)==1,oid
  hits[0]['version']=2
  hits[0]['note']={
   'BIO-P-0481':'Namnreservationen och äldst bland redovisade består i F@2; samma C0548-vigselnyckel 1879-11-21 utan egen vigselpost, ingen ny identitetsröst.',
   'RESEARCH-P-0481-9d76f0343410':'Namnreservationen och aritmetiken fyllda 21 år 1902 består i F@2 utan inskrivningspåstående; C0548-vigselnyckeln preciseras utan egen vigselpost.'
  }[oid]
 changes.append({'id':oid,'kind':kind,'expectedVersion':rev['version'],'data':newdata,
                 'disposition':metadata['disposition'],'evidenceStatus':metadata['evidenceStatus'],
                 'rationale':metadata['rationale'],'caveat':metadata['caveat'],
                 'origins':origins,'evidence':newevidence})

for a in other['bounded_adoptions_proposed']:
 oid=a['object_id'];assert not rows('SELECT id FROM object WHERE id=?',(oid,))
 changes.append({'id':oid,'kind':'assessment','expectedVersion':None,
                 'data':{'subject_id':a['subject_id'],'criteria':'bounded_source_adoption/1',
                         'outcome':'adopted_with_limits','body':a['body']},
                 'disposition':'recorded','evidenceStatus':None,
                 'rationale':'T-0677: C-0751:s avgränsade källadoption; inga identitets-, trädverkans- eller livsbildsgrindar uppgraderas.',
                 'caveat':'','evidence':[edge(e) for e in a['evidence']]})
key=other['new_key_candidate'];assert not rows('SELECT id FROM object WHERE id=?',(key['object_id'],))
changes.append({'id':key['object_id'],'kind':'assessment','expectedVersion':None,
                'data':{'subject_id':key['subject_id'],'criteria':key['criteria'],
                        'outcome':key['outcome'],'body':key['body']},
                'disposition':'recorded','evidenceStatus':None,
                'rationale':'T-0677: avgränsad söknyckel, kandidat utan person- eller föräldralänk.',
                'caveat':'','evidence':[edge(e) for e in key['evidence']]})
assert len(changes)==135 and len({x['id'] for x in changes})==135
assert sum(x['expectedVersion'] is None for x in changes)==16
assert sum(x['expectedVersion'] is not None for x in changes)==119

# Topological order among revised/created objects. Only root-approved version
# substitutions above; order itself cannot silently change an evidence claim.
byid={x['id']:x for x in changes};deps={}
for x in changes:
 deps[x['id']]={e['object'] for e in x.get('evidence',[]) if e['object'] in byid
               and e['version']==(byid[e['object']]['expectedVersion'] or 0)+1}
done=set();ordered=[]
while len(done)<len(changes):
 ready=[oid for oid in byid if oid not in done and deps[oid]<=done]
 assert ready,{'cycle_or_bad_edges':{k:sorted(v-done) for k,v in deps.items() if k not in done}}
 for oid in ready:ordered.append(byid[oid]);done.add(oid)
changes=ordered
assert changes.index(byid['F-P-0481-source_interpretation-individual-limits'])<changes.index(byid['BIO-P-0481'])
assert changes.index(byid['F-P-0481-source_interpretation-individual-limits'])<changes.index(byid['RESEARCH-P-0481-9d76f0343410'])
revised={x['id'] for x in changes if x['expectedVersion'] is not None}
stale=[]
for x in changes:
 for e in x.get('evidence',[]):
  if e['object'] in revised and e['version']==byid[e['object']]['expectedVersion']:
   stale.append({'target':x['id'],'basis':e['object'],'version':e['version'],'role':e['role']})
assert not stale,stale

op={'id':'T-0677/C0751-source-marriage-impact-v1','actor':'Codex Sol; root/Astra approved bounded inputs',
    'reason':'T-0677 C-0751: 169 fysiska celler med exakt återbruk och kontrollerad källaudit; tre R-källgränser, individuella person-/forskningsföljder, dokumentär C0548-vigselnyckel och avgränsade adoptioner. Ingen ny föräldralänk, identitet eller kontraktsgrind.',
    'dependencyReviewVersion':2,'changes':changes}
OUT.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
report={'task':'T-0677','state':'COMBINED_PROPOSAL_FOR_ISOLATED_TEMP_NOT_CANONICAL_APPLY',
        'operation_path':str(OUT.relative_to(ROOT)),'operation_sha256':sha(OUT),
        'input_sha256':{str(v.relative_to(ROOT)):sha(v) for v in FILES.values()},
        'counts':{'objects':135,'revisions':119,'creates':16,'source_objects':10,
                  'marriage_fields':19,'other_fields':101,'composed_overlap_fields':7,
                  'format_applied_marriage_only_fields':3,'format_superseded_by_other_fields':5,
                  'root_text_amendments':2,'stale_old_basis_edges_remaining':len(stale)},
        'source_checks':source_checks,'followup_field_checks':field_checks,
        'format_applied':format_applied,'format_superseded':format_superseded,
        'text_amendments':amended,'approved_F481_rebases':['BIO-P-0481','RESEARCH-P-0481-9d76f0343410'],
        'no_canonical_apply':True,'no_review_resolution':True}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'operation_sha256':sha(OUT),'buildcheck_sha256':sha(REPORT),
                  'counts':report['counts']}))
