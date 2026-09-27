"""Read-only current C0032 inventory; hashes asset bytes without decoding image."""
import hashlib,json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];H=ROOT/'genealogy2/verification/T-0677'
DB=ROOT/'genealogy2/data/research.sqlite';c=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);c.row_factory=sqlite3.Row
rows=lambda q,a=():[dict(x) for x in c.execute(q,a)]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
head=sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1].name;assert head.startswith('000000195-'),head
pending=rows('SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id WHERE rs.request_id IS NULL');assert not pending
R='R-05055c1adb1f17278c7a5ec6';RREV=R+'@1';S='S-0027';C='C-0032'
def obj(oid):
 o=rows('SELECT kind FROM object WHERE id=?',(oid,));assert len(o)==1,oid
 rev=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,));assert len(rev)==1
 rev=rev[0];data=rows(f"SELECT * FROM {o[0]['kind']} WHERE revision_id=?",(rev['id'],));assert len(data)==1
 origins=rows('SELECT * FROM origin WHERE revision_id=? ORDER BY unit_id',(rev['id'],))
 ev=rows('SELECT * FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role',(rev['id'],))
 return {'id':oid,'revision':rev,'kind':o[0]['kind'],'data':data[0],'origins':origins,'evidence':ev}
robj=obj(R);assert robj['revision']['id']==RREV and robj['data']['source_id']==S
media=rows('SELECT * FROM record_asset WHERE revision_id=?',(RREV,))
assert len(media)==1,media
assetpath=media[0]['asset_path'];f=ROOT/assetpath;assert f.is_file()
assetdb=rows('SELECT * FROM asset WHERE path=?',(assetpath,));assert len(assetdb)==1
asset={'path':assetpath,'sha256':sha(f),'bytes':f.stat().st_size,'db':assetdb[0],'record_asset':media[0],'displayed_or_decoded':False}
assert asset['sha256']==assetdb[0]['sha256'] and asset['bytes']==assetdb[0]['bytes']
all_same=[]
for x in rows('SELECT * FROM record_asset WHERE asset_path=?',(assetpath,)):
 rid=x['revision_id'];oid=rid.rsplit('@',1)[0]
 latest=rows('SELECT id FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))[0]['id']
 all_same.append({'record_id':oid,'revision_id':rid,'current':rid==latest,'binding':x})
cur_scope=json.loads((H/'scope-proposed-j180-20260924.json').read_text())['current']
scope_recs=cur_scope['records'];
if isinstance(scope_recs,list):scope_ids={x if isinstance(x,str) else x.get('object_id',x.get('id',x.get('record_id'))) for x in scope_recs}
else:scope_ids=set(scope_recs)
for x in all_same:x['T0677_locked_scope_member']=x['record_id'] in scope_ids
citationpath='genealogy/citations/C-0032-arne-forsamlingsbok-sida-1084.md';citefile=ROOT/citationpath
citation={'path':citationpath,'sha256':sha(citefile),'text':citefile.read_text(),'document':rows('SELECT * FROM document WHERE path=?',(citationpath,)),'units':rows('SELECT * FROM unit WHERE document_path=? ORDER BY start_byte,id',(citationpath,))}
assert len(citation['document'])==1 and citation['document'][0]['sha256']==citation['sha256']
direct=rows('SELECT * FROM dependency WHERE basis_revision_id=? ORDER BY revision_id',(RREV,))
linked_ids=set()
for table in ('mention','observation','transcription'):
 linked_ids.update(x['revision_id'].rsplit('@',1)[0] for x in rows(f'SELECT revision_id FROM {table} WHERE record_id=?',(R,)))
linked_ids.update(x['revision_id'].rsplit('@',1)[0] for x in direct if x['revision_id'].startswith(('READ-','TR-','O-','M-')))
research=[];matchterms=('C-0032','C0032','R-05055c1adb1f17278c7a5ec6','s.1084','sida 1084')
for pid in ('P-0003','P-0042','P-0043'):
 for r in rows('SELECT id FROM object WHERE id LIKE ? ORDER BY id',('%'+pid+'%',)):
  oid=r['id']
  if oid==f'CONTRACT-{pid}-PK-05':research.append({'id':oid,'selection':'PK05 current'});continue
  if '/Q-' not in oid and '-KP-' not in oid:continue
  item=obj(oid)
  text=json.dumps(item['data'],ensure_ascii=False)+json.dumps(item['evidence'],ensure_ascii=False)
  if any(term in text for term in matchterms):research.append({'id':oid,'selection':'literal C0032/R/page reference'})
ids={R,S,*linked_ids,*(x['revision_id'].rsplit('@',1)[0] for x in direct),*(x['id'] for x in research)}
objects={oid:obj(oid) for oid in sorted(ids)}
pviews=[]
for pid in ('P-0003','P-0042','P-0043'):
 path=H/f'c0032-current-person-{pid}-j195-20260926.json';raw=json.loads(path.read_text())
 pviews.append({'person_id':pid,'path':str(path.relative_to(ROOT)),'sha256':sha(path),'bytes':path.stat().st_size,'command':f'node genealogy2/cli.mjs person {pid} --full --format json','exit_code':0,'json_top_keys':list(raw)})
report={'task':'T-0677','status':'DOCUMENTARY_CURRENT_INVENTORY_ONLY_NO_SOURCE_ACTIVATION','journal':head,'journal_sha256':sha(ROOT/'genealogy2/journal'/head),'pending':0,'record_id':R,'source_id':S,'citation_id':C,'scope_records_same_asset':[x['record_id'] for x in all_same if x['T0677_locked_scope_member']],'all_current_records_same_asset':[x['record_id'] for x in all_same if x['current']],'same_image_bindings':all_same,'objects':objects,'linked_ids':sorted(linked_ids),'direct_dependencies':direct,'selected_research':research,'selected_research_ids':[x['id'] for x in research],'current_person_views':pviews,'asset':asset,'citation':citation,'cli_inspect_views':[{ 'path':str((H/f'c0032-current-inspect-{kind}-j195-20260926.json').relative_to(ROOT)), 'sha256':sha(H/f'c0032-current-inspect-{kind}-j195-20260926.json'), 'bytes':(H/f'c0032-current-inspect-{kind}-j195-20260926.json').stat().st_size} for kind in ('record','source')], 'counts':{'objects':len(objects),'linked':len(linked_ids),'direct_dependencies':len(direct),'selected_research':len(research),'citation_units':len(citation['units']),'same_image_record_bindings':len(all_same)},'norm_history_metadata':['C-0032 citation text and units preserved including T-0123/T-0129 read history; no adequacy decision.'],'no_image_decode_or_display':True,'no_native_or_Wotan_write':True}
out=H/'c0032-documentary-current-inventory-j195-20260926.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out.relative_to(ROOT)),'sha256':sha(out),'counts':report['counts'],'linked_ids':report['linked_ids'],'selected_research_ids':report['selected_research_ids'],'same_image_records':report['all_current_records_same_asset']}))
