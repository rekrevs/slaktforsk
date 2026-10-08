import json,importlib.util
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0808';S=D/'implementation/stage470-v1';sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(S/'stage.sqlite');b=h.conn(D/'preparation/baseline469.sqlite');assert h.state(c)['journal_head']==470;refs={};out=[]
def register(rid):
 if rid not in refs:refs[rid]=h.native(c,rid)
 return rid
for q in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid'):
 n=h.native(c,q['affected_revision_id']);old=h.native(c,q['changed_revision_id']);cur=h.native(c,h.current(c,old['object_id']));record={'request':dict(q),'affected_full_native':n,'affected_current_id':h.current(c,n['object_id']),'changed_old_full_native':old,'changed_current_full_native':cur,'affected_direct_basis_and_current_stronger':[]}
 for edge in n['evidence']:
  basis=h.native(c,edge['basis_revision_id']);current=h.native(c,h.current(c,basis['object_id']));record['affected_direct_basis_and_current_stronger'].append({'edge':edge,'exact_revision_id':register(basis['id']),'current_stronger_revision_id':register(current['id'])})
 out.append(record)
f=S/'actual-dependency-contexts-full-v1.json';f.write_text(json.dumps({'state':h.state(c),'requests':out,'support_reference_native':list(refs.values()),'note':'Exact actual dependency input only; individual source decisions still required. Full direct basis/current stronger refs are not certified independence.'},ensure_ascii=False,indent=2)+'\n');print('requests',len(out),'basisrefs',len(refs))
