"""Readonly existing468 input locators plus one authorized current447 SQLite backup."""
from pathlib import Path
import json,sqlite3,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('proven',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
M=R/'genealogy2/data/research.sqlite';expected='1b551564c2067226be4083b52ee471c57268d719ad4aaa53b9d2dc2d43275e21';assert h.sha(M)==expected;c=h.conn(M);assert h.state(c)=={'journal_head':447,'pending':0}
db=R/'evaluations/T-0787/preparation/baseline-j447.sqlite';assert not db.exists();dest=sqlite3.connect(db);c.backup(dest);dest.close();b=h.conn(db)
before=h.all50(c);assert h.all50(b)==before and h.state(b)==h.state(c)
prot=json.loads((R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json').read_text())['objects'];assert len(prot)==42
for rid,n in prot.items():assert h.current(b,n['object_id'])==rid and h.native(b,rid)==n
assert h.sha(M)==expected
bp=h.write(R/'evaluations/T-0787/preparation/fresh447-physical-backup-full50-logical-equality-and-protected42-proof-v1.json',{'main_pin':h.pin(M),'baseline_pin':h.pin(db),'actual_state':h.state(c),'all50':before,'all50_logical_schema_rows_BLOB_native_array_order_equal':True,'protected42_exact':True,'root_actual447_handoff_pin':h.pin(R/'evaluations/T-0786/root-controlled-postlogin-one-search-v1/complete-postlogin-one-search-actual447-handoff.json'),'backup_is_preservation_not_stage_or_DB_replace':True,'native_operation_or_Wotan_write':False})
p=O/'complete-bounded-current744-two-person-and-accepted-support-native-inputs-v1.json';assert h.sha(p)=='03e4ecb85c5437a66ffc28418421adeba4d5d2098772497154e191f1317ab14d';j=json.loads(p.read_text());objects=j['objects'];assert len(objects)==468
record='R-ab847c1960d02f28801419b3@1';tr=[rid for rid,n in objects.items() if n['kind']=='transcription' and n['data']['record_id']==record.rsplit('@',1)[0]];read=[rid for rid,n in objects.items() if n['object_id'].startswith('READ-') and any(e['basis_revision_id'] in [record,*tr] for e in n['evidence'])]
sourceids=[record,*tr,*read];rows=[];incoming=[];terms=['C-0973','C0973','744','1942-02-02','9–10','9–13','9-10','9-13'];source_oids={rid.rsplit('@',1)[0] for rid in sourceids}
for rid,n in objects.items():
 if h.current(b,n['object_id'])!=rid:continue
 subject=n['data'].get('subject_id',n['data'].get('person_id'))
 relevant=subject in ['P-0007','P-0017'] or any(person in n['object_id'] for person in ['P-0007','P-0017']) or n['object_id'] in source_oids
 if not relevant:continue
 matches=[]
 for key,val in [('caveat',n['caveat']),*[('data.'+k,v) for k,v in n['data'].items() if k!='revision_id']]:
  if isinstance(val,str):
   found=[t for t in terms if t in val]
   if found:matches.append({'field':key,'matched_literal_terms':found,'whole_exact_field_pointer':'/objects/'+rid.replace('~','~0').replace('/','~1')+'/'+key.replace('.','/')})
 if matches or rid in sourceids or n['object_id'] in ['BIO-P-0007','BIO-P-0017','RESEARCH-P-0007-9d76f0343410','RESEARCH-P-0017-9d76f0343410']:
  assert h.native(b,rid)==n
  pointer='/objects/'+rid.replace('~','~0').replace('/','~1')
  edges=[]
  for er in b.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(rid,)):
   e=dict(er);cr=b.execute('select object_id from revision where id=?',(e['revision_id'],)).fetchone()[0];e['caller_current_revision_id']=h.current(b,cr);e['caller_is_current']=e['caller_current_revision_id']==e['revision_id'];e['existing468_caller_pointer']=('/objects/'+e['revision_id'].replace('~','~0').replace('/','~1')) if e['revision_id'] in objects else None;edges.append(e);incoming.append(e)
  rows.append({'revision_id':rid,'kind':n['kind'],'subject_id':subject,'existing_whole_native_pointer':pointer,'whole_body_pointers':[pointer+'/data/'+key for key in ['body','markdown','text','reading_note'] if key in n['data']],'whole_caveat_pointer':pointer+'/caveat','data_keys':list(n['data']),'matches_relevance_only':matches,'saved_full_native_equal_actual447_backup':True,'incoming_current_basis_edges':edges})
assert h.sha(M)==expected
out=h.write(O/'narrow744-existing468-native-body-caveat-routing-and-incoming-current447-locators-v1.json',{'task':'T-0788','source_input_pin':h.pin(p),'fresh447_baseline_proof_pin':bp,'actual_baseline_state':h.state(b),'R_TR_READ_exact_input_pointers':sourceids,'rows':rows,'incoming':incoming,'own_current_person_view_pins':json.loads((O/'complete-exact744-current444-media-and-accepted-reuse-lock-v1.json').read_text())['whole_person_pins'],'scope':'Existing468 two-person accepted nativeinput only; wholebody/caveat pointers not a new source reading/grade; current flags/equality mechanical. No omitted caller treated as read. SourceAstra judges relevance.','new_broad_native_pool_or_original_read':False,'operations_or_runtime_canonical_Wotan_mutation':False,'counts':{'locator_rows':len(rows),'incoming_edges':len(incoming),'saved_input_objects':468},'usage':'UNKNOWN pending root collector'})
print(json.dumps({'fresh447_backup_proof_pin':bp,'locator_pin':out,'rows':len(rows),'incoming':len(incoming),'R_TR_READ':sourceids}));c.close();b.close()
