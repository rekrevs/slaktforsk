import pathlib,json,sqlite3,copy,collections
P=pathlib.Path(__file__).resolve().parent;B=P.parent;c=sqlite3.connect(P/'clone/c1047-candidate-v1.sqlite');c.row_factory=sqlite3.Row;ns={'connection':c};exec((P/'native_payload.py').read_text(),ns);group=collections.OrderedDict()
for name in ['C-1047-current-source-decisions-v1.json','C-1047-Astrid-current-decisions-v1.json','C-1047-media-extraction-current-decisions-v1.json','C-1047-current-copy-amendment-v4.json']:
 s=json.loads((B/'source-review'/name).read_text())
 for d in s['changes']:
  if d['object'].startswith('R-'):continue
  group.setdefault(d['object'],[]).append({**d,'source_spec':name})
cs=[];rows=[]
def append(ch,ref):
 oid,v=ref.rsplit('@',1)
 if not any(e['object']==oid and e['version']==int(v) for e in ch['evidence']):ch['evidence'].append({'object':oid,'version':int(v),'role':'supports','note':'T-0778 AC2/5: individually approved source-bound current correction.'})
for oid,ds in group.items():
 ch=ns['existing'](oid,ds[0]['version']);old=copy.deepcopy(ch)
 for d in ds:
  assert d['version']==ch['expectedVersion'];f=d['field'];p=ch if f in ch else ch['data'];expected=d['before'];new=d['after']
  if f.endswith('_json'):
   if isinstance(expected,str):expected=json.loads(expected)
   if isinstance(new,str):new=json.loads(new)
  assert p[f]==expected,(oid,f,'exact match failure');p[f]=new
  for ref in d.get('append_supports',[]):append(ch,ref)
 rebind=None
 if oid=='READ-60cae76b5df58a0a53a72ca1' or oid=='O-P-0003-C1047-reference':rebind='R-33b612f0da2f3aa6fc2addc7'
 if oid=='READ-96c6d6c5a5c464427e4caa5e':rebind='R-c81e3c93931ef93d3beb7c4a'
 if rebind:
  matches=[e for e in ch['evidence'] if e['object']==rebind and e['version']==1];assert len(matches)==1,(oid,'unexpected rebind');matches[0]['version']=2
 if oid=='O-P-0003-C1047-reference':append(ch,'AUDIT-T0778-C1047-family@1')
 if oid=='ADOPT-T0677-C0008-P-0003':
  append(ch,'AUDIT-T0778-C1047-family@1');append(ch,'AUDIT-T0677-C0034@1')
 cs.append(ch);rows.append({'object':oid,'old_full_payload':old,'new_full_payload':ch,'exact_decisions':ds,'approved_rebind':rebind})
request={'id':'T-0778/C1047-current-consequences-v1','actor':'Codex Sol exact settled implementation','reason':'T-0778 AC2/5: individual fullfield current consequences, dated history/stronger supports and all unspecified metadata preserved.','dependencyReviewVersion':2,'changes':cs};(P/'C1047-current-consequences-operation-v1.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n');(P/'C1047-current-consequence-table-v1.json').write_text(json.dumps({'task':'T-0778','rows':rows},ensure_ascii=False,indent=2)+'\n');print(len(cs),'complete native revisions')
