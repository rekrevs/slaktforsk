import json,pathlib,re,sys
b=pathlib.Path(__file__).resolve().parent;r=json.loads((b/'x/private/rubric.json').read_text())
norm=lambda x:re.sub(r'[^a-zåäö0-9]','',str(x).lower())
a=json.loads(pathlib.Path(sys.argv[1]).read_text());fs=a.get('fields',[]);d={v.get('id'):v for v in fs};rows=[]
for f in r['fields']:
 g=d.get(f['id'],{});raw=g.get('raw');state=g.get('state');preferred=norm(f['preferred_raw']);same=raw is not None and norm(raw)==preferred
 alternatives=[norm(x) for x in f['acceptable_raw_alternatives']]
 content=2 if same else (2 if raw is not None and norm(raw) in alternatives else None)
 needs=content is None or bool(f['critical_errors']) or state=='uncertain'
 rows.append({'id':f['id'],'candidate_content_score':content,'candidate_state_score':int(state in f['acceptable_states']),'needs_manual':needs,'raw':raw,'state':state,'alternatives':g.get('alternatives'),'note':g.get('note')})
print(json.dumps({'schema_ok':len(fs)==25 and set(d)=={f['id'] for f in r['fields']},'fields':rows,'status':'PRESCREEN_ONLY_NOT_FINAL','manual_required':True},ensure_ascii=False,indent=2))
