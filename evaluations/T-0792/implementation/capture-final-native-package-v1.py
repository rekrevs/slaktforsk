import hashlib,importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0792/implementation';ST=D/'stage464-v1';H=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';s=importlib.util.spec_from_file_location('h',H);h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(ST/'stage.sqlite');assert h.state(c)=={'journal_head':464,'pending':0}
def native(rid):
 n=h.native(c,rid)
 for k,t in [('origins','origin'),('evidence','dependency')]:n[k]=[dict(x)for x in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
ops=[D/'candidate-operation-v2.json',D/'candidate-fourteen-retains-operation-v1.json'];objects={}
for x in json.loads(ops[0].read_text())['changes']:objects[x['id']]=native(h.current(c,x['id']))
tab=json.loads((D/'individual-consequence-table-v2.json').read_text());retains={r['revision_id']:native(r['revision_id'])for r in tab['retains']};reviewretain=json.loads((ST/'fourteen-exact-retains-full-native-and-order-proof.json').read_text())['affected_native_unchanged'];protected={}
for r in c.execute("select r.* from current_revision r left join assessment a on a.revision_id=r.id where r.evidence_status='OWNER_CONFIRMED' or (r.kind='assessment' and a.criteria in ('identity_review/1','tree_effect/1')) order by r.object_id"):protected[r['id']]=native(r['id'])
p=ST/'final-full-targets-retains-protected-native.json';assert not p.exists();p.write_text(json.dumps({'targets':objects,'retains':retains,'individual_review_retains':reviewretain,'protected':protected,'state':h.state(c),'raw_array_order':'Native rowid order; complete evidence/origins for every object; no sorted-inspect substitution'},ensure_ascii=False,indent=2)+'\n');c.close();print(json.dumps({'targets':len(objects),'retains':len(retains),'review_retains':len(reviewretain),'protected':len(protected),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
