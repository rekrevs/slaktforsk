import pathlib,json,sqlite3,datetime,hashlib,native_payload
B=pathlib.Path(__file__).resolve().parent;native_payload.connection=sqlite3.connect('file:'+str(B/'clone/research-candidate-v6.sqlite')+'?mode=ro',uri=True);native_payload.connection.row_factory=sqlite3.Row
dec=json.loads((B/'source-decisions/C-0083-decisions-amendment-v1.json').read_text());grouped={};table=[]
for e in dec['native_changes']:
 if e['id'] in ['E-other-P-0015-folio1851904','PATH-P-0015-KP-06']:
  table.append({**e,'implementation':'Already applied independent final IF2/IF3 exact authorized wording; no duplicate application, primary confirmation requested.'});continue
 obj=grouped.setdefault(e['id'],native_payload.existing(e['id'],e['expectedVersion']));field=e['field'];target=obj if field=='caveat' else obj['data']
 if field.endswith('_json'):
  raw=native_payload.rows('select '+field+' from '+obj['kind']+' where revision_id=?',(e['id']+'@'+str(e['expectedVersion']),))[0][field];count=raw.count(e['before']);assert count==e['expected_match_count'];target[field]=json.loads(raw.replace(e['before'],e['after'],1))
 else:
  count=target[field].count(e['before']);assert count==e['expected_match_count'],(e['id'],field,count);target[field]=target[field].replace(e['before'],e['after'],1)
 for binding in e['approved_support']:
  oid,ver=binding.rsplit('@',1)
  if not any(x['object']==oid and x['version']==int(ver) for x in obj['evidence']):obj['evidence'].append({'object':oid,'version':int(ver),'role':'supports','note':'T-0776: explicit individuellt Astra-prövat äldre källstöd; ingen ny originalöppning.'})
 obj['rationale']+=' T-0776 AC3: '+e['reason'];table.append({**e,'actual_match_count':count,'implementation':'Exact revision'})
op={'id':'T-0776/C0083-consequence-amendment-v1','actor':'Codex Sol mechanical implementation of settled primary Astra consequence decisions','reason':'T-0776 AC3–4: exakt konsolidering av källkedja, släktskapsordning, fadderroll och registrerad frånvaro; kontrollerad kanonisk införsel efter självständig slutgranskning.','dependencyReviewVersion':2,'changes':list(grouped.values())}
def save(name,x):(B/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
p=B/'C-0083-consequence-amendment-operation-v1.json';save(p.name,op);save('C-0083-consequence-amendment-table-v1.json',{'rows':table});files=[p,B/'source-decisions/C-0083-decisions-amendment-v1.json',B/'C-0083-consequence-amendment-table-v1.json'];save('C-0083-consequence-amendment-freeze-v1.json',{'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in files]});print('6 exact patches across',len(grouped),'objects frozen')
