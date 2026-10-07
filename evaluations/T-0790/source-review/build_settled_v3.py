import json,hashlib
from pathlib import Path
D=Path(__file__).parent
v=json.loads((D/'settled-90-dispositions-and-literal-field-decisions-v2.json').read_text())
n=json.loads((D.parent/'preparation/complete-current-history-support-native.json').read_text())['objects']
for c in v['exact_changes']:
 if c['target_revision']=='THEME-P-0211-SYN@1':
  c['target_revision']='THEME-P-0211-SYN@2';c['expectedVersion']=2
  for f in c['field_changes']:f['old']=n[c['target_revision']]['data'][f['field']]
  c['reason']+=' V3: rättar v2:s felaktiga äldre måltavla; nuvarande T0674-caveat, rationale och två evidencekanter bevaras från @2.'
  c['amendment_caveat']+=' V3 utgår uttryckligen från current THEME-P-0211-SYN@2, inte @1.'
 if c['target_revision']=='CONTRACT-P-0005-PK-03@1':
  c['supporting_versions']=['BIO-P-0005@3' if x=='BIO-P-0005@2' else x for x in c['supporting_versions']]
  c['support_binding_decision']='BIO-P-0005@3: bind den i föregående mutation korrigerade dopkonsolideringen; @2 är historiskt underlag men inte aktuell API-basis vid denna ordning.'
for r in v['individual_table']:
 if r['object_id']=='THEME-P-0211-SYN':
  r['disposition']='revise';r['final_revision']='THEME-P-0211-SYN@3'
  r['final_supporting_versions']=['THEME-P-0211-SYN@3' if x=='THEME-P-0211-SYN@2' else x for x in r['final_supporting_versions']]
  r['individual_rationale']+=' Nuvarande @2:s T0674-förbehåll bevaras; endast den minimala sammanfattningen konsolideras i @3.'
 if r['person']=='P-0005' and r['item']=='PK-10':r['individual_rationale']=r['individual_rationale'].replace('BIO@2','korrigerad BIO-P-0005@3')
 if r['person']=='P-0212' and r['item']=='PK-10':r['individual_rationale']='STYRKT med korrigerad BIO-P-0212@6: C0906 begränsas till daterade lokala prov, obestyrkt Stockholmstraktsbostad tas bort och odaterad utbildning/möte placeras inte efter1962. Dotterns födelseort och flyttens ursprungsort förblir okända. Detta gör berättelsen sakligt korrekt men fyller inte livsluckan1951–1962 eller PK03/04/08.'
for rv in v['six_life_reviews']:
 p=rv['data']['subject_id']
 if p=='P-0211':
  for e in rv['evidence']:
   if e['object']=='THEME-P-0211-SYN':assert e['version']==2;e['version']=3
 if p=='P-0005':rv['data']['body']=rv['data']['body'].replace('BIO@2 bär berättelsen','korrigerad BIO-P-0005@3 bär berättelsen')
 if p=='P-0212':
  lines=rv['data']['body'].splitlines(); rationale=next(r['individual_rationale'] for r in v['individual_table'] if r['person']==p and r['item']=='PK-10')
  rv['data']['body']='\n'.join('PK-10 — STYRKT. '+rationale if x.startswith('PK-10 —') else x for x in lines)
# Exact per-target preserved and added edges. Do not infer any rebind in the assembler.
for c in v['exact_changes']:
 old=n[c['target_revision']]; ev=[]; decisions=[]
 for i,e in enumerate(old['evidence']):
  oid,ver=e['basis_revision_id'].rsplit('@',1)
  literal=dict(object=oid,version=int(ver),role=e['role'],note=e['note'])
  ev.append(literal);decisions.append(dict(source='existing',edge_index=i,action='retain exact',old_edge=e,literal_api_edge=literal,reason='Bevarat underlag och dess roll/notering; full mekanisk frågelista finner denna version aktuell vid angiven ordning. Ingen saklig ombindning behövs.'))
 for i,s in enumerate(c['supporting_versions']):
  oid,ver=s.rsplit('@',1);literal=dict(object=oid,version=int(ver),role='supports',note='T-0790: '+c['reason'])
  if any(x['object']==oid and x['version']==int(ver) and x['role']=='supports' for x in ev):
   decisions.append(dict(source='added support',support_index=i,action='reuse exact existing edge',basis=s,reason='Samma objekt/version/roll finns redan bland bevarade kanter; befintlig note behålls.'));continue
  ev.append(literal);decisions.append(dict(source='added support',support_index=i,action='bind literal',basis=s,literal_api_edge=literal,reason=c.get('support_binding_decision') if s=='BIO-P-0005@3' else 'Exakt accepterad version stödjer den angivna fälträttelsen; ingen ny oberoende källröst.'))
 c['literal_api_evidence']=ev;c['individual_evidence_decisions']=decisions
v['freeze']='Settled comparative amendment v3; v1 and flawed v2 preserved.'
v['amendment_v3']={'v2_sha256':'011e36d7fec196201345423f1277741be1b0879861693c7c7e359ecde795af90','corrections':['Evy SYN current target@2, planned@3, exact current caveat/edges; table and newlife rebound explicitly','P0005 PK03 added BIO support@3; PK10 newlife prose names final@3','Gunnar PK10 review rationale includes Stockholm and chronology corrections','Every existing target has literal API evidence list and per-edge retain/add decision; no runtime inference']}
p=D/'settled-90-dispositions-and-literal-field-decisions-v3.json';p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(hashlib.sha256(p.read_bytes()).hexdigest())
# Check all literal edge references against exact sequential current state.
heads={}
for x in n.values():heads[x['object_id']]=max(heads.get(x['object_id'],0),x['version'])
errors=[]
for c in v['exact_changes']:
 oid=c['target_revision'].rsplit('@',1)[0]
 for e in c['literal_api_evidence']:
  if heads.get(e['object'])!=e['version']:errors.append((oid,e,heads.get(e['object'])))
 assert heads[oid]==c['expectedVersion'];heads[oid]+=1
for rv in v['six_life_reviews']:
 for e in rv['evidence']:
  if heads.get(e['object'])!=e['version']:errors.append((rv['id'],e,heads.get(e['object'])))
print('sequential_edge_errors',json.dumps(errors,ensure_ascii=False))
