import pathlib,json,sqlite3,copy,hashlib
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1];connection=sqlite3.connect(B/'clone/research-pre.sqlite');connection.row_factory=sqlite3.Row;ns={'connection':connection};exec((B/'native_payload.py').read_text(),ns);specs=[]
for n in ['C-1060-current-revisions-v1.json','C-1060-and-group-copy-amendment-v3.json']:
 for d in json.loads((B/'source-review'/n).read_text())['changes']:specs.append((n,d))
changes=[];table=[]
for fn,d in specs:
 ch=ns['existing'](d['object'],d['expectedVersion']);old=copy.deepcopy(ch)
 for f in d['fields']:
  parent=ch if f['field'] in ch else ch['data'];assert parent[f['field']]==f['before'],(d['object'],f['field'],'wholefield mismatch');parent[f['field']]=f['after']
 for e in d.get('append_supports',[]):ch['evidence'].append({**e,'note':e.get('note','T-0778 AC2–4: individuell avgjord käll- och följdprövning.')})
 for e in d.get('approved_rebinds',[]):
  oid,v=e['from'].rsplit('@',1);dst,nv=e['to'].rsplit('@',1);found=[x for x in ch['evidence'] if x['object']==oid and x['version']==int(v)];assert len(found)==1,(d['object'],e,'unexpected match count');found[0].update(object=dst,version=int(nv))
 if d.get('media_instruction'):
  ch['assets']=[{'path':r['asset_path'],'region':r['region']} for r in connection.execute('select * from record_asset where revision_id=?',(d['object']+'@'+str(d['expectedVersion']),))]
  ch['media']=[{'id':r['asset_id'],'region':r['region']} for r in connection.execute('select * from record_media where revision_id=?',(d['object']+'@'+str(d['expectedVersion']),))]+[{'id':d['media_instruction']['attach_asset'],'region':'C-1060 own1884post33full28fields/headers/margins; otherentriesoutside extraction.'}]
 changes.append(ch);table.append({'object':ch['id'],'version':ch['expectedVersion'],'source_spec':fn,'exact_fields':d['fields'],'old_full_payload':old,'new_full_payload':ch,'disposition':d['disposition'],'reason':d['reason'],'approved_rebinds':d.get('approved_rebinds',[])})
meta=[c for c in changes if c['id'] in ['S-0016','R-beaee87a400dd929753d190d']];rest=[c for c in changes if c not in meta]
def op(n,cs,media=None):
 x={'id':'T-0778/'+n,'actor':'Codex Sol mechanical implementation of exact Astra decisions','reason':'T-0778 AC2–4: individuellt avgjorda exakta källfält, metadata och konsekvenser; historik och gränser bevaras.','dependencyReviewVersion':2,'changes':cs}
 if media:x['media']=media
 p=B/(n+'-operation-v1.json');p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
m=json.loads((B/'C-1060-stage-media-v1.json').read_text());op('C1060-metadata',meta,[m]);op('C1060-consequences',rest)
(B/'C-1060-individual-consequence-table-v1.json').write_text(json.dumps({'task':'T-0778','revisions':table,'individual_retains':json.loads((B/'source-review/C-1060-individual-retains-v1.json').read_text()),'structured_data_full':True},ensure_ascii=False,indent=2)+'\n');print('metadata',len(meta),'consequences',len(rest))
