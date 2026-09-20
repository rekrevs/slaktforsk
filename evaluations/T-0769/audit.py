import pathlib,json,hashlib,re
b=pathlib.Path(__file__).resolve().parent
f=json.loads((b/'frozen-manifest.json').read_text());issues=[]
for name,h in f['files'].items():
 if hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest()!=h:issues.append({'kind':'frozen_changed','file':name})
rows=[]
for r in json.loads((b/'measurements.json').read_text()):
 t=json.loads((b/'runs'/r['id']/'telemetry.json').read_text());public=b/r['task']/'public'
 input_ok=all((b/'runs'/r['id']/p.name).read_bytes()==p.read_bytes() for p in public.iterdir() if p.is_file())
 model_ok=all(x=={'model':r['model'],'effort':'medium'} for x in t['actual_models'])
 findings=[]
 for call in t['calls']:
  args=str(call.get('arguments',''))
  for term in ['rubric','reference.json','blind-map','/sessions/','genealogy2/data','private/evaluate','collaboration.spawn','web__run','mcp__cua','agent-principles','README.md','NORTH-STAR.md','AGENTS.md','/tmp/']:
   if term in args or term in str(call.get('name','')):findings.append({'term':term,'call':call})
 rows.append({'id':r['id'],'input_unchanged':input_ok,'model_matches':model_ok,'suspicious_calls':findings,'note':'Automatisk triage; faktisk läs-/skrivomfattning granskas även i sparade verktygsanrop.'})
(b/'audit.json').write_text(json.dumps({'frozen_issues':issues,'runs':rows},ensure_ascii=False,indent=2)+'\n')
print('frozen issues',len(issues),'runs',len(rows),'suspicious',sum(bool(r['suspicious_calls']) for r in rows),'mismatches',sum(not r['model_matches'] for r in rows))
