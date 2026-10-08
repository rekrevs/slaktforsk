import json,importlib.util,sqlite3
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0818';S=D/'implementation/stage488-sequence-v1';sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);b=h.conn(D/'preparation/baseline486.sqlite');a=h.conn(S/'stage.sqlite');proof={}
for t in h.all50(b)['tables']:
 if t in h.DERIVED:continue
 sql=b.execute('select sql from sqlite_master where name=?',(t,)).fetchone()[0]
 if 'WITHOUT ROWID' in sql.upper():assert {json.dumps(r)for r in h.rows(b,t)}<={json.dumps(r)for r in h.rows(a,t)},t
 else:
  n=b.execute('select max(rowid) from "'+t+'"').fetchone()[0]
  if n is not None:assert h.rows(b,t,True)==h.rows(a,t,True,n),t
 proof[t]={'old_native_rows_exact':True,'baseline_rows':b.execute('select count(*) from "'+t+'"').fetchone()[0]}
(S/'protected-native-prefix-proof.json').write_text(json.dumps({'all_non_derived_old_rows_exact':True,'tables':proof,'ordered_arrays_exact':list(h.ORDER_TABLES)},indent=2)+'\n');print('PASS',len(proof))
