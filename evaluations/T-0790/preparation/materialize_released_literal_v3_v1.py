"""Root released v3 mechanical APIs/table only. No apply/stage/canonical path."""
from pathlib import Path
import json,hashlib,importlib.util,time
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0790/preparation';SOURCE=R/'evaluations/T-0790/source-review/settled-90-dispositions-and-literal-field-decisions-v3.json';SHA='67f02b6574640d933bf89183ac259ff1fba0eb94a7a9fcdb74fdd68541d27070';start=time.monotonic()
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA;v=json.loads(SOURCE.read_text());assert v['task']=='T-0790'
lib=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';assert hashlib.sha256(lib.read_bytes()).hexdigest()=='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2';sp=importlib.util.spec_from_file_location('h',lib);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
bs=json.loads((O/'baseline-state.json').read_text());assert h.sha(R/bs['backup']['path'])==bs['backup']['sha256'];c=h.conn(R/bs['backup']['path']);assert h.state(c)=={'journal_head':454,'pending':0} and h.all50(c)==bs['all50'];assert h.sha(R/'genealogy2/data/research.sqlite')==bs['main']['sha256']
dictionary=json.loads((O/'complete-current-history-support-native.json').read_text())['objects'];heads=dict(c.execute('select object_id,max(version) from revision group by object_id'));changes=[];table=[];proof=[]
for x in v['exact_changes']:
 rid=x['target_revision'];n=dictionary[rid];oid=n['object_id'];assert h.current(c,oid)==rid and n['version']==x['expectedVersion'] and n['kind']==x['kind']
 # Complete ordered native arrays already fixed/captured; h.api does not reread.
 api=h.api(n);api['expectedVersion']=n['version'];oldapi=json.loads(json.dumps(api))
 for f in x['field_changes']:
  key=f['field'];assert key in n['data'] and n['data'][key]==f['old'],('Return Astra: missing/stale literal field',rid,key)
  api['data'][key]=json.loads(f['new']) if key.endswith('_json') and isinstance(f['new'],str) else f['new']
 api['caveat']=n['caveat']+('\n\n' if n['caveat'] else '')+x['amendment_caveat']
 api['evidence']=x['literal_api_evidence']
 for e in api['evidence']:assert heads.get(e['object'])==e['version'],('Return Astra: noncurrent ordered evidence',oid,e,heads.get(e['object']))
 heads[oid]=n['version']+1
 assert api['origins']==oldapi['origins'] and api['rationale']==oldapi['rationale'] and api['disposition']==oldapi['disposition'] and api['evidenceStatus']==oldapi['evidenceStatus']
 alloweddata={f['field'] for f in x['field_changes']};assert all(api['data'][k]==val for k,val in oldapi['data'].items() if k not in alloweddata)
 changes.append(api);table.append({'old_native':n,'old_full_api':oldapi,'new_api':api,'source_disposition':'revise','rationale':x['reason'],'individual_field_consequences':x['field_changes'],'individual_evidence_decisions':x['individual_evidence_decisions'],'amendment_caveat_exact':x['amendment_caveat'],'source_spec_pointer':'/exact_changes/'+str(len(table))});proof.append({'object':oid,'unspecified_fields_metadata_origins_exact':True,'evidence_literal_exact':True})
for x in v['six_life_reviews']:
 assert x['expectedVersion'] is None and x['id'] not in heads and not c.execute('select 1 from object where id=?',(x['id'],)).fetchone()
 for e in x['evidence']:assert heads.get(e['object'])==e['version'],('Return Astra: noncurrent newlife evidence',x['id'],e)
 changes.append(x);table.append({'old_native':None,'new_api':x,'source_disposition':'create','rationale':x['rationale'],'source_spec_pointer':'/six_life_reviews/'+str(len(table)-34)});heads[x['id']]=1
assert len(changes)==40 and len({x['id'] for x in changes})==40
changed={x['id'] for x in changes};retains=[]
for row in v['individual_table']:
 if row['object_id'] in changed:assert row['disposition']=='revise';continue
 assert row['disposition']=='retain';rid=row['final_revision'];n=dictionary[rid];assert h.current(c,row['object_id'])==rid
 retains.append({'revision_id':rid,'old_native':n,'source_disposition':'retain','rationale':row['individual_rationale'],'source_individual_disposition':row})
assert len(retains)==72 and len(v['individual_table'])==90
out=O/'materialized-source-v3-literal-v1';assert not out.exists();out.mkdir()
op={'id':'T0790-existing-material-life-six-v1','actor':'Codex/Sol-mechanical-from-source-v3','reason':'T-0790 AC1–4: sex personers befintligmaterial-livsbild; individuella90 PK/temadispositioner,34 källrollsbeslutade fälträttelser och6 native livsgranskningar. Inga nya original/kataloger. Exakt sourcev3 SHA '+SHA,'dependencyReviewVersion':2,'changes':changes}
op_pin=h.write(out/'operation-literal.json',op);table_pin=h.write(out/'individual-consequence-table.json',{'operation_sha256':op_pin['sha256'],'source_spec_pin':h.pin(SOURCE),'changes':table,'retains':retains,'all90_individual_dispositions':v['individual_table'],'followup':v['bounded_followup'],'literal_spec_mapping':'old_native exact dictionary; full API data decoded JSON; field old match raw native then exact new copied/JSON parsed; caveat existing plus two literal newline bytes if nonempty plus exact amendment_caveat; source literal_api_evidence copied intact;6new APIs byte-value copied;90table supporting versions NOT selfsupport addedges','canonical_or_stage':False})
h.write(out/'mechanical-validation-result.json',{'source_pin':h.pin(SOURCE),'operation_pin':op_pin,'consequence_table_pin':table_pin,'changed_existing':34,'new_life':6,'retains':72,'all_individual':90,'proof':proof,'current_bindings_checked_sequentially':True,'baseline454_all50_and_mainSHA_exact':True,'source_and_independent_exact_hash_approval_required':True,'stage_or_canonical_run':False,'elapsed_monotonic_seconds':time.monotonic()-start})
assert h.sha(R/'genealogy2/data/research.sqlite')==bs['main']['sha256'];print(json.dumps({'operation':op_pin,'table':table_pin,'elapsed_monotonic_seconds':time.monotonic()-start}));c.close()
