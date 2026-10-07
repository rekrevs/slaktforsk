import pathlib,json,sqlite3,copy
B=pathlib.Path(__file__).resolve().parent;c=sqlite3.connect(B/'clone/research-pre.sqlite');c.row_factory=sqlite3.Row;ns={'connection':c};exec((B/'native_payload.py').read_text(),ns);cs=[];rows=[]
for d in json.loads((B/'source-review/current-semantic-copy-amendment-v4.json').read_text())['changes']:
 ch=ns['existing'](d['object'],d['expectedVersion']);old=copy.deepcopy(ch)
 for f in d['fields']:
  p=ch if f['field'] in ch else ch['data'];assert p[f['field']]==f['before'],(d['object'],f['field']);p[f['field']]=f['after']
 for e in d.get('append_supports',[]):ch['evidence'].append({**e,'note':e.get('note','T-0778 AC2/5: individuellt avgjord precisering med tidigare accepterat eget stöd.')})
 cs.append(ch);rows.append({'object':d['object'],'version':d['expectedVersion'],'exact_fields':d['fields'],'old_full_payload':old,'new_full_payload':ch,'reason':d.get('reason'),'disposition':'revise','required_support_rebinds':'ASTRA_RESPONSE_PENDING_FOR_AUDIT_AND_PATH'})
x={'id':'T-0778/group-copy-amendment-v4-v1','actor':'Codex Sol mechanical implementation of exact Astra decisions','reason':'T-0778 AC2/5: sju avgjorda aktuella kopieprecisioner, inget nytt original.','dependencyReviewVersion':2,'changes':cs};(B/'group-copy-v4-candidate-operation-v1.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');(B/'group-copy-v4-consequence-table-v1.json').write_text(json.dumps({'task':'T-0778','revisions':rows},ensure_ascii=False,indent=2)+'\n')
