import importlib.util,json,hashlib,datetime
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0820';S=D/'implementation/stage490-sequence-v1'
hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py'
assert hashlib.sha256(hp.read_bytes()).hexdigest()=='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2'
sp=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
a=h.conn(R/'genealogy2/data/research.sqlite');b=h.conn(S/'stage.sqlite')
assert h.state(a)==h.state(b)=={'journal_head':490,'pending':0}
aa=h.all50(a);bb=h.all50(b);assert aa['schema']==bb['schema']
allowed=['T-0820/C0800-exact-continuation-and-current-consequences-v1','T-0820/two-exact-scope-repairs-and20-individual-resolutions-v1']
cols=[r[1]for r in a.execute('pragma table_info(operation)')];ii=cols.index('id');ti=cols.index('recorded_at')
ar=h.rows(a,'operation');br=h.rows(b,'operation');seen=[]
for xs in [ar,br]:
    found=[]
    for row in xs:
        if row[ii]in allowed:found.append(row[ii]);row[ti]='EXACT_NAMED_OPERATION_TIMESTAMP_ONLY'
    assert sorted(found)==sorted(allowed);seen.append(found)
assert h.row_digest(ar,False)==h.row_digest(br,False)
for name in aa['tables']:
    if name!='operation':assert aa['tables'][name]==bb['tables'][name],name
assert aa['ordered_native_arrays']==bb['ordered_native_arrays']
out=D/'root-live-versus-reviewed-final-stage-v1.json';assert not out.exists()
out.write_text(json.dumps({'task':'T-0820','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':h.state(a),'all50_tables_exact_except_two_named_operation_timestamps':True,'ordered_native_arrays_exact':True,'normalized_operation_ids_only':allowed,'live_db_sha256':hashlib.sha256((R/'genealogy2/data/research.sqlite').read_bytes()).hexdigest(),'stage_db_sha256':hashlib.sha256((S/'stage.sqlite').read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
print('Live490/pending0 equals reviewed final stage; only two named recorded_at fields normalized.')
