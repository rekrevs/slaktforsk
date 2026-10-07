import pathlib,json,hashlib,datetime
R=pathlib.Path(__file__).resolve().parents[2];B=R/'evaluations/T-0776'
manifest_paths=['evaluations/T-0775/completion-manifest-v1.json','evaluations/T-0775/protected-before-final-review.json','evaluations/T-0773/completion-manifest.json','evaluations/T-0774/completion-manifest.json']
bindings=[]
for mp in manifest_paths:
 p=R/mp;x=json.loads(p.read_text());
 if mp.endswith('protected-before-final-review.json'): rows=x['files']
 elif 'artifacts' in x:rows=x['artifacts']
 elif 'evidence_sha256' in x:rows=[{'path':str(p.parent/R if False else p.parent/k),'sha256':v} for k,v in x['evidence_sha256'].items()]
 else:rows=[{'path':str(p.parent/k),'sha256':v} for k,v in x['files'].items()]
 for row in rows:
  q=pathlib.Path(row['path']);q=q if q.is_absolute() else R/q;rel=str(q.relative_to(R))
  if not rel.startswith(('evaluations/T-0775/','evaluations/T-0773/','evaluations/T-0774/','genealogy/','dashboard/')):continue
  actual=hashlib.sha256(q.read_bytes()).hexdigest() if q.is_file() else None
  bindings.append({'manifest':mp,'path':rel,'expected':row['sha256'],'actual':actual,'match':actual==row['sha256']})
# Added meter amendment has separate later provenance and is not asserted pinned by older completion.
p=R/'evaluations/T-0775/budget-amendment-v1.json';extra={'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'baseline':'Current immutable later amendment; separate from older completion bindings.'} if p.exists() else None
out={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Only actual hash bindings in named prior manifests; no broad unrecorded filesystem assertion.','bindings':bindings,'all_match':all(v['match'] for v in bindings),'count':len(bindings),'separate_budget_amendment':extra}
(B/'prior-pilot-preservation-v1.json').write_text(json.dumps(out,indent=2)+'\n');print(len(bindings),'bindings;',sum(not r['match'] for r in bindings),'mismatches')
for r in bindings:
 if not r['match']:print(r['manifest'],r['path'])
