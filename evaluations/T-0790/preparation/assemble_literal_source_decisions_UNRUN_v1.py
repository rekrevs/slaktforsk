"""UNRUN mechanical interface. No source interpretation or prose substitution.
Input shape documented in literal-mechanics-UNRUN-v1.md; root releases input pins.
"""
import argparse,copy,importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
STAGE=R/'evaluations/T-0790/preparation/stage_literal_authorized_v1.py'
def main():
 assert __debug__
 p=argparse.ArgumentParser();p.add_argument('--authorization',required=True,type=Path);p.add_argument('--sha256',required=True);a=p.parse_args()
 s=importlib.util.spec_from_file_location('stage_ro',STAGE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 assert m.sha(a.authorization)==a.sha256
 auth=json.loads(a.authorization.read_text());assert auth['task']=='T-0790' and auth['mode']=='ASSEMBLE_LITERAL_ONLY' and auth['code_sha256']==m.sha(__file__)
 assert m.sha(STAGE)==auth['stage_helper_sha256']
 _,source=m.loadpin(auth['source_decisions_pin']);_,dictionary=m.loadpin(auth['native_dictionary_pin'])
 assert source['settled_literal_decisions'] is True
 assert m.sha(m.LIB)==m.LIB_SHA
 spec=importlib.util.spec_from_file_location('native_ro',m.LIB);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
 _,bs=m.loadpin(auth['baseline_state_pin']);c=h.conn(R/bs['backup']['path']);assert m.sha(m.MAIN)==bs['main']['sha256'] and h.state(c)=={'journal_head':454,'pending':0}
 out=(R/auth['output_path']).resolve();assert out.is_relative_to(R/'evaluations/T-0790/preparation') and not out.exists();out.mkdir()
 changes=[];rows=[];retains=[];seen=set()
 for d in source['decisions']:
  oid=d['object_id'];assert oid not in seen;seen.add(oid);assert d['source_rationale'] and d['disposition'] in ['revise','create','retain']
  if d['disposition']=='create':
   assert not c.execute('select 1 from object where id=?',(oid,)).fetchone();old=None;new=copy.deepcopy(d['complete_new_api']);assert new['id']==oid and new['expectedVersion'] is None
  else:
   rid=d['old_revision_id'];old=m.native(h,c,rid);assert h.current(c,oid)==rid and old['object_id']==oid and old==dictionary['objects'][rid]
   if d['disposition']=='retain':retains.append({'revision_id':rid,'old_native':old,'source_disposition':'retain','rationale':d['source_rationale']});continue
   new=h.api(old);new['expectedVersion']=old['version']
   for f in d['literal_field_changes']:
    keys=f['path'];assert keys and all(isinstance(k,str) for k in keys);v=new
    for k in keys[:-1]:assert isinstance(v,dict) and k in v;v=v[k]
    assert keys[-1] in v and v[keys[-1]]==f['old_value'],('Return to Astra: exact field stale/missing',oid,keys)
    v[keys[-1]]=copy.deepcopy(f['new_value'])
  assert new['id']==oid
  changes.append(new);rows.append({'old_native':old,'new_api':new,'source_disposition':d['disposition'],'rationale':d['source_rationale'],'individual_field_consequences':d.get('literal_field_changes',[]),'source_decision':d})
 assert [x['id'] for x in changes]==auth['ordered_authorized_change_ids']
 op={'id':source['operation_id'],'actor':source['actor'],'reason':source['reason'],'dependencyReviewVersion':2,'changes':changes};assert 'T-0790' in op['reason']
 op_pin=m.save(out/'operation-literal.json',op);table_pin=m.save(out/'individual-consequence-table.json',{'operation_sha256':op_pin['sha256'],'changes':rows,'retains':retains,'source_decisions_pin':auth['source_decisions_pin']})
 m.save(out/'assembler-result.json',{'operation_pin':op_pin,'consequence_table_pin':table_pin,'canonical_changed':False,'source_approval_of_materialized_exact_hashes':'REQUIRED_FROM_BOTH_ASTRA','literal_order_preserved':True});c.close()
if __name__=='__main__':main()
