import pathlib,json,sqlite3,copy
P=pathlib.Path(__file__).resolve().parent;B=P.parent;c=sqlite3.connect(P/'clone/research-pre.sqlite');c.row_factory=sqlite3.Row;ns={'connection':c};exec((P/'native_payload.py').read_text(),ns);s=json.loads((B/'source-review/C-1047-current-source-decisions-v1.json').read_text());media=json.loads((B/'C1047-stage-media-v1.json').read_text());changes=[];table=[]
for binding in s['asset_bindings']:
 oid=binding['object'];ch=ns['existing'](oid,binding['version']);old=copy.deepcopy(ch)
 ds=[d for d in s['changes'] if d['object']==oid];assert len(ds)==1;d=ds[0];assert ch[d['field']]==d['before'];ch[d['field']]=d['after']
 ch['assets']=[{'path':r['asset_path'],'region':r['region']} for r in c.execute('select * from record_asset where revision_id=?',(oid+'@1',))]
 ch['media']=[{'id':r['asset_id'],'region':r['region']} for r in c.execute('select * from record_media where revision_id=?',(oid+'@1',))]
 ch['media'].append({'id':media['id'],'region':'C-1047 '+binding['scope']+'; full18columns per ownrow, headers/blanks/margins; other groups separately represented.'})
 changes.append(ch);table.append({'object':oid,'old_full_native_payload':old,'new_full_native_payload':ch,'source_decision':d})
req={'id':'T-0778/C1047-native-media-v1','actor':'Codex Sol exact settled implementation','reason':'T-0778 AC2: two own source records retain complete metadata and S0026@1; preserved exact original attached with source-bound precision.','dependencyReviewVersion':2,'changes':changes,'media':[media]}
(P/'C1047-metadata-operation-v1.json').write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n');(P/'C1047-metadata-consequence-table-v1.json').write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');print('2 complete record revisions assembled')
