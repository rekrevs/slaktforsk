import json,importlib.util,hashlib
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0806';S=D/'implementation/stage468-v2';s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
c=h.conn(R/'genealogy2/data/research.sqlite');stage=h.conn(S/'stage.sqlite');assert h.state(c)==h.state(stage)=={'journal_head':468,'pending':0};a=h.all50(c);b=h.all50(stage);assert a['schema']==b['schema'];assert a['ordered_native_arrays']==b['ordered_native_arrays'];proof={}
for t in a['tables']:
 if t!='operation':assert a['tables'][t]==b['tables'][t],t;proof[t]='exact full rows'
 else:
  sr=[dict(x)for x in stage.execute('select * from operation order by id')];ar=[dict(x)for x in c.execute('select * from operation order by id')];oid='T-0806/accepted-identity-two-person-v1';st=next(x['recorded_at']for x in sr if x['id']==oid);rr=next(x for x in ar if x['id']==oid);delta={'stage':st,'actual':rr['recorded_at']};rr['recorded_at']=st;assert ar==sr;proof[t]={'only_exact_operation_recorded_at_normalized':delta}
p=D/'actual-main-stage-comparison-v1.json';assert not p.exists();p.write_text(json.dumps({'passed':True,'state':h.state(c),'all50':proof,'all_ordered_native_arrays_exact':True,'exact81_and236_and_protected_native_included':True,'main_sha256':hashlib.sha256((R/'genealogy2/data/research.sqlite').read_bytes()).hexdigest()},indent=2)+'\n');print('PASS all50 exact, only approved operation timestamp normalization')
