import pathlib,json,sqlite3,hashlib
P=pathlib.Path(__file__).resolve().parent;B=P.parent;c=sqlite3.connect(P/'clone/research-pre.sqlite');c.row_factory=sqlite3.Row;ns={'connection':c};exec((P/'native_payload.py').read_text(),ns)
out=[]
for name in ['C-1047-current-source-decisions-v1.json','C-1047-Astrid-current-decisions-v1.json','C-1047-media-extraction-current-decisions-v1.json']:
 path=B/'source-review'/name;s=json.loads(path.read_text())
 for d in s['changes']:
  p=ns['existing'](d['object'],d['version']);f=d['field'];actual=(p if f in p else p['data'])[f];expected=d['before']
  if f.endswith('_json') and isinstance(expected,str):expected=json.loads(expected)
  assert actual==expected,(d['object'],f,'unexpected wholefield match')
  out.append({**d,'old_full_native_payload':p,'source_decision':name,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'disposition':'revise'})
(P/'C1047-settled-individual-field-table-v2.json').write_text(json.dumps({'task':'T-0778','baseline':277,'state':'FIELD_CHECKED_NOT_EXECUTABLE_PACKAGE','fields':out},ensure_ascii=False,indent=2)+'\n')
print(len(out),'exact matched fields;',len(set(d['object'] for d in out)),'objects')
