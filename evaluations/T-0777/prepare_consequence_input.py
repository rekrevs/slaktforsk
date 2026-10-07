"""Mechanical actual-current routing and full fields; no disposition judgement."""
import pathlib,json,re,hashlib
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
m=json.loads((B/'current-manifest.json').read_text());capture={x['id']:x for x in m['captures'] if x['view']=='inspect'}
for cid,case in m['cases'].items():
 rows=[]
 for oid in case['impact_objects']:
  cap=capture[oid];x=json.loads((R/cap['path']).read_text());cur=x['current'];fields={k:v for k,v in cur.items() if isinstance(v,str) and k in ['body','markdown','text','rationale','caveat','value_literal','outcome','property','criteria']}
  rows.append({'id':oid,'version':x['currentVersion'],'kind':x['kind'],'capture':cap,'full_current_fields':fields,'current_data':cur,'evidence':cur.get('evidence',x.get('evidence')),'disposition':None,'reason':None,'source_decision_datum':None,'semantic_judgement':'UNDECIDED: Astra must assign individual disposition, including retains'})
 save(B/(cid+'-consequence-input-v1.json'),{'task':'T-0777','case':cid,'baseline_journal':255,'rows':rows,'fields_truncated':False,'registered_impact_is_not_semantic_exhaustiveness':True})
# independent mechanical scan beyond literal citation-id across native current fields
patterns=['opröva','okänd','inte läst','ingen egen','tom','endast','luck','ditto','1902','1900','1930','638','563','Buberget','Rosinedal','1904','Floda','Flen','Segerslund','Ökna','30/10','11/11']
hits=[]
for oid,cap in capture.items():
 if not any(p in oid for case in m['cases'].values() for p in case['person_routes']):continue
 x=json.loads((R/cap['path']).read_text());cur=x['current']
 for field in ['body','markdown','caveat','rationale','text','value_literal']:
  value=cur.get(field)
  if not isinstance(value,str):continue
  terms=[t for t in patterns if t.lower() in value.lower()]
  if terms:hits.append({'id':oid,'version':x['currentVersion'],'field':field,'routing_terms':terms,'full_field':value,'capture':cap,'disposition':None})
save(B/'semantic-current-copy-routing-v1.json',{'task':'T-0777','baseline_journal':255,'mechanical_case_insensitive_substrings':patterns,'rows':hits,'truncated':False,'no_semantic_disposition':True,'limitation':'Routing terms do not prove relevance or error. Independent Astra must search native current DB outside this list and inspect full supports.'})
print('Consequence impact rows:',[(c,len(v['impact_objects'])) for c,v in m['cases'].items()],'semantic fullfield hits',len(hits))
