"""Readonly exact eight source-spec guards; no operations, source grades or native writes."""
import json,hashlib,sqlite3,importlib.util,datetime,copy
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=R/'evaluations/T-0784';S=B/'source-review/six-native-review-and-three-Maj-copy-exact-source-specification-v3.json';O=B/'exact-nine-source-spec-mechanical-guards-v1'
EXPECTED='4e894f94981d72c7b3460aaf12399a81ad9323e3bd9a43a3946d32f7f9c165c1';MAIN=R/'genealogy2/data/research.sqlite';M='42321e363573c243597aded458e6a10d2d6cd8e4be47da02a227b149bbaed45f'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(Path(p).relative_to(R)),'sha256':sha(p)}
def diff(a,b,path=''):
 if type(a)!=type(b):return [{'field':path,'old':a,'new':b}]
 if isinstance(a,dict):
  out=[]
  for k in a.keys()|b.keys():
   if k not in a or k not in b:out.append({'field':path+'/'+k,'old_present':k in a,'new_present':k in b,'old':a.get(k),'new':b.get(k)})
   else:out+=diff(a[k],b[k],path+'/'+k)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [{'field':path,'old':a,'new':b}]
  return sum((diff(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [{'field':path,'old':a,'new':b}]
assert sha(S)==EXPECTED and sha(MAIN)==M and not O.exists()
helper=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py'
assert sha(helper)=='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2'
z=importlib.util.spec_from_file_location('h',helper);h=importlib.util.module_from_spec(z);z.loader.exec_module(h)
c=h.conn(MAIN);before=h.all50(c);state=h.state(c);assert state=={'journal_head':442,'pending':0}
s=json.loads(S.read_text());specs=s['specifications'];byid={x['object_id']:x for x in specs};order=s['required_order'];assert len(byid)==len(specs)==9 and set(order)==set(byid)
O.mkdir();rows=[];issues=[];newheads={};contexts={}
for pos,oid in enumerate(order):
 x=byid[oid];a=x['full_new_API'];head=c.execute('select * from current_revision where object_id=?',(oid,)).fetchone();n=h.native(c,head['id']) if head else None
 schema=[]
 assert a['id']==oid and a['kind'] in ['assessment','narrative']
 cols=[dict(t) for t in c.execute('pragma table_info('+a['kind']+')') if t['name']!='revision_id'];valid={t['name'] for t in cols}
 if set(a['data'])-valid:schema.append('unknown data field')
 if any(t['notnull'] and a['data'].get(t['name']) is None for t in cols):schema.append('missing required data field')
 if not c.execute('select id from object where id=?',(a['data']['subject_id'],)).fetchone():schema.append('missing subject')
 for origin in a['origins']:
  if not c.execute('select id from unit where id=?',(origin['unit'],)).fetchone():schema.append('missing origin unit')
 if not a.get('rationale','').strip():schema.append('missing rationale')
 oldAPI=None;incoming=[];hist=[]
 if x.get('expected_absent') is True:
  if head is not None:schema.append('expected absent object exists')
  if a['expectedVersion'] is not None:schema.append('CLI absent-head requires expectedVersion:null; supplied '+str(a['expectedVersion']))
  native_equal=api_equal=None
 else:
  assert head is not None
  oldAPI=h.api(n);oldAPI['expectedVersion']=n['version']
  native_equal=n==x['whole_old_native'];api_equal=oldAPI==x['full_old_API']
  if not native_equal:issues.append({'id':oid,'whole_old_native_diff':diff(x['whole_old_native'],n)})
  if not api_equal:issues.append({'id':oid,'whole_old_API_diff':diff(x['full_old_API'],oldAPI)})
  if a['expectedVersion']!=n['version']:schema.append('expected current version mismatch')
  hist=[r[0] for r in c.execute('select id from revision where object_id=? order by version',(oid,))]
  for rid in hist:
   contexts[rid]=h.native(c,rid)
   for edge in c.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(rid,)):
    e=dict(edge);caller=h.native(c,e['revision_id']);contexts[e['revision_id']]=caller;e['caller_is_current']=h.current(c,caller['object_id'])==e['revision_id'];incoming.append(e)
 edges=[]
 for i,e in enumerate(a['evidence']):
  current=c.execute('select id,version from current_revision where object_id=?',(e['object'],)).fetchone();actual=dict(current) if current else None
  planned=newheads.get(e['object']);effective=planned or (actual['version'] if actual else None)
  ok=effective==e['version'];edges.append({'index':i,'edge':e,'actual_current':actual,'prior_ordered_producer_version':planned,'sequential_head_equal':ok})
  if not ok:schema.append('support head mismatch '+e['object'])
  if actual:contexts[actual['id']]=h.native(c,actual['id'])
 if schema:issues.append({'id':oid,'schema_or_head_issues':schema})
 rows.append({'ordered_index':pos,'object_id':oid,'action':x['action'],'source_spec_pointer':'/specifications/'+str(specs.index(x)),'source_disposition':x.get('source_disposition','Exact source-owned new axis API; no Sol grade'),'OLD_native':n,'OLD_API':oldAPI,'NEW_exact_source_API':a,'whole_old_native_equal':native_equal,'whole_old_API_equal':api_equal,'expected_absence':head is None,'all_history_revision_ids':hist,'incoming_all_history':incoming,'current_incoming_count':sum(e['caller_is_current'] for e in incoming),'support_edges':edges,'full_old_new_diff':diff(oldAPI,a) if oldAPI else [{'field':'entire new API','old':None,'new':a}],'explicit_exact_changes':x.get('exact_changes',[]),'source_retains':s['preserve'],'schema_issues':schema})
 newheads[oid]=(head['version'] if head else 0)+1
assert h.all50(c)==before and h.state(c)==state and sha(MAIN)==M and sha(S)==EXPECTED
out={'task':'T-0784','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'STOP_SCHEMA_QUESTIONS_RETURNED_TO_PRIMARY' if issues else 'MECHANICAL_GUARDS_PASS_NOT_SOURCE_OR_RUNTIME_APPROVAL','source_spec_pin':pin(S),'domain_schema_pin':pin(R/'genealogy2/lib/domain.mjs'),'MAIN_pin':pin(MAIN),'actual_state':state,'all50_readonly_unchanged':True,'required_order':order,'counts':{'targets':9,'creates':6,'revisions':3,'incoming_all_history':sum(len(r['incoming_all_history']) for r in rows)},'issues':issues,'rows':rows,'full_relevant_support_and_incoming_native':contexts,'scope':'Mechanical equality/locators only. Source and independent approval remain separate. No operation construction or runtime/Wotan writes.'}
p=O/'exact-nine-individual-full-consequence-and-mechanical-guards-v1.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pin':pin(p),'counts':out['counts'],'issues':issues},ensure_ascii=False))
