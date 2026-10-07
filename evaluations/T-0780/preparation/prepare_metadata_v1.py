import json,sqlite3,subprocess,hashlib,re,time
from pathlib import Path
base=Path('evaluations/T-0780/preparation');start=time.time()
def write(p,x): (base/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def cli(args,p):
 r=subprocess.run(['node','genealogy2/cli.mjs',*args],capture_output=True,text=True);(base/p).write_text(r.stdout);assert r.returncode==0,r.stderr;return json.loads(r.stdout)
def hash(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
assert (base/'baseline-j281.sqlite').exists() # original read-only backup preserved
m=json.load(open('genealogy2/verification/T-0673/manifest.json'));co=json.load(open('genealogy2/verification/T-0673/cohorts-draft.json'));g=next(x for x in co['cohorts'] if x['cohort_key']=='G002');pr=json.load(open('genealogy2/verification/T-0673/priority.json'))
write(Path('G002-fixed-cohort-v1.json'),g)
current={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')}
def obj(oid):
 r=current[oid].copy();rid=r['id'];r['data']=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(rid,)).fetchone());r['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=?',(rid,))];r['origins']=[dict(x) for x in c.execute('select o.*,u.document_path,u.start_line,u.end_line from origin o join unit u on o.unit_id=u.id where revision_id=?',(rid,))];return r
allobj={k:obj(k) for k in current}
write(Path('protected-state-v1.json'),[x for x in allobj.values() if x['evidence_status']=='OWNER_CONFIRMED' or x['kind']=='assessment' and x['data']['criteria'] in ['identity_review/1','tree_effect/1','life_picture_review/1']])
status=cli(['status'],Path('status-v1.json'));cli(['inventory'],Path('inventory-v1.json'));cli(['pedigree','P-0269'],Path('pedigree-P0269-verified-v1.json'))
seq=c.execute('select max(sequence),count(*) from operation_payload').fetchone();pending=status['domain']['pendingReviews'];assert seq[0]==281 and pending==0
cm=json.load(open('evaluations/T-0778/completion-manifest-v2.json'));pins=[{'path':x['path'],'expected':x['sha256'],'actual':hash(x['path'])} for x in cm['pins']];assert all(x['expected']==x['actual'] for x in pins)
write(Path('baseline-reconciliation-v1.json'),{'journal':seq[0],'pending':pending,'G001_completion':cm,'pins':pins,'journal_tail':dict(c.execute('select * from operation_payload order by sequence desc limit 1').fetchone()),'cohort_counts':g['member_counts']})
(base/'git-status-v1.txt').write_text(subprocess.check_output(['git','status','--short'],text=True))
cits={x['id']:x for x in m['citations']};records={x['object_id']:x for x in m['records']};assets={x['path']:x for x in m['imported_assets']};cards=[]
for cid in g['members']['citations']:
 ci=cits[cid];rids=sorted(set(ci['native_record_ids'])|{r for r in g['members']['records'] if cid in records[r]['citation_ids']});claims=[x for x in pr['claims'] if set(x['record_object_ids'])&set(rids)];paths=set(ci['legacy_media_paths'])
 for rid in rids:
  rr=current[rid]['id'];paths.update(x[0] for x in c.execute('select asset_path from record_asset where revision_id=?',(rr,)))
 medias=[]
 for p in sorted(paths):
  if p not in assets:continue
  a=assets[p];mrow={'path':p,'manifest_sha256':a['sha256'],'actual_sha256':hash(p),'bytes':Path(p).stat().st_size,'owners':[x for x in co['content_reading_owners'] if x.get('sha256')==a['sha256']]}
  try:
   out=subprocess.check_output(['sips','-g','pixelWidth','-g','pixelHeight',p],text=True,stderr=subprocess.DEVNULL);mrow.update(width=int(re.search(r'pixelWidth: (\d+)',out).group(1)),height=int(re.search(r'pixelHeight: (\d+)',out).group(1)))
  except Exception:mrow['non_raster']=True
  medias.append(mrow)
 direct=[x for x in allobj.values() if x['object_id'] in rids or any(e['basis_revision_id'].split('@')[0] in rids for e in x['evidence'])]
 persons=sorted(set(x['data'].get('person_id') for x in direct if x['data'].get('person_id')))
 for x in direct:
  for k in ['from_person','to_person','subject_id']:
   if str(x['data'].get(k,'')).startswith('P-'):persons.append(x['data'][k])
 persons=sorted(set(persons));audits=[x for x in allobj.values() if x['kind']=='assessment' and (x['data'].get('subject_id') in rids or cid in x['object_id']) and ('audit' in x['object_id'].lower() or 'reread' in x['data'].get('criteria',''))]
 card={'citation':cid,'metadata_only_not_source_people_certification':True,'manifest_citation':ci,'current_records':[obj(x) for x in rids],'baseline_priority_claims':claims,'current_claim_revisions':[obj(x['object_id']) for x in claims if x['object_id'] in current],'current_direct_consumers':direct,'metadata_person_routing':persons,'media':medias,'existing_audits':audits,'full_unit_limit':'Full citation scope; record count, locator and media links are routing only; Astra must determine relevant households, headers, continuation, margins and dependence.'}
 write(Path(cid+'-routing-v1.json'),card);cards.append({'citation':cid,'path':str(base/(cid+'-routing-v1.json')),'title':ci['title'],'records':len(rids),'media':len(medias),'person_ids':persons,'priority_scope_counts':{s:sum(x['scope']==s for x in claims) for s in sorted(set(x['scope'] for x in claims))},'prior_audits':[x['object_id'] for x in audits]})
write(Path('routing-index-v1.json'),{'task':'T-0780','journal':281,'metadata_only':True,'cards':cards,'elapsed_seconds':time.time()-start,'failure_notes':['Pillow unavailable in first run; sips dimension probe used. Initial combined inspect/pedigree output exceeded display limit; persisted outputs are complete.']})
print(json.dumps(cards,ensure_ascii=False))
