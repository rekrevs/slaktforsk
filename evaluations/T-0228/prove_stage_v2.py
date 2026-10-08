import pathlib,sqlite3,json,hashlib,collections,datetime
B=pathlib.Path(__file__).resolve().parent;ROOT=B.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def conn(p):
 c=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
b=conn(B/'clone/baseline.sqlite');s=conn(B/'clone/final-stage.sqlite')
errors=[];tableproof=[]
for q in b.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'"):
 t=q[0]
 if t.startswith('object_search'):continue # derived FTS cache intentionally rebuilds touched current objects; not immutable evidence
 old=[tuple(x)for x in b.execute('select * from "'+t+'"')];new=collections.Counter(tuple(x)for x in s.execute('select * from "'+t+'"'));missing=[r for r,n in collections.Counter(old).items()if new[r]<n]
 # Object current_version is the controlled revisable pointer.
 if t=='object':
  missing=[]
  for r in old:
   a=s.execute('select * from object where id=?',(r[0],)).fetchone()
   if a is None or tuple(a)!=r:missing.append(r)
 if missing:errors.append({'table':t,'baseline_rows_changed':len(missing)})
 tableproof.append({'table':t,'old_rows':len(old),'stage_rows':sum(new.values()),'old_immutable_rows_retained':not missing})
op=json.loads((B/'operation-v1.json').read_text());revised={x['id']for x in op['changes']if x['expectedVersion']is not None};newids={x['id']for x in op['changes']if x['expectedVersion']is None}
heads=lambda c:{r['object_id']:r['version']for r in c.execute('select object_id,version from current_revision')}
bh,sh=heads(b),heads(s);diff={o:(v,sh.get(o))for o,v in bh.items()if sh.get(o)!=v}
if set(diff)!=revised:errors.append({'unexpected_head_delta':diff})
for o,(v,w)in diff.items():
 if w!=v+1:errors.append({'wrong_revision_step':o})
if set(sh)-set(bh)!=newids:errors.append({'unexpected_new_heads':list(set(sh)-set(bh)-newids)})
connection=b;exec((ROOT/'evaluations/T-0778/native_payload.py').read_text());payloadproof=[]
for x in op['changes']:
 if x['id']not in revised:continue
 old=existing(x['id'],x['expectedVersion']);body=old['data']['body'];ok=x['data']['body'].startswith(body+'\n\n')
 for k,v in old['data'].items():
  if k=='body':continue
  if x['id']=='PATH-P-0003-KP-03'and k=='outcome':ok=ok and x['data'][k].startswith(v+' T-0228:');continue
  ok=ok and x['data'][k]==v
 ok=ok and x['origins']==old['origins']and x['evidence'][:len(old['evidence'])]==old['evidence']
 for k in ('disposition','evidenceStatus','caveat'):ok=ok and x[k]==old[k]
 payloadproof.append({'id':x['id'],'old_version':x['expectedVersion'],'new_version':x['expectedVersion']+1,'old_data_prefix_and_other_fields_preserved':ok,'old_evidence_order':old['evidence'],'origins_exact':old['origins']})
 if not ok:errors.append({'payload_difference':x['id']})
protected=[]
for r in b.execute('select * from current_revision'):
 if r['object_id']in revised:continue
 if r['kind']in ('person','relation','fact','identity','identity_resolution')or r['object_id'].startswith(('IDENTITY-REVIEW','TREE-EFFECT','LIFE-','CONTRACT-'))or r['evidence_status']=='OWNER_CONFIRMED':
  a=s.execute('select * from current_revision where object_id=?',(r['object_id'],)).fetchone();ok=tuple(a)==tuple(r);protected.append({'id':r['object_id'],'version':r['version'],'kind':r['kind'],'exact':ok})
  if not ok:errors.append({'protected_changed':r['object_id']})
pending=s.execute('select count(*) from review_request q where not exists(select 1 from review_resolution r where r.request_id=q.id)').fetchone()[0]
if pending:errors.append({'pending':pending})
result={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':not errors,'errors':errors,'baseline_sha256':sha(B/'clone/baseline.sqlite'),'stage_sha256':sha(B/'clone/final-stage.sqlite'),'live_sha256':sha(ROOT/'genealogy2/data/research.sqlite'),'baseline_journal':b.execute('select max(sequence)from operation_payload').fetchone()[0],'stage_journal':s.execute('select max(sequence)from operation_payload').fetchone()[0],'pending':pending,'operations':[{'path':str((B/n).relative_to(ROOT)),'sha256':sha(B/n)}for n in ('operation-v1.json','retain-resolutions-v2.json')],'derived_FTS_excluded':'object_search* intentionally rebuilds touched current heads; not immutable domain/ledger. All other baseline table rows compared exactly.','tables':tableproof,'head_changes':diff,'new_heads':sorted(newids),'untouched_head_count':len(bh)-len(revised),'protected_count':len(protected),'protected':protected,'payloads':payloadproof,'scope':{'parts':2,'person_folios':1,'originals_downloaded':6,'reused_endpoint_records':['C-0910','C-1047']}}
(B/'stage-proof-v2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k]for k in ('pass','errors','baseline_sha256','stage_sha256','stage_journal','pending','untouched_head_count','protected_count')},indent=2))
