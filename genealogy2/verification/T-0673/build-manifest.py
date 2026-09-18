#!/usr/bin/env python3
"""Read-only T-0673 inventory. Output is exclusive-create; never overwrites a lock."""
import argparse
import hashlib
import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()

def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def search_inventory(db):
    """All current searches, with exact provenance and no duplicated body text."""
    def rows(query):
        return [dict(row) for row in db.execute(query)]
    searches = rows("SELECT c.object_id,c.id AS revision_id,c.version,c.disposition,c.evidence_status,c.caveat,s.question_id,s.source_id,s.scope_json,s.outcome,s.body FROM current_revision c JOIN search s ON s.revision_id=c.id ORDER BY c.object_id")
    links = defaultdict(list)
    for a in rows("SELECT c.object_id,o.unit_id,u.document_path,u.historical,'current_origin' AS mapping FROM current_revision c JOIN origin o ON o.revision_id=c.id JOIN unit u ON u.id=o.unit_id WHERE c.kind='search' UNION SELECT c.object_id,t.unit_id,u.document_path,u.historical,'current_unit_target' AS mapping FROM current_revision c JOIN current_unit_target t ON t.target_id=c.object_id JOIN unit u ON u.id=t.unit_id WHERE c.kind='search' ORDER BY object_id,unit_id,mapping"):
        links[a.pop('object_id')].append(a)
    citations = {r['document_path']:r['id'] for r in rows("SELECT id,document_path FROM legacy_entity WHERE kind='citation'")}
    dependencies = defaultdict(list)
    for d in rows("SELECT c.object_id,d.basis_revision_id,b.object_id AS basis_object_id,o.kind AS basis_kind,d.role,d.note FROM current_revision c JOIN dependency d ON d.revision_id=c.id JOIN revision b ON b.id=d.basis_revision_id JOIN object o ON o.id=b.object_id WHERE c.kind='search' ORDER BY c.object_id,d.basis_revision_id,d.role"):
        dependencies[d.pop('object_id')].append(d)
    # Search has no direct media table: expose exact dependency-revision assets,
    # distinguishing historical assets from the current record's assets.
    media = defaultdict(list)
    for m in rows("SELECT a.revision_id,r.object_id,'imported' AS asset_kind,a.asset_path AS asset_id,a.region,CASE WHEN c.id IS NULL THEN 0 ELSE 1 END AS current_record_revision FROM record_asset a JOIN revision r ON r.id=a.revision_id LEFT JOIN current_revision c ON c.id=a.revision_id UNION ALL SELECT a.revision_id,r.object_id,'native' AS asset_kind,a.asset_id,a.region,CASE WHEN c.id IS NULL THEN 0 ELSE 1 END AS current_record_revision FROM record_media a JOIN revision r ON r.id=a.revision_id LEFT JOIN current_revision c ON c.id=a.revision_id ORDER BY revision_id,asset_kind,asset_id"):
        media[m['revision_id']].append(m)
    for s in searches:
        s['stored_search_row_sha256'] = digest({k:s[k] for k in ('revision_id','question_id','source_id','scope_json','outcome','body')})
        s['body_sha256'] = hashlib.sha256(s.pop('body').encode()).hexdigest()
        s['scope'] = json.loads(s.pop('scope_json'))
        s['document_associations'] = links[s['object_id']]
        s['citation_ids'] = sorted({citations[a['document_path']] for a in s['document_associations'] if a['document_path'] in citations})
        s['dependencies'] = dependencies[s['object_id']]
        s['dependency_record_media'] = [m for d in s['dependencies'] for m in media[d['basis_revision_id']]]
        s['no_citation_mapping'] = not s['citation_ids']
        s['no_current_dependency_record_media'] = not any(m['current_record_revision'] for m in s['dependency_record_media'])
        s['no_dependencies'] = not s['dependencies']
        s['media_scope'] = 'Only exact direct dependency revisions with record media; not transitive support or complete media availability. Search has no direct media field.'
    return searches

def build(db_path):
    db = sqlite3.connect(f'{db_path.resolve().as_uri()}?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA query_only=ON')
    db.execute('BEGIN')
    def rows(query):
        return [dict(row) for row in db.execute(query)]
    operations = rows('SELECT sequence, operation.id AS operation_id, request_hash, policy FROM operation LEFT JOIN operation_payload ON operation.id=operation_id ORDER BY sequence,operation.id')
    if len(operations) != 53:
        raise SystemExit('Expected locked 53-operation baseline; use its read-only recovery copy after later changes.')
    current = rows('SELECT * FROM current_revision ORDER BY object_id')
    # Complete logical baseline digest: table boundaries, sorted column names and rows.
    # FTS caches and sqlite internal state are excluded; no full payloads are copied.
    h = hashlib.sha256()
    for table in sorted(r['name'] for r in rows("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'document_search%' AND name NOT LIKE 'object_search%' AND name NOT LIKE 'sqlite_%'")):
        data = rows(f'SELECT * FROM "{table}"')
        h.update(encoded([table, sorted(data, key=lambda row: encoded(row))]))
    docs = {r['path']: r for r in rows('SELECT path,sha256,bytes,text FROM document')}
    entities = rows('SELECT * FROM legacy_entity ORDER BY kind,id')
    citations = {r['id']: dict(r) for r in entities if r['kind'] == 'citation'}
    legacy_sources = {r['id']: dict(r) for r in entities if r['kind'] == 'source'}
    records = rows('SELECT c.object_id,c.id AS revision_id,c.version,c.disposition,c.evidence_status,c.caveat,r.source_id,r.record_type,r.locator,r.dependence_note FROM current_revision c JOIN record r ON r.revision_id=c.id ORDER BY c.object_id')
    sources = rows('SELECT c.object_id,c.id AS revision_id,c.version,c.disposition,c.evidence_status,c.caveat,s.title,s.archive_reference,s.source_class FROM current_revision c JOIN source s ON s.revision_id=c.id ORDER BY c.object_id')
    record_ids = {r['object_id'] for r in records}
    source_ids = {r['object_id'] for r in sources}
    current_ids = {r['id'] for r in current}
    associations = rows("SELECT r.object_id, o.revision_id, u.id AS unit_id,u.document_path,u.historical,'origin' AS mapping FROM origin o JOIN revision r ON r.id=o.revision_id JOIN unit u ON u.id=o.unit_id JOIN object obj ON obj.id=r.object_id WHERE obj.kind IN ('record','source') ORDER BY r.object_id,o.revision_id,u.id")
    associations += rows("SELECT t.target_id AS object_id,NULL AS revision_id,u.id AS unit_id,u.document_path,u.historical,'current_unit_target' AS mapping FROM current_unit_target t JOIN unit u ON u.id=t.unit_id JOIN object o ON o.id=t.target_id WHERE o.kind IN ('record','source') ORDER BY t.target_id,u.id")
    by_doc = {r['document_path']: r['id'] for r in entities if r['kind'] in ('citation','source')}
    obj_citations = defaultdict(set)
    obj_sources = defaultdict(set)
    for a in associations:
        a['current_revision'] = a['revision_id'] in current_ids if a['revision_id'] else None
        a['legacy_id'] = by_doc.get(a['document_path'])
        if a['legacy_id'] in citations:
            obj_citations[a['object_id']].add(a['legacy_id'])
        if a['legacy_id'] in legacy_sources:
            obj_sources[a['object_id']].add(a['legacy_id'])
    citation_other_targets = defaultdict(dict)
    for a in rows("SELECT u.document_path,c.object_id,c.kind FROM origin o JOIN current_revision c ON c.id=o.revision_id JOIN unit u ON u.id=o.unit_id WHERE c.kind NOT IN ('record','source') UNION SELECT u.document_path,c.object_id,c.kind FROM current_unit_target t JOIN current_revision c ON c.object_id=t.target_id JOIN unit u ON u.id=t.unit_id WHERE c.kind NOT IN ('record','source')"):
        cid = by_doc.get(a['document_path'])
        if cid in citations:
            citation_other_targets[cid][a['object_id']] = a['kind']
    media_links = rows("SELECT r.object_id,a.revision_id,'imported' AS asset_kind,a.asset_path AS asset_id,a.region FROM record_asset a JOIN revision r ON r.id=a.revision_id ORDER BY r.object_id,a.revision_id,a.asset_path")
    media_links += rows("SELECT r.object_id,a.revision_id,'native' AS asset_kind,a.asset_id,a.region FROM record_media a JOIN revision r ON r.id=a.revision_id ORDER BY r.object_id,a.revision_id,a.asset_id")
    current_media = defaultdict(list)
    all_media = defaultdict(list)
    for a in media_links:
        a['current_revision'] = a['revision_id'] in current_ids
        all_media[(a['asset_kind'], a['asset_id'])].append(a['revision_id'])
        if a['current_revision']:
            current_media[a['object_id']].append([a['asset_kind'], a['asset_id']])
    assets = rows('SELECT * FROM asset ORDER BY path')
    native_assets = rows('SELECT * FROM native_asset ORDER BY id')
    media_manifest_path = ROOT / 'genealogy/media-manifest.json'
    media_manifest = json.loads(media_manifest_path.read_text())
    media_provenance = {e['path']: e for e in media_manifest['entries']}
    file_issues = []
    for a, kind, path_key, id_key in [(a,'imported','path','path') for a in assets] + [(a,'native','storage_path','id') for a in native_assets]:
        path = ROOT / a[path_key]
        a['file_check'] = 'match' if path.is_file() and path.stat().st_size == a['bytes'] and file_hash(path) == a['sha256'] else 'missing_or_mismatch'
        if a['file_check'] != 'match':
            file_issues.append(a[path_key])
        links = all_media[(kind,a[id_key])]
        a['record_revision_ids'] = sorted(set(links))
        a['has_current_record_link'] = any(x in current_ids for x in links)
        a['historical_only_record_links'] = bool(links) and not a['has_current_record_link']
        a['no_record_links'] = not links
        if kind == 'imported':
            a['inside_legacy_media'] = a['path'].startswith('genealogy/media/')
            a['legacy_provenance'] = {k:v for k,v in media_provenance.get(a['path'],{}).items() if k not in ('path','bytes','sha256')}
    for e in list(citations.values()) + list(legacy_sources.values()):
        doc = docs[e['document_path']]
        e['document_sha256'] = doc['sha256']
        e['document_bytes'] = doc['bytes']
        e['file_matches_import'] = (ROOT/e['document_path']).is_file() and file_hash(ROOT/e['document_path']) == doc['sha256']
        if not e['file_matches_import']:
            file_issues.append(e['document_path'])
        e['explicit_source_id_mentions'] = sorted(set(re.findall(r'\bS-\d{4}\b', doc['text'])))
        e['native_record_ids'] = sorted(r for r in record_ids if e['id'] in obj_citations[r] or e['id'] in obj_sources[r])
        e['native_source_ids'] = sorted(r for r in source_ids if e['id'] in obj_sources[r])
        e['legacy_media_paths'] = sorted(p for p,m in media_provenance.items() if e['document_path'] in m.get('citation_records',[]) + m.get('source_records',[]))
        e['no_native_record_mapping'] = not e['native_record_ids']
        if e['id'] in citations:
            e['other_current_native_targets'] = [{'object_id':oid,'kind':kind} for oid,kind in sorted(citation_other_targets[e['id']].items())]
    asset_sha = {('imported',a['path']):a['sha256'] for a in assets}
    asset_sha.update({('native',a['id']):a['sha256'] for a in native_assets})
    for r in records:
        r['citation_ids'] = sorted(obj_citations[r['object_id']])
        r['legacy_source_ids'] = sorted(obj_sources[r['source_id']])
        r['current_media'] = sorted(current_media[r['object_id']])
        r['no_citation_mapping'] = not r['citation_ids']
        r['possible_citation_ids_from_object_name_only'] = sorted({f'C-{digits}' for digits in re.findall(r'C-?(\d{4})', r['object_id']) if f'C-{digits}' in citations} - set(r['citation_ids']))
        r['no_current_media'] = not r['current_media']
        r['suggested_group_keys'] = ['record:'+r['object_id'], 'source_locator:'+digest([r['source_id'],r['locator']])] + ['image:'+kind+':'+asset for kind,asset in r['current_media']] + sorted({'image_sha256:'+asset_sha[(kind,asset)] for kind,asset in r['current_media']})
    for s in sources:
        s['legacy_source_ids'] = sorted(obj_sources[s['object_id']])
        s['record_ids'] = sorted(r['object_id'] for r in records if r['source_id'] == s['object_id'])
        s['no_current_records'] = not s['record_ids']
    audits = rows("SELECT c.object_id,c.id AS revision_id,a.subject_id,a.criteria,a.outcome FROM current_revision c JOIN assessment a ON a.revision_id=c.id WHERE c.object_id LIKE 'AUDIT-T0110-%' ORDER BY c.object_id")
    fs_c = sorted(str(p.relative_to(ROOT)) for p in (ROOT/'genealogy/citations').glob('C-*.md'))
    fs_s = sorted(str(p.relative_to(ROOT)) for p in (ROOT/'genealogy/sources').glob('S-*.md'))
    fs_m = sorted(str(p.relative_to(ROOT)) for p in (ROOT/'genealogy/media').rglob('*') if p.is_file())
    fs_n = sorted(str(p.relative_to(ROOT)) for p in (ROOT/'genealogy2/media/objects').rglob('*') if p.is_file())
    def compare(a,b):
        return {'left_count':len(a),'right_count':len(b),'left_only': sorted(set(a)-set(b)), 'right_only':sorted(set(b)-set(a))}
    reconciliation = {
        'citation_files_vs_legacy_entities': compare(fs_c,[e['document_path'] for e in citations.values()]),
        'source_files_vs_legacy_entities': compare(fs_s,[e['document_path'] for e in legacy_sources.values()]),
        'media_files_vs_imported_assets': compare(fs_m,[a['path'] for a in assets if a['inside_legacy_media']]),
        'media_files_vs_legacy_media_manifest': compare(fs_m,list(media_provenance)),
        'native_object_files_vs_native_assets': compare(fs_n,[a['storage_path'] for a in native_assets]),
        'file_hash_issues':sorted(file_issues),
        'sql_counts': {table:db.execute(f'SELECT count(*) FROM {table}').fetchone()[0] for table in ('asset','native_asset','operation','record','source')},
    }
    duplicate_hashes = defaultdict(list)
    for a in assets + native_assets:
        duplicate_hashes[a['sha256']].append(a.get('path',a.get('storage_path')))
    result = {
        'schema':'genealogy2-original-revision-manifest/1', 'task':'T-0673',
        'state':'unreviewed_inventory',
        'semantics': {
            'provenance_is_not_support':True, 'membership_is_not_review':True,
            'mapping_scope':'Citation/source document origins across all revisions plus current unit targets; historical mappings remain marked and do not prove present support.',
            'grouping':'Candidate keys only. Shared images/locators do not make records or witnesses independent or identical. source_locator hashes exact source/locator strings, not normalized pages; image_sha256 keys also join byte-identical files at different paths.',
            'legacy_media_provenance':'Frozen media-manifest exact/source_scoped/citation_scoped/unlinked classifications retained without upgrading them to record support.',
            'audits':'T-0110 audit objects identify possible reuse; read exact recorded scope before reuse, never auto-pass the whole citation/image.',
            'baseline_hash':'Canonical sorted contents of all non-FTS user tables, table names included; current_revision metadata digest separately. No DB binary copied.'},
        'baseline':{'operation_count':len(operations),'operations':operations,'logical_database_sha256':h.hexdigest(),'current_revision_count':len(current),'current_revision_metadata_sha256':digest(current),'schema_hash':db.execute("SELECT value FROM meta WHERE key='schema_hash'").fetchone()[0]},
        'searches':search_inventory(db),
        'citations':list(citations.values()), 'legacy_sources':list(legacy_sources.values()), 'records':records,'sources':sources,
        'imported_assets':assets,'native_assets':native_assets,
        'document_object_associations':sorted(associations,key=lambda a:encoded(a)),
        'record_media_associations':sorted(media_links,key=lambda a:encoded(a)),
        'known_T0110_audits':audits,
        'duplicate_content_paths':[{'sha256':sha,'paths':sorted(paths)} for sha,paths in sorted(duplicate_hashes.items()) if len(paths)>1],
        'legacy_media_manifest_sha256':file_hash(media_manifest_path), 'reconciliation':reconciliation,
    }
    result['counts'] = {k:len(result[k]) for k in ('citations','legacy_sources','records','sources','searches','imported_assets','native_assets','document_object_associations','record_media_associations','known_T0110_audits','duplicate_content_paths')}
    result['counts'].update({'records_without_citation':sum(r['no_citation_mapping'] for r in records),'records_without_current_media':sum(r['no_current_media'] for r in records),'citations_without_record':sum(c['no_native_record_mapping'] for c in citations.values()),'imported_assets_outside_media':sum(not a['inside_legacy_media'] for a in assets),'assets_without_any_record_link':sum(a['no_record_links'] for a in assets+native_assets),'assets_with_only_historical_record_links':sum(a['historical_only_record_links'] for a in assets+native_assets)})
    db.rollback()
    db.close()
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',type=Path,default=ROOT/'genealogy2/data/research.sqlite')
    parser.add_argument('--draft-output',type=Path,required=True,help='New draft path only; existing files are never overwritten.')
    args = parser.parse_args()
    if args.draft_output.exists() or 'draft' not in args.draft_output.name:
        parser.error('Output must be a new file with draft in its name; locked manifests cannot be overwritten.')
    result = build(args.db)
    with args.draft_output.open('x') as handle:
        json.dump(result,handle,ensure_ascii=False,sort_keys=True,indent=2)
        handle.write('\n')
    print(json.dumps({'counts':result['counts'],'reconciliation':result['reconciliation'],'output_sha256':file_hash(args.draft_output)},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
