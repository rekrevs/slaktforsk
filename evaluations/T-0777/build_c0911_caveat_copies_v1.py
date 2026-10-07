import pathlib,json,sqlite3
B=pathlib.Path(__file__).resolve().parent;c=sqlite3.connect(B/'clone/final-candidate-v3.sqlite');c.row_factory=sqlite3.Row;ns={'connection':c};exec((B/'native_payload.py').read_text(),ns);changes=[]
for d in json.loads((B/'source-review/C-0911-relation-caveat-copies-amendment-v7.json').read_text())['decisions']:
 ch=ns['existing'](d['object'],d['version']);f=d['fields'][0];assert ch['caveat']==f['old_full_field'];ch['caveat']=f['new_full_field']
 for rid in d['append_evidence']:
  oid,v=rid.rsplit('@',1);ch['evidence'].append({'object':oid,'version':int(v),'role':'supports','note':'T-0777 AC3: individuell C0911 egen döds-/änkedagskorrigering; relation och övriga källfält bevaras.'})
 changes.append(ch)
x={'id':'T-0777/C0911-caveat-copies-v1','actor':'Codex Sol mechanical implementation of individual Astra decisions','reason':'T-0777 AC3–4: nio individuellt prövade aktuella relationscaveats; inga ändrade relationsvärden.','dependencyReviewVersion':2,'changes':changes};(B/'C-0911-caveat-copies-candidate-operation-v1.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
