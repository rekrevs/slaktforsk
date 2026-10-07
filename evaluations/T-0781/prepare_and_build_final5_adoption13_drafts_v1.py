"""Final five settled clause + thirteen exact adoption draft guard/build; no runtime path."""
import ast,copy,json,sqlite3,hashlib,datetime
from pathlib import Path
B=Path('evaluations/T-0781'); G=B/'bounded-consequence-inputs-v1'; W=B/'implementation/final-five-and-thirteen-adoption-drafts-v1'
parent=B/'build_settled_core_and_PATH98_drafts_v2.py'; code=parent.read_text().split('assert W.exists();')[0]; exec(compile(code,str(parent),'exec'))
W=B/'implementation/final-five-and-thirteen-adoption-drafts-v1';assert not W.exists();W.mkdir()
prep=B/'prepare_bounded_consequence_inputs_v1.py'; scope={};exec(compile(prep.read_text().split('assert not W.exists();')[0],str(prep),'exec'),scope)
c=scope['conn'](scope['BASE']); live=scope['conn'](scope['MAIN']); native=scope['native'];current=scope['current']
mainpin=pin(scope['MAIN']);assert mainpin['sha256']=='efea4dfa8feec3f2f5bff8167792b01513ebb5689d9d2ec5278983a23ca208b3'
sp=B/'source-review/two-source-five-final-direct-semantic-copy-clause-decisions-v1.json';assert pin(sp)['sha256']=='2e8f89f4f96011323ba7b1c3c4978a7b7669f822010c0108845cf5f5de83f4a9';s=load(sp)
ap=B/'source-review/two-source-thirteen-individual-bounded-adoption-specifications-v1.json';assert pin(ap)['sha256']=='c19697a31cf220de5e1d6bab35c0e0bddcc583368f75ccad8351dd7663b9ef76';a=load(ap)
existing={}
for p in (B/'implementation').rglob('*draft-operation-v1.json'):
 op=load(p)
 for i,x in enumerate(op['changes']):existing.setdefault(x['id'],[]).append({'operation_pin':pin(p),'change_index':i,'payload':x})
rows=[];pool={}
def add(rid):
 if rid not in pool:pool[rid]=native(c,rid);assert pool[rid]==native(live,rid)
 return '/objects/'+rid.replace('~','~0').replace('/','~1')
for x in s['objects']:
 oid=x['object_id'];rid=current(c,oid);add(rid);assert pool[rid]==x['current']
 hs=[r[0] for r in c.execute('select id from revision where object_id=? order by version',(oid,))];edges=[]
 for h in hs:
  add(h)
  for e in c.execute('select rowid as native_edge_rowid,* from dependency where basis_revision_id=? order by rowid',(h,)):
   e=dict(e);add(e['revision_id']);cur=current(c,pool[e['revision_id']]['object_id']);add(cur);edges.append({'edge':e,'affected_current_revision_id':cur,'affected_is_current':cur==e['revision_id']})
 for e in pool[rid]['evidence']:add(e['basis_revision_id'])
 for e in x['edits']:assert (pool[rid]['data'] if e['field'].startswith('data.') else pool[rid])[e['field'].split('.')[-1]]==e['old']
 rows.append({'object_id':oid,'source_row_pointer':'/objects/'+str(s['objects'].index(x)),'complete_current':pool[rid],'ordered_history_revision_ids':hs,'allhistory_incoming':edges,'existing_draft_overlap':existing.get(oid,[]),'exact_oldfields_match':True})
absence=[]
for i,x in enumerate(a['new_objects']):
 oid=x['object_id'];count=c.execute('select count(*) from object where id=?',(oid,)).fetchone()[0];lc=live.execute('select count(*) from object where id=?',(oid,)).fetchone()[0];assert count==lc
 absence.append({'object_id':oid,'source_row_pointer':'/new_objects/'+str(i),'existing_native_object_count':count,'existing_draft_overlap':existing.get(oid,[])})
np=save('five-targets-full-native-current-history-support-incoming-v1.json',{'objects':pool,'order':'all native arrays ORDER BY rowid; data JSON text unchanged','entire_each_native_equals_main425':True})
gp=save('five-current-fields-and-thirteen-absence-exact-guards-v1.json',{'source_five_pin':pin(sp),'source_adoption_pin':pin(ap),'full_native_pin':np,'rows':rows,'new_object_absence_guards':absence,'main_before':mainpin,'mechanical_match_is_not_grade':True})
assert all(not r['allhistory_incoming'] and not r['existing_draft_overlap'] for r in rows),('Incoming/overlap requires Astra',gp)
assert len(rows)==5 and len(absence)==13 and all(r['existing_native_object_count']==0 and not r['existing_draft_overlap'] for r in absence)
protected=load(B/'mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json')['objects'];protected_ids={x['object_id'] for x in protected.values()};assert not protected_ids.intersection([r['object_id'] for r in rows+absence])
cs=[];table=[]
for x in s['objects']:
 old,new=revise(x,x['current']);cs.append(new);table.append({'object_id':x['object_id'],'old_API':old,'new_API':new,'source_exact_edits':x['edits'],'source_reason':x['reason'],'source_preserve':x['preserve'],'source_row_pointer':'/objects/'+str(s['objects'].index(x))})
op1=operation(1,'two-source-final-direct-copy5',cs,pin(sp));op2=operation(2,'two-source-thirteen-bounded-adoptions',[copy.deepcopy(x['new_entire_API']) for x in a['new_objects']],pin(ap))
tp=save('five-full-individual-clause-consequence-and-preservation-table-v1.json',{'source_spec_pin':pin(sp),'guard_pin':gp,'operation_pin':op1,'rows':table,'no_fanout':True,'all_unamended_metadata_arrays_preserved':True})
result=save('final-five-and-thirteen-exact-draft-operation-index-v1.json',{'operation_pins':[op1,op2],'clause_consequence_table_pin':tp,'exact_guards_pin':gp,'adoptions_entire_API_equal_source_rows':True,'producer_order':a['producer_order'],'unique_targets':18,'protected42_intersection':[],'main_after':pin(scope['MAIN']),'stage':'UNRUN','canonical_apply':'UNRUN','global_gates':'PENDING'})
assert pin(scope['MAIN'])==mainpin;c.close();live.close();print(json.dumps({'index_pin':result,'operation_pins':[op1,op2],'guards_pin':gp},indent=2))
