"""Read-only C-0028 native and frozen-citation inventory; never opens the image."""
import hashlib
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DB = ROOT / 'genealogy2/data/research.sqlite'
SCOPE = HERE / 'scope-proposed-j180-20260924.json'
OUT = HERE / 'c0028-documentary-inventory-proposed-j186-20260925.json'
ASSET = 'genealogy/media/C-0028-riksarkivet-SE-ULA-10422-C8-bild-37-sida-34.jpg'
CITATION = 'genealogy/citations/C-0028-maj-amalia-originalfodelse-1920.md'
RECORD_ID = 'R-C0028-15'
SOURCE_ID = 'S-0024'
EXPECTED_ASSET_SHA = 'd01488e2690492835c2dbb0f6f1a8a8f63111a00dcc57b9de3f23d2fa53426b0'
TERMS = ('C-0028', 'C0028', 'R-C0028-15', '1881-03-20', '1881-05-30')

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

scope = json.loads(SCOPE.read_text())
conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
def rows(sql, args=()):
    return [dict(x) for x in conn.execute(sql, args)]
def head(oid):
    found = rows('SELECT * FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1', (oid,))
    assert len(found) == 1, oid
    return found[0]
def full(oid):
    revision = head(oid)
    kind_rows = rows('SELECT kind FROM object WHERE id=?', (oid,))
    assert len(kind_rows) == 1
    kind = kind_rows[0]['kind']
    data = rows(f'SELECT * FROM {kind} WHERE revision_id=?', (revision['id'],))
    assert len(data) == 1
    data = data[0]
    data.pop('revision_id')
    for key, value in tuple(data.items()):
        if key.endswith('_json') and value is not None:
            data[key] = json.loads(value)
    origins = rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id', (revision['id'],))
    evidence = rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role', (revision['id'],))
    item = {'object_id':oid,'kind':kind,'revision':revision,'data':data,'origins':origins,'evidence':evidence}
    if kind == 'record':
        item['imported_media_bindings'] = rows('''SELECT ra.asset_path,ra.region,a.sha256,a.bytes,a.frozen,a.batch_id
          FROM record_asset ra JOIN asset a ON a.path=ra.asset_path WHERE ra.revision_id=? ORDER BY ra.asset_path''', (revision['id'],))
        item['native_media_bindings'] = rows('''SELECT rm.asset_id,rm.region,na.storage_path,na.sha256,na.bytes,na.provenance
          FROM record_media rm JOIN native_asset na ON na.id=rm.asset_id WHERE rm.revision_id=? ORDER BY rm.asset_id''', (revision['id'],))
    return item

record = full(RECORD_ID)
source = full(SOURCE_ID)
assert record['revision']['id'] == 'R-C0028-15@1'
assert record['data']['source_id'] == SOURCE_ID
assert any(x['asset_path'] == ASSET for x in record['imported_media_bindings'])
scope_records = [x for x in scope['current']['records'] if x['object_id'] == RECORD_ID]
assert len(scope_records) == 1 and scope_records[0]['prep_head_id'] == record['revision']['id']
scope_asset = [x for x in scope['current']['owned_imported_assets'] if x['path'] == ASSET]
assert len(scope_asset) == 1 and scope_asset[0]['sha256_current'] == EXPECTED_ASSET_SHA
scope_citation = [x for x in scope['current']['citations'] if x['id'] == 'C-0028']
assert len(scope_citation) == 1 and scope_citation[0]['path'] == CITATION

heads = {r['object_id']:r['id'] for r in rows('''SELECT r.object_id,r.id FROM revision r
  JOIN (SELECT object_id,max(version) version FROM revision GROUP BY object_id) h
  ON h.object_id=r.object_id AND h.version=r.version''')}
record_revision = record['revision']['id']
direct_all = rows('''SELECT d.revision_id,d.role,d.note,r.object_id,o.kind
  FROM dependency d JOIN revision r ON r.id=d.revision_id JOIN object o ON o.id=r.object_id
  WHERE d.basis_revision_id=? ORDER BY r.object_id''', (record_revision,))
direct_current = [x for x in direct_all if heads[x['object_id']] == x['revision_id']]
direct_historical = [x for x in direct_all if heads[x['object_id']] != x['revision_id']]
linked = {}
for kind in ('transcription','mention','observation'):
    for x in rows(f'SELECT revision_id FROM {kind} WHERE record_id=? ORDER BY revision_id', (RECORD_ID,)):
        rid = x['revision_id']
        oid = rid.rsplit('@',1)[0]
        if heads[oid] == rid:
            linked[oid] = full(oid)
read_ids = {x['object_id'] for x in direct_current if x['object_id'].startswith('READ-')}
for oid in read_ids:
    linked[oid] = full(oid)
direct_objects = {x['object_id']:full(x['object_id']) for x in direct_current}

person_ids = ['P-0007','P-0015','P-0016']
person_heads = {pid:full(pid) for pid in person_ids}
research = {}
cross_person_research_refs = []
for kind in ('assessment','question','narrative','fact'):
    for oid,rid in sorted(heads.items()):
        if not oid.startswith(('ASSESSMENT-','AUDIT-','CONTRACT-','KEY-','PATH-','READ-','RESEARCH-','THEME-','P-','BIO-','F-')):
            continue
        if rows('SELECT kind FROM object WHERE id=?',(oid,))[0]['kind'] != kind:
            continue
        item = full(oid)
        textual = json.dumps({'revision':item['revision'],'data':item['data']},ensure_ascii=False)
        matches = [term for term in TERMS if term in textual]
        if not matches:
            continue
        subject = item['data'].get('subject_id')
        own_pid = subject if subject in person_ids else next((pid for pid in person_ids if oid.startswith((f'{kind.upper()}-{pid}',f'BIO-{pid}',f'F-{pid}',f'KEY-{pid}',f'PATH-{pid}',f'RESEARCH-{pid}',f'THEME-{pid}',f'{pid}/'))),None)
        if own_pid is not None:
            research[oid] = {'matched_terms':matches,'own_person_id':own_pid,'full':item}
        else:
            cross_person_research_refs.append({'object_id':oid,'revision_id':rid,'kind':kind,'matched_terms':matches,'subject_id':subject})

asset_path = ROOT / ASSET
citation_path = ROOT / CITATION
asset_stat = asset_path.stat()
asset_sha = sha(asset_path)  # bytes only; no image decoding or display
assert asset_sha == EXPECTED_ASSET_SHA
assert asset_stat.st_size == scope_asset[0]['bytes']
citation_bytes = citation_path.read_bytes()
doc_rows = rows('SELECT * FROM document WHERE path=?',(CITATION,))
assert len(doc_rows) == 1
assert hashlib.sha256(citation_bytes).hexdigest() == doc_rows[0]['sha256']
assert citation_bytes.decode('utf-8') == doc_rows[0]['text']
units = rows('SELECT * FROM unit WHERE document_path=? ORDER BY start_byte,end_byte,id',(CITATION,))
for x in units:
    x['parsed_json'] = json.loads(x['parsed_json'])
decision_units = {}
for item in [record,source,*direct_objects.values(),*linked.values(),*person_heads.values(),*(x['full'] for x in research.values())]:
    for o in item['origins']:
        decision_units[o['unit_id']] = True
unit_decisions = rows('''SELECT ud.* FROM unit_decision ud JOIN
  (SELECT unit_id,max(version) version FROM unit_decision GROUP BY unit_id) h
  ON h.unit_id=ud.unit_id AND h.version=ud.version
  WHERE ud.unit_id IN (SELECT id FROM unit WHERE document_path=?) ORDER BY ud.unit_id''',(CITATION,))

head_file = sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1].name
assert head_file.startswith('000000186-')
pending = rows('''SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id
  WHERE rs.request_id IS NULL''')
assert not pending
out = {
  'task':'T-0677','state':'PROPOSED_READ_ONLY_DOCUMENTARY_INVENTORY_NO_ASSESSMENT',
  'canonical_head_file':head_file,'canonical_pending':0,
  'scope_input':{'path':str(SCOPE.relative_to(ROOT)),'sha256':sha(SCOPE),'baseline_head':scope['journal_head'],
    'record_binding':scope_records[0],'citation_binding':scope_citation[0],'asset_binding':scope_asset[0]},
  'selection_rule':{'record_id':RECORD_ID,'source_id':SOURCE_ID,'relevant_person_ids':person_ids,
    'research_terms':list(TERMS),'research_kinds':['assessment','question','narrative','fact'],
    'direct_dependents':'all current revisions with dependency basis R-C0028-15@1',
    'linked_objects':'current transcription/mention/observation rows whose record_id is R-C0028-15, plus current directly dependent READ',
    'no_image_decode_or_display':True,'no_C0020_C0083_image_access':True},
  'source_record':record,'source':source,
  'linked_record_objects':[linked[k] for k in sorted(linked)],
  'direct_current_dependents':{'edges':direct_current,'objects':[direct_objects[k] for k in sorted(direct_objects)]},
  'historical_nonhead_direct_edges':direct_historical,
  'relevant_person_heads':[person_heads[k] for k in person_ids],
  'matching_own_current_research':[research[k] for k in sorted(research)],
  'other_current_research_text_matches_metadata_only':cross_person_research_refs,
  'citation_provenance':{'path':CITATION,'bytes':len(citation_bytes),'sha256':hashlib.sha256(citation_bytes).hexdigest(),
    'imported_document':doc_rows[0],'raw_text':citation_bytes.decode('utf-8'),
    'units':units,'current_unit_decisions':unit_decisions},
  'owned_asset_hash_only':{'path':ASSET,'bytes':asset_stat.st_size,'sha256':asset_sha,
    'expected_sha256':EXPECTED_ASSET_SHA,'matches_expected':True,
    'asset_table':rows('SELECT * FROM asset WHERE path=?',(ASSET,))},
  'counts':{'direct_current_dependents':len(direct_current),'historical_nonhead_direct_edges':len(direct_historical),
    'linked_transcriptions':sum(x['kind']=='transcription' for x in linked.values()),
    'linked_mentions':sum(x['kind']=='mention' for x in linked.values()),
    'linked_observations':sum(x['kind']=='observation' for x in linked.values()),
    'linked_reads':sum(x['object_id'].startswith('READ-') for x in linked.values()),
    'relevant_person_heads':len(person_ids),'matching_own_current_research':len(research),
    'other_current_research_text_matches_metadata_only':len(cross_person_research_refs),
    'citation_units':len(units),'citation_current_unit_decisions':len(unit_decisions)},
  'limits':['Read-only current native extraction and frozen citation text; no documentary adequacy conclusion.',
    'Historical citation text and imported units are provenance, not a new original-image reading.',
    'Direct dependencies and string matches are mechanical selection, not endorsement of claims.']
}
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(OUT.with_suffix(OUT.suffix+'.sha256')).write_text(sha(OUT)+'  '+OUT.name+'\n')
print(json.dumps({'path':str(OUT.relative_to(ROOT)),'sha256':sha(OUT),'counts':out['counts']},ensure_ascii=False))
