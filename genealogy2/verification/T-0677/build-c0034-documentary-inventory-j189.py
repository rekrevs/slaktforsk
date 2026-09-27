"""Read-only C-0034 native/provenance inventory; JPEG header only, no pixels."""
import hashlib
import json
import re
import sqlite3
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
SCOPE=HERE/'scope-proposed-j180-20260924.json'
OUT=HERE/'c0034-documentary-inventory-proposed-j189-20260925.json'
RECORD_ID='R-bbe424c723e313d730a6f028'
SOURCE_ID='S-0028'
CITATION='genealogy/citations/C-0034-arne-maj-vigsel-1938.md'
ASSET='genealogy/media/C-0034-riksarkivet-SE-ULA-10257-EI4-bild-17-sida-14.jpg'
EXPECTED_ASSET_SHA='a2c08811c1a8a4dcde11521c3ed96b4def26b0d31056c1cd318ab5f301731868'
TERMS=('C-0034','R-bbe424c723e313d730a6f028')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(path.read_text())
scope=load(SCOPE)
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(x) for x in conn.execute(sql,args)]
def head(oid):
 x=rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
 assert len(x)==1,oid
 return x[0]
def full(oid):
 rev=head(oid);kind=rows('SELECT kind FROM object WHERE id=?',(oid,))[0]['kind']
 data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rev['id'],));assert len(data)==1
 data=data[0];data.pop('revision_id')
 for k,v in tuple(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origins=rows('''SELECT o.revision_id,o.unit_id,o.coverage,o.note,u.document_path,u.start_line,u.end_line,
   d.sha256 document_sha256 FROM origin o JOIN unit u ON u.id=o.unit_id
   JOIN document d ON d.path=u.document_path WHERE o.revision_id=? ORDER BY o.unit_id''',(rev['id'],))
 evidence=rows('SELECT revision_id,basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role',(rev['id'],))
 item={'object_id':oid,'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}
 if kind=='record':
  item['imported_media_bindings']=rows('''SELECT ra.asset_path,ra.region,a.sha256,a.bytes,a.frozen,a.batch_id
    FROM record_asset ra JOIN asset a ON a.path=ra.asset_path WHERE ra.revision_id=? ORDER BY ra.asset_path''',(rev['id'],))
  item['native_media_bindings']=rows('''SELECT rm.asset_id,rm.region,na.storage_path,na.sha256,na.bytes,na.provenance
    FROM record_media rm JOIN native_asset na ON na.id=rm.asset_id WHERE rm.revision_id=? ORDER BY rm.asset_id''',(rev['id'],))
 return item

record=full(RECORD_ID);source=full(SOURCE_ID)
assert record['revision']['id']==RECORD_ID+'@1' and record['data']['source_id']==SOURCE_ID
scope_record=[x for x in scope['current']['records'] if x['object_id']==RECORD_ID]
scope_citation=[x for x in scope['current']['citations'] if x['id']=='C-0034']
scope_asset=[x for x in scope['current']['owned_imported_assets'] if x['path']==ASSET]
assert len(scope_record)==len(scope_citation)==len(scope_asset)==1
assert scope_record[0]['prep_head_id']==record['revision']['id']
assert scope_citation[0]['path']==CITATION
assert scope_asset[0]['sha256_current']==EXPECTED_ASSET_SHA

heads={r['object_id']:r['id'] for r in rows('''SELECT r.object_id,r.id FROM revision r JOIN
  (SELECT object_id,max(version) version FROM revision GROUP BY object_id) h
  ON h.object_id=r.object_id AND h.version=r.version''')}
direct_all=rows('''SELECT d.revision_id,d.basis_revision_id,d.role,d.note,r.object_id,o.kind
  FROM dependency d JOIN revision r ON r.id=d.revision_id JOIN object o ON o.id=r.object_id
  WHERE d.basis_revision_id=? ORDER BY r.object_id''',(record['revision']['id'],))
direct_current=[x for x in direct_all if heads[x['object_id']]==x['revision_id']]
direct_nonhead=[x for x in direct_all if heads[x['object_id']]!=x['revision_id']]
linked={}
for kind in ('transcription','mention','observation'):
 for x in rows(f'SELECT revision_id FROM {kind} WHERE record_id=? ORDER BY revision_id',(RECORD_ID,)):
  rid=x['revision_id'];oid=rid.rsplit('@',1)[0]
  if heads[oid]==rid:linked[oid]=full(oid)
for x in direct_current:
 if x['object_id'].startswith('READ-'):linked[x['object_id']]=full(x['object_id'])
direct_objects={x['object_id']:full(x['object_id']) for x in direct_current}

qpk={}
for pid in ('P-0003','P-0007'):
 ids=[r['id'] for r in rows('''SELECT id FROM object WHERE id LIKE ? OR id LIKE ? OR id LIKE ? ORDER BY id''',
  (f'{pid}/Q-%',f'CONTRACT-{pid}-PK-%',f'PATH-{pid}-KP-%'))]
 qpk[pid]=[full(oid) for oid in ids]

citation_path=ROOT/CITATION
citation_bytes=citation_path.read_bytes()
doc=rows('SELECT * FROM document WHERE path=?',(CITATION,));assert len(doc)==1
assert hashlib.sha256(citation_bytes).hexdigest()==doc[0]['sha256']
assert citation_bytes.decode('utf-8')==doc[0]['text']
units=rows('SELECT * FROM unit WHERE document_path=? ORDER BY start_byte,end_byte,id',(CITATION,))
for u in units:u['parsed_json']=json.loads(u['parsed_json'])
unit_decisions=rows('''SELECT ud.* FROM unit_decision ud JOIN
  (SELECT unit_id,max(version) version FROM unit_decision GROUP BY unit_id) h
  ON h.unit_id=ud.unit_id AND h.version=ud.version
  WHERE ud.unit_id IN (SELECT id FROM unit WHERE document_path=?) ORDER BY ud.unit_id''',(CITATION,))

asset_path=ROOT/ASSET
assert sha(asset_path)==EXPECTED_ASSET_SHA and asset_path.stat().st_size==scope_asset[0]['bytes']
def jpeg_sof_metadata(path):
 # Parse marker headers only. Do not decode scan/image data or display pixels.
 with path.open('rb') as f:
  assert f.read(2)==b'\xff\xd8'
  while True:
   marker=f.read(1)
   if not marker:break
   if marker!=b'\xff':continue
   while marker==b'\xff':marker=f.read(1)
   if not marker:break
   code=marker[0]
   if code in (0xd9,0xda):break
   if code in (0x01,*range(0xd0,0xd8)):continue
   length=int.from_bytes(f.read(2),'big')
   assert length>=2
   if code in (0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf):
    meta=f.read(6)
    return {'width_pixels':int.from_bytes(meta[3:5],'big'),
      'height_pixels':int.from_bytes(meta[1:3],'big'),
      'precision_bits':meta[0], 'jpeg_sof_marker':hex(code),
      'method':'JPEG SOF header bytes only; no scan data decoded'}
   f.seek(length-2,1)
 return {'width_pixels':None,'height_pixels':None,'method':'No JPEG SOF before scan; no decode attempted'}
dimensions=jpeg_sof_metadata(asset_path)

# Preserve exact earlier-control matches with JSON pointer, scalar hash and a
# bounded literal excerpt; large prior person payloads are not reinterpreted.
prior=[]
prior_files=[ROOT/'genealogy2/verification/T-0110/frame.json']
prior_files += sorted(p for p in (ROOT/'genealogy2/verification/T-0675').glob('*.json')
 if any(term in p.read_text(errors='replace') for term in TERMS))
def walk(value,pointer,matches):
 if isinstance(value,dict):
  for key,v in value.items():walk(v,pointer+'/'+str(key).replace('~','~0').replace('/','~1'),matches)
 elif isinstance(value,list):
  for i,v in enumerate(value):walk(v,pointer+'/'+str(i),matches)
 elif isinstance(value,str):
  for term in TERMS:
   for m in re.finditer(re.escape(term),value):
    lo=max(0,m.start()-180);hi=min(len(value),m.end()+220)
    matches.append({'json_pointer':pointer,'term':term,'offset':m.start(),
      'scalar_sha256':hashlib.sha256(value.encode()).hexdigest(),
      'scalar_length':len(value),'exact_excerpt':value[lo:hi]})
for path in prior_files:
 matches=[];walk(load(path),'',matches)
 if matches:
  prior.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),
                'match_count':len(matches),'matches':matches})
t0110=load(ROOT/'genealogy2/verification/T-0110/frame.json')
t0110_rows=[x for x in t0110['rows'] if x.get('citation')=='C-0034']
assert len(t0110_rows)==1

head_file=sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1]
assert head_file.name.startswith('000000189-')
pending=rows('''SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id
 WHERE rs.request_id IS NULL''')
assert not pending
out={'task':'T-0677','state':'PROPOSED_READ_ONLY_DOCUMENTARY_INVENTORY_NO_ASSESSMENT',
 'canonical_head_file':head_file.name,'canonical_head_sha256':sha(head_file),'canonical_pending':0,
 'scope_input':{'path':str(SCOPE.relative_to(ROOT)),'sha256':sha(SCOPE),
  'baseline_head':scope['journal_head'],'record_binding':scope_record[0],
  'citation_binding':scope_citation[0],'asset_binding':scope_asset[0]},
 'selection_rule':{'record_id':RECORD_ID,'source_id':SOURCE_ID,
  'linked_objects':'current TR/M/O by record_id and directly dependent current READ',
  'direct_dependents':'current heads with explicit dependency basis R@1',
  'q_pk_kp':'all current Q, CONTRACT-PK and PATH-KP heads for P-0003 and P-0007',
  'prior_matches':'exact literal C-0034/R-id matches in T-0110 frame and T-0675 JSON; excerpts only, pointer/hash preserved',
  'no_image_decode_or_display':True},
 'source_record':record,'source':source,
 'linked_record_objects':[linked[k] for k in sorted(linked)],
 'direct_current_dependents':{'edges':direct_current,'objects':[direct_objects[k] for k in sorted(direct_objects)]},
 'historical_nonhead_direct_edges':direct_nonhead,
 'person_q_pk_kp_current_full':qpk,
 'citation_provenance':{'path':CITATION,'bytes':len(citation_bytes),'sha256':hashlib.sha256(citation_bytes).hexdigest(),
  'imported_document':doc[0],'raw_text':citation_bytes.decode('utf-8'),
  'units':units,'current_unit_decisions':unit_decisions},
 'owned_asset_metadata_only':{'path':ASSET,'bytes':asset_path.stat().st_size,'sha256':sha(asset_path),
  'expected_sha256':EXPECTED_ASSET_SHA,'matches_expected':True,
  'jpeg_header_dimensions':dimensions,'asset_table':rows('SELECT * FROM asset WHERE path=?',(ASSET,)),
  'manifest_entry':[x for x in load(ROOT/'genealogy/media-manifest.json')['entries'] if x['path']==ASSET]},
 'prior_T0110_C0034_row_exact':t0110_rows[0],
 'prior_T0110_T0675_literal_matches':prior,
 'uncertain_mapping_flags_for_Astra':[
  'T-0110 frame maps C-0034 to two parent-relation supports; this is recorded as prior routing only, not verified as a direct C-0034 evidence path.',
  'Earlier T-0675 prose cites C-0034 across person and PK/KP texts; literal matches do not establish which fields were visually controlled.'
 ],
 'counts':{'linked_transcriptions':sum(x['kind']=='transcription' for x in linked.values()),
  'linked_reads':sum(x['object_id'].startswith('READ-') for x in linked.values()),
  'linked_mentions':sum(x['kind']=='mention' for x in linked.values()),
  'linked_observations':sum(x['kind']=='observation' for x in linked.values()),
  'direct_current_dependents':len(direct_current),
  'person_q_pk_kp_heads':{pid:len(items) for pid,items in qpk.items()},
  'citation_units':len(units),'citation_current_unit_decisions':len(unit_decisions),
  'prior_match_files':len(prior),'prior_literal_matches':sum(x['match_count'] for x in prior)},
 'limits':['No genealogy conclusion, source activation, original image viewing or native/Wotan write.',
  'JPEG dimensions obtained from header metadata only; no scan/pixel data decoded.',
  'Historical T-0110/T-0675 matches are controls/provenance, not current source support or completed field audit.']}
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(OUT.relative_to(ROOT)),'sha256':sha(OUT),'counts':out['counts'],
  'dimensions':dimensions},ensure_ascii=False))
